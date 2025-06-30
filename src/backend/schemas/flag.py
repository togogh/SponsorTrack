from pydantic import BaseModel, UUID4, HttpUrl, model_validator, FieldValidationInfo
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


class ValueFlaggedValidatorMixin:
    @model_validator(mode="after")
    def validate_value_flagged(cls, model, info: FieldValidationInfo):
        field = getattr(model, "field_flagged", None)

        if field is None:
            field = info.context.get("field_flagged")

        if field is None:
            raise ValueError("field_flagged must be provided on the model or via context")

        value = model.value_flagged

        if field == "sponsor_links":
            if value is not None:
                if not isinstance(value, list):
                    raise ValueError("value_flagged must be a list for sponsor_links")
                try:
                    value = [str(HttpUrl(link)) for link in value]
                except Exception as e:
                    raise ValueError(f"value_flagged must contain valid URLs: {e}")
            model.value_flagged = value
        else:
            if value is not None and not isinstance(value, str):
                raise ValueError(f"value_flagged must be a string for field_flagged '{field}'")

        return model


class SponsorshipFlagPost(BaseModel):
    field_flagged: SponsorshipFlaggedField


class VideoFlagPost(BaseModel):
    field_flagged: VideoFlaggedField


class FlagCreate(BaseModel):
    field_flagged: str
    value_flagged: str | None
    status: FlagStatus = "pending"
    entity_id: UUID4


class SponsorshipFlagCreate(ValueFlaggedValidatorMixin, FlagCreate):
    field_flagged: SponsorshipFlaggedField
    value_flagged: str | list[str] | None


class VideoFlagCreate(FlagCreate):
    field_flagged: VideoFlaggedField


class FlagUpdate(BaseModel):
    value_flagged: str | None = None
    status: FlagStatus | None = None


class SponsorshipFlagUpdate(ValueFlaggedValidatorMixin, FlagUpdate):
    value_flagged: str | list[str] | None = None
    status: FlagStatus | None = None


class SponsorshipFlagPostResponse(ValueFlaggedValidatorMixin, BaseModel):
    id: UUID4
    field_flagged: SponsorshipFlaggedField
    value_flagged: str | list[str] | None
    status: FlagStatus


class VideoFlagPostResponse(BaseModel):
    id: UUID4
    field_flagged: VideoFlaggedField
    value_flagged: str | None
    status: FlagStatus
