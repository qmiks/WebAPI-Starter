#!/usr/bin/env python3
"""
Test API Edge Cases
Test various scenarios that might cause Internal Server Error.
"""

import requests
import json

def test_api_edge_cases():
    """Test various edge cases that might cause 500 errors"""
    print("🔬 **Testing API Edge Cases**")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    # First, get a valid token
    print("   Setting up valid token...")
    
    # Create app and get token (reusing working code)
    session = requests.Session()
    login_data = {"username": "admin", "password": "admin123"}
    session.post(f"{base_url}/auth/login", data=login_data)
    
    app_data = {"name": "Edge Test App", "description": "For edge case testing"}
    create_response = session.post(f"{base_url}/admin/client-apps/create", data=app_data)
    
    # Extract credentials using regex from the previous test
    import re
    onclick_pattern = r"generateTestToken\('([^']+)',\s*'([^']+)',\s*'[^']+'\)"
    onclick_matches = re.findall(onclick_pattern, create_response.text)
    
    if not onclick_matches:
        print("   ❌ Could not set up test app")
        return
    
    app_id, app_secret = onclick_matches[0]
    
    # Get valid token
    token_data = {"app_id": app_id, "app_secret": app_secret, "expires_in": 3600}
    token_response = requests.post(f"{base_url}/api/v1/auth/token", data=token_data)
    
    if token_response.status_code != 200:
        print(f"   ❌ Could not get valid token: {token_response.status_code}")
        return
    
    valid_token = token_response.json()['access_token']
    print(f"   ✅ Valid token obtained")
    
    # Now test edge cases
    test_cases = [
        ("Invalid token", {"Authorization": "Bearer invalid_token"}),
        ("Malformed token", {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid"}),
        ("No Authorization header", {}),
        ("Wrong auth scheme", {"Authorization": "Basic dGVzdA=="}),
        ("Empty token", {"Authorization": "Bearer "}),
        ("Valid token", {"Authorization": f"Bearer {valid_token}"}),
    ]
    
    endpoints = [
        ("/api/v1/users/", "Users"),
        ("/api/v1/items/", "Items"),
        ("/api/v1/users/999", "User by ID"),
        ("/api/v1/items/999", "Item by ID"),
    ]
    
    for case_name, headers in test_cases:
        print(f"\n   🧪 Testing case: {case_name}")
        
        for endpoint, endpoint_name in endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=10)
                status = response.status_code
                
                if status == 500:
                    print(f"   ❌ **500 ERROR in {endpoint_name}** with {case_name}")
                    print(f"      Endpoint: {endpoint}")
                    print(f"      Headers: {headers}")
                    print(f"      Response: {response.text[:200]}")
                    print(f"      Response headers: {dict(response.headers)}")
                elif status in [200, 401, 403, 404]:
                    print(f"   ✅ {endpoint_name}: {status} (expected)")
                else:
                    print(f"   ⚠️ {endpoint_name}: {status} (unexpected)")
                    
            except Exception as e:
                print(f"   ❌ Error calling {endpoint_name}: {e}")

def test_api_with_post_requests():
    """Test POST requests which might have different error handling"""
    print("\n🚀 **Testing POST Requests**")
    print("-" * 30)
    
    base_url = "http://127.0.0.1:8000"
    
    # Get valid token (same setup as before)
    session = requests.Session()
    login_data = {"username": "admin", "password": "admin123"}
    session.post(f"{base_url}/auth/login", data=login_data)
    
    app_data = {"name": "POST Test App", "description": "For POST testing"}
    create_response = session.post(f"{base_url}/admin/client-apps/create", data=app_data)
    
    import re
    onclick_pattern = r"generateTestToken\('([^']+)',\s*'([^']+)',\s*'[^']+'\)"
    onclick_matches = re.findall(onclick_pattern, create_response.text)
    
    if onclick_matches:
        app_id, app_secret = onclick_matches[0]
        token_data = {"app_id": app_id, "app_secret": app_secret, "expires_in": 3600}
        token_response = requests.post(f"{base_url}/api/v1/auth/token", data=token_data)
        
        if token_response.status_code == 200:
            valid_token = token_response.json()['access_token']
            headers = {
                "Authorization": f"Bearer {valid_token}",
                "Content-Type": "application/json"
            }
            
            # Test POST requests
            post_tests = [
                {
                    "name": "Create User",
                    "endpoint": "/api/v1/users/",
                    "data": {
                        "username": "testuser",
                        "email": "test@example.com",
                        "full_name": "Test User",
                        "password": "testpass123"
                    }
                },
                {
                    "name": "Create Item", 
                    "endpoint": "/api/v1/items/",
                    "data": {
                        "name": "Test Item",
                        "description": "Test item description",
                        "price": 99.99,
                        "status": "AVAILABLE"
                    }
                }
            ]
            
            for test in post_tests:
                print(f"   Testing {test['name']}...")
                try:
                    response = requests.post(
                        f"{base_url}{test['endpoint']}", 
                        headers=headers,
                        json=test['data'],
                        timeout=10
                    )
                    
                    print(f"   {test['name']}: {response.status_code}")
                    
                    if response.status_code == 500:
                        print(f"   ❌ **500 ERROR in {test['name']}**")
                        print(f"      Response: {response.text}")
                    elif response.status_code in [200, 201]:
                        print(f"   ✅ {test['name']} successful")
                        try:
                            data = response.json()
                            print(f"      Created: {data.get('username') or data.get('name', 'Unknown')}")
                        except:
                            print(f"      Response length: {len(response.text)} chars")
                    else:
                        print(f"   ⚠️ {test['name']}: {response.status_code}")
                        print(f"      Response: {response.text[:200]}")
                        
                except Exception as e:
                    print(f"   ❌ Error in {test['name']}: {e}")

def test_concurrent_requests():
    """Test concurrent API requests"""
    print("\n🔄 **Testing Concurrent Requests**")
    print("-" * 30)
    
    import threading
    import time
    
    base_url = "http://127.0.0.1:8000"
    errors = []
    
    # Get valid token
    session = requests.Session()
    login_data = {"username": "admin", "password": "admin123"}
    session.post(f"{base_url}/auth/login", data=login_data)
    
    app_data = {"name": "Concurrent Test App", "description": "For concurrent testing"}
    create_response = session.post(f"{base_url}/admin/client-apps/create", data=app_data)
    
    import re
    onclick_pattern = r"generateTestToken\('([^']+)',\s*'([^']+)',\s*'[^']+'\)"
    onclick_matches = re.findall(onclick_pattern, create_response.text)
    
    if onclick_matches:
        app_id, app_secret = onclick_matches[0]
        token_data = {"app_id": app_id, "app_secret": app_secret, "expires_in": 3600}
        token_response = requests.post(f"{base_url}/api/v1/auth/token", data=token_data)
        
        if token_response.status_code == 200:
            valid_token = token_response.json()['access_token']
            headers = {"Authorization": f"Bearer {valid_token}"}
            
            def make_request(thread_id):
                try:
                    response = requests.get(f"{base_url}/api/v1/users/", headers=headers)
                    if response.status_code == 500:
                        errors.append(f"Thread {thread_id}: 500 error - {response.text[:100]}")
                    elif response.status_code != 200:
                        errors.append(f"Thread {thread_id}: {response.status_code} - {response.text[:100]}")
                except Exception as e:
                    errors.append(f"Thread {thread_id}: Exception - {e}")
            
            # Launch multiple concurrent requests
            threads = []
            for i in range(10):
                thread = threading.Thread(target=make_request, args=(i,))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads
            for thread in threads:
                thread.join()
            
            if errors:
                print(f"   ❌ Found {len(errors)} errors in concurrent requests:")
                for error in errors[:5]:  # Show first 5 errors
                    print(f"      {error}")
            else:
                print(f"   ✅ All 10 concurrent requests successful")

def main():
    print("🔬 **API Edge Case Testing**")
    print("=" * 60)
    
    test_api_edge_cases()
    test_api_with_post_requests()
    test_concurrent_requests()
    
    print("\n" + "=" * 60)
    print("🏁 **Edge Case Testing Complete**")

if __name__ == "__main__":
    main()
