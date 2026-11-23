import csv
from datetime import datetime
from io import StringIO
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy import or_, select

from .admin_auth import Database, current_account
from .admin_models import (
    AdminAccount,
    AdminRole,
    AuditAction,
    AuditRecord,
    AuditTarget,
    RecruitmentReviewer,
)
from .domain import ClubDomain
from .publication import can_review_transition
from .recruitment_models import Application, ApplicationRoute, ApplicationStatus, RecruitmentCycle

router = APIRouter(prefix="/api/admin/recruitment", tags=["Application review"])
PAGE_SIZE = 50


def review_account(account: Annotated[AdminAccount, Depends(current_account)]):
    if account.role not in (AdminRole.ADMIN, AdminRole.REVIEWER):
        raise HTTPException(403, "Your account does not have access to application review.")
    return account


Reviewer = Annotated[AdminAccount, Depends(review_account)]


def reviewable_cycles(account):
    # Historical applications remain reviewable when a cycle closes or is unpublished.
    has_applications = (
        select(Application.id).where(Application.cycle_id == RecruitmentCycle.id).exists()
    )
    query = select(RecruitmentCycle.id, RecruitmentCycle.title).where(
        or_(
            RecruitmentCycle.public_snapshot["route"].as_string() == ApplicationRoute.LOCAL,
            RecruitmentCycle.route == ApplicationRoute.LOCAL,
            has_applications,
        )
    )
    if account.role == AdminRole.REVIEWER:
        query = query.join(RecruitmentReviewer).where(RecruitmentReviewer.account_id == account.id)
    return query


class CycleSummary(BaseModel):
    id: int
    title: str


def review_cycle(cycle_id: int, db: Database, account: Reviewer):
    cycle = db.execute(
        reviewable_cycles(account).where(RecruitmentCycle.id == cycle_id)
    ).one_or_none()
    if cycle is None:
        raise HTTPException(404, "Recruitment cycle unavailable.")
    return CycleSummary(id=cycle.id, title=cycle.title)


Cycle = Annotated[CycleSummary, Depends(review_cycle)]


class ApplicationSummary(BaseModel):
    id: int
    full_name: str
    domain: ClubDomain
    status: ApplicationStatus
    submitted_at: datetime


class DecisionRecord(BaseModel):
    previous_state: ApplicationStatus
    new_state: ApplicationStatus
    reviewer: str
    occurred_at: datetime


class ApplicationDetail(ApplicationSummary):
    university_email: str
    motivation: str | None
    portfolio_url: str | None
    allowed_statuses: list[ApplicationStatus]
    history: list[DecisionRecord]


class Decision(BaseModel):
    expected_status: ApplicationStatus
    status: ApplicationStatus


class ApplicationPage(BaseModel):
    cycle: CycleSummary
    applications: list[ApplicationSummary]
    has_more: bool
    can_export: bool


@router.get("", response_model=list[CycleSummary])
def list_cycles(db: Database, account: Reviewer):
    return db.execute(reviewable_cycles(account).order_by(RecruitmentCycle.id.desc())).all()


@router.get("/{cycle_id}/applications", response_model=ApplicationPage)
def list_applications(
    cycle: Cycle,
    db: Database,
    account: Reviewer,
    domain: ClubDomain | None = None,
    status: ApplicationStatus | None = None,
    page: Annotated[int, Query(ge=1, le=1000000)] = 1,
):
    query = select(
        Application.id,
        Application.full_name,
        Application.domain,
        Application.status,
        Application.submitted_at,
    ).where(Application.cycle_id == cycle.id)
    query = filter_applications(query, domain, status)
    rows = db.execute(
        query.order_by(Application.id.desc()).offset((page - 1) * PAGE_SIZE).limit(PAGE_SIZE + 1)
    ).all()
    return {
        "cycle": cycle,
        "applications": rows[:PAGE_SIZE],
        "has_more": len(rows) > PAGE_SIZE,
        "can_export": account.role == AdminRole.ADMIN,
    }


def filter_applications(query, domain, status):
    if domain:
        query = query.where(Application.domain == domain)
    if status:
        query = query.where(Application.status == status)
    return query


