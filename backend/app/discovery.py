import os
from html import escape
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.exc import SQLAlchemyError

from .content_models import Event, Project
from .public_content import Database, published

router = APIRouter(include_in_schema=False)
BUILT_INDEX = Path(__file__).resolve().parents[2] / "frontend" / "dist" / "index.html"
DEFAULT_TITLE = "<title>Code2Chill | Chitkara University</title>"
SHARE_IMAGE = "/share/code2chill.png"
PAGES = {
    "/": (
        "Code2Chill | Chitkara University",
        "Explore the events, student projects and people of Code2Chill, the student-led technical club at Chitkara University.",
    ),
    "/about": (
        "About the club",
        "Learn how Code2Chill students build together through workshops, hackathons and coding events at Chitkara University.",
    ),
    "/events": (
        "Events",
        "Browse upcoming Code2Chill events, revisit past challenges and explore the club’s event gallery.",
    ),
    "/projects": (
        "Student projects",
        "Explore projects built by Code2Chill participants, meet their contributors and find available demos and source code.",
    ),
    "/team": (
        "Meet the team",
        "Meet the Code2Chill leadership, core members and teams behind technical work, content, social media and promotion.",
    ),
    "/join": (
        "Join the club",
        "Find recruitment information and express your interest in joining Code2Chill through the university club portal.",
    ),
    "/contact": (
        "Contact",
        "Find Code2Chill on the Chitkara University club portal, Instagram and LinkedIn.",
    ),
    "/join/apply": ("Recruitment application", "Apply to an open Code2Chill recruitment cycle."),
    "/status": ("Service status", "Check connectivity to the Code2Chill services."),
}


def describe(path, db):
    if path in PAGES:
        title, description = PAGES[path]
        return title, description, 200
    if path == "/admin" or path.startswith("/admin/"):
        return "Staff access", "Code2Chill staff area.", 200
    parts = path.strip("/").split("/")
    if len(parts) == 2 and parts[0] in {"events", "projects"}:
        model = Event if parts[0] == "events" else Project
        try:
            record = db.scalar(published(model).where(model.slug == parts[1]))
        except SQLAlchemyError:
            return "Content temporarily unavailable", "Please try again shortly.", 503
        if record:
            return record["title"], record["summary"], 200
        return f"{model.__name__} not found", "This item is unavailable.", 404
    return "Page not found", "Return to the Code2Chill homepage to explore the club.", 404


def page_head(request, path, db):
    path = "/" + path.strip("/")
    # React Router matches route names case-insensitively. Slugs still match the
    # published record exactly, as they do in the content API.
    section, separator, slug = path[1:].partition("/")
    canonical_path = "/" + section.lower() + separator + slug
    if canonical_path.lower() == "/join/apply":
        canonical_path = "/join/apply"
    title, description, status = describe(canonical_path, db)
    if canonical_path != "/":
        title += " | Code2Chill"
    title = escape(title)
    description = escape(" ".join(description.split())[:300])
    origin = (os.getenv("PUBLIC_SITE_URL") or str(request.base_url)).rstrip("/")
    canonical = escape(origin + quote(canonical_path, safe="/"))
    image = escape(origin + SHARE_IMAGE)
    tags = [
        f'<title data-page-path="{escape(path)}">{title}</title>',
        f'<meta name="description" content="{description}">',
    ]
    if status != 200 or canonical_path in {"/status", "/join/apply"} or section.lower() == "admin":
        tags.append('<meta name="robots" content="noindex, nofollow">')
    else:
        tags.extend(
            [
                f'<link rel="canonical" href="{canonical}">',
                '<meta property="og:type" content="website">',
                '<meta property="og:site_name" content="Code2Chill">',
                f'<meta property="og:title" content="{title}">',
                f'<meta property="og:description" content="{description}">',
                f'<meta property="og:url" content="{canonical}">',
                f'<meta property="og:image" content="{image}">',
                '<meta property="og:image:width" content="1200">',
                '<meta property="og:image:height" content="630">',
                '<meta property="og:image:alt" content="Code2Chill student technical club at Chitkara University">',
                '<meta name="twitter:card" content="summary_large_image">',
                f'<meta name="twitter:title" content="{title}">',
                f'<meta name="twitter:description" content="{description}">',
                f'<meta name="twitter:image" content="{image}">',
            ]
        )
    return "\n".join(tags), status


@router.get("/api/page-head", response_class=HTMLResponse)
def metadata(request: Request, path: str, db: Database):
    head, status = page_head(request, path, db)
    return HTMLResponse(head, status_code=status, headers={"Cache-Control": "no-store"})


@router.api_route("/web/{path:path}", methods=["GET", "HEAD"], response_class=HTMLResponse)
def web_document(request: Request, path: str, db: Database):
    head, status = page_head(request, path, db)
    shell = BUILT_INDEX.read_text(encoding="utf-8")
    return HTMLResponse(
        shell.replace(DEFAULT_TITLE, head, 1),
        status_code=status,
        headers={"Cache-Control": "no-cache"},
    )
