"""Count unsuccessful checks for each issued recruitment code."""

import sqlalchemy as sa
from alembic import op

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "recruitment_email_challenge",
        sa.Column("failed_checks", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade():
    op.drop_column("recruitment_email_challenge", "failed_checks")
