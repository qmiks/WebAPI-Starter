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
from utils.i18n import get_locale_from_request, get_translations_for_locale, t
from typing import Optional

router = APIRouter(prefix="/auth", tags=["authentication"])
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(
    request: Request, 
    error: Optional[str] = None, 
    redirect_url: str = "/admin",
    lang: Optional[str] = None
):
    """Display login page with language support."""
    try:
        # Get locale (URL param -> cookie -> header -> default)
        locale = get_locale_from_request(request)
        if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
            locale = lang
        
        # Get translations
        translations = get_translations_for_locale(locale)
        
        context = {
            "request": request,
            "error": error,
            "redirect_url": redirect_url,
            "locale": locale,
            "lang": locale,
            "t": lambda key: t(key, locale),
            "translations": translations
        }
        
        response = templates.TemplateResponse("auth/login.html", context)
        
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
        
    except Exception as e:
        print(f"Login page error: {e}")
        return templates.TemplateResponse("error_page.html", {
            "request": request,
            "error": "Login page error"
        })

@router.post("/login")
async def login_for_access_token(request: Request):
    """Process login form with language support."""
    print(f"DEBUG: Received request to /auth/login")
    print(f"DEBUG: Request method: {request.method}")
    print(f"DEBUG: Request URL: {request.url}")
    
    try:
        # Try to get form data
        print("DEBUG: Attempting to get form data...")
        form_data = await request.form()
        print(f"DEBUG: Form data received: {dict(form_data)}")
        
        username = form_data.get("username")
        password = form_data.get("password")
        redirect_url = form_data.get("redirect_url", "/admin")
        lang = form_data.get("lang", "en")
        
        print(f"DEBUG: Login attempt - username: {username}, redirect_url: {redirect_url}, lang: {lang}")
        
        # Validate language
        if lang not in ['en', 'es', 'fr', 'de']:
            lang = 'en'
        
        if not username or not password:
            print("DEBUG: Missing username or password")
            error_msg = t("auth.invalid_credentials", lang)
            return RedirectResponse(
                url=f"/auth/login?error={error_msg}&redirect_url={redirect_url}&lang={lang}",
                status_code=status.HTTP_303_SEE_OTHER
            )
        
        user = authenticate_user(username, password)
        if not user:
            print(f"DEBUG: Authentication failed for user: {username}")
            error_msg = t("auth.invalid_credentials", lang)
            return RedirectResponse(
                url=f"/auth/login?error={error_msg}&redirect_url={redirect_url}&lang={lang}",
                status_code=status.HTTP_303_SEE_OTHER
            )
        
        print(f"DEBUG: Authentication successful for user: {username}")
        # Create session
        session_token = create_session(user)
        
        # Build redirect URL with language parameter
        if redirect_url:
            # Add lang parameter to redirect URL if not already present
            separator = "&" if "?" in redirect_url else "?"
            if "lang=" not in redirect_url:
                redirect_url = f"{redirect_url}{separator}lang={lang}"
        else:
            redirect_url = f"/?lang={lang}"
        
        # Set secure cookie and language preference
        response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key="session_token",
            value=session_token,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax"
        )
        
        # Set language preference cookie
        response.set_cookie(
            key="lang_preference",
            value=lang,
            max_age=60*60*24*30,  # 30 days
            httponly=True,
            secure=False
        )
        
        print(f"DEBUG: Login successful, redirecting to {redirect_url} with lang={lang}")
        return response
        
    except Exception as e:
        print(f"DEBUG: Error processing login: {e}")
        error_msg = t("auth.login_error", lang if 'lang' in locals() else 'en')
        return RedirectResponse(
            url=f"/auth/login?error={error_msg}&redirect_url={redirect_url}&lang={lang if 'lang' in locals() else 'en'}",
            status_code=status.HTTP_303_SEE_OTHER
        )
        return RedirectResponse(
            url="/auth/login?error=Login processing error",
            status_code=status.HTTP_303_SEE_OTHER
        )
        
