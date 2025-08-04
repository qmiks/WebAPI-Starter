"""
Authentication and authorization utilities for the WebAPI Starter application.
"""

from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse
import secrets

# Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mock user database with admin user
USERS_DB = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": pwd_context.hash("admin123"),  # Default password: admin123
        "role": "admin",
        "is_active": True,
        "full_name": "Administrator"
    },
    "user": {
        "username": "user",
        "email": "user@example.com", 
        "hashed_password": pwd_context.hash("user123"),  # Default password: user123
        "role": "user",
        "is_active": True,
        "full_name": "Regular User"
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def get_user(username: str) -> Optional[dict]:
    """Get user from database. Check database first, then USERS_DB for demo accounts."""
    # First check the actual database
    from data.database import user_crud
    users = user_crud.get_users()
    for user in users:
        if user["username"] == username:
            return user
    
    # Fallback to check the mock USERS_DB for demo accounts
    if username in USERS_DB:
        return USERS_DB[username]
    
    return None

def authenticate_user(username: str, password: str) -> Union[dict, bool]:
    """Authenticate a user with username and password."""
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return {"username": username}
    except JWTError:
        return None

def get_current_user_from_session(request: Request) -> Optional[dict]:
    """Get current user from session cookie."""
    session_token = request.cookies.get("session_token")
    if not session_token:
        return None
    
    token_data = verify_token(session_token)
    if token_data is None:
        return None
    
    user = get_user(token_data["username"])
    return user

def require_login(request: Request) -> dict:
    """Dependency that requires any authenticated user."""
    current_user = get_current_user_from_session(request)
    
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    return current_user

# Session storage (in production, use Redis or database)
active_sessions = {}

def create_session(user: dict) -> str:
    """Create a new session for a user."""
    session_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    active_sessions[session_token] = {
        "user": user,
        "created_at": datetime.utcnow()
    }
    return session_token

def invalidate_session(session_token: str):
    """Invalidate a session."""
    if session_token in active_sessions:
        del active_sessions[session_token]
