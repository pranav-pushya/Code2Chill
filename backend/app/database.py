import os
from pathlib import Path

from dotenv import dotenv_values
from fastapi import Request
from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


def database_engine() -> Engine:
    settings = {**dotenv_values(ENV_FILE), **os.environ}
    url = settings.get("DATABASE_URL")
    if url:
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg://", 1)
        elif url.startswith("postgresql://") and not url.startswith("postgresql+psycopg://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    if not url:
        password = settings.get("POSTGRES_PASSWORD")
        if not password:
            raise RuntimeError(
                "Configure POSTGRES_PASSWORD or DATABASE_URL before starting the API."
            )
        url = URL.create(
            "postgresql+psycopg",
            username="code2chill",
            password=password,
            host=settings.get("DB_HOST", "127.0.0.1"),
            port=int(settings.get("DB_HOST_PORT", "55432")),
            database="code2chill",
        )
    return create_engine(
        url, pool_pre_ping=True, pool_timeout=5, connect_args={"connect_timeout": 3}
    )


def request_session(request: Request):
    with Session(request.app.state.database) as session:
        yield session
