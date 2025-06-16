from pydantic import BaseModel, model_validator, PositiveFloat, UUID4


class SponsoredSegmentCreate(BaseModel):
    sponsorblock_id: str
    start_time: PositiveFloat
    end_time: PositiveFloat
    duration: PositiveFloat
    parent_video_id: UUID4

    @model_validator(mode="after")
    def validate_times(self) -> "SponsoredSegmentCreate":
        if self.start_time > self.end_time:
            raise ValueError("Start time should be on or before end time")
        if self.duration != self.end_time - self.start_time:
            raise ValueError("Duration doesn't match start and end times")
        return self


class SponsoredSegmentUpdateSubtitles(BaseModel):
    subtitles: str
