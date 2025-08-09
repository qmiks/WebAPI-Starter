"""
API Token Models
Pydantic models for API token management in the WebAPI Starter application.
"""

from pydantic import BaseModel, Field
from typing import Optional


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
