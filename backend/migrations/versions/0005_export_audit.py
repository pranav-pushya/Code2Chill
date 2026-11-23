"""Record bulk application exports in the staff audit."""

from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def set_actions(values):
    name = op.f("ck_audit_record_auditaction")
    op.drop_constraint(name, "audit_record", type_="check")
    op.create_check_constraint(
        name, "audit_record", "action IN (" + ", ".join(repr(v) for v in values) + ")"
    )


actions = ("create", "update", "publish", "unpublish", "review")


def upgrade():
    set_actions((*actions, "export"))


def downgrade():
    op.execute("DELETE FROM audit_record WHERE action = 'export'")
    set_actions(actions)
