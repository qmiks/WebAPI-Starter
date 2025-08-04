#!/usr/bin/env python3
"""
Test Validation Handling
"""

import requests
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:8000"

def test_validation():
    """Test validation error handling"""
    
    # Create session and login
    session = requests.Session()
    login_data = {"username": "admin", "password": "admin123"}
    login_response = session.post(urljoin(BASE_URL, "/auth/login"), data=login_data, allow_redirects=True)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return
    
    print("✅ Admin login successful")
    
    # Test with empty name
    print("🧪 Testing empty name validation...")
    incomplete_data = {"name": "", "description": "test"}
    response = session.post(urljoin(BASE_URL, "/admin/client-apps/create"), data=incomplete_data)
    
    print(f"Response status: {response.status_code}")
    print(f"Response length: {len(response.text)} chars")
    
    if response.status_code == 500:
        print("❌ Server returned 500 error - this suggests validation is not handled properly")
        print(f"Response preview: {response.text[:300]}...")
    elif response.status_code == 200:
        print("✅ Server returned 200 - checking for validation messages...")
        if "error" in response.text.lower() or "required" in response.text.lower():
            print("✅ Validation messages found")
        else:
            print("⚠️ No clear validation messages found")
            print(f"Response preview: {response.text[:300]}...")
    else:
        print(f"ℹ️ Unexpected status: {response.status_code}")

if __name__ == "__main__":
    print("🧪 Testing Validation Error Handling")
    print("=" * 40)
    test_validation()
