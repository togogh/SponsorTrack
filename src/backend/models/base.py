from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, DateTime, MetaData
from sqlalchemy.orm import as_declarative
from sqlalchemy.sql import func


metadata = MetaData(schema="env")


@as_declarative(metadata=metadata)
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    created_at = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


def fk(ref: str) -> str:
    return f"env.{ref}"
