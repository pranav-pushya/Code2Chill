from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from . import (
    admin_auth,
    admin_content,
    admin_events,
    admin_recruitment,
    discovery,
    public_content,
    recruitment,
)
from .database import database_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = database_engine()
    app.state.database = engine
    try:
        yield
    finally:
        engine.dispose()


app = FastAPI(
    title="Code2Chill API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url=None,
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)
app.include_router(admin_auth.router)
app.include_router(admin_content.router)
app.include_router(admin_events.router)
app.include_router(admin_recruitment.router)
app.include_router(public_content.router)
app.include_router(recruitment.router)
app.include_router(discovery.router)


@app.middleware("http")
async def protect_admin_requests(request: Request, call_next):
    if request.url.path.startswith("/api/recruitment"):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        return response
    if not request.url.path.startswith("/api/admin/"):
        return await call_next(request)
    # This API only serves its same-origin UI. Cross-origin scripts need CORS
    # permission to send this header, and ordinary HTML forms cannot send it.
    if (
        request.method not in ("GET", "HEAD", "OPTIONS")
        and request.headers.get("X-Code2Chill-Admin") != "1"
    ):
        response = JSONResponse(
            {"detail": "Administrator request header required."}, status_code=403
        )
    else:
        response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    return response


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    if request.url.path.startswith("/api/recruitment/"):
        field = exc.errors()[0]["loc"][-1]
        messages = {
            "university_email": "Enter a valid university email.",
            "full_name": "Enter your full name (up to 160 characters).",
            "domain": "Choose an enabled domain.",
            "portfolio_url": "Enter a valid HTTPS portfolio link.",
            "motivation": "Keep your motivation within 2,000 characters.",
            "code": "Enter the code from your email.",
        }
        return JSONResponse(
            {"detail": messages.get(field, "Check your application details.")}, status_code=422
        )
    credential_messages = {
        "/api/admin/sign-in": "Enter an email address and password.",
        "/api/admin/change-password": "Enter your current password and a new password.",
    }
    if message := credential_messages.get(request.url.path):
        return JSONResponse({"detail": message}, status_code=422)
    return await request_validation_exception_handler(request, exc)


@app.get("/api/health")
def health(request: Request) -> dict[str, str]:
    try:
        with request.app.state.database.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="Database unavailable") from None
    return {"status": "ok"}
