from sqlalchemy import Column, String, Float, Date, UUID
from sponsortrack.backend.models.base import Base, fk
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Video(Base):
    youtube_id = Column(String, unique=True, nullable=False)
    language = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    channel_id = Column(
        UUID(as_uuid=True), ForeignKey(fk("channel.id")), nullable=False, index=True
    )
    channel = relationship("Channel", back_populates="videos")
    uploader_id = Column(String, nullable=False)
    upload_date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    duration = Column(Float, nullable=False)
    segments = relationship("Segment", back_populates="parent_video")
