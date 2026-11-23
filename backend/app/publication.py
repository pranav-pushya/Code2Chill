import re
from collections.abc import Mapping
from datetime import datetime
from urllib.parse import urlsplit

from sqlalchemy import select
from sqlalchemy.orm import Session

from .admin_models import (
    AdminAccount,
    AdminRole,
    AuditAction,
    AuditRecord,
    AuditTarget,
    RecruitmentReviewer,
)
from .content_models import Event, MediaAsset, Member, Project, RegistrationStatus, SiteSettings
from .publication_fields import PublicationState
from .recruitment_models import ApplicationRoute, ApplicationStatus, RecruitmentCycle
from .time_rules import as_utc, campus_date, window_is_open

Publishable = Event | Member | Project | RecruitmentCycle | SiteSettings

TARGETS = {
    SiteSettings: AuditTarget.SITE_SETTINGS,
    Event: AuditTarget.EVENT,
    Member: AuditTarget.MEMBER,
    Project: AuditTarget.PROJECT,
    RecruitmentCycle: AuditTarget.RECRUITMENT_CYCLE,
}
REVIEW_TRANSITIONS = {
    ApplicationStatus.PENDING: {
        ApplicationStatus.SHORTLISTED,
        ApplicationStatus.ACCEPTED,
        ApplicationStatus.REJECTED,
    },
    ApplicationStatus.SHORTLISTED: {ApplicationStatus.ACCEPTED, ApplicationStatus.REJECTED},
}


class PublicationError(ValueError):
    pass


class DraftConflict(PublicationError):
    pass


def https_link(value: str):
    try:
        url = urlsplit(value)
        if (
            url.scheme == "https"
            and url.hostname
            and url.username is None
            and url.password is None
            and not any(c.isspace() or ord(c) < 32 or c == "\\" for c in value)
        ):
            _ = url.port
            return url
    except ValueError:
        pass
    raise PublicationError("Use a valid HTTPS link.")


def university_signup(value: str):
    url = https_link(value)
    if url.netloc != "chitkarau.life" or not re.fullmatch(
        r"/events/[a-z0-9]+(?:-[a-z0-9]+)*/?", url.path
    ):
        raise PublicationError("Use the verified event-specific university registration link.")
    return value


def media_snapshot(asset: MediaAsset | None) -> dict[str, str] | None:
    if asset is None:
        return None
    if not asset.approved_for_publication:
        raise PublicationError("Approve the selected asset before publishing.")
    return {
        "storage_key": asset.storage_key,
        "asset_url": asset.asset_url,
        "alt_text": asset.alt_text,
        "credit": asset.credit,
    }


def public_payload(session: Session, record: Publishable) -> dict[str, object]:
    if isinstance(record, SiteSettings):
        links = {key: getattr(record, key) for key in ("university", "instagram", "linkedin")}
        for link in links.values():
            https_link(link)
        return links
    if isinstance(record, Member):
        return {
            "slug": record.slug,
            "name": record.name,
            "role_title": record.role_title,
            "domain": record.domain,
            "bio": record.bio,
            "display_order": record.display_order,
            "portrait": media_snapshot(record.portrait),
        }

    payload: dict[str, object] = {"slug": record.slug, "title": record.title}
    if isinstance(record, Event):
        if record.event_date is None:
            raise PublicationError("Set the confirmed event date before publishing.")
        if record.official_url:
            https_link(record.official_url)
        if record.registration_status == RegistrationStatus.OPEN and not record.registration_url:
            raise PublicationError("Open registration requires a verified university link.")
        if record.registration_url:
            university_signup(record.registration_url)
        return payload | {
            "summary": record.summary,
            "event_date": record.event_date.isoformat(),
            "starts_at": record.starts_at,
            "ends_at": record.ends_at,
            "venue": record.venue,
            "official_url": record.official_url,
            "registration_url": record.registration_url,
            "registration_status": record.registration_status,
            "is_demo": record.is_demo,
            "registration_opens_at": record.registration_opens_at,
            "registration_closes_at": record.registration_closes_at,
            "poster": media_snapshot(record.poster),
        }

    if isinstance(record, Project):
        for link in (record.repository_url, record.demo_url):
            if link:
                https_link(link)
        return payload | {
            "summary": record.summary,
            "repository_url": record.repository_url,
            "demo_url": record.demo_url,
            "credits": [credit.name for credit in record.credits],
            "screenshot": media_snapshot(record.screenshot),
        }

    if not (
        record.opens_at
        and record.closes_at
        and record.eligibility
        and record.eligibility.strip()
        and record.domains
        and record.route != ApplicationRoute.PENDING
    ):
        raise PublicationError(
            "Set both dates, eligibility, domains and an approved application route."
        )
    reviewer = session.scalar(
        select(RecruitmentReviewer.account_id)
        .join(AdminAccount, AdminAccount.id == RecruitmentReviewer.account_id)
        .where(
            RecruitmentReviewer.cycle_id == record.id,
            AdminAccount.active.is_(True),
            AdminAccount.role.in_((AdminRole.ADMIN, AdminRole.REVIEWER)),
        )
        .limit(1)
    )
    if reviewer is None:
        raise PublicationError("Assign an active reviewer before publishing the cycle.")
    if record.route == ApplicationRoute.EXTERNAL:
        if not record.external_url:
            raise PublicationError("Set the approved external application URL.")
        https_link(record.external_url)
    if record.route == ApplicationRoute.LOCAL:
        if not valid_email_domain(record.email_domain):
            raise PublicationError("Set the approved university email domain for this cycle.")
        if record.optional_field not in (None, "motivation", "portfolio_url"):
            raise PublicationError("Choose motivation, portfolio link or no optional field.")
    return payload | {
        "opens_at": record.opens_at,
        "closes_at": record.closes_at,
        "eligibility": record.eligibility,
        "route": record.route,
        "external_url": record.external_url if record.route == ApplicationRoute.EXTERNAL else None,
        "domains": sorted(item.domain.value for item in record.domains),
        "email_domain": record.email_domain if record.route == ApplicationRoute.LOCAL else None,
        "optional_field": record.optional_field if record.route == ApplicationRoute.LOCAL else None,
    }


