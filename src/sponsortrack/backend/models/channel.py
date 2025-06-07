from sqlalchemy import Column, String
from sponsortrack.backend.models.base import Base
from sqlalchemy.orm import relationship


class Channel(Base):
    youtube_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    handle = Column(String, nullable=False, index=True)
    videos = relationship("Video", back_populates="channel")
