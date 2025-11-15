"""
Workout and workout exercise models for exercise tracking.
"""

from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Time,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Workout(Base):
    """Workout model for tracking exercise sessions."""

    __tablename__ = "workouts"

    # Foreign keys
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )

    # Workout info
    workout_date = Column(Date, nullable=False)
    workout_time = Column(Time)
    workout_type = Column(String(50), nullable=False)
    workout_name = Column(String(255))

    # Metrics
    duration_minutes = Column(Integer)
    calories_burned = Column(Numeric(8, 2))
    intensity = Column(String(20))

    # Additional info
    location = Column(String(100))
    notes = Column(String)
    mood_before = Column(String(20))
    mood_after = Column(String(20))

    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "intensity IN ('low', 'medium', 'high')", name="ck_workout_intensity"
        ),
    )

    # Relationships
    user = relationship("User", back_populates="workouts")
    exercises = relationship(
        "WorkoutExercise", back_populates="workout", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Workout(id={self.id}, type={self.workout_type}, date={self.workout_date})>"


class WorkoutExercise(Base):
    """Workout exercise model for individual exercises within a workout."""

    __tablename__ = "workout_exercises"

    # Foreign keys
    workout_id = Column(
        UUID(as_uuid=True), ForeignKey("workouts.id"), nullable=False, index=True
    )

    # Exercise info
    exercise_name = Column(String(255), nullable=False)
    exercise_type = Column(String(50))

    # Strength training metrics
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Numeric(6, 2))
    weight_unit = Column(String(10), default="lbs")

    # Cardio metrics
    distance = Column(Numeric(8, 2))
    distance_unit = Column(String(10))
    duration_seconds = Column(Integer)

    # Additional info
    rest_seconds = Column(Integer)
    notes = Column(String)
    order_index = Column(Integer, default=0)

    # Constraints
    __table_args__ = (
        CheckConstraint("weight_unit IN ('lbs', 'kg')", name="ck_exercise_weight_unit"),
        CheckConstraint(
            "distance_unit IN ('miles', 'km', 'meters')",
            name="ck_exercise_distance_unit",
        ),
    )

    # Relationships
    workout = relationship("Workout", back_populates="exercises")

    def __repr__(self) -> str:
        return f"<WorkoutExercise(id={self.id}, name={self.exercise_name})>"
