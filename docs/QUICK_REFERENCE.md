# Technical Architecture Summary

## Quick Reference Guide

This document provides a quick reference to the Let's Manifest technical architecture.

## Technology Stack at a Glance

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 18 + TypeScript | User interface |
| Build Tool | Vite | Fast development and building |
| Backend | FastAPI + Python 3.11 | REST API server |
| ORM | SQLAlchemy 2.0 (async) | Database operations |
| Database | PostgreSQL 15+ | Data persistence |
| Authentication | JWT | Secure user authentication |
| Container | Docker + Compose | Development environment |

## Project Structure Overview

```
lets_manifest/                    # Root monorepo
│
├── 📱 frontend/                  # React application
│   ├── src/
│   │   ├── components/          # UI components
│   │   ├── pages/               # Route pages
│   │   ├── api/                 # API client
│   │   ├── services/            # Business logic
│   │   └── ...
│   └── tests/                   # Frontend tests
│
├── 🔧 backend/                   # FastAPI application
│   ├── app/
│   │   ├── api/v1/endpoints/    # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── repositories/        # Data access
│   │   ├── models/              # DB models
│   │   └── schemas/             # Pydantic schemas
│   └── tests/                   # Backend tests
│
├── 🗄️  database/                 # Database files
│   ├── migrations/              # SQL migrations
│   ├── seeds/                   # Seed data
│   └── schemas/                 # Schema docs
│
├── 🐳 docker/                    # Docker configs
│   ├── frontend/                # Frontend Dockerfile
│   ├── backend/                 # Backend Dockerfile
│   └── postgres/                # Postgres init
│
├── 📚 docs/                      # Documentation
│   ├── api/                     # API reference
│   ├── guides/                  # How-to guides
│   └── diagrams/                # Architecture diagrams
│
└── 🔨 scripts/                   # Utility scripts
```

## API Architecture

### Layered Architecture

```
┌─────────────────────────────────────────┐
│         API Endpoints (Routes)          │  ← HTTP requests
│         /api/v1/journals               │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│      Business Logic (Services)          │  ← Domain logic
│      JournalService                     │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│     Data Access (Repositories)          │  ← Database queries
│     JournalRepository                   │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│        SQLAlchemy ORM                   │  ← ORM layer
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│         PostgreSQL Database              │  ← Data storage
└──────────────────────────────────────────┘
```

### Request Flow

```
1. Client → HTTP Request → API Endpoint
2. API Endpoint → Validates input (Pydantic) → Service
3. Service → Business logic → Repository
4. Repository → Database query (SQLAlchemy) → PostgreSQL
5. PostgreSQL → Data → Repository → Service → Endpoint
6. Endpoint → HTTP Response → Client
```

## Key API Endpoints

| Resource | Endpoints | Purpose |
|----------|-----------|---------|
| `/auth` | POST /register, /login, /logout | Authentication |
| `/users` | GET/PUT /me | User profile |
| `/journals` | GET, POST, PUT, DELETE /{id} | Journal entries |
| `/manifestations` | GET, POST, PUT, DELETE /{id} | Manifestation goals |
| `/tags` | GET, POST, PUT, DELETE /{id} | Tags/categories |

## Database Schema (High Level)

```
┌──────────────┐
│    Users     │
│─────────────│
│ id (PK)      │
│ email        │◄─────┐
│ password     │      │
│ full_name    │      │
└──────────────┘      │
                      │
┌──────────────┐      │         ┌──────────────┐
│   Journals   │      │         │     Tags     │
│─────────────│      │         │─────────────│
│ id (PK)      │      │         │ id (PK)      │
│ user_id (FK) │──────┘         │ name         │
│ title        │                │ color        │
│ content      │◄───────────────┤              │
│ created_at   │  many-to-many  └──────────────┘
└──────────────┘

┌──────────────────┐
│  Manifestations  │
│─────────────────│
│ id (PK)          │
│ user_id (FK)     │──────┐
│ title            │      │
│ description      │      │
│ target_date      │      │
│ status           │      │
│ progress         │      │
└──────────────────┘      │
                          │
                  ┌───────▼──────┐
                  │    Users     │
                  └──────────────┘
```

## Development Workflow

### 1. Setup

```bash
# Clone and start
git clone https://github.com/Rafi653/lets_manifest.git
cd lets_manifest
docker-compose up -d
```

### 2. Development

```bash
# Frontend (auto-reload)
cd frontend
npm run dev
# → http://localhost:5173

# Backend (auto-reload)
cd backend
uvicorn app.main:app --reload
# → http://localhost:8000
# → http://localhost:8000/docs (Swagger)
```

### 3. Testing

```bash
# Frontend tests
cd frontend
npm run test

# Backend tests
cd backend
pytest --cov=app tests/
```

### 4. Code Quality

```bash
# Frontend
npm run lint
npm run format
npm run type-check

# Backend
black app/
ruff check app/
mypy app/
```

## Security Features

| Feature | Implementation |
|---------|---------------|
| Authentication | JWT tokens (access + refresh) |
| Password Hashing | bcrypt |
| CORS | Configured origins |
| SQL Injection | ORM (SQLAlchemy) |
| Input Validation | Pydantic schemas |
| Rate Limiting | Per-endpoint limits |

## Performance Optimizations

### Frontend
- Code splitting with React.lazy()
- Asset optimization (images, bundles)
- Browser caching
- CDN for static assets

### Backend
- Async/await (non-blocking I/O)
- Connection pooling
- Database query optimization
- Pagination for large datasets

### Database
- Proper indexing
- Query optimization
- Connection pooling
- Regular VACUUM operations

## Deployment Strategy

### Development
- Docker Compose
- Hot reload enabled
- Local PostgreSQL

### Production
- Containerized services
- Managed PostgreSQL
- CDN for frontend assets
- Load balancer for backend

## Monitoring & Observability

### Logs
- Structured logging
- Request ID tracking
- Error tracking

### Metrics
- Response times
- Request counts
- Error rates
- Database query performance

### Health Checks
- `/health` endpoints
- Database connectivity
- Service status

## Scalability Considerations

### Horizontal Scaling
- Stateless API servers
- Load balancer distribution
- Session stored in JWT

### Vertical Scaling
- Database optimization
- Connection pooling
- Caching layer (future: Redis)

### Future Enhancements
- Redis for caching
- Message queue (Celery)
- CDN for media files
- Microservices (if needed)

## Common Commands

### Docker
```bash
docker-compose up -d           # Start all services
docker-compose down            # Stop all services
docker-compose logs -f         # View logs
docker-compose exec backend bash  # Access backend shell
```

### Database
```bash
alembic upgrade head           # Apply migrations
alembic revision --autogenerate -m "msg"  # Create migration
python scripts/seed_data.py    # Seed data
```

### Testing
```bash
pytest                         # Run backend tests
pytest --cov=app tests/        # With coverage
npm run test                   # Run frontend tests
```

## Next Steps

1. ✅ Architecture defined (this document)
2. 🔄 Database schema design
3. 🔄 Application skeleton
4. 🔄 Authentication system
5. 🔄 Core features implementation

## Documentation Links

- [Full Architecture](../ARCHITECTURE.md)
- [Folder Structure](../FOLDER_STRUCTURE.md)
- [Setup Guide](../docs/guides/setup.md)
- [API Reference](../docs/api/API_ENDPOINTS.md)
- [Contributing](../docs/guides/contributing.md)
