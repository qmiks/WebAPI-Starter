"""
WebAPI Starter - Main Entry Point
This is the main # Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add internationalization middleware
app.add_middleware(LocaleMiddleware, i18n_instance=i18n)t starts the WebAPI Starter application.
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer
import uvicorn

from routers import users, items, admin, auth, user_portal, client_apps
from data.models import User, Item, UserCreate, ItemCreate
from data.database import get_db, user_crud, item_crud
from utils.i18n import LocaleMiddleware, i18n, get_locale_from_request, t, get_translations_for_locale

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Create FastAPI instance with enhanced security documentation
app = FastAPI(
    title="WebAPI Starter",
    description="""
    A comprehensive WebAPI Starter application with CRUD operations and API token authentication.
    
    ## Authentication
    
    This API uses **Bearer Token Authentication**. To access protected endpoints:
    
    1. **Get Client Credentials**: 
       - Login to admin panel: `/admin/client-apps/`
       - Create a new client application
       - Save your App ID and App Secret
    
    2. **Get Access Token**:
       - POST `/api/v1/auth/token`
       - Provide your `app_id` and `app_secret`
       - Receive a JWT token
    
    3. **Use Token**:
       - Click "Authorize" button below
       - Enter: `Bearer your_jwt_token_here`
       - Or add header: `Authorization: Bearer your_jwt_token_here`
    
    ## Example Token Request
    ```bash
    curl -X POST /api/v1/auth/token \\
      -d "app_id=your_app_id&app_secret=your_app_secret"
    ```
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")
app.include_router(auth.router)
app.include_router(user_portal.router)
app.include_router(admin.router)

# Include client apps routers
for router in client_apps.get_routers():
    app.include_router(router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root(request: Request, locale: str = Depends(get_locale_from_request)):
    """Landing page with application overview"""
    return templates.TemplateResponse("landing.html", {
        "request": request,
        "locale": locale,
        "t": lambda key, **kwargs: t(key, locale, **kwargs)
    })

# Internationalization endpoints
@app.get("/api/v1/i18n/translations/{locale}")
async def get_translations(locale: str):
    """Get all translations for a specific locale"""
    if locale not in i18n.supported_locales:
        raise HTTPException(status_code=404, detail=f"Locale '{locale}' not supported")
    
    return {
        "locale": locale,
        "translations": get_translations_for_locale(locale),
        "supported_locales": i18n.supported_locales
    }

@app.get("/api/v1/i18n/locales")
async def get_supported_locales():
    """Get list of supported locales"""
    return {
        "supported_locales": i18n.supported_locales,
        "default_locale": i18n.default_locale
    }

@app.get("/api/v1/i18n/translate/{key:path}")
async def translate_key(key: str, request: Request, lang: str = None):
    """Translate a specific key"""
    # Get locale from URL parameter, request state, or default
    if lang and lang in i18n.supported_locales:
        locale = lang
    else:
        locale = getattr(request.state, 'locale', i18n.default_locale)
    
    # Replace slashes with dots in URL path for key lookup
    key = key.replace('/', '.')
    
    return {
        "key": key,
        "locale": locale,
        "translation": t(key, locale)
    }

# User portal endpoint - redirect to user search
@app.get("/user-portal", response_class=HTMLResponse)
async def user_portal_redirect(request: Request):
    """User portal - redirects to user search page"""
    return RedirectResponse(url="/user/search", status_code=302)

# Legacy home page (for backward compatibility)
@app.get("/home", response_class=HTMLResponse)
async def legacy_home():
    """Legacy home endpoint with basic HTML response"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebAPI Starter</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #009688; text-align: center; }
            .links { text-align: center; margin-top: 30px; }
            .links a { display: inline-block; margin: 10px; padding: 10px 20px; background: #009688; color: white; text-decoration: none; border-radius: 5px; }
            .links a:hover { background: #00796b; }
            .features { margin-top: 30px; }
            .feature { background: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #009688; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Welcome to WebAPI Starter</h1>
            <p>This is a comprehensive WebAPI Starter application with the following features:</p>
            
            <div class="features">
                <div class="feature">
                    <strong>🛠️ Admin Panel:</strong> Web-based admin interface for user management
                </div>
                <div class="feature">
                    <strong>🧑‍💼 User Management:</strong> Complete CRUD operations for users
                </div>
                <div class="feature">
                    <strong>📦 Item Management:</strong> Full item management system
                </div>
                <div class="feature">
                    <strong>📖 API Documentation:</strong> Automatic OpenAPI documentation
                </div>
                <div class="feature">
                    <strong>🔒 Data Validation:</strong> Pydantic models for data validation
                </div>
                <div class="feature">
                    <strong>🌐 CORS Support:</strong> Cross-origin resource sharing enabled
                </div>
            </div>
            
            <div class="links">
                <a href="/admin">🛠️ Admin Panel</a>
                <a href="/docs">📚 API Documentation (Swagger)</a>
                <a href="/redoc">📋 ReDoc Documentation</a>
                <a href="/api/v1/users">👥 Users API</a>
                <a href="/api/v1/items">📦 Items API</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "WebAPI Starter is running successfully!",
        "version": "1.0.0"
    }

# Application info endpoint
@app.get("/info")
async def app_info():
    """Application information endpoint"""
    return {
        "app_name": "WebAPI Starter",
        "version": "1.0.0",
        "framework": "FastAPI",
        "python_version": "3.11+",
        "features": [
            "Admin Panel",
            "User Management",
            "Item Management", 
            "API Documentation",
            "Data Validation",
            "CORS Support"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
