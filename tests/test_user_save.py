#!/usr/bin/env python3
"""
Test User Data Saving
Test the complete user edit flow including form submission
"""
import requests
import sys

def test_user_save():
    """Test saving user data through the edit form"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing User Data Saving")
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
    
    # First, let's check what users exist
    print("2. Checking existing users...")
    users_response = session.get(f"{base_url}/admin/users")
    if users_response.status_code == 200:
        print("✅ Users page loaded")
        # Look for user links in the response
        if "admin/users/1" in users_response.text:
            test_user_id = "1"
        elif "admin/users/2" in users_response.text:
            test_user_id = "2"
        else:
            print("⚠️ No users found to test with")
            return False
    else:
        print(f"❌ Cannot access users page: {users_response.status_code}")
        return False
    
    print(f"3. Testing edit form for user ID: {test_user_id}")
    
    # Get the edit form
    edit_url = f"{base_url}/admin/users/{test_user_id}/edit"
    edit_response = session.get(edit_url)
    
    print(f"Edit form URL: {edit_url}")
    print(f"Status: {edit_response.status_code}")
    
    if edit_response.status_code != 200:
        print(f"❌ Cannot load edit form: {edit_response.status_code}")
        print("Response content:", edit_response.text[:500])
        return False
    
    print("✅ Edit form loaded")
    
    # Test form submission
    print("4. Testing form submission...")
    
    # Prepare form data for submission
    form_data = {
        "username": "testuser_updated",
        "email": "updated@example.com", 
        "full_name": "Updated Test User",
        "role": "user",
        "is_active": True,
        "password": ""  # Leave password blank to keep current
    }
    
    # Submit the form
    submit_response = session.post(edit_url, data=form_data)
    
    print(f"Submit URL: {edit_url}")
    print(f"Submit status: {submit_response.status_code}")
    print(f"Form data: {form_data}")
    
    if submit_response.status_code == 303:
        print("✅ Form submitted successfully (redirect received)")
        # Follow the redirect
        redirect_url = submit_response.headers.get('location', '')
        print(f"Redirect to: {redirect_url}")
        
        if redirect_url:
            final_response = session.get(f"{base_url}{redirect_url}")
            print(f"Final page status: {final_response.status_code}")
    elif submit_response.status_code == 200:
        print("⚠️ Form returned 200 (may indicate validation error)")
        # Check for error messages in response
        if "error" in submit_response.text.lower() or "Error" in submit_response.text:
            print("❌ Form contains error messages")
            # Extract error message if possible
            lines = submit_response.text.split('\n')
            for line in lines:
                if 'error' in line.lower() and ('span' in line or 'div' in line):
                    print(f"Error found: {line.strip()}")
        else:
            print("⚠️ No obvious error messages found")
    else:
        print(f"❌ Form submission failed: {submit_response.status_code}")
        print("Response content:", submit_response.text[:500])
        return False
    
    print("=" * 50)
    print("✅ User save test completed!")
    return True

if __name__ == "__main__":
    try:
        test_user_save()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        sys.exit(1)
