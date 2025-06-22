from pydantic import BaseModel, UUID4, field_validator, model_validator


class SponsorshipFlagCreate(BaseModel):
    flagged_field: str
    current_value: str
    corrected_value: str | None = None
    status: str = "open"
    sponsorship_id: UUID4

    @field_validator("flagged_field")
    @classmethod
    def validate_flagged_field(cls, flagged_field: str) -> str:
        sponsor_fields = [
            "sponsor_name",
            "sponsor_description",
            "sponsor_links",
            "sponsor_coupon_code",
            "sponsor_offer",
        ]
        if flagged_field not in sponsor_fields:
            raise ValueError(f"flagged_field must be one of {', '.join(sponsor_fields)}")
        return flagged_field

    @model_validator(mode="after")
    def validate_value_types(self) -> "SponsorshipFlagCreate":
        if self.flagged_field == "sponsor_links":
            self.current_value: list[str] | None
            self.corrected_value_value: list[str] | None
        else:
            self.current_value: str | None
            self.corrected_value_value: str | None
        return self


class SponsorshipFlagUpdate(BaseModel):
    current_value: str | None = None
    corrected_value: str | None = None
    status: str | None = None
