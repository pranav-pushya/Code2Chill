from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app import recruitment_mail
from app.admin_models import AdminAccount, AdminRole, RecruitmentReviewer
from app.publication import change_publication
from app.recruitment_models import (
    Application,
    ApplicationRoute,
    EmailChallenge,
    RecruitmentCycle,
    RecruitmentDomain,
)


def create_cycle(connection, *, route=ApplicationRoute.LOCAL, start=-1, end=1):
    now = datetime.now(UTC)
    with Session(connection, join_transaction_mode="create_savepoint") as db, db.begin():
        reviewer = AdminAccount(
            role=AdminRole.REVIEWER, email=f"{uuid4()}@example.test", password_hash="unused"
        )
        cycle = RecruitmentCycle(
            slug=f"cycle-{uuid4()}",
            title="Test recruitment",
            route=route,
            opens_at=now + timedelta(hours=start),
            closes_at=now + timedelta(hours=end),
            eligibility="Current students",
            email_domain="campus.example",
            optional_field="motivation",
            external_url="https://example.test/apply",
            domains=[RecruitmentDomain(domain="technical")],
        )
        db.add_all([cycle, reviewer])
        db.flush()
        db.add(RecruitmentReviewer(cycle_id=cycle.id, account_id=reviewer.id))
        db.flush()
        change_publication(
            db,
            RecruitmentCycle,
            cycle.id,
            expected_revision=cycle.revision,
            actor_id=reviewer.id,
            now=now,
            publish=True,
        )
        return cycle.id


def test_join_shows_published_cycle_and_current_reviewer(api_db, monkeypatch):
    client, connection = api_db
    monkeypatch.setattr(recruitment_mail, "mail_ready", lambda: False)
    assert client.get("/api/recruitment").json() == {"state": "announcement"}
    create_cycle(connection, start=-2, end=-1)
    assert client.get("/api/recruitment").json()["state"] == "closed"
    create_cycle(connection, start=1, end=2)
    assert client.get("/api/recruitment").json()["state"] == "scheduled"
    external = create_cycle(connection, route=ApplicationRoute.EXTERNAL)
    result = client.get("/api/recruitment").json()
    assert result["id"] == external and result["external_url"] == "https://example.test/apply"
    connection.execute(update(AdminAccount).values(active=False))
    local = create_cycle(connection)
    assert "route" not in client.get("/api/recruitment").json()
    monkeypatch.setattr(recruitment_mail, "mail_ready", lambda: True)
    connection.execute(
        update(RecruitmentCycle).where(RecruitmentCycle.id == local).values(title="Private draft")
    )
    result = client.get("/api/recruitment")
    assert result.headers["cache-control"] == "no-store"
    assert result.json()["title"] == "Test recruitment" and result.json()["route"] == "local"
    assert client.get("/api/page-head?path=/join/APPLY").status_code == 200
    connection.execute(update(AdminAccount).values(active=False))
    assert client.get("/api/recruitment").json() == {"state": "announcement"}
    identity = {"attempt_id": str(uuid4()), "university_email": "student@campus.example"}
    assert client.post(f"/api/recruitment/{local}/email-code", json=identity).status_code == 409


def test_verified_intake_and_retry_after_cutoff(api_db, monkeypatch):
    client, connection = api_db
    cycle = create_cycle(connection)
    path = f"/api/recruitment/{cycle}"
    delivered = {}
    monkeypatch.setattr(recruitment_mail, "mail_ready", lambda: True)
    monkeypatch.setattr(recruitment_mail, "send_code", delivered.__setitem__)
    email = "student@campus.example"
    identity = {"attempt_id": str(uuid4()), "university_email": email.upper()}
    assert (
        client.post(
            path + "/email-code", json=identity | {"university_email": "student@other.example"}
        ).status_code
        == 422
    )
    assert client.post(path + "/email-code", json=identity).status_code == 204
    assert client.post(path + "/email-code", json=identity).status_code == 429
    form = identity | {
        "code": delivered[email],
        "domain": "technical",
        "full_name": "Demo Student",
        "motivation": "Build a project",
    }

    def submit(**changes):
        return client.post(path + "/applications", json=form | changes)

    assert submit(code="wrong").status_code == 403
    assert submit(domain="content").status_code == 422
    assert submit(portfolio_url="https://example.test").status_code == 422
    assert submit(full_name="   ").status_code == 422
    receipt = submit().json()["receipt"]
    assert UUID(receipt)
    assert submit(full_name="Changed name").status_code == 409
    assert submit().json() == {"receipt": receipt}
    old = datetime.now(UTC) - timedelta(minutes=20)
    connection.execute(update(EmailChallenge).values(sent_at=old))
    duplicate = identity | {"attempt_id": str(uuid4())}
    assert client.post(path + "/email-code", json=duplicate).status_code == 204
    assert submit(**duplicate, code=delivered[email]).status_code == 409
    assert submit().status_code == 403
    with Session(connection, join_transaction_mode="create_savepoint") as db, db.begin():
        record = db.get(RecruitmentCycle, cycle)
        record.public_snapshot = record.public_snapshot | {"closes_at": old.isoformat()}
    assert submit(**duplicate, code=delivered[email]).status_code == 409
    connection.execute(update(EmailChallenge).values(sent_at=old))
    assert client.post(path + "/email-code", json=identity).status_code == 204
    assert submit(code=delivered[email]).json() == {"receipt": receipt}
    assert (
        client.post(path + "/email-code", json=identity | {"attempt_id": str(uuid4())}).status_code
        == 409
    )
    assert connection.scalar(select(func.count()).select_from(Application)) == 1


def test_intake_limits_and_code_renewal(api_db, monkeypatch):
    client, connection = api_db
    cycle = create_cycle(connection)
    path = f"/api/recruitment/{cycle}"
    sent = {}
    monkeypatch.setattr(recruitment_mail, "mail_ready", lambda: True)
    monkeypatch.setattr(recruitment_mail, "send_code", sent.__setitem__)
    email = "student@campus.example"
    identity = {"attempt_id": str(uuid4()), "university_email": email}
    for route in ("/applications", "/email-code"):
        assert (
            client.post(path + route, files={"file": ("example.txt", b"sample")}).status_code == 415
        )
        oversized = client.post(
            path + route,
            headers={"content-type": "application/json"},
            content=iter([b" " * 16384] * 3),
        )
        assert oversized.status_code == 413
    assert client.post(path + "/email-code", json=identity).status_code == 204
    assert client.post(path + "/email-code", json=identity).headers["Retry-After"] == "60"
    form = identity | {"code": "incorrect", "domain": "technical", "full_name": "Test Student"}
    for _ in range(5):
        assert client.post(path + "/applications", json=form).status_code == 403
    form["code"] = sent[email]
    assert client.post(path + "/applications", json=form).status_code == 429
    connection.execute(
        update(EmailChallenge).values(sent_at=datetime.now(UTC) - timedelta(minutes=2))
    )
    assert client.post(path + "/email-code", json=identity).status_code == 204
    assert client.post(path + "/applications", json=form | {"code": sent[email]}).status_code == 200
