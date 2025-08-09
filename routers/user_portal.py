"""
User Router for authenticated users
This module contains endpoints for regular authenticated users (not admin).
"""

from fastapi import APIRouter, Request, Form, HTTPException, Depends, Query, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List, Dict, Any
from data.models import ItemStatus, ItemCreate, ItemUpdate
from data.database import get_db, user_crud, item_crud
from auth import require_login, get_current_user_from_session
from utils.html_errors import create_access_denied_response, expects_html
from utils.i18n import get_locale_from_request, get_translations_for_locale, t

# Initialize templates
templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

def get_current_user_or_redirect(request: Request):
    """Get current user or redirect to login"""
    current_user = get_current_user_from_session(request)
    
    if not current_user:
        # Create redirect URL
        redirect_url = f"/auth/login?redirect_url={request.url.path}"
        return RedirectResponse(url=redirect_url, status_code=302)
    
    return current_user

@router.get("/search", response_class=HTMLResponse)
async def user_search_items(
    request: Request, 
    q: Optional[str] = Query(None, description="Search query"),
    status: Optional[str] = Query(None, description="Item status filter"),
    owner: Optional[str] = Query(None, description="Owner filter"),
    min_price: Optional[str] = Query(None, description="Minimum price"),
    max_price: Optional[str] = Query(None, description="Maximum price"),
    sort_by: Optional[str] = Query("created_at", description="Sort field"),
    sort_order: Optional[str] = Query("desc", description="Sort order"),
    db=Depends(get_db)
):
    """Search and filter items page for authenticated users"""
    
    # Check authentication
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url={request.url.path}",
            status_code=302
        )
    
    # Convert price parameters to float, handling empty strings
    min_price_float = None
    max_price_float = None
    
    try:
        if min_price and min_price.strip():
            min_price_float = float(min_price)
    except (ValueError, AttributeError):
        min_price_float = None
        
    try:
        if max_price and max_price.strip():
            max_price_float = float(max_price)
    except (ValueError, AttributeError):
        max_price_float = None
    
    # Get all items and users
    all_items = item_crud.get_items()
    all_users = user_crud.get_users()
    
    # Create user lookup dictionary
    user_dict = {user["id"]: user for user in all_users}
    
    # Add owner information to items
    for item in all_items:
        owner_info = user_dict.get(item["owner_id"])
        item["owner_username"] = owner_info["username"] if owner_info else "Unknown"
        item["owner_full_name"] = owner_info["full_name"] if owner_info else "Unknown"
    
    # Apply filters
    filtered_items = all_items.copy()
    
    # Text search filter
    if q:
        q_lower = q.lower()
        filtered_items = [
            item for item in filtered_items
            if (q_lower in item["name"].lower() or 
                q_lower in item["description"].lower() or
                q_lower in item["owner_username"].lower())
        ]
    
    # Status filter
    if status and status != "all":
        filtered_items = [item for item in filtered_items if item["status"] == status]
    
    # Owner filter
    if owner and owner != "all":
        filtered_items = [item for item in filtered_items if item["owner_id"] == owner]
    
    # Price range filters
    if min_price_float is not None:
        filtered_items = [item for item in filtered_items if item["price"] >= min_price_float]
    
    if max_price_float is not None:
        filtered_items = [item for item in filtered_items if item["price"] <= max_price_float]
    
    # Sorting
    reverse_order = sort_order == "desc"
    
    if sort_by == "name":
        filtered_items.sort(key=lambda x: x["name"].lower(), reverse=reverse_order)
    elif sort_by == "price":
        filtered_items.sort(key=lambda x: x["price"], reverse=reverse_order)
    elif sort_by == "status":
        filtered_items.sort(key=lambda x: x["status"], reverse=reverse_order)
    elif sort_by == "owner":
        filtered_items.sort(key=lambda x: x["owner_username"].lower(), reverse=reverse_order)
    else:  # default to created_at
        filtered_items.sort(key=lambda x: x["created_at"], reverse=reverse_order)
    
    # Get unique values for filter dropdowns
    unique_statuses = list(set(item["status"] for item in all_items))
    unique_owners = [(user["id"], user["username"], user["full_name"]) for user in all_users if user["is_active"]]
    
    # Price range for display
    if all_items:
        price_range = {
            "min": min(item["price"] for item in all_items),
            "max": max(item["price"] for item in all_items)
        }
    else:
        price_range = {"min": 0, "max": 1000}
    
    return templates.TemplateResponse("user/search.html", {
        "request": request,
        "current_user": current_user,
        "items": filtered_items,
        "total_items": len(filtered_items),
        "all_items_count": len(all_items),
        "unique_statuses": unique_statuses,
        "unique_owners": unique_owners,
        "price_range": price_range,
        "search_params": {
            "q": q or "",
            "status": status or "all",
            "owner": owner or "all",
            "min_price": min_price,
            "max_price": max_price,
            "sort_by": sort_by,
            "sort_order": sort_order
        }
    })

