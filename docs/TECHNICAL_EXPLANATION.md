# Code2Chill Technical Architecture & Viva Explanation Guide

This document provides a comprehensive technical breakdown of Code2Chill's software architecture, request lifecycles, data validation, authentication mechanisms, database migrations, and engineering tradeoffs. It serves as the definitive reference for project defense and technical evaluations.

---

## 1. System Architecture & Request Lifecycle

```
[ Client Browser ]
        │
        │ HTTPS (TLS 1.3 / Port 443)
        ▼
[ Caddy 2 Reverse Proxy ]
  ├── Automatic TLS via ACME (Let's Encrypt / ZeroSSL)
  ├── Security Headers: HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy
  ├── High-performance compression: zstd, gzip
  ├── Serves pre-built React SPA static assets from /srv
  ├── Direct file serving for /media/* (persistent volume, read-only)
  └── Reverse proxies /api/* to internal network
        │
        │ HTTP (Internal Docker bridge network)
        ▼
[ FastAPI Application Server ]
  ├── Execution under non-root user (nobody:nogroup / UID 65534)
  ├── Request timing & structured operational logging middleware
  ├── 32 KiB streaming payload byte cap for public endpoints
  ├── Custom CSRF guard: X-Code2Chill-Admin header enforcement
  ├── Pydantic V2 input validation & schema contracts
  └── Connection pooling with SQLAlchemy (pool_pre_ping=True, pool_timeout=5s)
        │
        │ PostgreSQL wire protocol (Port 5432, internal only)
        ▼
[ PostgreSQL 17 Database Engine ]
  ├── Network isolation (no host port binding)
  ├── Relational schema with strict foreign keys & check constraints
  ├── JSONB published snapshots for zero-join public reads
  └── Persistent Docker volume (postgres-prod-data)
```

### Complete Request-Response Lifecycle
1. **Network Ingress**: The visitor's client initiates a TLS connection to port 443. Caddy terminates TLS using automatic ACME certificates and applies production security headers (including `Strict-Transport-Security: max-age=31536000`).
2. **Static Asset Serving vs. API Routing**: If the path matches static files (`/assets/*`, `/media/*`, `/licenses/*`), Caddy serves them directly from disk with immutable caching headers. If the path matches `/api/*`, Caddy proxies the request to `api:8000`. Any other URL falls back to `/index.html` for client-side React routing.
3. **ASGI Middleware Pipeline**:
   - `monitor_requests`: Records the start timestamp using high-resolution monotonic clock (`time.perf_counter()`), awaits downstream processing, calculates duration in milliseconds, logs structured request details, and intercepts unhandled exceptions to return a clean HTTP 500 without leaking stack traces or database connection strings.
   - `protect_admin_requests`: Enforces `X-Code2Chill-Admin: 1` on all non-safe state-changing admin requests (`POST`, `PUT`, `DELETE`, `PATCH`), rejecting cross-origin submissions with HTTP 403. Sets `Cache-Control: no-store` on all administrative and recruitment responses.
4. **Authoritative Routing & ORM Session**: FastAPI resolves the matching route, executes dependency injection (`request_session`) providing a transactional SQLAlchemy Session from the pool, executes the business logic, and serializes the response via Pydantic models.

---

## 2. End-to-End Data Flow

### A. Public Content Read Flow
```
Visitor opens /events ──► Caddy proxies GET /api/events ──► FastAPI runs SELECT public_snapshot FROM event
                                                                 │
                                                                 ▼
                                                    Computes dynamic registration status
                                                    (OPEN, CLOSED, FULL, ENDED) via campus clock
                                                                 │
                                                                 ▼
                                                    Returns Schedule(upcoming=[...], past=[...])
```
- **Zero-Join Reads**: Public event listings query the pre-generated `public_snapshot` JSONB column. This completely eliminates expensive joins against audit, user, or draft tables during high-traffic surges.
- **Dynamic Clock Evaluation**: Registration status is computed on read by comparing UTC campus dates against `registration_opens_at` and `registration_closes_at`. If the window closes, `registration_url` is automatically stripped from the response payload to prevent stale submissions.

