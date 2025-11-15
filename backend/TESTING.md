# Backend API Testing Guide

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 3. Start the API Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python -m app.main
```

### 4. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Overview

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication

All protected endpoints require a JWT Bearer token in the Authorization header:

```bash
Authorization: Bearer <your_jwt_token>
```

## Testing with cURL

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "SecurePassword123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

Save the `access_token` from the response.

### 3. Create a Goal

```bash
curl -X POST http://localhost:8000/api/v1/goals \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "title": "Complete Marathon",
    "description": "Run a full marathon",
    "goal_type": "yearly",
    "category": "fitness",
    "target_value": 42.195,
    "target_unit": "km",
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "priority": 5
  }'
```

### 4. List Goals

```bash
curl -X GET "http://localhost:8000/api/v1/goals?page=1&limit=20" \
  -H "Authorization: Bearer <your_access_token>"
```

### 5. Create a Habit

```bash
curl -X POST http://localhost:8000/api/v1/habits \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "name": "Morning Meditation",
    "description": "Meditate for 10 minutes every morning",
    "frequency": "daily",
    "category": "wellness",
    "color": "#4CAF50"
  }'
```

### 6. Log Food Entry

```bash
curl -X POST http://localhost:8000/api/v1/foods \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "meal_date": "2025-11-15",
    "meal_type": "breakfast",
    "food_name": "Oatmeal with berries",
    "calories": 350,
    "protein_grams": 12,
    "carbs_grams": 65,
    "fats_grams": 5
  }'
```

### 7. Create Workout

```bash
curl -X POST http://localhost:8000/api/v1/workouts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "workout_date": "2025-11-15",
    "workout_type": "Strength Training",
    "duration_minutes": 60,
    "intensity": "high",
    "exercises": [
      {
        "exercise_name": "Bench Press",
        "sets": 4,
        "reps": 10,
        "weight": 135,
        "weight_unit": "lbs"
      },
      {
        "exercise_name": "Squats",
        "sets": 4,
        "reps": 12,
        "weight": 185,
        "weight_unit": "lbs"
      }
    ]
  }'
```

### 8. Create Daily Review

```bash
curl -X POST http://localhost:8000/api/v1/daily-reviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "review_date": "2025-11-15",
    "mood_rating": 8,
    "energy_level": 7,
    "productivity_rating": 9,
    "sleep_hours": 7.5,
    "sleep_quality": 8,
    "accomplishments": "Completed 3 major tasks",
    "gratitude": "Grateful for my health and family"
  }'
```

### 9. Create Blog Entry

```bash
curl -X POST http://localhost:8000/api/v1/blog-entries \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "title": "My Journey to Better Health",
    "content": "Today marks the beginning of...",
    "status": "published",
    "is_public": true
  }'
```

### 10. Create Progress Snapshot

```bash
curl -X POST http://localhost:8000/api/v1/progress \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "snapshot_date": "2025-11-15",
    "snapshot_type": "weekly",
    "total_goals": 5,
    "completed_goals": 2,
    "active_habits": 3,
    "total_workouts": 4,
    "average_daily_mood": 8.5
  }'
