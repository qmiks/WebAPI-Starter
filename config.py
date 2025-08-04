"""
Configuration Module
This module contains configuration settings for the WebAPI Starter application.
"""

import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "WebAPI Starter"
    API_DESCRIPTION: str = "A comprehensive WebAPI Starter application with CRUD operations"
    API_VERSION: str = "1.0.0"
    
    # Server Settings
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    
    # Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Settings (for future use)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # CORS Settings
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]
    
    # Pagination Settings
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

# Create settings instance
settings = Settings()
