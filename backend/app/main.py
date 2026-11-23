from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

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


@app.get("/api/health")
def health(request: Request) -> dict[str, str]:
    try:
        with request.app.state.database.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="Database unavailable") from None
    return {"status": "ok"}
