"""
Daily review model for end-of-day reflection.
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
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class DailyReview(Base):
    """Daily review model for end-of-day reflection and tracking."""

    __tablename__ = "daily_reviews"

    # Foreign keys
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )

    # Review date
    review_date = Column(Date, nullable=False)

    # Ratings (1-10 scale)
    mood_rating = Column(Integer)
    energy_level = Column(Integer)
    productivity_rating = Column(Integer)

    # Sleep tracking
    sleep_hours = Column(Numeric(3, 1))
    sleep_quality = Column(Integer)

    # Health tracking
    water_intake_ml = Column(Integer)
    screen_time_minutes = Column(Integer)
    steps = Column(Integer)

    # Reflections
    accomplishments = Column(String)
    challenges = Column(String)
    lessons_learned = Column(String)
    gratitude = Column(String)
    tomorrow_intentions = Column(String)
    highlights = Column(String)

    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "mood_rating >= 1 AND mood_rating <= 10", name="ck_review_mood_rating"
        ),
        CheckConstraint(
            "energy_level >= 1 AND energy_level <= 10", name="ck_review_energy_level"
        ),
        CheckConstraint(
            "productivity_rating >= 1 AND productivity_rating <= 10",
            name="ck_review_productivity",
        ),
        CheckConstraint(
            "sleep_quality >= 1 AND sleep_quality <= 10", name="ck_review_sleep_quality"
        ),
        UniqueConstraint("user_id", "review_date", name="uq_user_review_date"),
    )

    # Relationships
    user = relationship("User", back_populates="daily_reviews")

    def __repr__(self) -> str:
        return f"<DailyReview(id={self.id}, date={self.review_date}, mood={self.mood_rating})>"