```

## Available Modules & Endpoints

### Authentication (3 endpoints)
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get tokens
- `POST /auth/logout` - Logout (client-side)

### Users (3 endpoints)
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update user profile
- `DELETE /users/me` - Delete user account

### Goals (7 endpoints)
- `GET /goals` - List all goals
- `POST /goals` - Create a goal
- `GET /goals/{id}` - Get specific goal
- `PUT /goals/{id}` - Update goal
- `DELETE /goals/{id}` - Delete goal
- `POST /goals/{id}/progress` - Add progress entry
- `GET /goals/{id}/progress` - Get progress entries

### Habits (7 endpoints)
- `GET /habits` - List all habits
- `POST /habits` - Create a habit
- `GET /habits/{id}` - Get specific habit
- `PUT /habits/{id}` - Update habit
- `DELETE /habits/{id}` - Delete habit
- `POST /habits/{id}/entries` - Create habit entry
- `GET /habits/{id}/entries` - Get habit entries

### Food Tracking (5 endpoints)
- `GET /foods` - List all food entries
- `POST /foods` - Create food entry
- `GET /foods/{id}` - Get specific food entry
- `PUT /foods/{id}` - Update food entry
- `DELETE /foods/{id}` - Delete food entry

### Workouts (5 endpoints)
- `GET /workouts` - List all workouts
- `POST /workouts` - Create workout
- `GET /workouts/{id}` - Get specific workout
- `PUT /workouts/{id}` - Update workout
- `DELETE /workouts/{id}` - Delete workout

### Daily Reviews (5 endpoints)
- `GET /daily-reviews` - List all daily reviews
- `POST /daily-reviews` - Create daily review
- `GET /daily-reviews/{id}` - Get specific review
- `PUT /daily-reviews/{id}` - Update review
- `DELETE /daily-reviews/{id}` - Delete review

### Blog Entries (5 endpoints)
- `GET /blog-entries` - List all blog entries
- `POST /blog-entries` - Create blog entry
- `GET /blog-entries/{id}` - Get specific entry
- `PUT /blog-entries/{id}` - Update entry
- `DELETE /blog-entries/{id}` - Delete entry

### Progress Tracking (5 endpoints)
- `GET /progress` - List all progress snapshots
- `POST /progress` - Create progress snapshot
- `GET /progress/{id}` - Get specific snapshot
- `PUT /progress/{id}` - Update snapshot
- `DELETE /progress/{id}` - Delete snapshot

## Response Format

All responses follow a consistent format:

```json
{
  "data": { ... },
  "message": "Success message",
  "errors": null,
  "meta": {
    "timestamp": "2025-11-15T02:59:00Z",
    "request_id": null
  }
}
```

### Success Response (200/201)

```json
{
  "data": {
    "id": "uuid",
    "title": "Complete Marathon",
    ...
  },
  "message": "Goal created successfully",
  "errors": null,
  "meta": { ... }
}
```

### Error Response (400/401/404/422)

```json
{
  "data": null,
  "message": "Validation error",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ],
  "meta": { ... }
}
```

## Pagination

List endpoints support pagination:

```bash
GET /api/v1/goals?page=1&limit=20
```

Response includes pagination metadata:

```json
{
  "data": {
    "items": [...],
    "total": 150,
    "page": 1,
    "limit": 20,
    "total_pages": 8
  }
}
```

## Filtering & Sorting

Many endpoints support filtering:

```bash
# Goals by type
GET /api/v1/goals?goal_type=daily&status=active

# Foods by meal type and date range
GET /api/v1/foods?meal_type=breakfast&start_date=2025-11-01&end_date=2025-11-15

# Workouts by type
GET /api/v1/workouts?workout_type=Cardio
```

## Development

### Run with Docker

```bash
# From project root
docker-compose up -d backend

# Check logs
docker-compose logs -f backend
```

### Code Quality

```bash
# Format code
black app/

# Lint code
ruff check app/

# Type checking (if mypy is configured)
mypy app/
```

## Testing

### Using Swagger UI

1. Navigate to http://localhost:8000/docs
2. Click "Authorize" button
3. Enter your JWT token
4. Test any endpoint interactively

### Using Postman

Import the OpenAPI schema from http://localhost:8000/openapi.json into Postman for a complete collection.

## Troubleshooting

### Database Connection Issues

Ensure PostgreSQL is running and accessible:

```bash
# Check database connection
psql -h localhost -U lets_manifest_user -d lets_manifest_dev
```

### Import Errors

Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Port Already in Use

Change the port in the uvicorn command:

```bash
uvicorn app.main:app --reload --port 8001
```

## Next Steps

1. Set up database migrations with Alembic
2. Add unit and integration tests
3. Configure rate limiting
4. Add caching layer (Redis)
5. Set up CI/CD pipeline
6. Deploy to production
