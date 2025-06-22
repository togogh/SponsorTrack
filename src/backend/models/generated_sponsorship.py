from sqlalchemy import Column, String, UUID
from backend.models.base import Base, fk
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY


class GeneratedSponsorship(Base):
    sponsor_name = Column(String, nullable=False)
    sponsor_description = Column(String)
    sponsor_links = Column(ARRAY(String))
    sponsor_coupon_code = Column(String)
    sponsor_offer = Column(String)
    generator = Column(String)
    provider = Column(String)
    model = Column(String)
    flags = sponsored_segment = relationship(
        "SponsorshipFlags", back_populates="generated_sponsorship"
    )
    sponsorship_id = Column(UUID(as_uuid=True), ForeignKey(fk("sponsoredsegment.id")), index=True)
    sponsorship = relationship("Sponsorship", back_populates="sponsorship")
