import pytest_asyncio
import pytest
from backend.core.session import get_engine, get_session
from sqlalchemy import text


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    async with get_engine(schema="test") as engine:
        yield engine


@pytest_asyncio.fixture(scope="session", autouse=True)
async def reset_test_schema(test_engine):
    async with get_session(engine=test_engine) as session:
        result = await session.execute(
            text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'test'
        """)
        )
        tables = result.fetchall()

        if tables:
            table_names = [f"test.{t[0]}" for t in tables]
            print(table_names)
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
