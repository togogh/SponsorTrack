from sqlalchemy import Column, String, UUID, JSON, Enum
from backend.models.base import Base
import enum


class FlagStatus(enum.Enum):
    pending = "pending"
    resolved = "resolved"
    dismissed = "dismissed"


class EntityType(enum.Enum):
    video = "video"
    sponsorship = "sponsorship"


class Flag(Base):
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    entity_flagged = Column(Enum(EntityType, schema="dev"), nullable=False, index=True)
    field_flagged = Column(String, nullable=False, index=True)
    value_flagged = Column(JSON)
    status = Column(Enum(FlagStatus, schema="dev"), default=FlagStatus.pending, index=True)

    # __mapper_args__ = {
    #     "polymorphic_identity": "flag",
    #     "polymorphic_on": entity_flagged,
    # }


# class VideoFlag(Flag):
#     video_id = Column(UUID(as_uuid=True), ForeignKey(fk("video.id")), nullable=False)
#     video = relationship("Video", back_populates="flags")

#     __tablename__ = None
#     __mapper_args__ = {
#         "polymorphic_identity": "video",
#     }

# class SponsorshipFlag(Flag):
#     sponsorship_id = Column(UUID(as_uuid=True), ForeignKey(fk("sponsorship.id")), nullable=False)
#     sponsorship = relationship("Sponsorship", back_populates="flags")

#     __tablename__ = None
#     __mapper_args__ = {
#         "polymorphic_identity": "sponsorship",
#     }
