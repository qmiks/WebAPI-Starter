"""
Admin Router
This module contains all admin-related endpoints for the web interface.
"""

from fastapi import APIRouter, Request, Form, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List, Dict, Any
from data.models import UserCreate, UserUpdate, UserRole, ItemCreate, ItemUpdate, ItemStatus
from data.database import get_db, user_crud, item_crud
from auth import require_admin, get_current_user_from_session

# Initialize templates
templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

def check_admin_auth(request: Request) -> Optional[RedirectResponse]:
    """Check if user is authenticated and has admin role. Return redirect if not."""
    current_user = get_current_user_from_session(request)
    
    if not current_user:
        # Not logged in - redirect to login with current URL as redirect_url
        return RedirectResponse(
            url=f"/auth/login?redirect_url={request.url.path}",
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    if current_user.get("role") != "admin":
        # Not admin - redirect to access denied or home
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return None

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

def get_flash_messages() -> List[Dict[str, str]]:
    """Get flash messages (simplified for demo)"""
    # In a real app, you'd use session storage
    return []

def add_flash_message(message: str, message_type: str = "success"):
    """Add flash message (simplified for demo)"""
    # In a real app, you'd use session storage
    pass

@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db=Depends(get_db)):
    """Admin dashboard with overview statistics - requires admin role"""
    # Check authentication and authorization
    auth_redirect = check_admin_auth(request)
    if auth_redirect:
        return auth_redirect
    
    current_user = get_current_user_from_session(request)
    # Get statistics
    all_users = user_crud.get_users()
    all_items = item_crud.get_items()
    
    total_users = len(all_users)
    active_users = len([user for user in all_users if user["is_active"]])
    total_items = len(all_items)
    active_items = len([item for item in all_items if item["status"] == "active"])
    
    # Get recent users and items (last 5)
    recent_users = sorted(all_users, key=lambda x: x["created_at"], reverse=True)[:5]
    recent_items = sorted(all_items, key=lambda x: x["created_at"], reverse=True)[:5]
    
    # Add owner usernames to items
    user_dict = {user["id"]: user["username"] for user in all_users}
    for item in recent_items:
        item["owner_username"] = user_dict.get(item["owner_id"], "Unknown")
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "current_user": current_user,
        "total_users": total_users,
        "active_users": active_users,
        "total_items": total_items,
        "active_items": active_items,
        "recent_users": recent_users,
        "recent_items": recent_items,
        "messages": get_flash_messages()
    })

@router.get("/users", response_class=HTMLResponse)
async def admin_users_list(request: Request, db=Depends(get_db)):
    """Display all users in a table"""
    # Check authentication and authorization
    auth_redirect = check_admin_auth(request)
    if auth_redirect:
        return auth_redirect
    
    current_user = get_current_user_from_session(request)
    users = user_crud.get_users()
    
    return templates.TemplateResponse("users.html", {
        "request": request,
        "current_user": current_user,
        "users": users,
        "messages": get_flash_messages()
    })

@router.get("/users/new", response_class=HTMLResponse)
async def admin_user_new_form(request: Request):
    """Show form to create a new user"""
    return templates.TemplateResponse("user_form.html", {
        "request": request,
        "user": None,
        "messages": get_flash_messages()
    })

@router.post("/users/new")
async def admin_user_create(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    full_name: Optional[str] = Form(None),
    password: str = Form(...),
    role: UserRole = Form(...),
    is_active: Optional[str] = Form(None),
    db=Depends(get_db)
):
    """Create a new user"""
    try:
        # Check if username already exists
        existing_user = user_crud.get_user_by_username(username)
        if existing_user:
            return templates.TemplateResponse("user_form.html", {
                "request": request,
                "user": None,
                "messages": [{"type": "error", "content": "Username already exists"}]
            })
        
        # Check if email already exists
        existing_email = user_crud.get_user_by_email(email)
        if existing_email:
            return templates.TemplateResponse("user_form.html", {
                "request": request,
                "user": None,
                "messages": [{"type": "error", "content": "Email already exists"}]
            })
        
        # Create user
        user_data = UserCreate(
            username=username,
            email=email,
            full_name=full_name if full_name else None,
            password=password,
            role=role,
            is_active=is_active == "true"
        )
        
        new_user = user_crud.create_user(user_data)
        add_flash_message(f"User '{username}' created successfully!")
        
        return RedirectResponse(url="/admin/users", status_code=303)
        
    except Exception as e:
        return templates.TemplateResponse("user_form.html", {
            "request": request,
            "user": None,
            "messages": [{"type": "error", "content": f"Error creating user: {str(e)}"}]
        })

@router.get("/users/{user_id}", response_class=HTMLResponse)
async def admin_user_detail(request: Request, user_id: int, db=Depends(get_db)):
    """Show user details"""
    user = user_crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's items
    user_items = item_crud.get_items(owner_id=user_id)
    
    return templates.TemplateResponse("user_detail.html", {
        "request": request,
        "user": user,
        "user_items": user_items,
        "messages": get_flash_messages()
    })

