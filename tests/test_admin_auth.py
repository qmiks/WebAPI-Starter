#!/usr/bin/env python3
"""
Test Admin Authentication and Routes
"""

import requests

BASE_URL = "http://127.0.0.1:8000"

def login_as_admin():
    """Login as admin and return session"""
    session = requests.Session()
    
    # Get login page first
    login_page = session.get(f"{BASE_URL}/auth/login")
    print(f"Login page status: {login_page.status_code}")
    
    # Submit login form
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    login_response = session.post(f"{BASE_URL}/auth/login", data=login_data, allow_redirects=False)
    print(f"Login response status: {login_response.status_code}")
    print(f"Login response headers: {dict(login_response.headers)}")
    
    return session

def test_admin_routes_with_auth():
    """Test admin routes with proper authentication"""
    print("🔐 Testing admin routes with authentication...")
    
    # Login first
    session = login_as_admin()
    
    routes_to_test = [
        "/admin",
        "/admin/users", 
        "/admin/users/new",
        "/admin/users/1",
        "/admin/items"
    ]
    
    for route in routes_to_test:
        print(f"\n🧪 Testing {route}")
        try:
            response = session.get(f"{BASE_URL}{route}")
            print(f"   Status: {response.status_code}")
            if response.status_code == 422:
                print(f"   Error: {response.text[:200]}...")
            elif response.status_code == 200:
                print("   ✅ Success")
            else:
                print(f"   ⚠️ Unexpected status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_admin_routes_with_auth()
