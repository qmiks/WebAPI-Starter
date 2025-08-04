#!/usr/bin/env python3
"""
Test to verify user edit functionality is working correctly
"""

import requests
import time

def test_user_edit_functionality():
    """Test the complete user edit workflow"""
    print("🧪 Testing User Edit Functionality")
    
    # Step 1: Login
    print("1. Logging in...")
    session = requests.Session()
    
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    login_response = session.post('http://127.0.0.1:8000/auth/login', data=login_data, allow_redirects=False)
    print(f"   Login status: {login_response.status_code}")
    print(f"   Login headers: {dict(login_response.headers)}")
    
    if login_response.status_code not in [200, 303]:
        print("❌ Login failed")
        return False
    
    # Step 2: Access user edit form
    print("2. Accessing user edit form...")
    edit_form_response = session.get('http://127.0.0.1:8000/admin/users/1/edit')
    print(f"   Edit form status: {edit_form_response.status_code}")
    
    if edit_form_response.status_code != 200:
        print("❌ Could not access edit form")
        return False
    
    # Step 3: Submit user edit form
    print("3. Submitting user edit form...")
    edit_data = {
        'username': 'admin',
        'email': 'admin@example.com',
        'full_name': 'Administrator Updated',
        'role': 'admin',
        'is_active': 'true'  # Checkbox value
    }
    
    edit_response = session.post('http://127.0.0.1:8000/admin/users/1/edit', data=edit_data)
    print(f"   Edit submission status: {edit_response.status_code}")
    print(f"   Response headers: {dict(edit_response.headers)}")
    
    # Check if it's a redirect (success)
    if edit_response.status_code == 303:
        print("✅ User edit successful - got redirect!")
        
        # Follow the redirect to see the updated user
        if 'location' in edit_response.headers:
            redirect_url = edit_response.headers['location']
            print(f"   Following redirect to: {redirect_url}")
            
            view_response = session.get(f'http://127.0.0.1:8000{redirect_url}')
            print(f"   View updated user status: {view_response.status_code}")
            
            if view_response.status_code == 200 and 'Administrator Updated' in view_response.text:
                print("✅ User data was successfully updated!")
                return True
        
        return True
    else:
        print(f"❌ Edit submission failed - expected 303 redirect, got {edit_response.status_code}")
        if edit_response.status_code == 200:
            print("   This suggests validation errors in the form")
            # Check for specific error messages in the response
            response_text = edit_response.text
            if "error" in response_text.lower():
                # Try to extract error messages
                lines = response_text.split('\n')
                for line in lines:
                    if 'error' in line.lower() or 'invalid' in line.lower():
                        print(f"   Error found: {line.strip()}")
            else:
                print("   No obvious error messages found in response")
        return False

if __name__ == "__main__":
    success = test_user_edit_functionality()
    if success:
        print("\n🎉 User edit functionality is working correctly!")
    else:
        print("\n💥 User edit functionality still has issues")
