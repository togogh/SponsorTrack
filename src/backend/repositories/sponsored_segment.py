from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.video import Video
from backend.models.sponsored_segment import SponsoredSegment
from backend.schemas.sponsored_segment import (
    SponsoredSegmentCreate,
    SponsoredSegmentUpdateSubtitles,
)
from sqlalchemy import select, update
from pydantic import UUID4


class SponsoredSegmentRepository:
    async def get_by_id(self, id: UUID4, session: AsyncSession):
        stmt = select(SponsoredSegment).where(SponsoredSegment.id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_video_id(self, video_id: UUID4, session: AsyncSession):
        stmt = select(SponsoredSegment).join(Video).where(Video.id == video_id)
        result = await session.execute(stmt)
        segments = result.scalars().all()
        return segments

    async def add(self, sponsored_segment_data: SponsoredSegmentCreate, session: AsyncSession):
        sponsored_segment = SponsoredSegment(**sponsored_segment_data.model_dump())
        session.add(sponsored_segment)
        await session.commit()
        await session.refresh(sponsored_segment)
        return sponsored_segment

    async def update_subtitles(
        self, segment_id: UUID4, subtitles: SponsoredSegmentUpdateSubtitles, session: AsyncSession
    ):
        await session.execute(
            update(SponsoredSegment)
            .where(SponsoredSegment.id == segment_id)
            .values(**subtitles.model_dump())
        )
        await session.commit()
