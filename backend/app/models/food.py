"""
Food model for food tracking and nutrition logging.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Time,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Food(Base):
    """Food model for tracking meals and nutrition."""

    __tablename__ = "foods"

    # Foreign keys
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )

    # Meal info
    meal_date = Column(Date, nullable=False)
    meal_time = Column(Time)
    meal_type = Column(String(20), nullable=False)
    food_name = Column(String(255), nullable=False)
    portion_size = Column(String(100))

    # Nutrition data
    calories = Column(Numeric(8, 2))
    protein_grams = Column(Numeric(6, 2))
    carbs_grams = Column(Numeric(6, 2))
    fats_grams = Column(Numeric(6, 2))
    fiber_grams = Column(Numeric(6, 2))
    sugar_grams = Column(Numeric(6, 2))
    sodium_mg = Column(Numeric(8, 2))

    # Additional info
    notes = Column(String)
    is_favorite = Column(Boolean, default=False)

    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')",
            name="ck_food_meal_type",
        ),
    )

    # Relationships
    user = relationship("User", back_populates="foods")

    def __repr__(self) -> str:
        return (
            f"<Food(id={self.id}, name={self.food_name}, meal_type={self.meal_type})>"
        )
