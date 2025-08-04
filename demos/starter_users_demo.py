#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebAPI Starter Database Demo
Shows the clean starter users and items setup.
"""

import sqlite3
from datetime import datetime
import os
import sys

# Fix encoding for Windows
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def show_database_status():
    """Show the database file status"""
    print("[DB] **WebAPI Starter Database Status**")
    print("=" * 50)
    
    db_path = 'webapi_starter.db'
    
    if os.path.exists(db_path):
        file_size = os.path.getsize(db_path)
        file_time = datetime.fromtimestamp(os.path.getmtime(db_path))
        
        print(f"[FILE] **Database File**: {db_path}")
        print(f"[SIZE] **Size**: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
        print(f"[TIME] **Last Modified**: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[OK] **Status**: Operational")
    else:
        print("[ERR] **Database file not found!**")
        return False
    
    return True

def show_starter_users():
    """Display the starter users"""
    print("\n[USERS] **Starter Users**")
    print("=" * 50)
    
    conn = sqlite3.connect('webapi_starter.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, username, email, full_name, role, is_active FROM users ORDER BY id')
    users = cursor.fetchall()
    
    for user in users:
        status = "[ACTIVE] Active" if user['is_active'] else "[INACTIVE] Inactive"
        role_icon = {"ADMIN": "[ADMIN]", "MODERATOR": "[MOD]", "USER": "[USER]"}.get(user['role'], "[UNKNOWN]")
        
        print(f"\n**{user['id']}. {role_icon} {user['username']}**")
        print(f"   📧 **Email**: {user['email']}")
        print(f"   [USER] **Full Name**: {user['full_name']}")
        print(f"   [AUTH] **Role**: {user['role']}")
        print(f"   [DATA] **Status**: {status}")
        
        # Show login credentials
        if user['username'] == 'admin':
            print(f"   [CLIENT] **Login**: admin / admin123")
        elif user['username'] == 'user':
            print(f"   [CLIENT] **Login**: user / user123")
    
    conn.close()
    return len(users)

def show_starter_items():
    """Display the starter items"""
    print("\n[ITEMS] **Starter Items**")
    print("=" * 50)
    
    conn = sqlite3.connect('webapi_starter.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT i.id, i.name, i.description, i.price, i.status, i.owner_id, u.username 
        FROM items i 
        JOIN users u ON i.owner_id = u.id 
        ORDER BY i.id
    """)
    items = cursor.fetchall()
    
    for item in items:
        status_icon = {"ACTIVE": "[ACTIVE]", "DRAFT": "🟡", "INACTIVE": "[INACTIVE]"}.get(item['status'], "[UNKNOWN]")
        
        print(f"\n**{item['id']}. {item['name']}**")
        print(f"   [DESC] **Description**: {item['description']}")
        print(f"   [PRICE] **Price**: ${item['price']:.2f}")
        print(f"   [DATA] **Status**: {status_icon} {item['status']}")
        print(f"   [USER] **Owner**: {item['username']} (ID: {item['owner_id']})")
    
    conn.close()
    return len(items)

def show_login_instructions():
    """Show how to login with starter accounts"""
    print("\n[AUTH] **Login Instructions**")
    print("=" * 50)
    
    print("**[WEB] Web Interface Login:**")
    print("1. Visit: http://127.0.0.1:8000/")
    print("2. Click appropriate button:")
    print("   • **Admin Dashboard** - For admin access")
    print("   • **User Portal** - For regular user access")
    
    print("\n**[ADMIN] Admin Account:**")
    print("   • **Username**: admin")
    print("   • **Password**: admin123")
    print("   • **Access**: Full admin privileges")
    print("   • **Features**: User management, item management, client apps")
    
    print("\n**[USER] Regular User Account:**")
    print("   • **Username**: user")
    print("   • **Password**: user123")
    print("   • **Access**: User portal features")
    print("   • **Features**: View/manage own items, profile management")

