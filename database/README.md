# Database

## Overview

This directory contains database-related files including migration scripts, seed data, and schema documentation for the Let's Manifest PostgreSQL database.

## Database: PostgreSQL 15+

PostgreSQL is chosen for its:
- ACID compliance and data integrity
- Rich feature set (JSON support, full-text search)
- Excellent performance and scalability
- Strong community and ecosystem
- Advanced indexing capabilities

## Directory Structure

```
database/
├── migrations/         # Manual SQL migrations (if needed)
├── seeds/              # Seed data files
│   ├── development/    # Development seed data
│   └── production/     # Production seed data
├── schemas/            # Database schema documentation
│   └── schema.sql      # Complete schema export
└── README.md           # This file
```

## Schema Management

Primary schema management is handled by Alembic migrations in the backend:

```
/backend/alembic/versions/
```

This directory serves as:
1. Documentation repository for database schemas
2. Storage for one-off migration scripts
3. Seed data for different environments
4. Schema exports for reference

## Database Schema Overview

### Core Tables

1. **users**
   - User accounts and profiles
   - Authentication credentials
   - User preferences

2. **journals**
   - Journal entries
   - Entry content and metadata
   - Timestamps and versioning

3. **manifestations**
   - Manifestation goals
   - Progress tracking
   - Affirmations and intentions

4. **tags**
   - Categorization system
   - Many-to-many with journals and manifestations

5. **media**
   - Uploaded file metadata
   - Storage references

6. **user_sessions**
   - Active user sessions
   - Token management

## Connection Details

### Development
```
Host: localhost
Port: 5432
Database: lets_manifest_dev
User: lets_manifest_user
```

### Connection String Format
```
postgresql+asyncpg://user:password@host:port/database
```

## Seed Data

### Development Seeds

Location: `seeds/development/`

Includes:
- Test users with known credentials
- Sample journal entries
- Example manifestations
- Common tags

Load development seeds:
```bash
cd backend
python scripts/seed_data.py --env development
```

### Production Seeds

Location: `seeds/production/`

Includes:
- Default system data
- Initial admin user
- Common tags/categories

Load production seeds:
```bash
cd backend
python scripts/seed_data.py --env production
```

## Database Initialization

### Using Docker Compose

The easiest way to set up the database:

```bash
docker-compose up -d postgres
```

### Manual Setup

1. Install PostgreSQL 15+
2. Create database:
```sql
CREATE DATABASE lets_manifest_dev;
CREATE USER lets_manifest_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE lets_manifest_dev TO lets_manifest_user;
```

3. Run migrations:
```bash
cd backend
alembic upgrade head
```

4. Load seed data:
```bash
python scripts/seed_data.py
```

## Backup and Restore

### Backup

```bash
pg_dump -U lets_manifest_user -h localhost lets_manifest_dev > backup.sql
```

### Restore

```bash
psql -U lets_manifest_user -h localhost lets_manifest_dev < backup.sql
```

### Automated Backups

See `/backend/scripts/backup_db.py` for automated backup script.

## Indexing Strategy

### Primary Indexes
- Primary keys on all tables
- Foreign key indexes for relationships
- Unique constraints on email, usernames

### Performance Indexes
- `users.email` - Login lookups
- `journals.user_id, created_at` - User journal queries
- `manifestations.user_id, status` - Active manifestations
- `tags.name` - Tag searches

### Full-Text Search
- GIN index on journal content
- GIN index on manifestation goals

## Database Best Practices

1. **Migrations**
   - Always use Alembic for schema changes
   - Test migrations on development data first
   - Create rollback plans for production

2. **Performance**
   - Use indexes appropriately
   - Monitor query performance
   - Regular VACUUM operations
   - Connection pooling

3. **Security**
   - Use environment variables for credentials
   - Encrypt connections (SSL)
   - Regular security updates
   - Limited user permissions

4. **Data Integrity**
   - Foreign key constraints
   - NOT NULL constraints where appropriate
   - Check constraints for data validation
   - Default values for timestamps

## Monitoring

### Useful Queries

Check database size:
```sql
SELECT pg_size_pretty(pg_database_size('lets_manifest_dev'));
```

Check table sizes:
```sql
SELECT 
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

Active connections:
```sql
SELECT count(*) FROM pg_stat_activity;
```

## Troubleshooting

### Connection Issues

Check PostgreSQL is running:
```bash
sudo systemctl status postgresql
```

Test connection:
```bash
psql -U lets_manifest_user -h localhost -d lets_manifest_dev
```

### Migration Issues

Check current migration version:
```bash
cd backend
alembic current
```

View migration history:
```bash
alembic history
```

## Related Documentation

- PostgreSQL Documentation: https://www.postgresql.org/docs/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- Alembic Documentation: https://alembic.sqlalchemy.org/
- Backend README: `/backend/README.md`
- Architecture Documentation: `/ARCHITECTURE.md`
