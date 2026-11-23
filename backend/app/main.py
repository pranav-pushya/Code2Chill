from contextlib import asynccontextmanager

from fastapi import FastAPI

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
