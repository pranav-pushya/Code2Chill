import argparse
from datetime import UTC, date, datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from .content_models import Event, Member, Project, ProjectCredit, RegistrationStatus, SiteSettings
from .database import database_engine
from .domain import ClubDomain
from .publication import snapshot_for

# Public evidence is documented in docs/CONTENT_REGISTER.md.
ROSTER = (
    ("lakshay-kalra", "Lakshay Kalra", "President", None),
    ("jiya-arora", "Jiya Arora", "Vice-president", None),
    ("divyana-garg", "Divyana Garg", "Core Member", None),
    ("hunar-mehndiratta", "Hunar Mehndiratta", "Core Member", None),
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
    ),
    (
        "domination-the-frontend-challenge",
        "DOMination – The Frontend Challenge",
        date(2026, 7, 18),
        (
            "Teams built web interfaces evaluated on design, responsiveness, accessibility, "
            "performance and relevance."
        ),
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

    for slug, title, event_date, summary in ARCHIVED_EVENTS:
        event = create_missing(
            session,
            Event,
            slug=slug,
            title=title,
            event_date=event_date,
            summary=summary,
            venue="Pierre Hall, Architecture Block",
            official_url=f"https://chitkarau.life/events/{slug}",
            registration_status=RegistrationStatus.ENDED,
        )
        if event is not None:
            event.public_snapshot = snapshot_for(session, event)
            event.published_at = now
            created["events"] += 1

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
