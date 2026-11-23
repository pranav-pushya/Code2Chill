from datetime import UTC, date, datetime
from typing import Annotated, Self

from fastapi import APIRouter, Depends, HTTPException
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator, model_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .admin_auth import Database, event_editor
from .admin_models import AdminAccount, AuditAction, AuditRecord, AuditTarget
from .content_models import Event, RegistrationStatus
from .public_content import PublicEvent, public_event
from .publication import (
    DraftConflict,
    PublicationError,
    change_publication,
    https_link,
    snapshot_for,
    university_signup,
)
from .publication_fields import PublicationState
from .time_rules import campus_date

router = APIRouter(
    prefix="/api/admin/events", tags=["Event management"], dependencies=[Depends(event_editor)]
)


class EventListItem(BaseModel):
    id: int
    title: str
    event_date: date | None
    publication_state: PublicationState


@router.get("", response_model=list[EventListItem])
def list_events(db: Database):
    events = db.scalars(select(Event).order_by(Event.event_date.desc().nulls_last(), Event.id))
    return [EventListItem.model_validate(event, from_attributes=True) for event in events]


Editor = Annotated[AdminAccount, Depends(event_editor)]


class EventFields(BaseModel):
    slug: str = Field(max_length=120, pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(min_length=1)
    event_date: date | None = None
    venue: str | None = Field(default=None, max_length=240)
    starts_at: AwareDatetime | None = None
    ends_at: AwareDatetime | None = None
    registration_status: RegistrationStatus = RegistrationStatus.PENDING
    registration_url: str | None = None
    official_url: str | None = None
    registration_opens_at: AwareDatetime | None = None
    registration_closes_at: AwareDatetime | None = None


class DraftFields(EventFields):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    @field_validator("*", mode="before")
    @classmethod
    def reject_null_characters(cls, value):
        if isinstance(value, str) and "\x00" in value:
            raise ValueError("Remove the null character.")
        return value

    @model_validator(mode="after")
    def validate_event(self) -> Self:
        if self.starts_at and campus_date(self.starts_at) != self.event_date:
            raise ValueError("The start must fall on the event date in India.")
        if self.ends_at and (not self.starts_at or self.ends_at <= self.starts_at):
            raise ValueError("The event end must follow its start.")
        if (
            self.registration_opens_at
            and self.registration_closes_at
            and self.registration_closes_at <= self.registration_opens_at
        ):
            raise ValueError("Registration must close after it opens.")
        if self.registration_url:
            university_signup(self.registration_url)
        if self.official_url:
            https_link(self.official_url)
        return self


class Revision(BaseModel):
    revision: int = Field(ge=1)


class DraftUpdate(DraftFields, Revision):
    pass


class SavedDraft(EventFields, Revision):
    id: int
    publication_state: PublicationState
    is_demo: bool


class Preview(BaseModel):
    draft: SavedDraft
    event: PublicEvent | None
    issue: str | None


def get_event(db, event_id, *, lock=False):
    event = db.get(Event, event_id, with_for_update=lock)
    if event is None:
        raise HTTPException(404, "Event not found.")
    return event


def save_draft(db, event, actor, action):
    try:
        db.flush()
        db.add(
            AuditRecord(
                actor_id=actor.id, action=action, target_type=AuditTarget.EVENT, target_id=event.id
            )
        )
        result = SavedDraft.model_validate(event, from_attributes=True)
        db.commit()
        return result
    except IntegrityError as exc:
        db.rollback()
        if exc.orig.sqlstate == "23505":
            raise HTTPException(409, "That event URL slug is already in use.") from None
        raise


@router.post("", status_code=201)
def create_event(fields: DraftFields, db: Database, actor: Editor) -> SavedDraft:
    event = Event(**fields.model_dump())
    db.add(event)
    return save_draft(db, event, actor, AuditAction.CREATE)


@router.get("/{event_id}", response_model=SavedDraft)
def read_draft(event_id: int, db: Database):
    return get_event(db, event_id)


@router.put("/{event_id}")
def edit_event(event_id: int, fields: DraftUpdate, db: Database, actor: Editor) -> SavedDraft:
    event = get_event(db, event_id, lock=True)
    if fields.revision != event.revision:
        raise HTTPException(409, "The saved draft changed. Reload it before saving.")
    if event.published_at and fields.slug != event.slug:
        raise HTTPException(422, "A published event must keep its URL slug.")
    for field, value in fields.model_dump(exclude={"revision"}).items():
        setattr(event, field, value)
    return save_draft(db, event, actor, AuditAction.UPDATE)


@router.get("/{event_id}/preview")
def preview_event(event_id: int, db: Database) -> Preview:
    event = get_event(db, event_id)
    draft = SavedDraft.model_validate(event, from_attributes=True)
    try:
        view = public_event(snapshot_for(db, event), datetime.now(UTC))
    except PublicationError as exc:
        return Preview(draft=draft, event=None, issue=str(exc))
    return Preview(draft=draft, event=view, issue=None)


@router.post("/{event_id}/publish", response_model=SavedDraft)
def publish_event(event_id: int, version: Revision, db: Database, actor: Editor):
    event = get_event(db, event_id, lock=True)
    try:
        change_publication(
            db,
            Event,
            event_id,
            expected_revision=version.revision,
            actor_id=actor.id,
            now=datetime.now(UTC),
            publish=True,
        )
    except DraftConflict as exc:
        raise HTTPException(409, str(exc)) from None
    except PublicationError as exc:
        raise HTTPException(422, str(exc)) from None
    result = SavedDraft.model_validate(event, from_attributes=True)
    db.commit()
    return result
