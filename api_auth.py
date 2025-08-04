"""
API Authentication Module
Handles JWT token generation and validation for client applications.
"""

import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from data.database import client_app_crud

# JWT Configuration
SECRET_KEY = "your-secret-key-change-this-in-production-super-secret-api-key-for-client-apps-12345"
ALGORITHM = "HS256"

# Security scheme for API token authentication
api_security = HTTPBearer(description="Enter your JWT Bearer token here")

def create_api_token(app_id: str, app_secret: str, expires_in: int = 3600) -> Dict[str, Any]:
    """
    Create JWT token for client application
    
    Args:
        app_id: Client application ID
        app_secret: Client application secret
        expires_in: Token expiration time in seconds
    
    Returns:
        Dictionary containing access token and metadata
    
    Raises:
        HTTPException: If credentials are invalid
    """
    # Verify app credentials
    client_app = client_app_crud.get_client_app_by_app_id(app_id)
    
    if not client_app:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client credentials"
        )
    
    if not client_app["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Client application is disabled"
        )
    
    if client_app["app_secret"] != app_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client credentials"
        )
    
    # Create token payload
    expire = datetime.utcnow() + timedelta(seconds=expires_in)
    payload = {
        "app_id": app_id,
        "app_name": client_app["name"],
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "api_token"
    }
    
    # Generate JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": expires_in,
        "expires_at": expire.isoformat()
    }

def verify_api_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode JWT API token
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded token payload
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Validate token format first
        if not token or not isinstance(token, str) or token.count('.') != 2:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format"
            )
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check token type
        if payload.get("type") != "api_token":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # Verify app still exists and is active
        app_id = payload.get("app_id")
        if not app_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        client_app = client_app_crud.get_client_app_by_app_id(app_id)
        if not client_app or not client_app["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Client application not found or disabled"
            )
        
        return payload
        
    except HTTPException:
        # Re-raise HTTP exceptions (properly formatted errors)
        raise
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature"
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token encoding"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        # Catch any other exceptions
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation failed"
        )

async def get_current_api_client(credentials: HTTPAuthorizationCredentials = Depends(api_security)) -> Dict[str, Any]:
    """
    FastAPI dependency to get current API client from token
    
    Args:
        credentials: HTTP Authorization credentials
    
    Returns:
        Current client app information
    
    Raises:
        HTTPException: If authentication fails
    """
    try:
        token = credentials.credentials
        payload = verify_api_token(token)
        
        # Get full client app details
        client_app = client_app_crud.get_client_app_by_app_id(payload["app_id"])
        if not client_app:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Client application not found"
            )
        
        return {
            "app_id": payload["app_id"],
            "app_name": payload["app_name"],
            "client_app": client_app,
            "token_payload": payload
        }
    except HTTPException:
        # Re-raise HTTP exceptions (these are properly formatted errors)
        raise
    except Exception as e:
        # Catch any other exceptions and convert to proper HTTP error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
