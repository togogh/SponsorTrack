from pydantic import BaseModel, UUID4


class VideoMetadataCreate(BaseModel):
    raw_json: dict
    video_id: UUID4


class VideoMetadataUpdateTranscript(BaseModel):
    raw_transcript: list
