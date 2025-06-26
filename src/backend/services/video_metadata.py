from backend.core.settings import ws_settings
import yt_dlp
from fastapi import HTTPException
from backend.models.all import Video, VideoMetadata
from backend.repositories.all import VideoMetadataRepository, VideoRepository
from backend.schemas.all import VideoMetadataCreate, KeyMetadata, VideoUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple
from datetime import datetime
from pydantic import ValidationError


async def download_metadata(youtube_id):
    if ws_settings.WS_PROXY_UN and ws_settings.WS_PROXY_PW:
        proxy_str = f"http://{ws_settings.WS_PROXY_UN}:{ws_settings.WS_PROXY_PW}@p.webshare.io:80/"
    else:
        proxy_str = ""

    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "no_warnings": True,
        "format_sort": ["+size", "+br", "+res", "+fps"],
        "fragment_retries": 10,
        "retries": 10,
        "no_cache_dir": True,
        "proxy": proxy_str,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            info = ydl.extract_info(youtube_url, download=False)
            metadata = ydl.sanitize_info(info)
    except yt_dlp.utils.DownloadError:
        raise HTTPException(
            status_code=404,
            detail="Can't connect to yt_dlp",
        )

    return metadata


async def get_or_create_video_metadata(
    video: Video, video_metadata_repo: VideoMetadataRepository, session: AsyncSession
) -> VideoMetadata:
    # Get video metadata, create if not there
    video_metadata = await video_metadata_repo.get_by_video_id(video.id, session)
    if not video_metadata:
        metadata_json = await download_metadata(video.youtube_id)
        video_metadata_create = VideoMetadataCreate(
            raw_json=metadata_json,
            video_id=video.id,
        )
        video_metadata = await video_metadata_repo.add(video_metadata_create, session)
    return video_metadata


async def get_or_extract_metadata(
    video: Video,
    video_repo: VideoRepository,
    video_metadata_repo: VideoMetadataRepository,
    session: AsyncSession,
) -> Tuple[KeyMetadata, VideoMetadata]:
    video_metadata = await get_or_create_video_metadata(video, video_metadata_repo, session)
    key_fields = KeyMetadata.model_fields
    try:
        key_metadata = KeyMetadata.model_validate(
            {field: getattr(video, field) for field in key_fields}
        )
    except ValidationError:
        key_metadata = KeyMetadata.model_validate(
            {field: video_metadata.raw_json.get(field) for field in key_fields}
        )
        video_update = VideoUpdate(
            language=key_metadata.language,
            title=key_metadata.title,
            upload_date=datetime.strptime(key_metadata.upload_date, "%Y%m%d"),
            description=key_metadata.description,
            duration=key_metadata.duration,
            channel=key_metadata.channel,
        )
        await video_repo.update(video.id, video_update, session)
    return key_metadata, video_metadata
