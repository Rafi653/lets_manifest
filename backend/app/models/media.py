"""
Media model for file uploads and media management.
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Media(Base):
    """Media model for file uploads and media management."""

    __tablename__ = "media"

    # Foreign keys
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )

    # File info
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(1000), nullable=False)
    file_type = Column(String(100), nullable=False, index=True)
    file_size = Column(BigInteger, nullable=False)

    # Image dimensions (if applicable)
    width = Column(Integer)
    height = Column(Integer)
    alt_text = Column(String(255))

    # Polymorphic association
    related_to_type = Column(String(50))
    related_to_id = Column(UUID(as_uuid=True))

    # Accessibility
    is_public = Column(Boolean, default=False)

    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="media")

    def __repr__(self) -> str:
        return (
            f"<Media(id={self.id}, filename={self.file_name}, type={self.file_type})>"
        )
