from backend.core.session import get_engine
from backend.models.all import Base
import asyncio


async def main():
    async with get_engine(schema="test") as engine:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(main())
