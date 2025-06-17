from backend.schemas.video_metadata import VideoMetadataUpdate


async def map_metadata_transcript(raw_transcript: list) -> VideoMetadataUpdate:
    return VideoMetadataUpdate(
        raw_transcript=raw_transcript,
    )
