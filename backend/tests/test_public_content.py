from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.content_models import Event, RegistrationStatus
from app.publication import snapshot_for
from app.seed import seed_content
from app.time_rules import campus_date


def test_public_pages_serve_the_published_version(api_db):
    client, connection = api_db
    assert client.get("/api/events").json() == {"upcoming": [], "past": []}
    with (
        Session(connection, join_transaction_mode="create_savepoint") as db,
        db.begin(),
    ):
        seed_content(db, include_demo=True)
        demo = db.scalar(select(Event).where(Event.is_demo.is_(True)))
        demo.event_date = campus_date(datetime.now(UTC))
        demo.public_snapshot = snapshot_for(db, demo)
        demo.published_at = datetime.now(UTC)

    schedule = client.get("/api/events").json()
    assert not schedule["upcoming"]
    assert [event["slug"] for event in schedule["past"]] == [
        "domination-the-frontend-challenge",
        "byte-the-vibe",
    ]
    assert client.get("/api/events/demo-event-handoff").status_code == 404
    archive = client.get("/api/events/byte-the-vibe").json()
    assert archive["registration_status"] == "ended" and archive["registration_url"] is None


def test_public_registration_handoff_follows_published_window(api_db):
    client, connection = api_db
    now = datetime.now(UTC)
    with (
        Session(connection, join_transaction_mode="create_savepoint") as db,
        db.begin(),
    ):
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
    with (
        Session(connection, join_transaction_mode="create_savepoint") as db,
        db.begin(),
    ):
        event = db.scalar(select(Event).where(Event.slug == "campus-workshop"))
        event.registration_closes_at = now - timedelta(minutes=1)
        event.public_snapshot = snapshot_for(db, event)
    closed = client.get(endpoint).json()
    assert closed["registration_status"] == "closed" and closed["registration_url"] is None
