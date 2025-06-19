from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.sponsorship import Sponsorship
from backend.schemas.sponsorship import SponsorshipCreate, SponsorshipUpdate
from sqlalchemy import select, update
from pydantic import UUID4
from backend.models.sponsored_segment import SponsoredSegment
from backend.models.video import Video


class SponsorshipRepository:
    async def get_by_id(self, id: UUID4, session: AsyncSession):
        stmt = select(Sponsorship).where(Sponsorship.id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_segment_id(self, segment_id: UUID4, session: AsyncSession):
        stmt = select(Sponsorship).join(SponsoredSegment).where(SponsoredSegment.id == segment_id)
        result = await session.execute(stmt)
        segments = result.scalars().all()
        return segments

    async def get_by_video_id(self, video_id: UUID4, session: AsyncSession):
        stmt = (
            select(Sponsorship)
            .join(SponsoredSegment)
            .where(Sponsorship.sponsored_segment_id == SponsoredSegment.id)
            .join(Video)
            .where(Video.id == video_id)
        )
        result = await session.execute(stmt)
        segments = result.scalars().all()
        return segments

    async def add(self, data: SponsorshipCreate, session: AsyncSession):
        sponsored_segment = Sponsorship(**data.model_dump())
        session.add(sponsored_segment)
        await session.commit()
        await session.refresh(sponsored_segment)
        return sponsored_segment

    async def update(self, id: UUID4, data: SponsorshipUpdate, session: AsyncSession):
        values = data.model_dump(exclude_unset=True)
        if not values:
            return
        await session.execute(
            update(Sponsorship)
            .where(Sponsorship.id == id)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        await session.commit()
