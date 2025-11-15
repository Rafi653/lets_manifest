"""
API v1 router aggregation.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    goals,
    habits,
    habit_analytics,
    foods,
    workouts,
    daily_reviews,
    blog_entries,
    progress,
    notifications,
    life_goals_analytics,
)

api_router = APIRouter()

# Authentication endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# User management endpoints
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Core module endpoints
api_router.include_router(goals.router, prefix="/goals", tags=["Goals"])
api_router.include_router(habits.router, prefix="/habits", tags=["Habits"])
api_router.include_router(
    habit_analytics.router, prefix="/habits", tags=["Habit Analytics"]
)
api_router.include_router(foods.router, prefix="/foods", tags=["Food Tracking"])
api_router.include_router(workouts.router, prefix="/workouts", tags=["Workouts"])
api_router.include_router(
    daily_reviews.router, prefix="/daily-reviews", tags=["Daily Reviews"]
)
api_router.include_router(
    blog_entries.router, prefix="/blog-entries", tags=["Blog Entries"]
)
api_router.include_router(
    progress.router, prefix="/progress", tags=["Progress Tracking"]
)
api_router.include_router(
    notifications.router, prefix="/notifications", tags=["Notifications"]
)
api_router.include_router(
    life_goals_analytics.router, prefix="/analytics", tags=["Life Goals Analytics"]
)
