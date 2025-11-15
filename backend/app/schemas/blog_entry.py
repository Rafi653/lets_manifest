"""
Blog entry-related Pydantic schemas.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class BlogEntryBase(BaseModel):
    """Base schema for blog entry."""
    title: str = Field(..., max_length=500)
    content: str
    excerpt: Optional[str] = None
    status: str = Field(default="draft", pattern="^(draft|published|archived)$")
    is_public: bool = False
    is_featured: bool = False


class BlogEntryCreate(BlogEntryBase):
    """Schema for creating blog entry."""
    pass


class BlogEntryUpdate(BaseModel):
    """Schema for updating blog entry."""
    title: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = None
    excerpt: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(draft|published|archived)$")
    is_public: Optional[bool] = None
    is_featured: Optional[bool] = None


class BlogEntryResponse(BlogEntryBase):
    """Schema for blog entry response."""
    id: UUID
    user_id: UUID
    slug: Optional[str] = None
    view_count: int
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
