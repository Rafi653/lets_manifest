# Let's Manifest - Technical Architecture

## Overview

Let's Manifest is a web-based manifestation journal application built with a modern, scalable architecture. The application follows a three-tier architecture pattern with clear separation of concerns between the presentation layer (React frontend), application layer (Python/FastAPI backend), and data layer (PostgreSQL database).

## Technology Stack

### Frontend
- **Framework**: React 18+ with TypeScript
- **State Management**: React Context API / Redux Toolkit (for complex state)
- **Routing**: React Router v6
- **UI Components**: Material-UI (MUI) or shadcn/ui
- **HTTP Client**: Axios
- **Form Management**: React Hook Form with Zod validation
- **Build Tool**: Vite
- **Testing**: Vitest + React Testing Library

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy 2.0
- **Migration Tool**: Alembic
- **Authentication**: JWT (JSON Web Tokens) with OAuth2
- **Validation**: Pydantic v2
- **Testing**: pytest + pytest-asyncio
- **ASGI Server**: Uvicorn

### Database
- **Primary Database**: PostgreSQL 15+
- **Connection Pooling**: SQLAlchemy async engine
- **Schema Management**: Alembic migrations

### DevOps & Infrastructure
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Code Quality**: ESLint, Prettier (frontend) / Black, Ruff (backend)
- **Type Checking**: TypeScript (frontend) / mypy (backend)

## Architecture Pattern

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Browser                        │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           React Application (Frontend)                 │  │
│  │  - Components, Pages, Hooks                           │  │
│  │  - State Management (Context/Redux)                   │  │
│  │  - API Client (Axios)                                 │  │
│  └────────────────────┬──────────────────────────────────┘  │
└─────────────────────────┼───────────────────────────────────┘
                          │
                    HTTPS/REST API
                          │
┌─────────────────────────┼───────────────────────────────────┐
│                         │                                     │
│  ┌──────────────────────▼──────────────────────────────┐    │
│  │         FastAPI Backend (Application Layer)         │    │
│  │  ┌─────────────────────────────────────────────┐   │    │
│  │  │  API Routes (Endpoints)                     │   │    │
│  │  └────────────┬────────────────────────────────┘   │    │
│  │               │                                     │    │
│  │  ┌────────────▼────────────────────────────────┐   │    │
│  │  │  Business Logic (Services)                  │   │    │
│  │  └────────────┬────────────────────────────────┘   │    │
│  │               │                                     │    │
│  │  ┌────────────▼────────────────────────────────┐   │    │
│  │  │  Data Access Layer (Repositories)           │   │    │
│  │  └────────────┬────────────────────────────────┘   │    │
│  └───────────────┼─────────────────────────────────────┘    │
│                  │                                           │
│     ┌────────────▼────────────┐                             │
│     │   SQLAlchemy ORM        │                             │
│     └────────────┬────────────┘                             │
│                  │                                           │
└──────────────────┼───────────────────────────────────────────┘
                   │
         Database Connection
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                PostgreSQL Database                           │
│  - Users, Journals, Manifestations, Tags, etc.              │
└──────────────────────────────────────────────────────────────┘
```

### Communication Strategy

#### API Communication
- **Protocol**: HTTPS (HTTP/2 where available)
- **API Style**: RESTful JSON API
- **Base URL**: `/api/v1/`
- **Authentication**: Bearer token (JWT) in Authorization header
- **Content Type**: `application/json`

#### API Conventions
- **HTTP Methods**:
  - `GET`: Retrieve resources
  - `POST`: Create new resources
  - `PUT/PATCH`: Update existing resources
  - `DELETE`: Remove resources
- **Status Codes**:
  - `200`: Success
  - `201`: Created
  - `204`: No Content (successful deletion)
  - `400`: Bad Request
  - `401`: Unauthorized
  - `403`: Forbidden
  - `404`: Not Found
  - `422`: Validation Error
  - `500`: Internal Server Error

#### API Response Format
```json
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

#### Error Response Format
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

## Core Components & Services

### Frontend Components

