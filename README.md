# 🚀 WebAPI Starter Template

**Your Web API Project Foundation**

A ready-to-use starter template for building professional web APIs with modern Python frameworks. Clone this project and start building immediately with pre-configured authentication, admin dashboard, user management, CRUD operations, and comprehensive documentation - all the boilerplate code you need to launch your next web application.

## 🎯 Why Use This Starter Template?

This template saves you weeks of development time by providing:

- ✅ **Complete Auth System** - JWT tokens, session management, role-based access control
- ✅ **Ready-Made Admin Panel** - User management, item management, system monitoring
- ✅ **CRUD Boilerplate** - Pre-built Create, Read, Update, Delete operations
- ✅ **API Structure Ready** - Well-organized project with best practices
- ✅ **UI Templates Included** - Professional responsive HTML templates
- ✅ **Production Patterns** - Error handling, validation, documentation

**Perfect for:** API-first applications, admin dashboards, SaaS backends, microservices, MVPs

## 🚀 Quick Start

1. **Clone and setup:**
   ```bash
   git clone <your-repo-url>
   cd webapi-starter
   pip install -r requirements.txt
   ```

2. **Start developing:**
   ```bash
   python main.py
   ```

3. **Explore what's included:**
   - 🏠 **Landing Page**: http://127.0.0.1:8000
   - 🛠️ **Admin Dashboard**: http://127.0.0.1:8000/admin
   - 📚 **API Docs**: http://127.0.0.1:8000/docs
   - 👤 **User Portal**: http://127.0.0.1:8000/user/search

## ✨ What's Included

### �️ Ready-Made Admin Panel
- Complete web-based administration interface
- User management with role-based access control
- Item management with status tracking
- System monitoring and statistics dashboard
- Beautiful responsive design ready to customize

### ⚡ Modern Framework Foundation  
- Modern, fast web framework with async/await
- Automatic API documentation (OpenAPI/Swagger)
- Built-in data validation with Pydantic
- High performance and scalability ready
- **🌍 Multi-Language Support (i18n)** - English, Spanish, French, German

### 🔒 Auth System Included
- JWT-based authentication with session management
- Password hashing and security best practices
- Role-based permissions (Admin, User, Moderator)
- No need to build authentication from scratch
- **Localized error messages** in multiple languages

### 📊 CRUD Boilerplate
- Pre-implemented Create, Read, Update, Delete operations
- Database models with validation and error handling
- Use as-is or extend for your custom data types
- Pagination and filtering built-in

### 🌐 API Structure Ready
- Well-organized project structure
- Automatic OpenAPI documentation generation
- CORS configuration and standardized responses
- Follow established patterns for consistency

### 📱 UI Templates Included
- Professional responsive HTML templates
- Forms, dashboards, and user interfaces
- Modern CSS styling with animations
- Perfect starting point for your frontend

### 🧪 Testing & Demos Ready
- Comprehensive test suite with 24+ test files
- Demo scripts and utilities for learning
- Documentation and usage guides
- Development tools and debugging utilities

## 📁 Template Structure

This starter template is organized for immediate productivity:

