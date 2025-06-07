from sqlalchemy import Column, String, Boolean
from sponsortrack.models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import ARRAY


class Extract(Base):
    sponsor_name = Column(String, nullable=False)
    sponsor_description = Column(String, nullable=False)
    sponsor_offer = Column(String)
    sponsor_code = Column(String)
    sponsor_links = Column(ARRAY(String))
    segment_id = Column(String, ForeignKey("segment.id"), nullable=False)
    segment = relationship("Segment", back_populates="sponsorship")
    sponsor_id = Column(String, ForeignKey("sponsor.id"))
    sponsor = relationship("Sponsor", back_populates="matched_sponsor")
    checked_extract = Column(Boolean, nullable=False)
    confirmed_extract = Column(Boolean, nullable=False)
    checked_match = Column(Boolean, nullable=False)
    confirmed_match = Column(Boolean, nullable=False)
    model_used = Column(String)
    model_api = Column(String)
    model_provider = Column(String)
