from sqlalchemy import Column, String, UUID
from backend.models.base import Base, fk
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class SponsorshipFlag(Base):
    flagged_field = Column(String, nullable=False)
    current_value = Column(String)
    corrected_value = Column(String)
    status = Column(String)
    sponsorship_id = Column(
        UUID(as_uuid=True), ForeignKey(fk("sponsorship.id")), nullable=False, index=True
    )
    sponsorship = relationship("Sponsorship", back_populates="flags")
