"""
Common Models
Common response models and utilities used across the WebAPI Starter application.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    success: bool = False


class APIResponse(BaseModel):
    """Generic API response wrapper"""
    data: Optional[dict] = None
    message: str
    success: bool
    timestamp: datetime = Field(default_factory=datetime.now)
