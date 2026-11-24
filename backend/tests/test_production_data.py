from datetime import date
from pathlib import Path
from uuid import uuid4

from alembic import command
from alembic.config import Config
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.content_models import Event, Member, Project, RegistrationStatus, SiteSettings
from app.database import database_engine
from app.recruitment_models import Application
from app.seed import ROSTER, seed_content


def test_production_migration_and_clean_data_bootstrap():
    """Verify that migrations and clean production seed load approved content only."""
    engine = database_engine()
    try:
        with engine.connect() as connection:
            transaction = connection.begin()
            try:
                schema = f"prod_data_test_{uuid4().hex}"
                connection.execute(text(f'CREATE SCHEMA "{schema}"'))
                connection.execute(text(f'SET LOCAL search_path TO "{schema}"'))

                config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
                config.attributes["connection"] = connection

                # 1. Run migrations to head
                command.upgrade(config, "head")

                with Session(bind=connection, join_transaction_mode="create_savepoint") as session:
                    # 2. Seed production data (clean, no demo records)
                    created = seed_content(session, include_demo=False)
                    assert created == {
                        "members": 10,
                        "events": 2,
                        "projects": 2,
                        "demo_events": 0,
                    }

                    # 3. Verify exactly 10 official members
                    members = session.scalars(select(Member).order_by(Member.display_order)).all()
                    assert len(members) == 10
                    assert [m.name for m in members] == [item[1] for item in ROSTER]
                    assert members[0].name == "Lakshay Kalra"
                    assert members[0].role_title == "President"
                    assert members[1].name == "Jiya Arora"
                    assert members[1].role_title == "Vice-president"
                    for m in members:
                        assert m.published_at is not None
                        assert m.public_snapshot is not None
                        assert m.public_snapshot["name"] == m.name

                    # 4. Verify exactly 2 archived events with verified venues
                    events = session.scalars(select(Event).order_by(Event.event_date)).all()
                    assert len(events) == 2
                    assert events[0].slug == "byte-the-vibe"
                    assert events[0].event_date == date(2026, 5, 18)
                    assert events[0].registration_status == RegistrationStatus.ENDED
                    assert events[0].venue == "Pierre Hall, Architecture Block"

                    assert events[1].slug == "domination-the-frontend-challenge"
                    assert events[1].event_date == date(2026, 7, 18)
                    assert events[1].registration_status == RegistrationStatus.ENDED

                    # 5. Verify NO demo records exist in production seed
                    demo_count = session.scalar(
                        select(func.count()).select_from(Event).where(Event.is_demo.is_(True))
                    )
                    assert demo_count == 0

                    # 6. Verify zero applicant records exist in fresh production state
                    app_count = session.scalar(select(func.count()).select_from(Application))
                    assert app_count == 0

                    # 7. Verify projects and attribution
                    projects = session.scalars(select(Project).order_by(Project.id)).all()
                    assert len(projects) == 2
                    assert projects[0].title == "NEXUS"
                    assert projects[0].public_snapshot["credits"] == [
                        "Ayush Sharma",
                        "Arnav Sharma",
                        "Anveer Singh Sandhu",
                    ]
                    assert projects[1].title == "ChronoAtlas – Travel Through Time"
                    assert projects[1].public_snapshot["credits"] == [
                        "Vibhanshu Jain",
                        "Dheraj Sharma",
                    ]

                    # 8. Verify site links (SiteSettings)
                    settings = session.get(SiteSettings, 1)
                    assert settings is not None
                    assert settings.public_snapshot is not None
                    assert (
                        settings.public_snapshot["university"]
                        == "https://chitkarau.life/clubs/code2chill"
                    )

                    # 9. Verify idempotency: re-running seed adds 0 new records
                    second_run = seed_content(session, include_demo=False)
                    assert not any(second_run.values())

            finally:
                transaction.rollback()
                connection.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
    finally:
        engine.dispose()
