from backend.core.session import get_engine
from backend.models.all import Base
import asyncio
import argparse


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", help="schema to refresh")
    args = parser.parse_args()
    async with get_engine(schema=args.schema) as engine:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(main())
