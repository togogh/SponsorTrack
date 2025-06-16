from pydantic import BaseModel, PastDate


class VideoCreate(BaseModel):
    youtube_id: str


class VideoUpdateMetadata(BaseModel):
    language: str
    title: str
    upload_date: PastDate
    description: str
    duration: float
