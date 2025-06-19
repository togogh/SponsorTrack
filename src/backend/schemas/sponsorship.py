from pydantic import BaseModel, UUID4


class SponsorshipCreate(BaseModel):
    sponsor_name: str
    sponsor_description: str
    sponsor_links: list[str] | None = None
    sponsor_coupon_code: str | None = None
    sponsor_offer: str | None = None
    sponsored_segment_id: UUID4
    generator: str
    provider: str | None = None
    model: str | None = None


class SponsorshipUpdate(BaseModel):
    sponsor_name: str | None = None
    sponsor_description: str | None = None
    sponsor_links: list[str] | None = None
    sponsor_coupon_code: str | None = None
    sponsor_offer: str | None = None
    generator: str | None = None
    provider: str | None = None
    model: str | None = None
