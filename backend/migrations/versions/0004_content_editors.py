"""Add editable site links and hosted media URLs."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def audit_targets(include_settings):
    targets = [
        "member",
        "event",
        "project",
        "media_asset",
        "recruitment_cycle",
        "application",
        "admin_account",
    ]
    if include_settings:
        targets.append("site_settings")
    name = op.f("ck_audit_record_audittarget")
    op.drop_constraint(name, "audit_record", type_="check")
    op.create_check_constraint(
        name, "audit_record", "target_type IN (" + ", ".join(repr(t) for t in targets) + ")"
    )


def upgrade():
    audit_targets(True)
    op.add_column(
        "media_asset", sa.Column("revision", sa.Integer(), nullable=False, server_default="1")
    )
    op.add_column("media_asset", sa.Column("asset_url", sa.Text()))
    table = op.create_table(
        "site_settings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("revision", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("public_snapshot", JSONB(none_as_null=True)),
        sa.Column("university", sa.Text(), nullable=False),
        sa.Column("instagram", sa.Text(), nullable=False),
        sa.Column("linkedin", sa.Text(), nullable=False),
        sa.CheckConstraint("id = 1", name="singleton"),
    )
    op.bulk_insert(
        table,
        [
            {
                "id": 1,
                "university": "https://chitkarau.life/clubs/code2chill",
                "instagram": "https://www.instagram.com/code2chill.osl?utm_source=ig_web_button_share_sheet&lqvp=ZDNlZDc0MzIxNw%3D%3D",
                "linkedin": "https://www.linkedin.com/company/code2chill/posts/?feedView=all",
            }
        ],
    )


def downgrade():
    op.drop_table("site_settings")
    op.drop_column("media_asset", "asset_url")
    op.drop_column("media_asset", "revision")
    op.execute("DELETE FROM audit_record WHERE target_type = 'site_settings'")
    audit_targets(False)