```
webapi-starter/
├── main.py              # 🚀 Main application entry point
├── config.py            # ⚙️ Configuration management
├── auth.py              # 🔐 Session-based authentication
├── api_auth.py          # 🔑 JWT API authentication
├── html_errors.py       # 🚨 HTML error handling system
├── requirements.txt     # 📦 Python dependencies
├── data/               # 🗄️ Data access layer
│   ├── models.py       # 📝 Pydantic models and schemas
│   ├── database.py     # 💾 Database operations and CRUD
│   └── README.md       # 📚 Data layer documentation
├── routers/            # �️ API route modules
│   ├── users.py        # 👥 User-related endpoints
│   ├── items.py        # 📦 Item-related endpoints
│   └── admin.py        # 🛠️ Admin interface endpoints
├── templates/          # 🎨 HTML templates
│   ├── base.html       # 🏗️ Base template with navigation
│   ├── landing.html    # 🏠 Welcome page
│   ├── admin/          # 🛠️ Admin interface templates
│   ├── auth/           # 🔐 Authentication templates
│   └── user/           # 👤 User portal templates
├── tests/              # 🧪 Comprehensive test suite
│   ├── test_*.py       # ✅ Individual test files (24+)
│   └── README.md       # 📋 Test documentation
├── demos/              # 🎯 Demo scripts and utilities
│   ├── *_demo.py       # 🎪 Demo scripts for learning
│   ├── debug_*.py      # 🔧 Debug utilities
│   └── README.md       # 📖 Demo documentation
└── docs/               # 📚 Documentation and guides
    ├── API_TOKEN_USAGE_GUIDE.md
    ├── SWAGGER_AUTHENTICATION_GUIDE.md
    └── *.md            # 📄 Additional guides
│   └── item_detail.html # Item detail page
├── routers/            # API route modules
│   ├── __init__.py
│   ├── users.py        # User-related endpoints
│   ├── items.py        # Item-related endpoints
│   └── admin.py        # Admin interface endpoints
├── tests/              # 🧪 Test suite (24 test files)
│   ├── README.md       # Test documentation
│   ├── __init__.py     # Test package init
│   ├── test_*.py       # Individual test files
│   └── ...
├── demos/              # 🎯 Demo scripts and utilities (22 files)
│   ├── README.md       # Demo documentation
│   ├── __init__.py     # Demo package init
│   ├── *_demo.py       # Demo scripts
│   ├── debug_*.py      # Debug utilities
│   ├── *.html          # Sample files
│   └── ...
├── run_tests.py        # Test runner script
├── run_demos.py        # Demo runner script
└── README.md           # This file
```

```

## 🛠️ Customization Guide

### 1. **Add Your Own Data Models**
```python
# In data/models.py - Add your custom models
class Product(BaseModel):
    name: str
    category: str
    price: float
    
# In data/database.py - Add CRUD operations
class ProductCRUD:
    def create_product(self, product: Product): ...
```

### 2. **Extend the Admin Interface**
```python
# In routers/admin.py - Add new admin pages
@router.get("/products")
async def admin_products_list(request: Request):
    # Your product management page
```

### 3. **Add New API Endpoints**
```python
# Create routers/products.py
@router.post("/api/v1/products/")
async def create_product(product: ProductCreate):
    # Your API logic here
