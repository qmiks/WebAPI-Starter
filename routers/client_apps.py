"""
Client App Management Router
Provides endpoints for managing client applications and API tokens.
"""

from fastapi import APIRouter, HTTPException, status, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from datetime import datetime

from data.models import (
    ClientAppCreate, ClientAppUpdate, ClientApp, ClientAppResponse, 
    ClientAppWithSecret, APITokenCreate, APIToken, MessageResponse
)
from data.database import client_app_crud
from api_auth import create_api_token, get_current_api_client
from auth import get_current_user_from_session
from utils.html_errors import create_access_denied_response, expects_html
from utils.i18n import get_locale_from_request, get_translations_for_locale, t

# Initialize templates
templates = Jinja2Templates(directory="templates")

def check_admin_access(request: Request, user=None):
    """Helper function to check admin access and return appropriate response"""
    if not user:
        user = get_current_user_from_session(request)
    
    if not user or user.get("role") != "admin":
        if expects_html(request):
            return create_access_denied_response(request, user)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
    return None  # Access granted

# Create router
router = APIRouter(
    prefix="/admin/client-apps",
    tags=["Client Apps Management"],
    dependencies=[]
)

# API Token endpoint (public for client apps)
token_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["API Authentication"]
)

@token_router.post("/token", response_model=APIToken)
async def create_token(
    app_id: str = Form(...),
    app_secret: str = Form(...),
    expires_in: Optional[int] = Form(3600)
):
    """
    Generate API token for client application
    
    This endpoint allows client applications to authenticate and receive
    an access token for API access.
    """
    return create_api_token(app_id, app_secret, expires_in)

# HTML Management Interface
@router.get("/", response_class=HTMLResponse)
async def client_apps_dashboard(request: Request, lang: Optional[str] = None):
    """Client apps management dashboard"""
    # Get locale for internationalization
    locale = get_locale_from_request(request)
    if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
        locale = lang
    
    # Check if user is authenticated and is admin
    user = get_current_user_from_session(request)
    access_error = check_admin_access(request, user)
    if access_error:
        return access_error
    
    client_apps = client_app_crud.get_client_apps()
    
    # Get translations
    translations = get_translations_for_locale(locale)
    
    response = templates.TemplateResponse("admin/client_apps.html", {
        "request": request,
        "client_apps": client_apps,
        "current_user": user,
        "locale": locale,
        "lang": locale,
        "t": lambda key: t(key, locale),
        "translations": translations
    })
    
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

@router.post("/create", response_class=HTMLResponse)
async def create_client_app_form(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    is_active: bool = Form(True)
):
    """Create new client app via form"""
    user = get_current_user_from_session(request)
    access_error = check_admin_access(request, user)
    if access_error:
        return access_error
    
    # Validate input
    if not name or len(name.strip()) < 3:
        client_apps = client_app_crud.get_client_apps()
        return templates.TemplateResponse("admin/client_apps.html", {
            "request": request,
            "client_apps": client_apps,
            "user": user,
            "error_message": "Client app name must be at least 3 characters long."
        })
    
    if len(name.strip()) > 100:
        client_apps = client_app_crud.get_client_apps()
        return templates.TemplateResponse("admin/client_apps.html", {
            "request": request,
            "client_apps": client_apps,
            "user": user,
            "error_message": "Client app name must be 100 characters or less."
        })
    
    app_data = ClientAppCreate(
        name=name.strip(),
        description=description.strip() if description else None,
        is_active=is_active
    )
    
    new_app = client_app_crud.create_client_app(app_data, user["id"])
    
    # Redirect back to dashboard with success message
    client_apps = client_app_crud.get_client_apps()
    return templates.TemplateResponse("admin/client_apps.html", {
        "request": request,
        "client_apps": client_apps,
        "user": user,
        "success_message": f"Client app '{name}' created successfully!",
        "new_app": new_app  # Show the new app with credentials
    })

@router.post("/{app_id}/regenerate-secret", response_class=HTMLResponse)
async def regenerate_secret_form(request: Request, app_id: int):
    """Regenerate app secret via form"""
    user = get_current_user_from_session(request)
    if not user or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    updated_app = client_app_crud.regenerate_secret(app_id)
    if not updated_app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client app not found"
        )
    
    client_apps = client_app_crud.get_client_apps()
    return templates.TemplateResponse("admin/client_apps.html", {
        "request": request,
        "client_apps": client_apps,
        "user": user,
        "success_message": "App secret regenerated successfully!",
        "updated_app": updated_app
    })

@router.post("/{app_id}/toggle-status", response_class=HTMLResponse)
async def toggle_app_status_form(request: Request, app_id: int):
    """Toggle app active status via form"""
    user = get_current_user_from_session(request)
    if not user or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    app = client_app_crud.get_client_app_by_id(app_id)
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client app not found"
        )
    
    # Toggle status
    update_data = ClientAppUpdate(is_active=not app["is_active"])
    updated_app = client_app_crud.update_client_app(app_id, update_data)
    
    client_apps = client_app_crud.get_client_apps()
    status_text = "activated" if updated_app["is_active"] else "deactivated"
    
    return templates.TemplateResponse("admin/client_apps.html", {
        "request": request,
        "client_apps": client_apps,
        "user": user,
        "success_message": f"App '{updated_app['name']}' {status_text} successfully!"
    })

@router.post("/{app_id}/delete", response_class=HTMLResponse)
async def delete_client_app_form(request: Request, app_id: int):
    """Delete client app via form"""
    user = get_current_user_from_session(request)
    if not user or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    app = client_app_crud.get_client_app_by_id(app_id)
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client app not found"
        )
    
    app_name = app["name"]
    success = client_app_crud.delete_client_app(app_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete client app"
        )
    
    client_apps = client_app_crud.get_client_apps()
    return templates.TemplateResponse("admin/client_apps.html", {
        "request": request,
        "client_apps": client_apps,
        "user": user,
        "success_message": f"App '{app_name}' deleted successfully!"
    })

# API Endpoints for programmatic access
@router.get("/api", response_model=List[ClientAppResponse])
async def get_client_apps_api(request: Request, skip: int = 0, limit: int = 100):
    """Get all client apps (API endpoint)"""
    user = get_current_user_from_session(request)
    if not user or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    client_apps = client_app_crud.get_client_apps(skip, limit)
    return [ClientAppResponse(**app) for app in client_apps]

@router.post("/api", response_model=ClientAppWithSecret)
async def create_client_app_api(request: Request, app_data: ClientAppCreate):
    """Create new client app (API endpoint)"""
    user = get_current_user_from_session(request)
    if not user or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    new_app = client_app_crud.create_client_app(app_data, user["id"])
    return ClientAppWithSecret(**new_app)

@router.delete("/api/{app_id}", response_model=MessageResponse)
async def delete_client_app_api(request: Request, app_id: int):
    """Delete client app (API endpoint)"""
    user = get_current_user_from_session(request)
    if not user or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    success = client_app_crud.delete_client_app(app_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client app not found"
        )
    
    return MessageResponse(message="Client app deleted successfully")

# Include token router
def get_routers():
    """Get all routers for this module"""
    return [router, token_router]
