import csv
from io import StringIO

from sqlalchemy import select, update
from test_admin_auth import HEADER, provision, sign_in
from test_admin_recruitment import cycle_with_applicant

from app.admin_models import AdminAccount, AdminRole, AuditAction, AuditRecord, RecruitmentReviewer


def test_csv_export_requires_admin_and_only_contains_selected_applications(api_db):
    client, conn = api_db
    cycle, _ = cycle_with_applicant(conn, "first", "=Private test")
    cycle_with_applicant(conn, "second", "Other")
    path = f"/api/admin/recruitment/{cycle}/export.csv"
    assert client.post(path, headers=HEADER).status_code == 401
    provision(conn, AdminRole.REVIEWER)
    actor = conn.scalar(select(AdminAccount.id))
    conn.execute(RecruitmentReviewer.__table__.insert().values(cycle_id=cycle, account_id=actor))
    sign_in(client)
    assert client.post(path, headers=HEADER).status_code == 403
    conn.execute(update(AdminAccount).values(role=AdminRole.ADMIN))
    assert client.post(path).status_code == 403
    empty = client.post(path + "?status=accepted", headers=HEADER)
    assert len(list(csv.reader(StringIO(empty.text)))) == 1
    response = client.post(path + "?domain=technical", headers=HEADER)
    rows = list(csv.reader(StringIO(response.text)))
    assert len(rows) == 2 and rows[1][:4] == [
        "'=Private test",
        "first@example.test",
        "technical",
        "pending",
    ]
    assert len(rows[0]) == 5
    assert response.headers["cache-control"] == "no-store"
    assert "attachment" in response.headers["content-disposition"]
    assert conn.scalars(
        select(AuditRecord.target_id).where(AuditRecord.action == AuditAction.EXPORT)
    ).all() == [cycle, cycle]
