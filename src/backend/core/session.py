import asyncssh
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from backend.core.settings import db_settings
from pydantic import PostgresDsn


@asynccontextmanager
async def create_ssh_tunnel():
    async with asyncssh.connect(
        str(db_settings.SERVER_IP_ADDRESS),
        username=db_settings.SSH_USERNAME,
        client_keys=[db_settings.SSH_PKEY_PATH],
    ) as conn:
        listener = await conn.forward_local_port(
            listen_host="127.0.0.1", listen_port=0, dest_host="127.0.0.1", dest_port=5432
        )
        local_port = listener.get_port()

        try:
            yield local_port
        finally:
            listener.close()
            await listener.wait_closed()


async def get_engine(port=None):
    if port is None:
        port = db_settings.POSTGRES_PORT
    DATABASE_URL: PostgresDsn = (
        f"postgresql+asyncpg://{db_settings.POSTGRES_USER}:"
        f"{db_settings.POSTGRES_PASSWORD}@127.0.0.1:{port}/"
        f"{db_settings.POSTGRES_DB}"
    )
    engine = create_async_engine(DATABASE_URL, echo=True)
    return engine


@asynccontextmanager
async def get_session():
    async with create_ssh_tunnel() as local_port:
        engine = await get_engine(local_port)
        async_session = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with async_session() as session:
            yield session
        await engine.dispose()


async def session_dependency():
    async with get_session() as session:
        yield session