@router.post("/logout")
async def logout(request: Request, response: Response, lang: Optional[str] = None):
    """Logout user by invalidating session."""
    session_token = request.cookies.get("session_token")
    if session_token:
        invalidate_session(session_token)
    
    # Get language preference
    locale = lang or get_locale_from_request(request)
    
    response = RedirectResponse(url=f"/?lang={locale}", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("session_token")
    
    # Keep language preference
    if locale != 'en':
        response.set_cookie(
            key="lang_preference",
            value=locale,
            max_age=60*60*24*30,
            httponly=True,
            secure=False
        )
    
    return response

@router.get("/logout")
async def logout_get(request: Request, lang: Optional[str] = None):
    """Logout via GET request."""
    session_token = request.cookies.get("session_token")
    if session_token:
        invalidate_session(session_token)
    
    # Get language preference
    locale = lang or get_locale_from_request(request)
    
    response = RedirectResponse(url=f"/?lang={locale}", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("session_token")
    
    # Keep language preference
    if locale != 'en':
        response.set_cookie(
            key="lang_preference",
            value=locale,
            max_age=60*60*24*30,
            httponly=True,
            secure=False
        )
    
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


@router.get("/register", response_class=HTMLResponse)
async def register_page(
    request: Request, 
    error: Optional[str] = None, 
    lang: Optional[str] = None
):
    """Display registration page with language support."""
    try:
        # Get locale (URL param -> cookie -> header -> default)
        locale = get_locale_from_request(request)
        if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
            locale = lang
        
        # Get translations
        translations = get_translations_for_locale(locale)
        
        context = {
            "request": request,
            "error": error,
            "locale": locale,
            "lang": locale,
            "t": lambda key: t(key, locale),
            "translations": translations
        }
        
        response = templates.TemplateResponse("register.html", context)
        
        # Set language cookie if specified
        if lang and lang in ['en', 'es', 'fr', 'de', 'pl']:
            response.set_cookie(
                key="lang_preference",
                value=lang,
                max_age=30 * 24 * 60 * 60,  # 30 days
                httponly=True,
                samesite="lax"
            )
        
        return response
        
    except Exception as e:
        print(f"Error in register_page: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/register", response_class=HTMLResponse)
async def register_user(request: Request):
    """Process user registration."""
    try:
        # Get locale for error messages
        locale = get_locale_from_request(request)
        
        # Get form data
        form_data = await request.form()
        username = form_data.get("username", "").strip()
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "")
        confirm_password = form_data.get("confirm_password", "")
        full_name = form_data.get("full_name", "").strip()
        
        # Basic validation
        if not username or not email or not password:
            error_msg = t("auth.all_fields_required", locale) or "All fields are required"
            return RedirectResponse(
                url=f"/auth/register?error={error_msg}&lang={locale}",
                status_code=302
            )
        
        if password != confirm_password:
            error_msg = t("auth.passwords_not_match", locale) or "Passwords do not match"
            return RedirectResponse(
                url=f"/auth/register?error={error_msg}&lang={locale}",
                status_code=302
            )
        
        if len(password) < 6:
            error_msg = t("auth.password_too_short", locale) or "Password must be at least 6 characters"
            return RedirectResponse(
                url=f"/auth/register?error={error_msg}&lang={locale}",
                status_code=302
            )
        
        # For now, just show a success message since we don't have user creation logic
        success_msg = t("auth.registration_success", locale) or "Registration successful! Please contact admin to activate your account."
        return RedirectResponse(
            url=f"/auth/login?message={success_msg}&lang={locale}",
            status_code=302
        )
        
    except Exception as e:
        print(f"Error in register_user: {e}")
        error_msg = t("general.internal_error", locale) or "Internal server error"
        return RedirectResponse(
            url=f"/auth/register?error={error_msg}&lang={locale}",
            status_code=302
        )
