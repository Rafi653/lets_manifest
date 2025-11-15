"""
Blog entry model for blog posts and journal entries.
"""
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class BlogEntry(Base):
    """Blog entry model for posts and journal entries."""

    __tablename__ = "blog_entries"

    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # Content
    title = Column(String(500), nullable=False)
    content = Column(String, nullable=False)
    excerpt = Column(String)
    slug = Column(String(500), unique=True, index=True)

    # Status
    status = Column(String(20), default="draft")
    is_public = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)

    # Metrics
    view_count = Column(Integer, default=0)

    # Timestamps
    published_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('draft', 'published', 'archived')", name="ck_blog_status"),
    )

    # Relationships
    user = relationship("User", back_populates="blog_entries")

    def __repr__(self) -> str:
        return f"<BlogEntry(id={self.id}, title={self.title}, status={self.status})>"
