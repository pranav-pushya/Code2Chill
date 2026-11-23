from pathlib import Path
from uuid import uuid4

from alembic import command
from alembic.config import Config
from sqlalchemy import func, inspect, select, text
from sqlalchemy.orm import Session

from app.content_models import Event, Member, Project
from app.database import database_engine
from app.model_base import Base
from app.seed import seed_content


def test_initial_migration_and_seed_round_trip():
    engine = database_engine()
    try:
        with engine.connect() as connection:
            transaction = connection.begin()
            try:
                schema = f"migration_test_{uuid4().hex}"
                connection.execute(text(f'CREATE SCHEMA "{schema}"'))
                connection.execute(text(f'SET LOCAL search_path TO "{schema}"'))
                config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
                config.attributes["connection"] = connection
                assert inspect(connection).get_table_names() == []

                command.upgrade(config, "head")
                assert set(inspect(connection).get_table_names()) == {
                    *Base.metadata.tables,
                    "alembic_version",
                }
                command.check(config)
                with Session(bind=connection, join_transaction_mode="create_savepoint") as session:
                    assert seed_content(session) == {
                        "members": 10,
                        "events": 2,
                        "projects": 2,
                        "demo_events": 0,
                    }
                    event = session.scalar(select(Event).where(Event.slug == "byte-the-vibe"))
                    assert event.public_snapshot["event_date"] == "2026-05-18"
                    assert event.starts_at is None and event.registration_url is None
                    event.title = "Local draft edit"
                    session.flush()

                    assert not any(seed_content(session).values())
                    assert event.title == "Local draft edit"
                    assert event.public_snapshot["title"] == "Byte The Vibe"
                    assert session.scalar(select(func.count()).select_from(Member)) == 10
                    nexus = session.scalar(select(Project).where(Project.slug == "nexus"))
                    assert nexus.event.slug == "domination-the-frontend-challenge"
                    assert len(nexus.credits) == 3

                    assert seed_content(session, include_demo=True)["demo_events"] == 1
                    assert not any(seed_content(session, include_demo=True).values())
                    demo = session.scalar(select(Event).where(Event.is_demo.is_(True)))
                    assert demo.title.startswith("Demo:")
                    assert demo.public_snapshot is None and demo.registration_url is None
                    session.commit()
                command.downgrade(config, "base")
                assert set(inspect(connection).get_table_names()) == {"alembic_version"}
                command.upgrade(config, "head")
                assert set(inspect(connection).get_table_names()) >= set(Base.metadata.tables)
            finally:
                transaction.rollback()
    finally:
        engine.dispose()
