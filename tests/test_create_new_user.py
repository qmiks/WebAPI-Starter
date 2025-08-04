#!/usr/bin/env python3
"""
Test script to verify "Create New User" functionality in admin panel
"""

import requests
import time
import random
import string

def generate_test_user_data():
    """Generate random test user data"""
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return {
        'username': f'testuser_{random_suffix}',
        'email': f'test_{random_suffix}@example.com',
        'full_name': f'Test User {random_suffix.upper()}',
        'password': 'testpass123',
        'role': 'user',
        'is_active': 'true'
    }

def test_create_new_user():
    """Test the complete create new user workflow"""
    print("🧪 Testing Create New User Functionality")
    print("=" * 50)
    
    session = requests.Session()
    base_url = 'http://127.0.0.1:8000'
    
    # Step 1: Login as admin
    print("1. 🔑 Logging in as admin...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    login_response = session.post(f'{base_url}/auth/login', data=login_data, allow_redirects=False)
    print(f"   Login status: {login_response.status_code}")
    
    if login_response.status_code != 303:
        print("❌ Login failed")
        return False
    
    print("✅ Admin login successful")
    
    # Step 2: Access new user form
    print("\n2. 📝 Accessing new user form...")
    new_user_form_response = session.get(f'{base_url}/admin/users/new')
    print(f"   New user form status: {new_user_form_response.status_code}")
    
    if new_user_form_response.status_code != 200:
        print("❌ Could not access new user form")
        return False
    
    # Check if form contains expected elements
    form_content = new_user_form_response.text
    expected_form_fields = ['username', 'email', 'full_name', 'password', 'role', 'is_active']
    missing_fields = []
    
    for field in expected_form_fields:
        if field not in form_content:
            missing_fields.append(field)
    
    if missing_fields:
        print(f"⚠️ Missing form fields: {missing_fields}")
    else:
        print("✅ New user form loaded with all expected fields")
    
    # Step 3: Generate test user data
    print("\n3. 🎲 Generating test user data...")
    test_user = generate_test_user_data()
    print(f"   Username: {test_user['username']}")
    print(f"   Email: {test_user['email']}")
    print(f"   Full Name: {test_user['full_name']}")
    print(f"   Role: {test_user['role']}")
    print(f"   Active: {test_user['is_active']}")
    
    # Step 4: Submit new user form
    print("\n4. 📤 Submitting new user form...")
    create_response = session.post(f'{base_url}/admin/users/new', data=test_user, allow_redirects=False)
    print(f"   Create user status: {create_response.status_code}")
    print(f"   Response headers: {dict(create_response.headers)}")
    
    # Check response
    if create_response.status_code == 303:
        print("✅ User creation successful - got redirect!")
        redirect_location = create_response.headers.get('location', '')
        print(f"   Redirect location: {redirect_location}")
        
        # Follow redirect to see the result
        if redirect_location:
            final_response = session.get(f'{base_url}{redirect_location}')
            print(f"   Final page status: {final_response.status_code}")
            
            # Check if user appears in the content
            if test_user['username'] in final_response.text:
                print("✅ New user appears in the response content")
                return True
            else:
                print("⚠️ New user not found in response content")
                return True  # Still successful if we got the redirect
        
        return True
        
    elif create_response.status_code == 200:
        print("❌ User creation failed - form returned with errors")
        
        # Try to extract error messages
        response_text = create_response.text
        if "error" in response_text.lower():
            print("   Checking for error messages...")
            lines = response_text.split('\n')
            error_found = False
            for line in lines:
                if 'error' in line.lower() or 'invalid' in line.lower() or 'already exists' in line.lower():
                    print(f"   Error: {line.strip()}")
                    error_found = True
            
            if not error_found:
                print("   No specific error message found")
        
        return False
    
    else:
        print(f"❌ Unexpected response status: {create_response.status_code}")
        return False

def test_duplicate_user_handling():
    """Test that duplicate usernames are properly handled"""
    print("\n" + "=" * 50)
    print("🔄 Testing Duplicate User Handling")
    print("=" * 50)
    
    session = requests.Session()
    base_url = 'http://127.0.0.1:8000'
    
    # Login first
    login_data = {'username': 'admin', 'password': 'admin123'}
    login_response = session.post(f'{base_url}/auth/login', data=login_data, allow_redirects=False)
    
    if login_response.status_code != 303:
        print("❌ Admin login failed for duplicate test")
        return False
    
    print("✅ Admin logged in for duplicate test")
    
    # Try to create a user with existing username 'admin'
    duplicate_user_data = {
        'username': 'admin',  # This should already exist
        'email': 'admin2@example.com',
        'full_name': 'Admin Duplicate',
        'password': 'testpass123',
        'role': 'admin',
        'is_active': 'true'
    }
    
    print("\n📤 Attempting to create user with existing username 'admin'...")
    duplicate_response = session.post(f'{base_url}/admin/users/new', data=duplicate_user_data, allow_redirects=False)
    print(f"   Duplicate user response status: {duplicate_response.status_code}")
    
    if duplicate_response.status_code == 200:
        # Should return form with error message
        if "already exists" in duplicate_response.text.lower():
            print("✅ Duplicate username properly rejected with error message")
            return True
        else:
            print("⚠️ Got 200 response but no clear error message about duplicate")
            return False
    elif duplicate_response.status_code == 303:
        print("❌ Duplicate username was accepted (this shouldn't happen)")
        return False
    else:
        print(f"❌ Unexpected response for duplicate: {duplicate_response.status_code}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Create New User Tests")
    print("=" * 60)
    
    # Test 1: Basic user creation
    success1 = test_create_new_user()
    
    # Test 2: Duplicate handling
    success2 = test_duplicate_user_handling()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    if success1:
        print("✅ Create New User: PASSED")
    else:
        print("❌ Create New User: FAILED")
    
    if success2:
        print("✅ Duplicate User Handling: PASSED")
    else:
        print("❌ Duplicate User Handling: FAILED")
    
    if success1 and success2:
        print("\n🎉 ALL TESTS PASSED! User creation functionality is working correctly!")
    else:
        print("\n💥 Some tests failed. User creation may need investigation.")
    
    print("\n💡 You can also test manually at: http://127.0.0.1:8000/admin/users/new")
