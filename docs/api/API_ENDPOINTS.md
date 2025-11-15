# API Endpoints Documentation

## Base URL

```
Development: http://localhost:8000/api/v1
Production: https://api.letsmanifest.com/api/v1
```

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## Endpoints Overview

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and get JWT token | No |
| POST | `/auth/refresh` | Refresh access token | No (refresh token) |
| POST | `/auth/logout` | Logout and invalidate token | Yes |
| POST | `/auth/forgot-password` | Request password reset | No |
| POST | `/auth/reset-password` | Reset password with token | No |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users/me` | Get current user profile | Yes |
| PUT | `/users/me` | Update current user profile | Yes |
| DELETE | `/users/me` | Delete current user account | Yes |
| GET | `/users/me/stats` | Get user statistics | Yes |

### Journals

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/journals` | List all journal entries | Yes |
| POST | `/journals` | Create a new journal entry | Yes |
| GET | `/journals/{id}` | Get specific journal entry | Yes |
| PUT | `/journals/{id}` | Update journal entry | Yes |
| DELETE | `/journals/{id}` | Delete journal entry | Yes |
| GET | `/journals/{id}/media` | Get journal media files | Yes |
| POST | `/journals/{id}/media` | Upload media to journal | Yes |

### Manifestations

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/manifestations` | List all manifestations | Yes |
| POST | `/manifestations` | Create a new manifestation | Yes |
| GET | `/manifestations/{id}` | Get specific manifestation | Yes |
| PUT | `/manifestations/{id}` | Update manifestation | Yes |
| DELETE | `/manifestations/{id}` | Delete manifestation | Yes |
| POST | `/manifestations/{id}/progress` | Update progress | Yes |

### Tags

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/tags` | List all tags | Yes |
| POST | `/tags` | Create a new tag | Yes |
| GET | `/tags/{id}` | Get specific tag | Yes |
| PUT | `/tags/{id}` | Update tag | Yes |
| DELETE | `/tags/{id}` | Delete tag | Yes |

## Detailed Endpoint Specifications

### POST /auth/register

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "created_at": "2025-11-15T02:13:00Z"
  },
  "message": "User registered successfully",
  "errors": null,
  "meta": {
    "timestamp": "2025-11-15T02:13:00Z",
    "request_id": "uuid"
  }
}
```

### POST /auth/login

Authenticate and receive JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
  },
  "message": "Login successful",
  "errors": null,
  "meta": {
    "timestamp": "2025-11-15T02:13:00Z",
    "request_id": "uuid"
  }
}
```

### GET /journals

List user's journal entries with pagination and filtering.

**Query Parameters:**
- `page` (integer, default: 1): Page number
- `limit` (integer, default: 20): Items per page
- `search` (string, optional): Search in content
- `tag_ids` (array, optional): Filter by tag IDs
- `start_date` (date, optional): Filter from date
- `end_date` (date, optional): Filter to date
- `sort_by` (string, default: "created_at"): Sort field
- `sort_order` (string, default: "desc"): Sort order (asc/desc)

**Response (200 OK):**
```json
{
  "data": {
    "items": [
      {
        "id": "uuid",
        "title": "Today's Gratitude",
        "content": "I am grateful for...",
        "created_at": "2025-11-15T02:13:00Z",
        "updated_at": "2025-11-15T02:13:00Z",
        "tags": [
          {
            "id": "uuid",
            "name": "gratitude",
            "color": "#4CAF50"
          }
        ]
      }
    ],
    "total": 150,
    "page": 1,
    "limit": 20,
    "total_pages": 8
  },
  "message": "Journals retrieved successfully",
  "errors": null,
  "meta": {
    "timestamp": "2025-11-15T02:13:00Z",
    "request_id": "uuid"
  }
}
```

### POST /journals

Create a new journal entry.

**Request Body:**
```json
{
  "title": "Today's Gratitude",
  "content": "I am grateful for all the blessings in my life...",
  "tag_ids": ["uuid1", "uuid2"],
  "is_private": true
}
```

**Response (201 Created):**
```json
{
  "data": {
    "id": "uuid",
    "title": "Today's Gratitude",
    "content": "I am grateful for all the blessings in my life...",
    "created_at": "2025-11-15T02:13:00Z",
    "updated_at": "2025-11-15T02:13:00Z",
    "is_private": true,
    "tags": [
      {
        "id": "uuid1",
        "name": "gratitude",
        "color": "#4CAF50"
      }
    ]
  },
  "message": "Journal entry created successfully",
  "errors": null,
  "meta": {
    "timestamp": "2025-11-15T02:13:00Z",
    "request_id": "uuid"
  }
}
```

### POST /manifestations

Create a new manifestation goal.

**Request Body:**
```json
{
  "title": "Career Success",
  "description": "Land my dream job as a senior developer",
  "target_date": "2026-06-01",
  "affirmations": [
    "I am worthy of success",
    "Opportunities come to me easily"
  ],
  "tag_ids": ["uuid1"]
}
```

**Response (201 Created):**
```json
{
  "data": {
    "id": "uuid",
    "title": "Career Success",
    "description": "Land my dream job as a senior developer",
    "target_date": "2026-06-01",
    "status": "active",
    "progress": 0,
    "affirmations": [
      "I am worthy of success",
      "Opportunities come to me easily"
    ],
    "created_at": "2025-11-15T02:13:00Z",
    "updated_at": "2025-11-15T02:13:00Z"
  },
  "message": "Manifestation created successfully",
  "errors": null,
  "meta": {
    "timestamp": "2025-11-15T02:13:00Z",
    "request_id": "uuid"
  }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "data": null,
  "message": "Invalid request data",
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

### 401 Unauthorized
```json
{
  "data": null,
  "message": "Authentication required",
  "errors": null,
  "meta": {
    "timestamp": "2025-11-15T02:13:00Z",
    "request_id": "uuid"
  }
}
```

### 404 Not Found
```json
{
  "data": null,
  "message": "Resource not found",
  "errors": null,
  "meta": {
    "timestamp": "2025-11-15T02:13:00Z",
    "request_id": "uuid"
  }
}
```

### 422 Validation Error
```json
{
  "data": null,
  "message": "Validation error",
  "errors": [
    {
      "field": "password",
      "message": "Password must be at least 8 characters"
    }
  ],
  "meta": {
    "timestamp": "2025-11-15T02:13:00Z",
    "request_id": "uuid"
  }
}
```

### 500 Internal Server Error
```json
{
  "data": null,
  "message": "Internal server error",
  "errors": null,
  "meta": {
    "timestamp": "2025-11-15T02:13:00Z",
    "request_id": "uuid"
  }
}
```

## Rate Limiting

- Anonymous endpoints: 100 requests per 15 minutes
- Authenticated endpoints: 1000 requests per 15 minutes
- Rate limit headers included in responses:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Pagination

List endpoints support pagination with the following parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

Response includes pagination metadata:
```json
{
  "total": 150,
  "page": 1,
  "limit": 20,
  "total_pages": 8
}
```

## Filtering and Sorting

Most list endpoints support:
- `search`: Full-text search
- `sort_by`: Field to sort by
- `sort_order`: `asc` or `desc`
- Resource-specific filters (dates, tags, status, etc.)

## API Versioning

The API uses URL-based versioning:
- Current version: `/api/v1/`
- Future versions: `/api/v2/`, etc.

## OpenAPI/Swagger

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
