# Database Setup and Migration Guide

## Overview

This guide covers PostgreSQL database setup, ORM configuration with SQLAlchemy, and database migrations with Alembic for the Let's Manifest application.

## Prerequisites

- PostgreSQL 15+ installed (or use Docker)
- Python 3.11+
- Backend dependencies installed (`pip install -r requirements.txt`)

## Database Configuration

### Environment Variables

Configure the database connection in `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://lets_manifest_user:lets_manifest_password@localhost:5432/lets_manifest_dev
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
```

### Connection Settings

The application uses:
- **asyncpg** driver for async database operations
- **Connection pooling** with configurable pool size and overflow
- **Pool pre-ping** to verify connections before use
- **Automatic session management** with commit/rollback

### Security Features

- Parameterized queries (SQL injection protection)
- Connection pooling limits resource usage
- UUID primary keys prevent enumeration attacks
- Database credentials managed via environment variables

## Quick Start with Docker

### 1. Start PostgreSQL

```bash
# From project root
docker compose up -d postgres

# Wait for database to be ready (5-10 seconds)
```

### 2. Run Migrations

```bash
cd backend

# Apply all pending migrations
alembic upgrade head

# Verify tables were created
docker compose exec postgres psql -U lets_manifest_user -d lets_manifest_dev -c "\dt"
```

### 3. Verify Connection

```bash
# Run database connectivity tests
pytest tests/integration/test_database_connectivity.py -v
```

## Manual Setup (Without Docker)

### 1. Create Database

```bash
# Create PostgreSQL user
createuser -P lets_manifest_user

# Create databases
createdb -O lets_manifest_user lets_manifest_dev
createdb -O lets_manifest_user lets_manifest_test

# Enable UUID extension
psql -U lets_manifest_user -d lets_manifest_dev -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
psql -U lets_manifest_user -d lets_manifest_test -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
```

### 2. Configure Connection

Update `.env` with your database credentials:

```env
DATABASE_URL=postgresql+asyncpg://lets_manifest_user:YOUR_PASSWORD@localhost:5432/lets_manifest_dev
```

### 3. Run Migrations

```bash
cd backend
alembic upgrade head
```

## Database Migrations with Alembic

### Creating New Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "description_of_changes"

# Create empty migration (for manual changes)
alembic revision -m "description_of_changes"
```

### Applying Migrations

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade by specific number of revisions
alembic upgrade +1

# Upgrade to specific revision
alembic upgrade <revision_id>
```

### Reverting Migrations

```bash
# Downgrade by one revision
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade <revision_id>

# Downgrade to base (empty database)
alembic downgrade base
```

### Migration History

```bash
# Show current revision
alembic current

# Show migration history
alembic history

# Show SQL that would be executed (dry run)
alembic upgrade head --sql
```

## Database Schema

### Tables Created

The initial migration creates 14 tables:

1. **users** - User authentication and profiles
2. **goals** - Goal definitions and tracking
3. **goal_progress** - Progress updates for goals
4. **habits** - Habit definitions
5. **habit_entries** - Daily habit completion records
6. **foods** - Food and nutrition tracking
7. **workouts** - Workout sessions
8. **workout_exercises** - Individual exercises in workouts
9. **daily_reviews** - End-of-day reflections
10. **blog_entries** - Blog posts and journal entries
11. **tags** - Tagging system
12. **taggables** - Polymorphic tag associations
13. **media** - File uploads and attachments
14. **progress_snapshots** - Aggregated progress tracking

### Key Features

- **UUID Primary Keys** - All tables use UUID v4 for primary keys
- **Timestamps** - Automatic `created_at` and `updated_at` tracking
- **Foreign Keys** - Relationships with CASCADE delete
- **Constraints** - Check constraints for data validation
- **Indexes** - Optimized indexes on frequently queried columns

## ORM Configuration

### Models

All models inherit from a custom `Base` class that provides:

```python
- UUID primary key (auto-generated)
- created_at timestamp
- to_dict() method for serialization
- Automatic table name generation
```

### Relationships

