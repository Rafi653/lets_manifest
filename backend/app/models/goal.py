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
    """Goal model for tracking daily, weekly, monthly, and yearly goals."""

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

    # Dates
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # Status and priority
    status = Column(String(20), default="active")
    priority = Column(Integer, default=0)

    # Recurring goals
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String(50))

    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "goal_type IN ('daily', 'weekly', 'monthly', 'yearly')", name="ck_goal_type"
        ),
        CheckConstraint(
            "status IN ('active', 'completed', 'cancelled', 'paused')",
            name="ck_goal_status",
        ),
        CheckConstraint("priority >= 0 AND priority <= 5", name="ck_goal_priority"),
    )

    # Relationships
    user = relationship("User", back_populates="goals")
    progress_entries = relationship(
        "GoalProgress", back_populates="goal", cascade="all, delete-orphan"
    )
    parent_goal = relationship("Goal", remote_side="Goal.id", backref="sub_goals")

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
