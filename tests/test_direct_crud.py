#!/usr/bin/env python3
"""
Direct Database Test for Client Apps
"""

import sys
import os
sys.path.append('.')

from data.database import client_app_crud
from data.models import ClientAppCreate

def test_client_app_crud():
    """Test client app CRUD operations directly"""
    
    print("🚀 Testing Client App CRUD directly")
    print("=" * 50)
    
    try:
        # Test 1: List existing client apps
        print("📋 Getting existing client apps...")
        existing_apps = client_app_crud.get_client_apps()
        print(f"Found {len(existing_apps)} existing client apps")
        
        # Test 2: Create a new client app
        print("➕ Creating new client app...")
        app_data = ClientAppCreate(
            name="Direct Test App",
            description="Testing direct database access",
            is_active=True
        )
        
        # Debug the creation process
        print(f"App data: {app_data}")
        print(f"Created_by: 1")
        
        new_app = client_app_crud.create_client_app(app_data, 1)  # created_by admin (id=1)
        print(f"Create result: {new_app}")
        
        if new_app is None:
            print("❌ Creation failed - returned None")
            # Let's try to debug by checking what went wrong
            print("🔍 Checking if there's an admin user with id=1...")
            # Check if admin user exists
            from data.database import user_crud
            admin_user = user_crud.get_user(1)
            print(f"Admin user: {admin_user}")
            return False
        
        print(f"✅ Created client app: {new_app}")
        
        # Test 3: Get the created app
        print("🔍 Retrieving created app...")
        retrieved_app = client_app_crud.get_client_app(new_app['id'])
        print(f"✅ Retrieved app: {retrieved_app}")
        
        # Test 4: Test regenerate secret
        print("🔄 Testing secret regeneration...")
        updated_app = client_app_crud.regenerate_secret(new_app['id'])
        print(f"✅ Regenerated secret: {updated_app['app_secret'] != new_app['app_secret']}")
        
        # Test 5: Clean up - delete the test app
        print("🗑️ Cleaning up test app...")
        deleted = client_app_crud.delete_client_app(new_app['id'])
        print(f"✅ Deleted: {deleted}")
        
        print("✅ All direct CRUD operations successful!")
        return True
        
    except Exception as e:
        print(f"❌ Error during direct CRUD test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_client_app_crud()
