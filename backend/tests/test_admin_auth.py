from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.admin_auth import COOKIE, token_digest
from app.admin_models import AdminAccount, AdminRole, AdminSession
from app.content_models import Event
from app.create_admin import create_account

HEADER = {"X-Code2Chill-Admin": "1"}
LOGIN = "/api/admin/sign-in"
LOGOUT = "/api/admin/sign-out"
EVENTS = "/api/admin/events"
SESSION = "/api/admin/session"
EMAIL = "staff@example.test"
PASSWORD = "test-only staff password"


def provision(connection, role=AdminRole.ADMIN):
    with Session(connection, join_transaction_mode="create_savepoint") as db, db.begin():
        create_account(db, EMAIL.upper(), PASSWORD, role)


def sign_in(client, email=EMAIL, password=PASSWORD):
    return client.post(LOGIN, headers=HEADER, json={"email": email, "password": password})


@pytest.mark.parametrize("role", list(AdminRole))
def test_event_permissions(api_db, role):
    client, connection = api_db
    provision(connection, role)
    connection.execute(
        Event.__table__.insert().values(slug="staff-draft", title="Draft", summary="Draft summary")
    )
    assert client.get(EVENTS).status_code == 401
    assert sign_in(client, f" {EMAIL.upper()} ").json() == {"email": EMAIL, "role": role}
    assert client.get(SESSION).json() == {"email": EMAIL, "role": role}
    listing = client.get(EVENTS)
    assert listing.headers["cache-control"] == "no-store"
    if role == AdminRole.REVIEWER:
        assert listing.status_code == 403
        assert "staff-draft" not in listing.text
    else:
        assert listing.status_code == 200
        assert listing.json()[0]["publication_state"] == "draft"
        connection.execute(AdminAccount.__table__.update().values(role=AdminRole.REVIEWER))
        assert client.get(EVENTS).status_code == 403
    connection.execute(AdminAccount.__table__.update().values(active=False))
    assert client.get(SESSION).status_code == 401
    assert sign_in(client).status_code == 401


def test_session_lifecycle(api_db):
    client, connection = api_db
    provision(connection)
    login = sign_in(client)
    assert login.status_code == 200
    cookie = login.headers["set-cookie"].lower()
    assert all(
        flag in cookie
        for flag in ("httponly", "secure", "samesite=strict", "path=/", "max-age=28800")
    )
    raw = client.cookies[COOKIE]
    assert raw not in login.text
    digest = connection.scalar(select(AdminSession.token_digest))
    assert digest == token_digest(raw)
    assert connection.scalar(select(AdminAccount.password_hash)).startswith("$argon2id$")
    assert sign_in(client).status_code == 200
    assert client.cookies[COOKIE] != raw
    first_session = select(AdminSession.revoked_at).where(AdminSession.token_digest == digest)
    assert connection.scalar(first_session) is not None
    active = client.cookies[COOKIE]
    assert client.post(LOGOUT).status_code == 403
    assert client.get(SESSION).status_code == 200
    assert client.post(LOGOUT, headers=HEADER).status_code == 204
    assert COOKIE not in client.cookies
    assert client.get(EVENTS, headers={"Cookie": f"{COOKIE}={active}"}).status_code == 401
    assert client.post(LOGOUT, headers=HEADER).status_code == 204

    assert sign_in(client).status_code == 200
    past = datetime.now(UTC) - timedelta(days=1)
    connection.execute(
        AdminSession.__table__.update()
        .where(AdminSession.revoked_at.is_(None))
        .values(created_at=past - timedelta(hours=8), expires_at=past)
    )
    assert client.get(SESSION).status_code == 401


def test_credential_checks_and_cooldown(api_db):
    client, connection = api_db
    provision(connection)
    with Session(connection, join_transaction_mode="create_savepoint") as db:
        with pytest.raises(ValueError, match="already uses"):
            create_account(db, EMAIL, "different password for testing", AdminRole.REVIEWER)
        with pytest.raises(ValueError, match="15 and 256"):
            create_account(db, "another@example.test", "short", AdminRole.EDITOR)
    assert client.post(LOGIN, json={"email": EMAIL, "password": PASSWORD}).status_code == 403
    invalid = client.post(LOGIN, headers=HEADER, json={"password": PASSWORD})
    assert invalid.status_code == 422 and PASSWORD not in invalid.text
    unknown = sign_in(client, email="unknown@example.test")
    assert unknown.status_code == 401 and unknown.headers["cache-control"] == "no-store"
    for _ in range(5):
        rejected = sign_in(client, password="wrong")
        assert rejected.status_code == 401 and rejected.json() == unknown.json()
    assert sign_in(client).status_code == 401
    assert COOKIE not in client.cookies
    assert connection.scalar(select(AdminSession.id)) is None
    connection.execute(
        AdminAccount.__table__.update().values(retry_after=datetime.now(UTC) - timedelta(seconds=1))
    )
    assert sign_in(client).status_code == 200
    assert connection.scalar(select(AdminAccount.retry_after)) is None
