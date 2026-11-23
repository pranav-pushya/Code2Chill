import hashlib
import re
import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import delete, func, select

from . import recruitment_mail
from .admin_models import AdminAccount, AdminRole, RecruitmentReviewer
from .domain import ClubDomain
from .public_content import Database
from .publication import https_link, recruitment_state, valid_email_domain
from .recruitment_models import Application, EmailChallenge, RecruitmentCycle

router = APIRouter(prefix="/api/recruitment", tags=["Recruitment"])
CODE_LIFETIME = timedelta(minutes=15)


class Identity(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    attempt_id: UUID
    university_email: str = Field(min_length=3, max_length=254)

    @field_validator("university_email")
    @classmethod
    def normalize(cls, value):
        local, _, domain = value.lower().partition("@")
        if (
            not re.fullmatch(
                r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*", local
            )
            or len(local) > 64
            or not valid_email_domain(domain)
        ):
            raise ValueError("Enter a valid university email.")
        return f"{local}@{domain}"


class Submission(Identity):
    full_name: str = Field(min_length=1, max_length=160, pattern=r"^[^\x00]+$")
    domain: ClubDomain
    motivation: str | None = Field(default=None, max_length=2000, pattern=r"^[^\x00]*$")
    portfolio_url: str | None = Field(default=None, max_length=2048)
    code: str = Field(min_length=1, max_length=64)

    @field_validator("portfolio_url")
    @classmethod
    def secure_link(cls, value):
        if value:
            https_link(value)
        return value or None


def reviewer_assigned():
    return (
        select(RecruitmentReviewer.account_id)
        .join(AdminAccount)
        .where(
            RecruitmentReviewer.cycle_id == RecruitmentCycle.id,
            AdminAccount.active.is_(True),
            AdminAccount.role.in_((AdminRole.ADMIN, AdminRole.REVIEWER)),
        )
        .exists()
    )


@router.get("")
def current_cycle(db: Database):
    now = datetime.now(UTC)
    rows = db.execute(
        select(RecruitmentCycle.id, RecruitmentCycle.public_snapshot).where(
            RecruitmentCycle.public_snapshot.is_not(None), reviewer_assigned()
        )
    )
    candidates = []
    for cycle_id, snap in rows:
        state = recruitment_state(snap, now)
        if state == "announcement":
            continue
        # Prefer the open cycle closing first, then the next scheduled or most recently closed.
        date = datetime.fromisoformat(
            snap["opens_at"] if state == "scheduled" else snap["closes_at"]
        )
        rank = (
            {"open": 0, "scheduled": 1, "closed": 2}[state],
            date.timestamp() * (-1 if state == "closed" else 1),
            cycle_id,
        )
        candidates.append((rank, cycle_id, snap, state))
    if not candidates:
        return {"state": "announcement"}
    _, cycle_id, snap, state = min(candidates)
    result = {
        key: snap.get(key)
        for key in (
            "title",
            "eligibility",
            "opens_at",
            "closes_at",
            "domains",
            "email_domain",
            "optional_field",
        )
    }
    result.update(state=state, id=cycle_id)
    if state == "open":
        if snap["route"] == "external":
            result.update(route="external", external_url=snap["external_url"])
    return result


def locked_cycle(db, cycle_id):
    cycle = db.scalar(
        select(RecruitmentCycle).where(RecruitmentCycle.id == cycle_id).with_for_update()
    )
    if not cycle:
        raise HTTPException(404, "Recruitment cycle unavailable.")
    return cycle


def check_open(db, cycle, email, now):
    snap = cycle.public_snapshot or {}
    if (
        snap.get("route") != "local"
        or recruitment_state(snap, now) != "open"
        or not db.scalar(
            select(reviewer_assigned())
            .select_from(RecruitmentCycle)
            .where(RecruitmentCycle.id == cycle.id)
        )
    ):
        raise HTTPException(409, "Applications are closed for this cycle.")
    if snap.get("email_domain") != email.partition("@")[2]:
        raise HTTPException(422, "Use the university email domain listed for this cycle.")
    return snap


def digest(code):
    return hashlib.sha256(code.encode()).hexdigest()


@router.post("/{cycle_id}/email-code", status_code=204)
def request_code(cycle_id: int, body: Identity, db: Database):
    cycle = locked_cycle(db, cycle_id)
    now = datetime.now(UTC)
    if not recruitment_mail.mail_ready():
        raise HTTPException(503, "Email verification is temporarily unavailable.")
    # The same saved attempt can request a fresh proof even after its challenge expires.
    challenge = db.get(EmailChallenge, (cycle_id, body.attempt_id))
    saved_attempt = db.scalar(
        select(Application.id).where(
            Application.cycle_id == cycle_id,
            Application.attempt_id == body.attempt_id,
            Application.university_email == body.university_email,
        )
    )
    if not saved_attempt:
        check_open(db, cycle, body.university_email, now)
    recent = (
        select(func.count())
        .select_from(EmailChallenge)
        .where(
            EmailChallenge.cycle_id == cycle_id, EmailChallenge.sent_at > now - timedelta(minutes=1)
        )
    )
    if db.scalar(recent) >= 20 or db.scalar(
        recent.where(EmailChallenge.email == body.university_email)
    ):
        raise HTTPException(429, "Wait a minute before requesting another code.")
    if challenge and challenge.email != body.university_email:
        raise HTTPException(409, "Start a new attempt for this email.")
    code = secrets.token_hex(8).upper()
    if not challenge:
        challenge = EmailChallenge(
            cycle_id=cycle_id, attempt_id=body.attempt_id, email=body.university_email
        )
        db.add(challenge)
    challenge.sent_at, challenge.digest = now, digest(code)
    db.execute(
        delete(EmailChallenge).where(
            EmailChallenge.cycle_id == cycle_id,
            EmailChallenge.sent_at < now - CODE_LIFETIME,
            EmailChallenge.attempt_id != body.attempt_id,
        )
    )
    db.commit()
    recruitment_mail.send_code(body.university_email, code)


def validate_new_application(db, cycle, body, now):
    snap = check_open(db, cycle, body.university_email, now)
    if body.domain not in snap["domains"]:
        raise HTTPException(422, "Choose a domain enabled for this cycle.")
    if any(
        getattr(body, key) and key != snap.get("optional_field")
        for key in ("motivation", "portfolio_url")
    ):
        raise HTTPException(422, "Use only the optional field available for this cycle.")
    if db.scalar(
        select(Application.id).where(
            Application.cycle_id == cycle.id, Application.university_email == body.university_email
        )
    ):
        raise HTTPException(409, "An application for this email already exists in this cycle.")
