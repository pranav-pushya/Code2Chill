from datetime import date

from sqlalchemy import Boolean, ForeignKey, String, Text, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .domain import ClubDomain, choices
from .model_base import Base


class MediaAsset(Base):
    __tablename__ = "media_asset"

    id: Mapped[int] = mapped_column(primary_key=True)
    storage_key: Mapped[str] = mapped_column(String(512))
    content_type: Mapped[str] = mapped_column(String(100))
    alt_text: Mapped[str] = mapped_column(String(300))
    credit: Mapped[str] = mapped_column(String(200))
    source_url: Mapped[str | None] = mapped_column(Text)
    approved_for_publication: Mapped[bool] = mapped_column(Boolean, server_default=false())


class Member(Base):
    __tablename__ = "member"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120))
    name: Mapped[str] = mapped_column(String(160))
    role_title: Mapped[str] = mapped_column(String(120))
    domain: Mapped[ClubDomain | None] = mapped_column(choices(ClubDomain))
    bio: Mapped[str | None] = mapped_column(Text)
    display_order: Mapped[int] = mapped_column(server_default="0")
    portrait_id: Mapped[int | None] = mapped_column(ForeignKey("media_asset.id"))
    portrait: Mapped[MediaAsset | None] = relationship()


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120))
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(Text)
    event_date: Mapped[date | None]
    venue: Mapped[str | None] = mapped_column(String(240))
    official_url: Mapped[str | None] = mapped_column(Text)
    poster_id: Mapped[int | None] = mapped_column(ForeignKey("media_asset.id"))
    poster: Mapped[MediaAsset | None] = relationship()


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120))
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(Text)
    repository_url: Mapped[str | None] = mapped_column(Text)
    demo_url: Mapped[str | None] = mapped_column(Text)
    event_id: Mapped[int | None] = mapped_column(ForeignKey("event.id"))
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

    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"), primary_key=True
    )
    position: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    member_id: Mapped[int | None] = mapped_column(ForeignKey("member.id", ondelete="SET NULL"))
    project: Mapped[Project] = relationship(back_populates="credits")
    member: Mapped[Member | None] = relationship()
