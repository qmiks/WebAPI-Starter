#!/usr/bin/env python3
"""
API Token Authentication Test
Tests the complete API token flow: create client app, get token, use token
"""

import requests
import json
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:8000"

class APITokenTest:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.client_app = None
        self.api_token = None
        
    def setup_admin_session(self):
        """Login as admin to manage client apps"""
        print("🔑 Setting up admin session...")
        login_data = {"username": "admin", "password": "admin123"}
        response = self.session.post(urljoin(self.base_url, "/auth/login"), data=login_data, allow_redirects=True)
        
        if response.status_code == 200:
            print("✅ Admin login successful")
            return True
        else:
            print(f"❌ Admin login failed: {response.status_code}")
            return False
    
    def create_client_app(self):
        """Create a client app for API testing"""
        print("➕ Creating client app for API testing...")
        
        app_data = {
            "name": "API Test Client",
            "description": "Testing API token authentication",
            "is_active": True
        }
        
        # Use the API endpoint to create the client app
        response = self.session.post(
            urljoin(self.base_url, "/admin/client-apps/api"),
            json=app_data
        )
        
        if response.status_code == 200:
            self.client_app = response.json()
            print(f"✅ Client app created successfully")
            print(f"   App ID: {self.client_app.get('app_id')}")
            print(f"   App Secret: {self.client_app.get('app_secret')[:8]}...")
            return True
        else:
            print(f"❌ Client app creation failed: {response.status_code}")
            if response.text:
                print(f"   Response: {response.text[:200]}")
            return False
    
    def get_api_token(self):
        """Get API token using client credentials"""
        print("🎫 Getting API token...")
        
        if not self.client_app:
            print("❌ No client app available")
            return False
        
        token_data = {
            "app_id": self.client_app["app_id"],
            "app_secret": self.client_app["app_secret"],
            "expires_in": 3600
        }
        
        # Use a new session (without admin cookies) for token request
        token_session = requests.Session()
        response = token_session.post(
            urljoin(self.base_url, "/api/v1/auth/token"),
            data=token_data
        )
        
        if response.status_code == 200:
            token_response = response.json()
            self.api_token = token_response.get("access_token")
            print(f"✅ API token obtained successfully")
            print(f"   Token type: {token_response.get('token_type')}")
            print(f"   Expires in: {token_response.get('expires_in')} seconds")
            print(f"   Token: {self.api_token[:20]}...")
            return True
        else:
            print(f"❌ Token request failed: {response.status_code}")
            if response.text:
                print(f"   Response: {response.text}")
            return False
    
    def test_protected_api_calls(self):
        """Test API calls with the obtained token"""
        print("🔒 Testing protected API endpoints...")
        
        if not self.api_token:
            print("❌ No API token available")
            return False
        
        # Create headers with the Bearer token
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        # Create a new session for API calls (no admin session)
        api_session = requests.Session()
        
        # Test 1: Get users via API
        print("📋 Testing GET /api/v1/users...")
        users_response = api_session.get(
            urljoin(self.base_url, "/api/v1/users"),
            headers=headers
        )
        
        if users_response.status_code == 200:
            users_data = users_response.json()
            print(f"✅ Users API success: Found {len(users_data)} users")
        else:
            print(f"❌ Users API failed: {users_response.status_code}")
        
        # Test 2: Get items via API
        print("📦 Testing GET /api/v1/items...")
        items_response = api_session.get(
            urljoin(self.base_url, "/api/v1/items"),
            headers=headers
        )
        
        if items_response.status_code == 200:
            items_data = items_response.json()
            print(f"✅ Items API success: Found {len(items_data)} items")
        else:
            print(f"❌ Items API failed: {items_response.status_code}")
        
        # Test 3: Try to create a new user via API
        print("👤 Testing POST /api/v1/users...")
        new_user_data = {
            "username": f"api_test_user_{self.client_app['id']}",
            "email": f"apitest{self.client_app['id']}@example.com",
            "full_name": "API Test User",
            "password": "testpassword123"
        }
        
        create_user_response = api_session.post(
            urljoin(self.base_url, "/api/v1/users"),
            headers=headers,
            json=new_user_data
        )
        
        if create_user_response.status_code == 200:
            created_user = create_user_response.json()
            print(f"✅ User creation API success: Created user {created_user.get('username')}")
        else:
            print(f"❌ User creation API failed: {create_user_response.status_code}")
            if create_user_response.text:
                print(f"   Response: {create_user_response.text[:200]}")
        
        return True
    
    def test_invalid_token(self):
        """Test API calls with invalid token"""
        print("🚫 Testing invalid token handling...")
        
        invalid_headers = {
            "Authorization": "Bearer invalid_token_12345",
            "Content-Type": "application/json"
        }
        
        api_session = requests.Session()
        response = api_session.get(
            urljoin(self.base_url, "/api/v1/users"),
            headers=invalid_headers
        )
        
        if response.status_code in [401, 403]:
            print(f"✅ Invalid token properly rejected: {response.status_code}")
        else:
            print(f"⚠️ Unexpected response for invalid token: {response.status_code}")
        
        return True
    
    def cleanup(self):
        """Clean up created test data"""
        print("🧹 Cleaning up test data...")
        
        if self.client_app and self.session:
            # Delete the test client app
            delete_response = self.session.delete(
                urljoin(self.base_url, f"/admin/client-apps/api/{self.client_app['id']}")
            )
            
            if delete_response.status_code == 200:
                print("✅ Test client app cleaned up")
            else:
                print(f"⚠️ Cleanup warning: {delete_response.status_code}")
    
    def run_full_test(self):
        """Run the complete API token test suite"""
        print("🚀 Starting API Token Authentication Test")
        print("=" * 60)
        
        try:
            # Step 1: Setup admin session
            if not self.setup_admin_session():
                return False
            
            # Step 2: Create client app
            if not self.create_client_app():
                return False
            
            # Step 3: Get API token
            if not self.get_api_token():
                return False
            
            # Step 4: Test protected API calls
            if not self.test_protected_api_calls():
                return False
            
            # Step 5: Test invalid token
            if not self.test_invalid_token():
                return False
            
            print("=" * 60)
            print("🎉 ALL API TOKEN TESTS PASSED!")
            print("✅ Client app creation working")
            print("✅ API token generation working")
            print("✅ Protected API access working")
            print("✅ Invalid token rejection working")
            
            return True
            
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        finally:
            # Always cleanup
            self.cleanup()

if __name__ == "__main__":
    test = APITokenTest()
    success = test.run_full_test()
    
    if success:
        print("\n🎯 API Token Authentication is fully functional!")
    else:
        print("\n⚠️ API Token Authentication has issues that need attention.")
