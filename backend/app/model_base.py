from sqlalchemy import CheckConstraint, MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


def required_text(column: str) -> CheckConstraint:
    return CheckConstraint(f"{column} ~ '[^[:space:]]'", name=f"{column}_present")


def route_slug() -> CheckConstraint:
    return CheckConstraint("slug ~ '^[a-z0-9]+(-[a-z0-9]+)*$'", name="slug_format")


def normalized_email(column: str) -> CheckConstraint:
    return CheckConstraint(
        f"{column} = lower(btrim({column})) AND {column} ~ '^[^[:space:]@]+@[^[:space:]@]+$'",
        name=f"{column}_normalized",
    )
