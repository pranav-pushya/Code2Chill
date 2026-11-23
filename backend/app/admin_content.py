from collections import defaultdict, deque
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .admin_auth import Database, current_account
from .admin_models import AdminAccount, AdminRole, AuditAction, AuditRecord, AuditTarget
from .content_models import Event, MediaAsset, Member, Project, ProjectCredit, SiteSettings
from .domain import ClubDomain
from .publication import https_link

router = APIRouter(prefix="/api/admin/content", tags=["Content management"])
Kind = Literal["members", "projects", "media", "settings"]
Account = Annotated[AdminAccount, Depends(current_account)]
Nonempty = Annotated[str, Field(min_length=1, max_length=160)]
Slug = Annotated[str, Field(max_length=120, pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")]


class Fields(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    @field_validator("*")
    @classmethod
    def validate_text(cls, value, info):
        strings = value if isinstance(value, list) else [value]
        if any(isinstance(s, str) and "\0" in s for s in strings):
            raise ValueError("Remove the null character.")
        if value and (
            info.field_name.endswith("_url")
            or info.field_name in ("university", "instagram", "linkedin")
        ):
            https_link(value)
        return value


class MemberFields(Fields):
    slug: Slug
    name: Nonempty
    role_title: Annotated[str, Field(min_length=1, max_length=120)]
    domain: ClubDomain | None = None
    display_order: int = Field(ge=0, le=2147483647)
    bio: str | None = None
    portrait_id: int | None = None


class ProjectFields(Fields):
    slug: Slug
    title: Annotated[str, Field(min_length=1, max_length=200)]
    summary: Annotated[str, Field(min_length=1)]
    repository_url: str | None = None
    demo_url: str | None = None
    screenshot_id: int | None = None
    event_id: int | None = None
    credits: list[Nonempty]


class MediaFields(Fields):
    storage_key: Annotated[str, Field(min_length=1, max_length=512)]
    content_type: Annotated[str, Field(min_length=1, max_length=100)]
    asset_url: str | None = None
    source_url: str | None = None
    alt_text: Annotated[str, Field(max_length=300)]
    credit: Annotated[str, Field(max_length=200)]
    approved_for_publication: bool


class SettingsFields(Fields):
    university: str
    instagram: str
    linkedin: str

    @field_validator("*")
    @classmethod
    def require_url(cls, value):
        https_link(value)
        return value


TYPES = {
    "members": (Member, MemberFields, AuditTarget.MEMBER),
    "projects": (Project, ProjectFields, AuditTarget.PROJECT),
    "media": (MediaAsset, MediaFields, AuditTarget.MEDIA_ASSET),
    "settings": (SiteSettings, SettingsFields, AuditTarget.SITE_SETTINGS),
}


def check_permission(kind, actor):
    if actor.role == AdminRole.REVIEWER or (kind == "settings" and actor.role != AdminRole.ADMIN):
        raise HTTPException(403, "Your account cannot manage this content.")


def saved(kind, record):
    values = {}
    for key in TYPES[kind][1].model_fields:
        values[key] = [c.name for c in record.credits] if key == "credits" else getattr(record, key)
    return {
        "id": record.id,
        "revision": record.revision,
        "fields": values,
        "published": bool(getattr(record, "published_at", None)),
    }


def get_record(db, kind, item_id, lock=False):
    record = db.get(TYPES[kind][0], item_id, with_for_update=lock)
    if record is None:
        raise HTTPException(404, "Content record unavailable.")
    return record


@router.get("/{kind}")
def list_records(kind: Kind, db: Database, actor: Account):
    check_permission(kind, actor)
    model = TYPES[kind][0]
    records = db.scalars(select(model).order_by(model.id))
    return [
        {
            "id": r.id,
            "label": getattr(r, "name", None)
            or getattr(r, "title", None)
            or getattr(r, "storage_key", "Site settings"),
        }
        for r in records
    ]


@router.get("/{kind}/{item_id}")
def read_record(kind: Kind, item_id: int, db: Database, actor: Account):
    check_permission(kind, actor)
    return saved(kind, get_record(db, kind, item_id))


class Edit(BaseModel):
    fields: dict
    revision: int | None = None


def write_record(db, kind, record, edit, actor, creating):
    try:
        fields = TYPES[kind][1].model_validate(edit.fields).model_dump()
    except ValidationError as exc:
        error = exc.errors()[0]
        raise HTTPException(422, f"{'.'.join(map(str, error['loc']))}: {error['msg']}") from None
    if not creating:
        if edit.revision != record.revision:
            raise HTTPException(409, "The record changed. Reload before saving.")
        if (
            getattr(record, "published_at", None)
            and "slug" in fields
            and record.slug != fields["slug"]
        ):
            raise HTTPException(422, "A published record must keep its URL slug.")
    if (
        kind == "media"
        and fields["approved_for_publication"]
        and not (fields["alt_text"] and fields["credit"])
    ):
        raise HTTPException(422, "Add alternative text and a credit before approving this asset.")
    for key, model in (
        ("portrait_id", MediaAsset),
        ("screenshot_id", MediaAsset),
        ("event_id", Event),
    ):
        if fields.get(key) is not None and db.get(model, fields[key]) is None:
            raise HTTPException(422, "The selected media or event no longer exists.")
    if kind == "projects":
        credits = fields.pop("credits")
        if credits != [c.name for c in record.credits]:
            links = defaultdict(deque)
            for c in record.credits:
                links[c.name].append(c.member_id)
            record.credits = [
                ProjectCredit(
                    position=i, name=name, member_id=links[name].popleft() if links[name] else None
                )
                for i, name in enumerate(credits)
            ]
    for key, value in fields.items():
        setattr(record, key, value)
    if not creating:
        record.revision += 1
    db.add(record)
    try:
        db.flush()
        db.add(
            AuditRecord(
                actor_id=actor.id,
                target_id=record.id,
                target_type=TYPES[kind][2],
                action=AuditAction.CREATE if creating else AuditAction.UPDATE,
            )
        )
        result = saved(kind, record)
        db.commit()
        return result
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            409,
            "Check that the slug or storage key is unique and the selected records still exist.",
        ) from None


@router.post("/{kind}", status_code=201)
def create_record(kind: Kind, edit: Edit, db: Database, actor: Account):
    check_permission(kind, actor)
    if kind == "settings":
        raise HTTPException(409, "Use the existing site settings.")
    return write_record(db, kind, TYPES[kind][0](), edit, actor, True)


@router.put("/{kind}/{item_id}")
def update_record(kind: Kind, item_id: int, edit: Edit, db: Database, actor: Account):
    check_permission(kind, actor)
    return write_record(db, kind, get_record(db, kind, item_id, lock=True), edit, actor, False)
