# Let's Manifest - Folder Structure

## Overview

This document outlines the folder structure for the Let's Manifest application. The project follows a **monorepo** approach with clear separation between frontend, backend, and shared resources.

## Repository Structure

```
lets_manifest/
├── .github/                    # GitHub specific files
│   ├── workflows/              # CI/CD workflows
│   │   ├── frontend-ci.yml
│   │   ├── backend-ci.yml
│   │   └── deploy.yml
│   └── agents/                 # GitHub Copilot agents
│
├── frontend/                   # React frontend application
│   ├── public/                 # Static assets
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── manifest.json
│   │
│   ├── src/                    # Source code
│   │   ├── api/                # API client and configurations
│   │   │   ├── client.ts       # Axios instance configuration
│   │   │   ├── endpoints.ts    # API endpoint definitions
│   │   │   └── interceptors.ts # Request/response interceptors
│   │   │
│   │   ├── assets/             # Images, fonts, icons
│   │   │   ├── images/
│   │   │   ├── icons/
│   │   │   └── fonts/
│   │   │
│   │   ├── components/         # Reusable components
│   │   │   ├── common/         # Common components
│   │   │   │   ├── Button/
│   │   │   │   ├── Input/
│   │   │   │   ├── Modal/
│   │   │   │   └── Card/
│   │   │   │
│   │   │   ├── layout/         # Layout components
│   │   │   │   ├── Header/
│   │   │   │   ├── Sidebar/
│   │   │   │   ├── Footer/
│   │   │   │   └── MainLayout/
│   │   │   │
│   │   │   └── features/       # Feature-specific components
│   │   │       ├── auth/
│   │   │       ├── journal/
│   │   │       └── manifestation/
│   │   │
│   │   ├── contexts/           # React Context providers
│   │   │   ├── AuthContext.tsx
│   │   │   ├── ThemeContext.tsx
│   │   │   └── NotificationContext.tsx
│   │   │
│   │   ├── hooks/              # Custom React hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useApi.ts
│   │   │   ├── useLocalStorage.ts
│   │   │   └── useDebounce.ts
│   │   │
│   │   ├── pages/              # Page components (routes)
│   │   │   ├── Home/
│   │   │   │   ├── index.tsx
│   │   │   │   └── Home.module.css
│   │   │   ├── Auth/
│   │   │   │   ├── Login.tsx
│   │   │   │   └── Register.tsx
│   │   │   ├── Dashboard/
│   │   │   │   └── index.tsx
│   │   │   ├── Journal/
│   │   │   │   ├── JournalList.tsx
│   │   │   │   ├── JournalDetail.tsx
│   │   │   │   └── JournalCreate.tsx
│   │   │   ├── Manifestation/
│   │   │   │   ├── ManifestationList.tsx
│   │   │   │   └── ManifestationDetail.tsx
│   │   │   └── NotFound/
│   │   │       └── index.tsx
│   │   │
│   │   ├── routes/             # Routing configuration
│   │   │   ├── index.tsx
│   │   │   ├── ProtectedRoute.tsx
│   │   │   └── PublicRoute.tsx
│   │   │
│   │   ├── services/           # Business logic services
│   │   │   ├── authService.ts
│   │   │   ├── journalService.ts
│   │   │   ├── manifestationService.ts
│   │   │   └── userService.ts
│   │   │
│   │   ├── store/              # State management (if using Redux)
│   │   │   ├── index.ts
│   │   │   ├── slices/
│   │   │   │   ├── authSlice.ts
│   │   │   │   ├── journalSlice.ts
│   │   │   │   └── uiSlice.ts
│   │   │   └── middleware/
│   │   │
│   │   ├── styles/             # Global styles
│   │   │   ├── globals.css
│   │   │   ├── variables.css
│   │   │   └── theme.ts
│   │   │
│   │   ├── types/              # TypeScript type definitions
│   │   │   ├── api.types.ts
│   │   │   ├── auth.types.ts
│   │   │   ├── journal.types.ts
│   │   │   └── user.types.ts
│   │   │
│   │   ├── utils/              # Utility functions
│   │   │   ├── validators.ts
│   │   │   ├── formatters.ts
│   │   │   ├── constants.ts
│   │   │   └── helpers.ts
│   │   │
│   │   ├── App.tsx             # Root component
│   │   ├── main.tsx            # Entry point
│   │   └── vite-env.d.ts       # Vite type definitions
│   │
│   ├── tests/                  # Test files
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   │
│   ├── .env.example            # Environment variables template
│   ├── .eslintrc.json          # ESLint configuration
│   ├── .prettierrc             # Prettier configuration
│   ├── package.json            # Dependencies and scripts
│   ├── tsconfig.json           # TypeScript configuration
│   ├── vite.config.ts          # Vite configuration
│   └── README.md               # Frontend documentation
│
├── backend/                    # Python/FastAPI backend
│   ├── alembic/                # Database migrations
│   │   ├── versions/           # Migration files
│   │   ├── env.py              # Alembic environment config
│   │   └── script.py.mako      # Migration template
│   │
│   ├── app/                    # Application source code
│   │   ├── api/                # API layer
│   │   │   ├── v1/             # API version 1
│   │   │   │   ├── endpoints/  # API endpoints
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── users.py
│   │   │   │   │   ├── journals.py
│   │   │   │   │   └── manifestations.py
│   │   │   │   └── api.py      # API router aggregation
│   │   │   └── deps.py         # API dependencies
│   │   │
│   │   ├── core/               # Core functionality
│   │   │   ├── config.py       # Application configuration
│   │   │   ├── security.py     # Security utilities (JWT, passwords)
│   │   │   ├── database.py     # Database connection
│   │   │   └── logging.py      # Logging configuration
│   │   │
│   │   ├── models/             # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── journal.py
│   │   │   ├── manifestation.py
│   │   │   ├── tag.py
│   │   │   └── base.py         # Base model class
│   │   │
│   │   ├── schemas/            # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── journal.py
│   │   │   ├── manifestation.py
│   │   │   ├── tag.py
│   │   │   └── common.py       # Common schemas (responses, etc.)
│   │   │
│   │   ├── services/           # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── journal_service.py
│   │   │   └── manifestation_service.py
│   │   │
│   │   ├── repositories/       # Data access layer
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # Base repository class
│   │   │   ├── user_repository.py
│   │   │   ├── journal_repository.py
│   │   │   └── manifestation_repository.py
│   │   │
│   │   ├── middleware/         # Custom middleware
│   │   │   ├── __init__.py
│   │   │   ├── cors.py
│   │   │   ├── error_handler.py
│   │   │   └── rate_limit.py
│   │   │
│   │   ├── utils/              # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── validators.py
│   │   │   ├── helpers.py
│   │   │   └── constants.py
│   │   │
│   │   ├── main.py             # FastAPI application entry point
│   │   └── __init__.py
│   │
│   ├── tests/                  # Test files
│   │   ├── __init__.py
│   │   ├── conftest.py         # Pytest configuration
│   │   ├── unit/               # Unit tests
│   │   │   ├── test_services/
│   │   │   └── test_repositories/
│   │   ├── integration/        # Integration tests
│   │   │   └── test_api/
│   │   └── fixtures/           # Test fixtures
│   │
│   ├── scripts/                # Utility scripts
│   │   ├── init_db.py          # Database initialization
│   │   ├── seed_data.py        # Seed database with test data
│   │   └── backup_db.py        # Database backup script
│   │
│   ├── .env.example            # Environment variables template
│   ├── .flake8                 # Flake8 configuration
│   ├── .python-version         # Python version specification
│   ├── alembic.ini             # Alembic configuration
│   ├── pyproject.toml          # Python project configuration
│   ├── requirements.txt        # Production dependencies
│   ├── requirements-dev.txt    # Development dependencies
│   └── README.md               # Backend documentation
│
├── database/                   # Database related files
│   ├── migrations/             # SQL migration scripts (if needed)
│   ├── seeds/                  # Seed data files
│   │   ├── development/
│   │   └── production/
│   ├── schemas/                # Database schema documentation
│   │   └── schema.sql          # SQL schema export
│   └── README.md               # Database documentation
│
├── docker/                     # Docker configurations
│   ├── frontend/
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   ├── backend/
│   │   └── Dockerfile
│   └── postgres/
│       └── init.sql
│
├── docs/                       # Additional documentation
│   ├── api/                    # API documentation
│   │   └── openapi.yaml        # OpenAPI specification
│   ├── guides/                 # User/developer guides
│   │   ├── setup.md
│   │   ├── deployment.md
│   │   └── contributing.md
│   └── diagrams/               # Architecture diagrams
│       ├── architecture.png
│       └── database-schema.png
│
├── scripts/                    # Project-level scripts
│   ├── setup.sh                # Initial setup script
│   ├── dev.sh                  # Start development environment
│   ├── test.sh                 # Run all tests
│   └── deploy.sh               # Deployment script
│
├── .gitignore                  # Git ignore rules
├── .editorconfig               # Editor configuration
├── docker-compose.yml          # Docker Compose for local development
├── docker-compose.prod.yml     # Docker Compose for production
├── ARCHITECTURE.md             # Architecture documentation
├── FOLDER_STRUCTURE.md         # This file
├── README.md                   # Project overview and setup
└── LICENSE                     # License file
```

