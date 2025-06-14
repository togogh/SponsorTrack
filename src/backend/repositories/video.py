from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.video import Video
from backend.schemas.video import VideoCreate
from sqlalchemy import select


class VideoRepository:
    async def get_by_youtube_id(self, youtube_id: str, session: AsyncSession):
        stmt = select(Video).where(Video.youtube_id == youtube_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, video_data: VideoCreate, session: AsyncSession):
        video = Video(**video_data.model_dump())
        session.add(video)
        await session.commit()
        await session.refresh(video)
        return video
