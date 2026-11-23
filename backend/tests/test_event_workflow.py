from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.admin_models import AdminRole, AuditAction, AuditRecord
from app.create_admin import create_account

STAFF = "/api/admin/events"
PUBLIC = "/api/events"
HEADER = {"X-Code2Chill-Admin": "1"}


def login(client, connection, role):
    email = "workflow@example.test"
    password = "temporary workflow password"
    with Session(connection, join_transaction_mode="create_savepoint") as db, db.begin():
        create_account(db, email, password, role)
    assert (
        client.post(
            "/api/admin/sign-in", headers=HEADER, json={"email": email, "password": password}
        ).status_code
        == 200
    )


def test_editor_publication_journey(api_db):
    client, connection = api_db
    login(client, connection, AdminRole.EDITOR)
    fields = {"slug": "studio-day", "title": "Studio day", "summary": "Student workshop"}
    created = client.post(STAFF, json=fields, headers=HEADER)
    assert created.status_code == 201
    url = STAFF + "/" + str(created.json()["id"])
    public = PUBLIC + "/studio-day"
    assert client.get(public).status_code == 404
    preview = client.get(url + "/preview").json()
    assert preview["issue"] and preview["event"] is None
    assert client.post(url + "/publish", headers=HEADER, json={"revision": 1}).status_code == 422
    assert client.post(STAFF, json=fields, headers=HEADER).status_code == 409
    fields.update(
        event_date="2099-01-01",
        registration_status="open",
        registration_url="https://chitkarau.life/events/studio-day",
    )
    saved = client.put(url, json=fields | {"revision": 1}, headers=HEADER)
    assert saved.status_code == 200
    preview = client.get(url + "/preview").json()
    version = {"revision": preview["draft"]["revision"]}
    assert preview["issue"] is None
    assert client.post(url + "/publish", headers=HEADER, json=version).status_code == 200
    assert client.get(public).json() == preview["event"] == client.get(PUBLIC).json()["upcoming"][0]
    assert client.get(public).json()["registration_url"] == fields["registration_url"]
    assert client.post(url + "/publish", headers=HEADER, json=version).status_code == 409
    revision = client.get(url).json()["revision"]
    assert (
        client.put(
            url, json=fields | {"revision": revision, "slug": "new-slug"}, headers=HEADER
        ).status_code
        == 422
    )
    fields.update(title="Studio day revised", registration_status="full")
    edit = client.put(url, json=fields | {"revision": revision}, headers=HEADER)
    assert edit.status_code == 200
    assert client.get(public).json()["title"] == "Studio day"
    assert client.put(url, json=fields | {"revision": revision}, headers=HEADER).status_code == 409
    assert (
        client.post(url + "/publish", json={"revision": revision}, headers=HEADER).status_code
        == 409
    )
    assert (
        client.post(
            url + "/publish", json={"revision": edit.json()["revision"]}, headers=HEADER
        ).status_code
        == 200
    )
    updated = client.get(public).json()
    assert updated["title"] == fields["title"] and updated["registration_status"] == "full"
    assert updated["registration_url"] is None
    assert list(connection.scalars(select(AuditRecord.action).order_by(AuditRecord.id))) == [
        AuditAction.CREATE,
        AuditAction.UPDATE,
        AuditAction.PUBLISH,
        AuditAction.UPDATE,
        AuditAction.PUBLISH,
    ]


def test_editor_input_validation(api_db):
    client, connection = api_db
    login(client, connection, AdminRole.ADMIN)
    fields = {"slug": "test", "title": "Test", "summary": "Summary"}
    now = datetime.now(UTC)
    for invalid in [
        {"title": "   "},
        {"slug": "two words"},
        {"registration_url": "https://other.example/events/test"},
        {"starts_at": "2099-01-01T18:30:00Z", "event_date": "2099-01-01"},
        {"ends_at": now.isoformat()},
        {
            "registration_opens_at": now.isoformat(),
            "registration_closes_at": (now - timedelta(minutes=1)).isoformat(),
        },
    ]:
        assert client.post(STAFF, json=fields | invalid, headers=HEADER).status_code == 422
    assert client.get(STAFF).json() == []


@pytest.mark.parametrize("role,expected", [(None, 401), (AdminRole.REVIEWER, 403)])
def test_protected_event_routes(api_db, role, expected):
    client, connection = api_db
    if role:
        login(client, connection, role)
    for method, path in [
        ("POST", ""),
        ("PUT", "/1"),
        ("GET", "/1"),
        ("GET", "/1/preview"),
        ("POST", "/1/publish"),
    ]:
        response = client.request(
            method, STAFF + path, headers=HEADER, **({} if method == "GET" else {"json": {}})
        )
        assert response.status_code == expected
