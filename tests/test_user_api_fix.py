#!/usr/bin/env python3

import requests
import json
from data.database import client_app_crud

def test_api_flow():
    # Get first active client app
    apps = client_app_crud.get_client_apps()
    if not apps:
        print("❌ No client apps found")
        return
        
    app = apps[0]  # Use first app
    app_id = app['app_id']
    app_secret = app['app_secret']
    
    print(f"🔐 Testing with App ID: {app_id}")
    print(f"📱 App Name: {app['name']}")
    
    # Test 1: Generate API token
    print("\n1️⃣ Testing API token generation...")
    token_data = {
        "app_id": app_id,
        "app_secret": app_secret,
        "expires_in": 3600
    }
    token_response = requests.post("http://localhost:8000/api/v1/auth/token", data=token_data)
    
    print(f"Token Response Status: {token_response.status_code}")
    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data['access_token']
        print(f"✅ Token generated successfully")
        print(f"🎫 Token: {access_token[:50]}...")
        
        # Test 2: Use token to access users endpoint
        print("\n2️⃣ Testing users endpoint with token...")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        users_response = requests.get("http://localhost:8000/api/v1/users", headers=headers)
        print(f"Users Response Status: {users_response.status_code}")
        
        if users_response.status_code == 200:
            users_data = users_response.json()
            print(f"✅ Users endpoint accessible")
            print(f"👥 Found {len(users_data)} users")
        else:
            print(f"❌ Users endpoint failed")
            print(f"Error: {users_response.text}")
            
        # Test 3: Test specific user endpoint
        print("\n3️⃣ Testing specific user endpoint...")
        user_response = requests.get("http://localhost:8000/api/v1/users/1", headers=headers)
        print(f"User 1 Response Status: {user_response.status_code}")
        
        if user_response.status_code == 200:
            print(f"✅ User 1 endpoint accessible")
        else:
            print(f"❌ User 1 endpoint failed")
            print(f"Error: {user_response.text}")
            
    else:
        print(f"❌ Token generation failed")
        print(f"Error: {token_response.text}")

if __name__ == "__main__":
    test_api_flow()