def valid_email_domain(value):
    return (
        isinstance(value, str)
        and len(value) <= 253
        and re.fullmatch(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}", value)
        is not None
    )


def snapshot_for(session: Session, record: Publishable) -> dict[str, object]:
    return {
        key: as_utc(value).isoformat() if isinstance(value, datetime) else value
        for key, value in public_payload(session, record).items()
    }


def change_publication(
    session: Session,
    model: type[Publishable],
    record_id: int,
    *,
    expected_revision: int,
    actor_id: int,
    now: datetime,
    publish: bool,
) -> None:
    record = session.scalar(
        select(model)
        .where(model.id == record_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if record is None:
        raise PublicationError("The draft no longer exists.")
    if record.revision != expected_revision:
        raise DraftConflict("The saved draft changed. Reload it before publishing.")
    previous_state = record.publication_state
    if publish:
        record.public_snapshot = snapshot_for(session, record)
        record.published_at = as_utc(now)
    else:
        if previous_state is PublicationState.DRAFT:
            raise PublicationError("Only published content can be unpublished.")
        record.public_snapshot = None
        record.published_at = None
    record.revision += 1
    session.add(
        AuditRecord(
            actor_id=actor_id,
            action=AuditAction.PUBLISH if publish else AuditAction.UNPUBLISH,
            target_type=TARGETS[model],
            target_id=record_id,
            previous_state=previous_state,
            new_state=record.publication_state,
        )
    )
    session.flush()


def snapshot_instant(snapshot: Mapping[str, object], name: str) -> datetime | None:
    value = snapshot.get(name)
    return datetime.fromisoformat(value) if isinstance(value, str) else None


def event_registration(snapshot: Mapping[str, object], now: datetime) -> RegistrationStatus:
    scheduled_end = snapshot_instant(snapshot, "ends_at")
    event_day = campus_date(now).isoformat()
    status = RegistrationStatus(str(snapshot["registration_status"]))
    if (
        status is RegistrationStatus.ENDED
        or (scheduled_end is not None and as_utc(now) >= scheduled_end)
        or (scheduled_end is None and event_day > str(snapshot["event_date"]))
    ):
        return RegistrationStatus.ENDED
    if status in {RegistrationStatus.CLOSED, RegistrationStatus.FULL}:
        return status
    closes_at = snapshot_instant(snapshot, "registration_closes_at")
    if closes_at and as_utc(now) >= closes_at:
        return RegistrationStatus.CLOSED
    opens_at = snapshot_instant(snapshot, "registration_opens_at")
    if (
        status is RegistrationStatus.OPEN
        and snapshot.get("registration_url")
        and window_is_open(now, opens_at, closes_at)
    ):
        return status
    return RegistrationStatus.PENDING


def recruitment_state(snapshot: Mapping[str, object] | None, now: datetime) -> str:
    if snapshot is None:
        return "announcement"
    opens_at = snapshot_instant(snapshot, "opens_at")
    closes_at = snapshot_instant(snapshot, "closes_at")
    if opens_at is None or closes_at is None:
        return "announcement"
    if as_utc(now) < opens_at:
        return "scheduled"
    return "open" if window_is_open(now, opens_at, closes_at) else "closed"


def can_review_transition(current: ApplicationStatus, requested: ApplicationStatus) -> bool:
    return requested in REVIEW_TRANSITIONS.get(current, ())
