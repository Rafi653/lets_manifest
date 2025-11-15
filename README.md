# Let's Manifest 🌟

A modern, full-stack web application for manifestation journaling, goal tracking, and personal development.

## Overview

Let's Manifest is a digital journal and manifestation tracker that helps users document their thoughts, set intentions, track goals, and manifest their dreams. Built with modern technologies and best practices, it provides a seamless, intuitive experience for users on their personal growth journey.

## Features

- 📝 **Digital Journaling**: Create, edit, and organize journal entries
- 🎯 **Manifestation Tracking**: Set goals and track progress
- 🏷️ **Tagging System**: Organize entries with custom tags
- 🔒 **Secure Authentication**: JWT-based user authentication
- 📊 **Analytics Dashboard**: Visualize your progress and insights
- 🌙 **Rich Text Editor**: Format your entries beautifully
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile

## Tech Stack

### Frontend
- **React 18+** with TypeScript
- **Vite** for fast development and building
- **React Router** for navigation
- **Material-UI / shadcn/ui** for UI components
- **Axios** for API communication

### Backend
- **FastAPI** (Python 3.11+) for high-performance API
- **SQLAlchemy 2.0** for ORM with async support
- **Alembic** for database migrations
- **Pydantic v2** for data validation
- **JWT** for authentication

### Database
- **PostgreSQL 15+** for reliable data storage
- Optimized with proper indexing and connection pooling

### DevOps
- **Docker & Docker Compose** for containerization
- **GitHub Actions** for CI/CD
- **ESLint, Prettier, Black, Ruff** for code quality

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/Rafi653/lets_manifest.git
cd lets_manifest

# Start all services
docker-compose up -d

# Initialize database
docker-compose exec backend alembic upgrade head

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Setup

See the [detailed setup guide](docs/guides/setup.md) for manual installation without Docker.

## Documentation

- **[Architecture Documentation](ARCHITECTURE.md)** - System architecture and design decisions
- **[Folder Structure](FOLDER_STRUCTURE.md)** - Project organization and directory layout
- **[API Documentation](docs/api/API_ENDPOINTS.md)** - Complete API reference
- **[Setup Guide](docs/guides/setup.md)** - Detailed installation and configuration
- **[Frontend README](frontend/README.md)** - Frontend-specific documentation
- **[Backend README](backend/README.md)** - Backend-specific documentation
- **[Database README](database/README.md)** - Database schema and management
- **[QA/Testing Plan](QA_TESTING_PLAN.md)** - Comprehensive testing strategy and QA documentation
- **[QA Quick Start](docs/QA_QUICK_START.md)** - Quick reference guide for testing

## Project Structure

```
lets_manifest/
├── frontend/          # React frontend application
├── backend/           # FastAPI backend API
├── database/          # Database scripts and seeds
├── docker/            # Docker configurations
├── docs/              # Additional documentation
├── scripts/           # Utility scripts
└── docker-compose.yml # Docker Compose configuration
```

## Development

### Prerequisites

- Docker & Docker Compose (recommended)
- OR Node.js 18+, Python 3.11+, and PostgreSQL 15+

### Running Tests

```bash
# Backend tests
cd backend
pytest --cov=app tests/

# Frontend tests
cd frontend
npm run test
```

### Code Quality

```bash
# Backend
cd backend
black app/
ruff check app/
mypy app/

# Frontend
cd frontend
npm run lint
npm run format
npm run type-check
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linters
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

See [CONTRIBUTING.md](docs/guides/contributing.md) for detailed guidelines.

## Roadmap

### Phase 1 (Current)
- [x] Technical architecture definition
- [x] Project structure setup
- [ ] Database schema design
- [ ] Authentication system
- [ ] Basic journal functionality

### Phase 2
- [ ] Manifestation goal tracking
- [ ] Tags and categories
- [ ] Rich text editor
- [ ] Media uploads

### Phase 3
- [ ] Analytics dashboard
- [ ] Advanced search
- [ ] Export functionality
- [ ] Mobile app (React Native)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with ❤️ by the Let's Manifest team
- Inspired by the power of manifestation and personal growth
- Special thanks to all contributors

## Support

- 📫 Email: support@letsmanifest.com
- 💬 GitHub Discussions: [Ask questions](https://github.com/Rafi653/lets_manifest/discussions)
- 🐛 Issues: [Report bugs](https://github.com/Rafi653/lets_manifest/issues)

---

**Start manifesting your dreams today!** ✨