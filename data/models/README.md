# Data Models Structure

The data models have been reorganized into a modular structure for better maintainability and separation of concerns.

## File Organization

```
data/models/
├── __init__.py          # Package initialization with all exports
├── user.py              # User-related models (User, UserCreate, UserUpdate, UserRole, etc.)
├── item.py              # Item-related models (Item, ItemCreate, ItemUpdate, ItemStatus, etc.)
├── client_app.py        # Client application models (ClientApp, ClientAppCreate, etc.)
├── api.py               # API token models (APIToken, APITokenCreate)
└── common.py            # Common response models (MessageResponse, ErrorResponse, APIResponse)
```

## Benefits

1. **Separation of Concerns**: Each entity has its own file with related models
2. **Better Maintainability**: Easier to find and modify specific model types
3. **Cleaner Imports**: The `__init__.py` provides a clean public API
4. **Scalability**: Easy to add new model types without cluttering a single file

## Usage

The import statements remain the same due to the `__init__.py` file:

```python
from data.models import User, UserCreate, Item, ItemCreate, ClientApp, APIToken
```

Or you can import specific modules if needed:

```python
from data.models.user import User, UserRole
from data.models.item import Item, ItemStatus
from data.models.client_app import ClientApp
```

## Models by Category

### User Models (user.py)
- `UserRole` (enum)
- `UserBase`
- `UserCreate`
- `UserUpdate` 
- `User`
- `UserListResponse`

### Item Models (item.py)
- `ItemStatus` (enum)
- `ItemBase`
- `ItemCreate`
- `ItemUpdate`
- `Item`
- `ItemListResponse`

### Client App Models (client_app.py)
- `ClientAppBase`
- `ClientAppCreate`
- `ClientAppUpdate`
- `ClientApp`
- `ClientAppResponse`
- `ClientAppWithSecret`

### API Models (api.py)
- `APITokenCreate`
- `APIToken`

### Common Models (common.py)
- `MessageResponse`
- `ErrorResponse`
- `APIResponse`
