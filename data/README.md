# Data Layer Documentation

This directory contains all data access and model definitions for the WebAPI Starter application.

## 📁 Directory Structure

```
data/
├── __init__.py      # Package initialization with convenient imports
├── models.py        # Pydantic models and data validation schemas
└── database.py      # Database operations, CRUD classes, and mock storage
```

## 📋 File Descriptions

### `models.py`
Contains all Pydantic models for data validation and serialization:

#### **Core Models**
- **User Models**: `User`, `UserCreate`, `UserUpdate`, `UserBase`
- **Item Models**: `Item`, `ItemCreate`, `ItemUpdate`, `ItemBase`
- **Client App Models**: `ClientApp`, `ClientAppCreate`, `ClientAppUpdate`

#### **Enums**
- **UserRole**: `ADMIN`, `USER`, `MODERATOR`
- **ItemStatus**: `ACTIVE`, `INACTIVE`, `DRAFT`

#### **Response Models**
- **List Responses**: `UserListResponse`, `ItemListResponse`
- **Generic Responses**: `MessageResponse`, `ErrorResponse`, `APIResponse`
- **API Token Models**: `APIToken`, `APITokenCreate`

### `database.py`
Handles all database operations and provides mock data storage:

#### **Mock Storage**
- **users_db**: List storing user data
- **items_db**: List storing item data  
- **client_apps_db**: List storing client application data

#### **CRUD Classes**
- **UserCRUD**: Complete user management operations
- **ItemCRUD**: Complete item management operations
- **ClientAppCRUD**: Complete client app management operations

#### **Utility Functions**
- **get_db()**: Database dependency for FastAPI
- **init_sample_data()**: Initialize with sample data
- **generate_app_id()**, **generate_app_secret()**: Client app utilities

## 🔧 Usage Examples

### Importing from Data Package

```python
# Import models
from data.models import User, UserCreate, UserRole, ItemStatus

# Import database operations
from data.database import user_crud, item_crud, get_db

# Import everything via package
from data import User, UserCreate, user_crud, get_db
```

### Using CRUD Operations

```python
from data import user_crud, item_crud, UserCreate, ItemCreate

# Create a user
user_data = UserCreate(
    username="newuser",
    email="user@example.com", 
    password="password123",
    full_name="New User"
)
new_user = user_crud.create_user(user_data)

# Get users with pagination
users = user_crud.get_users(skip=0, limit=10)

# Create an item
item_data = ItemCreate(
    name="New Product",
    description="A great product",
    price=99.99,
    owner_id=new_user["id"]
)
new_item = item_crud.create_item(item_data)
```

### Model Validation

```python
from data.models import UserCreate, ValidationError

try:
    # This will validate automatically
    user_data = UserCreate(
        username="u",  # Too short - will raise validation error
        email="invalid-email",  # Invalid format
        password="123"  # Too short
    )
except ValidationError as e:
    print(f"Validation errors: {e}")
```

## 🏗️ Database Architecture

### Current Implementation
- **Mock Database**: In-memory lists for development and testing
- **No Persistence**: Data resets on application restart
- **Sample Data**: Automatically populated on startup

### Migration Path
The current structure is designed to easily migrate to a real database:

```python
# Current (Mock)
from data.database import user_crud, get_db

# Future (Real Database) 
from data.database import user_crud, get_db  # Same interface!
```

## 📊 Data Relationships

```
User (1) ──── (many) Item
  │
  └── has role (admin/user/moderator)

ClientApp ──── generates ──── APIToken
  │
  └── has credentials (app_id, app_secret)
```

## 🔐 Security Considerations

### Password Security
- Passwords are hashed using bcrypt
- Plain text passwords never stored
- Password validation enforced (min 8 characters)

### API Security
- Client apps have unique app_id and app_secret
- Secrets are generated cryptographically
- JWT tokens for API authentication

## 📈 Scalability

### Current Limitations
- In-memory storage (not persistent)
- No indexing or query optimization
- Single-threaded access

### Future Improvements
- Replace with SQLAlchemy + PostgreSQL/MySQL
- Add database migrations
- Implement connection pooling
- Add caching layer (Redis)

## 🧪 Testing

### Unit Tests
```python
from data.models import UserCreate
from data.database import user_crud

def test_user_creation():
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    user = user_crud.create_user(user_data)
    assert user["username"] == "testuser"
    assert "hashed_password" in user
```

### Integration Tests
```python
from fastapi.testclient import TestClient
from main import app
from data import get_db

client = TestClient(app)

def test_user_api():
    response = client.post("/api/v1/users/", json={
        "username": "apiuser",
        "email": "api@example.com", 
        "password": "password123"
    })
    assert response.status_code == 201
```

## 📝 Best Practices

### Model Design
1. **Use descriptive field names**
2. **Add proper validation constraints**
3. **Include helpful descriptions**
4. **Separate create/update models**

### CRUD Operations
1. **Handle errors gracefully**
2. **Return consistent data structures**
3. **Use type hints**
4. **Implement proper pagination**

### Database Access
1. **Use dependency injection** (`Depends(get_db)`)
2. **Keep operations atomic**
3. **Handle concurrent access**
4. **Log important operations**

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pydantic Documentation**: https://pydantic-docs.helpmanual.io/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/ (for future migration)

---

*The data layer provides a clean, type-safe interface for all data operations while maintaining flexibility for future enhancements and database migrations.*