@router.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def admin_user_edit_form(request: Request, user_id: int, db=Depends(get_db)):
    """Show form to edit a user"""
    user = user_crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return templates.TemplateResponse("user_form.html", {
        "request": request,
        "user": user,
        "messages": get_flash_messages()
    })

@router.post("/users/{user_id}/edit")
async def admin_user_update(
    request: Request,
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    full_name: Optional[str] = Form(None),
    role: UserRole = Form(...),
    is_active: Optional[str] = Form(None),
    db=Depends(get_db)
):
    """Update an existing user"""
    try:
        user = user_crud.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if username is being changed and already exists
        if username != user["username"]:
            existing_user = user_crud.get_user_by_username(username)
            if existing_user:
                return templates.TemplateResponse("user_form.html", {
                    "request": request,
                    "user": user,
                    "messages": [{"type": "error", "content": "Username already exists"}]
                })
        
        # Check if email is being changed and already exists
        if email != user["email"]:
            existing_email = user_crud.get_user_by_email(email)
            if existing_email:
                return templates.TemplateResponse("user_form.html", {
                    "request": request,
                    "user": user,
                    "messages": [{"type": "error", "content": "Email already exists"}]
                })
        
        # Update user
        user_data = UserUpdate(
            username=username,
            email=email,
            full_name=full_name if full_name else None,
            role=role,
            is_active=is_active == "true"
        )
        
        updated_user = user_crud.update_user(user_id, user_data)
        add_flash_message(f"User '{username}' updated successfully!")
        
        return RedirectResponse(url=f"/admin/users/{user_id}", status_code=303)
        
    except Exception as e:
        return templates.TemplateResponse("user_form.html", {
            "request": request,
            "user": user,
            "messages": [{"type": "error", "content": f"Error updating user: {str(e)}"}]
        })

@router.post("/users/{user_id}/delete")
async def admin_user_delete(user_id: int, db=Depends(get_db)):
    """Delete a user and all their items"""
    user = user_crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        # Delete user's items first
        user_items = item_crud.get_items(owner_id=user_id)
        for item in user_items:
            item_crud.delete_item(item["id"])
        
        # Delete user
        success = user_crud.delete_user(user_id)
        if success:
            add_flash_message(f"User '{user['username']}' and {len(user_items)} items deleted successfully!")
        else:
            add_flash_message("Failed to delete user", "error")
        
    except Exception as e:
        add_flash_message(f"Error deleting user: {str(e)}", "error")
    
    return RedirectResponse(url="/admin/users", status_code=303)

@router.post("/users/{user_id}/activate")
async def admin_user_activate(user_id: int, db=Depends(get_db)):
    """Activate a user"""
    user = user_crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        user_data = UserUpdate(is_active=True)
        user_crud.update_user(user_id, user_data)
        add_flash_message(f"User '{user['username']}' activated successfully!")
    except Exception as e:
        add_flash_message(f"Error activating user: {str(e)}", "error")
    
    # Redirect back to the referring page
    return RedirectResponse(url=f"/admin/users/{user_id}", status_code=303)

@router.post("/users/{user_id}/deactivate")
async def admin_user_deactivate(user_id: int, db=Depends(get_db)):
    """Deactivate a user"""
    user = user_crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        user_data = UserUpdate(is_active=False)
        user_crud.update_user(user_id, user_data)
        add_flash_message(f"User '{user['username']}' deactivated successfully!")
    except Exception as e:
        add_flash_message(f"Error deactivating user: {str(e)}", "error")
    
    # Redirect back to the referring page
    return RedirectResponse(url=f"/admin/users/{user_id}", status_code=303)

@router.get("/items", response_class=HTMLResponse)
async def admin_items_list(request: Request, db=Depends(get_db)):
    """Display all items in a table"""
    items = item_crud.get_items()
    users = user_crud.get_users()
    
    # Add owner usernames to items
    user_dict = {user["id"]: user["username"] for user in users}
    for item in items:
        item["owner_username"] = user_dict.get(item["owner_id"], "Unknown")
    
    return templates.TemplateResponse("items.html", {
        "request": request,
        "items": items,
        "messages": get_flash_messages()
    })

@router.get("/items/new", response_class=HTMLResponse)
async def admin_item_new_form(request: Request, db=Depends(get_db)):
    """Show form to create a new item"""
    users = user_crud.get_users()
    active_users = [user for user in users if user["is_active"]]
    
    return templates.TemplateResponse("item_form.html", {
        "request": request,
        "item": None,
        "users": active_users,
        "messages": get_flash_messages()
    })

@router.get("/items/{item_id}", response_class=HTMLResponse)
async def admin_item_detail(request: Request, item_id: int, db=Depends(get_db)):
    """Show item details"""
    item = item_crud.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Get owner information
    owner = user_crud.get_user_by_id(item["owner_id"])
    item["owner"] = owner
    
    return templates.TemplateResponse("item_detail.html", {
        "request": request,
        "item": item,
        "messages": get_flash_messages()
    })

