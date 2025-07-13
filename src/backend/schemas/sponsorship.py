from pydantic import BaseModel, UUID4, field_validator, HttpUrl
from typing import Optional


class SponsorLinksValidatorMixin:
    @field_validator("sponsor_links", mode="after")
    @classmethod
    def convert_sponsor_links_to_str(cls, v: Optional[list[HttpUrl]]) -> Optional[list[str]]:
        if v is None:
            return None
        return [str(link) for link in v]


class SponsorshipCreate(SponsorLinksValidatorMixin, BaseModel):
    sponsor_name: str
    sponsor_description: str | None = None
    sponsor_links: list[HttpUrl] | None = None
    sponsor_coupon_code: str | None = None
    sponsor_offer: str | None = None
    sponsored_segment_id: UUID4


class SponsorshipUpdate(SponsorLinksValidatorMixin, BaseModel):
    sponsor_name: str | None = None
    sponsor_description: str | None = None
    sponsor_links: list[HttpUrl] | None = None
    sponsor_coupon_code: str | None = None
    sponsor_offer: str | None = None
