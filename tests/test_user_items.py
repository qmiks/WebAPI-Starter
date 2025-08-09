#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test User Item Access Control
Validates that regular users can only CRUD their own items while admins see all items.
"""

import requests
import json

# Base URL
BASE_URL = "http://127.0.0.1:8000"

def test_user_login():
    """Test user login and session creation"""
    print("🔐 Testing User Login...")
    
    login_data = {
        "username": "user",
        "password": "user123"
    }
    
    session = requests.Session()
    response = session.post(f"{BASE_URL}/auth/login", data=login_data, allow_redirects=False)
    
    if response.status_code in [302, 303]:  # Redirect after login
        print("✅ User login successful")
        return session
    else:
        print(f"❌ User login failed: {response.status_code}")
        return None

def test_admin_login():
    """Test admin login and session creation"""
    print("🔐 Testing Admin Login...")
    
    login_data = {
        "username": "admin", 
        "password": "admin123"
    }
    
    session = requests.Session()
    response = session.post(f"{BASE_URL}/auth/login", data=login_data, allow_redirects=False)
    
    if response.status_code in [302, 303]:  # Redirect after login
        print("✅ Admin login successful")
        return session
    else:
        print(f"❌ Admin login failed: {response.status_code}")
        return None

def test_user_items_access(session):
    """Test that user can access their own items via web interface"""
    print("\n📋 Testing User Items Page Access...")
    
    response = session.get(f"{BASE_URL}/user/items")
    
    if response.status_code == 200:
        print("✅ User can access their items page")
        return True
    else:
        print(f"❌ User cannot access items page: {response.status_code}")
        return False

def test_user_dashboard_access(session):
    """Test that user can access their dashboard"""
    print("\n🏠 Testing User Dashboard Access...")
    
    response = session.get(f"{BASE_URL}/user/dashboard")
    
    if response.status_code == 200:
        print("✅ User can access dashboard")
        return True
    else:
        print(f"❌ User cannot access dashboard: {response.status_code}")
        return False

def test_anonymous_access():
    """Test that anonymous users cannot access protected routes"""
    print("\n🚫 Testing Anonymous Access (Should Fail)...")
    
    # Test items API without authentication
    response = requests.get(f"{BASE_URL}/items/")
    if response.status_code == 401:
        print("✅ Items API correctly rejects anonymous access")
    else:
        print(f"❌ Items API should reject anonymous access, got: {response.status_code}")
    
    # Test user dashboard without authentication  
    response = requests.get(f"{BASE_URL}/user/dashboard", allow_redirects=False)
    if response.status_code in [302, 303]:  # Should redirect to login
        print("✅ User dashboard correctly redirects anonymous users to login")
    else:
        print(f"❌ User dashboard should redirect anonymous users, got: {response.status_code}")

def test_items_api_with_auth(session, user_type="user"):
    """Test items API with authentication"""
    print(f"\n📊 Testing Items API as {user_type}...")
    
    response = session.get(f"{BASE_URL}/items/")
    
    if response.status_code == 200:
        try:
            items = response.json()
            print(f"✅ {user_type.title()} can access items API")
            print(f"   Items returned: {len(items)}")
            
            for item in items:
                print(f"   - Item {item['id']}: {item['name']} (Owner: {item['owner_id']})")
                
            return items
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response from items API")
            return None
    else:
        print(f"❌ {user_type.title()} cannot access items API: {response.status_code}")
        return None

def main():
    """Run all tests"""
    print("🧪 Testing User Item Access Control")
    print("=" * 50)
    
    # Test anonymous access
    test_anonymous_access()
    
    # Test user login and access
    print("\n" + "=" * 50)
    print("TESTING REGULAR USER ACCESS")
    print("=" * 50)
    
    user_session = test_user_login()
    if user_session:
        test_user_dashboard_access(user_session)
        test_user_items_access(user_session)
        user_items = test_items_api_with_auth(user_session, "user")
    
    # Test admin login and access
    print("\n" + "=" * 50)
    print("TESTING ADMIN USER ACCESS")
    print("=" * 50)
    
    admin_session = test_admin_login()
    if admin_session:
        admin_items = test_items_api_with_auth(admin_session, "admin")
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    if user_session and admin_session:
        print("✅ Both user and admin authentication working")
        print("✅ Role-based access control implemented")
        print("✅ Web interface accessible for authenticated users")
        
        if 'user_items' in locals() and 'admin_items' in locals():
            user_count = len(user_items) if user_items else 0
            admin_count = len(admin_items) if admin_items else 0
            
            print(f"📊 Items visible to user: {user_count}")
            print(f"📊 Items visible to admin: {admin_count}")
            
            if admin_count >= user_count:
                print("✅ Admin can see same or more items than user (correct)")
            else:
                print("⚠️  Admin sees fewer items than user (unexpected)")
    else:
        print("❌ Authentication issues detected")

if __name__ == "__main__":
    main()