```

### 4. **Customize Authentication**
```python
# In auth.py - Modify authentication logic
# In api_auth.py - Customize JWT handling
```

### 5. **Update Templates**
```html
<!-- Customize templates/admin/ for your needs -->
<!-- Add new pages, modify styling, add features -->
```

## 🏃‍♂️ Getting Started

### Step 1: Clone and Setup
```bash
# Clone this starter template
git clone <your-repo-url>
cd webapi-starter

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Start Development Server
```bash
# Option 1: Use the main script
python main.py

# Option 2: Use uvicorn directly
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Step 3: Explore Your New Foundation
Visit these URLs to see what's ready for you:

- 🏠 **Welcome Page**: http://127.0.0.1:8000
- 🛠️ **Admin Dashboard**: http://127.0.0.1:8000/admin  
- 👤 **User Portal**: http://127.0.0.1:8000/user/search
- 📚 **API Documentation**: http://127.0.0.1:8000/docs
- 📖 **ReDoc**: http://127.0.0.1:8000/redoc
- ⚕️ **Health Check**: http://127.0.0.1:8000/health

### Step 4: Start Building Your Features
1. **Add your data models** in `data/models.py`
2. **Create CRUD operations** in `data/database.py`  
3. **Build API endpoints** in `routers/`
4. **Customize admin interface** in `templates/admin/`
5. **Add your business logic**

## 🎯 What You Get Out of the Box

### 🛠️ Pre-Built Admin Dashboard
Complete administration interface with:
- **User Management**: Create, edit, activate/deactivate users
- **Item Management**: Full CRUD operations with status tracking  
- **Role-Based Access**: Admin, User, Moderator permissions
- **Statistics Dashboard**: System overview and monitoring
- **Responsive Design**: Works on all devices

### 👥 Sample Users Ready to Use
- **admin** / **admin123** (Administrator access)
- **john_doe** / **password123** (Regular user)  
- **jane_smith** / **password123** (Moderator)

### 📦 Sample Data Included
- Pre-loaded users and items for immediate testing
- Realistic data relationships and examples
- Easy to replace with your own data

### 🔐 Complete Authentication System
- **Session-based auth** for web interface
- **JWT tokens** for API access
- **Password hashing** with bcrypt
- **Role-based permissions** throughout the app

### 📚 Automatic API Documentation
- **Swagger UI** at `/docs` - interactive API explorer
- **ReDoc** at `/redoc` - beautiful documentation
- **OpenAPI schema** - fully documented endpoints
- **Authentication integrated** - test APIs directly

## 🔧 Development Features

### 🧪 Testing & Quality
- **24+ Test Files**: Comprehensive test coverage
- **Test Categories**: Auth, API, UI, Admin, Data management
- **Demo Scripts**: 22+ demo files for learning and testing
- **Type Safety**: Full type hints with Pydantic validation
- **Error Handling**: Robust error handling throughout

### 📁 Clean Architecture
- **Modular Structure**: Organized routers, models, templates
- **Separation of Concerns**: Clear data layer, business logic, presentation
- **Best Practices**: Following modern Python web development conventions
- **Scalable Foundation**: Easy to extend and maintain

### 🚀 Production Ready Features
- **CORS Configuration**: Cross-origin support
- **Health Checks**: Monitoring endpoints
- **Error Pages**: User-friendly error handling
- **Security**: Password hashing, JWT tokens, input validation
- **Performance**: Async/await patterns throughout
- **🌍 Internationalization**: Full i18n support for global applications

## 📖 API Reference

### 🌍 Internationalization API

- `GET /api/v1/i18n/locales` - Get supported locales
- `GET /api/v1/i18n/translations/{locale}` - Get all translations for a locale
- `GET /api/v1/i18n/translate/{key}?lang={locale}` - Translate a specific key

**Multi-Language Support:**
- **English (en)** - Default
- **Spanish (es)** - Español  
- **French (fr)** - Français
- **German (de)** - Deutsch

**Usage Examples:**
```bash
# Get Spanish translations
curl "http://localhost:8000/api/v1/i18n/translations/es"

# Translate with URL parameter
curl "http://localhost:8000/api/v1/i18n/translate/users.user_not_found?lang=fr"

# Automatic detection via Accept-Language header
curl -H "Accept-Language: de-DE,de;q=0.9" "http://localhost:8000/api/v1/users/999"
```

### Users API

- `GET /api/v1/users/` - Get all users (with pagination)
- `GET /api/v1/users/{user_id}` - Get user by ID
- `GET /api/v1/users/username/{username}` - Get user by username
- `GET /api/v1/users/email/{email}` - Get user by email
- `POST /api/v1/users/` - Create a new user
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Items API

- `GET /api/v1/items/` - Get all items (with pagination and filtering)
- `GET /api/v1/items/{item_id}` - Get item by ID
- `GET /api/v1/items/owner/{owner_id}` - Get items by owner
- `GET /api/v1/items/status/{status}` - Get items by status
- `POST /api/v1/items/` - Create a new item
- `PUT /api/v1/items/{item_id}` - Update item
- `PATCH /api/v1/items/{item_id}/status` - Update item status only
- `DELETE /api/v1/items/{item_id}` - Delete item

### General Endpoints

- `GET /` - Application home page
- `GET /health` - Health check endpoint
- `GET /info` - Application information

## Sample Data

The application comes with sample data including:

### Users:
- **admin** (Administrator)
- **john_doe** (Regular User)
- **jane_smith** (Moderator)

### Items:
- **Laptop** (owned by john_doe)
- **Smartphone** (owned by john_doe)
- **Book** (owned by jane_smith)

## Usage Examples

### Create a New User

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "newuser",
       "email": "newuser@example.com",
       "password": "securepassword",
       "full_name": "New User",
       "role": "user"
     }'
```

