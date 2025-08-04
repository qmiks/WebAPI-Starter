#!/usr/bin/env python3
"""
Direct User Search Test
Test the /user/search endpoint directly to identify the error.
"""

import requests
import traceback

def test_user_search_direct():
    print("🔍 **Testing /user/search Directly**")
    print("=" * 45)
    
    base_url = "http://127.0.0.1:8000"
    
    # First login to get session cookie
    print("\n1️⃣ **Login to get session**")
    login_data = {
        "username": "user",
        "password": "user123", 
        "redirect_url": "/user/search"
    }
    
    try:
        login_response = requests.post(
            f"{base_url}/auth/login",
            data=login_data,
            allow_redirects=False
        )
        
        if login_response.status_code not in [302, 303]:
            print(f"   ❌ Login failed: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            return
            
        print(f"   ✅ Login successful: {login_response.status_code}")
        cookies = login_response.cookies
        print(f"   Session token: {cookies.get('session_token', 'None')[:50]}...")
        
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # Test direct access to /user/search  
    print("\n2️⃣ **Testing /user/search**")
    try:
        search_response = requests.get(
            f"{base_url}/user/search",
            cookies=cookies
        )
        
        print(f"   Status: {search_response.status_code}")
        
        if search_response.status_code == 500:
            print(f"   ❌ **INTERNAL SERVER ERROR!**")
            print(f"   Content-Type: {search_response.headers.get('content-type', 'unknown')}")
            print(f"   Response length: {len(search_response.text)}")
            print(f"   First 1000 chars: {search_response.text[:1000]}")
            
            # Try to extract error details
            if 'traceback' in search_response.text.lower() or 'exception' in search_response.text.lower():
                print("\n   🔍 **Potential error details found in response**")
                
        elif search_response.status_code == 200:
            print(f"   ✅ Success! Page loaded.")
            print(f"   Content length: {len(search_response.text)}")
            
            # Check if it looks like the correct page
            if 'search' in search_response.text.lower() and 'items' in search_response.text.lower():
                print(f"   ✅ Appears to be the search page")
            else:
                print(f"   ⚠️ Might not be the expected search page")
                
        else:
            print(f"   ⚠️ Unexpected status: {search_response.status_code}")
            print(f"   Response: {search_response.text[:300]}")
            
    except Exception as e:
        print(f"   ❌ Error accessing search: {e}")
        traceback.print_exc()

def test_admin_comparison():
    print("\n🔄 **Testing Admin Dashboard for comparison**")
    print("-" * 40)
    
    base_url = "http://127.0.0.1:8000"
    
    # Login as admin
    login_data = {
        "username": "admin",
        "password": "admin123",
        "redirect_url": "/admin"
    }
    
    try:
        login_response = requests.post(
            f"{base_url}/auth/login",
            data=login_data,
            allow_redirects=False
        )
        
        if login_response.status_code in [302, 303]:
            cookies = login_response.cookies
            
            # Test admin page
            admin_response = requests.get(f"{base_url}/admin", cookies=cookies)
            print(f"   Admin dashboard status: {admin_response.status_code}")
            
            if admin_response.status_code == 200:
                print(f"   ✅ Admin dashboard works fine")
            else:
                print(f"   ❌ Admin dashboard also has issues: {admin_response.status_code}")
                
    except Exception as e:
        print(f"   ❌ Admin test error: {e}")

def main():
    test_user_search_direct()
    test_admin_comparison()
    
    print("\n💡 **Next Steps:**")
    print("If user search fails but admin works, the issue is likely:")
    print("1. Missing imports in user_portal.py")
    print("2. Error in user/search.html template")
    print("3. Database access issue in user search logic")
    print("4. Session handling problem for regular users")

if __name__ == "__main__":
    main()
