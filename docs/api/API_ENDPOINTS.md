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

## Daily Reviews

### GET /daily-reviews

List all daily reviews for the current user with optional filtering.

**Auth Required:** Yes

**Query Parameters:**
- `start_date` (optional): ISO date string for filtering reviews from this date
- `end_date` (optional): ISO date string for filtering reviews up to this date
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Results per page (default: 20, max: 100)

**Response (200 OK):**
```json
{
  "data": {
    "items": [
      {
        "id": "uuid",
        "user_id": "uuid",
        "review_date": "2025-11-15",
        "mood_rating": 8,
        "energy_level": 7,
        "productivity_rating": 9,
        "sleep_hours": 7.5,
        "sleep_quality": 8,
        "water_intake_ml": 2000,
        "screen_time_minutes": 360,
        "steps": 10000,
        "accomplishments": "Completed project milestone",
        "challenges": "Dealt with unexpected bugs",
        "lessons_learned": "Importance of thorough testing",
        "gratitude": "Grateful for supportive team",
        "tomorrow_intentions": "Focus on code review",
        "highlights": "Successfully deployed new feature",
        "created_at": "2025-11-15T22:00:00Z",
        "updated_at": "2025-11-15T22:30:00Z"
      }
    ],
    "total": 30,
    "page": 1,
    "limit": 20,
    "total_pages": 2
  },
  "message": "Daily reviews retrieved successfully"
}
```

### POST /daily-reviews

Create a new daily review entry.

**Auth Required:** Yes

**Request Body:**
```json
{
  "review_date": "2025-11-15",
  "mood_rating": 8,
  "energy_level": 7,
  "productivity_rating": 9,
  "sleep_hours": 7.5,
  "sleep_quality": 8,
  "water_intake_ml": 2000,
  "screen_time_minutes": 360,
  "steps": 10000,
  "accomplishments": "Completed project milestone",
  "challenges": "Dealt with unexpected bugs",
  "lessons_learned": "Importance of thorough testing",
  "gratitude": "Grateful for supportive team",
  "tomorrow_intentions": "Focus on code review",
  "highlights": "Successfully deployed new feature"
}
```

**Response (201 Created):**
```json
{
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "review_date": "2025-11-15",
    "mood_rating": 8,
    "energy_level": 7,
    "productivity_rating": 9,
    "sleep_hours": 7.5,
    "sleep_quality": 8,
    "water_intake_ml": 2000,
    "screen_time_minutes": 360,
    "steps": 10000,
    "accomplishments": "Completed project milestone",
    "challenges": "Dealt with unexpected bugs",
    "lessons_learned": "Importance of thorough testing",
    "gratitude": "Grateful for supportive team",
    "tomorrow_intentions": "Focus on code review",
    "highlights": "Successfully deployed new feature",
    "created_at": "2025-11-15T22:00:00Z",
    "updated_at": null
  },
  "message": "Daily review created successfully"
}
```

### GET /daily-reviews/{review_id}

Get a specific daily review by ID.

**Auth Required:** Yes

**Response (200 OK):**
```json
{
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "review_date": "2025-11-15",
    "mood_rating": 8,
    "energy_level": 7,
    "productivity_rating": 9,
    "sleep_hours": 7.5,
    "sleep_quality": 8,
    "water_intake_ml": 2000,
    "screen_time_minutes": 360,
    "steps": 10000,
    "accomplishments": "Completed project milestone",
    "challenges": "Dealt with unexpected bugs",
    "lessons_learned": "Importance of thorough testing",
    "gratitude": "Grateful for supportive team",
    "tomorrow_intentions": "Focus on code review",
    "highlights": "Successfully deployed new feature",
    "created_at": "2025-11-15T22:00:00Z",
    "updated_at": null
  },
  "message": "Daily review retrieved successfully"
}
```

### PUT /daily-reviews/{review_id}

Update a daily review entry.

**Auth Required:** Yes

**Request Body:**
```json
{
  "mood_rating": 9,
  "energy_level": 8,
  "accomplishments": "Updated accomplishments text"
}
```

**Response (200 OK):**
```json
{
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "review_date": "2025-11-15",
    "mood_rating": 9,
    "energy_level": 8,
    "productivity_rating": 9,
    "sleep_hours": 7.5,
    "sleep_quality": 8,
    "water_intake_ml": 2000,
    "screen_time_minutes": 360,
    "steps": 10000,
    "accomplishments": "Updated accomplishments text",
    "challenges": "Dealt with unexpected bugs",
    "lessons_learned": "Importance of thorough testing",
    "gratitude": "Grateful for supportive team",
    "tomorrow_intentions": "Focus on code review",
    "highlights": "Successfully deployed new feature",
    "created_at": "2025-11-15T22:00:00Z",
    "updated_at": "2025-11-15T23:00:00Z"
  },
  "message": "Daily review updated successfully"
}
```

### DELETE /daily-reviews/{review_id}

Delete a daily review entry.

**Auth Required:** Yes

**Response (200 OK):**
```json
{
  "data": {
    "deleted": true
  },
  "message": "Daily review deleted successfully"
}
```

## Blog Entries

### GET /blog-entries

List all blog entries for the current user with optional filtering.

**Auth Required:** Yes

**Query Parameters:**
- `status_filter` (optional): Filter by status ('draft', 'published', 'archived')
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Results per page (default: 20, max: 100)

