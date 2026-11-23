"""Track administrator sign-in attempts."""

import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "admin_account",
        sa.Column("failed_sign_ins", sa.Integer(), server_default="0", nullable=False),
    )
    op.add_column("admin_account", sa.Column("retry_after", sa.DateTime(timezone=True)))


def downgrade() -> None:
    op.drop_column("admin_account", "retry_after")
    op.drop_column("admin_account", "failed_sign_ins")
