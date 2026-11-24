import os
import subprocess
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, insert, select, text
from sqlalchemy.orm import Session
from test_admin_recruitment import cycle_with_applicant

from app.content_models import Project
from app.database import database_engine
from app.recruitment_models import Application, EmailChallenge
from app.seed import seed_content


@contextmanager
def empty_database(container, url):
    name = "c2c_recovery_" + uuid4().hex
    docker = ["docker", "exec", container]
    subprocess.run([*docker, "createdb", "-U", url.username, "-T", "template0", name], check=True)
    engine = create_engine(url.set(database=name))
    try:
        yield engine
    finally:
        engine.dispose()
        subprocess.run([*docker, "dropdb", "-U", url.username, name], check=True)


def migration_config(connection):
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    config.attributes["connection"] = connection
    return config


@pytest.mark.skipif(
    not os.getenv("RECOVERY_DB_CONTAINER"), reason="requires PostgreSQL Docker tools"
)
def test_restore_previous_release_and_upgrade():
    container = os.environ["RECOVERY_DB_CONTAINER"]
    configured = database_engine()
    url = configured.url
    configured.dispose()
    with empty_database(container, url) as source, empty_database(container, url) as restored:
        with source.begin() as connection:
            command.upgrade(migration_config(connection), "0005")
            with Session(connection) as db:
                seed_content(db)
                db.commit()
            cycle, application_id = cycle_with_applicant(connection, "recovery", "Test Applicant")
            receipt = connection.scalar(
                select(Application.receipt).where(Application.id == application_id)
            )
            connection.execute(
                insert(EmailChallenge).values(
                    cycle_id=cycle,
                    attempt_id=uuid4(),
                    email="recovery@example.test",
                    digest="0" * 64,
                    sent_at=datetime.now(UTC),
                )
            )

        dump = subprocess.run(
            [
                "docker",
                "exec",
                container,
                "pg_dump",
                "-U",
                url.username,
                "-Fc",
                source.url.database,
            ],
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        subprocess.run(
            [
                "docker",
                "exec",
                "-i",
                container,
                "pg_restore",
                "-U",
                url.username,
                "--single-transaction",
                "--no-owner",
                "--no-acl",
                "-d",
                restored.url.database,
            ],
            input=dump,
            check=True,
        )
        with restored.begin() as connection:
            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0005"
            config = migration_config(connection)
            command.upgrade(config, "head")
            command.check(config)
            with Session(connection) as db:
                application = db.get(Application, application_id)
                assert (application.receipt, application.cycle_id) == (receipt, cycle)
                assert db.scalar(select(EmailChallenge.failed_checks)) == 0
                project = db.scalar(select(Project).where(Project.slug == "nexus"))
                assert project.public_snapshot["title"] == "NEXUS"
                assert project.event.slug == "domination-the-frontend-challenge"
                assert len(project.credits) == 3
            _, next_application = cycle_with_applicant(connection, "next", "Next Applicant")
            assert next_application > application_id
