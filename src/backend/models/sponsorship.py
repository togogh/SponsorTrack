from sqlalchemy import Column, String, UUID
from backend.models.base import Base, fk
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY


class Sponsorship(Base):
    sponsor_name = Column(String, nullable=False)
    sponsor_description = Column(String)
    sponsor_links = Column(ARRAY(String))
    sponsor_coupon_code = Column(String)
    sponsor_offer = Column(String)
    sponsored_segment_id = Column(
        UUID(as_uuid=True), ForeignKey(fk("sponsoredsegment.id")), nullable=False, index=True
    )
    sponsored_segment = relationship("SponsoredSegment", back_populates="sponsorships")
    generated_sponsorships = relationship("GeneratedSponsorship", back_populates="sponsorship")
    flags = relationship("SponsorshipFlag", back_populates="sponsorship")
