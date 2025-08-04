"""
Data Layer Package
This package contains all data access related modules for the WebAPI Starter application.
"""

# Import main classes for easy access
from .models import (
    User, UserCreate, UserUpdate, UserBase,
    Item, ItemCreate, ItemUpdate, ItemBase,
    ClientApp, ClientAppCreate, ClientAppUpdate, ClientAppBase,
    UserRole, ItemStatus,
    APIToken, APITokenCreate,
    UserListResponse, ItemListResponse,
    MessageResponse, ErrorResponse, APIResponse
)

from .database import (
    get_db, init_sample_data, init_database, initialize_sqlite_database,
    user_crud, item_crud, client_app_crud
)

__all__ = [
    # Models
    "User", "UserCreate", "UserUpdate", "UserBase",
    "Item", "ItemCreate", "ItemUpdate", "ItemBase", 
    "ClientApp", "ClientAppCreate", "ClientAppUpdate", "ClientAppBase",
    "UserRole", "ItemStatus",
    "APIToken", "APITokenCreate",
    "UserListResponse", "ItemListResponse",
    "MessageResponse", "ErrorResponse", "APIResponse",
    
    # Database
    "get_db", "init_sample_data", "init_database", "initialize_sqlite_database",
    "user_crud", "item_crud", "client_app_crud"
]
