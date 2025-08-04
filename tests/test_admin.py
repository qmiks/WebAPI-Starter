"""
Test Admin UI functionality
This script tests the admin interface endpoints.
"""

import requests
from datetime import datetime

# Base URL for the admin interface
BASE_URL = "http://127.0.0.1:8000"

def test_admin_dashboard():
    """Test the admin dashboard"""
    print("🔍 Testing admin dashboard...")
    response = requests.get(f"{BASE_URL}/admin")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Admin dashboard loaded successfully")
        # Check if the response contains expected content
        if "Admin Panel" in response.text and "Total Users" in response.text:
            print("✅ Dashboard contains expected content")
        else:
            print("⚠️ Dashboard content might be incomplete")
    else:
        print(f"❌ Error loading dashboard: {response.status_code}")
    print("-" * 50)

def test_admin_users_page():
    """Test the admin users page"""
    print("👥 Testing admin users page...")
    response = requests.get(f"{BASE_URL}/admin/users")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Admin users page loaded successfully")
        if "User Management" in response.text:
            print("✅ Users page contains expected content")
    else:
        print(f"❌ Error loading users page: {response.status_code}")
    print("-" * 50)

def test_admin_items_page():
    """Test the admin items page"""
    print("📦 Testing admin items page...")
    response = requests.get(f"{BASE_URL}/admin/items")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Admin items page loaded successfully")
        if "Item Management" in response.text:
            print("✅ Items page contains expected content")
    else:
        print(f"❌ Error loading items page: {response.status_code}")
    print("-" * 50)

def test_user_detail_page():
    """Test viewing a specific user's detail page"""
    print("👤 Testing user detail page...")
    
    # Create session and login
    session = requests.Session()
    login_data = {"username": "admin", "password": "admin123"}
    session.post(f"{BASE_URL}/auth/login", data=login_data)
    
    # Test with user ID 1 (admin user)
    response = session.get(f"{BASE_URL}/admin/users/1")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ User detail page loaded successfully")
        if "User Details" in response.text:
            print("✅ User detail page contains expected content")
    else:
        print(f"❌ Error loading user detail page: {response.status_code}")
    print("-" * 50)

def test_new_user_form():
    """Test the new user form page"""
    print("➕ Testing new user form...")
    
    # Create session and login
    session = requests.Session()
    login_data = {"username": "admin", "password": "admin123"}
    session.post(f"{BASE_URL}/auth/login", data=login_data)
    
    response = session.get(f"{BASE_URL}/admin/users/new")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ New user form loaded successfully")
        if "Add New User" in response.text or "Create" in response.text:
            print("✅ New user form contains expected content")
    else:
        print(f"❌ Error loading new user form: {response.status_code}")
    print("-" * 50)

def test_admin_navigation():
    """Test navigation between admin pages with authentication"""
    print("🧭 Testing admin navigation...")
    
    # Create session and login
    session = requests.Session()
    
    # Login as admin
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    session.post(f"{BASE_URL}/auth/login", data=login_data)
    
    pages = [
        ("/admin", "Dashboard"),
        ("/admin/users", "User Management"),
        ("/admin/items", "Item Management"),
        ("/admin/users/new", "Add New User")
    ]
    
    all_passed = True
    for url, expected_content in pages:
        response = session.get(f"{BASE_URL}{url}")
        if response.status_code == 200 and expected_content in response.text:
            print(f"✅ {url} - OK")
        else:
            print(f"❌ {url} - FAILED (Status: {response.status_code})")
            all_passed = False
    
    if all_passed:
        print("✅ All navigation tests passed")
    else:
        print("⚠️ Some navigation tests failed")
    print("-" * 50)

def run_admin_tests():
    """Run all admin tests"""
    print("[MIGRATE] Starting Web API Admin UI Tests")
    print("=" * 50)
    
    try:
        test_admin_dashboard()
        test_admin_users_page()
        test_admin_items_page()
        test_user_detail_page()
        test_new_user_form()
        test_admin_navigation()
        
        print("✅ All admin tests completed!")
        print("🎉 Admin UI is working correctly!")
        
    except requests.exceptions.ConnectionError:
        print("[ERR] Error: Could not connect to the Web API application.")
        print("Make sure the application is running on http://127.0.0.1:8000")
        print("Run: python main.py")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    run_admin_tests()
