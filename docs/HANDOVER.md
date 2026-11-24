# Code2Chill Production Handover & Operations Guide

This guide enables authorized club leads and technical administrators to operate, maintain, deploy, and troubleshoot the Code2Chill website independently.

---

## 1. System Architecture

```
Internet (HTTPS :443 / HTTP :80)
            │
            ▼
   ┌─────────────────┐
   │  Caddy (web)    │ ◄── Automated Let's Encrypt / ZeroSSL HTTPS
   └────────┬────────┘     Security headers, zstd/gzip, static assets (/srv)
            │
     ┌──────┴──────────────────────┐
     │ /api/*                      │ /media/* (read-only)
     ▼                             ▼
┌──────────────────┐      ┌─────────────────────────┐
│ FastAPI (api)    │      │ Persistent Media Volume │
│ (non-root 65534) │◄────►│ (media-prod-data)       │
└────────┬─────────┘      └─────────────────────────┘
         │
         │ Internal Docker Network (no host port binding)
         ▼
┌──────────────────┐
│ PostgreSQL 17    │ ◄── Persistent Data Volume (postgres-prod-data)
│ (db)             │
└──────────────────┘
```

- **Reverse Proxy (`web`)**: Caddy 2 container serving built React assets from `/srv`, enforcing HTTP->HTTPS redirection, applying HSTS and security headers, serving `/media/*`, and proxying `/api/*` to `api:8000`.
- **Backend API (`api`)**: Python 3.14 FastAPI service running under non-root user `nobody:nogroup`. Connects internally to PostgreSQL.
- **Database (`db`)**: PostgreSQL 17 container on an isolated internal bridge network (`ports: !reset []`). Accessible only by the `api` container.
- **Persistent Storage**:
  - `postgres-prod-data`: Database files.
  - `caddy-prod-data` / `caddy-prod-config`: TLS certificates and runtime configuration.
  - `media-prod-data`: Uploaded club assets and photography.

---

## 2. Production Deployment

### Prerequisites
- Docker Engine 24+ and Docker Compose 2.24+
- Domain DNS records (`A`/`AAAA`) pointed to the host server IP.

### Step 1: Environment Configuration
Copy the template and fill in required values:
```bash
cp backend/.env.production.example backend/.env.production
chmod 600 backend/.env.production
```

Generate a secure database password:
```bash
openssl rand -hex 24
```
Ensure the following variables are defined in `backend/.env.production`:
- `POSTGRES_PASSWORD`: Strong generated password.
- `PUBLIC_SITE_URL`: Canonical public URL (e.g. `https://code2chill.chitkara.edu.in`).
- `SERVER_NAME`: Domain name matching DNS (e.g. `code2chill.chitkara.edu.in`).
- `PROD_HTTP_PORT`: `80`
- `PROD_HTTPS_PORT`: `443`
- `RECRUITMENT_SMTP_*`: SMTP credentials for applicant verification emails.

### Step 2: Build and Launch Containers
```bash
docker compose --env-file backend/.env.production -f backend/compose.prod.yaml up --build -d
```

Verify all three containers are healthy:
```bash
docker compose --env-file backend/.env.production -f backend/compose.prod.yaml ps
```

### Step 3: Run Database Migrations
```bash
docker compose --env-file backend/.env.production -f backend/compose.prod.yaml run --rm api .venv/bin/alembic upgrade head
```

### Step 4: Seed Approved Production Data
Run seed without demo records:
```bash
docker compose --env-file backend/.env.production -f backend/compose.prod.yaml run --rm api .venv/bin/python -m app.seed
```

### Step 5: Verify Service Health
Run the automated operations probe:
```bash
python backend/scripts/health_monitor.py --url https://code2chill.chitkara.edu.in --json
```

---

## 3. Administrator Onboarding

Staff accounts are managed via the CLI to avoid public account creation endpoints.

