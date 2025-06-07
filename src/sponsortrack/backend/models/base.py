from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, DateTime, MetaData
from sqlalchemy.orm import as_declarative
from sponsortrack.backend.core.config import settings

metadata = MetaData(schema=settings.POSTGRES_SCHEMA)


@as_declarative(metadata=metadata)
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


def fk(ref: str) -> str:
    return f"{settings.POSTGRES_SCHEMA}.{ref}"
