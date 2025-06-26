from pydantic import BaseModel, UUID4


class VideoMetadataCreate(BaseModel):
    video_id: UUID4
    raw_json: dict
    raw_transcript: list | None = None


class VideoMetadataUpdate(BaseModel):
    raw_json: dict | None = None
    raw_transcript: list | None = None


class KeyMetadata(BaseModel):
    language: str | None
    title: str
    upload_date: str
    description: str
    duration: float
    channel: str
