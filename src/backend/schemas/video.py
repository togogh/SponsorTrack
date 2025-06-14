from pydantic import BaseModel


class VideoCreate(BaseModel):
    youtube_id: str
