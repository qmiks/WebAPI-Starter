"""
Updated Admin Router with Authentication
This module contains all admin-related endpoints for the web interface with authentication.
"""

from fastapi import APIRouter, Request, Form, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List, Dict, Any
from functools import wraps
from data.models import UserCreate, UserUpdate, UserRole, ItemCreate, ItemUpdate, ItemStatus
from data.database import get_db, user_crud, item_crud, client_app_crud
from auth import get_current_user_from_session, get_password_hash
from utils.html_errors import create_access_denied_response, expects_html

# Initialize templates
templates = Jinja2Templates(directory="templates")

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

async def require_admin_user(request: Request) -> dict:
    """FastAPI dependency to require admin access"""
    current_user = get_current_user_from_session(request)
    
    if not current_user:
        # Not logged in - redirect to login with current URL as redirect_url
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"redirect:/auth/login?redirect_url={request.url.path}",
            headers={"Location": f"/auth/login?redirect_url={request.url.path}"}
        )
    
    if current_user.get("role") != "admin":
        # Not admin - check if HTML request and return appropriate response
        if expects_html(request):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
    
    return current_user

@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Admin dashboard with statistics and navigation"""
    print(f"DEBUG: Admin dashboard called")
    
    # Manual authentication check
    session_token = request.cookies.get("session_token")
    print(f"DEBUG: Session token found: {bool(session_token)}")
    if session_token:
        print(f"DEBUG: Token preview: {session_token[:20]}...")
        
    current_user = get_current_user_from_session(request)
    print(f"DEBUG: Current user: {current_user}")
    
    if not current_user:
        print("DEBUG: No current user, redirecting to login")
        return RedirectResponse(
            url=f"/auth/login?redirect_url={request.url.path}",
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    if current_user.get("role") != "admin":
        print("DEBUG: User is not admin, returning HTML error page")
        return create_access_denied_response(request, current_user)
    
    print("DEBUG: Authentication successful, loading dashboard")
    
    # Get statistics
    all_users = user_crud.get_users()
    all_items = item_crud.get_items()
    all_client_apps = client_app_crud.get_client_apps()
    
    total_users = len(all_users)
    active_users = len([user for user in all_users if user["is_active"]])
    total_items = len(all_items)
    active_items = len([item for item in all_items if item["status"] == "active"])
    total_client_apps = len(all_client_apps)
    active_client_apps = len([app for app in all_client_apps if app["is_active"]])
    
    # Recent activity counts
    from datetime import datetime, timedelta
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    
    # For now, use simple counts until created_at is properly implemented
    recent_users_count = max(0, len(all_users) - 1)  # Exclude initial sample users
    recent_items_count = len(all_items)
    recent_apps_count = len(all_client_apps)
    
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "user": current_user,
        "total_users": total_users,
        "active_users": active_users,
        "total_items": total_items,
        "active_items": active_items,
        "total_client_apps": total_client_apps,
        "active_client_apps": active_client_apps,
        "recent_users_count": recent_users_count,
        "recent_items_count": recent_items_count,
        "recent_apps_count": recent_apps_count,
        "api_calls_today": 42,  # Mock data
        "total_api_calls": 1337,  # Mock data
        "storage_usage": "78%"  # Mock data
    })
    
    try:
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "current_user": current_user,
            "total_users": total_users,
            "active_users": active_users,
            "total_items": total_items,
            "active_items": active_items,
            "total_client_apps": total_client_apps,
            "active_client_apps": active_client_apps,
            "recent_users": recent_users,
            "recent_items": recent_items,
            "recent_client_apps": recent_client_apps,
            "messages": get_flash_messages()
        })
    except Exception as e:
        print(f"DEBUG: Template error: {e}")
        # Fallback to simple HTML if template fails
        return HTMLResponse(content=f"""
        <html>
            <head><title>Admin Dashboard</title></head>
            <body>
                <h1>Welcome to Admin Dashboard!</h1>
                <p>Hello, {current_user.get('username', 'Admin')}!</p>
                <p>Users: {total_users} (Active: {active_users})</p>
                <p>Items: {total_items} (Active: {active_items})</p>
                <p>Client Apps: {total_client_apps} (Active: {active_client_apps})</p>
                <p><a href="/admin/users">Manage Users</a></p>
                <p><a href="/admin/items">Manage Items</a></p>
                <p><a href="/admin/client-apps">Manage Client Apps</a></p>
                <p><a href="/user/search">User Portal</a></p>
                <p><a href="/auth/logout">Logout</a></p>
            </body>
        </html>
        """)

@router.get("/users", response_class=HTMLResponse)
async def admin_users_list(request: Request):
    """Users management page"""
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(url=f"/auth/login?redirect_url={request.url.path}")
    
    if current_user.get("role") != "admin":
        return create_access_denied_response(request, current_user)
    
    # Get all users with additional statistics
    all_users = user_crud.get_users()
    total_users = len(all_users)
    active_users = len([user for user in all_users if user["is_active"]])
    admin_users = len([user for user in all_users if user["role"] == "admin"])
    
    # Recent users count (this week) - simplified for now
    from datetime import datetime, timedelta
    week_ago = datetime.now() - timedelta(days=7)
    recent_users_count = max(0, len(all_users) - 2)  # Simple count excluding starter users
    
    return templates.TemplateResponse("admin/users.html", {
        "request": request,
        "user": current_user,
        "users": all_users,
        "total_users": total_users,
        "active_users": active_users,
        "admin_users": admin_users,
        "recent_users_count": recent_users_count
    })

@router.get("/users/new", response_class=HTMLResponse)
async def admin_user_new_form(request: Request, current_user: dict = Depends(require_admin_user)):
    """Show form to create a new user"""
    return templates.TemplateResponse("user_form.html", {
        "request": request,
        "current_user": current_user,
        "user": None,
        "action": "Create",
        "form_action": "/admin/users/new"
    })

@router.post("/users/new")
async def admin_user_create(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    role: UserRole = Form(...),
    is_active: Optional[str] = Form(None),
    current_user: dict = Depends(require_admin_user),
    db=Depends(get_db)
):
    """Create a new user"""
    try:
        # Convert checkbox value to boolean (checkbox sends "true" when checked, None when unchecked)
        is_active_bool = is_active == "true" if is_active else False
        
        print(f"DEBUG: Creating new user - username={username}, email={email}, role={role}, is_active={is_active} -> {is_active_bool}")
        
        # Check if username already exists
        existing_users = user_crud.get_users()
        print(f"DEBUG: Checking username '{username}' against existing users")
        print(f"DEBUG: Existing usernames: {[user['username'] for user in existing_users]}")
        
        if any(user["username"] == username for user in existing_users):
            print(f"DEBUG: Username '{username}' already exists! Returning error.")
            return templates.TemplateResponse("user_form.html", {
                "request": request,
                "current_user": current_user,
                "user": None,
                "action": "Create",
                "form_action": "/admin/users/new",
                "error": f"Username '{username}' already exists",
                "form_data": {
                    "username": username,
                    "email": email,
                    "full_name": full_name,
                    "role": role.value,
                    "is_active": is_active_bool
                }
            })
        
        # Check if email already exists
        if any(user["email"] == email for user in existing_users):
            return templates.TemplateResponse("user_form.html", {
                "request": request,
                "current_user": current_user,
                "user": None,
                "action": "Create", 
                "form_action": "/admin/users/new",
                "error": f"Email '{email}' already exists",
                "form_data": {
                    "username": username,
                    "email": email,
                    "full_name": full_name,
                    "role": role.value,
                    "is_active": is_active_bool
                }
            })
        
        # Create user
        user_data = UserCreate(
            username=username,
            email=email,
            full_name=full_name,
            password=password,
            role=role,
            is_active=is_active_bool
        )
        
        new_user = user_crud.create_user(user_data)
        print(f"DEBUG: User created successfully: {new_user}")
        add_flash_message(f"User '{username}' created successfully!")
        
        return RedirectResponse(url="/admin/users", status_code=303)
        
    except Exception as e:
        print(f"DEBUG: Error creating user: {e}")
        return templates.TemplateResponse("user_form.html", {
            "request": request,
            "current_user": current_user,
            "user": None,
            "action": "Create",
            "form_action": "/admin/users/new",
            "error": f"Error creating user: {str(e)}",
            "form_data": {
                "username": username,
                "email": email,
                "full_name": full_name,
                "role": role.value,
                "is_active": is_active_bool
            }
        })

@router.get("/users/{user_id}", response_class=HTMLResponse)
async def admin_user_detail(request: Request, user_id: str, current_user: dict = Depends(require_admin_user), db=Depends(get_db)):
    """Display detailed user information"""
    user = user_crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's items
    all_items = item_crud.get_items()
    user_items = [item for item in all_items if item["owner_id"] == user_id]
    
    return templates.TemplateResponse("user_detail.html", {
        "request": request,
        "current_user": current_user,
        "user": user,
        "user_items": user_items,
        "messages": get_flash_messages()
    })

@router.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def admin_user_edit_form(request: Request, user_id: str, current_user: dict = Depends(require_admin_user), db=Depends(get_db)):
    """Show form to edit a user"""
    user = user_crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return templates.TemplateResponse("user_form.html", {
        "request": request,
        "current_user": current_user,
        "user": user,
        "action": "Edit",
        "form_action": f"/admin/users/{user_id}/edit",
        "messages": get_flash_messages()
    })

@router.post("/users/{user_id}/edit")
async def admin_user_edit_submit(
    request: Request,
    user_id: str,
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(""),
    role: str = Form(...),
    is_active: Optional[str] = Form(None),
    password: str = Form(""),
    current_user: dict = Depends(require_admin_user),
    db=Depends(get_db)
):
    """Handle user edit form submission"""
    try:
        # Validate role
        if role not in ["user", "admin"]:
            raise ValueError("Invalid role")
        
        # Get existing user
        existing_user = user_crud.get_user(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Convert checkbox value to boolean (checkbox sends "true" when checked, None when unchecked)
        is_active_bool = is_active == "true" if is_active else False
        
        # Prepare update data
        update_data = {
            "username": username,
            "email": email,
            "full_name": full_name if full_name else None,
            "role": role,
            "is_active": is_active_bool
        }
        
        # Only update password if provided
        if password and password.strip():
            update_data["password"] = password
        
        # Create UserUpdate object
        user_update = UserUpdate(**update_data)
        
        # Update the user
        updated_user = user_crud.update_user(user_id, user_update)
        
        add_flash_message(f"User '{username}' updated successfully!")
        return RedirectResponse(url=f"/admin/users/{user_id}", status_code=303)
        
    except Exception as e:
        print(f"DEBUG: Error updating user: {e}")
        # Return form with error
        user = user_crud.get_user(user_id)
        return templates.TemplateResponse("user_form.html", {
            "request": request,
            "current_user": current_user,
            "user": user,
            "action": "Edit",
            "form_action": f"/admin/users/{user_id}/edit",
            "error": f"Error updating user: {str(e)}"
        })

@router.post("/users/{user_id}/delete")
async def admin_delete_user(request: Request, user_id: str, current_user: dict = Depends(require_admin_user)):
    """Delete a user"""
    try:
        # Check if user exists
        user = user_crud.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Prevent deletion of the current user (admin deleting themselves)
        if str(current_user.get("id")) == str(user_id):
            add_flash_message("You cannot delete your own account!")
            return RedirectResponse(url="/admin/users", status_code=303)
        
        # Delete the user
        success = user_crud.delete_user(user_id)
        if success:
            add_flash_message(f"User '{user['username']}' has been deleted successfully!")
            print(f"DEBUG: User {user_id} ({user['username']}) deleted by admin {current_user.get('username')}")
        else:
            add_flash_message("Failed to delete user. Please try again.")
            print(f"DEBUG: Failed to delete user {user_id}")
        
        return RedirectResponse(url="/admin/users", status_code=303)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: Error deleting user: {e}")
        add_flash_message(f"Error deleting user: {str(e)}")
        return RedirectResponse(url="/admin/users", status_code=303)

# Continue with remaining routes using the same pattern...
# For brevity, I'll include a few more key routes

@router.get("/items", response_class=HTMLResponse)
async def admin_items_list(request: Request):
    """Items management page"""
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(url=f"/auth/login?redirect_url={request.url.path}")
    
    if current_user.get("role") != "admin":
        return create_access_denied_response(request, current_user)
    
    # Get all items with additional statistics
    all_items = item_crud.get_items()
    total_items = len(all_items)
    active_items = len([item for item in all_items if item["status"] == "active"])
    draft_items = len([item for item in all_items if item["status"] == "draft"])
    
    # Recent items count (today) - simplified for now
    from datetime import datetime
    today = datetime.now().date()
    recent_items_count = len(all_items)  # Simple count of all items
    
    return templates.TemplateResponse("admin/items.html", {
        "request": request,
        "user": current_user,
        "items": all_items,
        "total_items": total_items,
        "active_items": active_items,
        "draft_items": draft_items,
        "recent_items_count": recent_items_count
    })

@router.get("/items/new", response_class=HTMLResponse)
async def admin_item_new_form(request: Request):
    """Show form to create a new item"""
    # Manual authentication check
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url={request.url.path}",
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    if current_user.get("role") != "admin":
        if expects_html(request):
            return create_access_denied_response(request, current_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
    
    users = user_crud.get_users()
    active_users = [user for user in users if user["is_active"]]
    
    return templates.TemplateResponse("item_form.html", {
        "request": request,
        "current_user": current_user,
        "item": None,
        "action": "Create",
        "form_action": "/admin/items/new",
        "users": active_users
    })

@router.post("/items/new")
async def admin_item_create(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    status: ItemStatus = Form(...),
    owner_id: str = Form(...)
):
    """Create a new item"""
    # Manual authentication check
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url=/admin/items",
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    if current_user.get("role") != "admin":
        if expects_html(request):
            return create_access_denied_response(request, current_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
    
    try:
        print(f"DEBUG: Creating item - name={name}, price={price}, status={status}, owner_id={owner_id}")
        
        # Validate price
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        
        # Create item data
        item_data = ItemCreate(
            name=name,
            description=description,
            price=price,
            status=status,
            owner_id=int(owner_id)  # Convert string to int
        )
        
        print(f"DEBUG: Item data created: {item_data.model_dump()}")
        
        # Create the item - pass ItemCreate object and owner_id separately
        new_item = item_crud.create_item(item_data, int(owner_id))
        print(f"DEBUG: Item created successfully: {new_item}")
        add_flash_message(f"Item '{name}' created successfully!")
        
        return RedirectResponse(url="/admin/items", status_code=303)
        
    except Exception as e:
        print(f"DEBUG: Error creating item: {e}")
        # Return form with error
        users = user_crud.get_users()
        active_users = [user for user in users if user["is_active"]]
        
        return templates.TemplateResponse("item_form.html", {
            "request": request,
            "current_user": current_user,
            "item": None,
            "action": "Create",
            "form_action": "/admin/items/new",
            "users": active_users,
            "error": f"Error creating item: {str(e)}"
        })

@router.get("/items/{item_id}/edit", response_class=HTMLResponse)
async def admin_item_edit_form(request: Request, item_id: str):
    """Show form to edit an item"""
    # Manual authentication check
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url={request.url.path}",
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    if current_user.get("role") != "admin":
        if expects_html(request):
            return create_access_denied_response(request, current_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
    
    item = item_crud.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    users = user_crud.get_users()
    active_users = [user for user in users if user["is_active"]]
    
    return templates.TemplateResponse("item_form.html", {
        "request": request,
        "current_user": current_user,
        "item": item,
        "action": "Edit",
        "form_action": f"/admin/items/{item_id}/edit",
        "users": active_users
    })

@router.post("/items/{item_id}/edit")
async def admin_item_update(
    request: Request,
    item_id: str,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    status: ItemStatus = Form(...),
    owner_id: str = Form(...)
):
    """Update an existing item"""
    # Manual authentication check
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url=/admin/items",
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    if current_user.get("role") != "admin":
        if expects_html(request):
            return create_access_denied_response(request, current_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
    
    try:
        print(f"DEBUG: Updating item {item_id} - name={name}, price={price}, status={status}, owner_id={owner_id}")
        
        # Check if item exists
        existing_item = item_crud.get_item(item_id)
        if not existing_item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Validate price
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        
        # Update item data
        item_data = ItemUpdate(
            name=name,
            description=description,
            price=price,
            status=status,
            owner_id=int(owner_id)  # Convert string to int
        )
        
        print(f"DEBUG: Update data: {item_data.model_dump()}")
        
        # Update the item - pass ItemUpdate object, not dict
        updated_item = item_crud.update_item(item_id, item_data)
        print(f"DEBUG: Item updated successfully: {updated_item}")
        add_flash_message(f"Item '{name}' updated successfully!")
        
        return RedirectResponse(url="/admin/items", status_code=303)
        
    except Exception as e:
        print(f"DEBUG: Error updating item: {e}")
        # Return form with error
        users = user_crud.get_users()
        active_users = [user for user in users if user["is_active"]]
        item = item_crud.get_item(item_id)
        
        return templates.TemplateResponse("item_form.html", {
            "request": request,
            "current_user": current_user,
            "item": item,
            "action": "Edit",
            "form_action": f"/admin/items/{item_id}/edit",
            "users": active_users,
            "error": f"Error updating item: {str(e)}"
        })

@router.get("/items/{item_id}", response_class=HTMLResponse)
async def admin_item_detail(request: Request, item_id: str):
    """Display detailed item information"""
    # Manual authentication check
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url={request.url.path}",
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    if current_user.get("role") != "admin":
        if expects_html(request):
            return create_access_denied_response(request, current_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
    
    item = item_crud.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Get owner information
    owner = None
    if item.get("owner_id"):
        owner = user_crud.get_user(item["owner_id"])
    
    return templates.TemplateResponse("item_detail.html", {
        "request": request,
        "current_user": current_user,
        "item": item,
        "owner": owner
    })

@router.post("/items/{item_id}/toggle-status")
async def admin_item_toggle_status(request: Request, item_id: str):
    """Toggle item status between active and inactive"""
    # Manual authentication check
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url=/admin/items",
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    if current_user.get("role") != "admin":
        if expects_html(request):
            return create_access_denied_response(request, current_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
    
    try:
        # Get current item
        item = item_crud.get_item(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Toggle status
        current_status = item.get("status", "inactive")
        if current_status == "active":
            new_status = ItemStatus.INACTIVE
            status_text = "deactivated"
        else:
            new_status = ItemStatus.ACTIVE
            status_text = "activated"
        
        # Update item status
        item_data = ItemUpdate(status=new_status)
        updated_item = item_crud.update_item(item_id, item_data)
        
        add_flash_message(f"Item '{item['name']}' {status_text} successfully!")
        return RedirectResponse(url="/admin/items", status_code=303)
        
    except Exception as e:
        print(f"DEBUG: Error toggling item status: {e}")
        add_flash_message(f"Error updating item: {str(e)}", "error")
        return RedirectResponse(url="/admin/items", status_code=303)

# Logout route
@router.get("/logout")
async def admin_logout(request: Request, current_user: dict = Depends(require_admin_user)):
    """Logout from admin panel"""
    response = RedirectResponse(url="/auth/logout", status_code=status.HTTP_303_SEE_OTHER)
    return response
