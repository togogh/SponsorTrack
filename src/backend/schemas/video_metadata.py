from pydantic import BaseModel, UUID4, ConfigDict
from typing_extensions import TypedDict


class TranscriptSegment(TypedDict):
    text: str
    start: float
    duration: float


class MetadataJson(TypedDict):
    __pydantic_config__ = ConfigDict(extra="allow")
    language: str | None
    title: str
    upload_date: str
    description: str
    duration: float
    channel: str


class VideoMetadataCreate(BaseModel):
    video_id: UUID4
    raw_json: MetadataJson
    raw_transcript: list[TranscriptSegment] | None = None


class VideoMetadataUpdate(BaseModel):
    raw_json: MetadataJson | None = None
    raw_transcript: list[TranscriptSegment] | None = None
