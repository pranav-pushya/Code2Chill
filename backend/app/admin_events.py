from datetime import date

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select

from .admin_auth import Database, event_editor
from .content_models import Event
from .publication_fields import PublicationState

router = APIRouter(
    prefix="/api/admin/events",
    tags=["Event management"],
    dependencies=[Depends(event_editor)],
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
