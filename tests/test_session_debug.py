import requests

def test_session_debug():
    """Debug session handling"""
    base_url = "http://localhost:8000"
    
    print("=== Debugging Session Handling ===")
    
    session = requests.Session()
    
    # Login as user
    login_data = {
        "username": "user",
        "password": "user123"
    }
    
    print("1. Logging in as user...")
    login_response = session.post(f"{base_url}/auth/login", data=login_data, allow_redirects=False)
    print(f"   Login response: {login_response.status_code}")
    print(f"   Login headers: {dict(login_response.headers)}")
    print(f"   Cookies after login: {session.cookies}")
    
    # Check if we have a session cookie
    session_token = None
    for cookie in session.cookies:
        if cookie.name == "session_token":
            session_token = cookie.value
            print(f"   Session token: {session_token[:20]}...")
            break
    
    if not session_token:
        print("   ❌ No session token found!")
        return
    
    # Try to access user search with the session
    print("\n2. Testing user search with session...")
    headers = {"Cookie": f"session_token={session_token}"}
    search_response = requests.get(f"{base_url}/user/search", headers=headers, allow_redirects=False)
    print(f"   Search response: {search_response.status_code}")
    print(f"   Search headers: {dict(search_response.headers)}")
    
    if search_response.status_code == 302:
        print(f"   Redirect location: {search_response.headers.get('location')}")
    
    # Test token verification directly
    print("\n3. Testing direct token verification...")
    verify_response = requests.get(f"{base_url}/auth/me", headers=headers)
    print(f"   Verify response: {verify_response.status_code}")
    if verify_response.status_code == 200:
        print(f"   User data: {verify_response.json()}")
    else:
        print(f"   Verify error: {verify_response.text}")

if __name__ == "__main__":
    test_session_debug()
