# Code2Chill — Local Development & Setup Guide

This guide details prerequisites, local environment configuration, and execution instructions for developing and running the Code2Chill full-stack application.

---

## 🛠️ Prerequisites

* **Python**: `3.13` or `3.14` (with [`uv`](https://github.com/astral-sh/uv) for the locked environment)
* **Node.js**: `24.x` with `npm`
* **Docker / Docker Compose**: For local PostgreSQL 17 database service

---

## 1. Database Setup (PostgreSQL)

The local development PostgreSQL container is configured via [backend/compose.yaml](../backend/compose.yaml):

On first setup, copy `backend/.env.example` to `backend/.env` and set `POSTGRES_PASSWORD` to a unique local password. Reuse that file for this database volume on later starts. Run the following from the repository root.

```bash
# Start PostgreSQL and wait for readiness
docker compose -p code2chill-dev --env-file backend/.env -f backend/compose.yaml up -d --wait db
```

The database port binds to `127.0.0.1:55432` by default. Verify its health status:
```bash
docker compose -p code2chill-dev --env-file backend/.env -f backend/compose.yaml ps
```

---

## 2. Backend Setup (FastAPI)

```bash
cd backend

# Use the configuration created before starting PostgreSQL
uv sync --locked

# Run the API development server
uv run --locked uvicorn app.main:app --reload --port 8000
```


### Initialize the data schema

Run these commands from `backend/` after `uv sync --locked` and after PostgreSQL reports ready.

```sh
uv run --locked alembic upgrade head
uv run --locked python -m app.seed
```

The first command creates the tables. Run it after pulling a schema change. The seed is optional for developers who want an empty schema. Repeat it to insert missing initial content without overwriting edits. To add the labeled practice draft to a development database, add `--include-demo` to the seed command.

### Enable local recruitment on a configured cycle

Apply migration `0003` with the schema command above. Set `RECRUITMENT_SMTP_HOST` and `RECRUITMENT_MAIL_FROM` in the backend environment. The mailer uses SMTP over TLS on port 465 by default. Set the port and any required credentials using the names in the [environment example](../backend/.env.example). For staging, supply the values in the staging Compose environment and recreate the API service.

The seed leaves recruitment unannounced. A published local cycle needs opening and closing times, eligibility, enabled domains, an active assigned reviewer, and the approved lowercase email domain (for example, `campus.example` in a test). Set `optional_field` to `motivation`, `portfolio_url` or leave it empty. Publish the configured cycle through the existing publication helper. Previously published local cycles need an approved email domain and a fresh publication before the application link appears. Cycle configuration currently requires backend access.

Applicants start at `/join`. Verification codes expire after 15 minutes. An applicant who loses the submit response should keep the page open and retry with the same details to recover the confirmation. The form keeps the attempt and entered values in page memory.

### Create a staff account

After applying migrations, run the command below from `backend/` in an interactive terminal. Substitute the staff member's email and choose the role they need. The command prompts twice for a hidden password of 15–256 characters. An existing email keeps its current password and role.

```sh
uv run --locked python -m app.create_admin --email editor@example.org --role editor
```

Start FastAPI and Vite, then open the [admin sign-in page](http://localhost:5173/admin/sign-in). Admins and editors can open **Manage events** and publish events. A reviewer can sign in and see their dashboard. To provision staff in local staging, run the same Python module inside the migrated API container.

Sign-in uses a host-only, Secure, HTTP-only cookie with an eight-hour lifetime. Use `localhost` for local browser development and HTTPS on a deployed hostname. The frontend and API share an origin through the Vite or Caddy proxy. Admin API clients must include `X-Code2Chill-Admin: 1` on POST requests, including sign-in and sign-out. Five consecutive failed password checks pause sign-in for that account for five minutes.

### Review recruitment applications

For recruitment, choose **Review applications** from the staff dashboard. Select a cycle, then filter by domain or status. Open a name to read the application. **Back to applications** restores the filters and page. Administrators can access all local recruitment cycles, and reviewers see cycles assigned to their active account. Editors manage public content.

### Publish an event

1. Open **Manage events** and choose **New draft**, or open an existing event. Enter a title, URL slug and summary. You can save the draft while the date is pending. Enter optional times in India Standard Time.
2. Confirm the event date before publishing. To open registration, choose **Open** and supply the organizer-verified event-specific university URL. The opening and closing times control when the public registration link appears.
3. Choose **Save draft**, then **Preview draft**. Check the event date, registration status and destination. The last published revision stays public while you work.
4. Choose **Publish event**, confirm, and follow **View published page**. If another editor has saved changes since your preview, reload the draft and review their changes before publishing.

The optional seeded practice event stays visible only to staff. Updates to ordinary events appear at `/events` and `/events/<slug>`.

### Verification Endpoints
* **Interactive API Documentation (Swagger)**: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
* **Health Check & Database Connectivity**: [http://localhost:8000/api/health](http://localhost:8000/api/health)
* **OpenAPI Schema**: [http://localhost:8000/api/openapi.json](http://localhost:8000/api/openapi.json)

---

Keep the API running and start the frontend in a second terminal from the repository root.

## 3. Frontend Setup (React + Vite + Tailwind)

```bash
cd frontend

# Install dependencies deterministically
npm ci

# Start the Vite development server with Hot Module Replacement
npm run dev
```

* **Local Web Interface**: [http://localhost:5173](http://localhost:5173)
* **Service Status Route**: [http://localhost:5173/status](http://localhost:5173/status)

### Verify the Vite API proxy

If the admin dashboard says “Couldn’t load this page,” open [the health endpoint through Vite](http://localhost:5173/api/health). It should return HTTP 200 with `{"status":"ok"}`. A 404 there and at `http://127.0.0.1:8000/api/health` indicates that Vite's default port is serving an app without the current health route.

If port 8000 is already in use, start this repository's API from `backend/` with `uv run --locked uvicorn app.main:app --reload --port 8001`. Set `API_PROXY_TARGET=http://127.0.0.1:8001` in `frontend/.env.local` and restart Vite if it hasn't reloaded. Verify the health endpoint through Vite again, then open `/admin` in a signed-out browser to check that it sends you to sign-in.

---

## 4. Quality Checks & Verification

### Frontend Checks
```bash
cd frontend

# Linting with Biome
npm run lint

# Formatting check
npm run format:check

# Production build test
npm run build
```

### Backend Checks
```bash
cd backend

# Run Ruff linter and format check
uv run --locked ruff check app migrations tests
uv run --locked ruff format --check app migrations tests

# Run test suite
uv run --locked python -m pytest -q
```

[GitHub Actions](../.github/workflows/ci.yml) runs these checks on pushes and pull requests with a fresh PostgreSQL service. The positive health test requires a reachable database. The failure test directs its own request to an unavailable port.

## Local staging

Staging builds the React production bundle and FastAPI runtime into separate images. Caddy serves JavaScript, styles, fonts and the branded share image. It forwards page requests to FastAPI, which inserts route-specific metadata into the built HTML. API requests still use the same origin. The staging database has its own volume and is reachable only on the staging network. Use Docker Compose 2.24.4 or newer for the port override.

The default canonical URL uses the request origin. When running the site behind a public HTTPS proxy, set `PUBLIC_SITE_URL` in the Compose environment file to the site's actual public origin, including its scheme. Link previews use the published event or project summary and the club's 1200 × 630 share image. To check a preview, view the page source of a published detail URL and open the URL in its `og:image` tag.

From the repository root, copy the backend environment template to a new file named `backend/.env.staging` on first setup. Give staging its own `POSTGRES_PASSWORD`. Run these commands from the repository root.

~~~sh
docker compose -p code2chill-staging --env-file backend/.env.staging -f backend/compose.yaml -f backend/compose.staging.yaml up --build -d --wait
docker compose -p code2chill-staging --env-file backend/.env.staging -f backend/compose.yaml -f backend/compose.staging.yaml ps
~~~

Open the [staging homepage](http://127.0.0.1:8084/) and follow **Service status**. Refreshing [the status page](http://127.0.0.1:8084/status) loads the application directly. The [readiness endpoint](http://127.0.0.1:8084/api/health) returns HTTP 200 after a successful database query. Set `STAGING_PORT` in the staging environment file if another service owns 8084.

Repeat the build command after changing code. To stop staging while keeping its database volume, run the following.

~~~sh
docker compose -p code2chill-staging --env-file backend/.env.staging -f backend/compose.yaml -f backend/compose.staging.yaml down
~~~

### Initialize the staging database

Run the staging build first, then apply the migration and seed against the staging volume.

```sh
docker compose -p code2chill-staging --env-file backend/.env.staging -f backend/compose.yaml -f backend/compose.staging.yaml run --rm --no-deps api .venv/bin/alembic upgrade head
docker compose -p code2chill-staging --env-file backend/.env.staging -f backend/compose.yaml -f backend/compose.staging.yaml run --rm --no-deps api .venv/bin/python -m app.seed
```
