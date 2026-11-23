from enum import StrEnum

from sqlalchemy import Enum


class ClubDomain(StrEnum):
    TECHNICAL = "technical"
    CONTENT = "content"
    SOCIAL_MEDIA = "social_media"
    PROMOTION = "promotion"


def choices(enum_class: type[StrEnum]) -> Enum:
    return Enum(
        enum_class,
        native_enum=False,
        create_constraint=True,
        validate_strings=True,
        values_callable=lambda members: [member.value for member in members],
    )
