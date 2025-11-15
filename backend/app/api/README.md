# Backend API Endpoints

This directory contains all API endpoint definitions organized by version and resource.

## Structure

```
api/
├── v1/              # API version 1
│   ├── endpoints/   # Endpoint modules
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── journals.py
│   │   └── manifestations.py
│   └── api.py       # API router aggregation
└── deps.py          # API dependencies (auth, db, etc.)
```

## Endpoint Guidelines

1. **Keep endpoints thin** - Business logic belongs in services, not endpoints
2. **Use proper HTTP methods** - GET, POST, PUT, PATCH, DELETE
3. **Return consistent responses** - Use standard response schemas
4. **Handle errors properly** - Use appropriate HTTP status codes
5. **Document with docstrings** - Clear descriptions for OpenAPI docs
6. **Validate input** - Use Pydantic schemas for request/response validation

## Example Endpoint

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.schemas.journal import JournalCreate, JournalResponse
from app.services.journal_service import JournalService

router = APIRouter()

@router.post("/", response_model=JournalResponse, status_code=201)
async def create_journal(
    journal_data: JournalCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new journal entry."""
    service = JournalService(db)
    journal = await service.create_journal(journal_data, current_user.id)
    return journal
```

## Response Standards

All endpoints should return responses in this format:

```python
{
    "data": { ... },
    "message": "Success message",
    "errors": null,
    "meta": {
        "timestamp": "2025-11-15T02:13:00Z",
        "request_id": "uuid"
    }
}
```
