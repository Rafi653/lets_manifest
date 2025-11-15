# Let's Manifest - Frontend

## Overview

The frontend application is built with React 18+ and TypeScript, using Vite as the build tool. It provides a modern, responsive user interface for the manifestation journal application.

## Tech Stack

- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **State Management**: React Context API / Redux Toolkit
- **Routing**: React Router v6
- **UI Library**: Material-UI (MUI) or shadcn/ui
- **HTTP Client**: Axios
- **Form Management**: React Hook Form + Zod
- **Testing**: Vitest + React Testing Library
- **Styling**: CSS Modules / Styled Components

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running (see `/backend/README.md`)

### Installation

```bash
cd frontend
npm install
```

### Environment Setup

Copy the example environment file and configure:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=Let's Manifest
```

### Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Build

Build for production:

```bash
npm run build
```

Preview production build:

```bash
npm run preview
```

## Project Structure

```
src/
├── api/              # API client and configurations
├── assets/           # Static assets (images, icons, fonts)
├── components/       # Reusable components
├── contexts/         # React Context providers
├── hooks/            # Custom React hooks
├── pages/            # Page components (routes)
├── routes/           # Routing configuration
├── services/         # Business logic services
├── store/            # State management (Redux)
├── styles/           # Global styles
├── types/            # TypeScript types
└── utils/            # Utility functions
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors
- `npm run format` - Format code with Prettier
- `npm run type-check` - Run TypeScript type checking
- `npm run test` - Run tests
- `npm run test:coverage` - Run tests with coverage

## Code Style

- Use TypeScript for all new files
- Follow React best practices and hooks rules
- Use functional components with hooks
- Keep components small and focused
- Co-locate component files with their styles and tests
- Use meaningful variable and function names
- Add JSDoc comments for complex logic

## Testing

- Unit tests for components and utilities
- Integration tests for feature flows
- E2E tests for critical user journeys
- Aim for 80%+ code coverage

Run tests:

```bash
npm run test
```

## Environment Variables

- `VITE_API_BASE_URL` - Backend API base URL
- `VITE_APP_TITLE` - Application title

## Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Write/update tests
4. Run linter and tests
5. Submit a pull request

## Architecture

See `/ARCHITECTURE.md` for detailed architecture documentation.
