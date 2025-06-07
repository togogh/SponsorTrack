from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


Base = declarative_base(cls=Base)
