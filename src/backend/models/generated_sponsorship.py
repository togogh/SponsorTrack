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
    generator = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    model = Column(String, nullable=False)
    prompt = Column(String)
    sponsorship_id = Column(UUID(as_uuid=True), ForeignKey(fk("sponsorship.id")), index=True)
    sponsorship = relationship("Sponsorship", back_populates="generated_sponsorships")
