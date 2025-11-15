# Let's Manifest - Frontend

Welcome to the Let's Manifest frontend! This is a React application built with TypeScript and Vite, designed for tracking goals, habits, nutrition, workouts, and overall personal progress.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Backend API running (see `/backend/README.md`)

### Installation

```bash
cd frontend
npm install
```

### Environment Setup

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your configuration (default values work for local development):
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

## 📁 Project Structure

```
src/
├── api/              # API client configuration
├── assets/           # Static assets (images, icons)
├── components/       # Reusable components
│   ├── common/       # Common UI components
│   └── layout/       # Layout components (Header, Footer, etc.)
├── contexts/         # React Context providers
├── hooks/            # Custom React hooks
├── pages/            # Page components (routes)
│   ├── Dashboard/    # Main dashboard
│   ├── Goals/        # Goals tracking
│   ├── Habits/       # Habits tracking
│   ├── Food/         # Food/nutrition tracking
│   ├── Workouts/     # Workout tracking
│   ├── Review/       # Daily reviews
│   ├── Blog/         # Blog entries
│   └── Progress/     # Progress visualization
├── routes/           # Routing configuration
├── services/         # Business logic services
├── styles/           # Global styles
├── types/            # TypeScript type definitions
└── utils/            # Utility functions
```

## 🛠️ Tech Stack

- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Styling**: CSS Modules
- **Code Quality**: ESLint

## 📜 Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint to check code quality

## 🎨 Code Style

- Use TypeScript for all new files
- Follow React best practices and hooks rules
- Use functional components with hooks
- Keep components small and focused
- Co-locate component files with their styles
- Use meaningful variable and function names

## 🗺️ Application Routes

The application includes the following main sections:

- `/` - Dashboard (home page)
- `/goals` - Goals tracking and management
- `/habits` - Daily habits tracking
- `/food` - Food and nutrition tracking
- `/workouts` - Workout logging
- `/review` - Daily reflection and review
- `/blog` - Personal blog entries
- `/progress` - Overall progress visualization

## 🔧 Development Guidelines

### Adding a New Page

1. Create a new directory in `src/pages/`
2. Add the component file (e.g., `MyPage.tsx`)
3. Create an `index.ts` barrel export
4. Add the route in `src/routes/AppRouter.tsx`
5. Update navigation in `src/components/layout/Header/Header.tsx`

### Adding a New Component

1. Create a directory in `src/components/common/` or `src/components/layout/`
2. Add the component file (e.g., `MyComponent.tsx`)
3. Add styles if needed (e.g., `MyComponent.css`)
4. Create an `index.ts` barrel export
5. Document the component's props with TypeScript interfaces

### Working with the API

1. Define types in `src/types/`
2. Create service functions in `src/services/`
3. Configure API client in `src/api/`
4. Use services in components or custom hooks

## 🤝 Contributing

1. Create a feature branch from `main`
2. Make your changes following the code style guidelines
3. Test your changes locally
4. Run linter: `npm run lint`
5. Build to ensure no errors: `npm run build`
6. Submit a pull request

## 📚 Learn More

- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Vite Documentation](https://vitejs.dev/)
- [React Router Documentation](https://reactrouter.com/)

## 🎯 Next Steps for Development

- [ ] Implement authentication flow
- [ ] Add form validation with Zod
- [ ] Integrate with backend API
- [ ] Add loading states and error handling
- [ ] Implement state management (Context or Redux)
- [ ] Add unit tests with Vitest
- [ ] Add E2E tests
- [ ] Implement responsive design improvements
- [ ] Add accessibility features (ARIA labels, keyboard navigation)

## 🐛 Troubleshooting

### Port 5173 is already in use
```bash
# Kill the process using the port
lsof -ti:5173 | xargs kill -9
```

### Node modules issues
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

### Build errors
```bash
# Check TypeScript errors
npm run build
```

## 📄 License

See the LICENSE file in the root of the project.

