# Frontend Components

This directory contains all React components used in the application.

## Structure

```
components/
├── common/       # Reusable UI components
├── layout/       # Layout components (Header, Sidebar, Footer)
└── features/     # Feature-specific components
```

## Component Guidelines

1. **Keep components small and focused** - Each component should do one thing well
2. **Use TypeScript** - All components should have proper type definitions
3. **Co-locate related files** - Keep component, styles, and tests together
4. **Write tests** - Every component should have unit tests
5. **Use meaningful names** - Component names should clearly describe their purpose

## Example Component Structure

```
Button/
├── Button.tsx           # Component implementation
├── Button.module.css    # Component styles
├── Button.test.tsx      # Component tests
├── Button.types.ts      # Type definitions
└── index.ts             # Barrel export
```

## Common Components

Place truly reusable components here (buttons, inputs, modals, cards, etc.)

## Layout Components

Components that define page structure (headers, sidebars, footers, page layouts)

## Feature Components

Feature-specific components organized by domain (auth, journal, manifestation, etc.)
