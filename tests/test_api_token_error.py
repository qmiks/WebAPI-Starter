#!/usr/bin/env python3
"""
Test API Token Authentication
Test calling API endpoints with JWT tokens to identify Internal Server Error.
"""

import requests
import json

def test_api_without_token():
    """Test API access without token (should get 401)"""
    print("🧪 **Testing API without token**")
    print("=" * 40)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        response = requests.get(f"{base_url}/api/v1/users/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 401:
            print("   ✅ Correctly returns 401 Unauthorized")
        else:
            print(f"   ⚠️ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_get_client_apps():
    """Check if there are any client apps available"""
    print("\n🔍 **Checking Client Apps**")
    print("-" * 30)
    
    base_url = "http://127.0.0.1:8000"
    
    # Login as admin first to check client apps
    session = requests.Session()
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        login_response = session.post(f"{base_url}/auth/login", data=login_data)
        print(f"   Admin login: {login_response.status_code}")
        
        if login_response.status_code == 200:
            # Try to access client apps management page
            apps_response = session.get(f"{base_url}/admin/client-apps/")
            print(f"   Apps page: {apps_response.status_code}")
            
            if apps_response.status_code == 200:
                # Check if there are any apps in the HTML
                if "No applications found" in apps_response.text:
                    print("   📝 No client apps found - need to create one")
                    return None
                else:
                    print("   ✅ Client apps exist")
                    # Try to extract app info from HTML (basic check)
                    if "app-" in apps_response.text:
                        print("   💡 Found app IDs in HTML")
                        return True
            else:
                print(f"   ❌ Could not access apps page: {apps_response.status_code}")
                print(f"   Response preview: {apps_response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error checking client apps: {e}")
    
    return None

def test_create_client_app():
    """Create a test client app"""
    print("\n🏗️ **Creating Test Client App**")
    print("-" * 30)
    
    base_url = "http://127.0.0.1:8000"
    
    # Login as admin
    session = requests.Session()
    login_data = {
        "username": "admin", 
        "password": "admin123"
    }
    
    try:
        login_response = session.post(f"{base_url}/auth/login", data=login_data)
        print(f"   Admin login: {login_response.status_code}")
        
        if login_response.status_code == 200:
            # Create a client app
            app_data = {
                "name": "Test API Client",
                "description": "Test application for API testing"
            }
            
            create_response = session.post(f"{base_url}/admin/client-apps/create", data=app_data)
            print(f"   Create app: {create_response.status_code}")
            
            if create_response.status_code == 200:
                print("   ✅ Client app created successfully")
                
                # Try to get the app list to find our new app
                apps_response = session.get(f"{base_url}/admin/client-apps/")
                if apps_response.status_code == 200:
                    # Look for app ID in the response
                    import re
                    app_ids = re.findall(r'app-([a-f0-9-]+)', apps_response.text)
                    if app_ids:
                        app_id = app_ids[0]
                        print(f"   📝 Found App ID: {app_id}")
                        
                        # Look for app secret in the HTML
                        secrets = re.findall(r'secret-([a-f0-9-]+)', apps_response.text)
                        if secrets:
                            app_secret = secrets[0]
                            print(f"   🔑 Found App Secret: {app_secret[:10]}...")
                            return app_id, app_secret
                        else:
                            print("   ⚠️ Could not find app secret in HTML")
                    else:
                        print("   ⚠️ Could not find app ID in HTML")
                else:
                    print(f"   ❌ Could not retrieve apps list: {apps_response.status_code}")
            else:
                print(f"   ❌ Failed to create app: {create_response.status_code}")
                print(f"   Response: {create_response.text[:200]}")
                
    except Exception as e:
        print(f"   ❌ Error creating client app: {e}")
    
    return None, None

def test_get_api_token(app_id, app_secret):
    """Test getting JWT token from app credentials"""
    print("\n🎫 **Getting API Token**")
    print("-" * 30)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        print(f"   App ID: {app_id}")
        print(f"   App Secret: {app_secret[:10]}...")
        
        # Try the API token endpoint first
        print("\n   Method 1: Using /api/v1/auth/token endpoint...")
        token_data = {
            "app_id": app_id,
            "app_secret": app_secret,
            "expires_in": 3600
        }
        
        response = requests.post(f"{base_url}/api/v1/auth/token", data=token_data)
        print(f"   Token endpoint status: {response.status_code}")
        
        if response.status_code == 500:
            print(f"   ❌ **INTERNAL SERVER ERROR in token generation!**")
            print(f"   Response: {response.text}")
            return None
        elif response.status_code == 200:
            token_response = response.json()
            print(f"   ✅ Token generated via API")
            print(f"   Token: {token_response['access_token'][:50]}...")
            return token_response['access_token']
        else:
            print(f"   ⚠️ Token endpoint error: {response.status_code}")
            print(f"   Response: {response.text}")
        
        # Fallback: Import and use directly
        print("\n   Method 2: Using direct import...")
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from api_auth import create_api_token
        
        try:
            token_data = create_api_token(app_id, app_secret)
            print(f"   ✅ Token generated directly")
            print(f"   Token: {token_data['access_token'][:50]}...")
            return token_data['access_token']
            
        except Exception as e:
            print(f"   ❌ Direct token generation failed: {e}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error in token test: {e}")
        return None

def test_api_with_token(token):
    """Test API calls with JWT token"""
    print("\n🚀 **Testing API with Token**")
    print("-" * 30)
    
    base_url = "http://127.0.0.1:8000"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test GET /api/v1/users/
    print("\n   Testing GET /api/v1/users/...")
    try:
        response = requests.get(f"{base_url}/api/v1/users/", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 500:
            print(f"   ❌ **INTERNAL SERVER ERROR FOUND!**")
            print(f"   Response: {response.text}")
        elif response.status_code == 200:
            print(f"   ✅ API call successful")
            data = response.json()
            print(f"   Users count: {len(data.get('users', []))}")
        else:
            print(f"   ⚠️ Unexpected status: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error calling API: {e}")
    
    # Test GET /api/v1/items/
    print("\n   Testing GET /api/v1/items/...")
    try:
        response = requests.get(f"{base_url}/api/v1/items/", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 500:
            print(f"   ❌ **INTERNAL SERVER ERROR FOUND!**")
            print(f"   Response: {response.text}")
        elif response.status_code == 200:
            print(f"   ✅ API call successful")
            data = response.json()
            print(f"   Items count: {len(data.get('items', []))}")
        else:
            print(f"   ⚠️ Unexpected status: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error calling API: {e}")

def main():
    print("🔍 **API Token Authentication Test**")
    print("=" * 50)
    
    # Test 1: API without token
    test_api_without_token()
    
    # Test 2: Check existing client apps
    apps_exist = test_get_client_apps()
    
    # Test 3: Create client app if none exist
    app_id, app_secret = None, None
    if not apps_exist:
        app_id, app_secret = test_create_client_app()
    
    # Test 4: Get API token
    if app_id and app_secret:
        token = test_get_api_token(app_id, app_secret)
        
        # Test 5: Use token with API
        if token:
            test_api_with_token(token)
        else:
            print("\n❌ Could not get valid token - cannot test API calls")
    else:
        print("\n❌ Could not get app credentials - cannot test token generation")
    
    print("\n" + "=" * 50)
    print("🏁 **Test Complete**")

if __name__ == "__main__":
    main()
