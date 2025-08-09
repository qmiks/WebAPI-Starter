"""
Item Models
Pydantic models for item-related operations in the WebAPI Starter application.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ItemStatus(str, Enum):
    """Item status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT = "draft"


class ItemBase(BaseModel):
    """Base item model with common fields"""
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price must be greater than 0")
    status: ItemStatus = Field(default=ItemStatus.ACTIVE, description="Item status")
    owner_id: Optional[int] = Field(None, description="ID of the user who owns this item (auto-assigned for regular users)")


class ItemCreate(BaseModel):
    """Model for creating a new item (owner_id is auto-assigned)"""
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price must be greater than 0")
    status: ItemStatus = Field(default=ItemStatus.ACTIVE, description="Item status")
    owner_id: Optional[int] = Field(None, description="Owner ID (only admins can set this, auto-assigned for regular users)")


class ItemUpdate(BaseModel):
    """Model for updating item information"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[ItemStatus] = None
    owner_id: Optional[int] = Field(None, description="Owner ID (only admins can change this)")


class Item(ItemBase):
    """Complete item model with ID and timestamps"""
    id: int = Field(..., description="Unique item identifier")
    owner_id: int = Field(..., description="ID of the user who owns this item")  # Required in response
    created_at: datetime = Field(..., description="When the item was created")
    updated_at: Optional[datetime] = Field(None, description="When the item was last updated")

    class Config:
        from_attributes = True


class ItemListResponse(BaseModel):
    """Response model for item list"""
    items: List[Item]
    total: int
    page: int
    size: int
