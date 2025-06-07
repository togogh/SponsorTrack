from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sponsortrack.backend.core.config import settings
from pydantic import PostgresDsn
from contextlib import contextmanager


def get_engine(port=None):
    if port is None:
        port = settings.POSTGRES_PORT
    DATABASE_URL: PostgresDsn = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{port}/{settings.POSTGRES_DB}"
    engine = create_engine(DATABASE_URL)
    return engine


@contextmanager
def get_remote_engine():
    with SSHTunnelForwarder(
        (settings.SERVER_IP_ADDRESS, 22),
        ssh_username=settings.SSH_USERNAME,
        ssh_pkey=settings.SSH_PKEY_PATH,
        remote_bind_address=("127.0.0.1", 5432),
    ) as tunnel:
        tunnel.start()
        try:
            engine = get_engine(tunnel.local_bind_port)
            yield engine
        finally:
            tunnel.stop()
