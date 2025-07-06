import pytest_asyncio
from backend.core.session import get_session
from backend.models.all import Base
from sqlalchemy import text


@pytest_asyncio.fixture(scope="session", autouse=True)
async def reset_test_schema():
    async with get_session("dev") as session:
        await session.execute(text("DROP SCHEMA IF EXISTS test CASCADE"))
        await session.execute(text("CREATE SCHEMA test"))
        await session.commit()

    async with get_session("test") as session:
        conn = await session.connection()
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(bind=sync_conn))
        await session.commit()

    yield


@pytest_asyncio.fixture(scope="class")
async def test_session(request):
    async with get_session("test") as session:
        request.cls.session = session
        yield


# def pytest_collection_modifyitems(items):
#     """Modifies test items in place to ensure test classes run in a given order."""
#     CLASS_ORDER = ["TestVideo", "TestSponsoredSegment"]
#     class_mapping = {item: item.cls.__name__ for item in items}

#     sorted_items = items.copy()
#     # Iteratively move tests of each class to the end of the test queue
#     for class_ in CLASS_ORDER:
#         sorted_items = [it for it in sorted_items if class_mapping[it] != class_] + [
#             it for it in sorted_items if class_mapping[it] == class_
#         ]
#     items[:] = sorted_items
