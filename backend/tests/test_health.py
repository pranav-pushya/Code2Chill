from fastapi.testclient import TestClient

from app.main import app


def test_database_ready():
    with TestClient(app) as client:
        response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_database_unreachable(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://unused@127.0.0.1:1/unavailable")
    with TestClient(app) as client:
        response = client.get("/api/health")
    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}
