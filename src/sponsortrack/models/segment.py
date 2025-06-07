from sqlalchemy import Column, String, Float
from sponsortrack.models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Segment(Base):
    sponsorblock_id = Column(String)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    subtitles = Column(String, nullable=False)
    duration = Column(Float, nullable=False)
    parent_video_id = Column(String, ForeignKey("video.id"), nullable=False, index=True)
    parent_video = relationship("Video", back_populates="segments")
    sponsorship = relationship("Sponsorship", back_populates="segment")
