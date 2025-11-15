"""
Habit and habit entry models for habit tracking.
"""
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Habit(Base):
    """Habit model for tracking habits with streak support."""

    __tablename__ = "habits"

    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # Basic info
    name = Column(String(255), nullable=False)
    description = Column(String)

    # Configuration
    frequency = Column(String(20), nullable=False)
    target_days = Column(Integer)
    category = Column(String(50))

    # UI customization
    color = Column(String(7))
    icon = Column(String(50))
    reminder_time = Column(Time)

    # Status and streaks
    is_active = Column(Boolean, default=True)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    total_completions = Column(Integer, default=0)

    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Constraints
    __table_args__ = (
        CheckConstraint("frequency IN ('daily', 'weekly', 'custom')", name="ck_habit_frequency"),
    )

    # Relationships
    user = relationship("User", back_populates="habits")
    entries = relationship("HabitEntry", back_populates="habit", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Habit(id={self.id}, name={self.name}, streak={self.current_streak})>"


class HabitEntry(Base):
    """Habit entry model for daily habit completion tracking."""

    __tablename__ = "habit_entries"

    # Foreign keys
    habit_id = Column(UUID(as_uuid=True), ForeignKey("habits.id"), nullable=False, index=True)

    # Entry data
    entry_date = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    notes = Column(String)
    mood = Column(String(20))

    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Constraints
    __table_args__ = (
        UniqueConstraint("habit_id", "entry_date", name="uq_habit_entry_date"),
    )

    # Relationships
    habit = relationship("Habit", back_populates="entries")

    def __repr__(self) -> str:
        return f"<HabitEntry(id={self.id}, habit_id={self.habit_id}, date={self.entry_date}, completed={self.completed})>"
