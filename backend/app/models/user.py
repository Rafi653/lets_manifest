"""
User model for authentication and profile management.
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    """User model for authentication and profile."""

    __tablename__ = "users"

    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    # Profile
    first_name = Column(String(100))
    last_name = Column(String(100))
    avatar_url = Column(String(500))
    bio = Column(String)

    # Settings
    timezone = Column(String(50), default="UTC")
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)

    # Timestamps
    email_verified_at = Column(DateTime)
    last_login_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    habits = relationship("Habit", back_populates="user", cascade="all, delete-orphan")
    foods = relationship("Food", back_populates="user", cascade="all, delete-orphan")
    workouts = relationship(
        "Workout", back_populates="user", cascade="all, delete-orphan"
    )
    daily_reviews = relationship(
        "DailyReview", back_populates="user", cascade="all, delete-orphan"
    )
    blog_entries = relationship(
        "BlogEntry", back_populates="user", cascade="all, delete-orphan"
    )
    media = relationship("Media", back_populates="user", cascade="all, delete-orphan")
    progress_snapshots = relationship(
        "ProgressSnapshot", back_populates="user", cascade="all, delete-orphan"
    )
    notifications = relationship(
        "Notification", back_populates="user", cascade="all, delete-orphan"
    )
    notification_settings = relationship(
        "NotificationSettings",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
