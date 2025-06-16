from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from backend.models.video_metadata import VideoMetadata
from backend.models.video import Video
from backend.schemas.video_metadata import VideoMetadataCreate, VideoMetadataUpdateTranscript
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

    async def update_transcript(
        self, id: UUID4, transcript: VideoMetadataUpdateTranscript, session: AsyncSession
    ):
        await session.execute(
            update(VideoMetadata).where(VideoMetadata.id == id).values(**transcript.model_dump())
        )
        await session.commit()
