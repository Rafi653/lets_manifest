"""
Common Pydantic schemas for API responses.
"""
from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class ResponseMetadata(BaseModel):
    """Metadata for API responses."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None


class ErrorDetail(BaseModel):
    """Error detail schema."""
    field: Optional[str] = None
    message: str


class APIResponse(BaseModel, Generic[DataT]):
    """Standard API response wrapper."""
    data: Optional[DataT] = None
    message: str = "Success"
    errors: Optional[List[ErrorDetail]] = None
    meta: ResponseMetadata = Field(default_factory=ResponseMetadata)


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(default=20, ge=1, le=100, description="Items per page")


class PaginatedResponse(BaseModel, Generic[DataT]):
    """Paginated response with items."""
    items: List[DataT]
    total: int
    page: int
    limit: int
    total_pages: int


class HealthCheck(BaseModel):
    """Health check response."""
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str
