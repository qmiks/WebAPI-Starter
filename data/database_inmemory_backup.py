"""
Database Module
This module handles database operations and provides mock data storage.
In a real application, this would connect to a database like PostgreSQL, MySQL, etc.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import secrets
import string
from .models import User, Item, UserCreate, ItemCreate, UserUpdate, ItemUpdate, UserRole, ItemStatus, ClientAppCreate, ClientAppUpdate

# Mock database storage
users_db: List[Dict[str, Any]] = []
items_db: List[Dict[str, Any]] = []
client_apps_db: List[Dict[str, Any]] = []

# Counters for IDs
user_id_counter = 1
item_id_counter = 1
client_app_id_counter = 1

# Initialize with some sample data
def init_sample_data():
    """Initialize the database with sample data"""
    global user_id_counter, item_id_counter
    
    # Import password hashing function
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Sample users
    sample_users = [
        {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "full_name": "Administrator",
            "role": UserRole.ADMIN,
            "hashed_password": pwd_context.hash("admin123"),
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": None
        },
        {
            "id": 2,
            "username": "john_doe",
            "email": "john@example.com",
            "full_name": "John Doe",
            "role": UserRole.USER,
            "hashed_password": pwd_context.hash("user123"),
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": None
        },
        {
            "id": 3,
            "username": "jane_smith",
            "email": "jane@example.com",
            "full_name": "Jane Smith",
            "role": UserRole.MODERATOR,
            "hashed_password": pwd_context.hash("jane123"),
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": None
        }
    ]
    
    # Sample items
    sample_items = [
        {
            "id": 1,
            "name": "Laptop",
            "description": "High-performance laptop for development",
            "price": 1299.99,
            "status": ItemStatus.ACTIVE,
            "owner_id": 2,
            "created_at": datetime.now(),
            "updated_at": None
        },
        {
            "id": 2,
            "name": "Smartphone",
            "description": "Latest smartphone with great camera",
            "price": 899.99,
            "status": ItemStatus.ACTIVE,
            "owner_id": 2,
            "created_at": datetime.now(),
            "updated_at": None
        },
        {
            "id": 3,
            "name": "Book",
            "description": "Programming book for Python developers",
            "price": 49.99,
            "status": ItemStatus.DRAFT,
            "owner_id": 3,
            "created_at": datetime.now(),
            "updated_at": None
        }
    ]
    
    users_db.extend(sample_users)
    items_db.extend(sample_items)
    user_id_counter = 4
    item_id_counter = 4

# Initialize sample data
init_sample_data()

def get_db():
    """Dependency to get database session (mock)"""
    return {"users": users_db, "items": items_db, "client_apps": client_apps_db}

# Utility functions for client apps
def generate_app_id() -> str:
    """Generate a unique app ID"""
    return f"app_{''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(16))}"

def generate_app_secret() -> str:
    """Generate a secure app secret"""
    return secrets.token_urlsafe(32)

# User CRUD operations
class UserCRUD:
    @staticmethod
    def get_users(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all users with pagination"""
        return users_db[skip: skip + limit]
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        for user in users_db:
            if user["id"] == user_id:
                return user
        return None
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        for user in users_db:
            if user["username"] == username:
                return user
        return None
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        for user in users_db:
            if user["email"] == email:
                return user
        return None
    
    @staticmethod
    def create_user(user_data: UserCreate) -> Dict[str, Any]:
        """Create a new user"""
        global user_id_counter
        
        new_user = {
            "id": user_id_counter,
            "username": user_data.username,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "role": user_data.role,
            "is_active": user_data.is_active,
            "created_at": datetime.now(),
            "updated_at": None
        }
        
        users_db.append(new_user)
        user_id_counter += 1
        return new_user
    
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate) -> Optional[Dict[str, Any]]:
        """Update an existing user"""
        for i, user in enumerate(users_db):
            if user["id"] == user_id:
                update_data = user_data.dict(exclude_unset=True)
                for key, value in update_data.items():
                    users_db[i][key] = value
                users_db[i]["updated_at"] = datetime.now()
                return users_db[i]
        return None
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        """Delete a user"""
        for i, user in enumerate(users_db):
            if user["id"] == user_id:
                users_db.pop(i)
                return True
        return False

