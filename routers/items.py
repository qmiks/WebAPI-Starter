"""
Item Router
This module contains all item-related API endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status, Request
from typing import List, Optional
from data.models import Item, ItemCreate, ItemUpdate, ItemListResponse, MessageResponse, ItemStatus
from data.database import get_db, item_crud, user_crud
from auth import require_login, get_current_user_from_session

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=ItemListResponse)
async def get_items(
    request: Request,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"),
    status: Optional[ItemStatus] = Query(None, description="Filter items by status"),
    db=Depends(get_db)
):
    """
    Get items with pagination and optional filtering.
    Regular users can only see their own items.
    Admins can see all items.
    
    - **skip**: Number of items to skip (for pagination)
    - **limit**: Maximum number of items to return
    - **status**: Filter items by status (active, inactive, draft)
    """
    # Get current user from session
    current_user = get_current_user_from_session(request)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # Determine owner_id based on user role
    owner_id = None
    if current_user.get("role") != "admin":
        # Regular users can only see their own items
        owner_id = current_user.get("id")
        if not owner_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID not found"
            )
    
    items = item_crud.get_items(skip=skip, limit=limit, owner_id=owner_id)
    
    # Filter by status if provided
    if status:
        items = [item for item in items if item["status"] == status]
    
    total = len(item_crud.get_items(owner_id=owner_id))
    if status:
        all_items = item_crud.get_items(owner_id=owner_id)
        total = len([item for item in all_items if item["status"] == status])
    
    return ItemListResponse(
        items=items,
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        size=len(items)
    )

@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int, request: Request, db=Depends(get_db)):
    """
    Get a specific item by ID.
    Regular users can only access their own items.
    Admins can access any item.
    
    - **item_id**: The ID of the item to retrieve
    """
    # Get current user from session
    current_user = get_current_user_from_session(request)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    item = item_crud.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    # Check ownership for non-admin users
    if current_user.get("role") != "admin" and item["owner_id"] != current_user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own items"
        )
    
    return item

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, request: Request, db=Depends(get_db)):
    """
    Create a new item.
    The item will be automatically assigned to the current user.
    
    - **name**: Item name (1-100 characters)
    - **description**: Optional item description
    - **price**: Item price (must be greater than 0)
    - **status**: Item status (active, inactive, draft)
    """
    # Get current user from session
    current_user = get_current_user_from_session(request)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # For regular users, automatically set owner to current user
    # For admins, allow setting owner_id if provided, otherwise default to current user
    owner_id = current_user.get("id")
    
    if current_user.get("role") == "admin" and hasattr(item, 'owner_id') and item.owner_id:
        # Admin can specify owner_id
        owner_id = item.owner_id
        # Check if specified owner exists
        owner = user_crud.get_user(owner_id)
        if not owner:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Owner with id {owner_id} not found"
            )
    
    # Create item data without owner_id in the model
    item_data = ItemCreate(
        name=item.name,
        description=item.description,
        price=item.price,
        status=item.status,
        owner_id=owner_id
    )
    
    new_item = item_crud.create_item(item_data, owner_id)
    return new_item

@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemUpdate, request: Request, db=Depends(get_db)):
    """
    Update an existing item.
    Regular users can only update their own items.
    Admins can update any item.
    
    - **item_id**: The ID of the item to update
    - **item_update**: Fields to update (only provided fields will be updated)
    """
    # Get current user from session
    current_user = get_current_user_from_session(request)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # Check if item exists
    existing_item = item_crud.get_item(item_id)
    if not existing_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    # Check ownership for non-admin users
    if current_user.get("role") != "admin" and existing_item["owner_id"] != current_user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own items"
        )
    
    # Prevent regular users from changing owner_id
    if current_user.get("role") != "admin" and item_update.owner_id is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot change the owner of an item"
        )
    
    updated_item = item_crud.update_item(item_id, item_update)
    return updated_item

@router.delete("/{item_id}", response_model=MessageResponse)
async def delete_item(item_id: int, request: Request, db=Depends(get_db)):
    """
    Delete an item.
    Regular users can only delete their own items.
    Admins can delete any item.
    
    - **item_id**: The ID of the item to delete
    """
    # Get current user from session
    current_user = get_current_user_from_session(request)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # Check if item exists
    existing_item = item_crud.get_item(item_id)
    if not existing_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    # Check ownership for non-admin users
    if current_user.get("role") != "admin" and existing_item["owner_id"] != current_user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own items"
        )
    
    success = item_crud.delete_item(item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item"
        )
    
    return MessageResponse(message=f"Item with id {item_id} has been deleted successfully")
