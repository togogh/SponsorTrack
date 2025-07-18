from pydantic import BaseModel, model_validator, NonNegativeFloat, UUID4


class SponsoredSegmentTimesValidatorMixin:
    @model_validator(mode="after")
    def validate_times(self) -> "SponsoredSegmentCreate":
        if self.start_time and self.end_time:
            if self.start_time > self.end_time:
                raise ValueError("Start time should be on or before end time")
        return self


class SponsoredSegmentCreate(SponsoredSegmentTimesValidatorMixin, BaseModel):
    sponsorblock_id: str | None = None
    start_time: NonNegativeFloat
    end_time: NonNegativeFloat
    parent_video_id: UUID4
    subtitles: str | None = None


class SponsoredSegmentUpdate(SponsoredSegmentTimesValidatorMixin, BaseModel):
    start_time: NonNegativeFloat | None = None
    end_time: NonNegativeFloat | None = None
    subtitles: str | None = None
