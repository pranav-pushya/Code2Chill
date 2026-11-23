from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .domain import ClubDomain, choices
from .model_base import Base


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

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120))
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
    receipt: Mapped[UUID] = mapped_column(default=uuid4)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
