from backend.schemas.video_metadata import VideoMetadataUpdateTranscript


async def map_metadata_transcript(raw_transcript: list) -> VideoMetadataUpdateTranscript:
    return VideoMetadataUpdateTranscript(
        raw_transcript=raw_transcript,
    )
