from pydantic import BaseModel, PastDate


class VideoCreate(BaseModel):
    youtube_id: str
    language: str | None = None
    title: str | None = None
    upload_date: PastDate | None = None
    description: str | None = None
    duration: float | None = None
    channel: str | None = None


class VideoUpdate(BaseModel):
    language: str | None = None
    title: str | None = None
    upload_date: PastDate | None = None
    description: str | None = None
    duration: float | None = None
    channel: str | None = None
