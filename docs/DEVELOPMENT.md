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

Staging builds the React production bundle and FastAPI runtime into separate images. Caddy serves the frontend and forwards API requests to FastAPI. The staging database has its own volume and is reachable only on the staging network. Use Docker Compose 2.24.4 or newer for the port override.

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