@router.get("/dashboard", response_class=HTMLResponse)
async def user_dashboard(
    request: Request,
    query: Optional[str] = Query(None, description="Search query"),
    status: Optional[str] = Query(None, description="Filter by status"),
    lang: Optional[str] = None,
    db=Depends(get_db)
):
    """User dashboard with search functionality and CRUD options - USER ONLY"""
    
    # Get locale for internationalization
    locale = get_locale_from_request(request)
    if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
        locale = lang
    
    # Check authentication
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url={request.url.path}&lang={locale}",
            status_code=302
        )
    
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID not found"
        )
    
    # Get all user's items for statistics
    all_user_items = item_crud.get_items(owner_id=user_id)
    
    # Calculate statistics
    user_stats = {
        "total_items": len(all_user_items),
        "active_items": len([item for item in all_user_items if item["status"] == "active"]),
        "total_value": sum(item["price"] for item in all_user_items),
        "recent_items": len([item for item in all_user_items if item.get("created_at")]) # Simplified count
    }
    
    # Search functionality
    search_results = []
    search_query = query
    
    if query:
        # Filter items based on search query
        search_results = [
            item for item in all_user_items
            if query.lower() in item["name"].lower() or 
               (item.get("description") and query.lower() in item["description"].lower())
        ]
        
        # Apply status filter if provided
        if status and status != "all":
            search_results = [item for item in search_results if item["status"] == status]
    else:
        # If no search query, show recent items (up to 10)
        search_results = sorted(all_user_items, key=lambda x: x.get("created_at", ""), reverse=True)[:10]
        
        # Apply status filter if provided
        if status and status != "all":
            search_results = [item for item in search_results if item["status"] == status]
    
    # Get translations
    translations = get_translations_for_locale(locale)
    
    context = {
        "request": request,
        "current_user": current_user,
        "user_stats": user_stats,
        "items": search_results,
        "search_query": search_query,
        "search_performed": bool(query),
        "current_status": status or "all",
        "locale": locale,
        "lang": locale,
        "t": lambda key: t(key, locale),
        "translations": translations
    }
    
    response = templates.TemplateResponse("user/dashboard.html", context)
    
    # Set language cookie if specified
    if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
        response.set_cookie(
            key="lang_preference",
            value=lang,
            max_age=60*60*24*30,
            httponly=True,
            secure=False
        )
    
    return response


# CRUD Endpoints for Items Management

@router.get("/items/new", response_class=HTMLResponse)
async def new_item_form(
    request: Request,
    lang: Optional[str] = None,
    error: Optional[str] = None,
    db=Depends(get_db)
):
    """Show form to create a new item"""
    
    # Get locale for internationalization
    locale = get_locale_from_request(request)
    if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
        locale = lang
    
    # Check authentication
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url={request.url.path}&lang={locale}",
            status_code=302
        )
    
    # Get translations
    translations = get_translations_for_locale(locale)
    
    context = {
        "request": request,
        "current_user": current_user,
        "item": None,  # No item for new form
        "error": error,
        "locale": locale,
        "lang": locale,
        "t": lambda key: t(key, locale),
        "translations": translations
    }
    
    response = templates.TemplateResponse("user/item_form.html", context)
    
    # Set language cookie if specified
    if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
        response.set_cookie(
            key="lang_preference",
            value=lang,
            max_age=60*60*24*30,
            httponly=True,
            secure=False
        )
    
    return response


@router.post("/items/new")
async def create_item(
    request: Request,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    status: str = Form("draft"),
    lang: Optional[str] = Form(None),
    db=Depends(get_db)
):
    """Create a new item"""
    
    # Get locale for internationalization
    locale = get_locale_from_request(request)
    if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
        locale = lang
    
    # Check authentication
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url={request.url.path}&lang={locale}",
            status_code=302
        )
    
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID not found"
        )
    
    try:
        # Create item data
        item_data = {
            "name": name,
            "description": description,
            "price": price,
            "status": status,
            "owner_id": user_id
        }
        
        # Create the item
        new_item = item_crud.create_item(item_data)
        
        # Redirect to dashboard
        redirect_url = f"/user/dashboard?lang={locale}"
        return RedirectResponse(url=redirect_url, status_code=302)
        
    except Exception as e:
        # Handle errors by redirecting back to form with error
        redirect_url = f"/user/items/new?lang={locale}&error={str(e)}"
        return RedirectResponse(url=redirect_url, status_code=302)


