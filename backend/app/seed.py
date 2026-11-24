import argparse
from datetime import UTC, date, datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from .content_models import (
    Event,
    MediaAsset,
    Member,
    Project,
    ProjectCredit,
    RegistrationStatus,
    SiteSettings,
)
from .database import database_engine
from .domain import ClubDomain
from .publication import snapshot_for

# Public evidence is documented in docs/CONTENT_REGISTER.md.
ROSTER = (
    ("lakshay-kalra", "Lakshay Kalra", "President", None),
    ("jiya-arora", "Jiya Arora", "Vice-president", None),
    ("divyana-garg", "Divyana Garg", "Core Member", None),
    ("hunar-mehndiratta", "Hunar Mehndiratta", "Core Member", None),
    ("pranav-pushya", "Pranav Pushya", "Core Member", None),
    ("tamanna-kakkar", "Tamanna Kakkar", "Content Head", ClubDomain.CONTENT),
    ("samanyu-thakur", "Samanyu Thakur", "Technical Head", ClubDomain.TECHNICAL),
    ("bhupinder-singh", "Bhupinder Singh", "Technical Head", ClubDomain.TECHNICAL),
    ("ayush-sharma", "Ayush Sharma", "Content Head", ClubDomain.CONTENT),
    ("jashan-bhalla", "Jashan Bhalla", "Social Media Head", ClubDomain.SOCIAL_MEDIA),
    ("muskan-dhanda", "Muskan Dhanda", "Promotion Head", ClubDomain.PROMOTION),
)
ARCHIVED_EVENTS = (
    (
        "byte-the-vibe",
        "Byte The Vibe",
        date(2026, 5, 18),
        "A team coding sprint with mentor guidance and judged final pitches.",
        "Pierre Hall, Architecture Block",
        "https://chitkarau.life/events/byte-the-vibe",
        datetime(2026, 5, 18, 7, 30, tzinfo=UTC),
        datetime(2026, 5, 18, 10, 30, tzinfo=UTC),
        "byte-the-vibe-poster",
    ),
    (
        "domination-the-frontend-challenge",
        "DOMination – The Frontend Challenge",
        date(2026, 7, 18),
        (
            "Teams built web interfaces evaluated on design, responsiveness, accessibility, "
            "performance and relevance."
        ),
        "Pierre Hall, Architecture Block",
        "https://chitkarau.life/events/domination-the-frontend-challenge",
        datetime(2026, 7, 18, 5, 30, tzinfo=UTC),
        None,
        "domination-poster",
    ),
    (
        "on-fire",
        "(O)n Fire – The LeetCode Competition",
        date(2026, 9, 23),
        (
            "A competitive programming contest focused on solving algorithmic LeetCode challenges "
            "under time pressure, featuring Rs 12,300+ in cash prizes, trophies and participation certificates."
        ),
        "Einstein Hall",
        "https://chitkarau.life/events/on-fire",
        datetime(2026, 9, 23, 4, 30, tzinfo=UTC),
        datetime(2026, 9, 23, 10, 30, tzinfo=UTC),
        "on-fire-poster",
    ),
)
EVENT_POSTERS = (
    (
        "byte-the-vibe-poster",
        "/media/byte-the-vibe.jpg",
        "Byte The Vibe official event banner",
        "Code2Chill & OSL",
    ),
    (
        "domination-poster",
        "/media/domination.jpg",
        "DOMination – The Frontend Challenge official event banner",
        "Code2Chill & OSL",
    ),
    (
        "on-fire-poster",
        "/media/on-fire-poster.jpg",
        "(O)n Fire: The LeetCode Competition official event poster",
        "Code2Chill & OSL",
    ),
)


def create_missing(session: Session, model, **values):
    statement = (
        insert(model)
        .values(**values)
        .on_conflict_do_nothing(index_elements=["slug"])
        .returning(model)
    )
    return session.scalar(statement)


