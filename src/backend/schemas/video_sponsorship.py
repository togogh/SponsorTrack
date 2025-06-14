from pydantic import BaseModel, HttpUrl, field_validator, model_validator
from typing import Optional
from backend.core.constants import constants
from urllib.parse import urlparse


class VideoSponsorshipRequest(BaseModel):
    id: Optional[str]
    url: Optional[HttpUrl]

    @field_validator("url")
    @classmethod
    def validate_youtube_url(cls, url: Optional[HttpUrl]) -> Optional[HttpUrl]:
        if not url:
            return None
        parse_result = urlparse(str(url))
        if parse_result.netloc not in constants.YOUTUBE_DOMAINS:
            raise ValueError("Url should be a valid Youtube url")
        return HttpUrl(url)

    @model_validator(mode="after")
    def ensure_url_or_id(self) -> "VideoSponsorshipRequest":
        if not self.id and not self.url:
            raise ValueError("One of `id` or `url` must be provided.")
        if self.id and self.url:
            raise ValueError("Only one of `id` or `url` should be provided.")
        return self


class VideoSponsorshipResponse(BaseModel):
    youtube_id: str
    sponsorship_info: str
