"""
SQLite Database Module
This module handles SQLite database operations and provides persistent data storage.
"""

import sqlite3
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
import secrets
import string
from contextlib import contextmanager
from .models import User, Item, UserCreate, ItemCreate, UserUpdate, ItemUpdate, UserRole, ItemStatus, ClientAppCreate, ClientAppUpdate

# Database configuration
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'webapi_starter.db')

# Ensure database directory exists
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_database():
    """Initialize the SQLite database with tables"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                full_name TEXT,
                role TEXT NOT NULL DEFAULT 'USER',
                hashed_password TEXT NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')
        
        # Create items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL,
                status TEXT NOT NULL DEFAULT 'DRAFT',
                owner_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users (id)
            )
        ''')
        
        # Create client_apps table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_apps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                app_id TEXT UNIQUE NOT NULL,
                app_secret TEXT NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT 1,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_items_owner ON items(owner_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_items_status ON items(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_client_apps_app_id ON client_apps(app_id)')

def init_sample_data():
    """Initialize the database with sample data"""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Check if we already have users
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] > 0:
            return  # Sample data already exists
        
        # Insert sample users
        sample_users = [
            ('admin', 'admin@example.com', 'Administrator', 'ADMIN', pwd_context.hash('admin123')),
            ('john_doe', 'john@example.com', 'John Doe', 'USER', pwd_context.hash('user123')),
            ('jane_smith', 'jane@example.com', 'Jane Smith', 'MODERATOR', pwd_context.hash('jane123'))
        ]
        
        cursor.executemany('''
            INSERT INTO users (username, email, full_name, role, hashed_password)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_users)
        
        # Insert sample items
        sample_items = [
            ('Laptop', 'High-performance laptop for development', 1299.99, 'ACTIVE', 2),
            ('Smartphone', 'Latest smartphone with great camera', 899.99, 'ACTIVE', 2),
            ('Book', 'Programming book for Python developers', 49.99, 'DRAFT', 3)
        ]
        
        cursor.executemany('''
            INSERT INTO items (name, description, price, status, owner_id)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_items)

def row_to_dict(row) -> Dict[str, Any]:
    """Convert SQLite Row to dictionary"""
    if row is None:
        return None
    return dict(row)

class SQLiteUserCRUD:
    """SQLite-based User CRUD operations"""
    
    def create_user(self, user: UserCreate) -> Dict[str, Any]:
        """Create a new user"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, email, full_name, role, hashed_password)
                VALUES (?, ?, ?, ?, ?)
            ''', (user.username, user.email, user.full_name, user.role.value, user.hashed_password))
            
            user_id = cursor.lastrowid
            return self.get_user(user_id)
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            return row_to_dict(row) if row else None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            return row_to_dict(row) if row else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            row = cursor.fetchone()
            return row_to_dict(row) if row else None
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get list of users with pagination"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users ORDER BY id LIMIT ? OFFSET ?', (limit, skip))
            rows = cursor.fetchall()
            return [row_to_dict(row) for row in rows]
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[Dict[str, Any]]:
        """Update an existing user"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Build dynamic update query
            update_fields = []
            values = []
            
            if user_update.email is not None:
                update_fields.append('email = ?')
                values.append(user_update.email)
            if user_update.full_name is not None:
                update_fields.append('full_name = ?')
                values.append(user_update.full_name)
            if user_update.role is not None:
                update_fields.append('role = ?')
                values.append(user_update.role.value)
            if user_update.is_active is not None:
                update_fields.append('is_active = ?')
                values.append(user_update.is_active)
            if user_update.hashed_password is not None:
                update_fields.append('hashed_password = ?')
                values.append(user_update.hashed_password)
            
            if not update_fields:
                return self.get_user(user_id)
            
            update_fields.append('updated_at = CURRENT_TIMESTAMP')
            values.append(user_id)
            
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, values)
            
            if cursor.rowcount == 0:
                return None
            
            return self.get_user(user_id)
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            return cursor.rowcount > 0

class SQLiteItemCRUD:
    """SQLite-based Item CRUD operations"""
    
    def create_item(self, item: ItemCreate, owner_id: int) -> Dict[str, Any]:
        """Create a new item"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO items (name, description, price, status, owner_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (item.name, item.description, item.price, item.status.value, owner_id))
            
            item_id = cursor.lastrowid
            return self.get_item(item_id)
    
    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Get item by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
            row = cursor.fetchone()
            return row_to_dict(row) if row else None
    
    def get_items(self, skip: int = 0, limit: int = 100, owner_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get list of items with pagination"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if owner_id:
                cursor.execute('SELECT * FROM items WHERE owner_id = ? ORDER BY id LIMIT ? OFFSET ?', 
                             (owner_id, limit, skip))
            else:
                cursor.execute('SELECT * FROM items ORDER BY id LIMIT ? OFFSET ?', (limit, skip))
            
            rows = cursor.fetchall()
            return [row_to_dict(row) for row in rows]
    
    def update_item(self, item_id: int, item_update: ItemUpdate) -> Optional[Dict[str, Any]]:
        """Update an existing item"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Build dynamic update query
            update_fields = []
            values = []
            
            if item_update.name is not None:
                update_fields.append('name = ?')
                values.append(item_update.name)
            if item_update.description is not None:
                update_fields.append('description = ?')
                values.append(item_update.description)
            if item_update.price is not None:
                update_fields.append('price = ?')
                values.append(item_update.price)
            if item_update.status is not None:
                update_fields.append('status = ?')
                values.append(item_update.status.value)
            if item_update.owner_id is not None:
                update_fields.append('owner_id = ?')
                values.append(item_update.owner_id)
            
            if not update_fields:
                return self.get_item(item_id)
            
            update_fields.append('updated_at = CURRENT_TIMESTAMP')
            values.append(item_id)
            
            query = f"UPDATE items SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, values)
            
            if cursor.rowcount == 0:
                return None
            
            return self.get_item(item_id)
    
    def delete_item(self, item_id: int) -> bool:
        """Delete an item"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
            return cursor.rowcount > 0

class SQLiteClientAppCRUD:
    """SQLite-based Client App CRUD operations"""
    
    def generate_app_credentials(self) -> tuple[str, str]:
        """Generate unique app_id and app_secret"""
        app_id = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        app_secret = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(32))
        return app_id, app_secret
    
    def create_client_app(self, client_app: ClientAppCreate, created_by: int) -> Dict[str, Any]:
        """Create a new client application"""
        app_id, app_secret = self.generate_app_credentials()
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO client_apps (name, description, app_id, app_secret, created_by)
                VALUES (?, ?, ?, ?, ?)
            ''', (client_app.name, client_app.description, app_id, app_secret, created_by))
            
            client_app_id = cursor.lastrowid
            return self.get_client_app(client_app_id)
    
    def get_client_app(self, client_app_id: int) -> Optional[Dict[str, Any]]:
        """Get client app by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM client_apps WHERE id = ?', (client_app_id,))
            row = cursor.fetchone()
            return row_to_dict(row) if row else None
    
    def get_client_app_by_app_id(self, app_id: str) -> Optional[Dict[str, Any]]:
        """Get client app by app_id"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM client_apps WHERE app_id = ?', (app_id,))
            row = cursor.fetchone()
            return row_to_dict(row) if row else None
    
    def get_client_apps(self, skip: int = 0, limit: int = 100, created_by: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get list of client apps with pagination"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if created_by:
                cursor.execute('SELECT * FROM client_apps WHERE created_by = ? ORDER BY id LIMIT ? OFFSET ?', 
                             (created_by, limit, skip))
            else:
                cursor.execute('SELECT * FROM client_apps ORDER BY id LIMIT ? OFFSET ?', (limit, skip))
            
            rows = cursor.fetchall()
            return [row_to_dict(row) for row in rows]
    
    def update_client_app(self, client_app_id: int, client_app_update: ClientAppUpdate) -> Optional[Dict[str, Any]]:
        """Update an existing client app"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Build dynamic update query
            update_fields = []
            values = []
            
            if client_app_update.name is not None:
                update_fields.append('name = ?')
                values.append(client_app_update.name)
            if client_app_update.description is not None:
                update_fields.append('description = ?')
                values.append(client_app_update.description)
            if client_app_update.is_active is not None:
                update_fields.append('is_active = ?')
                values.append(client_app_update.is_active)
            
            if not update_fields:
                return self.get_client_app(client_app_id)
            
            update_fields.append('updated_at = CURRENT_TIMESTAMP')
            values.append(client_app_id)
            
            query = f"UPDATE client_apps SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, values)
            
            if cursor.rowcount == 0:
                return None
            
            return self.get_client_app(client_app_id)
    
    def delete_client_app(self, client_app_id: int) -> bool:
        """Delete a client app"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM client_apps WHERE id = ?', (client_app_id,))
            return cursor.rowcount > 0

# Initialize database instances
def get_db():
    """Get database connection (for dependency injection)"""
    return get_db_connection()

# Create CRUD instances
user_crud = SQLiteUserCRUD()
item_crud = SQLiteItemCRUD()
client_app_crud = SQLiteClientAppCRUD()

# Initialize database and sample data on module load
def initialize_sqlite_database():
    """Initialize the SQLite database and sample data"""
    init_database()
    init_sample_data()

# Call initialization
initialize_sqlite_database()
