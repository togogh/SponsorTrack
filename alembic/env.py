from logging.config import fileConfig
from backend.core.session import get_engine
from backend.models.all import Base
from backend.core.settings import db_settings
from sqlalchemy import MetaData
from alembic import context
import asyncio
from backend.logs.config import get_logger


logger = get_logger(__name__)


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = Base.metadata
# target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def include_name(object, name, type_):
    if type_ == "schema" and name == db_settings.POSTGRES_PROD_SCHEMA:
        return True
    return False


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    raise Exception("Offline mode not supported with async or SSH tunneling.")


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    translated = MetaData()

    def translate_schema(table, to_schema, constraint, referred_schema):
        return to_schema

    for table in Base.metadata.tables.values():
        table.tometadata(
            translated,
            schema=db_settings.POSTGRES_PROD_SCHEMA if table.schema == "env" else table.schema,
            referred_schema_fn=translate_schema,
        )

    async with get_engine() as engine:
        async with engine.connect() as connection:
            await connection.run_sync(
                lambda sync_conn: context.configure(
                    connection=sync_conn,
                    target_metadata=translated,
                    compare_type=True,
                    include_schemas=True,
                    version_table_schema="public",
                    compare_server_default=True,
                    include_name=include_name,
                )
            )

            def do_run_migrations(sync_conn):
                return context.run_migrations()

            async with connection.begin():
                await connection.run_sync(do_run_migrations)


try:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())
except Exception as e:
    logger.error(e)
    raise e
