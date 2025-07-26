from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.all import Video, SponsoredSegment, Sponsorship
from backend.schemas.sponsored_segment import SponsoredSegmentCreate, SponsoredSegmentUpdate
from sqlalchemy import select, update
from pydantic import UUID4


class SponsoredSegmentRepository:
    async def get_by_id(self, id: UUID4, session: AsyncSession):
        stmt = select(SponsoredSegment).where(SponsoredSegment.id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_sponsorblock_id(self, id: str, session: AsyncSession):
        stmt = select(SponsoredSegment).where(SponsoredSegment.sponsorblock_id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_video_id(self, video_id: UUID4, session: AsyncSession):
        stmt = select(SponsoredSegment).join(Video).where(Video.id == video_id)
        result = await session.execute(stmt)
        segments = result.scalars().all()
        return segments

    async def get_by_sponsorship_id(self, sponsorship_id: UUID4, session: AsyncSession):
        stmt = select(SponsoredSegment).join(Sponsorship).where(Sponsorship.id == sponsorship_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, data: SponsoredSegmentCreate, session: AsyncSession):
        sponsored_segment = SponsoredSegment(**data.model_dump())
        session.add(sponsored_segment)
        await session.commit()
        await session.refresh(sponsored_segment)
        return sponsored_segment

    async def update(self, id: UUID4, data: SponsoredSegmentUpdate, session: AsyncSession):
        values = data.model_dump(exclude_unset=True)
        if not values:
            return
        await session.execute(
            update(SponsoredSegment)
            .where(SponsoredSegment.id == id)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        await session.commit()