### Create a New Item

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/items/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "New Product",
       "description": "A great new product",
       "price": 99.99,
       "status": "active",
       "owner_id": 2
     }'
```

### Get Users with Pagination

```bash
curl "http://127.0.0.1:8000/api/v1/users/?skip=0&limit=10"
```

### Filter Items by Status

```bash
curl "http://127.0.0.1:8000/api/v1/items/?status=active"
```

## Data Models

### User Model
- `id`: Unique identifier
- `username`: Unique username (3-50 characters)
- `email`: Valid email address
- `full_name`: Optional full name
- `role`: User role (admin, user, moderator)
- `is_active`: Whether the user is active
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Item Model
- `id`: Unique identifier
- `name`: Item name (1-100 characters)
- `description`: Optional description
- `price`: Item price (must be > 0)
- `status`: Item status (active, inactive, draft)
- `owner_id`: ID of the owning user
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Development

This application uses:
- **FastAPI**: For the web framework
- **Pydantic**: For data validation and serialization
- **Uvicorn**: As the ASGI server
- **Type Hints**: For better code quality and IDE support

### Data Layer Architecture

The application features a clean data access layer in the `data/` directory:
- **`data/models.py`**: All Pydantic models and validation schemas
- **`data/database.py`**: CRUD operations and mock database storage
- **`data/__init__.py`**: Convenient imports for the entire data layer

This structure provides type safety, clear separation of concerns, and easy migration path to real databases.

```python
# Clean imports from the data layer
from data import User, UserCreate, user_crud, get_db
```

## Testing

The application includes a comprehensive test suite organized in the `tests/` directory:

### Running Tests

**List all available tests:**
```bash
python run_tests.py --list
```

**Run a specific test:**
```bash
python run_tests.py --test test_authorization_errors.py
```

**Run tests by category:**
```bash
python run_tests.py --category auth    # Authentication tests
python run_tests.py --category api     # API tests
python run_tests.py --category ui      # UI tests
python run_tests.py --category admin   # Admin tests
python run_tests.py --category data    # Data management tests
```

**Run all tests:**
```bash
python run_tests.py --all
```

### Test Categories

- **🔐 Authentication & Authorization**: Login, session management, access control
- **🔧 API Tests**: Endpoint functionality, error handling, edge cases
- **👥 User Interface**: Web UI functionality, redirects, user experience
- **📊 Data Management**: CRUD operations, data validation
- **🎨 UI & Error Pages**: Error page display, user-friendly messages
- **🛠️ Admin Interface**: Admin panel functionality

See `tests/README.md` for detailed test documentation.

## Demos and Utilities

The application includes comprehensive demo scripts and utilities organized in the `demos/` directory:

### Running Demos

**List all available demos:**
```bash
python run_demos.py --list
```

**Run a specific demo:**
```bash
python run_demos.py --demo api_token_demo.py
```

**Run demos by category:**
```bash
python run_demos.py --category admin   # Admin interface demos
python run_demos.py --category auth    # Authentication demos
python run_demos.py --category tokens  # Token management demos
python run_demos.py --category debug   # Debugging utilities
python run_demos.py --category utils   # Development utilities
```

**Open sample files:**
```bash
python run_demos.py --open error_page_sample.html
```

### Demo Categories

- **🎯 Admin Interface**: Admin structure, user portal access demos
- **🔐 Authentication**: API tokens, login context, Swagger authentication
- **🔑 Token Management**: Token generation, credential management
- **🔧 Debugging Tools**: Auth debugging, client app troubleshooting
- **🛠️ Development Tools**: Utility scripts for development

See `demos/README.md` for detailed demo documentation.

## Documentation

The application includes comprehensive documentation organized in the `docs/` directory:

### Available Documentation

- **[API Token Usage Guide](docs/API_TOKEN_USAGE_GUIDE.md)**: Complete guide for JWT token authentication
- **[Swagger Authentication Guide](docs/SWAGGER_AUTHENTICATION_GUIDE.md)**: How to authenticate with Swagger UI
- **[How to Get Bearer Token](docs/HOW_TO_GET_BEARER_TOKEN.md)**: Step-by-step token acquisition
- **[Test Organization Summary](docs/TEST_ORGANIZATION_SUMMARY.md)**: Overview of test suite structure
- **[Demo Organization Summary](docs/DEMO_ORGANIZATION_SUMMARY.md)**: Overview of demo scripts organization

### Quick Start with Documentation

1. **For API Users**: Start with [How to Get Bearer Token](docs/HOW_TO_GET_BEARER_TOKEN.md)
2. **For Developers**: Review [API Token Usage Guide](docs/API_TOKEN_USAGE_GUIDE.md)
3. **For Testing**: Check [Test Organization Summary](docs/TEST_ORGANIZATION_SUMMARY.md)

See `docs/README.md` for complete documentation index.

## 🎯 Perfect For Building

This starter template is ideal for:

- **🚀 API-First Applications**: Microservices, backends, data APIs
- **🛠️ Admin Dashboards**: Management interfaces, internal tools
- **💼 SaaS Backends**: Multi-tenant applications, subscription services  
- **📱 Mobile App Backends**: User management, content APIs
- **🔧 Internal Tools**: Company dashboards, data management systems
- **📊 MVPs & Prototypes**: Quick validation of ideas with full features

## 🔮 Next Steps for Your Project

### Immediate Customizations
1. **Replace sample data** with your domain models
2. **Customize the admin interface** for your use case
3. **Add your business logic** to the API endpoints
4. **Update branding** and styling in templates
5. **Configure database** (PostgreSQL, MySQL, etc.)

### Advanced Features to Add
- **File upload** capabilities
- **Real-time features** with WebSockets
- **Background tasks** with Celery
- **Caching** with Redis
- **Email system** for notifications
- **Advanced permissions** and workflows
- **API rate limiting**
- **Logging and monitoring**
- **CI/CD pipeline**
- **Cloud deployment**

## 🛠️ Built With Modern Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation using Python type hints
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server  
- **[Jinja2](https://jinja.palletsprojects.com/)** - Modern templating for Python
- **[SQLite](https://www.sqlite.org/)** - Lightweight database (easily replaceable)
- **[JWT](https://jwt.io/)** - JSON Web Tokens for API authentication
- **[bcrypt](https://github.com/pyca/bcrypt/)** - Modern password hashing

## 📚 Learning Resources

### Documentation Included
- **[API Token Usage Guide](docs/API_TOKEN_USAGE_GUIDE.md)** - JWT authentication
- **[Swagger Authentication Guide](docs/SWAGGER_AUTHENTICATION_GUIDE.md)** - API testing
- **[Test Organization](docs/TEST_ORGANIZATION_SUMMARY.md)** - Understanding tests
- **[Demo Organization](docs/DEMO_ORGANIZATION_SUMMARY.md)** - Demo scripts

### Getting Help
- **Explore the `/demos` folder** for usage examples
- **Run the test suite** to understand functionality  
- **Check `/docs` folder** for detailed guides
- **Examine the code** - it's well-commented and organized

## 🤝 Contributing

This is a starter template - make it your own! 

When you build something amazing with this template:
- ⭐ Star this repository  
- 🍴 Fork it for your own projects
- 📢 Share what you built
- 🐛 Report any issues you find
- 💡 Suggest improvements

## 📄 License

This starter template is provided for educational and development purposes.
Use it as a foundation for your own projects - no attribution required!

---

## 🚀 Ready to Build?

```bash
# Clone this starter template and start building!
git clone <your-repo-url>
cd webapi-starter  
pip install -r requirements.txt
python main.py

# Your Web API foundation is ready! 🎉
```

**Happy coding!** 🎉 Build something amazing with your new Web API foundation.
