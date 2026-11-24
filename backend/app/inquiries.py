import re

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .publication import valid_email_domain

router = APIRouter(prefix="/api", tags=["Inquiries"])


class InquirySubmission(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    full_name: str = Field(min_length=2, max_length=160)
    email: str = Field(min_length=3, max_length=254)
    category: str = Field(default="general", min_length=2, max_length=60)
    message: str = Field(min_length=5, max_length=2000)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        local, _, domain = value.lower().partition("@")
        if (
            not local
            or not domain
            or not re.fullmatch(
                r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*", local
            )
            or not valid_email_domain(domain)
        ):
            raise ValueError("Enter a valid university email address.")
        return value.lower()


@router.post("/inquiries")
async def submit_inquiry(inquiry: InquirySubmission) -> dict[str, str]:
    # Future integration: store in inquiry database or dispatch notification.
    return {
        "status": "received",
        "message": "Thank you! Your inquiry has been received by the Code2Chill coordinator desk.",
    }
