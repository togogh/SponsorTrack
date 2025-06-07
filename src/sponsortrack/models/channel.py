from sqlalchemy import Column, String
from sponsortrack.models.base import Base
from sqlalchemy.orm import relationship


class Channel(Base):
    youtube_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    handle = Column(String, nullable=False)
    videos = relationship("Video", back_populates="channel")
