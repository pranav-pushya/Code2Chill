from datetime import date, datetime
from enum import StrEnum

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, String, Text, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .domain import ClubDomain, choices
from .model_base import Base, required_text, route_slug
from .publication_fields import PublicationFields, publication_integrity
from .time_rules import UTCDateTime


class RegistrationStatus(StrEnum):
    PENDING = "pending"
    OPEN = "open"
    CLOSED = "closed"
    FULL = "full"
    ENDED = "ended"


class MediaAsset(Base):
    __tablename__ = "media_asset"
    __table_args__ = (
        required_text("storage_key"),
        required_text("content_type"),
        CheckConstraint(
            "NOT approved_for_publication OR (alt_text ~ '[^[:space:]]' AND credit ~ '[^[:space:]]')",
            name="approved_metadata",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    storage_key: Mapped[str] = mapped_column(String(512), unique=True)
    content_type: Mapped[str] = mapped_column(String(100))
    alt_text: Mapped[str] = mapped_column(String(300))
    credit: Mapped[str] = mapped_column(String(200))
    source_url: Mapped[str | None] = mapped_column(Text)
    approved_for_publication: Mapped[bool] = mapped_column(Boolean, server_default=false())


class Member(PublicationFields, Base):
    __tablename__ = "member"
    __table_args__ = (
        publication_integrity(),
        route_slug(),
        required_text("name"),
        required_text("role_title"),
        CheckConstraint("display_order >= 0", name="display_order"),
        Index("ix_member_display_order", "display_order", "id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True)
    name: Mapped[str] = mapped_column(String(160))
    role_title: Mapped[str] = mapped_column(String(120))
    domain: Mapped[ClubDomain | None] = mapped_column(choices(ClubDomain))
    bio: Mapped[str | None] = mapped_column(Text)
    display_order: Mapped[int] = mapped_column(server_default="0")
    portrait_id: Mapped[int | None] = mapped_column(ForeignKey("media_asset.id"))
    portrait: Mapped[MediaAsset | None] = relationship()


class Event(PublicationFields, Base):
    __tablename__ = "event"
    __table_args__ = (
        publication_integrity(),
        route_slug(),
        required_text("title"),
        required_text("summary"),
        CheckConstraint(
            "starts_at IS NULL OR (event_date IS NOT NULL AND "
            "event_date = (starts_at AT TIME ZONE 'Asia/Kolkata')::date)",
            name="campus_date",
        ),
        CheckConstraint(
            "ends_at IS NULL OR (starts_at IS NOT NULL AND ends_at > starts_at)",
            name="event_duration",
        ),
        CheckConstraint(
            "registration_opens_at IS NULL OR registration_closes_at IS NULL "
            "OR registration_closes_at > registration_opens_at",
            name="registration_window",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True)
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(Text)
    event_date: Mapped[date | None] = mapped_column(index=True)
    starts_at: Mapped[datetime | None] = mapped_column(UTCDateTime())
    ends_at: Mapped[datetime | None] = mapped_column(UTCDateTime())
    registration_opens_at: Mapped[datetime | None] = mapped_column(UTCDateTime())
    registration_closes_at: Mapped[datetime | None] = mapped_column(UTCDateTime())
    venue: Mapped[str | None] = mapped_column(String(240))
    is_demo: Mapped[bool] = mapped_column(Boolean, server_default=false())
    official_url: Mapped[str | None] = mapped_column(Text)
    registration_url: Mapped[str | None] = mapped_column(Text)
    registration_status: Mapped[RegistrationStatus] = mapped_column(
        choices(RegistrationStatus), server_default=RegistrationStatus.PENDING
    )
    poster_id: Mapped[int | None] = mapped_column(ForeignKey("media_asset.id"))
    poster: Mapped[MediaAsset | None] = relationship()


class Project(PublicationFields, Base):
    __tablename__ = "project"
    __table_args__ = (
        publication_integrity(),
        route_slug(),
        required_text("title"),
        required_text("summary"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True)
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(Text)
    repository_url: Mapped[str | None] = mapped_column(Text)
    demo_url: Mapped[str | None] = mapped_column(Text)
    event_id: Mapped[int | None] = mapped_column(ForeignKey("event.id"), index=True)
    screenshot_id: Mapped[int | None] = mapped_column(ForeignKey("media_asset.id"))
    event: Mapped[Event | None] = relationship()
    screenshot: Mapped[MediaAsset | None] = relationship()
    credits: Mapped[list["ProjectCredit"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="ProjectCredit.position",
    )


class ProjectCredit(Base):
    __tablename__ = "project_credit"
    __table_args__ = (
        required_text("name"),
        CheckConstraint("position >= 0", name="position"),
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"), primary_key=True
    )
    position: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    member_id: Mapped[int | None] = mapped_column(ForeignKey("member.id", ondelete="SET NULL"))
    project: Mapped[Project] = relationship(back_populates="credits")
    member: Mapped[Member | None] = relationship()
