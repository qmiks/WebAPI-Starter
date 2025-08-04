"""
Authentication routes for login, logout, and user management.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import timedelta
from auth import (
    authenticate_user, create_session, invalidate_session,
    get_current_user_from_session, ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["authentication"])
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None, redirect_url: str = "/admin"):
    """Display login page."""
    return templates.TemplateResponse("auth/login.html", {
        "request": request,
        "error": error,
        "redirect_url": redirect_url
    })

@router.post("/login")
async def login_for_access_token(request: Request):
    """Process login form."""
    print(f"DEBUG: Received request to /auth/login")
    print(f"DEBUG: Request method: {request.method}")
    print(f"DEBUG: Request headers: {dict(request.headers)}")
    print(f"DEBUG: Request URL: {request.url}")
    
    try:
        # Try to get form data
        print("DEBUG: Attempting to get form data...")
        form_data = await request.form()
        print(f"DEBUG: Form data received: {dict(form_data)}")
        
        username = form_data.get("username")
        password = form_data.get("password")
        redirect_url = form_data.get("redirect_url", "/admin")
        
        print(f"DEBUG: Login attempt - username: {username}, redirect_url: {redirect_url}")
        
        if not username or not password:
            print("DEBUG: Missing username or password")
            return RedirectResponse(
                url="/auth/login?error=Username and password required",
                status_code=status.HTTP_303_SEE_OTHER
            )
        
        user = authenticate_user(username, password)
        if not user:
            print(f"DEBUG: Authentication failed for user: {username}")
            return RedirectResponse(
                url="/auth/login?error=Invalid username or password",
                status_code=status.HTTP_303_SEE_OTHER
            )
        
        print(f"DEBUG: Authentication successful for user: {username}")
        # Create session
        session_token = create_session(user)
        
        # Set secure cookie
        response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key="session_token",
            value=session_token,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax"
        )
        
        return response
        
    except Exception as e:
        print(f"DEBUG: Error processing login: {e}")
        return RedirectResponse(
            url="/auth/login?error=Login processing error",
            status_code=status.HTTP_303_SEE_OTHER
        )
        
@router.post("/logout")
async def logout(request: Request, response: Response):
    """Logout user by invalidating session."""
    session_token = request.cookies.get("session_token")
    if session_token:
        invalidate_session(session_token)
    
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("session_token")
    return response

@router.get("/logout")
async def logout_get(request: Request):
    """Logout via GET request."""
    session_token = request.cookies.get("session_token")
    if session_token:
        invalidate_session(session_token)
    
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("session_token")
    return response

@router.get("/me")
async def get_current_user_info(request: Request):
    """Get current user information."""
    current_user = get_current_user_from_session(request)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Remove sensitive information
    user_info = current_user.copy()
    user_info.pop("hashed_password", None)
    return user_info
