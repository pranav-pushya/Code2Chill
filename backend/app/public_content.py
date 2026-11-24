from datetime import UTC, date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from .content_models import Event, Member, Project, RegistrationStatus, SiteSettings
from .database import request_session
from .domain import ClubDomain
from .publication import event_registration

router = APIRouter(prefix="/api", tags=["Public content"])
Database = Annotated[Session, Depends(request_session)]


class PublicImage(BaseModel):
    asset_url: str | None = None
    alt_text: str
    credit: str


class PublicEvent(BaseModel):
    poster: PublicImage | None = None
    slug: str
    title: str
    summary: str
    event_date: date
    venue: str | None
    starts_at: datetime | None
    ends_at: datetime | None
    registration_status: RegistrationStatus
    registration_url: str | None
    official_url: str | None


class Schedule(BaseModel):
    upcoming: list[PublicEvent]
    past: list[PublicEvent]


class PublicProject(BaseModel):
    screenshot: PublicImage | None = None
    slug: str
    title: str
    summary: str
    credits: list[str]
    repository_url: str | None
    demo_url: str | None


class PublicMember(BaseModel):
    portrait: PublicImage | None = None
    slug: str
    name: str
    role_title: str
    domain: ClubDomain | None
    bio: str | None


def published(model):
    query = select(model.public_snapshot).where(model.public_snapshot.is_not(None))
    if model is Event:
        query = query.where(model.public_snapshot["is_demo"].as_boolean().is_not(True))
    return query


@router.get("/site-links")
def published_links(db: Database):
    return db.scalar(select(SiteSettings.public_snapshot).where(SiteSettings.id == 1))


def detail(db, model, slug):
    snapshot = db.scalar(published(model).where(model.slug == slug))
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return snapshot


def public_event(snapshot, now):
    status = event_registration(snapshot, now)
    return PublicEvent.model_validate(
        snapshot
        | {
            "registration_status": status,
            "registration_url": snapshot["registration_url"]
            if status == RegistrationStatus.OPEN
            else None,
        }
    )


@router.get("/events")
def list_events(db: Database) -> Schedule:
    now = datetime.now(UTC)
    upcoming, past = [], []
    for snapshot in db.scalars(published(Event).order_by(Event.slug)):
        event = public_event(snapshot, now)
        (past if event.registration_status == RegistrationStatus.ENDED else upcoming).append(event)
    upcoming.sort(key=lambda event: event.event_date)
    past.sort(key=lambda event: event.event_date, reverse=True)
    return Schedule(upcoming=upcoming, past=past)


@router.get("/events/{slug}")
def event_detail(slug: str, db: Database) -> PublicEvent:
    return public_event(detail(db, Event, slug), datetime.now(UTC))


@router.get("/projects", response_model=list[PublicProject])
def list_projects(db: Database):
    return db.scalars(published(Project).order_by(Project.id)).all()


@router.get("/projects/{slug}", response_model=PublicProject)
def project_detail(slug: str, db: Database):
    return detail(db, Project, slug)


@router.get("/team", response_model=list[PublicMember])
def list_members(db: Database):
    order = Member.public_snapshot["display_order"].as_integer()
    return db.scalars(published(Member).order_by(order, Member.id)).all()
