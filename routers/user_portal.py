"""
User Router for authenticated users
This module contains endpoints for regular authenticated users (not admin).
"""

from fastapi import APIRouter, Request, Form, HTTPException, Depends, Query, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List, Dict, Any
from data.models import ItemStatus
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
async def user_dashboard(request: Request, db=Depends(get_db), lang: Optional[str] = None):
    """Admin dashboard with overview of items and recent activity - ADMIN ONLY"""
    
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
    
    # Check admin role
    if current_user.get("role") != "admin":
        if expects_html(request):
            return create_access_denied_response(request, current_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
    
    # Get all items and users for admin overview
    all_items = item_crud.get_items()
    all_users = user_crud.get_users()
    
    # Calculate admin statistics (system-wide)
    total_items = len(all_items)
    active_items = len([item for item in all_items if item["status"] == "active"])
    total_value = sum(item["price"] for item in all_items)
    total_users = len([user for user in all_users if user["is_active"]])
    
    # Get recent items (last 5 system-wide)
    recent_items = sorted(all_items, key=lambda x: x["created_at"], reverse=True)[:5]
    
    # Get translations
    translations = get_translations_for_locale(locale)
    
    context = {
        "request": request,
        "current_user": current_user,
        "total_items": total_items,
        "active_items": active_items,
        "total_value": total_value,
        "total_users": total_users,
        "recent_items": recent_items,
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
