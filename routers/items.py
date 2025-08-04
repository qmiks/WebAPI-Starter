"""
Item Router
This module contains all item-related API endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
from data.models import Item, ItemCreate, ItemUpdate, ItemListResponse, MessageResponse, ItemStatus
from data.database import get_db, item_crud, user_crud

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=ItemListResponse)
async def get_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"),
    owner_id: Optional[int] = Query(None, description="Filter items by owner ID"),
    status: Optional[ItemStatus] = Query(None, description="Filter items by status"),
    db=Depends(get_db)
):
    """
    Get all items with pagination and optional filtering.
    
    - **skip**: Number of items to skip (for pagination)
    - **limit**: Maximum number of items to return
    - **owner_id**: Filter items by owner ID
    - **status**: Filter items by status (active, inactive, draft)
    """
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
async def get_item(item_id: int, db=Depends(get_db)):
    """
    Get a specific item by ID.
    
    - **item_id**: The ID of the item to retrieve
    """
    item = item_crud.get_item_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return item

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, db=Depends(get_db)):
    """
    Create a new item.
    
    - **name**: Item name (1-100 characters)
    - **description**: Optional item description
    - **price**: Item price (must be greater than 0)
    - **status**: Item status (active, inactive, draft)
    - **owner_id**: ID of the user who owns this item
    """
    # Check if owner exists
    owner = user_crud.get_user_by_id(item.owner_id)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Owner with id {item.owner_id} not found"
        )
    
    new_item = item_crud.create_item(item)
    return new_item

@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemUpdate, db=Depends(get_db)):
    """
    Update an existing item.
    
    - **item_id**: The ID of the item to update
    - **item_update**: Fields to update (only provided fields will be updated)
    """
    # Check if item exists
    existing_item = item_crud.get_item_by_id(item_id)
    if not existing_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    updated_item = item_crud.update_item(item_id, item_update)
    return updated_item

@router.delete("/{item_id}", response_model=MessageResponse)
async def delete_item(item_id: int, db=Depends(get_db)):
    """
    Delete an item.
    
    - **item_id**: The ID of the item to delete
    """
    # Check if item exists
    existing_item = item_crud.get_item_by_id(item_id)
    if not existing_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    success = item_crud.delete_item(item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item"
        )
    
    return MessageResponse(message=f"Item with id {item_id} has been deleted successfully")
