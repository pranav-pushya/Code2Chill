from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import discovery
from app.content_models import Project
from app.seed import seed_content


def test_initial_html_and_navigation_use_the_published_metadata(api_db, monkeypatch):
    client, connection = api_db
    template = Path(__file__).resolve().parents[2] / "frontend" / "index.html"
    monkeypatch.setattr(discovery, "BUILT_INDEX", template)
    monkeypatch.setenv("PUBLIC_SITE_URL", "https://club.example.test")
    with Session(connection, join_transaction_mode="create_savepoint") as db, db.begin():
        seed_content(db, include_demo=True)
        project = db.scalar(select(Project).where(Project.slug == "nexus"))
        project.public_snapshot = project.public_snapshot | {
            "title": "Games & design",
            "summary": 'A "hands-on" project.',
        }
        project.title = "Private draft"
        db.add(Project(slug="work-in-progress", title="Private draft", summary="Private draft"))

    url = "/projects/nexus"
    page = client.get(f"/web{url}?utm_source=test")
    fragment = client.get("/api/page-head", params={"path": url})
    assert page.status_code == fragment.status_code == 200
    assert fragment.text in page.text and page.text.count("<title") == 1
    assert "Games &amp; design | Code2Chill" in page.text
    assert "A &quot;hands-on&quot; project." in page.text
    assert "Private draft" not in page.text and "utm_source" not in page.text
    assert 'rel="canonical" href="https://club.example.test/projects/nexus"' in page.text
    assert 'content="https://club.example.test/share/code2chill.png"' in page.text
    assert 'name="twitter:card" content="summary_large_image"' in page.text
    assert 'id="root"' in page.text
    assert "Byte The Vibe | Code2Chill" in client.get("/web/events/byte-the-vibe").text
    mixed_case = client.get("/web/PROJECTS/nexus")
    assert mixed_case.status_code == 200
    assert 'data-page-path="/PROJECTS/nexus"' in mixed_case.text
    assert 'rel="canonical" href="https://club.example.test/projects/nexus"' in mixed_case.text
    team = client.get("/api/page-head", params={"path": "/TEAM"})
    assert team.status_code == 200
    assert 'rel="canonical" href="https://club.example.test/team"' in team.text

    for path in (
        "/projects/NEXUS",
        "/projects/work-in-progress",
        "/events/demo-event-handoff",
        "/absent",
    ):
        response = client.get("/web" + path)
        assert response.status_code == 404
        assert "noindex" in response.text and 'property="og:image"' not in response.text
    staff = client.get("/web/ADMIN/content/events/1/preview")
    assert (
        staff.status_code == 200 and "noindex" in staff.text and "Private draft" not in staff.text
    )
