from datetime import datetime
from enum import StrEnum

from sqlalchemy import CheckConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from .time_rules import UTCDateTime


class PublicationState(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"


class PublicationFields:
    revision: Mapped[int] = mapped_column(default=1, server_default=text("1"))
    published_at: Mapped[datetime | None] = mapped_column(UTCDateTime())
    public_snapshot: Mapped[dict[str, object] | None] = mapped_column(JSONB(none_as_null=True))

    @declared_attr.directive
    def __mapper_args__(cls):
        return {"version_id_col": cls.revision}

    @property
    def publication_state(self) -> PublicationState:
        return (
            PublicationState.PUBLISHED
            if self.public_snapshot is not None
            else PublicationState.DRAFT
        )


def publication_integrity() -> CheckConstraint:
    return CheckConstraint(
        "revision > 0 AND ((public_snapshot IS NULL AND published_at IS NULL) OR "
        "(published_at IS NOT NULL AND jsonb_typeof(public_snapshot) = 'object' "
        "AND (public_snapshot->>'slug') IS NOT DISTINCT FROM slug))",
        name="publication",
    )
