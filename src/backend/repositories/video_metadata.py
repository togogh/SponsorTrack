from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models.video_metadata import VideoMetadata
from backend.models.video import Video
from backend.schemas.video_metadata import VideoMetadataCreate


class VideoMetadataRepository:
    async def get_by_video_id(self, video_id: str, session: AsyncSession):
        stmt = select(VideoMetadata).join(Video).where(Video.id == video_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, mapped_metadata: VideoMetadataCreate, session: AsyncSession):
        video_metadata = VideoMetadata(**mapped_metadata.model_dump())
        session.add(video_metadata)
        await session.commit()
        await session.refresh(video_metadata)
        return video_metadata
