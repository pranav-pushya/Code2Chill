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
uv run --locked ruff check app tests
uv run --locked ruff format --check app tests

# Run test suite
uv run --locked python -m pytest -q
```

[GitHub Actions](../.github/workflows/ci.yml) runs these checks on pushes and pull requests with a fresh PostgreSQL service. The positive health test requires a reachable database. The failure test directs its own request to an unavailable port.
