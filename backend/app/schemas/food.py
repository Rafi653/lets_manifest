"""
Food-related Pydantic schemas.
"""
from datetime import date, datetime, time
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class FoodBase(BaseModel):
    """Base schema for food tracking."""
    meal_date: date
    meal_time: Optional[time] = None
    meal_type: str = Field(..., pattern="^(breakfast|lunch|dinner|snack)$")
    food_name: str = Field(..., max_length=255)
    portion_size: Optional[str] = Field(None, max_length=100)
    calories: Optional[Decimal] = Field(None, ge=0)
    protein_grams: Optional[Decimal] = Field(None, ge=0)
    carbs_grams: Optional[Decimal] = Field(None, ge=0)
    fats_grams: Optional[Decimal] = Field(None, ge=0)
    fiber_grams: Optional[Decimal] = Field(None, ge=0)
    sugar_grams: Optional[Decimal] = Field(None, ge=0)
    sodium_mg: Optional[Decimal] = Field(None, ge=0)
    notes: Optional[str] = None
    is_favorite: bool = False


class FoodCreate(FoodBase):
    """Schema for creating food entry."""
    pass


class FoodUpdate(BaseModel):
    """Schema for updating food entry."""
    meal_time: Optional[time] = None
    food_name: Optional[str] = Field(None, max_length=255)
    portion_size: Optional[str] = Field(None, max_length=100)
    calories: Optional[Decimal] = Field(None, ge=0)
    protein_grams: Optional[Decimal] = Field(None, ge=0)
    carbs_grams: Optional[Decimal] = Field(None, ge=0)
    fats_grams: Optional[Decimal] = Field(None, ge=0)
    fiber_grams: Optional[Decimal] = Field(None, ge=0)
    sugar_grams: Optional[Decimal] = Field(None, ge=0)
    sodium_mg: Optional[Decimal] = Field(None, ge=0)
    notes: Optional[str] = None
    is_favorite: Optional[bool] = None


class FoodResponse(FoodBase):
    """Schema for food response."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
