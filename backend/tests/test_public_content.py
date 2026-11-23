from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.content_models import Event, Member, Project, RegistrationStatus
from app.publication import snapshot_for
from app.seed import seed_content
from app.time_rules import campus_date


def test_public_pages_serve_the_published_version(api_db):
    client, connection = api_db
    assert client.get("/api/events").json() == {"upcoming": [], "past": []}
    assert client.get("/api/projects").json() == client.get("/api/team").json() == []
    with Session(connection, join_transaction_mode="create_savepoint") as db, db.begin():
        seed_content(db, include_demo=True)
        nexus = db.scalar(select(Project).where(Project.slug == "nexus"))
        nexus.summary = "Unpublished revision"
        leader = db.scalar(select(Member).where(Member.slug == "lakshay-kalra"))
        leader.display_order = 99
        leader.role_title = "Unpublished role"
        demo = db.scalar(select(Event).where(Event.is_demo.is_(True)))
        demo.event_date = campus_date(datetime.now(UTC))
        demo.public_snapshot = snapshot_for(db, demo)
        demo.published_at = datetime.now(UTC)
        db.add(Project(slug="draft-project", title="Draft", summary="Draft only"))

    schedule = client.get("/api/events").json()
    assert not schedule["upcoming"]
    assert [event["slug"] for event in schedule["past"]] == [
        "domination-the-frontend-challenge",
        "byte-the-vibe",
    ]
    assert client.get("/api/events/demo-event-handoff").status_code == 404
    archive = client.get("/api/events/byte-the-vibe").json()
    assert archive["registration_status"] == "ended" and archive["registration_url"] is None
    projects = client.get("/api/projects").json()
    assert [project["slug"] for project in projects] == ["nexus", "chronoatlas"]
    assert client.get("/api/projects/nexus").json() == projects[0]
    assert projects[0]["credits"] == ["Ayush Sharma", "Arnav Sharma", "Anveer Singh Sandhu"]
    assert "Unpublished" not in projects[0]["summary"]
    assert client.get("/api/projects/draft-project").status_code == 404
    assert client.get("/api/projects/absent").status_code == 404
    members = client.get("/api/team").json()
    assert len(members) == 10
    assert (members[0]["name"], members[0]["role_title"]) == ("Lakshay Kalra", "President")


def test_public_registration_handoff_follows_published_window(api_db):
    client, connection = api_db
    now = datetime.now(UTC)
    with Session(connection, join_transaction_mode="create_savepoint") as db, db.begin():
        event = Event(
            slug="campus-workshop",
            title="Workshop",
            summary="A test workshop",
            event_date=campus_date(now + timedelta(days=2)),
            registration_url="https://chitkarau.life/events/campus-workshop",
            registration_status=RegistrationStatus.OPEN,
        )
        db.add(event)
        db.flush()
        event.public_snapshot = snapshot_for(db, event)
        event.published_at = now
    endpoint = "/api/events/campus-workshop"
    result = client.get(endpoint).json()
    assert result == client.get("/api/events").json()["upcoming"][0]
    assert result["registration_status"] == "open"
    assert result["registration_url"] == "https://chitkarau.life/events/campus-workshop"
    with Session(connection, join_transaction_mode="create_savepoint") as db, db.begin():
        event = db.scalar(select(Event).where(Event.slug == "campus-workshop"))
        event.registration_closes_at = now - timedelta(minutes=1)
        event.public_snapshot = snapshot_for(db, event)
    closed = client.get(endpoint).json()
    assert closed["registration_status"] == "closed" and closed["registration_url"] is None
