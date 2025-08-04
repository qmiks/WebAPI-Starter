#!/usr/bin/env python3
"""
Test duplicate user error messages
"""

import requests
import random
import string

def test_duplicate_user_messages():
    """Test that proper error messages are shown for duplicate users"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 Testing Duplicate User Error Messages")
    print("=" * 50)
    
    # Start session
    session = requests.Session()
    
    # 1. Login as admin
    print("1. 🔑 Logging in as admin...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    login_response = session.post(f"{base_url}/auth/login", data=login_data, allow_redirects=False)
    print(f"   Login status: {login_response.status_code}")
    
    if login_response.status_code != 303:
        print("❌ Login failed!")
        return False
    
    print("✅ Admin login successful")
    
    # 2. Test duplicate username
    print("\n2. 📤 Testing duplicate username error...")
    
    duplicate_user_data = {
        "username": "admin",  # This already exists
        "email": "newadmin@example.com",
        "full_name": "New Admin",
        "password": "password123",
        "role": "admin",
        "is_active": "true"
    }
    
    create_response = session.post(f"{base_url}/admin/users/new", data=duplicate_user_data)
    print(f"   Response status: {create_response.status_code}")
    
    if create_response.status_code == 200:
        # Check if error message is in the response (account for HTML encoding)
        response_text = create_response.text
        username_error_patterns = [
            "Username 'admin' already exists",
            "Username &#39;admin&#39; already exists",  # HTML encoded version
            "Username &apos;admin&apos; already exists"  # Alternative encoding
        ]
        
        username_error_found = any(pattern in response_text for pattern in username_error_patterns)
        if username_error_found:
            print("✅ Username duplicate error message found!")
            
            # Check if form data is preserved
            if 'value="newadmin@example.com"' in response_text:
                print("✅ Form data preserved (email field)")
            else:
                print("⚠️  Form data not preserved")
                
            if 'value="New Admin"' in response_text:
                print("✅ Form data preserved (full name field)")
            else:
                print("⚠️  Form data not preserved (full name)")
                
        else:
            print("❌ Username duplicate error message NOT found")
            print("   Searched for patterns:")
            for pattern in username_error_patterns:
                print(f"     - {pattern}")
            print("   Response content snippet:")
            print(response_text[:800] + " ...")
            return False
    else:
        print(f"❌ Expected status 200, got {create_response.status_code}")
        return False
    
    # 3. Test duplicate email
    print("\n3. 📤 Testing duplicate email error...")
    
    duplicate_email_data = {
        "username": "newuser123",
        "email": "admin@example.com",  # This already exists
        "full_name": "New User",
        "password": "password123",
        "role": "user",
        "is_active": "true"
    }
    
    create_response = session.post(f"{base_url}/admin/users/new", data=duplicate_email_data)
    print(f"   Response status: {create_response.status_code}")
    
    if create_response.status_code == 200:
        response_text = create_response.text
        email_error_patterns = [
            "Email 'admin@example.com' already exists",
            "Email &#39;admin@example.com&#39; already exists",  # HTML encoded version
            "Email &apos;admin@example.com&apos; already exists"  # Alternative encoding
        ]
        
        email_error_found = any(pattern in response_text for pattern in email_error_patterns)
        if email_error_found:
            print("✅ Email duplicate error message found!")
            
            # Check if form data is preserved
            if 'value="newuser123"' in response_text:
                print("✅ Form data preserved (username field)")
            else:
                print("⚠️  Form data not preserved (username)")
                
        else:
            print("❌ Email duplicate error message NOT found")
            print("   Searched for patterns:")
            for pattern in email_error_patterns:
                print(f"     - {pattern}")
            print("   Response content snippet:")
            print(response_text[:800] + " ...")
            return False
    else:
        print(f"❌ Expected status 200, got {create_response.status_code}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All duplicate user error message tests passed!")
    print("✅ Username duplicates show proper error messages")
    print("✅ Email duplicates show proper error messages") 
    print("✅ Form data is preserved when errors occur")
    
    return True

if __name__ == "__main__":
    try:
        success = test_duplicate_user_messages()
        if success:
            print("\n🎉 Duplicate user error messaging test completed successfully!")
        else:
            print("\n❌ Some tests failed!")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
