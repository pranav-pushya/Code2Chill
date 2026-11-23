from test_admin_auth import HEADER, provision, sign_in


def test_publish_checks_saved_preview_and_related_media(api_db):
    client, conn = api_db
    provision(conn)
    sign_in(client)
    root = "/api/admin/content"

    def create(kind, fields):
        result = client.post(f"{root}/{kind}", headers=HEADER, json={"fields": fields})
        assert result.status_code == 201
        return result.json()

    media = create(
        "media",
        {
            "storage_key": "a",
            "asset_url": "https://example.test/a.png",
            "credit": "Club",
            "alt_text": "Poster",
            "content_type": "image/png",
            "approved_for_publication": True,
        },
    )
    project = create(
        "projects",
        {
            "title": "Robotics",
            "slug": "robotics",
            "summary": "Student project",
            "credits": ["Student"],
            "screenshot_id": media["id"],
        },
    )
    path = f"{root}/projects/{project['id']}"
    preview = client.get(path + "/preview").json()
    assert not client.get("/api/projects").json()
    edit = client.put(
        f"{root}/media/{media['id']}",
        headers=HEADER,
        json={
            "revision": media["revision"],
            "fields": media["fields"] | {"credit": "Updated credit"},
        },
    )
    assert edit.status_code == 200
    assert client.post(path + "/publish", headers=HEADER, json=preview).status_code == 409
    preview = client.get(path + "/preview").json()
    assert client.post(path + "/publish", headers=HEADER, json=preview).status_code == 200
    assert client.get("/api/projects/robotics").json()["screenshot"]["credit"] == "Updated credit"
    assert client.post(path + "/publish", headers=HEADER, json=preview).status_code == 409
    settings = client.get(f"{root}/settings/1").json()
    assert (
        client.put(
            f"{root}/settings/1",
            headers=HEADER,
            json={
                "revision": settings["revision"],
                "fields": settings["fields"] | {"instagram": "https://example.test/profile"},
            },
        ).status_code
        == 200
    )
    assert client.get("/api/site-links").json() is None
    settings_preview = client.get(f"{root}/settings/1/preview").json()
    assert (
        client.post(f"{root}/settings/1/publish", headers=HEADER, json=settings_preview).status_code
        == 200
    )
    assert client.get("/api/site-links").json()["instagram"] == "https://example.test/profile"