@router.post("/items/new")
async def admin_item_create(
    request: Request,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    status: ItemStatus = Form(...),
    owner_id: int = Form(...),
    db=Depends(get_db)
):
    """Create a new item"""
    try:
        # Check if owner exists
        owner = user_crud.get_user_by_id(owner_id)
        if not owner:
            users = user_crud.get_users()
            active_users = [user for user in users if user["is_active"]]
            return templates.TemplateResponse("item_form.html", {
                "request": request,
                "item": None,
                "users": active_users,
                "messages": [{"type": "error", "content": "Selected owner does not exist"}]
            })
        
        # Create item
        item_data = ItemCreate(
            name=name,
            description=description,
            price=price,
            status=status,
            owner_id=owner_id
        )
        
        new_item = item_crud.create_item(item_data)
        add_flash_message(f"Item '{name}' created successfully!")
        
        return RedirectResponse(url="/admin/items", status_code=303)
        
    except Exception as e:
        users = user_crud.get_users()
        active_users = [user for user in users if user["is_active"]]
        return templates.TemplateResponse("item_form.html", {
            "request": request,
            "item": None,
            "users": active_users,
            "messages": [{"type": "error", "content": f"Error creating item: {str(e)}"}]
        })

@router.get("/items/{item_id}/edit", response_class=HTMLResponse)
async def admin_item_edit_form(request: Request, item_id: int, db=Depends(get_db)):
    """Show form to edit an item"""
    item = item_crud.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    users = user_crud.get_users()
    active_users = [user for user in users if user["is_active"]]
    
    return templates.TemplateResponse("item_form.html", {
        "request": request,
        "item": item,
        "users": active_users,
        "messages": get_flash_messages()
    })

@router.post("/items/{item_id}/edit")
async def admin_item_update(
    request: Request,
    item_id: int,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    status: ItemStatus = Form(...),
    owner_id: int = Form(...),
    db=Depends(get_db)
):
    """Update an existing item"""
    try:
        item = item_crud.get_item_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Check if owner exists
        owner = user_crud.get_user_by_id(owner_id)
        if not owner:
            users = user_crud.get_users()
            active_users = [user for user in users if user["is_active"]]
            return templates.TemplateResponse("item_form.html", {
                "request": request,
                "item": item,
                "users": active_users,
                "messages": [{"type": "error", "content": "Selected owner does not exist"}]
            })
        
        # Update item
        item_data = ItemUpdate(
            name=name,
            description=description,
            price=price,
            status=status,
            owner_id=owner_id
        )
        
        updated_item = item_crud.update_item(item_id, item_data)
        add_flash_message(f"Item '{name}' updated successfully!")
        
        return RedirectResponse(url=f"/admin/items/{item_id}", status_code=303)
        
    except Exception as e:
        users = user_crud.get_users()
        active_users = [user for user in users if user["is_active"]]
        return templates.TemplateResponse("item_form.html", {
            "request": request,
            "item": item,
            "users": active_users,
            "messages": [{"type": "error", "content": f"Error updating item: {str(e)}"}]
        })

@router.post("/items/{item_id}/delete")
async def admin_item_delete(item_id: int, db=Depends(get_db)):
    """Delete an item"""
    item = item_crud.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    try:
        success = item_crud.delete_item(item_id)
        if success:
            add_flash_message(f"Item '{item['name']}' deleted successfully!")
        else:
            add_flash_message("Failed to delete item", "error")
        
    except Exception as e:
        add_flash_message(f"Error deleting item: {str(e)}", "error")
    
    return RedirectResponse(url="/admin/items", status_code=303)

@router.post("/items/{item_id}/activate")
async def admin_item_activate(item_id: int, db=Depends(get_db)):
    """Activate an item"""
    item = item_crud.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    try:
        item_data = ItemUpdate(status=ItemStatus.ACTIVE)
        item_crud.update_item(item_id, item_data)
        add_flash_message(f"Item '{item['name']}' activated successfully!")
    except Exception as e:
        add_flash_message(f"Error activating item: {str(e)}", "error")
    
    return RedirectResponse(url=f"/admin/items/{item_id}", status_code=303)

@router.post("/items/{item_id}/deactivate")
async def admin_item_deactivate(item_id: int, db=Depends(get_db)):
    """Deactivate an item"""
    item = item_crud.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    try:
        item_data = ItemUpdate(status=ItemStatus.INACTIVE)
        item_crud.update_item(item_id, item_data)
        add_flash_message(f"Item '{item['name']}' deactivated successfully!")
    except Exception as e:
        add_flash_message(f"Error deactivating item: {str(e)}", "error")
    
    return RedirectResponse(url=f"/admin/items/{item_id}", status_code=303)
