"""Configure local intake and store short-lived email challenges."""

import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("recruitment_cycle", sa.Column("email_domain", sa.String(253)))
    op.add_column("recruitment_cycle", sa.Column("optional_field", sa.String(16)))
    op.create_table(
        "recruitment_email_challenge",
        sa.Column(
            "cycle_id",
            sa.Integer(),
            sa.ForeignKey("recruitment_cycle.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("attempt_id", sa.Uuid(), primary_key=True),
        sa.Column("email", sa.String(254), nullable=False),
        sa.Column("digest", sa.String(64), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_recruitment_email_challenge_sent_at", "recruitment_email_challenge", ["sent_at"]
    )


def downgrade():
    op.drop_table("recruitment_email_challenge")
    op.drop_column("recruitment_cycle", "optional_field")
    op.drop_column("recruitment_cycle", "email_domain")
