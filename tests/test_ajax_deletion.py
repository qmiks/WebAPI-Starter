#!/usr/bin/env python3
"""
Test user deletion through JavaScript/AJAX interface
"""

import requests

def test_ajax_user_deletion():
    """Test user deletion via JavaScript fetch (AJAX)"""
    
    base_url = "http://127.0.0.1:8000"
    session = requests.Session()
    
    print("🗑️ Testing AJAX User Deletion")
    print("=" * 40)
    
    # Login as admin
    print("1. 🔑 Logging in...")
    login_data = {"username": "admin", "password": "admin123"}
    session.post(f"{base_url}/auth/login", data=login_data)
    
    # Create test user
    print("2. 👤 Creating test user...")
    test_user_data = {
        "username": "ajaxtest",
        "email": "ajaxtest@example.com",
        "full_name": "AJAX Test User",
        "password": "testpass123",
        "role": "user",
        "is_active": "true"
    }
    
    create_response = session.post(f"{base_url}/admin/users/new", data=test_user_data, allow_redirects=False)
    
    if create_response.status_code != 303:
        print(f"❌ User creation failed: {create_response.status_code}")
        return False
    
    # Get users list to find ID
    users_response = session.get(f"{base_url}/admin/users")
    import re
    
    print(f"   Looking for user: {test_user_data['username']}")
    username_pos = users_response.text.find(test_user_data['username'])
    if username_pos != -1:
        print(f"   Found username at position: {username_pos}")
        surrounding_text = users_response.text[max(0, username_pos-300):username_pos+300]
        print(f"   Surrounding text: {surrounding_text[:100]}...")
        id_pattern = r'/admin/users/(\d+)(?:/edit|")'
        id_matches = re.findall(id_pattern, surrounding_text)
        print(f"   ID matches found: {id_matches}")
        if id_matches:
            user_id = id_matches[-1]
            print(f"✅ Found user ID: {user_id}")
        else:
            print("❌ Could not find user ID")
            # Try broader search
            all_ids = re.findall(r'/admin/users/(\d+)', users_response.text)
            print(f"   All user IDs in page: {all_ids}")
            return False
    else:
        print("❌ Could not find user in list")
        # Show a snippet of the page to debug
        if len(users_response.text) > 500:
            print("   Page content snippet:")
            print(users_response.text[1000:1500])
        return False
    
    # Test AJAX-style deletion (simulating the JavaScript fetch)
    print("3. 🗑️ Testing AJAX deletion...")
    delete_response = session.post(f"{base_url}/admin/users/{user_id}/delete")
    
    if delete_response.status_code in [200, 303, 302]:
        print(f"✅ AJAX delete successful: {delete_response.status_code}")
        
        # Verify user is gone
        verify_response = session.get(f"{base_url}/admin/users")
        if test_user_data['username'] not in verify_response.text:
            print("✅ User successfully deleted via AJAX!")
            return True
        else:
            print("❌ User still exists after deletion")
            return False
    else:
        print(f"❌ AJAX delete failed: {delete_response.status_code}")
        return False

if __name__ == "__main__":
    success = test_ajax_user_deletion()
    print("\n" + "=" * 40)
    if success:
        print("🎉 AJAX user deletion works!")
    else:
        print("❌ AJAX user deletion failed!")
    print("=" * 40)
