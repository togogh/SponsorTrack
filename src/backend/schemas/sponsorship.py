from pydantic import BaseModel, UUID4, field_validator, HttpUrl, TypeAdapter
from typing import Optional


class SponsorLinksValidatorMixin:
    @field_validator("sponsor_links", mode="after")
    @classmethod
    def validate_sponsor_links(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        if v is None:
            return None
        ta_url = TypeAdapter(HttpUrl)
        for link in v:
            ta_url.validate_python(link)
        return v


class SponsorshipCreate(SponsorLinksValidatorMixin, BaseModel):
    sponsor_name: str
    sponsor_description: str | None = None
    sponsor_links: list[str] | None = None
    sponsor_coupon_code: str | None = None
    sponsor_offer: str | None = None
    sponsored_segment_id: UUID4


class SponsorshipUpdate(SponsorLinksValidatorMixin, BaseModel):
    sponsor_name: str | None = None
    sponsor_description: str | None = None
    sponsor_links: list[str] | None = None
    sponsor_coupon_code: str | None = None
    sponsor_offer: str | None = None
