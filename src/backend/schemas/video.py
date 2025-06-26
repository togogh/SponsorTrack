from pydantic import BaseModel, PastDate, field_validator
import requests


class VideoCreate(BaseModel):
    youtube_id: str
    language: str | None = None
    title: str | None = None
    upload_date: PastDate | None = None
    description: str | None = None
    duration: float | None = None
    channel: str | None = None

    @field_validator("youtube_id")
    @classmethod
    def ensure_video_exists_on_youtube(cls, youtube_id: str) -> str:
        # Check if video id belongs to an actual youtube video
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={youtube_id}&format=json"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise ValueError("Video id doesn't exist on Youtube")
        except Exception:
            raise ValueError("Unable to check validity of video id")
        return youtube_id


class VideoUpdate(BaseModel):
    language: str | None = None
    title: str | None = None
    upload_date: PastDate | None = None
    description: str | None = None
    duration: float | None = None
    channel: str | None = None
