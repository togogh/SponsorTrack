from backend.schemas.video import VideoCreate


async def map_youtube_id_to_video(youtube_id: str) -> VideoCreate:
    return VideoCreate(youtube_id=youtube_id)