def seed_content(session: Session, *, include_demo: bool = False) -> dict[str, int]:
    now = datetime.now(UTC)
    created = {"members": 0, "events": 0, "projects": 0, "demo_events": 0}

    for position, (slug, name, role, domain) in enumerate(ROSTER):
        member = create_missing(
            session,
            Member,
            slug=slug,
            name=name,
            role_title=role,
            domain=domain,
            display_order=position,
        )
        if member is not None:
            member.public_snapshot = snapshot_for(session, member)
            member.published_at = now
            created["members"] += 1

    for storage_key, asset_url, alt_text, credit in EVENT_POSTERS:
        poster = session.scalar(
            select(MediaAsset).where(MediaAsset.storage_key == storage_key)
        )
        if poster is None:
            poster = MediaAsset(
                storage_key=storage_key,
                asset_url=asset_url,
                content_type="image/jpeg",
                alt_text=alt_text,
                credit=credit,
                approved_for_publication=True,
            )
            session.add(poster)
            session.flush()

    for (
        slug,
        title,
        event_date,
        summary,
        venue,
        official_url,
        starts_at,
        ends_at,
        poster_key,
    ) in ARCHIVED_EVENTS:
        poster_id = None
        if poster_key:
            poster_id = session.scalar(
                select(MediaAsset.id).where(MediaAsset.storage_key == poster_key)
            )
        event = create_missing(
            session,
            Event,
            slug=slug,
            title=title,
            event_date=event_date,
            summary=summary,
            venue=venue,
            official_url=official_url,
            starts_at=starts_at,
            ends_at=ends_at,
            poster_id=poster_id,
            registration_status=RegistrationStatus.ENDED,
        )
        if event is not None:
            if poster_id:
                event.poster = session.get(MediaAsset, poster_id)
            event.public_snapshot = snapshot_for(session, event)
            event.published_at = now
            created["events"] += 1
        else:
            existing = session.scalar(select(Event).where(Event.slug == slug))
            if existing is not None and poster_id and existing.poster_id != poster_id:
                existing.poster_id = poster_id
                existing.poster = session.get(MediaAsset, poster_id)
                if starts_at and not existing.starts_at:
                    existing.starts_at = starts_at
                    existing.ends_at = ends_at
                existing.public_snapshot = snapshot_for(session, existing)
                existing.published_at = now

    event_id = session.scalar(
        select(Event.id).where(Event.slug == "domination-the-frontend-challenge")
    )
    ayush_id = session.scalar(select(Member.id).where(Member.slug == "ayush-sharma"))
    nexus = create_missing(
        session,
        Project,
        slug="nexus",
        title="NEXUS",
        event_id=event_id,
        summary="A survival game that adjusts difficulty using gameplay, facial and audio signals.",
        repository_url="https://github.com/thisIsAyushFr/Nexus-Emotion-Detection",
        demo_url="https://c2c-event.vercel.app/",
    )
    if nexus is not None:
        nexus.credits = [
            ProjectCredit(position=0, name="Ayush Sharma", member_id=ayush_id),
            ProjectCredit(position=1, name="Arnav Sharma"),
            ProjectCredit(position=2, name="Anveer Singh Sandhu"),
        ]
        nexus.public_snapshot = snapshot_for(session, nexus)
        nexus.published_at = now
        created["projects"] += 1

    chronoatlas = create_missing(
        session,
        Project,
        slug="chronoatlas",
        title="ChronoAtlas – Travel Through Time",
        event_id=event_id,
        summary="A frontend project built at DOMination.",
    )
    if chronoatlas is not None:
        chronoatlas.credits = [
            ProjectCredit(position=0, name="Vibhanshu Jain"),
            ProjectCredit(position=1, name="Dheraj Sharma"),
        ]
        chronoatlas.public_snapshot = snapshot_for(session, chronoatlas)
        chronoatlas.published_at = now
        created["projects"] += 1

    settings = session.get(SiteSettings, 1)
    if settings is not None and settings.public_snapshot is None:
        settings.public_snapshot = snapshot_for(session, settings)
        settings.published_at = now

    if include_demo:
        demo = create_missing(
            session,
            Event,
            slug="demo-event-handoff",
            title="Demo: Event handoff rehearsal",
            summary="Practice record for demonstrating the event editor.",
            is_demo=True,
        )
        created["demo_events"] = int(demo is not None)
    session.flush()
    return created


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Insert missing Code2Chill content after migration."
    )
    parser.add_argument(
        "--include-demo", action="store_true", help="Add a labeled draft event for practice."
    )
    args = parser.parse_args()
    engine = database_engine()
    try:
        with Session(engine) as session, session.begin():
            created = seed_content(session, include_demo=args.include_demo)
    finally:
        engine.dispose()
    print(
        "Inserted "
        + ", ".join(f"{count} {kind.replace('_', ' ')}" for kind, count in created.items())
    )


if __name__ == "__main__":
    main()
