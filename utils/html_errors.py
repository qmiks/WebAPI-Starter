"""
HTML Error Handlers
Custom error handling for HTML routes that provides user-friendly error pages
instead of JSON responses.
"""

from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, Dict, Any
import os
from utils.i18n import t, get_translations_for_locale

# Initialize templates
templates = Jinja2Templates(directory="templates")

class HTMLException(Exception):
    """Custom exception that will render HTML error pages instead of JSON"""
    
    def __init__(
        self, 
        status_code: int, 
        title: str, 
        message: str, 
        details: Optional[str] = None,
        user_info: Optional[Dict[str, Any]] = None,
        show_contact: bool = True,
        contact_message: Optional[str] = None
    ):
        self.status_code = status_code
        self.title = title
        self.message = message
        self.details = details
        self.user_info = user_info
        self.show_contact = show_contact
        self.contact_message = contact_message
        super().__init__(self.message)

def create_error_response(
    request: Request,
    status_code: int,
    title: str,
    message: str,
    details: Optional[str] = None,
    user_info: Optional[Dict[str, Any]] = None,
    show_contact: bool = True,
    contact_message: Optional[str] = None
) -> HTMLResponse:
    """Create an HTML error response"""
    
    # Get language preference
    locale = request.cookies.get("lang_preference", "en")
    if not locale or locale not in ['en', 'es', 'fr', 'de', 'pl']:
        locale = "en"
    
    # Get translations
    translations = get_translations_for_locale(locale)
    
    return templates.TemplateResponse(
        "error_page.html",
        {
            "request": request,
            "status_code": status_code,
            "title": title,
            "message": message,
            "details": details,
            "user_info": user_info,
            "current_url": str(request.url.path),
            "show_contact": show_contact,
            "contact_message": contact_message,
            "locale": locale,
            "lang": locale,
            "t": lambda key: t(key, locale),
            "translations": translations
        },
        status_code=status_code
    )

def create_access_denied_response(
    request: Request,
    user_info: Optional[Dict[str, Any]] = None,
    custom_message: Optional[str] = None
) -> HTMLResponse:
    """Create an access denied error page"""
    
    # Get language preference
    locale = request.cookies.get("lang_preference", "en")
    if not locale or locale not in ['en', 'es', 'fr', 'de', 'pl']:
        locale = "en"
    
    # Get translations
    translations = get_translations_for_locale(locale)
    
    if user_info and user_info.get("role") == "user":
        default_message = "You don't have permission to access this admin area. This section is restricted to administrators only."
        details = f"You are logged in as: {user_info.get('username', 'Unknown')} (Role: {user_info.get('role', 'Unknown')})"
    elif user_info:
        default_message = "You don't have sufficient permissions to access this resource."
        details = f"You are logged in as: {user_info.get('username', 'Unknown')} (Role: {user_info.get('role', 'Unknown')})"
    else:
        default_message = "You need to login to access this resource."
        details = "Please login with appropriate credentials to continue."
    
    message = custom_message or default_message
    
    return templates.TemplateResponse(
        "error_access_denied.html",
        {
            "request": request,
            "error_message": message,
            "error_details": details,
            "user_info": user_info,
            "current_url": str(request.url.path),
            "show_contact": True if user_info else False,
            "locale": locale,
            "lang": locale,
            "t": lambda key: t(key, locale),
            "translations": translations
        },
        status_code=403
    )

def create_not_found_response(
    request: Request,
    user_info: Optional[Dict[str, Any]] = None,
    custom_message: Optional[str] = None
) -> HTMLResponse:
    """Create a not found error page"""
    
    default_message = "The page you're looking for doesn't exist or has been moved."
    message = custom_message or default_message
    
    return create_error_response(
        request=request,
        status_code=404,
        title="Page Not Found",
        message=message,
        details=f"Requested URL: {request.url.path}",
        user_info=user_info,
        show_contact=False
    )

def create_server_error_response(
    request: Request,
    user_info: Optional[Dict[str, Any]] = None,
    custom_message: Optional[str] = None,
    error_details: Optional[str] = None
) -> HTMLResponse:
    """Create a server error page"""
    
    default_message = "An unexpected error occurred on our servers. Please try again later."
    message = custom_message or default_message
    
    return create_error_response(
        request=request,
        status_code=500,
        title="Internal Server Error",
        message=message,
        details=error_details,
        user_info=user_info,
        show_contact=True,
        contact_message="If this problem persists, please contact technical support."
    )

# Helper function to check if request expects HTML
def expects_html(request: Request) -> bool:
    """Check if the request expects HTML response"""
    accept_header = request.headers.get("accept", "")
    
    # Check if it's likely a browser request
    return (
        "text/html" in accept_header or
        "text/*" in accept_header or
        "*/*" in accept_header or
        not accept_header  # Default to HTML if no accept header
    )

# Decorator for HTML-aware authentication
def html_auth_required(admin_required: bool = False):
    """Decorator that provides HTML-friendly authentication errors"""
    
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            from auth import get_current_user_from_request
            
            # Get current user
            current_user = get_current_user_from_request(request)
            
            # Check if user is authenticated
            if not current_user:
                if expects_html(request):
                    # Redirect to login for HTML requests
                    from fastapi.responses import RedirectResponse
                    return RedirectResponse(
                        url=f"/auth/login?redirect_url={request.url.path}",
                        status_code=303
                    )
                else:
                    # Return JSON error for API requests
                    raise HTTPException(
                        status_code=401,
                        detail="Authentication required"
                    )
            
            # Check admin access if required
            if admin_required and current_user.get("role") != "admin":
                if expects_html(request):
                    # Return HTML error page
                    return create_access_denied_response(request, current_user)
                else:
                    # Return JSON error for API requests
                    raise HTTPException(
                        status_code=403,
                        detail="Admin access required"
                    )
            
            # Call the original function with current_user
            return await func(request, current_user, *args, **kwargs)
        
        return wrapper
    return decorator