1. **Authentication Module**
   - Login/Register components
   - Protected route wrapper
   - Auth context provider
   - Token management

2. **Dashboard Module**
   - User dashboard
   - Statistics/Analytics widgets
   - Quick action panel

3. **Journal Module**
   - Journal entry creation/editing
   - Journal list/grid view
   - Rich text editor integration
   - Media upload handling

4. **Manifestation Module**
   - Manifestation goal tracking
   - Progress visualization
   - Affirmation management

5. **Shared/Common**
   - Reusable UI components (buttons, forms, modals)
   - Layout components (header, sidebar, footer)
   - Utility hooks
   - API client configuration

### Backend Services

1. **Authentication Service**
   - User registration
   - Login/logout
   - Token generation/validation
   - Password reset
   - OAuth integration (future)

2. **User Service**
   - User profile management
   - User preferences
   - Account settings

3. **Journal Service**
   - CRUD operations for journal entries
   - Search and filtering
   - Media attachment handling
   - Tagging system

4. **Manifestation Service**
   - Goal creation and tracking
   - Progress updates
   - Affirmation management
   - Reminder system

5. **Analytics Service**
   - User activity tracking
   - Dashboard statistics
   - Trend analysis

### Database Schema Components

1. **Users**
   - User authentication and profile data
   - Preferences and settings

2. **Journals**
   - Journal entries with content
   - Timestamps and metadata

3. **Manifestations**
   - Goals and affirmations
   - Progress tracking

4. **Tags**
   - Categorization system
   - Many-to-many relationships

5. **Media**
   - File metadata and references
   - Storage location tracking

## Deployment Architecture

### Development Environment
- Local development with Docker Compose
- Hot-reload for both frontend and backend
- Local PostgreSQL instance
- Environment-specific configuration files

### Production Environment
- Containerized deployment
- Separate frontend and backend services
- Managed PostgreSQL database
- CDN for static assets
- Load balancer for API scaling
- Redis for caching (future enhancement)

## Security Considerations

1. **Authentication & Authorization**
   - JWT-based authentication
   - Refresh token rotation
   - Role-based access control (RBAC)
   - Password hashing with bcrypt

2. **API Security**
   - CORS configuration
   - Rate limiting
   - Request validation
   - SQL injection prevention (via ORM)
   - XSS prevention

3. **Data Protection**
   - Encrypted database connections
   - Secure password storage
   - GDPR compliance considerations
   - Regular security audits

## Scalability & Performance

1. **Frontend Optimization**
   - Code splitting and lazy loading
   - Asset optimization (images, bundles)
   - Browser caching strategies
   - CDN for static content

2. **Backend Optimization**
   - Database query optimization
   - Connection pooling
   - Async/await patterns
   - Pagination for large datasets
   - Caching layer (Redis - future)

3. **Database Optimization**
   - Proper indexing strategy
   - Query optimization
   - Regular VACUUM operations
   - Database connection pooling

## Development Workflow

1. **Version Control**
   - Git flow branching strategy
   - Feature branches from main
   - Pull request reviews required
   - CI/CD checks before merge

2. **Code Quality**
   - Linting on pre-commit hooks
   - Type checking in CI
   - Automated testing
   - Code coverage requirements

3. **Testing Strategy**
   - Unit tests (80%+ coverage target)
   - Integration tests for API endpoints
   - E2E tests for critical user flows
   - Performance testing

## Future Enhancements

1. **Phase 2 Features**
   - Real-time collaboration
   - WebSocket support for notifications
   - Advanced analytics dashboard
   - Mobile app (React Native)

2. **Infrastructure Improvements**
   - Redis caching layer
   - Elasticsearch for advanced search
   - Message queue (RabbitMQ/Celery)
   - Microservices architecture (if needed)

## References & Best Practices

- [React Best Practices](https://react.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Best Practices](https://wiki.postgresql.org/wiki/Don%27t_Do_This)
- [REST API Design Guidelines](https://restfulapi.net/)
- [12-Factor App Methodology](https://12factor.net/)