Models use SQLAlchemy relationships:

```python
# One-to-Many
user.goals  # User has many goals
goal.user   # Goal belongs to one user

# With cascade delete
cascade="all, delete-orphan"
```

### Session Management

Use the async session dependency:

```python
from app.core.database import get_db

async def endpoint(db: AsyncSession = Depends(get_db)):
    # Session automatically commits on success
    # Or rolls back on error
    pass
```

## Testing

### Test Database

Tests use a separate `lets_manifest_test` database to avoid affecting development data.

### Running Tests

```bash
# All integration tests
pytest tests/integration/ -v

# Specific test file
pytest tests/integration/test_user_crud.py -v

# With coverage
pytest tests/integration/ --cov=app --cov-report=html
```

### Test Fixtures

```python
@pytest.mark.asyncio
async def test_example(db_session: AsyncSession):
    # db_session provides a fresh database session
    # Tables are created before test and dropped after
    pass
```

## Performance Optimization

### Connection Pooling

```python
# Configured in app/core/database.py
pool_size = 5          # Number of persistent connections
max_overflow = 10      # Additional connections when needed
pool_pre_ping = True   # Verify connections before use
```

### Query Optimization

```python
# Use eager loading for relationships
from sqlalchemy.orm import selectinload

result = await session.execute(
    select(User)
    .options(selectinload(User.goals))
    .where(User.id == user_id)
)
```

### Indexing

Common query patterns have indexes:
- Email and username (unique indexes)
- Foreign keys (for joins)
- Status fields (for filtering)
- Date fields (for range queries)

## Troubleshooting

### Connection Errors

```bash
# Check PostgreSQL is running
docker compose ps postgres

# View PostgreSQL logs
docker compose logs postgres

# Test connection manually
psql -h localhost -U lets_manifest_user -d lets_manifest_dev
```

### Migration Issues

```bash
# Check current migration state
alembic current

# If migrations are out of sync, stamp the database
alembic stamp head

# Force a clean migration (WARNING: destroys data)
alembic downgrade base
alembic upgrade head
```

### UUID Extension Missing

```bash
# Enable UUID extension
docker compose exec postgres psql -U lets_manifest_user -d lets_manifest_dev \
  -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
```

## Production Deployment

### Pre-Deployment Checklist

- [ ] Update `DATABASE_URL` with production credentials
- [ ] Set `SECRET_KEY` to a strong random value
- [ ] Configure `DATABASE_POOL_SIZE` based on load
- [ ] Enable SSL for database connections
- [ ] Set up database backups
- [ ] Configure monitoring and alerting
- [ ] Run migrations in a maintenance window

### Running Migrations in Production

```bash
# 1. Backup database first
pg_dump -U lets_manifest_user lets_manifest_prod > backup.sql

# 2. Run migrations
alembic upgrade head

# 3. Verify migration succeeded
alembic current

# 4. Monitor application logs
```

### Database Backups

```bash
# Create backup
docker compose exec postgres pg_dump -U lets_manifest_user lets_manifest_dev > backup-$(date +%Y%m%d).sql

# Restore backup
docker compose exec -T postgres psql -U lets_manifest_user lets_manifest_dev < backup.sql
```

## Monitoring

### Connection Pool Stats

Monitor these metrics:
- Pool size usage
- Connection checkout time
- Number of overflows
- Failed connections

### Query Performance

```bash
# Enable query logging in development
# In app/core/database.py, set echo=True

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Logs all SQL queries
)
```

### Database Health Check

```bash
# Check database status
docker compose exec postgres psql -U lets_manifest_user -d lets_manifest_dev \
  -c "SELECT version();"

# Check table sizes
docker compose exec postgres psql -U lets_manifest_user -d lets_manifest_dev \
  -c "SELECT schemaname,tablename,pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) FROM pg_tables WHERE schemaname='public' ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;"
```

## Additional Resources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [FastAPI with Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)

## Support

For issues or questions:
1. Check the [troubleshooting](#troubleshooting) section
2. Review application logs
3. Consult database error messages
4. Open an issue on GitHub
