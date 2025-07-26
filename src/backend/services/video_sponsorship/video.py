from pydantic import HttpUrl
from urllib.parse import urlparse, parse_qs
from fastapi import HTTPException
from backend.repositories.all import VideoRepository
from backend.schemas.all import VideoCreate
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.all import Video


async def extract_id_from_url(url: HttpUrl) -> str:
    # Extract video id from url

    parse_result = urlparse(str(url))

    try:
        if parse_result.path == "/watch":
            video_id = parse_qs(parse_result.query)["v"][0]
        elif parse_result.netloc == "youtu.be":
            video_id = parse_result.path.split("/")[1]
        elif parse_result.path.startswith("/embed/"):
            video_id = parse_result.path.split("/embed/")[1]
        elif parse_result.path.startswith("/shorts/"):
            video_id = parse_result.path.split("/shorts/")[1]
    except Exception:
        raise HTTPException(status_code=400, detail="Input url doesn't contain a valid video id")

    try:
        if len(video_id) > 0:
            return video_id
        else:
            raise Exception
    except Exception:
        raise HTTPException(status_code=400, detail="Input url doesn't contain a valid video id")


async def get_youtube_id(id: str, url: HttpUrl) -> str:
    return id or await extract_id_from_url(url)


async def create_video(
    youtube_id: str, video_repo: VideoRepository, session: AsyncSession
) -> Video:
    video_create_data = VideoCreate(youtube_id=youtube_id)
    video = await video_repo.add(video_create_data, session)
    return video


async def get_or_create_video(
    youtube_id: str, video_repo: VideoRepository, session: AsyncSession
) -> Video:
    video = await video_repo.get_by_youtube_id(youtube_id, session)
    if not video:
        video = await create_video(youtube_id, video_repo, session)
    return video