### B. Event Editorial & Publishing Flow
```
Editor saves draft ──► Validates fields ──► Saves to event table (public_snapshot untouched)
                                                    │
                                                    ▼
Editor clicks "Publish" ──► Backend validates business constraints (e.g., valid HTTPS university signup URL)
                                                    │
                                                    ▼
                        Generates immutable public_snapshot JSONB
                                                    │
                                                    ▼
                        Inserts row in audit_record (actor_id, action="publish", target_type="event")
                                                    │
                                                    ▼
                        Commits database transaction (Atomic release)
```
- **Draft Isolation**: Changes made in the editor do not affect the public website until an authorized lead clicks "Publish". If an editor abandons or cancels draft edits, the public snapshot remains intact.
- **Audit Trails**: Every publication, modification, and deletion records an entry in `audit_record` with the actor's account ID, timestamp, and target entity.

### C. Public Recruitment Intake & Anti-Abuse Flow
```
Applicant submits email ──► Rate limit check ──► Generates 6-digit cryptographic code
                                                       │
                                                       ▼
Applicant submits code + form ──► Reads cycle with FOR UPDATE lock
                                                       │
                                                       ▼
                                  Exceeded 5 incorrect attempts? ──► REJECT (Code exhausted)
                                                       │ No
                                  Valid code? ──► Insert application ──► Return unique receipt
```
- **Body Byte Limit**: The endpoint counts incoming bytes and terminates requests exceeding 32 KiB with HTTP 413, defending against memory exhaustion attacks before JSON parsing.
- **Brute Force Lockout**: Email verification codes are protected by an attempt counter. After 5 incorrect submissions, the code is invalidated, requiring the candidate to request a fresh verification token.
- **Concurrency Control**: Cycle verification uses PostgreSQL pessimistic locking (`FOR UPDATE`), preventing race conditions during concurrent applications.

---

## 3. Data Validation Strategy (Defense in Depth)

The platform implements a multi-tiered validation architecture:

| Tier | Enforcement Point | Mechanism | Failure Behavior |
| :--- | :--- | :--- | :--- |
| **Layer 1: Browser** | React inputs | HTML5 validation (`required`, `type="email"`, `maxLength`) + keyboard focus handling. | Client-side visual error messages before request dispatch. |
| **Layer 2: Edge / Stream** | FastAPI request stream | Manual byte counting on chunked requests up to 32 KiB. | HTTP 413 Payload Too Large before parsing. |
| **Layer 3: Schema API** | Pydantic V2 models | Strict type validation, regex email formats, length constraints, HTTPS link schemes. | HTTP 422 Unprocessable Entity with clear, accessible field-level error messages. |
| **Layer 4: Relational DB** | PostgreSQL constraints | Foreign key constraints, `CheckConstraint`, `UNIQUE` indexes, ENUM columns. | Database rejects transaction rollback if bypassed. |

---

## 4. Authentication, Sessions & Security

### Cryptographic Password Hashing
- Uses **Argon2id** via `pwdlib` (`PASSWORD_HASHER`). Argon2id provides memory-hard protection against GPU and ASIC cracking attacks.
- Minimum password length is enforced at 15 characters (up to 256 characters) with mandatory confirmation.

### Session Architecture
- Sessions are stored in the `admin_session` table.
- When an administrator signs in, the backend generates a 256-bit cryptographic token using `secrets.token_urlsafe(32)`.
- The token is hashed with **SHA-256** before database storage. The raw token is delivered to the browser inside an `HttpOnly`, `SameSite=Lax`, `Path=/api/admin` cookie named `c2c_session`.
- If the database is compromised, the stored SHA-256 session digests cannot be reversed into valid session cookies.

