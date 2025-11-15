# API Client

This directory contains API client configuration and utilities for making HTTP requests to the backend.

## Files

- `client.ts` - Axios instance configuration
- `endpoints.ts` - API endpoint definitions
- `interceptors.ts` - Request/response interceptors

## Usage

```typescript
import api from './api/client';

// Example API call
const response = await api.get('/users/me');
```

## Configuration

API configuration is managed through environment variables:
- `VITE_API_BASE_URL` - Backend API base URL
