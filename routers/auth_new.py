"""
Simplified Authentication Router
"""

from fastapi import APIRouter, Request, Body, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from auth import authenticate_user, create_session, ACCESS_TOKEN_EXPIRE_MINUTES
from data.models import UserCreate, UserRole
from data.database import user_crud
from pydantic import BaseModel, ValidationError
from urllib.parse import quote
import re

router = APIRouter(prefix="/auth", tags=["authentication"])
templates = Jinja2Templates(directory="templates")

class LoginRequest(BaseModel):
    username: str
    password: str

@router.get("/login")
async def login_page(request: Request, error: str = None, success: str = None, redirect_url: str = "/admin"):
    """Display login page."""
    return templates.TemplateResponse("auth/login.html", {
        "request": request,
        "error": error,
        "success": success,
        "redirect_url": redirect_url
    })

@router.post("/login")
async def process_login(request: Request):
    """Process login form with simplified approach"""
    print(f"DEBUG: Processing login form submission")
    
    try:
        form_data = await request.form()
        print(f"DEBUG: Form data received: {dict(form_data)}")
        
        username = form_data.get("username")
        password = form_data.get("password")
        redirect_url = form_data.get("redirect_url")
        
        if not username or not password:
            error_redirect = f"/auth/login?error=Username and password required"
            if redirect_url:
                error_redirect += f"&redirect_url={quote(redirect_url)}"
            return RedirectResponse(
                url=error_redirect,
                status_code=303
            )
        
        user = authenticate_user(username, password)
        if not user:
            error_redirect = f"/auth/login?error=Invalid credentials"
            if redirect_url:
                error_redirect += f"&redirect_url={quote(redirect_url)}"
            return RedirectResponse(
                url=error_redirect,
                status_code=303
            )
        
        # Create session
        session_token = create_session(user)
        
        # Determine redirect URL based on user role if not specified
        if not redirect_url:
            if user.get("role") == "admin":
                redirect_url = "/admin/"
            else:
                redirect_url = "/user/search"
        
        # Redirect with session cookie
        response = RedirectResponse(url=redirect_url, status_code=303)
        response.set_cookie(
            key="session_token",
            value=session_token,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=False
        )
        
        print(f"DEBUG: Login successful for {username}, redirecting to {redirect_url}")
        return response
        
    except Exception as e:
        print(f"DEBUG: Login error: {e}")
        return RedirectResponse(
            url=f"/auth/login?error=Login processing error",
            status_code=303
        )

@router.post("/form-login")
async def form_login(request: Request):
    """Dedicated form-based login endpoint"""
    print(f"DEBUG: Form-based login attempt")
    
    try:
        form_data = await request.form()
        print(f"DEBUG: Form data: {dict(form_data)}")
        
        username = form_data.get("username")
        password = form_data.get("password")
        redirect_url = form_data.get("redirect_url")
        
        if not username or not password:
            return RedirectResponse(
                url=f"/auth/login?error=Missing credentials",
                status_code=303
            )
        
        user = authenticate_user(username, password)
        if not user:
            return RedirectResponse(
                url=f"/auth/login?error=Invalid credentials",
                status_code=303
            )
        
        # Create session
        session_token = create_session(user)
        print(f"DEBUG: Created session token: {session_token[:20]}...")
        
        # Determine redirect URL based on user role if not specified
        if not redirect_url:
            if user.get("role") == "admin":
                redirect_url = "/admin/"
            else:
                redirect_url = "/user/search"
        
        # Redirect with session cookie
        response = RedirectResponse(url=redirect_url, status_code=303)
        response.set_cookie(
            key="session_token",
            value=session_token,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=False
        )
        
        print(f"DEBUG: Set cookie and redirecting to {redirect_url}")
        print(f"DEBUG: User role: {user.get('role')}")
        print(f"DEBUG: Form login successful for {username}, redirecting to {redirect_url}")
        return response
        
    except Exception as e:
        print(f"DEBUG: Form login error: {e}")
        return RedirectResponse(
            url=f"/auth/login?error=Login error",
            status_code=303
        )

@router.get("/register")
async def register_page(request: Request, error: str = None, success: str = None):
    """Display user registration page."""
    return templates.TemplateResponse("register.html", {
        "request": request,
        "error": error,
        "success": success
    })

@router.post("/register")
async def process_registration(request: Request):
    """Process user registration form"""
    print(f"DEBUG: Processing registration form submission")
    
    try:
        form_data = await request.form()
        print(f"DEBUG: Registration form data received: {dict(form_data)}")
        
        username = form_data.get("username", "").strip()
        email = form_data.get("email", "").strip()
        full_name = form_data.get("full_name", "").strip()
        password = form_data.get("password", "")
        confirm_password = form_data.get("confirm_password", "")
        
        # Basic validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append("Username must be at least 3 characters long")
        elif len(username) > 50:
            errors.append("Username must be less than 50 characters")
        elif not re.match(r'^[a-zA-Z0-9_-]+$', username):
            errors.append("Username can only contain letters, numbers, hyphens, and underscores")
            
        if not email:
            errors.append("Email is required")
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors.append("Please enter a valid email address")
            
        if not password:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        elif not re.search(r'[a-zA-Z]', password):
            errors.append("Password must contain at least one letter")
        elif not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
            
        if password != confirm_password:
            errors.append("Passwords do not match")
            
        # Check if username or email already exists
        existing_users = user_crud.get_users()
        if any(user["username"].lower() == username.lower() for user in existing_users):
            errors.append("Username already exists")
        if any(user["email"].lower() == email.lower() for user in existing_users):
            errors.append("Email already exists")
            
        if errors:
            error_message = ". ".join(errors)
            return templates.TemplateResponse("register.html", {
                "request": request,
                "error": error_message,
                "username": username,
                "email": email,
                "full_name": full_name
            })
        
        # Create user
        try:
            user_data = UserCreate(
                username=username,
                email=email,
                full_name=full_name if full_name else None,
                password=password,
                role=UserRole.USER,  # Regular users get USER role
                is_active=True
            )
            
            # Hash password and create user
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            new_user = {
                "id": len(existing_users) + 1,
                "username": user_data.username,
                "email": user_data.email,
                "full_name": user_data.full_name,
                "role": user_data.role,
                "hashed_password": pwd_context.hash(user_data.password),
                "is_active": user_data.is_active,
                "created_at": __import__('datetime').datetime.now(),
                "updated_at": None
            }
            
            # Add to database
            from data.database import users_db, user_id_counter
            users_db.append(new_user)
            
            print(f"DEBUG: User {username} registered successfully")
            
            # Redirect to login with success message
            return RedirectResponse(
                url=f"/auth/login?success=Registration successful! Please log in with your new account.",
                status_code=303
            )
            
        except ValidationError as ve:
            error_message = ". ".join([f"{err['loc'][-1]}: {err['msg']}" for err in ve.errors()])
            return templates.TemplateResponse("register.html", {
                "request": request,
                "error": f"Validation error: {error_message}",
                "username": username,
                "email": email,
                "full_name": full_name
            })
            
        except Exception as e:
            print(f"DEBUG: Registration error: {e}")
            return templates.TemplateResponse("register.html", {
                "request": request,
                "error": "Registration failed. Please try again.",
                "username": username,
                "email": email,
                "full_name": full_name
            })
        
    except Exception as e:
        print(f"DEBUG: Registration processing error: {e}")
        return RedirectResponse(
            url=f"/auth/register?error=Registration processing error",
            status_code=303
        )
