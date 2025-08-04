import requests

def test_user_search_access():
    """Test direct access to user search after login"""
    base_url = "http://localhost:8000"
    
    print("=== Testing User Search Access ===")
    
    session = requests.Session()
    
    # Login as user
    login_data = {
        "username": "user123",
        "password": "userpass"
    }
    
    print("1. Logging in as user...")
    login_response = session.post(f"{base_url}/auth/login", data=login_data)
    print(f"   Login response: {login_response.status_code}")
    print(f"   Cookies: {session.cookies}")
    
    if login_response.status_code == 200:
        print("   ✅ User login successful!")
        
        # Test direct access to /user/search
        print("\n2. Testing direct access to /user/search...")
        search_response = session.get(f"{base_url}/user/search")
        print(f"   Search response: {search_response.status_code}")
        print(f"   Final URL: {search_response.url}")
        
        if search_response.status_code == 200:
            print("   ✅ User search accessible!")
            print(f"   Page contains 'Search': {'Search' in search_response.text}")
            print(f"   Page contains 'Items': {'Items' in search_response.text}")
        else:
            print(f"   ❌ Search access failed: {search_response.status_code}")
            print(f"   Content preview: {search_response.text[:200]}")
    else:
        print(f"   ❌ User login failed: {login_response.status_code}")

if __name__ == "__main__":
    test_user_search_access()
