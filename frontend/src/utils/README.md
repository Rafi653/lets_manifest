# Utility Functions

This directory contains utility functions and helper methods used throughout the application.

## Purpose

Utilities help:
- Avoid code duplication
- Centralize common operations
- Keep components clean and focused
- Make testing easier

## Common Utilities

- `formatters.ts` - Date, number, and text formatting functions
- `validators.ts` - Input validation functions
- `constants.ts` - Application-wide constants
- `helpers.ts` - General helper functions

## Example

```typescript
// utils/formatters.ts
export const formatDate = (date: string | Date): string => {
  const d = new Date(date);
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

export const formatNumber = (num: number): string => {
  return new Intl.NumberFormat('en-US').format(num);
};
```
