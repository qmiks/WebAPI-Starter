#!/usr/bin/env python3
"""
Extract the actual error content from duplicate user response
"""

import requests

def extract_error_content():
    """Get the exact error content from duplicate user response"""
    
    base_url = "http://127.0.0.1:8000"
    session = requests.Session()
    
    # Login as admin
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    session.post(f"{base_url}/auth/login", data=login_data, allow_redirects=False)
    
    # Try to create duplicate user
    duplicate_user_data = {
        "username": "admin",
        "email": "newadmin@example.com", 
        "full_name": "New Admin User",
        "password": "newpassword123",
        "role": "admin",
        "is_active": "true"
    }
    
    response = session.post(f"{base_url}/admin/users/new", data=duplicate_user_data, allow_redirects=False)
    html_content = response.text
    
    # Find error div section
    lines = html_content.split('\n')
    in_error_section = False
    error_content = []
    
    for i, line in enumerate(lines):
        # Look for the error div
        if 'if error' in line or '{% if error %}' in line:
            in_error_section = True
            print(f"Found error template block at line {i+1}:")
            # Show surrounding context
            start = max(0, i-5)
            end = min(len(lines), i+15)
            for j in range(start, end):
                marker = " >>> " if j == i else "     "
                print(f"{marker}{j+1:3}: {lines[j]}")
            break
            
        # Also check for actual error content
        if 'alert-error' in line:
            print(f"Found alert-error at line {i+1}:")
            start = max(0, i-3)
            end = min(len(lines), i+8)
            for j in range(start, end):
                marker = " >>> " if j == i else "     "
                print(f"{marker}{j+1:3}: {lines[j]}")
            
        # Look for any line containing "admin"
        if 'admin' in line.lower() and ('already' in line.lower() or 'exists' in line.lower()):
            print(f"Found admin/exists at line {i+1}: {line.strip()}")

if __name__ == "__main__":
    extract_error_content()
