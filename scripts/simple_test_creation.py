#!/usr/bin/env python3
"""
Simple Client App Creation Test
"""

import requests
import re
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:8000"

def test_simple_creation():
    """Test simple client app creation"""
    
    # Create session
    session = requests.Session()
    
    # Login as admin
    print("🔑 Logging in as admin...")
    login_data = {"username": "admin", "password": "admin123"}
    login_response = session.post(urljoin(BASE_URL, "/auth/login"), data=login_data, allow_redirects=True)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return False
    
    print("✅ Admin login successful")
    
    # Create a client app
    print("➕ Creating client app...")
    create_data = {
        "name": "Simple Test App",
        "description": "Testing simple creation",
        "is_active": True
    }
    
    create_response = session.post(
        urljoin(BASE_URL, "/admin/client-apps/create"),
        data=create_data,
        allow_redirects=False
    )
    
    print(f"Create response status: {create_response.status_code}")
    
    if create_response.status_code == 200:
        print("✅ Client app created successfully (200 OK)")
        
        # Check if the app name appears in the response
        if create_data["name"] in create_response.text:
            print("✅ App name found in response")
            
            # Try to extract app ID patterns
            id_patterns = re.findall(r'/admin/client-apps/(\d+)', create_response.text)
            print(f"Found ID patterns: {id_patterns}")
            
            app_secret_patterns = re.findall(r'app_secret["\']?\s*:\s*["\']([^"\']+)["\']', create_response.text)
            print(f"Found app secret patterns: {app_secret_patterns}")
            
            # Look for specific content in the response
            if "created successfully" in create_response.text:
                print("✅ Success message found")
            
        else:
            print("❌ App name not found in response")
            
    elif create_response.status_code == 303:
        print("✅ Client app created successfully (303 redirect)")
        redirect_location = create_response.headers.get('location', 'No location')
        print(f"Redirect to: {redirect_location}")
    else:
        print(f"❌ Unexpected status: {create_response.status_code}")
        print(f"Response: {create_response.text[:500]}")
    
    return True

if __name__ == "__main__":
    print("🚀 Simple Client App Creation Test")
    print("=" * 50)
    test_simple_creation()
