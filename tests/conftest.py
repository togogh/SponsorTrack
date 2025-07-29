import pytest_asyncio
import pytest
from backend.core.session import get_engine, get_session, session_dependency
from backend.core.settings import db_settings
from sqlalchemy import text
from httpx import AsyncClient, ASGITransport
from backend.main import app


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    async with get_engine(schema=db_settings.POSTGRES_TEST_SCHEMA) as engine:
        yield engine


@pytest_asyncio.fixture(scope="session", autouse=True)
async def reset_test_schema(test_engine):
    async with get_session(engine=test_engine) as session:
        result = await session.execute(
            text(f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = '{db_settings.POSTGRES_TEST_SCHEMA}'
        """)
        )
        tables = result.fetchall()

        if tables:
            table_names = [f"{db_settings.POSTGRES_TEST_SCHEMA}.{t[0]}" for t in tables]
            await session.execute(
                text(f"TRUNCATE TABLE {', '.join(table_names)} RESTART IDENTITY CASCADE")
            )
            await session.commit()


@pytest_asyncio.fixture(scope="session")
async def test_session(test_engine):
    async with get_session(engine=test_engine) as session:
        yield session


@pytest.fixture
def base_fields():
    return ["id", "created_at", "updated_at"]


@pytest.fixture(scope="session")
async def client(test_session):
    async def override_session_dependency():
        yield test_session

    app.dependency_overrides[session_dependency] = override_session_dependency
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.fixture
def fuzzy_match_threshold():
    return 85
