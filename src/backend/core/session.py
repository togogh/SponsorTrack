# import asyncssh
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from backend.core.settings import db_settings
from pydantic import PostgresDsn


# @asynccontextmanager
# async def create_ssh_tunnel():
#     async with asyncssh.connect(
#         str(db_settings.SERVER_IP_ADDRESS),
#         username=db_settings.SSH_USERNAME,
#         client_keys=[db_settings.SSH_PKEY_PATH],
#     ) as conn:
#         listener = await conn.forward_local_port(
#             listen_host="127.0.0.1", listen_port=0, dest_host="127.0.0.1", dest_port=5432
#         )
#         local_port = listener.get_port()

#         try:
#             yield local_port
#         finally:
#             listener.close()
#             await listener.wait_closed()


@asynccontextmanager
async def get_engine(schema=None):
    port = db_settings.POSTGRES_LOCAL_PORT
    DATABASE_URL: PostgresDsn = (
        f"postgresql+asyncpg://{db_settings.POSTGRES_USER}:"
        f"{db_settings.POSTGRES_PASSWORD}@127.0.0.1:{port}/"
        f"{db_settings.POSTGRES_DB}"
    )
    if not schema:
        schema = db_settings.POSTGRES_SCHEMA
    engine = create_async_engine(
        DATABASE_URL, echo=True, execution_options={"schema_translate_map": {"env": schema}}
    )
    try:
        yield engine
    finally:
        await engine.dispose()


# @asynccontextmanager
# async def get_ssh_engine(schema=None):
#     async with create_ssh_tunnel() as local_port:
#         engine = await get_engine(local_port, schema)
#         yield engine


@asynccontextmanager
async def get_session(schema=None, engine=None):
    if not engine:
        with await get_engine(schema) as engine:
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
    # await engine.dispose()


async def session_dependency(schema=None, engine=None):
    async with get_session(schema, engine) as session:
        yield session
