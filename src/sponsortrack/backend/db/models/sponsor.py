from sqlalchemy import Column, String
from sponsortrack.backend.db.models.base import Base
from sqlalchemy.orm import relationship


class Sponsor(Base):
    name = Column(String, index=True)
    description = Column(String)
    matched_extracts = relationship("Extract", back_populates="matched_sponsor")
