#!/usr/bin/env python3
"""
Test user deletion functionality
"""

import requests
import random
import string

def generate_random_string(length=8):
    """Generate a random string for unique test data"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_user_deletion():
    """Test user deletion functionality"""
    
    base_url = "http://127.0.0.1:8000"
    session = requests.Session()
    
    print("🗑️ Testing User Deletion Functionality")
    print("=" * 50)
    
    # 1. Login as admin
    print("1. 🔑 Logging in as admin...")
    login_data = {"username": "admin", "password": "admin123"}
    login_response = session.post(f"{base_url}/auth/login", data=login_data, allow_redirects=False)
    
    if login_response.status_code not in [303, 302]:
        print(f"❌ Login failed! Status: {login_response.status_code}")
        return False
    
    print("✅ Admin login successful")
    
    # 2. Create a test user to delete
    print("2. 👤 Creating test user...")
    random_id = generate_random_string(6)
    test_user_data = {
        "username": f"deletetest_{random_id}",
        "email": f"deletetest_{random_id}@example.com",
        "full_name": f"Delete Test User {random_id}",
        "password": "testpass123",
        "role": "user",
        "is_active": "true"
    }
    
    create_response = session.post(f"{base_url}/admin/users/new", data=test_user_data, allow_redirects=False)
    
    if create_response.status_code != 303:
        print(f"❌ User creation failed! Status: {create_response.status_code}")
        return False
    
    print(f"✅ Test user '{test_user_data['username']}' created successfully")
    
    # 3. Get the user list to find the user ID
    print("3. 🔍 Finding created user ID...")
    users_response = session.get(f"{base_url}/admin/users")
    
    if users_response.status_code != 200:
        print(f"❌ Failed to get users list! Status: {users_response.status_code}")
        return False
    
    # Look for the user ID in the HTML (simple approach)
    users_html = users_response.text
    
    # Find the user ID by looking for the username in the HTML
    import re
    # Look for pattern like: href="/admin/users/123" in the HTML around our username
    pattern = rf'{test_user_data["username"]}.*?href="/admin/users/(\d+)"'
    match = re.search(pattern, users_html, re.DOTALL)
    
    if not match:
        # Try alternative pattern - look for user ID in any nearby link
        username_pos = users_html.find(test_user_data['username'])
        if username_pos != -1:
            # Look for user ID patterns around the username
            surrounding_text = users_html[max(0, username_pos-300):username_pos+300]
            id_pattern = r'/admin/users/(\d+)(?:/edit|")'
            id_matches = re.findall(id_pattern, surrounding_text)
            if id_matches:
                user_id = id_matches[-1]  # Take the last match
                print(f"✅ Found user ID (alternative method): {user_id}")
            else:
                print(f"❌ Could not find user ID for '{test_user_data['username']}'")
                print("Available content snippet:")
                print(surrounding_text)
                return False
        else:
            print(f"❌ Could not find username '{test_user_data['username']}' in HTML")
            return False
    else:
        user_id = match.group(1)
        print(f"✅ Found user ID: {user_id}")
    
    # 4. Test delete functionality
    print("4. 🗑️ Testing user deletion...")
    delete_response = session.post(f"{base_url}/admin/users/{user_id}/delete", allow_redirects=False)
    
    if delete_response.status_code == 303:
        print("✅ Delete request successful (redirect)")
    else:
        print(f"❌ Delete failed! Status: {delete_response.status_code}")
        print("Response content:")
        print(delete_response.text[:500])
        return False
    
    # 5. Verify user is deleted
    print("5. ✅ Verifying user deletion...")
    verify_response = session.get(f"{base_url}/admin/users")
    
    if verify_response.status_code == 200:
        verify_html = verify_response.text
        if test_user_data['username'] not in verify_html:
            print(f"✅ User '{test_user_data['username']}' successfully deleted!")
            print("✅ User deletion functionality is working correctly!")
            return True
        else:
            print(f"❌ User '{test_user_data['username']}' still appears in users list")
            return False
    else:
        print(f"❌ Failed to verify deletion! Status: {verify_response.status_code}")
        return False

if __name__ == "__main__":
    success = test_user_deletion()
    print("\n" + "=" * 50)
    if success:
        print("🎉 User deletion test PASSED!")
    else:
        print("❌ User deletion test FAILED!")
    print("=" * 50)