### Permission Tiers & Least Privilege
- Three distinct roles: `admin`, `editor`, and `reviewer`.
- Endpoints use FastAPI dependency injection (`event_editor`, `review_account`, `current_account`) to verify permissions on every request.
- Deactivating an account (`active = false`) immediately blocks active sessions on their next request because the session join filters by `AdminAccount.active.is_(True)`.

### CSRF Protection via Custom Request Headers
- The API serves its same-origin frontend.
- All mutating administrative requests require the custom header `X-Code2Chill-Admin: 1`.
- Standard HTML `<form action="...">` submissions from third-party sites cannot attach custom headers without preflight CORS approval, rendering cross-site request forgery attacks ineffective.

---

## 5. Database Migrations & Recovery

### Alembic Migration Architecture
- Migrations are linear, version-controlled scripts located in `backend/migrations/versions/`:
  - `0001_initial_data_model`: Core entities (events, members, projects, audit, admin accounts).
  - `0002_sign_in_attempts`: Authentication brute-force tracking.
  - `0003_recruitment_intake`: Student recruitment cycles and applications.
  - `0004_content_editors`: Site settings and hosted media assets.
  - `0005_export_audit`: Application CSV export audit logging.
  - `0006_code_failures`: Verification code failure counters.
- All migrations execute inside atomic database transactions (`with context.begin_transaction()`). If any DDL operation fails, PostgreSQL rolls back the schema to the exact previous revision.

### Automated Backups & Restoration Verification
- Automated backups use PostgreSQL custom archive format (`pg_dump -Fc`), applying level 9 compression.
- Backups generate SHA-256 checksum files (`.dump.sha256`) to guarantee storage integrity.
- Automated retention policy purges archives older than 14 days (`BACKUP_RETENTION_DAYS`).
- Recovery is verified through an automated drill (`test_recovery.py`) that restores a previous-release archive into an isolated database, applies migrations to head, checks schema drift, and verifies application data continuity.

---

## 6. Key Engineering Tradeoffs

### 1. SPA with Pre-rendered Metadata vs. Full Server-Side Rendering (SSR)
- *Decision*: Built client-side React 19 SPA served by Caddy, with FastAPI providing dynamic metadata injection for social crawlers (`/api/page-head`).
- *Tradeoff*: SSR requires running a persistent Node.js server process in production, increasing RAM consumption and operational maintenance. The SPA approach allows Caddy to serve static assets directly from disk with sub-millisecond response times, while API and database queries are isolated to dynamic routes.

### 2. CSS Compositor Transitions vs. Canvas/SVG Displacement Ink Animations
- *Decision*: Use CSS GPU compositor transforms (`cubic-bezier(0.22, 1, 0.36, 1)`) with `prefers-reduced-motion` compliance.
- *Tradeoff*: Canvas 2D and SVG turbulence filters simulate realistic liquid ink bleeds, but require continuous CPU software rasterization, consuming 25MB–60MB of RAM and dropping frame rates below 30 FPS on mobile devices. The CSS hardware-accelerated transition runs at 60/120 FPS with 0 KB memory overhead.

### 3. PostgreSQL JSONB Public Snapshots vs. On-the-Fly Relational Joins
- *Decision*: Store published content representations in `public_snapshot` JSONB columns alongside normalized draft tables.
- *Tradeoff*: Slight denormalization storage cost (under 500 KB for the entire club archive). In exchange, public traffic queries execute zero relational joins, drafts remain isolated without locking public reads, and published snapshots are immutable against in-progress editor drafts.

### 4. University Portal Handoff vs. Custom In-House Event Booking
- *Decision*: Provide official university portal links (`https://chitkarau.life/events/...`) for event registration.
- *Tradeoff*: The club website does not store individual student attendance records. However, this aligns with university governance policies, eliminates the liability of collecting student IDs or payments, and guarantees seamless access through the official campus portal.

---

## 7. Comprehensive Viva Defense Q&A

