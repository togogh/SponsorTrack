from pydantic import BaseModel, UUID4, ConfigDict, field_validator
from typing_extensions import TypedDict
from typing import Optional
from langcodes import parse_tag, tag_is_valid


class TranscriptSegment(TypedDict):
    text: str
    start: float
    duration: float


class MetadataJson(BaseModel):
    __pydantic_config__ = ConfigDict(extra="allow")
    language: str | None
    title: str
    upload_date: str
    description: str
    duration: float
    channel: str

    @field_validator("language", mode="after")
    def validate_language(v: Optional[str]) -> Optional[str]:
        print("hello")
        if v is None:
            return None
        if not tag_is_valid(v):
            raise ValueError("Language code is not valid")
        parsed = parse_tag(v)
        parsed_language = [p[1] for p in parsed if p[0] == "language"][0]
        return parsed_language


class VideoMetadataCreate(BaseModel):
    video_id: UUID4
    raw_json: MetadataJson
    raw_transcript: list[TranscriptSegment] | None = None


class VideoMetadataUpdate(BaseModel):
    raw_json: MetadataJson | None = None
    raw_transcript: list[TranscriptSegment] | None = None
