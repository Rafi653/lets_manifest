"""
Progress snapshot model for long-term progress tracking.
"""
from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class ProgressSnapshot(Base):
    """Progress snapshot model for aggregated progress tracking."""

    __tablename__ = "progress_snapshots"

    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # Snapshot info
    snapshot_date = Column(Date, nullable=False)
    snapshot_type = Column(String(50), nullable=False)

    # Goals metrics
    total_goals = Column(Integer, default=0)
    completed_goals = Column(Integer, default=0)

    # Habits metrics
    active_habits = Column(Integer, default=0)
    habit_completion_rate = Column(Numeric(5, 2))

    # Workout metrics
    total_workouts = Column(Integer, default=0)
    total_workout_minutes = Column(Integer, default=0)

    # Daily review metrics
    average_daily_mood = Column(Numeric(3, 1))
    average_energy_level = Column(Numeric(3, 1))

    # Content metrics
    total_blog_entries = Column(Integer, default=0)

    # Health metrics
    weight = Column(Numeric(5, 2))
    weight_unit = Column(String(10), default="lbs")
    body_fat_percentage = Column(Numeric(4, 2))

    # Additional notes
    notes = Column(String)

    # Constraints
    __table_args__ = (
        CheckConstraint("snapshot_type IN ('weekly', 'monthly', 'yearly')", name="ck_snapshot_type"),
        CheckConstraint("weight_unit IN ('lbs', 'kg')", name="ck_snapshot_weight_unit"),
        UniqueConstraint("user_id", "snapshot_date", "snapshot_type", name="uq_user_snapshot"),
    )

    # Relationships
    user = relationship("User", back_populates="progress_snapshots")

    def __repr__(self) -> str:
        return f"<ProgressSnapshot(id={self.id}, date={self.snapshot_date}, type={self.snapshot_type})>"