def csv_cell(value):
    if isinstance(value, datetime):
        return value.isoformat()
    text = str(value)
    if text.startswith(("\t", "\r", "\n")) or text.lstrip().startswith(
        ("=", "+", "-", "@", "＝", "＋", "－", "＠")
    ):
        return "'" + text
    return text


@router.post("/{cycle_id}/export.csv")
def export_applications(
    cycle: Cycle,
    account: Reviewer,
    db: Database,
    domain: ClubDomain | None = None,
    status: ApplicationStatus | None = None,
):
    if account.role != AdminRole.ADMIN:
        raise HTTPException(403, "Only administrators can export applications.")
    query = select(
        Application.full_name,
        Application.university_email,
        Application.domain,
        Application.status,
        Application.submitted_at,
    ).where(Application.cycle_id == cycle.id)
    query = filter_applications(query, domain, status).order_by(Application.id.desc())
    db.add(
        AuditRecord(
            actor_id=account.id,
            target_id=cycle.id,
            target_type=AuditTarget.RECRUITMENT_CYCLE,
            action=AuditAction.EXPORT,
        )
    )
    db.commit()

    def csv_rows():
        buffer = StringIO(newline="")
        writer = csv.writer(buffer)
        writer.writerow(["Name", "University email", "Domain", "Status", "Submitted at"])
        yield buffer.getvalue()
        for batch in db.execute(query.execution_options(yield_per=200)).partitions(200):
            buffer.seek(0)
            buffer.truncate()
            writer.writerows([csv_cell(value) for value in row] for row in batch)
            yield buffer.getvalue()

    return StreamingResponse(
        csv_rows(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="applications-{cycle.id}.csv"'},
    )


def get_application(db, cycle_id, application_id, *, lock=False):
    query = select(Application).where(
        Application.cycle_id == cycle_id, Application.id == application_id
    )
    # Keep the status and its audit history consistent across the two reads.
    item = db.scalar(query.with_for_update(read=not lock))
    if item is None:
        raise HTTPException(404, "Application unavailable.")
    return item


def detail_with_history(db, item):
    history = db.execute(
        select(
            AuditRecord.previous_state,
            AuditRecord.new_state,
            AdminAccount.email.label("reviewer"),
            AuditRecord.occurred_at,
        )
        .join(AdminAccount, AdminAccount.id == AuditRecord.actor_id)
        .where(
            AuditRecord.target_type == AuditTarget.APPLICATION,
            AuditRecord.target_id == item.id,
            AuditRecord.action == AuditAction.REVIEW,
        )
        .order_by(AuditRecord.occurred_at, AuditRecord.id)
    ).all()
    return ApplicationDetail(
        **ApplicationSummary.model_validate(item, from_attributes=True).model_dump(),
        university_email=item.university_email,
        motivation=item.motivation,
        portfolio_url=item.portfolio_url,
        allowed_statuses=[s for s in ApplicationStatus if can_review_transition(item.status, s)],
        history=[DecisionRecord.model_validate(row, from_attributes=True) for row in history],
    )


@router.get("/{cycle_id}/applications/{application_id}", response_model=ApplicationDetail)
def application_detail(application_id: int, cycle: Cycle, db: Database):
    return detail_with_history(db, get_application(db, cycle.id, application_id))


@router.patch("/{cycle_id}/applications/{application_id}", response_model=ApplicationDetail)
def record_decision(
    application_id: int, decision: Decision, cycle: Cycle, account: Reviewer, db: Database
):
    item = get_application(db, cycle.id, application_id, lock=True)
    if item.status != decision.expected_status:
        raise HTTPException(
            409, "Another reviewer changed this application. Reload it to see the current status."
        )
    if not can_review_transition(item.status, decision.status):
        raise HTTPException(409, "This decision is unavailable for the current status.")
    db.add(
        AuditRecord(
            actor_id=account.id,
            target_id=item.id,
            target_type=AuditTarget.APPLICATION,
            action=AuditAction.REVIEW,
            previous_state=item.status,
            new_state=decision.status,
        )
    )
    item.status = decision.status
    db.flush()
    result = detail_with_history(db, item)
    db.commit()
    return result
