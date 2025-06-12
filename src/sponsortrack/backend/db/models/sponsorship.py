from sqlalchemy import Column, String, Boolean, UUID
from sponsortrack.backend.db.models.base import Base, fk
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import ARRAY


class Sponsorship(Base):
    sponsor_name = Column(String, nullable=False, index=True)
    sponsor_description = Column(String, nullable=False)
    sponsor_offer = Column(String)
    sponsor_code = Column(String)
    sponsor_links = Column(ARRAY(String))
    segment_id = Column(
        UUID(as_uuid=True), ForeignKey(fk("segment.id")), nullable=False, index=True
    )
    segment = relationship("Segment", back_populates="sponsorship_extracts")
    sponsor_id = Column(UUID(as_uuid=True), ForeignKey(fk("sponsor.id")), index=True)
    sponsor = relationship("Sponsor", back_populates="matched_extracts")
    checked_extract = Column(Boolean, nullable=False)
    confirmed_extract = Column(Boolean, nullable=False)
    checked_match = Column(Boolean, nullable=False)
    confirmed_match = Column(Boolean, nullable=False)
    model_used = Column(String, index=True)
    model_api = Column(String, index=True)
    model_provider = Column(String, index=True)