**Response (200 OK):**
```json
{
  "data": {
    "items": [
      {
        "id": "uuid",
        "user_id": "uuid",
        "title": "My Journey with Manifestation",
        "content": "Today I learned...",
        "excerpt": "A brief summary of my manifestation journey",
        "slug": "my-journey-with-manifestation",
        "status": "published",
        "is_public": true,
        "is_featured": false,
        "view_count": 42,
        "published_at": "2025-11-15T10:00:00Z",
        "created_at": "2025-11-15T09:00:00Z",
        "updated_at": "2025-11-15T10:00:00Z"
      }
    ],
    "total": 15,
    "page": 1,
    "limit": 20,
    "total_pages": 1
  },
  "message": "Blog entries retrieved successfully"
}
```

### POST /blog-entries

Create a new blog entry.

**Auth Required:** Yes

**Request Body:**
```json
{
  "title": "My Journey with Manifestation",
  "content": "Today I learned about the power of visualization...",
  "excerpt": "A brief summary of my manifestation journey",
  "status": "draft",
  "is_public": false,
  "is_featured": false
}
```

**Response (201 Created):**
```json
{
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "My Journey with Manifestation",
    "content": "Today I learned about the power of visualization...",
    "excerpt": "A brief summary of my manifestation journey",
    "slug": "my-journey-with-manifestation",
    "status": "draft",
    "is_public": false,
    "is_featured": false,
    "view_count": 0,
    "published_at": null,
    "created_at": "2025-11-15T09:00:00Z",
    "updated_at": null
  },
  "message": "Blog entry created successfully"
}
```

### POST /blog-entries/generate-from-review/{review_id}

Generate a blog entry automatically from a daily review.

**Auth Required:** Yes

**Response (201 Created):**
```json
{
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "Daily Reflection: November 15, 2025",
    "content": "## How I Felt Today\nMood: 8/10\nEnergy Level: 7/10\n\n## Today's Metrics\nSteps: 10,000\nScreen Time: 6h 0m\n\n## Accomplishments\nCompleted project milestone...",
    "excerpt": "Completed project milestone...",
    "slug": "daily-reflection-november-15-2025",
    "status": "draft",
    "is_public": false,
    "is_featured": false,
    "view_count": 0,
    "published_at": null,
    "created_at": "2025-11-15T22:00:00Z",
    "updated_at": null
  },
  "message": "Blog entry generated successfully from daily review"
}
```

### GET /blog-entries/{entry_id}

Get a specific blog entry by ID.

**Auth Required:** Yes

**Response (200 OK):**
```json
{
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "My Journey with Manifestation",
    "content": "Today I learned about the power of visualization...",
    "excerpt": "A brief summary of my manifestation journey",
    "slug": "my-journey-with-manifestation",
    "status": "published",
    "is_public": true,
    "is_featured": false,
    "view_count": 42,
    "published_at": "2025-11-15T10:00:00Z",
    "created_at": "2025-11-15T09:00:00Z",
    "updated_at": "2025-11-15T10:00:00Z"
  },
  "message": "Blog entry retrieved successfully"
}
```

### PUT /blog-entries/{entry_id}

Update a blog entry.

**Auth Required:** Yes

**Request Body:**
```json
{
  "title": "Updated Title",
  "status": "published",
  "is_public": true
}
```

**Response (200 OK):**
```json
{
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "Updated Title",
    "content": "Today I learned about the power of visualization...",
    "excerpt": "A brief summary of my manifestation journey",
    "slug": "updated-title",
    "status": "published",
    "is_public": true,
    "is_featured": false,
    "view_count": 42,
    "published_at": "2025-11-15T11:00:00Z",
    "created_at": "2025-11-15T09:00:00Z",
    "updated_at": "2025-11-15T11:00:00Z"
  },
  "message": "Blog entry updated successfully"
}
```

### DELETE /blog-entries/{entry_id}

Delete a blog entry.

**Auth Required:** Yes

**Response (200 OK):**
```json
{
  "data": {
    "deleted": true
  },
  "message": "Blog entry deleted successfully"
}
```

## Field Descriptions

### Daily Review Fields

- `review_date` (required): ISO date string for the review date
- `mood_rating` (optional): Integer 1-10 rating for mood
- `energy_level` (optional): Integer 1-10 rating for energy
- `productivity_rating` (optional): Integer 1-10 rating for productivity
- `sleep_hours` (optional): Decimal 0-24 for hours of sleep
- `sleep_quality` (optional): Integer 1-10 rating for sleep quality
- `water_intake_ml` (optional): Integer for water consumed in milliliters
- `screen_time_minutes` (optional): Integer for total screen time in minutes
- `steps` (optional): Integer for total steps walked
- `accomplishments` (optional): Text field for daily accomplishments
- `challenges` (optional): Text field for challenges faced
- `lessons_learned` (optional): Text field for lessons learned
- `gratitude` (optional): Text field for things to be grateful for
- `tomorrow_intentions` (optional): Text field for next day's intentions
- `highlights` (optional): Text field for day's highlights

### Blog Entry Fields

- `title` (required): String up to 500 characters for the blog post title
- `content` (required): Text field for the main blog content
- `excerpt` (optional): Text field for a brief summary or preview
- `status` (optional): Enum ('draft', 'published', 'archived'), default 'draft'
- `is_public` (optional): Boolean for public visibility, default false
- `is_featured` (optional): Boolean for featured status, default false
- `slug`: Auto-generated URL-friendly version of the title
- `view_count`: Auto-tracked number of views
- `published_at`: Auto-set timestamp when status changes to 'published'

## Notes

- All rating fields (mood_rating, energy_level, etc.) must be integers between 1 and 10
- Sleep hours must be between 0 and 24
- All numeric health metrics (water_intake_ml, screen_time_minutes, steps) must be non-negative
- Only one daily review can exist per user per date
- Blog entry slug is automatically generated from the title
- When a blog entry status changes to 'published', the published_at timestamp is set automatically
- All timestamps are in UTC format
