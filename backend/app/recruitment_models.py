from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .domain import ClubDomain, choices
from .model_base import Base, normalized_email, required_text, route_slug


class ApplicationRoute(StrEnum):
    PENDING = "pending"
    EXTERNAL = "external"
    LOCAL = "local"


class ApplicationStatus(StrEnum):
    PENDING = "pending"
    SHORTLISTED = "shortlisted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class RecruitmentCycle(Base):
    __tablename__ = "recruitment_cycle"
    __table_args__ = (route_slug(), required_text("title"))

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True)
    title: Mapped[str] = mapped_column(String(200))
    opens_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    closes_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    eligibility: Mapped[str | None] = mapped_column(Text)
    route: Mapped[ApplicationRoute] = mapped_column(
        choices(ApplicationRoute), server_default=ApplicationRoute.PENDING
    )
    external_url: Mapped[str | None] = mapped_column(Text)
    domains: Mapped[list["RecruitmentDomain"]] = relationship(
        cascade="all, delete-orphan", back_populates="cycle"
    )


class RecruitmentDomain(Base):
    __tablename__ = "recruitment_domain"

    cycle_id: Mapped[int] = mapped_column(
        ForeignKey("recruitment_cycle.id", ondelete="CASCADE"), primary_key=True
    )
    domain: Mapped[ClubDomain] = mapped_column(choices(ClubDomain), primary_key=True)
    cycle: Mapped[RecruitmentCycle] = relationship(back_populates="domains")


class Application(Base):
    __tablename__ = "application"
    __table_args__ = (
        normalized_email("university_email"),
        required_text("full_name"),
        UniqueConstraint("cycle_id", "university_email", name="uq_application_cycle_email"),
        UniqueConstraint("cycle_id", "attempt_id", name="uq_application_cycle_attempt"),
        Index("ix_application_cycle_status_domain", "cycle_id", "status", "domain"),
        Index("ix_application_cycle_domain", "cycle_id", "domain"),
        ForeignKeyConstraint(
            ["cycle_id", "domain"],
            ["recruitment_domain.cycle_id", "recruitment_domain.domain"],
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    cycle_id: Mapped[int]
    domain: Mapped[ClubDomain] = mapped_column(choices(ClubDomain))
    full_name: Mapped[str] = mapped_column(String(160))
    university_email: Mapped[str] = mapped_column(String(254))
    motivation: Mapped[str | None] = mapped_column(Text)
    portfolio_url: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ApplicationStatus] = mapped_column(
        choices(ApplicationStatus), server_default=ApplicationStatus.PENDING
    )
    attempt_id: Mapped[UUID]
    receipt: Mapped[UUID] = mapped_column(default=uuid4, unique=True)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
