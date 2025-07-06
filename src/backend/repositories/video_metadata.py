from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from backend.models.all import VideoMetadata, Video
from backend.schemas.video_metadata import VideoMetadataCreate, VideoMetadataUpdate
from pydantic import UUID4


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

    async def update(self, id: UUID4, data: VideoMetadataUpdate, session: AsyncSession):
        values = data.model_dump(exclude_unset=True)
        if not values:
            return
        await session.execute(
            update(VideoMetadata)
            .where(VideoMetadata.id == id)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        await session.commit()
