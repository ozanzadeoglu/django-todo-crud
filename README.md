# Django Todo CRUD API

A RESTful Todo API built with Django and Django REST Framework, connected to PostgreSQL database.

## Features
- Complete CRUD operations for todos
- PostgreSQL database integration
- Optional pagination support
- RESTful API design

## Tech Stack
- **Backend**: Django 5.2.6, Django REST Framework
- **Database**: PostgreSQL
- **Python**: 3.12


```

## API Endpoints

Base URL: `http://127.0.0.1:8000/api/`

### Todo Operations

#### 1. List All Todos
```http
GET /api/todos/
```
**Response:**
```json
{
    "results": [
        {
            "title": "Example todo",
            "description": "Todo description"
        }
    ]
}
```

#### 2. List Todos with Pagination
```http
GET /api/todos/?page=1&page_size=5
```
**Response:**
```json
{
    "page": 1,
    "page_size": 5,
    "total_pages": 3,
    "results": [...]
}
```

#### 3. Create New Todo
```http
POST /api/todos/
Content-Type: application/json

{
    "title": "New todo",
    "description": "Todo description",
    "completed": false
}
```

#### 4. Get Specific Todo
```http
GET /api/todos/{id}/
```

#### 5. Update Todo (Full Update)
```http
PUT /api/todos/{id}/
Content-Type: application/json

{
    "title": "Updated title",
    "description": "Updated description",
    "completed": true
}
```

#### 6. Update Todo (Partial Update)
```http
PATCH /api/todos/{id}/
Content-Type: application/json

{
    "completed": true
}
```

#### 7. Delete Todo
```http
DELETE /api/todos/{id}/
```

## Database Schema

### Todo Model
```python
class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
