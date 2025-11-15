"""
Base model class for SQLAlchemy models.
"""
from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import DeclarativeMeta


class CustomBase:
    """Base class for all models with common fields and methods."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name."""
        return cls.__name__.lower()

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict[str, Any]:
        """Convert model instance to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def __repr__(self) -> str:
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={self.id})>"


Base: DeclarativeMeta = declarative_base(cls=CustomBase)