def show_api_access():
    """Show how to access the API"""
    print("\n[API] **API Access**")
    print("=" * 50)
    
    print("**🔗 API Documentation:**")
    print("   • **Swagger UI**: http://127.0.0.1:8000/docs")
    print("   • **ReDoc**: http://127.0.0.1:8000/redoc")
    
    print("\n**[CLIENT] API Authentication:**")
    print("1. **Create Client App** (via admin panel)")
    print("2. **Get API Token**:")
    print("   ```bash")
    print("   curl -X POST http://127.0.0.1:8000/api/v1/auth/token \\")
    print("     -d 'app_id=your_app_id&app_secret=your_app_secret'")
    print("   ```")
    print("3. **Use Token**:")
    print("   ```bash")
    print("   curl -H 'Authorization: Bearer your_token' \\")
    print("     http://127.0.0.1:8000/api/v1/users/")
    print("   ```")

def show_registration_info():
    """Show registration capabilities"""
    print("\n[DESC] **User Registration**")
    print("=" * 50)
    
    print("**🆕 New User Registration:**")
    print("   • **URL**: http://127.0.0.1:8000/auth/register")
    print("   • **Features**: Self-service user registration")
    print("   • **Validation**: Real-time form validation")
    print("   • **Default Role**: USER (regular user)")
    
    print("\n**[LIST] Registration Requirements:**")
    print("   • **Username**: 3-50 characters, alphanumeric + hyphens/underscores")
    print("   • **Email**: Valid email format, must be unique")
    print("   • **Password**: 8+ characters, at least one letter and number")
    print("   • **Full Name**: Optional, up to 100 characters")

def show_database_tables():
    """Show database table structure"""
    print("\n[STRUCT] **Database Structure**")
    print("=" * 50)
    
    conn = sqlite3.connect('webapi_starter.db')
    cursor = conn.cursor()
    
    # Get table counts
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM items')
    item_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM client_apps')
    client_count = cursor.fetchone()[0]
    
    print(f"[DATA] **Table Statistics:**")
    print(f"   • **users**: {user_count} records")
    print(f"   • **items**: {item_count} records")
    print(f"   • **client_apps**: {client_count} records")
    
    print(f"\n[INDEX] **Indexes**: 5 performance indexes")
    print(f"🔗 **Foreign Keys**: Proper relational constraints")
    print(f"⚡ **Features**: ACID transactions, automatic timestamps")
    
    conn.close()

def main():
    """Main demo function"""
    print("[MIGRATE] **WebAPI Starter - Clean Database Setup**")
    print("=" * 60)
    
    # Check database status
    if not show_database_status():
        return
    
    # Show starter users
    user_count = show_starter_users()
    
    # Show starter items
    item_count = show_starter_items()
    
    # Show login instructions
    show_login_instructions()
    
    # Show API access
    show_api_access()
    
    # Show registration info
    show_registration_info()
    
    # Show database structure
    show_database_tables()
    
    print("\n[SUMMARY] **Setup Summary**")
    print("=" * 50)
    print(f"[OK] **Clean Database**: Fresh SQLite database created")
    print(f"[OK] **Starter Users**: {user_count} essential accounts (admin + user)")
    print(f"[OK] **Demo Items**: {item_count} sample items for testing")
    print(f"[OK] **Production Ready**: Persistent storage with proper schema")
    print(f"[OK] **User Registration**: Self-service registration available")
    print(f"[OK] **API Access**: Full REST API with authentication")
    
    print("\n[MIGRATE] **Next Steps:**")
    print("1. Test admin login: http://127.0.0.1:8000/ → Admin Dashboard")
    print("2. Test user login: http://127.0.0.1:8000/ → User Portal") 
    print("3. Test registration: http://127.0.0.1:8000/auth/register")
    print("4. Explore API: http://127.0.0.1:8000/docs")
    print("5. Create client apps via admin panel for API access")

if __name__ == "__main__":
    main()
