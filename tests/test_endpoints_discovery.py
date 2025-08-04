#!/usr/bin/env python3
"""
Simple API Endpoint Discovery Test
"""

import requests
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:8000"

def test_endpoints():
    """Test what endpoints are available and working"""
    
    print("🔍 API Endpoint Discovery Test")
    print("=" * 40)
    
    # Test basic endpoints without authentication
    basic_endpoints = [
        "/",
        "/docs", 
        "/redoc",
        "/auth/login",
        "/admin/client-apps/",
        "/admin/",
        "/user/search"
    ]
    
    print("📋 Testing Basic Endpoints (No Auth):")
    for endpoint in basic_endpoints:
        try:
            response = requests.get(urljoin(BASE_URL, endpoint), timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {endpoint} - Working")
            elif response.status_code == 302:
                print(f"  🔄 {endpoint} - Redirect")
            elif response.status_code == 403:
                print(f"  🔒 {endpoint} - Access Denied")
            else:
                print(f"  ❌ {endpoint} - Status {response.status_code}")
        except Exception as e:
            print(f"  💥 {endpoint} - Error: {e}")
    
    # Get a valid token for API testing
    print("\n🎫 Getting API Token...")
    session = requests.Session()
    
    # Login as admin
    login_data = {"username": "admin", "password": "admin123"}
    login_response = session.post(urljoin(BASE_URL, "/auth/login"), data=login_data, allow_redirects=True)
    
    if login_response.status_code != 200:
        print("❌ Could not login to get token")
        return
    
    # Get existing client apps to use one for token generation
    apps_response = session.get(urljoin(BASE_URL, "/admin/client-apps/api"))
    
    if apps_response.status_code == 200:
        try:
            apps = apps_response.json()
            if apps and len(apps) > 0:
                # Use first available app
                app = apps[0]
                app_id = app.get('app_id')
                
                if app_id:
                    print(f"✅ Found client app: {app_id}")
                    
                    # We'd need the app_secret, but it's not returned in the list
                    # So let's test with client apps API endpoints that we know work
                    
                    print("\n📋 Testing Client Apps API:")
                    
                    client_app_endpoints = [
                        "/admin/client-apps/api",
                    ]
                    
                    for endpoint in client_app_endpoints:
                        try:
                            response = session.get(urljoin(BASE_URL, endpoint))
                            if response.status_code == 200:
                                print(f"  ✅ {endpoint} - Working")
                                try:
                                    data = response.json()
                                    print(f"      📊 Returned {len(data)} items")
                                except:
                                    print(f"      📊 Non-JSON response")
                            else:
                                print(f"  ❌ {endpoint} - Status {response.status_code}")
                        except Exception as e:
                            print(f"  💥 {endpoint} - Error: {e}")
            else:
                print("⚠️ No client apps found")
        except Exception as e:
            print(f"❌ Error parsing apps response: {e}")
    else:
        print(f"❌ Could not get client apps: {apps_response.status_code}")
    
    print("\n📋 Testing Problematic API Endpoints:")
    
    # Test the endpoints that were failing
    problem_endpoints = [
        "/api/v1/users",
        "/api/v1/items"
    ]
    
    for endpoint in problem_endpoints:
        try:
            # Test without auth first
            response = requests.get(urljoin(BASE_URL, endpoint), timeout=5)
            if response.status_code == 401:
                print(f"  🔒 {endpoint} - Requires Authentication (Good)")
            elif response.status_code == 404:
                print(f"  ❓ {endpoint} - Not Found")
            elif response.status_code == 500:
                print(f"  💥 {endpoint} - Server Error")
            elif response.status_code == 200:
                print(f"  ✅ {endpoint} - Working (No Auth Required)")
            else:
                print(f"  ❌ {endpoint} - Status {response.status_code}")
        except Exception as e:
            print(f"  💥 {endpoint} - Error: {e}")

if __name__ == "__main__":
    test_endpoints()
