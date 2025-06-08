from sqlalchemy import Column, String, Boolean
from sponsortrack.backend.db.models.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    email = Column(String, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    access_tokens = relationship("AccessToken", back_populates="user")
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_verified = Column(Boolean, nullable=False, default=False)
