from pydantic import BaseModel, HttpUrl, field_validator, model_validator
from typing import Optional
from urllib.parse import urlparse
from sponsortrack.backend.core.constants import constants


class SponsorshipRequest(BaseModel):
    id: Optional[str] = None
    url: Optional[HttpUrl] = None

    @field_validator("url")
    @classmethod
    def validate_url_domain(cls, url: HttpUrl):
        hostname = urlparse(str(url)).hostname
        if hostname not in constants.YOUTUBE_DOMAINS:
            raise ValueError(f"URL must be from one of: {', '.join(constants.YOUTUBE_DOMAINS)}")
        return url

    @model_validator
    @classmethod
    def validate_id_or_url(cls, values):
        if not values.get("id") and not values.get("url"):
            raise ValueError("Either 'id' or 'url' must be provided.")
        return values