@router.get("/items/{item_id}", response_class=HTMLResponse)
async def view_item(
    request: Request,
    item_id: int,
    lang: Optional[str] = None,
    error: Optional[str] = None,
    db=Depends(get_db)
):
    """View item details"""
    
    # Get locale for internationalization
    locale = get_locale_from_request(request)
    if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
        locale = lang
    
    # Check authentication
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url={request.url.path}&lang={locale}",
            status_code=302
        )
    
    # Get item
    item = item_crud.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    # Check ownership (users can only view their own items, unless admin)
    if current_user.get("role") != "admin" and item["owner_id"] != current_user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own items"
        )
    
    # Get translations
    translations = get_translations_for_locale(locale)
    
    context = {
        "request": request,
        "current_user": current_user,
        "item": item,
        "error": error,
        "locale": locale,
        "lang": locale,
        "t": lambda key: t(key, locale),
        "translations": translations
    }
    
    response = templates.TemplateResponse("user/item_detail.html", context)
    
    # Set language cookie if specified
    if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
        response.set_cookie(
            key="lang_preference",
            value=lang,
            max_age=60*60*24*30,
            httponly=True,
            secure=False
        )
    
    return response


@router.get("/items/{item_id}/edit", response_class=HTMLResponse)
async def edit_item_form(
    request: Request,
    item_id: int,
    lang: Optional[str] = None,
    error: Optional[str] = None,
    db=Depends(get_db)
):
    """Show form to edit an item"""
    
    # Get locale for internationalization
    locale = get_locale_from_request(request)
    if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
        locale = lang
    
    # Check authentication
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url={request.url.path}&lang={locale}",
            status_code=302
        )
    
    # Get item
    item = item_crud.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    # Check ownership (users can only edit their own items, unless admin)
    if current_user.get("role") != "admin" and item["owner_id"] != current_user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own items"
        )
    
    # Get translations
    translations = get_translations_for_locale(locale)
    
    context = {
        "request": request,
        "current_user": current_user,
        "item": item,
        "error": error,
        "locale": locale,
        "lang": locale,
        "t": lambda key: t(key, locale),
        "translations": translations
    }
    
    response = templates.TemplateResponse("user/item_form.html", context)
    
    # Set language cookie if specified
    if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
        response.set_cookie(
            key="lang_preference",
            value=lang,
            max_age=60*60*24*30,
            httponly=True,
            secure=False
        )
    
    return response


@router.post("/items/{item_id}/edit")
async def update_item(
    request: Request,
    item_id: int,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    status: str = Form("draft"),
    lang: Optional[str] = Form(None),
    db=Depends(get_db)
):
    """Update an item"""
    
    # Get locale for internationalization
    locale = get_locale_from_request(request)
    if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
        locale = lang
    
    # Check authentication
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url={request.url.path}&lang={locale}",
            status_code=302
        )
    
    # Get item
    item = item_crud.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    # Check ownership (users can only edit their own items, unless admin)
    if current_user.get("role") != "admin" and item["owner_id"] != current_user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own items"
        )
    
    try:
        # Create ItemUpdate object
        from data.models.item import ItemUpdate
        item_update = ItemUpdate(
            name=name,
            description=description,
            price=price,
            status=status
        )
        
        # Update the item
        updated_item = item_crud.update_item(item_id, item_update)
        if not updated_item:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update item"
            )
        
        # Redirect to item detail
        redirect_url = f"/user/items/{item_id}?lang={locale}"
        return RedirectResponse(url=redirect_url, status_code=302)
        
    except Exception as e:
        # Handle errors by redirecting back to edit form with error
        redirect_url = f"/user/items/{item_id}/edit?lang={locale}&error={str(e)}"
        return RedirectResponse(url=redirect_url, status_code=302)


@router.post("/items/{item_id}/delete")
async def delete_item(
    request: Request,
    item_id: int,
    lang: Optional[str] = Form(None),
    db=Depends(get_db)
):
    """Delete an item"""
    
    # Get locale for internationalization
    locale = get_locale_from_request(request)
    if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
        locale = lang
    
    # Check authentication
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url={request.url.path}&lang={locale}",
            status_code=302
        )
    
    # Get item
    item = item_crud.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    # Check ownership (users can only delete their own items)
    if current_user.get("role") != "admin" and item["owner_id"] != current_user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own items"
        )
    
    try:
        # Delete item
        success = item_crud.delete_item(item_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete item"
            )
        
        # Redirect to dashboard
        redirect_url = f"/user/dashboard?lang={locale}"
        return RedirectResponse(url=redirect_url, status_code=302)
        
    except Exception as e:
        # Handle errors by redirecting back to item detail with error
        redirect_url = f"/user/items/{item_id}?lang={locale}&error={str(e)}"
        return RedirectResponse(url=redirect_url, status_code=302)


@router.get("/profile", response_class=HTMLResponse)
async def user_profile(request: Request):
    """User profile page"""
    
    # Check authentication
    current_user = get_current_user_from_session(request)
    if not current_user:
        return RedirectResponse(
            url=f"/auth/login?redirect_url={request.url.path}",
            status_code=302
        )
    
    return templates.TemplateResponse("user/profile.html", {
        "request": request,
        "current_user": current_user
    })
