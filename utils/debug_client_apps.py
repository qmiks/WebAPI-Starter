#!/usr/bin/env python3
"""
Debug Client Apps Creation Issue
"""

import requests
import sys
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:8000"

def test_client_app_creation():
    """Test client app creation to debug the 500 error"""
    
    # Create session
    session = requests.Session()
    
    # Step 1: Login as admin
    print("🔑 Logging in as admin...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    login_response = session.post(
        urljoin(BASE_URL, "/auth/login"),
        data=login_data,
        allow_redirects=True
    )
    
    if login_response.status_code not in [302, 200]:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text[:500]}")
        return False
    
    print("✅ Admin login successful")
    print(f"Session cookies: {session.cookies}")
    
    # Step 2: Get client apps page
    print("📋 Getting client apps page...")
    apps_response = session.get(urljoin(BASE_URL, "/admin/client-apps/"))
    print(f"Client apps page status: {apps_response.status_code}")
    print(f"Session cookies after apps page: {session.cookies}")
    
    if apps_response.status_code != 200:
        print(f"❌ Client apps page failed: {apps_response.status_code}")
        print(f"Response: {apps_response.text[:500]}")
        return False
    
    # Step 3: Try to create a client app
    print("➕ Creating client app...")
    create_data = {
        "name": "Test Debug App",
        "description": "Testing client app creation",
        "is_active": True
    }
    
    create_response = session.post(
        urljoin(BASE_URL, "/admin/client-apps/create"),
        data=create_data,
        allow_redirects=False
    )
    
    print(f"Create response status: {create_response.status_code}")
    print(f"Create response headers: {dict(create_response.headers)}")
    
    if create_response.status_code == 500:
        print("❌ 500 Server Error occurred!")
        print(f"Response content: {create_response.text[:1000]}")
    elif create_response.status_code == 200:
        print("✅ Client app created successfully")
        if "Test Debug App" in create_response.text:
            print("✅ App appears in response")
        else:
            print("⚠️ App might not have been created properly")
    else:
        print(f"⚠️ Unexpected status: {create_response.status_code}")
        print(f"Response: {create_response.text[:500]}")
    
    return create_response.status_code == 200

if __name__ == "__main__":
    print("🚀 Debugging Client App Creation Issue")
    print("=" * 50)
    
    try:
        success = test_client_app_creation()
        if success:
            print("✅ Debug test passed!")
        else:
            print("❌ Debug test failed!")
    except Exception as e:
        print(f"❌ Exception during testing: {e}")
        import traceback
        traceback.print_exc()
