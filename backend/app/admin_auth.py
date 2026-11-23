import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Annotated

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, SecretStr
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from .admin_models import AdminAccount, AdminRole, AdminSession
from .database import request_session

router = APIRouter(prefix="/api/admin", tags=["Administrator access"])
Database = Annotated[Session, Depends(request_session)]
COOKIE = "__Host-code2chill_session"
SESSION_LIFETIME = timedelta(hours=8)
PASSWORD_HASHER = PasswordHasher()
# Keep failed credential checks comparable even when the address has no account.
_DUMMY_HASH = PASSWORD_HASHER.hash(secrets.token_urlsafe(32))


class Credentials(BaseModel):
    email: str
    password: SecretStr


class AccountInfo(BaseModel):
    email: str
    role: AdminRole


def token_digest(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def revoke_cookie_session(request: Request, db: Session, now: datetime) -> None:
    token = request.cookies.get(COOKIE)
    if token:
        db.execute(
            update(AdminSession)
            .where(
                AdminSession.token_digest == token_digest(token), AdminSession.revoked_at.is_(None)
            )
            .values(revoked_at=now)
        )


@router.post("/sign-in", response_model=AccountInfo)
def sign_in(credentials: Credentials, request: Request, response: Response, db: Database):
    denied = HTTPException(401, "Sign-in failed. Check your details or try again later.")
    email = credentials.email.strip().lower()
    password = credentials.password.get_secret_value()
    if not 1 <= len(email) <= 254 or "\x00" in email or not 1 <= len(password) <= 256:
        raise denied
    account = db.scalar(select(AdminAccount).where(AdminAccount.email == email).with_for_update())
    now = datetime.now(UTC)
    allowed = account and account.active and (not account.retry_after or now >= account.retry_after)
    stored_hash = account.password_hash if allowed else _DUMMY_HASH
    try:
        matches = PASSWORD_HASHER.verify(stored_hash, password)
    except (VerificationError, InvalidHashError):
        matches = False
    if not allowed or not matches:
        if allowed:
            account.failed_sign_ins += 1
            if account.failed_sign_ins >= 5:
                account.failed_sign_ins = 0
                account.retry_after = now + timedelta(minutes=5)
            db.commit()
        raise denied

    account.failed_sign_ins = 0
    account.retry_after = None
    if PASSWORD_HASHER.check_needs_rehash(stored_hash):
        account.password_hash = PASSWORD_HASHER.hash(password)
    revoke_cookie_session(request, db, now)
    token = secrets.token_urlsafe(32)
    db.add(
        AdminSession(
            account_id=account.id,
            token_digest=token_digest(token),
            created_at=now,
            expires_at=now + SESSION_LIFETIME,
        )
    )
    info = AccountInfo(email=account.email, role=account.role)
    db.commit()
    response.set_cookie(
        COOKIE,
        token,
        max_age=int(SESSION_LIFETIME.total_seconds()),
        secure=True,
        httponly=True,
        samesite="strict",
        path="/",
    )
    return info


def current_account(request: Request, db: Database) -> AdminAccount:
    token = request.cookies.get(COOKIE)
    if token:
        account = db.scalar(
            select(AdminAccount)
            .join(AdminSession, AdminSession.account_id == AdminAccount.id)
            .where(
                AdminSession.token_digest == token_digest(token),
                AdminSession.revoked_at.is_(None),
                AdminSession.expires_at > datetime.now(UTC),
                AdminAccount.active.is_(True),
            )
        )
        if account:
            return account
    raise HTTPException(401, "Sign in to continue.")


@router.get("/session", response_model=AccountInfo)
def read_session(account: Annotated[AdminAccount, Depends(current_account)]):
    return AccountInfo(email=account.email, role=account.role)


@router.post("/sign-out", status_code=204)
def sign_out(request: Request, response: Response, db: Database):
    revoke_cookie_session(request, db, datetime.now(UTC))
    db.commit()
    response.delete_cookie(COOKIE, path="/", secure=True, httponly=True, samesite="strict")


def event_editor(account: Annotated[AdminAccount, Depends(current_account)]) -> AdminAccount:
    if account.role not in (AdminRole.ADMIN, AdminRole.EDITOR):
        raise HTTPException(403, "You do not have permission to manage events.")
    return account
