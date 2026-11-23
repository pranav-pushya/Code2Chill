"""Create the initial Code2Chill data model."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "admin_account",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("password_hash", sa.String(length=512), nullable=False),
        sa.Column(
            "role",
            sa.Enum(
                "admin",
                "editor",
                "reviewer",
                name="adminrole",
                native_enum=False,
                create_constraint=True,
            ),
            nullable=False,
        ),
        sa.Column("active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.CheckConstraint(
            "email = lower(btrim(email)) AND email ~ '^[^[:space:]@]+@[^[:space:]@]+$'",
            name=op.f("ck_admin_account_email_normalized"),
        ),
        sa.CheckConstraint(
            "password_hash ~ '[^[:space:]]'", name=op.f("ck_admin_account_password_hash_present")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_admin_account")),
        sa.UniqueConstraint("email", name=op.f("uq_admin_account_email")),
    )
    op.create_table(
        "media_asset",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("storage_key", sa.String(length=512), nullable=False),
        sa.Column("content_type", sa.String(length=100), nullable=False),
        sa.Column("alt_text", sa.String(length=300), nullable=False),
        sa.Column("credit", sa.String(length=200), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column(
            "approved_for_publication",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "NOT approved_for_publication OR (alt_text ~ '[^[:space:]]' AND credit ~ '[^[:space:]]')",
            name=op.f("ck_media_asset_approved_metadata"),
        ),
        sa.CheckConstraint(
            "content_type ~ '[^[:space:]]'", name=op.f("ck_media_asset_content_type_present")
        ),
        sa.CheckConstraint(
            "storage_key ~ '[^[:space:]]'", name=op.f("ck_media_asset_storage_key_present")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_media_asset")),
        sa.UniqueConstraint("storage_key", name=op.f("uq_media_asset_storage_key")),
    )
    op.create_table(
        "recruitment_cycle",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("opens_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("closes_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("eligibility", sa.Text(), nullable=True),
        sa.Column(
            "route",
            sa.Enum(
                "pending",
                "external",
                "local",
                name="applicationroute",
                native_enum=False,
                create_constraint=True,
            ),
            server_default="pending",
            nullable=False,
        ),
        sa.Column("external_url", sa.Text(), nullable=True),
        sa.Column("revision", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "public_snapshot",
            postgresql.JSONB(none_as_null=True, astext_type=sa.Text()),
            nullable=True,
        ),
        sa.CheckConstraint(
            "revision > 0 AND ((public_snapshot IS NULL AND published_at IS NULL) OR (published_at IS NOT NULL AND jsonb_typeof(public_snapshot) = 'object' AND (public_snapshot->>'slug') IS NOT DISTINCT FROM slug))",
            name=op.f("ck_recruitment_cycle_publication"),
        ),
        sa.CheckConstraint(
            "slug ~ '^[a-z0-9]+(-[a-z0-9]+)*$'", name=op.f("ck_recruitment_cycle_slug_format")
        ),
        sa.CheckConstraint(
            "title ~ '[^[:space:]]'", name=op.f("ck_recruitment_cycle_title_present")
        ),
        sa.CheckConstraint(
            "opens_at IS NULL OR closes_at IS NULL OR closes_at > opens_at",
            name=op.f("ck_recruitment_cycle_application_window"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_recruitment_cycle")),
        sa.UniqueConstraint("slug", name=op.f("uq_recruitment_cycle_slug")),
    )
    op.create_table(
        "admin_session",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("token_digest", sa.String(length=64), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "token_digest ~ '^[0-9a-f]{64}$'", name=op.f("ck_admin_session_digest_format")
        ),
        sa.CheckConstraint("expires_at > created_at", name=op.f("ck_admin_session_expiry_order")),
        sa.CheckConstraint(
            "revoked_at IS NULL OR revoked_at >= created_at",
            name=op.f("ck_admin_session_revocation_order"),
        ),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["admin_account.id"],
            name=op.f("fk_admin_session_account_id_admin_account"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_admin_session")),
        sa.UniqueConstraint("token_digest", name=op.f("uq_admin_session_token_digest")),
    )
    op.create_index(
        op.f("ix_admin_session_account_id"), "admin_session", ["account_id"], unique=False
    )
    op.create_table(
        "audit_record",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("actor_id", sa.Integer(), nullable=False),
        sa.Column(
            "action",
            sa.Enum(
                "create",
                "update",
                "publish",
                "unpublish",
                "review",
                name="auditaction",
                native_enum=False,
                create_constraint=True,
            ),
            nullable=False,
        ),
        sa.Column(
            "target_type",
            sa.Enum(
                "member",
                "event",
                "project",
                "media_asset",
                "recruitment_cycle",
                "application",
                "admin_account",
                name="audittarget",
                native_enum=False,
                create_constraint=True,
            ),
            nullable=False,
        ),
        sa.Column("target_id", sa.Integer(), nullable=False),
        sa.Column("previous_state", sa.String(length=32), nullable=True),
        sa.Column("new_state", sa.String(length=32), nullable=True),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["actor_id"], ["admin_account.id"], name=op.f("fk_audit_record_actor_id_admin_account")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_audit_record")),
    )
    op.create_index(
        "ix_audit_record_target",
        "audit_record",
        ["target_type", "target_id", "occurred_at"],
        unique=False,
    )
    op.create_table(
        "event",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("event_date", sa.Date(), nullable=True),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("registration_opens_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("registration_closes_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("venue", sa.String(length=240), nullable=True),
        sa.Column("is_demo", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("official_url", sa.Text(), nullable=True),
        sa.Column("registration_url", sa.Text(), nullable=True),
        sa.Column(
            "registration_status",
            sa.Enum(
                "pending",
                "open",
                "closed",
                "full",
                "ended",
                name="registrationstatus",
                native_enum=False,
                create_constraint=True,
            ),
            server_default="pending",
            nullable=False,
        ),
        sa.Column("poster_id", sa.Integer(), nullable=True),
        sa.Column("revision", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "public_snapshot",
            postgresql.JSONB(none_as_null=True, astext_type=sa.Text()),
            nullable=True,
        ),
        sa.CheckConstraint(
            "revision > 0 AND ((public_snapshot IS NULL AND published_at IS NULL) OR (published_at IS NOT NULL AND jsonb_typeof(public_snapshot) = 'object' AND (public_snapshot->>'slug') IS NOT DISTINCT FROM slug))",
            name=op.f("ck_event_publication"),
        ),
        sa.CheckConstraint("slug ~ '^[a-z0-9]+(-[a-z0-9]+)*$'", name=op.f("ck_event_slug_format")),
        sa.CheckConstraint(
            "starts_at IS NULL OR (event_date IS NOT NULL AND event_date = (starts_at AT TIME ZONE 'Asia/Kolkata')::date)",
            name=op.f("ck_event_campus_date"),
        ),
        sa.CheckConstraint("summary ~ '[^[:space:]]'", name=op.f("ck_event_summary_present")),
        sa.CheckConstraint("title ~ '[^[:space:]]'", name=op.f("ck_event_title_present")),
        sa.CheckConstraint(
            "ends_at IS NULL OR (starts_at IS NOT NULL AND ends_at > starts_at)",
            name=op.f("ck_event_event_duration"),
        ),
        sa.CheckConstraint(
            "registration_opens_at IS NULL OR registration_closes_at IS NULL OR registration_closes_at > registration_opens_at",
            name=op.f("ck_event_registration_window"),
        ),
        sa.ForeignKeyConstraint(
            ["poster_id"], ["media_asset.id"], name=op.f("fk_event_poster_id_media_asset")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_event")),
        sa.UniqueConstraint("slug", name=op.f("uq_event_slug")),
    )
    op.create_index(op.f("ix_event_event_date"), "event", ["event_date"], unique=False)
    op.create_table(
        "member",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("role_title", sa.String(length=120), nullable=False),
        sa.Column(
            "domain",
            sa.Enum(
                "technical",
                "content",
                "social_media",
                "promotion",
                name="clubdomain",
                native_enum=False,
                create_constraint=True,
            ),
            nullable=True,
        ),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("display_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("portrait_id", sa.Integer(), nullable=True),
        sa.Column("revision", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "public_snapshot",
            postgresql.JSONB(none_as_null=True, astext_type=sa.Text()),
            nullable=True,
        ),
        sa.CheckConstraint("name ~ '[^[:space:]]'", name=op.f("ck_member_name_present")),
        sa.CheckConstraint(
            "revision > 0 AND ((public_snapshot IS NULL AND published_at IS NULL) OR (published_at IS NOT NULL AND jsonb_typeof(public_snapshot) = 'object' AND (public_snapshot->>'slug') IS NOT DISTINCT FROM slug))",
            name=op.f("ck_member_publication"),
        ),
        sa.CheckConstraint(
            "role_title ~ '[^[:space:]]'", name=op.f("ck_member_role_title_present")
        ),
        sa.CheckConstraint("slug ~ '^[a-z0-9]+(-[a-z0-9]+)*$'", name=op.f("ck_member_slug_format")),
        sa.CheckConstraint("display_order >= 0", name=op.f("ck_member_display_order")),
        sa.ForeignKeyConstraint(
            ["portrait_id"], ["media_asset.id"], name=op.f("fk_member_portrait_id_media_asset")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_member")),
        sa.UniqueConstraint("slug", name=op.f("uq_member_slug")),
    )
    op.create_index("ix_member_display_order", "member", ["display_order", "id"], unique=False)
    op.create_table(
        "recruitment_domain",
        sa.Column("cycle_id", sa.Integer(), nullable=False),
        sa.Column(
            "domain",
            sa.Enum(
                "technical",
                "content",
                "social_media",
                "promotion",
                name="clubdomain",
                native_enum=False,
                create_constraint=True,
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["cycle_id"],
            ["recruitment_cycle.id"],
            name=op.f("fk_recruitment_domain_cycle_id_recruitment_cycle"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("cycle_id", "domain", name=op.f("pk_recruitment_domain")),
    )
    op.create_table(
        "recruitment_reviewer",
        sa.Column("cycle_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["admin_account.id"],
            name=op.f("fk_recruitment_reviewer_account_id_admin_account"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["cycle_id"],
            ["recruitment_cycle.id"],
            name=op.f("fk_recruitment_reviewer_cycle_id_recruitment_cycle"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("cycle_id", "account_id", name=op.f("pk_recruitment_reviewer")),
    )
    op.create_table(
        "application",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cycle_id", sa.Integer(), nullable=False),
        sa.Column(
            "domain",
            sa.Enum(
                "technical",
                "content",
                "social_media",
                "promotion",
                name="clubdomain",
                native_enum=False,
                create_constraint=True,
            ),
            nullable=False,
        ),
        sa.Column("full_name", sa.String(length=160), nullable=False),
        sa.Column("university_email", sa.String(length=254), nullable=False),
        sa.Column("motivation", sa.Text(), nullable=True),
        sa.Column("portfolio_url", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "pending",
                "shortlisted",
                "accepted",
                "rejected",
                name="applicationstatus",
                native_enum=False,
                create_constraint=True,
            ),
            server_default="pending",
            nullable=False,
        ),
        sa.Column("attempt_id", sa.Uuid(), nullable=False),
        sa.Column("receipt", sa.Uuid(), nullable=False),
        sa.Column(
            "submitted_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "full_name ~ '[^[:space:]]'", name=op.f("ck_application_full_name_present")
        ),
        sa.CheckConstraint(
            "university_email = lower(btrim(university_email)) AND university_email ~ '^[^[:space:]@]+@[^[:space:]@]+$'",
            name=op.f("ck_application_university_email_normalized"),
        ),
        sa.ForeignKeyConstraint(
            ["cycle_id", "domain"],
            ["recruitment_domain.cycle_id", "recruitment_domain.domain"],
            name=op.f("fk_application_cycle_id_recruitment_domain"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_application")),
        sa.UniqueConstraint("cycle_id", "attempt_id", name="uq_application_cycle_attempt"),
        sa.UniqueConstraint("cycle_id", "university_email", name="uq_application_cycle_email"),
        sa.UniqueConstraint("receipt", name=op.f("uq_application_receipt")),
    )
    op.create_index(
        "ix_application_cycle_domain", "application", ["cycle_id", "domain"], unique=False
    )
    op.create_index(
        "ix_application_cycle_status_domain",
        "application",
        ["cycle_id", "status", "domain"],
        unique=False,
    )
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("repository_url", sa.Text(), nullable=True),
        sa.Column("demo_url", sa.Text(), nullable=True),
        sa.Column("event_id", sa.Integer(), nullable=True),
        sa.Column("screenshot_id", sa.Integer(), nullable=True),
        sa.Column("revision", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "public_snapshot",
            postgresql.JSONB(none_as_null=True, astext_type=sa.Text()),
            nullable=True,
        ),
        sa.CheckConstraint(
            "revision > 0 AND ((public_snapshot IS NULL AND published_at IS NULL) OR (published_at IS NOT NULL AND jsonb_typeof(public_snapshot) = 'object' AND (public_snapshot->>'slug') IS NOT DISTINCT FROM slug))",
            name=op.f("ck_project_publication"),
        ),
        sa.CheckConstraint(
            "slug ~ '^[a-z0-9]+(-[a-z0-9]+)*$'", name=op.f("ck_project_slug_format")
        ),
        sa.CheckConstraint("summary ~ '[^[:space:]]'", name=op.f("ck_project_summary_present")),
        sa.CheckConstraint("title ~ '[^[:space:]]'", name=op.f("ck_project_title_present")),
        sa.ForeignKeyConstraint(["event_id"], ["event.id"], name=op.f("fk_project_event_id_event")),
        sa.ForeignKeyConstraint(
            ["screenshot_id"], ["media_asset.id"], name=op.f("fk_project_screenshot_id_media_asset")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_project")),
        sa.UniqueConstraint("slug", name=op.f("uq_project_slug")),
    )
    op.create_index(op.f("ix_project_event_id"), "project", ["event_id"], unique=False)
    op.create_table(
        "project_credit",
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("member_id", sa.Integer(), nullable=True),
        sa.CheckConstraint("name ~ '[^[:space:]]'", name=op.f("ck_project_credit_name_present")),
        sa.CheckConstraint("position >= 0", name=op.f("ck_project_credit_position")),
        sa.ForeignKeyConstraint(
            ["member_id"],
            ["member.id"],
            name=op.f("fk_project_credit_member_id_member"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
            name=op.f("fk_project_credit_project_id_project"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("project_id", "position", name=op.f("pk_project_credit")),
    )


def downgrade() -> None:
    op.drop_table("project_credit")
    op.drop_index(op.f("ix_project_event_id"), table_name="project")
    op.drop_table("project")
    op.drop_index("ix_application_cycle_status_domain", table_name="application")
    op.drop_index("ix_application_cycle_domain", table_name="application")
    op.drop_table("application")
    op.drop_table("recruitment_reviewer")
    op.drop_table("recruitment_domain")
    op.drop_index("ix_member_display_order", table_name="member")
    op.drop_table("member")
    op.drop_index(op.f("ix_event_event_date"), table_name="event")
    op.drop_table("event")
    op.drop_index("ix_audit_record_target", table_name="audit_record")
    op.drop_table("audit_record")
    op.drop_index(op.f("ix_admin_session_account_id"), table_name="admin_session")
    op.drop_table("admin_session")
    op.drop_table("recruitment_cycle")
    op.drop_table("media_asset")
    op.drop_table("admin_account")
