from sqlalchemy import select
from test_admin_auth import HEADER, provision, sign_in

from app.admin_models import AdminRole, AuditRecord

BASE = "/api/admin/content"


def test_content_edits_and_permissions(api_db):
    client, conn = api_db
    member = {
        "name": "Test member",
        "slug": "test-member",
        "role_title": "Lead",
        "display_order": 1,
    }
    assert client.get(f"{BASE}/members").status_code == 401
    provision(conn, AdminRole.EDITOR)
    sign_in(client)

    def create(kind, fields):
        return client.post(f"{BASE}/{kind}", headers=HEADER, json={"fields": fields})

    media = create(
        "media",
        {
            "storage_key": "portraits/lead",
            "content_type": "image/webp",
            "alt_text": "Lead",
            "credit": "Club",
            "approved_for_publication": True,
            "asset_url": "https://example.test/lead.webp",
        },
    ).json()
    member["portrait_id"] = media["id"]
    saved = create("members", member).json()
    path = f"{BASE}/members/{saved['id']}"
    assert client.get(path).json() == saved
    assert client.get("/api/team").json() == []
    edit = {"revision": saved["revision"], "fields": member | {"name": "Updated"}}
    assert client.put(path, headers=HEADER, json=edit).json()["fields"]["name"] == "Updated"
    assert client.put(path, headers=HEADER, json=edit).status_code == 409
    project = create(
        "projects",
        {"slug": "demo", "title": "Demo", "summary": "Summary", "credits": ["Ada", "Bea"]},
    ).json()
    fields = project["fields"] | {"credits": ["Bea", "Ada", "Cy"]}
    assert (
        client.put(
            f"{BASE}/projects/{project['id']}",
            headers=HEADER,
            json={"fields": fields, "revision": project["revision"]},
        ).json()["fields"]["credits"]
        == fields["credits"]
    )
    assert client.get(f"{BASE}/settings/1").status_code == 403
    assert len(conn.execute(select(AuditRecord.id)).all()) == 5
