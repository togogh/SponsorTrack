from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.flag import FlagCreate, FlagUpdate
from sqlalchemy import select, update
from pydantic import UUID4
from backend.models.all import Sponsorship, Video, Flag
from backend.models.flag import EntityType


class FlagRepository:
    async def get_by_id(self, id: UUID4, session: AsyncSession):
        stmt = select(Flag).where(Flag.id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_sponsorship_id(self, sponsorship_id: UUID4, session: AsyncSession):
        stmt = (
            select(Flag)
            .where(Flag.entity_flagged == "sponsorship")
            .join(Sponsorship, Flag.entity_id == Sponsorship.id)
            .where(Sponsorship.id == sponsorship_id)
        )
        result = await session.execute(stmt)
        segments = result.scalars().all()
        return segments

    async def get_by_video_id(self, video_id: UUID4, session: AsyncSession):
        stmt = (
            select(Flag)
            .where(Flag.entity_flagged == "video")
            .join(Video, Flag.entity_id == Video.id)
            .where(Video.id == video_id)
        )
        result = await session.execute(stmt)
        segments = result.scalars().all()
        return segments

    async def add(self, entity_flagged: EntityType, data: FlagCreate, session: AsyncSession):
        record = Flag(**data.model_dump())
        record.entity_flagged = entity_flagged
        session.add(record)
        await session.commit()
        await session.refresh(record)
        return record

    async def update(self, id: UUID4, data: FlagUpdate, session: AsyncSession):
        values = data.model_dump(exclude_unset=True)
        if not values:
            return
        await session.execute(
            update(Flag)
            .where(Flag.id == id)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        await session.commit()
