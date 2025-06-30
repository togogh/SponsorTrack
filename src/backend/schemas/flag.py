from pydantic import BaseModel, UUID4, model_validator
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


def validate_value_types(field_flagged: str):
    @model_validator(mode="after")
    def validator(cls, model, info):
        try:
            value = getattr(model, field_flagged)
        except Exception:
            value = info.context.get(field_flagged)

        if field_flagged == "sponsor_links":
            if not isinstance(value, (list, type(None))):
                raise ValueError(f"{field_flagged} must be a list for sponsor_links")
        else:
            if not isinstance(value, (str, type(None))):
                raise ValueError(f"{field_flagged} must be a string")
        return model

    return validator


class SponsorshipFlagPost(BaseModel):
    field_flagged: SponsorshipFlaggedField


class VideoFlagPost(BaseModel):
    field_flagged: VideoFlaggedField


class FlagCreate(BaseModel):
    field_flagged: str
    value_flagged: str | None
    status: FlagStatus = "pending"
    entity_id: UUID4


class SponsorshipFlagCreate(FlagCreate):
    field_flagged: SponsorshipFlaggedField
    value_flagged: str | list[str] | None

    validate_value = validate_value_types("field_flagged")


class VideoFlagCreate(FlagCreate):
    field_flagged: VideoFlaggedField


class FlagUpdate(BaseModel):
    value_flagged: str | None = None
    status: FlagStatus | None = None


class SponsorshipFlagUpdate(FlagUpdate):
    value_flagged: str | list[str] | None = None
    status: FlagStatus | None = None

    validate_value = validate_value_types("field_flagged")


class SponsorshipFlagPostResponse(BaseModel):
    id: UUID4
    field_flagged: SponsorshipFlaggedField
    value_flagged: str | list[str] | None
    status: FlagStatus

    validate_value = validate_value_types("field_flagged")


class VideoFlagPostResponse(BaseModel):
    id: UUID4
    field_flagged: VideoFlaggedField
    value_flagged: str | None
    status: FlagStatus
