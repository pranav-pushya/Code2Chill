import argparse
import re
from getpass import getpass

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from .admin_auth import PASSWORD_HASHER
from .admin_models import AdminAccount, AdminRole
from .database import database_engine


def create_account(db: Session, email: str, password: str, role: AdminRole) -> None:
    email = email.strip().lower()
    if len(email) > 254 or not re.fullmatch(r"[^\s@\x00]+@[^\s@\x00]+", email):
        raise ValueError("Enter a valid email address.")
    if not 15 <= len(password) <= 256:
        raise ValueError("Use a password between 15 and 256 characters.")
    record_id = db.scalar(
        insert(AdminAccount)
        .values(email=email, password_hash=PASSWORD_HASHER.hash(password), role=role)
        .on_conflict_do_nothing(index_elements=[AdminAccount.email])
        .returning(AdminAccount.id)
    )
    if record_id is None:
        raise ValueError("An account already uses this email address.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Code2Chill staff account.")
    parser.add_argument("--email", required=True)
    parser.add_argument("--role", choices=list(AdminRole), required=True)
    args = parser.parse_args()
    password = getpass("New password (15 to 256 characters): ")
    if password != getpass("Confirm password: "):
        parser.exit(1, "Passwords did not match.\n")
    engine = database_engine()
    try:
        with Session(engine) as db, db.begin():
            create_account(db, args.email, password, AdminRole(args.role))
    except ValueError as exc:
        parser.exit(1, f"{exc}\n")
    finally:
        engine.dispose()
    print("Account created.")


if __name__ == "__main__":
    main()
