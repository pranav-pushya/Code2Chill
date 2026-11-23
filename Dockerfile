FROM node:24-bookworm-slim AS frontend-build
WORKDIR /source/frontend
COPY frontend/package*.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/index.html frontend/tsconfig.json frontend/vite.config.ts ./
COPY frontend/src/ ./src/
COPY docs/design/ /source/docs/design/
RUN npm run build

FROM caddy:2-alpine AS web
COPY backend/Caddyfile /etc/caddy/Caddyfile
COPY --from=frontend-build /source/frontend/dist /srv
COPY docs/design/fonts/*-OFL.txt /srv/licenses/

FROM python:3.14-slim-bookworm AS api
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /srv/backend
RUN pip install --no-cache-dir uv==0.13.9
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --locked --no-dev --no-cache
COPY backend/app ./app
COPY backend/alembic.ini ./
COPY backend/migrations ./migrations
USER 65534:65534
CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
