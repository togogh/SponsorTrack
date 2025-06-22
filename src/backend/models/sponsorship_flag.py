from sqlalchemy import Column, String, UUID
from backend.models.base import Base, fk
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class SponsorshipFlag(Base):
    flagged_field = Column(String, nullable=False)
    correction = Column(String)
    generated_sponsorship_id = Column(
        UUID(as_uuid=True), ForeignKey(fk("generatedsponsorship.id")), nullable=False, index=True
    )
    generated_sponsorship = relationship("GeneratedSponsorship", back_populates="flags")
