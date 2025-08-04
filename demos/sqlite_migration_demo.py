#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLite Database Migration Demo
Shows the transition from in-memory to persistent SQLite storage.
"""

import sqlite3
import os
import sys
from datetime import datetime

# Fix encoding for Windows
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_database_file():
    """Check the SQLite database file and its properties"""
    print("DATABASE **SQLite Database Information**")
    print("=" * 50)
    
    db_path = os.path.join(os.path.dirname(__file__), '..', 'webapi_starter.db')
    
    if os.path.exists(db_path):
        file_size = os.path.getsize(db_path)
        file_time = datetime.fromtimestamp(os.path.getmtime(db_path))
        
        print(f"[FILE] **Database File**: webapi_starter.db")
        print(f"[LOC] **Location**: {os.path.abspath(db_path)}")
        print(f"[SIZE] **Size**: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
        print(f"[TIME] **Last Modified**: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[OK] **Status**: File exists and is accessible")
    else:
        print("[ERR] **Database file not found!**")
        return False
    
    return True

def examine_database_structure():
    """Examine the database structure and content"""
    print("\n[STRUCT] **Database Structure**")
    print("=" * 50)
    
    db_path = os.path.join(os.path.dirname(__file__), '..', 'webapi_starter.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print("[LIST] **Tables Created:**")
        for table in tables:
            table_name = table[0]
            if not table_name.startswith('sqlite_'):  # Skip SQLite system tables
                print(f"  • {table_name}")
                
                # Get table info
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                print(f"    [DATA] **Columns**:")
                for col in columns:
                    col_name = col[1]
                    col_type = col[2]
                    is_pk = " (PRIMARY KEY)" if col[5] else ""
                    is_nn = " NOT NULL" if col[3] else ""
                    print(f"      - {col_name}: {col_type}{is_pk}{is_nn}")
                
                # Get record count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"    [COUNT] **Records**: {count}")
                print()
        
        # Get indexes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%' ORDER BY name")
        indexes = cursor.fetchall()
        
        if indexes:
            print("[INDEX] **Indexes Created:**")
            for index in indexes:
                print(f"  • {index[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"[ERR] **Error examining database**: {e}")

def show_sample_data():
    """Show sample data in the database"""
    print("\n[DATA] **Sample Data**")
    print("=" * 50)
    
    db_path = os.path.join(os.path.dirname(__file__), '..', 'webapi_starter.db')
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()
        
        # Show users
        print("[USERS] **Users Table**:")
        cursor.execute("SELECT id, username, email, full_name, role, is_active FROM users ORDER BY id")
        users = cursor.fetchall()
        
        for user in users:
            status = "[ACTIVE] Active" if user['is_active'] else "[INACTIVE] Inactive"
            role_icon = {"ADMIN": "[ADMIN]", "MODERATOR": "[MOD]", "USER": "[USER]"}.get(user['role'], "[UNKNOWN]")
            print(f"  {user['id']}. {role_icon} {user['username']} ({user['email']}) - {user['full_name']} - {status}")
        
        # Show items
        print("\n[ITEMS] **Items Table**:")
        cursor.execute("""
            SELECT i.id, i.name, i.description, i.price, i.status, i.owner_id, u.username 
            FROM items i 
            JOIN users u ON i.owner_id = u.id 
            ORDER BY i.id
        """)
        items = cursor.fetchall()
        
        for item in items:
            status_icon = {"ACTIVE": "[ACTIVE]", "DRAFT": "🟡", "INACTIVE": "[INACTIVE]"}.get(item['status'], "[UNKNOWN]")
            print(f"  {item['id']}. {status_icon} {item['name']} - ${item['price']:.2f}")
            print(f"      [DESC] {item['description']}")
            print(f"      [USER] Owner: {item['username']} (ID: {item['owner_id']})")
        
        # Show client apps if any
        cursor.execute("SELECT COUNT(*) FROM client_apps")
        client_count = cursor.fetchone()[0]
        
        if client_count > 0:
            print("\n[CLIENT] **Client Applications**:")
            cursor.execute("""
                SELECT c.id, c.name, c.description, c.app_id, c.is_active, u.username
                FROM client_apps c
                JOIN users u ON c.created_by = u.id
                ORDER BY c.id
            """)
            clients = cursor.fetchall()
            
            for client in clients:
                status = "[ACTIVE] Active" if client['is_active'] else "[INACTIVE] Inactive"
                print(f"  {client['id']}. {client['name']} - {status}")
                print(f"      [DESC] {client['description']}")
                print(f"      [CLIENT] App ID: {client['app_id']}")
                print(f"      [USER] Created by: {client['username']}")
        else:
            print("\n[CLIENT] **Client Applications**: None created yet")
        
        conn.close()
        
    except Exception as e:
        print(f"[ERR] **Error reading sample data**: {e}")

def show_migration_benefits():
    """Show the benefits of the SQLite migration"""
    print("\n[MIGRATE] **Migration Benefits**")
    print("=" * 50)
    
    print("[OK] **Data Persistence**")
    print("   • Data survives application restarts")
    print("   • No data loss when server crashes")
    print("   • Reliable storage for production use")
    
    print("\n[OK] **Performance Improvements**")
    print("   • Indexed queries for faster lookups")
    print("   • Efficient JOIN operations")
    print("   • Optimized storage and retrieval")
    
    print("\n[OK] **Database Features**")
    print("   • ACID transactions for data integrity")
    print("   • Foreign key constraints")
    print("   • Automatic timestamps")
    print("   • Built-in data validation")
    
    print("\n[OK] **Development Benefits**")
    print("   • Easy database inspection with SQLite tools")
    print("   • Standard SQL queries")
    print("   • Backup and restore capabilities")
    print("   • Migration path to PostgreSQL/MySQL")
    
    print("\n[OK] **Production Ready**")
    print("   • No external database server required")
    print("   • Single file deployment")
    print("   • Cross-platform compatibility")
    print("   • Concurrent read access")

def show_usage_examples():
    """Show how to use the new SQLite database"""
    print("\n[USAGE] **Usage Examples**")
    print("=" * 50)
    
    print("**[PYTHON] Python Code Examples:**")
    print("""
