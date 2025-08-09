"""
Data Models Package
This package contains all the Pydantic models used in the WebAPI Starter application.
Each entity is organized in its own module for better maintainability.
"""

from .user import User, UserBase, UserCreate, UserUpdate, UserRole, UserListResponse
from .item import Item, ItemBase, ItemCreate, ItemUpdate, ItemStatus, ItemListResponse
from .client_app import (
    ClientApp, 
    ClientAppBase, 
    ClientAppCreate, 
    ClientAppUpdate, 
    ClientAppResponse, 
    ClientAppWithSecret
)
from .api import APIToken, APITokenCreate
from .common import MessageResponse, ErrorResponse, APIResponse

__all__ = [
    # User models
    "User", "UserBase", "UserCreate", "UserUpdate", "UserRole", "UserListResponse",
    # Item models
    "Item", "ItemBase", "ItemCreate", "ItemUpdate", "ItemStatus", "ItemListResponse",
    # Client App models
    "ClientApp", "ClientAppBase", "ClientAppCreate", "ClientAppUpdate", 
    "ClientAppResponse", "ClientAppWithSecret",
    # API models
    "APIToken", "APITokenCreate",
    # Common models
    "MessageResponse", "ErrorResponse", "APIResponse"
]
