# Let's Manifest - Backend

## Overview

The backend is built with FastAPI and Python 3.11+, providing a robust RESTful API for the manifestation journal application. It uses SQLAlchemy for ORM, Alembic for migrations, and PostgreSQL as the database.

## Tech Stack

- **Framework**: FastAPI
- **Python Version**: 3.11+
- **ORM**: SQLAlchemy 2.0 (async)
- **Database**: PostgreSQL 15+
- **Migration Tool**: Alembic
- **Validation**: Pydantic v2
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: pytest + pytest-asyncio
- **ASGI Server**: Uvicorn

## Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 15+
- pip or poetry for dependency management

### Installation

```bash
cd backend
pip install -r requirements.txt
```

For development dependencies:

```bash
pip install -r requirements-dev.txt
```

### Environment Setup

Copy the example environment file and configure:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Application
APP_NAME=Let's Manifest API
APP_VERSION=1.0.0
DEBUG=True

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/lets_manifest
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Environment
ENVIRONMENT=development
```

### Database Setup

Initialize the database:

```bash
python scripts/init_db.py
```

Run migrations:

```bash
alembic upgrade head
```

Seed development data (optional):

```bash
python scripts/seed_data.py
```

### Development

Start the development server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI): `http://localhost:8000/docs`

Alternative documentation (ReDoc): `http://localhost:8000/redoc`

## Project Structure

```
app/
├── api/              # API layer
│   ├── v1/           # API version 1
│   │   └── endpoints/  # API endpoints
│   └── deps.py       # Dependencies
├── core/             # Core functionality
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas
├── services/         # Business logic
├── repositories/     # Data access layer
├── middleware/       # Custom middleware
├── utils/            # Utility functions
└── main.py           # Application entry point
```

## Available Scripts

Development:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run tests:
```bash
pytest
pytest --cov=app tests/  # With coverage
```

Run linter:
```bash
ruff check app/
black --check app/
```

Format code:
```bash
black app/
ruff check --fix app/
```

Type checking:
```bash
mypy app/
```

Create migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## API Structure

### Endpoint Organization

```
/api/v1/
├── /auth           # Authentication endpoints
├── /users          # User management
├── /journals       # Journal entries
├── /manifestations # Manifestation goals
└── /tags           # Tags and categories
```

### Standard Response Format

Success Response:
```json
{
  "data": { ... },
  "message": "Success",
  "errors": null,
  "meta": {
    "timestamp": "2025-11-15T02:13:00Z",
    "request_id": "uuid"
  }
}
```

Error Response:
```json
{
  "data": null,
  "message": "Error message",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ],
  "meta": {
    "timestamp": "2025-11-15T02:13:00Z",
    "request_id": "uuid"
  }
}
```

## Authentication

The API uses JWT-based authentication with Bearer tokens.

To authenticate requests, include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Code Style

- Follow PEP 8 style guide
- Use type hints for all functions
- Keep functions small and focused
- Use async/await for all database operations
- Add docstrings for classes and functions
- Keep business logic in services, not endpoints
- Use repository pattern for data access

## Testing

- Unit tests for services and repositories
- Integration tests for API endpoints
- Mock external dependencies
- Aim for 80%+ code coverage

Run tests:

```bash
pytest
pytest -v  # Verbose output
pytest --cov=app tests/  # With coverage
pytest tests/unit/  # Run specific test directory
```

## Database Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "Add user table"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback:

```bash
alembic downgrade -1  # Rollback one migration
alembic downgrade <revision>  # Rollback to specific revision
```

View migration history:

```bash
alembic history
alembic current
```

## Environment Variables

### Required
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Secret key for JWT tokens

### Optional
- `DEBUG` - Enable debug mode (default: False)
- `ENVIRONMENT` - Environment name (development/staging/production)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT expiration time
- `BACKEND_CORS_ORIGINS` - Allowed CORS origins

## Security

- Passwords are hashed with bcrypt
- JWT tokens for authentication
- CORS properly configured
- SQL injection protection via ORM
- Input validation with Pydantic
- Rate limiting on sensitive endpoints

## Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Write/update tests
4. Run linter and tests
5. Update API documentation if needed
6. Submit a pull request

## Architecture

See `/ARCHITECTURE.md` for detailed architecture documentation.

## Deployment

See `/docs/guides/deployment.md` for deployment instructions.
