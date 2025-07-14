from pydantic import BaseModel, UUID4, model_validator
from typing import Any
from enum import Enum
from backend.models.flag import FlagStatus


class SponsorshipFlaggedField(str, Enum):
    sponsor_name = "sponsor_name"
    sponsor_description = "sponsor_description"
    sponsor_links = "sponsor_links"
    sponsor_coupon_code = "sponsor_coupon_code"
    sponsor_offer = "sponsor_offer"


class VideoFlaggedField(str, Enum):
    language = "language"
    title = "title"
    upload_date = "upload_date"
    description = "description"
    duration = "duration"
    channel = "channel"
    num_sponsored_segments = "num_sponsored_segments"


class SponsoredSegmentFlaggedField(str, Enum):
    start_time = "start_time"
    end_time = "end_time"
    subtitles = "subtitles"


class SponsorshipFlagPost(BaseModel):
    field_flagged: SponsorshipFlaggedField


class VideoFlagPost(BaseModel):
    field_flagged: VideoFlaggedField


class VideoFlagPostParams(BaseModel):
    video_id: UUID4 | None
    youtube_id: str | None

    @model_validator(mode="after")
    def ensure_one_id(self) -> "VideoFlagPostParams":
        if not self.video_id and not self.youtube_id:
            raise ValueError("One of `video_id` or `youtube_id` must be provided.")
        if self.video_id and self.youtube_id:
            raise ValueError("Only one of `video_id` or `youtube_id` should be provided.")
        return self


class SponsoredSegmentFlagPost(BaseModel):
    field_flagged: SponsoredSegmentFlaggedField


class FlagCreate(BaseModel):
    field_flagged: str
    value_flagged: Any
    status: FlagStatus = FlagStatus.pending
    entity_id: UUID4


class SponsorshipFlagCreate(FlagCreate):
    field_flagged: SponsorshipFlaggedField


class VideoFlagCreate(FlagCreate):
    field_flagged: VideoFlaggedField


class SponsoredSegmentFlagCreate(FlagCreate):
    field_flagged: SponsoredSegmentFlaggedField


class FlagUpdate(BaseModel):
    status: FlagStatus | None = None


class FlagPostResponse(BaseModel):
    id: UUID4
    field_flagged: str
    value_flagged: Any
    status: FlagStatus


class SponsorshipFlagPostResponse(FlagPostResponse):
    field_flagged: SponsorshipFlaggedField


class VideoFlagPostResponse(FlagPostResponse):
    field_flagged: VideoFlaggedField


class SponsoredSegmentFlagPostResponse(FlagPostResponse):
    field_flagged: SponsoredSegmentFlaggedField
