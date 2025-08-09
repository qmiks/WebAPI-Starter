"""
Client Application Models
Pydantic models for client application management in the WebAPI Starter application.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


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
