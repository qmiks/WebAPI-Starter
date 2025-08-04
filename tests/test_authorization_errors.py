#!/usr/bin/env python3
"""
Test Authorization Error Handling
Test what happens when users try to access unauthorized areas.
"""

import requests

def test_user_accessing_admin():
    print("🔒 **Testing User Authorization Errors**")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    # Step 1: Login as regular user
    print("\n1️⃣ **Login as Regular User**")
    session = requests.Session()
    
    login_data = {
        "username": "user",
        "password": "user123"
    }
    
    login_response = session.post(f"{base_url}/auth/login", data=login_data)
    print(f"   Login Status: {login_response.status_code}")
    
    if login_response.status_code not in [200, 303, 302]:
        print(f"   ❌ Login failed: {login_response.text}")
        return
    
    print("   ✅ Logged in as regular user")
    
    # Step 2: Try to access admin areas
    admin_endpoints = [
        "/admin",
        "/admin/",
        "/admin/dashboard",
        "/admin/users",
        "/admin/client-apps",
        "/admin/client-apps/",
    ]
    
    print("\n2️⃣ **Trying to Access Admin Areas**")
    for endpoint in admin_endpoints:
        print(f"\n   🔍 Testing: {endpoint}")
        try:
            response = session.get(f"{base_url}{endpoint}")
            print(f"      Status: {response.status_code}")
            print(f"      Content-Type: {response.headers.get('content-type', 'unknown')}")
            
            if response.status_code == 403:
                if 'application/json' in response.headers.get('content-type', ''):
                    print(f"      ❌ **RAW JSON ERROR**: {response.text}")
                    print(f"      ⚠️  User sees raw JSON instead of nice error page!")
                else:
                    print(f"      ✅ Proper HTML error page")
            elif response.status_code == 200:
                print(f"      ⚠️  User can access admin area (security issue?)")
            else:
                print(f"      Response: {response.text[:100]}...")
                
        except Exception as e:
            print(f"      ❌ Error: {e}")

def test_unauthenticated_access():
    print("\n🚫 **Testing Unauthenticated Access**")
    print("-" * 40)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test without any login
    endpoints_to_test = [
        "/admin",
        "/admin/dashboard", 
        "/admin/users",
        "/user-portal",
        "/user/search"
    ]
    
    for endpoint in endpoints_to_test:
        print(f"\n   🔍 Testing: {endpoint}")
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"      Status: {response.status_code}")
            print(f"      Content-Type: {response.headers.get('content-type', 'unknown')}")
            
            if response.status_code == 401 or response.status_code == 403:
                if 'application/json' in response.headers.get('content-type', ''):
                    print(f"      ❌ **RAW JSON ERROR**: {response.text}")
                else:
                    print(f"      ✅ Proper redirect or error page")
            elif response.status_code == 302 or response.status_code == 303:
                location = response.headers.get('location', 'No location')
                print(f"      ✅ Redirected to: {location}")
            else:
                print(f"      Response length: {len(response.text)} chars")
                
        except Exception as e:
            print(f"      ❌ Error: {e}")

def main():
    test_user_accessing_admin()
    test_unauthenticated_access()
    
    print("\n" + "=" * 60)
    print("🎯 **Summary:**")
    print("Look for '❌ RAW JSON ERROR' - these need proper HTML error pages")
    print("Users should see friendly error pages, not JSON responses")

if __name__ == "__main__":
    main()
