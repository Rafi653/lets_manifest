# Daily Review & Blog API Documentation

## Daily Reviews API

### Overview
The Daily Reviews API allows users to track their daily activities, reflections, and metrics including mood, energy, productivity, sleep, health metrics, and reflections.

### Endpoints

#### List Daily Reviews
```
GET /api/v1/daily-reviews
```

**Query Parameters:**
- `start_date` (optional): ISO date string
- `end_date` (optional): ISO date string
- `page` (optional): Page number (default: 1)
- `limit` (optional): Results per page (default: 20, max: 100)

**Response:** Paginated list of daily reviews

#### Create Daily Review
```
POST /api/v1/daily-reviews
```

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

#### Get Daily Review
```
GET /api/v1/daily-reviews/{review_id}
```

#### Update Daily Review
```
PUT /api/v1/daily-reviews/{review_id}
```

#### Delete Daily Review
```
DELETE /api/v1/daily-reviews/{review_id}
```

### Field Descriptions

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| review_date | date | Yes | ISO date | Date of the review |
| mood_rating | integer | No | 1-10 | Mood rating for the day |
| energy_level | integer | No | 1-10 | Energy level rating |
| productivity_rating | integer | No | 1-10 | Productivity rating |
| sleep_hours | decimal | No | 0-24 | Hours of sleep |
| sleep_quality | integer | No | 1-10 | Sleep quality rating |
| water_intake_ml | integer | No | ≥0 | Water intake in milliliters |
| screen_time_minutes | integer | No | ≥0 | Screen time in minutes |
| steps | integer | No | ≥0 | Number of steps walked |
| accomplishments | text | No | - | Daily accomplishments |
| challenges | text | No | - | Challenges faced |
| lessons_learned | text | No | - | Lessons learned |
| gratitude | text | No | - | Things to be grateful for |
| tomorrow_intentions | text | No | - | Intentions for tomorrow |
| highlights | text | No | - | Day's highlights |

### Business Rules

- Only one daily review per user per date
- All ratings must be between 1 and 10
- Sleep hours must be between 0 and 24
- All numeric health metrics must be non-negative

## Blog Entries API

### Overview
The Blog Entries API enables users to create, manage, and share blog posts. Posts can be manually created or auto-generated from daily reviews.

### Endpoints

#### List Blog Entries
```
GET /api/v1/blog-entries
```

**Query Parameters:**
- `status_filter` (optional): 'draft', 'published', or 'archived'
- `page` (optional): Page number (default: 1)
- `limit` (optional): Results per page (default: 20, max: 100)

**Response:** Paginated list of blog entries

#### Create Blog Entry
```
POST /api/v1/blog-entries
```

**Request Body:**
```json
{
  "title": "My Journey with Manifestation",
  "content": "Today I learned about the power of visualization...",
  "excerpt": "A brief summary",
  "status": "draft",
  "is_public": false,
  "is_featured": false
}
```

#### Generate Blog from Review
```
POST /api/v1/blog-entries/generate-from-review/{review_id}
```

**Description:** Automatically generates a blog entry from a daily review using a template-based approach.

**Generated Content Structure:**
- Title: "Daily Reflection: {date}"
- Sections:
  - How I Felt Today (mood, energy, productivity)
  - Today's Metrics (steps, screen time)
  - Accomplishments
  - Challenges Faced
  - Gratitude
  - Lessons Learned
  - Intentions for Tomorrow
  - Highlights

#### Get Blog Entry
```
GET /api/v1/blog-entries/{entry_id}
```

#### Update Blog Entry
```
PUT /api/v1/blog-entries/{entry_id}
```

#### Delete Blog Entry
```
DELETE /api/v1/blog-entries/{entry_id}
```

### Field Descriptions

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| title | string | Yes | ≤500 chars | Blog post title |
| content | text | Yes | - | Main blog content |
| excerpt | text | No | - | Brief summary/preview |
| slug | string | Auto | - | URL-friendly title |
| status | enum | No | draft/published/archived | Publication status |
| is_public | boolean | No | - | Public visibility |
| is_featured | boolean | No | - | Featured status |
| view_count | integer | Auto | - | Number of views |
| published_at | datetime | Auto | - | Publication timestamp |

### Business Rules

- Slug is auto-generated from title
- When status changes to 'published', published_at is set automatically
- Draft posts are private by default
- View count is automatically tracked

## Integration Features

### Daily Review to Blog Generation

The auto-generation feature creates a structured blog post from daily review data:

1. **User selects a daily review** from the review selection UI
2. **System generates content** by transforming review fields into markdown sections
3. **Blog entry created** as a draft with:
   - Title based on review date
   - Content organized into sections
   - Excerpt from highlights or accomplishments
   - Default privacy settings (private draft)

### Progress Tracking Integration

Daily reviews feed into progress tracking:
- Mood and energy trends over time
- Activity metrics (steps, screen time)
- Sleep pattern analysis
- Productivity insights

## Security & Privacy

### Access Control
- Users can only access their own daily reviews and blog entries
- JWT authentication required for all endpoints
- User ID automatically extracted from JWT token

### Privacy Controls
- Blog entries support public/private visibility
- Draft status keeps entries private
- Archived status removes from active listings
- Daily reviews are always private to the user

## Usage Examples

### Creating a Daily Review with New Fields

```bash
curl -X POST http://localhost:8000/api/v1/daily-reviews \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "review_date": "2025-11-15",
    "mood_rating": 8,
    "screen_time_minutes": 420,
    "steps": 12500,
    "accomplishments": "Completed feature implementation"
  }'
```

### Generating Blog from Review

```bash
curl -X POST http://localhost:8000/api/v1/blog-entries/generate-from-review/{review_id} \
  -H "Authorization: Bearer {token}"
```

### Publishing a Blog Entry

```bash
curl -X PUT http://localhost:8000/api/v1/blog-entries/{entry_id} \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "published",
    "is_public": true
  }'
```

## Migration Notes

### Database Changes

A new migration adds two fields to the daily_reviews table:
- `screen_time_minutes` (integer, nullable)
- `steps` (integer, nullable)

To apply the migration:
```bash
cd backend
alembic upgrade head
```

## Frontend Integration

### Components
- `DailyReviewForm`: Enhanced with screen time and steps inputs
- `DailyReviewList`: Displays new metrics
- `BlogEntryForm`: Create/edit blog posts
- `BlogEntryList`: Browse blog entries
- `BlogEntryDetail`: View individual posts

### Services
- `dailyReviewService`: API calls for daily reviews
- `blogEntryService`: API calls for blog entries including generation

### Types
- Updated `DailyReview` interface with new fields
- New `BlogEntry` interface for blog posts
