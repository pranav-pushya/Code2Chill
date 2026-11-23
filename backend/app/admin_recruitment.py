from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import or_, select

from .admin_auth import Database, current_account
from .admin_models import AdminAccount, AdminRole, RecruitmentReviewer
from .domain import ClubDomain
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


class ApplicationDetail(ApplicationSummary):
    university_email: str
    motivation: str | None
    portfolio_url: str | None


class ApplicationPage(BaseModel):
    cycle: CycleSummary
    applications: list[ApplicationSummary]
    has_more: bool


@router.get("", response_model=list[CycleSummary])
def list_cycles(db: Database, account: Reviewer):
    return db.execute(reviewable_cycles(account).order_by(RecruitmentCycle.id.desc())).all()


@router.get("/{cycle_id}/applications", response_model=ApplicationPage)
def list_applications(
    cycle: Cycle,
    db: Database,
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
    if domain:
        query = query.where(Application.domain == domain)
    if status:
        query = query.where(Application.status == status)
    rows = db.execute(
        query.order_by(Application.id.desc()).offset((page - 1) * PAGE_SIZE).limit(PAGE_SIZE + 1)
    ).all()
    return {"cycle": cycle, "applications": rows[:PAGE_SIZE], "has_more": len(rows) > PAGE_SIZE}


@router.get("/{cycle_id}/applications/{application_id}", response_model=ApplicationDetail)
def application_detail(application_id: int, cycle: Cycle, db: Database):
    item = db.scalar(
        select(Application).where(
            Application.cycle_id == cycle.id, Application.id == application_id
        )
    )
    if item is None:
        raise HTTPException(404, "Application unavailable.")
    return item