## Detailed Directory Purposes

### Frontend (`/frontend`)

#### `/src/api`
API client setup, endpoint definitions, and HTTP interceptors for handling authentication and errors.

#### `/src/components`
- **common**: Reusable UI components used throughout the app (buttons, inputs, modals)
- **layout**: Components that define page structure (headers, sidebars, footers)
- **features**: Feature-specific components organized by domain

#### `/src/contexts`
React Context providers for global state management (authentication, theme, notifications).

#### `/src/hooks`
Custom React hooks for reusable logic (API calls, localStorage, form handling).

#### `/src/pages`
Page-level components that map to routes. Each page may have its own subdirectory with related components.

#### `/src/services`
Frontend service layer that encapsulates API calls and business logic.

#### `/src/types`
TypeScript type definitions and interfaces shared across the frontend.

### Backend (`/backend`)

#### `/app/api`
API layer with versioned endpoints. Each version (v1, v2) contains endpoint modules organized by resource.

#### `/app/core`
Core application configuration including settings, security utilities, and database setup.

#### `/app/models`
SQLAlchemy ORM models representing database tables.

#### `/app/schemas`
Pydantic schemas for request/response validation and serialization.

#### `/app/services`
Business logic layer implementing core application functionality.

#### `/app/repositories`
Data access layer abstracting database operations from services.

