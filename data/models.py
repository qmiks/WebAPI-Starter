"""
Pydantic Models for Data Validation
This file contains all the data models used in the WebAPI Starter application.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class ItemStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT = "draft"

# Base Models
class UserBase(BaseModel):
    """Base user model with common fields"""
    username: str = Field(..., min_length=3, max_length=50, description="Username must be 3-50 characters")
    email: str = Field(..., description="Valid email address")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name of the user")
    role: UserRole = Field(default=UserRole.USER, description="User role")
    is_active: bool = Field(default=True, description="Whether the user is active")

class UserCreate(UserBase):
    """Model for creating a new user"""
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

class UserUpdate(BaseModel):
    """Model for updating user information"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = None
    full_name: Optional[str] = Field(None, max_length=100)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, description="New password (optional)")

class User(UserBase):
    """Complete user model with ID and timestamps"""
    id: int = Field(..., description="Unique user identifier")
    created_at: datetime = Field(..., description="When the user was created")
    updated_at: Optional[datetime] = Field(None, description="When the user was last updated")

    class Config:
        from_attributes = True

# Item Models
class ItemBase(BaseModel):
    """Base item model with common fields"""
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price must be greater than 0")
    status: ItemStatus = Field(default=ItemStatus.ACTIVE, description="Item status")
    owner_id: int = Field(..., description="ID of the user who owns this item")

class ItemCreate(ItemBase):
    """Model for creating a new item"""
    pass

class ItemUpdate(BaseModel):
    """Model for updating item information"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[ItemStatus] = None
    owner_id: Optional[int] = None

class Item(ItemBase):
    """Complete item model with ID and timestamps"""
    id: int = Field(..., description="Unique item identifier")
    created_at: datetime = Field(..., description="When the item was created")
    updated_at: Optional[datetime] = Field(None, description="When the item was last updated")

    class Config:
        from_attributes = True

# Response Models
class UserListResponse(BaseModel):
    """Response model for user list"""
    users: List[User]
    total: int
    page: int
    size: int

class ItemListResponse(BaseModel):
    """Response model for item list"""
    items: List[Item]
    total: int
    page: int
    size: int

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    success: bool = False

# Client App Models
class ClientAppBase(BaseModel):
    """Base client app model with common fields"""
    name: str = Field(..., min_length=3, max_length=100, description="Client application name")
    description: Optional[str] = Field(None, max_length=500, description="Client application description")
    is_active: bool = Field(default=True, description="Whether the client app is active")

class ClientAppCreate(ClientAppBase):
    """Model for creating a new client app"""
    pass

class ClientAppUpdate(BaseModel):
    """Model for updating client app information"""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

class ClientApp(ClientAppBase):
    """Complete client app model with ID, credentials and timestamps"""
    id: int = Field(..., description="Unique client app identifier")
    app_id: str = Field(..., description="Client application ID")
    app_secret: str = Field(..., description="Client application secret")
    created_at: datetime = Field(..., description="When the client app was created")
    updated_at: Optional[datetime] = Field(None, description="When the client app was last updated")

    class Config:
        from_attributes = True

class ClientAppResponse(BaseModel):
    """Client app response model (without secret)"""
    id: int
    name: str
    description: Optional[str]
    app_id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

class ClientAppWithSecret(ClientApp):
    """Client app model including secret (for creation response only)"""
    pass

# API Token Models
class APITokenCreate(BaseModel):
    """Model for creating an API token"""
    app_id: str = Field(..., description="Client application ID")
    app_secret: str = Field(..., description="Client application secret")
    expires_in: Optional[int] = Field(default=3600, description="Token expiration time in seconds")

class APIToken(BaseModel):
    """API token response model"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")

# API Response Models
class APIResponse(BaseModel):
    """Generic API response wrapper"""
    data: Optional[dict] = None
    message: str
    success: bool
    timestamp: datetime = Field(default_factory=datetime.now)
