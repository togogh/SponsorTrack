from sqlalchemy import Column, String
from sponsortrack.models.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    email = Column(String, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False)
    pasword = Column(String, nullable=False)
    access_token = relationship("AccessToken", back_populates="user")
