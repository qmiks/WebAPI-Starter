#!/usr/bin/env python3
"""
End-to-End API Test
Create app, generate token, and test API in one go to avoid database resets.
"""

import requests

def create_app_and_test_api():
    """Create app and test API in one session"""
    print("🔍 **End-to-End API Test**")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    # Step 1: Login as admin
    print("   Step 1: Admin login...")
    session = requests.Session()
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    login_response = session.post(f"{base_url}/auth/login", data=login_data)
    print(f"   Login: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print(f"   ❌ Login failed: {login_response.text}")
        return
    
    # Step 2: Create client app via web interface
    print("   Step 2: Creating client app...")
    app_data = {
        "name": "API Test App",
        "description": "Test app for API testing"
    }
    
    create_response = session.post(f"{base_url}/admin/client-apps/create", data=app_data)
    print(f"   Create app: {create_response.status_code}")
    
    if create_response.status_code == 500:
        print(f"   ❌ **INTERNAL SERVER ERROR during app creation!**")
        print(f"   Response: {create_response.text}")
        return
    elif create_response.status_code != 200:
        print(f"   ❌ App creation failed: {create_response.status_code}")
        print(f"   Response: {create_response.text}")
        return
    
    print(f"   ✅ App created successfully")
    
    # Step 3: Extract app credentials from the response
    print("   Step 3: Extracting app credentials...")
    
    # The create response might contain the credentials, or we need to get the list
    apps_response = session.get(f"{base_url}/admin/client-apps/")
    print(f"   Apps list: {apps_response.status_code}")
    
    if apps_response.status_code != 200:
        print(f"   ❌ Could not get apps list: {apps_response.text}")
        return
    
    # Look for credentials in the HTML
    html = apps_response.text
    
    # Try to find our app - it should be the most recent one
    if "API Test App" in html:
        print(f"   ✅ Found our app in the list")
        
        # Extract the app section
        app_start = html.find("API Test App")
        # Look for the next few hundred characters for UUIDs
        app_section = html[app_start:app_start+1000] if app_start != -1 else ""
        
        # Look for UUID patterns around our app
        import re
        uuids = re.findall(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', app_section)
        
        if len(uuids) >= 2:
            app_id = uuids[0]
            app_secret = uuids[1]
            print(f"   App ID: {app_id}")
            print(f"   Secret: {app_secret[:10]}...")
        else:
            # Try alternative approach - use the admin API endpoint if available
            print(f"   Trying alternative extraction...")
            
            # Look for any hex strings that might be app credentials
            hex_strings = re.findall(r'[a-zA-Z0-9_-]{20,}', app_section)
            
            if len(hex_strings) >= 2:
                # Filter for likely app_id (starts with "app_") and secret patterns
                app_ids = [s for s in hex_strings if s.startswith('app_')]
                secrets = [s for s in hex_strings if not s.startswith('app_') and len(s) > 20]
                
                if app_ids and secrets:
                    app_id = app_ids[0]
                    app_secret = secrets[0]
                    print(f"   App ID: {app_id}")
                    print(f"   Secret: {app_secret[:10]}...")
                else:
                    print(f"   ❌ Could not extract credentials from HTML")
                    print(f"   Found hex strings: {len(hex_strings)}")
                    print(f"   Sample: {hex_strings[:3] if hex_strings else 'None'}")
                    return
            else:
                print(f"   ❌ Could not find credentials")
                print(f"   App section: {app_section[:200]}...")
                return
    else:
        print(f"   ❌ Could not find our app in the HTML")
        return
    
    # Step 4: Generate API token
    print("   Step 4: Generating API token...")
    token_data = {
        "app_id": app_id,
        "app_secret": app_secret,
        "expires_in": 3600
    }
    
    # Use a fresh session for the token request (no admin cookies)
    token_response = requests.post(f"{base_url}/api/v1/auth/token", data=token_data)
    print(f"   Token response: {token_response.status_code}")
    
    if token_response.status_code == 500:
        print(f"   ❌ **INTERNAL SERVER ERROR in token generation!**")
        print(f"   Error: {token_response.text}")
        return
    elif token_response.status_code != 200:
        print(f"   ❌ Token generation failed: {token_response.status_code}")
        print(f"   Response: {token_response.text}")
        return
    
    token_data = token_response.json()
    token = token_data.get('access_token')
    print(f"   ✅ Token generated: {token[:50]}...")
    
    # Step 5: Test API endpoints
    print("   Step 5: Testing API endpoints...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test users API
    print(f"   Testing /api/v1/users/...")
    users_response = requests.get(f"{base_url}/api/v1/users/", headers=headers)
    print(f"   Users API: {users_response.status_code}")
    
    if users_response.status_code == 500:
        print(f"   ❌ **INTERNAL SERVER ERROR in users API!**")
        print(f"   Error response: {users_response.text}")
    elif users_response.status_code == 200:
        print(f"   ✅ Users API successful")
        try:
            data = users_response.json()
            print(f"   Users count: {len(data.get('users', []))}")
        except:
            print(f"   Response length: {len(users_response.text)} chars")
    elif users_response.status_code == 401:
        print(f"   ❌ Unauthorized - token issue")
        print(f"   Response: {users_response.text}")
    else:
        print(f"   ⚠️ Unexpected status: {users_response.status_code}")
        print(f"   Response: {users_response.text[:200]}")
    
    # Test items API
    print(f"   Testing /api/v1/items/...")
    items_response = requests.get(f"{base_url}/api/v1/items/", headers=headers)
    print(f"   Items API: {items_response.status_code}")
    
    if items_response.status_code == 500:
        print(f"   ❌ **INTERNAL SERVER ERROR in items API!**")
        print(f"   Error response: {items_response.text}")
    elif items_response.status_code == 200:
        print(f"   ✅ Items API successful")
        try:
            data = items_response.json()
            print(f"   Items count: {len(data.get('items', []))}")
        except:
            print(f"   Response length: {len(items_response.text)} chars")
    elif items_response.status_code == 401:
        print(f"   ❌ Unauthorized - token issue")
        print(f"   Response: {items_response.text}")
    else:
        print(f"   ⚠️ Unexpected status: {items_response.status_code}")
        print(f"   Response: {items_response.text[:200]}")
    
    print(f"\n   🏁 End-to-end test complete!")

if __name__ == "__main__":
    create_app_and_test_api()