### Q1: Why did you choose a multi-container Docker architecture instead of deploying directly on a bare VM?
**Answer:** Docker containers isolate runtime dependencies (Python 3.14, Node built assets, PostgreSQL 17) from the host environment, preventing version conflicts. It enables reproducible environments between local development, CI testing, and production deployment. Most importantly, it allows network isolation: PostgreSQL runs on an internal bridge network with unmapped host ports, completely shielding the database from public network exposure.

### Q2: Why is Caddy used as the reverse proxy instead of Nginx or Traefik?
**Answer:** Caddy handles automatic HTTPS certificate acquisition and renewal natively via Let's Encrypt and ZeroSSL without needing external cron jobs or Certbot containers. It natively supports high-performance `zstd` and `gzip` compression and provides an elegant configuration syntax that simplifies security header enforcement and SPA fallback routing.

### Q3: What is the purpose of the `X-Code2Chill-Admin: 1` header in administrative requests?
**Answer:** It acts as a lightweight, robust CSRF defense for single-page applications. While browsers automatically attach session cookies to cross-origin requests, cross-origin HTML forms and scripts cannot send custom HTTP headers without explicit preflight CORS approval. By requiring this header on all mutating admin requests, unauthorized cross-origin requests are rejected with HTTP 403 before executing business logic.

### Q4: How does the backend prevent brute-force attacks on applicant verification codes?
**Answer:** Each verification challenge has an attempt counter stored in the database. When an applicant submits a code, the backend locks the challenge record using `FOR UPDATE`. If five incorrect attempts are recorded, the challenge is marked exhausted. Further attempts are rejected, requiring the user to request a fresh verification email. Additionally, resending codes is throttled by a cooldown interval.

### Q5: Why are database migrations necessary if SQLAlchemy can create tables automatically with `Base.metadata.create_all()`?
**Answer:** `create_all()` only creates tables that do not exist; it cannot alter existing tables, add columns, modify constraints, or migrate existing data without dropping tables and losing data. Alembic migrations provide version-controlled, incremental, and reversible schema changes that safely evolve the database schema across releases.

### Q6: How does the system handle reduced-motion preferences for accessibility?
**Answer:** The frontend queries `@media (prefers-reduced-motion: reduce)` in CSS. When enabled, transition durations are collapsed to 0.01ms, spatial translations (`translateY`) and scaling transforms are disabled, and UI state changes transition instantaneously with tactile visual feedback (contrast shifts and borders), protecting visitors with vestibular disorders.

### Q7: What is the difference between authentication and authorization in Code2Chill?
**Answer:** Authentication verifies *who* the user is (verifying email and Argon2id password hash, issuing an authenticated session cookie). Authorization determines *what* the authenticated user is allowed to do (checking whether the account role is `admin`, `editor`, or `reviewer` before allowing actions like exporting applications, editing events, or changing site links).

### Q8: Why mount the media volume as read-only (`:ro`) in the Caddy web container?
**Answer:** Following the principle of least privilege: only the Python API service needs write permissions to upload, validate, and store media files; the Caddy web server only needs to read and serve those files to visitors under `/media/*`. Mounting the volume read-only prevents any web server vulnerability from modifying stored media.

### Q9: How do you verify database backup integrity before disaster strikes?
**Answer:** Every backup generated by `backup.py` computes an accompanying SHA-256 checksum manifest. During operational checks or recovery drills, `--verify` checks the bit-level integrity of the dump file against the manifest. Furthermore, automated integration tests (`test_recovery.py`) simulate a complete restore into a clean database and verify data continuity.

### Q10: Why did you limit incoming public request streams to 32 KiB?
**Answer:** Public endpoints accept untrusted data over the internet. Malicious clients can stream gigabytes of junk data without declaring a `Content-Length` header (chunked transfer encoding) to exhaust server memory (Slowloris attack). By counting bytes directly on the incoming stream and cutting off requests at 32 KiB, the server protects memory before Pydantic parses the payload.
