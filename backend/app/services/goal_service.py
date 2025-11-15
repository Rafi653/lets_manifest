"""
Goal service for business logic.
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.goal import Goal, GoalProgress
from app.repositories.goal_repository import GoalRepository, GoalProgressRepository
from app.schemas.goal import GoalCreate, GoalUpdate, GoalProgressCreate


class GoalService:
    """Service for goal-related operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = GoalRepository(db)
        self.progress_repository = GoalProgressRepository(db)
    
    async def create_goal(self, user_id: UUID, goal_data: GoalCreate) -> Goal:
        """Create a new goal for a user."""
        goal = Goal(
            user_id=user_id,
            **goal_data.model_dump()
        )
        return await self.repository.create(goal)
    
    async def get_goal(self, goal_id: UUID, user_id: UUID) -> Goal:
        """Get a goal by ID, ensuring it belongs to the user."""
        goal = await self.repository.get_by_id(goal_id)
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        if goal.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this goal"
            )
        return goal
    
    async def get_user_goals(
        self,
        user_id: UUID,
        goal_type: Optional[str] = None,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Goal], int]:
        """Get all goals for a user with pagination."""
        goals = await self.repository.get_user_goals(
            user_id, goal_type, status_filter, skip, limit
        )
        total = await self.repository.count_user_goals(user_id, status_filter)
        return goals, total
    
    async def update_goal(
        self,
        goal_id: UUID,
        user_id: UUID,
        goal_data: GoalUpdate
    ) -> Goal:
        """Update a goal."""
        goal = await self.get_goal(goal_id, user_id)
        
        update_data = goal_data.model_dump(exclude_unset=True)
        
        # Auto-complete goal if status is completed
        if update_data.get("status") == "completed" and not goal.completed_at:
            update_data["completed_at"] = datetime.utcnow()
        
        return await self.repository.update(goal, update_data)
    
    async def delete_goal(self, goal_id: UUID, user_id: UUID) -> bool:
        """Delete a goal."""
        goal = await self.get_goal(goal_id, user_id)
        return await self.repository.delete(goal.id)
    
    async def add_progress(
        self,
        goal_id: UUID,
        user_id: UUID,
        progress_data: GoalProgressCreate
    ) -> GoalProgress:
        """Add progress to a goal."""
        goal = await self.get_goal(goal_id, user_id)
        
        # Calculate percentage if target value exists
        percentage = None
        if goal.target_value and goal.target_value > 0:
            percentage = (progress_data.value / goal.target_value) * 100
        
        progress = GoalProgress(
            goal_id=goal_id,
            progress_date=progress_data.progress_date,
            value=progress_data.value,
            percentage=percentage,
            notes=progress_data.notes
        )
        
        # Update goal's current value
        goal.current_value = progress_data.value
        
        return await self.progress_repository.create(progress)
    
    async def get_goal_progress(
        self,
        goal_id: UUID,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[GoalProgress]:
        """Get progress entries for a goal."""
        # Verify user owns the goal
        await self.get_goal(goal_id, user_id)
        return await self.progress_repository.get_goal_progress(goal_id, skip, limit)
