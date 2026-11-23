from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import database_engine, request_session
from app.main import app


@pytest.fixture
def api_db():
    engine = database_engine()
    try:
        with engine.connect() as connection, connection.begin() as transaction:
            schema = f"api_test_{uuid4().hex}"
            connection.execute(text(f'CREATE SCHEMA "{schema}"'))
            connection.execute(text(f'SET LOCAL search_path TO "{schema}"'))
            config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
            config.attributes["connection"] = connection
            command.upgrade(config, "head")

            def test_session():
                with Session(connection, join_transaction_mode="create_savepoint") as db:
                    yield db

            app.dependency_overrides[request_session] = test_session
            try:
                with TestClient(app, base_url="https://testserver") as client:
                    yield client, connection
            finally:
                del app.dependency_overrides[request_session]
                transaction.rollback()
    finally:
        engine.dispose()
