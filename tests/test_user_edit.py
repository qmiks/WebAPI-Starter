#!/usr/bin/env python3
"""
Test User Edit Functionality
"""
import requests
import sys

def test_user_edit():
    """Test the user editing functionality"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing User Edit Functionality")
    print("=" * 50)
    
    # Create a session for authentication
    session = requests.Session()
    
    # Login as admin
    print("1. Logging in as admin...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    login_response = session.post(f"{base_url}/auth/login", data=login_data)
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return False
    
    print("✅ Login successful")
    
    # Test accessing user edit form (assuming user ID 1 exists)
    print("2. Testing user edit form access...")
    
    user_id = "1"  # Test with user ID 1
    edit_url = f"{base_url}/admin/users/{user_id}/edit"
    
    edit_response = session.get(edit_url)
    print(f"Edit form URL: {edit_url}")
    print(f"Status: {edit_response.status_code}")
    
    if edit_response.status_code == 200:
        print("✅ User edit form loaded successfully")
        # Check if the form contains expected elements
        if "Edit User" in edit_response.text and "form" in edit_response.text:
            print("✅ Form contains expected content")
        else:
            print("⚠️ Form may be missing expected content")
    elif edit_response.status_code == 404:
        print("⚠️ User not found (ID may not exist)")
    else:
        print(f"❌ Failed to load user edit form: {edit_response.status_code}")
        print("Response content:", edit_response.text[:200])
        return False
    
    # Test user list to see available users
    print("3. Checking available users...")
    users_response = session.get(f"{base_url}/admin/users")
    if users_response.status_code == 200:
        print("✅ User list accessible")
    else:
        print(f"❌ Cannot access user list: {users_response.status_code}")
    
    print("=" * 50)
    print("✅ User edit functionality test completed!")
    return True

if __name__ == "__main__":
    try:
        test_user_edit()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        sys.exit(1)
