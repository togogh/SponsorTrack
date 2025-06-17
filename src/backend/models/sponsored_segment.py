from sqlalchemy import Column, String, Float, UUID
from backend.models.base import Base, fk
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class SponsoredSegment(Base):
    sponsorblock_id = Column(String, unique=True)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    subtitles = Column(String)
    duration = Column(Float, nullable=False)
    parent_video_id = Column(
        UUID(as_uuid=True), ForeignKey(fk("video.id")), nullable=False, index=True
    )
    parent_video = relationship("Video", back_populates="sponsored_segments")
    # sponsorships = relationship("Sponsorship", back_populates="segment")
