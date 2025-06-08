from sqlalchemy import Column, String, DateTime, Boolean, UUID
from sponsortrack.backend.db.models.base import Base, fk
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class AccessToken(Base):
    token_hash = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, index=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey(fk("accesstoken.id")), nullable=False, index=True
    )
    user = relationship("User", back_populates="access_token")
