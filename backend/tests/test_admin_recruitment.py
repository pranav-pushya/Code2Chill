from uuid import uuid4

from sqlalchemy import delete, insert, select, update
from test_admin_auth import EMAIL, provision, sign_in

from app.admin_models import AdminAccount, AdminRole, RecruitmentReviewer
from app.recruitment_models import (
    Application,
    ApplicationRoute,
    RecruitmentCycle,
    RecruitmentDomain,
)

ROOT = "/api/admin/recruitment"


def cycle_with_applicant(connection, slug, name):
    cycle_id = connection.scalar(
        insert(RecruitmentCycle)
        .values(slug=slug, title=slug.title(), route=ApplicationRoute.LOCAL)
        .returning(RecruitmentCycle.id)
    )
    connection.execute(insert(RecruitmentDomain).values(cycle_id=cycle_id, domain="technical"))
    application_id = connection.scalar(
        insert(Application)
        .values(
            cycle_id=cycle_id,
            domain="technical",
            full_name=name,
            university_email=f"{slug}@example.test",
            motivation="Test motivation",
            attempt_id=uuid4(),
        )
        .returning(Application.id)
    )
    return cycle_id, application_id


def test_review_scope_filters_and_private_detail(api_db):
    client, connection = api_db
    first, first_id = cycle_with_applicant(connection, "spring", "First applicant")
    second, second_id = cycle_with_applicant(connection, "autumn", "Other applicant")
    path = f"{ROOT}/{first}/applications"
    other_path = f"{ROOT}/{second}/applications"
    assert client.get(path).status_code == 401
    provision(connection, AdminRole.REVIEWER)
    sign_in(client)
    assert client.get(ROOT).json() == []
    actor = connection.scalar(select(AdminAccount.id).where(AdminAccount.email == EMAIL))
    connection.execute(insert(RecruitmentReviewer).values(account_id=actor, cycle_id=first))
    assert client.get(ROOT).json() == [{"id": first, "title": "Spring"}]
    listing = client.get(path, params={"domain": "technical", "status": "pending"})
    assert listing.headers["cache-control"] == "no-store"
    assert [item["id"] for item in listing.json()["applications"]] == [first_id]
    assert "university_email" not in listing.text and "Other applicant" not in listing.text
    assert client.get(path + "?domain=content").json()["applications"] == []
    assert client.get(path + "?status=accepted").json()["applications"] == []
    assert client.get(path + "?page=0").status_code == 422
    detail = client.get(f"{path}/{first_id}")
    assert detail.json()["university_email"] == "spring@example.test"
    assert {"receipt", "attempt_id", "cycle_id"}.isdisjoint(detail.json())
    assert client.get(f"{path}/{second_id}").status_code == 404
    assert (
        client.get(other_path).status_code
        == client.get(f"{other_path}/{second_id}").status_code
        == 404
    )
    connection.execute(delete(RecruitmentReviewer).where(RecruitmentReviewer.account_id == actor))
    assert client.get(f"{path}/{first_id}").status_code == 404
    connection.execute(
        update(AdminAccount).where(AdminAccount.id == actor).values(role=AdminRole.ADMIN)
    )
    assert len(client.get(ROOT).json()) == 2
    assert client.get(other_path).status_code == 200
    connection.execute(
        update(AdminAccount).where(AdminAccount.id == actor).values(role=AdminRole.EDITOR)
    )
    assert (
        client.get(ROOT).status_code
        == client.get(path).status_code
        == client.get(f"{path}/{first_id}").status_code
        == 403
    )
