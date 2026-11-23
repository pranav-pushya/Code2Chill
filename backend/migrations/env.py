from alembic import context
from sqlalchemy.engine import Connection

from app import admin_models, content_models, recruitment_models  # noqa: F401
from app.database import database_engine
from app.model_base import Base
from app.time_rules import UTCDateTime


def render_item(kind, item, autogen_context):
    if kind == "type" and isinstance(item, UTCDateTime):
        return "sa.DateTime(timezone=True)"
    return False


def configure_online(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=Base.metadata,
        render_item=render_item,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    context.configure(
        dialect_name="postgresql",
        target_metadata=Base.metadata,
        literal_binds=True,
        render_item=render_item,
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    connection = context.config.attributes.get("connection")
    if connection is not None:
        configure_online(connection)
    else:
        engine = database_engine()
        try:
            with engine.connect() as connection:
                configure_online(connection)
        finally:
            engine.dispose()
