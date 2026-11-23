from datetime import datetime
from enum import StrEnum

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, String, func, true
from sqlalchemy.orm import Mapped, mapped_column

from .domain import choices
from .model_base import Base, normalized_email, required_text
from .time_rules import UTCDateTime


class AdminRole(StrEnum):
    ADMIN = "admin"
    EDITOR = "editor"
    REVIEWER = "reviewer"


class AuditAction(StrEnum):
    CREATE = "create"
    UPDATE = "update"
    PUBLISH = "publish"
    UNPUBLISH = "unpublish"
    REVIEW = "review"


class AuditTarget(StrEnum):
    MEMBER = "member"
    EVENT = "event"
    PROJECT = "project"
    MEDIA_ASSET = "media_asset"
    RECRUITMENT_CYCLE = "recruitment_cycle"
    APPLICATION = "application"
    ADMIN_ACCOUNT = "admin_account"


class AdminAccount(Base):
    __tablename__ = "admin_account"
    __table_args__ = (normalized_email("email"), required_text("password_hash"))

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password_hash: Mapped[str] = mapped_column(String(512))
    role: Mapped[AdminRole] = mapped_column(choices(AdminRole))
    active: Mapped[bool] = mapped_column(Boolean, server_default=true())
    failed_sign_ins: Mapped[int] = mapped_column(server_default="0")
    retry_after: Mapped[datetime | None] = mapped_column(UTCDateTime())


class AdminSession(Base):
    __tablename__ = "admin_session"
    __table_args__ = (
        CheckConstraint("token_digest ~ '^[0-9a-f]{64}$'", name="digest_format"),
        CheckConstraint("expires_at > created_at", name="expiry_order"),
        CheckConstraint("revoked_at IS NULL OR revoked_at >= created_at", name="revocation_order"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("admin_account.id", ondelete="CASCADE"), index=True
    )
    token_digest: Mapped[str] = mapped_column(String(64), unique=True)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(UTCDateTime())
    revoked_at: Mapped[datetime | None] = mapped_column(UTCDateTime())


class RecruitmentReviewer(Base):
    __tablename__ = "recruitment_reviewer"

    cycle_id: Mapped[int] = mapped_column(
        ForeignKey("recruitment_cycle.id", ondelete="CASCADE"), primary_key=True
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("admin_account.id", ondelete="CASCADE"), primary_key=True
    )


class AuditRecord(Base):
    __tablename__ = "audit_record"
    __table_args__ = (Index("ix_audit_record_target", "target_type", "target_id", "occurred_at"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    actor_id: Mapped[int] = mapped_column(ForeignKey("admin_account.id"))
    action: Mapped[AuditAction] = mapped_column(choices(AuditAction))
    target_type: Mapped[AuditTarget] = mapped_column(choices(AuditTarget))
    target_id: Mapped[int]
    previous_state: Mapped[str | None] = mapped_column(String(32))
    new_state: Mapped[str | None] = mapped_column(String(32))
    occurred_at: Mapped[datetime] = mapped_column(UTCDateTime(), server_default=func.now())
