from sqlalchemy import Column, String
from sponsortrack.backend.db.models.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    email = Column(String, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    access_tokens = relationship("AccessToken", back_populates="user")
