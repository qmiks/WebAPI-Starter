#!/usr/bin/env python3
"""
Create Client App and Test API
Create a client app through the web interface and then test the API.
"""

import requests
import re

def create_client_app():
    """Create a client app through the web interface"""
    print("🏗️ **Creating Client App**")
    print("=" * 30)
    
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
            # Create client app
            app_data = {
                "name": "Test API Client",
                "description": "Test client for API testing"
            }
            
            create_response = session.post(f"{base_url}/admin/client-apps/create", data=app_data)
            print(f"   Create app response: {create_response.status_code}")
            
            if create_response.status_code == 200:
                print(f"   ✅ App created successfully")
                
                # Get the updated apps list
                apps_response = session.get(f"{base_url}/admin/client-apps/")
                if apps_response.status_code == 200:
                    html = apps_response.text
                    
                    # Look for app credentials in the HTML - try multiple patterns
                    print(f"   Searching for credentials in HTML...")
                    
                    # Pattern 1: Look for UUID-like strings (app IDs and secrets)
                    uuids = re.findall(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', html)
                    print(f"   Found {len(uuids)} UUID patterns")
                    
                    if len(uuids) >= 2:
                        return uuids[0], uuids[1]  # First two UUIDs are likely ID and secret
                    
                    # Pattern 2: Look for specific HTML elements with app data
                    app_id_match = re.search(r'id["\']?\s*[:=]\s*["\']?([a-f0-9-]{36})', html, re.IGNORECASE)
                    secret_match = re.search(r'secret["\']?\s*[:=]\s*["\']?([a-f0-9-]{36})', html, re.IGNORECASE)
                    
                    if app_id_match and secret_match:
                        return app_id_match.group(1), secret_match.group(1)
                    
                    # Pattern 3: Look for any 36-character hex strings
                    hex_strings = re.findall(r'[a-f0-9]{32,36}', html)
                    print(f"   Found {len(hex_strings)} hex strings")
                    
                    if len(hex_strings) >= 2:
                        return hex_strings[0], hex_strings[1]
                    
                    # If no patterns match, let's look at the actual HTML structure
                    print(f"   Could not extract credentials automatically")
                    print(f"   HTML contains 'Test API Client': {'Test API Client' in html}")
                    
                    # Look for our created app specifically
                    if "Test API Client" in html:
                        # Find the section with our app
                        start = html.find("Test API Client")
                        section = html[start:start+1000] if start != -1 else ""
                        print(f"   App section: {section[:200]}...")
                        
                        # Look for UUIDs in this section
                        section_uuids = re.findall(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', section)
                        if len(section_uuids) >= 2:
                            return section_uuids[0], section_uuids[1]
                    
                    print(f"   ❌ Could not extract app credentials from HTML")
                    return None, None
                else:
                    print(f"   ❌ Could not retrieve apps list: {apps_response.status_code}")
                    return None, None
            
            elif create_response.status_code == 500:
                print(f"   ❌ **INTERNAL SERVER ERROR during app creation!**")
                print(f"   Response: {create_response.text}")
                return None, None
            else:
                print(f"   ❌ App creation failed: {create_response.status_code}")
                print(f"   Response: {create_response.text[:200]}")
                return None, None
        else:
            print(f"   ❌ Admin login failed: {login_response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"   ❌ Error creating app: {e}")
        return None, None

def test_with_hardcoded_app():
    """Test by creating app via direct database access"""
    print("\n🔧 **Testing with Direct Database Access**")
    print("-" * 40)
    
    try:
        # Import database functions directly
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from data.database import client_app_crud
        from data.models import ClientAppCreate
        
        # Create a test app directly
        app_data = ClientAppCreate(
            name="Direct Test App",
            description="Created directly for testing"
        )
        
        created_app = client_app_crud.create_client_app(app_data)
        print(f"   ✅ App created directly")
        print(f"   App ID: {created_app['app_id']}")
        print(f"   App Secret: {created_app['app_secret'][:10]}...")
        
        return created_app['app_id'], created_app['app_secret']
        
    except Exception as e:
        print(f"   ❌ Direct creation failed: {e}")
        return None, None

def test_token_and_api(app_id, app_secret):
    """Test token generation and API calls"""
    print(f"\n🎫 **Testing Token Generation and API Calls**")
    print("-" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    if not app_id or not app_secret:
        print("   ⚠️ No credentials available")
        return
    
    print(f"   Using App ID: {app_id}")
    print(f"   Using Secret: {app_secret[:10]}...")
    
    # Test 1: Generate token
    print(f"\n   🔑 Step 1: Generating token...")
    token_data = {
        "app_id": app_id,
        "app_secret": app_secret,
        "expires_in": 3600
    }
    
    try:
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
        
        # Test 2: Use token with API
        print(f"\n   🚀 Step 2: Testing API calls with token...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Test users endpoint
        print(f"   Testing GET /api/v1/users/...")
        users_response = requests.get(f"{base_url}/api/v1/users/", headers=headers)
        print(f"   Users API: {users_response.status_code}")
        
        if users_response.status_code == 500:
            print(f"   ❌ **INTERNAL SERVER ERROR in users API!**")
            print(f"   Error: {users_response.text}")
        elif users_response.status_code == 200:
            print(f"   ✅ Users API works")
            data = users_response.json()
            print(f"   Users count: {len(data.get('users', []))}")
        else:
            print(f"   ⚠️ Users API unexpected: {users_response.status_code}")
            print(f"   Response: {users_response.text[:200]}")
        
        # Test items endpoint
        print(f"   Testing GET /api/v1/items/...")
        items_response = requests.get(f"{base_url}/api/v1/items/", headers=headers)
        print(f"   Items API: {items_response.status_code}")
        
        if items_response.status_code == 500:
            print(f"   ❌ **INTERNAL SERVER ERROR in items API!**")
            print(f"   Error: {items_response.text}")
        elif items_response.status_code == 200:
            print(f"   ✅ Items API works")
            data = items_response.json()
            print(f"   Items count: {len(data.get('items', []))}")
        else:
            print(f"   ⚠️ Items API unexpected: {items_response.status_code}")
            print(f"   Response: {items_response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Error in token/API test: {e}")

def main():
    print("🔍 **Create App and Test API**")
    print("=" * 50)
    
    # Method 1: Try creating app through web interface
    app_id, app_secret = create_client_app()
    
    # Method 2: If web interface fails, try direct database
    if not app_id or not app_secret:
        app_id, app_secret = test_with_hardcoded_app()
    
    # Test token generation and API calls
    if app_id and app_secret:
        test_token_and_api(app_id, app_secret)
    else:
        print("\n❌ Could not create client app - cannot test API")
    
    print("\n" + "=" * 50)
    print("🏁 **Test Complete**")

if __name__ == "__main__":
    main()