# Item CRUD operations
class ItemCRUD:
    @staticmethod
    def get_items(skip: int = 0, limit: int = 100, owner_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all items with pagination and optional owner filter"""
        items = items_db
        if owner_id:
            items = [item for item in items if item["owner_id"] == owner_id]
        return items[skip: skip + limit]
    
    @staticmethod
    def get_item_by_id(item_id: int) -> Optional[Dict[str, Any]]:
        """Get item by ID"""
        for item in items_db:
            if item["id"] == item_id:
                return item
        return None
    
    @staticmethod
    def create_item(item_data: ItemCreate) -> Dict[str, Any]:
        """Create a new item"""
        global item_id_counter
        
        new_item = {
            "id": item_id_counter,
            "name": item_data.name,
            "description": item_data.description,
            "price": item_data.price,
            "status": item_data.status,
            "owner_id": item_data.owner_id,
            "created_at": datetime.now(),
            "updated_at": None
        }
        
        items_db.append(new_item)
        item_id_counter += 1
        return new_item
    
    @staticmethod
    def update_item(item_id: int, item_data: ItemUpdate) -> Optional[Dict[str, Any]]:
        """Update an existing item"""
        for i, item in enumerate(items_db):
            if item["id"] == item_id:
                update_data = item_data.dict(exclude_unset=True)
                for key, value in update_data.items():
                    items_db[i][key] = value
                items_db[i]["updated_at"] = datetime.now()
                return items_db[i]
        return None
    
    @staticmethod
    def delete_item(item_id: int) -> bool:
        """Delete an item"""
        for i, item in enumerate(items_db):
            if item["id"] == item_id:
                items_db.pop(i)
                return True
        return False

# Create instances
user_crud = UserCRUD()
item_crud = ItemCRUD()

# Client App CRUD operations
class ClientAppCRUD:
    @staticmethod
    def get_client_apps(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all client apps with pagination"""
        return client_apps_db[skip: skip + limit]
    
    @staticmethod
    def get_client_app_by_id(app_id: int) -> Optional[Dict[str, Any]]:
        """Get client app by ID"""
        for app in client_apps_db:
            if app["id"] == app_id:
                return app
        return None
    
    @staticmethod
    def get_client_app_by_app_id(app_id: str) -> Optional[Dict[str, Any]]:
        """Get client app by app_id"""
        for app in client_apps_db:
            if app["app_id"] == app_id:
                return app
        return None
    
    @staticmethod
    def create_client_app(app_data: ClientAppCreate) -> Dict[str, Any]:
        """Create a new client app"""
        global client_app_id_counter
        
        new_app = {
            "id": client_app_id_counter,
            "name": app_data.name,
            "description": app_data.description,
            "app_id": generate_app_id(),
            "app_secret": generate_app_secret(),
            "is_active": app_data.is_active,
            "created_at": datetime.now(),
            "updated_at": None
        }
        
        client_apps_db.append(new_app)
        client_app_id_counter += 1
        return new_app
    
    @staticmethod
    def update_client_app(app_id: int, app_data: ClientAppUpdate) -> Optional[Dict[str, Any]]:
        """Update an existing client app"""
        for i, app in enumerate(client_apps_db):
            if app["id"] == app_id:
                update_data = app_data.dict(exclude_unset=True)
                for key, value in update_data.items():
                    client_apps_db[i][key] = value
                client_apps_db[i]["updated_at"] = datetime.now()
                return client_apps_db[i]
        return None
    
    @staticmethod
    def delete_client_app(app_id: int) -> bool:
        """Delete a client app"""
        for i, app in enumerate(client_apps_db):
            if app["id"] == app_id:
                client_apps_db.pop(i)
                return True
        return False
    
    @staticmethod
    def regenerate_secret(app_id: int) -> Optional[Dict[str, Any]]:
        """Regenerate app secret for a client app"""
        for i, app in enumerate(client_apps_db):
            if app["id"] == app_id:
                client_apps_db[i]["app_secret"] = generate_app_secret()
                client_apps_db[i]["updated_at"] = datetime.now()
                return client_apps_db[i]
        return None

# Create instances
client_app_crud = ClientAppCRUD()
