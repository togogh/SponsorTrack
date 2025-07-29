# import asyncssh
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from backend.core.settings import db_settings, deploy_settings
from backend.core.types import DeployEnv
from pydantic import PostgresDsn


@asynccontextmanager
async def get_engine(schema=None):
    port = db_settings.POSTGRES_LOCAL_PORT
    DATABASE_URL: PostgresDsn = (
        f"postgresql+asyncpg://{db_settings.POSTGRES_USER}:"
        f"{db_settings.POSTGRES_PASSWORD}@{db_settings.POSTGRES_SERVER}:{port}/"
        f"{db_settings.POSTGRES_DB}"
    )
    if not schema:
        if deploy_settings.DEPLOY_ENV == DeployEnv.PROD:
            schema = db_settings.POSTGRES_PROD_SCHEMA
        elif deploy_settings.DEPLOY_ENV == DeployEnv.TEST:
            schema = db_settings.POSTGRES_TEST_SCHEMA
        else:
            schema = db_settings.POSTGRES_DEV_SCHEMA
    engine = create_async_engine(
        DATABASE_URL, echo=True, execution_options={"schema_translate_map": {"env": schema}}
    )
    try:
        yield engine
    finally:
        await engine.dispose()


@asynccontextmanager
async def get_session(schema=None, engine=None):
    if not engine:
        async with get_engine(schema) as engine:
            async_session = sessionmaker(
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            async with async_session() as session:
                try:
                    yield session
                finally:
                    await session.close()
    else:
        async_session = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with async_session() as session:
            try:
                yield session
            finally:
                await session.close()


async def session_dependency():
    async with get_session() as session:
        yield session
