from backend.schemas.video_metadata import VideoMetadataCreate


async def map_metadata_json(video_id: str, raw_json: dict) -> VideoMetadataCreate:
    return VideoMetadataCreate(
        raw_json=raw_json,
        video_id=video_id,
    )