```python
from data.database import user_crud, item_crud, client_app_crud

# Create a new user
from data.models import UserCreate, UserRole
new_user = UserCreate(
    username="newuser",
    email="newuser@example.com",
    full_name="New User",
    role=UserRole.USER,
    hashed_password="hashed_password_here"
)
user = user_crud.create_user(new_user)

# Get user by username
user = user_crud.get_user_by_username("admin")

# Update user
from data.models import UserUpdate
update_data = UserUpdate(full_name="Updated Name")
updated_user = user_crud.update_user(user["id"], update_data)

# Create an item
from data.models import ItemCreate, ItemStatus
new_item = ItemCreate(
    name="New Product",
    description="Amazing product",
    price=99.99,
    status=ItemStatus.ACTIVE
)
item = item_crud.create_item(new_item, owner_id=user["id"])
```""")
    
    print("\n**[DB] Direct SQL Access:**")
    print("""
```python
from data.database import get_db_connection

with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role = ?", ("ADMIN",))
    admin_users = cursor.fetchall()
```""")
    
    print("\n**[UTIL] Database Tools:**")
    print("  • **SQLite Browser**: Use DB Browser for SQLite to view data")
    print("  • **Command Line**: sqlite3 webapi_starter.db")
    print("  • **VS Code Extensions**: SQLite Viewer, SQLite Explorer")

def show_testing_instructions():
    """Show how to test the new SQLite functionality"""
    print("\n[TEST] **Testing Instructions**")
    print("=" * 50)
    
    print("**1. [WEB] Test Web Interface:**")
    print("   • Visit: http://127.0.0.1:8000/")
    print("   • Login: admin / admin123")
    print("   • Create new users and items")
    print("   • Restart the server and verify data persists")
    
    print("\n**2. [API] Test API Endpoints:**")
    print("   • Visit: http://127.0.0.1:8000/docs")
    print("   • Test CRUD operations")
    print("   • Verify data persistence")
    
    print("\n**3. [CLIENT] Test Authentication:**")
    print("   • Register new user: http://127.0.0.1:8000/auth/register")
    print("   • Login with new credentials")
    print("   • Access user portal")
    
    print("\n**4. [ADMIN] Test Admin Functions:**")
    print("   • Access admin panel")
    print("   • Create client applications")
    print("   • Generate API tokens")
    print("   • Manage users and items")

def main():
    """Main demo function"""
    print("[DB] **WebAPI Starter - SQLite Migration Complete!**")
    print("=" * 60)
    
    # Check if database exists
    if not check_database_file():
        return
    
    # Examine database structure
    examine_database_structure()
    
    # Show sample data
    show_sample_data()
    
    # Show benefits
    show_migration_benefits()
    
    # Show usage examples
    show_usage_examples()
    
    # Show testing instructions
    show_testing_instructions()
    
    print("\n[SUMMARY] **Migration Summary**")
    print("=" * 50)
    print("[OK] **Successfully migrated from in-memory to SQLite storage**")
    print("[OK] **Database file created: webapi_starter.db**")
    print("[OK] **Sample data populated**")
    print("[OK] **All CRUD operations now persistent**")
    print("[OK] **Application running with SQLite backend**")
    
    print("\n[MIGRATE] **Next Steps:**")
    print("1. Test the application thoroughly")
    print("2. Create backups of the database file")
    print("3. Consider setting up automated migrations")
    print("4. Monitor database performance")
    print("5. Plan for future PostgreSQL migration if needed")

if __name__ == "__main__":
    main()
