#!/usr/bin/env python3
"""
Debug duplicate user error messages by inspecting the full response
"""

import requests
import sys

def debug_duplicate_user_error():
    """Test duplicate user error with detailed debugging"""
    
    base_url = "http://127.0.0.1:8000"
    session = requests.Session()
    
    print("🚀 Debugging Duplicate User Error Messages")
    print("=" * 50)
    
    # 1. Login as admin
    print("1. 🔑 Logging in as admin...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    login_response = session.post(f"{base_url}/auth/login", data=login_data, allow_redirects=False)
    print(f"   Login status: {login_response.status_code}")
    
    if login_response.status_code not in [303, 302]:
        print("❌ Login failed!")
        print(f"   Response: {login_response.text[:500]}")
        return False
    
    print("✅ Admin login successful")
    
    # 2. Try to create user with duplicate username 'admin'
    print("2. 📤 Testing duplicate username 'admin'...")
    duplicate_user_data = {
        "username": "admin",
        "email": "newadmin@example.com", 
        "full_name": "New Admin User",
        "password": "newpassword123",
        "role": "admin",
        "is_active": "true"
    }
    
    duplicate_response = session.post(f"{base_url}/admin/users/new", data=duplicate_user_data, allow_redirects=False)
    print(f"   Response status: {duplicate_response.status_code}")
    print(f"   Content-Type: {duplicate_response.headers.get('content-type', 'unknown')}")
    print(f"   Content length: {len(duplicate_response.text)}")
    
    # Check if error message is present
    html_content = duplicate_response.text
    error_indicators = [
        "Username 'admin' already exists",
        "already exists",
        "alert-error",
        "class=\"error\"",
        "error-message"
    ]
    
    print("3. 🔍 Searching for error indicators...")
    for indicator in error_indicators:
        if indicator in html_content:
            print(f"   ✅ Found: {indicator}")
        else:
            print(f"   ❌ Missing: {indicator}")
    
    # Look for form fields to see if data is preserved
    form_indicators = [
        'value="admin"',
        'value="newadmin@example.com"',
        'value="New Admin User"'
    ]
    
    print("4. 🔍 Checking form data preservation...")
    for indicator in form_indicators:
        if indicator in html_content:
            print(f"   ✅ Found: {indicator}")
        else:
            print(f"   ❌ Missing: {indicator}")
    
    # Print a section of the HTML around where the error should be
    print("5. 📋 HTML content around error section...")
    lines = html_content.split('\n')
    for i, line in enumerate(lines):
        if 'error' in line.lower() or 'alert' in line.lower():
            start = max(0, i-2)
            end = min(len(lines), i+3)
            print(f"   Lines {start+1}-{end}:")
            for j in range(start, end):
                marker = " >>> " if j == i else "     "
                print(f"{marker}{j+1:3}: {lines[j]}")
            break
    else:
        print("   No error-related content found in HTML")
        # Show the first part of the form
        for i, line in enumerate(lines):
            if '<form' in line:
                start = max(0, i)
                end = min(len(lines), i+20)
                print(f"   Form section (lines {start+1}-{end}):")
                for j in range(start, end):
                    print(f"     {j+1:3}: {lines[j]}")
                break

if __name__ == "__main__":
    debug_duplicate_user_error()
