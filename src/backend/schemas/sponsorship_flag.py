from pydantic import BaseModel, UUID4, model_validator
from enum import Enum


class FlaggedField(str, Enum):
    sponsor_name = "sponsor_name"
    sponsor_description = "sponsor_description"
    sponsor_links = "sponsor_links"
    sponsor_coupon_code = "sponsor_coupon_code"
    sponsor_offer = "sponsor_offer"


def validate_value_types(value_type: str):
    @model_validator(mode="after")
    def validator(cls, model, info):
        value = getattr(model, value_type)
        try:
            flagged_field = getattr(model, "flagged_field")
        except Exception:
            flagged_field = info.context.get("flagged_field")
        if flagged_field == "sponsor_links":
            if not isinstance(value, (list, type(None))):
                raise ValueError(f"{value_type} must be a list for sponsor_links")
        else:
            if not isinstance(value, (str, type(None))):
                raise ValueError(f"{value_type} must be a string")
        return model

    return validator


class SponsorshipFlagPost(BaseModel):
    flagged_field: FlaggedField
    corrected_value: str | list[str] | None = None

    validate_corrected_value = validate_value_types("corrected_value")


class SponsorshipFlagCreate(BaseModel):
    flagged_field: FlaggedField
    current_value: str | list[str] | None
    corrected_value: str | list[str] | None = None
    status: str = "open"
    sponsorship_id: UUID4

    validate_corrected_value = validate_value_types("corrected_value")
    validate_current_value = validate_value_types("current_value")


class SponsorshipFlagUpdate(BaseModel):
    current_value: str | list[str] | None = None
    corrected_value: str | list[str] | None = None
    status: str | None = None

    validate_corrected_value = validate_value_types("corrected_value")
    validate_current_value = validate_value_types("current_value")


class SponsorshipFlagPostResponse(BaseModel):
    id: UUID4
    flagged_field: FlaggedField
    current_value: str | list[str] | None
    corrected_value: str | list[str] | None
    status: str

    validate_corrected_value = validate_value_types("corrected_value")
    validate_current_value = validate_value_types("current_value")