#### `/app/middleware`
Custom FastAPI middleware for cross-cutting concerns (CORS, logging, rate limiting).

### Database (`/database`)

Contains database-related files including migration scripts, seed data, and schema documentation.

### Docker (`/docker`)

Dockerfile configurations for each service and any service-specific configuration files.

### Documentation (`/docs`)

Comprehensive project documentation including API specs, setup guides, and architecture diagrams.

## Naming Conventions

### Frontend
- **Components**: PascalCase (e.g., `UserProfile.tsx`)
- **Hooks**: camelCase with `use` prefix (e.g., `useAuth.ts`)
- **Utils/Services**: camelCase (e.g., `formatDate.ts`)
- **Types**: PascalCase with `.types.ts` suffix (e.g., `User.types.ts`)
- **Test files**: `*.test.tsx` or `*.spec.tsx`

### Backend
- **Modules**: snake_case (e.g., `user_service.py`)
- **Classes**: PascalCase (e.g., `UserService`)
- **Functions**: snake_case (e.g., `get_user_by_id`)
- **Test files**: `test_*.py`
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_LOGIN_ATTEMPTS`)

## Monorepo Rationale

We chose a **monorepo approach** for the following reasons:

1. **Unified Version Control**: Single source of truth for all code
2. **Shared Dependencies**: Common tools and configurations across frontend/backend
3. **Atomic Changes**: Frontend and backend changes can be committed together
4. **Simplified CI/CD**: Single repository to monitor and deploy
5. **Easier Refactoring**: Cross-cutting changes are easier to implement
6. **Team Collaboration**: Developers can work across the full stack

### Alternative: Multi-Repo Approach

If the project grows significantly, we could split into separate repositories:
- `lets-manifest-frontend`
- `lets-manifest-backend`
- `lets-manifest-shared` (for shared types/utilities)

This decision can be revisited as the team and codebase scale.

## Best Practices

1. **Module Boundaries**: Maintain clear boundaries between layers (API, Service, Repository)
2. **Co-location**: Keep related files close together (components with their styles and tests)
3. **Flat Structure**: Avoid deep nesting (max 3-4 levels)
4. **Index Files**: Use `index.ts/tsx` for clean imports
5. **Feature Folders**: Group by feature when it makes sense (e.g., `/features/auth`)
6. **Separation of Concerns**: Keep business logic out of components/endpoints
7. **DRY Principle**: Extract reusable code into utilities/services
8. **Type Safety**: Define types/schemas for all data structures

## Migration Path

1. **Phase 1**: Create basic folder structure with README placeholders
2. **Phase 2**: Initialize frontend and backend with basic configuration
3. **Phase 3**: Implement authentication module end-to-end
4. **Phase 4**: Build out core features (journals, manifestations)
5. **Phase 5**: Add testing, documentation, and CI/CD

## References

- [React Project Structure Best Practices](https://react.dev/learn/thinking-in-react)
- [FastAPI Project Structure](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [Monorepo Tools](https://monorepo.tools/)
