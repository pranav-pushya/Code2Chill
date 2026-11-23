from datetime import UTC, datetime

from fastapi import APIRouter
from sqlalchemy import select

from .admin_models import AdminAccount, AdminRole, RecruitmentReviewer
from .public_content import Database
from .publication import recruitment_state
from .recruitment_models import RecruitmentCycle

router = APIRouter(prefix="/api/recruitment", tags=["Recruitment"])


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
