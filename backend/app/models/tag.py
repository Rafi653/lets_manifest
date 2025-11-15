"""
Tag and taggable models for categorization system.
"""
from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Tag(Base):
    """Tag model for categorization."""

    __tablename__ = "tags"

    # Tag info
    name = Column(String(50), nullable=False)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    category = Column(String(50), index=True)
    color = Column(String(7))
    description = Column(String)
    usage_count = Column(Integer, default=0)

    # Relationships
    taggables = relationship("Taggable", back_populates="tag", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, name={self.name})>"


class Taggable(Base):
    """Taggable model for polymorphic tag associations."""

    __tablename__ = "taggables"

    # Foreign keys
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=False, index=True)

    # Polymorphic association
    taggable_id = Column(UUID(as_uuid=True), nullable=False)
    taggable_type = Column(String(50), nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "taggable_type IN ('goal', 'habit', 'blog_entry', 'workout', 'food', 'daily_review')",
            name="ck_taggable_type",
        ),
        UniqueConstraint("tag_id", "taggable_type", "taggable_id", name="uq_tag_taggable"),
    )

    # Relationships
    tag = relationship("Tag", back_populates="taggables")

    def __repr__(self) -> str:
        return f"<Taggable(id={self.id}, tag_id={self.tag_id}, type={self.taggable_type})>"
