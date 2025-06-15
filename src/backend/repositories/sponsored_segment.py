from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.video import Video
from backend.models.sponsored_segment import SponsoredSegment
from backend.schemas.sponsored_segment import SponsoredSegmentCreate
from sqlalchemy import select


class SponsoredSegmentRepository:
    async def get_by_video_id(self, video_id: str, session: AsyncSession):
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