### Roles and Permissions
| Role | Capabilities |
| --- | --- |
| `admin` | Full system access: manage staff accounts, open recruitment cycles, export applications to CSV, publish events/projects/members/links. |
| `editor` | Content management: create drafts, edit, and publish events, projects, and team members. |
| `reviewer` | Recruitment screening: review candidate submissions, shortlist or reject applicants, view review audit history. |

### Creating a Staff Account
Run the interactive CLI inside the API container or locally with connection credentials:
```bash
docker compose --env-file backend/.env.production -f backend/compose.prod.yaml run --rm api \
  .venv/bin/python -m app.create_admin --email lead@chitkara.edu.in --role admin
```
The prompt asks for a secure password (minimum 15 characters). Passwords are hashed with Argon2 (`PASSWORD_HASHER`).

### Deactivating an Account
To revoke access immediately without deleting audit trails:
```sql
UPDATE admin_account SET active = false WHERE email = 'former_member@chitkara.edu.in';
```
Deactivating an account immediately terminates active sessions on their next request.

---

## 4. Content Management & Publishing

### Accessing the Dashboard
Navigate to `/admin` in the browser and sign in. All administrative API calls require the custom header `X-Code2Chill-Admin: 1`, preventing cross-site request forgery.

### Publishing an Event
1. Sign in as `admin` or `editor`.
2. Open **Events** and click **New Event Draft**.
3. Fill in the title, confirmed event date, venue, and summary.
4. Set registration status:
   - For open events: provide the approved university registration URL (`https://chitkarau.life/...`).
   - For past events: set status to `ended`.
5. Click **Publish**. The backend generates an immutable `public_snapshot` visible on the public `/events` page.

### Updating Team Leadership
1. Open **Team** in the dashboard.
2. Edit member name, role title, domain, or display order.
3. Click **Publish**.

### Updating Official Social Links
1. Open **Settings** in the dashboard.
2. Update the university portal URL, Instagram URL, or LinkedIn URL.
3. Click **Publish Links**.

---

## 5. Rollback Procedures

### Application / Code Rollback
If an issue occurs in a newly deployed release:
1. Revert to the previous git release commit:
   ```bash
   git checkout <previous_commit_or_tag>
   ```
2. Rebuild and restart containers:
   ```bash
   docker compose --env-file backend/.env.production -f backend/compose.prod.yaml up --build -d
   ```

### Database Migration Rollback
If a database migration needs to be reversed:
```bash
docker compose --env-file backend/.env.production -f backend/compose.prod.yaml run --rm api .venv/bin/alembic downgrade -1
```

### Full Database Disaster Recovery
To restore from a backup:
```bash
# 1. Locate latest verified backup
python backend/scripts/backup.py --list

# 2. Verify backup checksum integrity
python backend/scripts/backup.py --verify backend/backups/code2chill_YYYYMMDD_HHMMSS.dump

# 3. Restore dump into fresh target database or active database
docker compose --env-file backend/.env.production -f backend/compose.prod.yaml exec -T db \
  pg_restore --clean --if-exists --single-transaction --no-owner --no-acl -U code2chill -d code2chill < backend/backups/code2chill_YYYYMMDD_HHMMSS.dump
```

---

## 6. Routine Maintenance & Operations

### Automated Backups
Schedule daily backups via cron:
```bash
0 3 * * * cd /opt/code2chill && python3 backend/scripts/backup.py >> /var/log/c2c_backup.log 2>&1
```
Backups older than `BACKUP_RETENTION_DAYS` (default 14 days) are automatically pruned.

### Log Monitoring
Stream container logs in real time:
```bash
docker compose --env-file backend/.env.production -f backend/compose.prod.yaml logs -f api
docker compose --env-file backend/.env.production -f backend/compose.prod.yaml logs -f web
```
The backend logs request latency in milliseconds (`duration_ms`), HTTP paths, and status codes. Any unhandled 500 error outputs an operational log entry without leaking private submission details.
