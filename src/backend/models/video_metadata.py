from sqlalchemy import Column, UUID, JSON
from backend.models.base import Base, fk
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class VideoMetadata(Base):
    raw_json = Column(JSON, nullable=False)
    raw_transcript = Column(JSON)
    video_id = Column(UUID(as_uuid=True), ForeignKey(fk("video.id")), nullable=False, index=True)
    video = relationship("Video", back_populates="video_metadata")
