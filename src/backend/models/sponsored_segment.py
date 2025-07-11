from sqlalchemy import Column, String, Float, UUID, Computed
from backend.models.base import Base, fk
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import NUMRANGE, ExcludeConstraint


class SponsoredSegment(Base):
    sponsorblock_id = Column(String, unique=True)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    subtitles = Column(String)
    parent_video_id = Column(
        UUID(as_uuid=True), ForeignKey(fk("video.id")), nullable=False, index=True
    )
    parent_video = relationship("Video", back_populates="sponsored_segments")
    sponsorships = relationship("Sponsorship", back_populates="sponsored_segment")

    time_range = Column(
        NUMRANGE,
        Computed("numrange(start_time::numeric, end_time::numeric)", persisted=True),
        nullable=False,
    )

    __table_args__ = (
        ExcludeConstraint(
            ("parent_video_id", "="),
            ("time_range", "&&"),
            name="no_overlap_per_video",
            using="gist",
        ),
    )
