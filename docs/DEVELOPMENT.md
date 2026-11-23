# Code2Chill — Local Development & Setup Guide

This guide details prerequisites, local environment configuration, and execution instructions for developing and running the Code2Chill full-stack application.

---

## 🛠️ Prerequisites

* **Python**: `3.13` or `3.14` (with [`uv`](https://github.com/astral-sh/uv) recommended, or standard `venv`)
* **Node.js**: `22+` with `npm`
* **Docker / Docker Compose**: For local PostgreSQL 17 database service

---

## 1. Database Setup (PostgreSQL)

The local development PostgreSQL container is configured via [backend/compose.yaml](../backend/compose.yaml):

```bash
# Start the PostgreSQL 17 container in the background
docker compose -f backend/compose.yaml up -d
```

The database port binds to `127.0.0.1:55432` by default. Verify its health status:
```bash
docker compose -f backend/compose.yaml ps
```

---

## 2. Backend Setup (FastAPI)

```bash
cd backend

# Create local environment configuration from template
cp .env.example .env

# Set your secure local POSTGRES_PASSWORD in .env
# DATABASE_URL=postgresql+psycopg://code2chill:<password>@127.0.0.1:55432/code2chill

# Install dependencies using uv
uv sync

# Run the API development server
uv run uvicorn app.main:app --reload --port 8000
```

### Verification Endpoints
* **Interactive API Documentation (Swagger)**: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
* **Health Check & Database Connectivity**: [http://localhost:8000/api/health](http://localhost:8000/api/health)
* **OpenAPI Schema**: [http://localhost:8000/api/openapi.json](http://localhost:8000/api/openapi.json)

---

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
uv run ruff check .
uv run ruff format --check .

# Run test suite
uv run pytest
```
