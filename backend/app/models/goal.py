"""
Goal and goal progress models for goal tracking.
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Goal(Base):
    """Goal model for tracking daily, weekly, monthly, yearly, and life goals."""

    __tablename__ = "goals"

    # Foreign keys
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    parent_goal_id = Column(UUID(as_uuid=True), ForeignKey("goals.id"), index=True)

    # Basic info
    title = Column(String(255), nullable=False)
    description = Column(String)

    # Goal configuration
    goal_type = Column(String(20), nullable=False, index=True)
    category = Column(String(50))
    target_value = Column(Numeric(10, 2))
    target_unit = Column(String(50))
    current_value = Column(Numeric(10, 2), default=Decimal("0"))

    # Dates (nullable for life goals without specific deadlines)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    # Status and priority
    status = Column(String(20), default="active")
    priority = Column(Integer, default=0)

    # Recurring goals
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String(50))

    # Reminder settings
    reminder_enabled = Column(Boolean, default=False)
    reminder_time = Column(String(5))  # HH:MM format
    reminder_days_before = Column(Integer)  # Days before deadline to remind

    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "goal_type IN ('daily', 'weekly', 'monthly', 'yearly', 'life_goal')", name="ck_goal_type"
        ),
        CheckConstraint(
            "status IN ('active', 'completed', 'cancelled', 'paused', 'in_progress')",
            name="ck_goal_status",
        ),
        CheckConstraint("priority >= 0 AND priority <= 5", name="ck_goal_priority"),
    )

    # Relationships
    user = relationship("User", back_populates="goals")
    progress_entries = relationship(
        "GoalProgress", back_populates="goal", cascade="all, delete-orphan"
    )
    milestones = relationship(
        "GoalMilestone", back_populates="goal", cascade="all, delete-orphan"
    )
    parent_goal = relationship("Goal", remote_side="Goal.id", backref="sub_goals")
    notifications = relationship(
        "Notification", back_populates="goal", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Goal(id={self.id}, title={self.title}, type={self.goal_type})>"


class GoalProgress(Base):
    """Goal progress tracking model."""

    __tablename__ = "goal_progress"

    # Foreign keys
    goal_id = Column(
        UUID(as_uuid=True), ForeignKey("goals.id"), nullable=False, index=True
    )

    # Progress data
    progress_date = Column(Date, nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    percentage = Column(Numeric(5, 2))
    notes = Column(String)

    # Relationships
    goal = relationship("Goal", back_populates="progress_entries")

    def __repr__(self) -> str:
        return f"<GoalProgress(id={self.id}, goal_id={self.goal_id}, date={self.progress_date})>"


class GoalMilestone(Base):
    """Goal milestone/checkpoint model for life goals."""

    __tablename__ = "goal_milestones"

    # Foreign keys
    goal_id = Column(
        UUID(as_uuid=True), ForeignKey("goals.id"), nullable=False, index=True
    )

    # Milestone data
    title = Column(String(255), nullable=False)
    description = Column(String)
    order_index = Column(Integer, default=0)
    status = Column(String(20), default="pending")
    target_date = Column(Date)

    # Timestamps
    completed_at = Column(DateTime)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'in_progress', 'completed', 'skipped')",
            name="ck_milestone_status",
        ),
    )

    # Relationships
    goal = relationship("Goal", back_populates="milestones")

    def __repr__(self) -> str:
        return f"<GoalMilestone(id={self.id}, goal_id={self.goal_id}, title={self.title})>"
