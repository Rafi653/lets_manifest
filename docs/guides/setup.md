# Let's Manifest - Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

### Required
- **Git**: Version control
- **Docker & Docker Compose**: For containerized development (recommended)
- **Node.js**: 18+ with npm or yarn (if not using Docker)
- **Python**: 3.11+ with pip (if not using Docker)
- **PostgreSQL**: 15+ (if not using Docker)

### Optional
- **make**: For using Makefile commands
- **VS Code**: Recommended IDE with extensions

## Quick Start (Docker - Recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/Rafi653/lets_manifest.git
cd lets_manifest
```

### 2. Start with Docker Compose

```bash
# Start all services (database, backend, frontend)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 3. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432

### 4. Initialize Database

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Seed development data (optional)
docker-compose exec backend python scripts/seed_data.py
```

That's it! The application should now be running.

## Manual Setup (Without Docker)

### 1. Clone the Repository

```bash
git clone https://github.com/Rafi653/lets_manifest.git
cd lets_manifest
```

### 2. Setup PostgreSQL

Install PostgreSQL and create a database:

```bash
# On Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# On macOS
brew install postgresql@15
brew services start postgresql@15
```

Create database and user:

```bash
psql postgres
```

```sql
CREATE DATABASE lets_manifest_dev;
CREATE USER lets_manifest_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE lets_manifest_dev TO lets_manifest_user;
\q
```

### 3. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copy environment file
cp .env.example .env

# Edit .env with your database credentials
nano .env

# Run migrations
alembic upgrade head

# Seed data (optional)
python scripts/seed_data.py

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at http://localhost:8000

### 4. Setup Frontend

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Edit .env if needed
nano .env

# Start development server
npm run dev
```

Frontend will be available at http://localhost:5173

## Environment Configuration

### Backend (.env)

Create `backend/.env` from `backend/.env.example`:

```env
# Application
APP_NAME=Let's Manifest API
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql+asyncpg://lets_manifest_user:your_password@localhost:5432/lets_manifest_dev
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# Security
SECRET_KEY=your-secret-key-here-generate-a-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

Generate a secure SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Frontend (.env)

Create `frontend/.env` from `frontend/.env.example`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=Let's Manifest
```

## Development Workflow

### Running Tests

#### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/  # With coverage
pytest tests/unit/  # Run specific tests
```

#### Frontend Tests
```bash
cd frontend
npm run test
npm run test:coverage  # With coverage
```

### Code Formatting

#### Backend
```bash
cd backend
black app/  # Format code
ruff check app/  # Lint code
ruff check --fix app/  # Fix linting issues
mypy app/  # Type checking
```

#### Frontend
```bash
cd frontend
npm run format  # Format with Prettier
npm run lint  # Run ESLint
npm run lint:fix  # Fix ESLint issues
npm run type-check  # TypeScript type checking
```

### Database Migrations

#### Create a new migration
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

#### Apply migrations
```bash
alembic upgrade head
```

#### Rollback migration
```bash
alembic downgrade -1
```

#### View migration history
```bash
alembic history
alembic current
```

## IDE Setup

### VS Code

Recommended extensions:
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- ESLint (dbaeumer.vscode-eslint)
- Prettier (esbenp.prettier-vscode)
- TypeScript (ms-vscode.typescript)
- Docker (ms-azuretools.vscode-docker)
- GitLens (eamodio.gitlens)

Workspace settings (`.vscode/settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

## Common Issues

### Port Already in Use

If you get "port already in use" errors:

```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Find and kill process using port 5173
lsof -ti:5173 | xargs kill -9
```

### Database Connection Issues

1. Check PostgreSQL is running:
```bash
sudo systemctl status postgresql
# or on macOS
brew services list
```

2. Verify connection:
```bash
psql -U lets_manifest_user -h localhost -d lets_manifest_dev
```

3. Check DATABASE_URL in `.env` is correct

### Module Not Found Errors

#### Backend
```bash
cd backend
pip install -r requirements.txt
```

#### Frontend
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Migration Issues

If migrations fail:

```bash
# Check current version
alembic current

# View history
alembic history

# Downgrade and re-apply
alembic downgrade -1
alembic upgrade head
```

## Next Steps

1. **Read the Documentation**
   - [ARCHITECTURE.md](../ARCHITECTURE.md) - Technical architecture
   - [FOLDER_STRUCTURE.md](../FOLDER_STRUCTURE.md) - Project organization
   - [API_ENDPOINTS.md](../docs/api/API_ENDPOINTS.md) - API documentation

2. **Explore the Code**
   - Frontend: Start with `frontend/src/App.tsx`
   - Backend: Start with `backend/app/main.py`

3. **Make Your First Change**
   - Create a feature branch
   - Make changes
   - Write tests
   - Submit a pull request

4. **Join the Team**
   - Read [CONTRIBUTING.md](../docs/guides/contributing.md)
   - Check open issues
   - Ask questions in discussions

## Getting Help

- **Documentation**: Check `/docs` directory
- **Issues**: GitHub Issues for bugs and features
- **Discussions**: GitHub Discussions for questions

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
