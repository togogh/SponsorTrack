from sqlalchemy import Column, String, Float, Date
from backend.models.base import Base
from sqlalchemy.orm import relationship


class Video(Base):
    youtube_id = Column(String, unique=True, nullable=False)
    language = Column(String, index=True)
    title = Column(String)
    # channel_id = Column(
    #     UUID(as_uuid=True), ForeignKey(fk("channel.id")), nullable=False, index=True
    # )
    # channel = relationship("Channel", back_populates="videos")
    uploader_id = Column(String)
    upload_date = Column(Date)
    description = Column(String)
    duration = Column(Float)
    sponsored_segments = relationship("SponsoredSegment", back_populates="parent_video")
