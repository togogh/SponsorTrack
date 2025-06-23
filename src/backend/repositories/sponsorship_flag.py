from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.sponsorship_flag import SponsorshipFlag
from backend.schemas.sponsorship_flag import SponsorshipFlagCreate, SponsorshipFlagUpdate
from sqlalchemy import select, update
from pydantic import UUID4
from backend.models.sponsorship import Sponsorship


class SponsorshipFlagRepository:
    async def get_by_id(self, id: UUID4, session: AsyncSession):
        stmt = select(SponsorshipFlag).where(SponsorshipFlag.id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_sponsorship_id(self, sponsorship_id: UUID4, session: AsyncSession):
        stmt = select(SponsorshipFlag).join(Sponsorship).where(Sponsorship.id == sponsorship_id)
        result = await session.execute(stmt)
        segments = result.scalars().all()
        return segments

    async def add(self, data: SponsorshipFlagCreate, session: AsyncSession):
        record = SponsorshipFlag(**data.model_dump())
        session.add(record)
        await session.commit()
        await session.refresh(record)
        return record

    async def update(self, id: UUID4, data: SponsorshipFlagUpdate, session: AsyncSession):
        values = data.model_dump(exclude_unset=True)
        if not values:
            return
        await session.execute(
            update(SponsorshipFlag)
            .where(SponsorshipFlag.id == id)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        await session.commit()
