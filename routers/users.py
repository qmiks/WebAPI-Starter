"""
User Router
This module contains all user-related API endpoints.
Supports both session-based and API token authentication.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status, Request
from typing import List, Optional, Union
from data.models import User, UserCreate, UserUpdate, UserListResponse, MessageResponse
from data.database import get_db, user_crud
from api_auth import get_current_api_client
from utils.localized_errors import (
    get_request_locale, 
    raise_user_not_found, 
    LocalizedBadRequest,
    create_success_response,
    create_error_response
)
from utils.i18n import t

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=UserListResponse)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of users to return"),
    client_info = Depends(get_current_api_client),
    db=Depends(get_db)
):
    """
    Get all users with pagination.
    
    **Requires Authentication**: Bearer token required
    
    - **skip**: Number of users to skip (for pagination) 
    - **limit**: Maximum number of users to return
    """
    users = user_crud.get_users(skip=skip, limit=limit)
    total = len(user_crud.get_users())
    
    return UserListResponse(
        users=users,
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        size=len(users)
    )

@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int, 
    request: Request,
    client_info = Depends(get_current_api_client),
    db=Depends(get_db)
):
    """
    Get a specific user by ID.
    
    **Requires Authentication**: Bearer token required
    
    - **user_id**: The ID of the user to retrieve
    """
    user = user_crud.get_user(user_id)
    if not user:
        raise_user_not_found(request)
    return user

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, 
    request: Request,
    client_info = Depends(get_current_api_client),
    db=Depends(get_db)
):
    """
    Create a new user.
    
    **Requires Authentication**: Bearer token required
    
    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address  
    - **password**: Password (minimum 8 characters)
    - **full_name**: Optional full name
    - **role**: User role (admin, user)
    """
    locale = get_request_locale(request)
    
    # Check if username already exists
    existing_user = user_crud.get_user_by_username(user.username)
    if existing_user:
        raise LocalizedBadRequest(
            "users.username_already_exists", 
            locale,
            username=user.username
        )
    
    # Check if email already exists
    existing_email = user_crud.get_user_by_email(user.email)
    if existing_email:
        raise LocalizedBadRequest(
            "users.email_already_exists", 
            locale,
            email=user.email
        )
    
    new_user = user_crud.create_user(user)
    return new_user
    
    new_user = user_crud.create_user(user)
    return new_user

@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    client_info = Depends(get_current_api_client),
    db=Depends(get_db)
):
    """
    Update an existing user.
    
    **Requires Authentication**: Bearer token required
    
    - **user_id**: The ID of the user to update
    - **user_update**: Fields to update (only provided fields will be updated)
    """
    # Check if user exists
    existing_user = user_crud.get_user(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Check if username is being updated and already exists
    if user_update.username:
        username_user = user_crud.get_user_by_username(user_update.username)
        if username_user and username_user["id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Check if email is being updated and already exists
    if user_update.email:
        email_user = user_crud.get_user_by_email(user_update.email)
        if email_user and email_user["id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )
    
    updated_user = user_crud.update_user(user_id, user_update)
    return updated_user

@router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: int, 
    client_info = Depends(get_current_api_client),
    db=Depends(get_db)
):
    """
    Delete a user.
    
    **Requires Authentication**: Bearer token required
    
    - **user_id**: The ID of the user to delete
    """
    # Check if user exists
    existing_user = user_crud.get_user(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    success = user_crud.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )
    
    return MessageResponse(message=f"User with id {user_id} has been deleted successfully")
