from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator

CAMPUS_ZONE = ZoneInfo("Asia/Kolkata")


def as_utc(instant: datetime) -> datetime:
    if instant.utcoffset() is None:
        raise ValueError("A timestamp must include its UTC offset.")
    return instant.astimezone(UTC)


def campus_time(instant: datetime) -> datetime:
    return as_utc(instant).astimezone(CAMPUS_ZONE)


def campus_date(instant: datetime) -> date:
    return campus_time(instant).date()


def window_is_open(now: datetime, opens_at: datetime | None, closes_at: datetime | None) -> bool:
    now = as_utc(now)
    return (opens_at is None or now >= as_utc(opens_at)) and (
        closes_at is None or now < as_utc(closes_at)
    )


class UTCDateTime(TypeDecorator[datetime]):
    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return as_utc(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return as_utc(value) if value is not None else None
