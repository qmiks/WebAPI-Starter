#!/usr/bin/env python3
"""
API Token Demo Script
===================

This script demonstrates how to use API tokens with the FastAPI application.

Before running this script:
1. Create a client app in the admin panel: http://127.0.0.1:8000/admin/client-apps/
2. Copy the App ID and App Secret
3. Set them as environment variables or modify the script below

Usage:
    python api_token_demo.py
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"

# IMPORTANT: Replace these with your actual client app credentials
# You can get these from: http://127.0.0.1:8000/admin/client-apps/
APP_ID = "app_example123"  # Replace with your actual App ID
APP_SECRET = "your_secret_here"  # Replace with your actual App Secret

def get_api_token(app_id, app_secret, expires_in=3600):
    """
    Step 1: Get an API token using client app credentials
    """
    print(f"[CLIENT] Getting API token...")
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/token", 
        data={
            "app_id": app_id,
            "app_secret": app_secret,
            "expires_in": expires_in
        }
    )
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"[OK] Token obtained successfully!")
        print(f"   Token type: {token_data['token_type']}")
        print(f"   Expires in: {token_data['expires_in']} seconds")
        print(f"   Token preview: {token_data['access_token'][:50]}...")
        return token_data["access_token"]
    else:
        print(f"[ERR] Failed to get token: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def test_api_endpoints(token):
    """
    Step 2: Test various API endpoints with the token
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"\n[TEST] Testing API endpoints with token...")
    
    # Test 1: Get all users
    print(f"\n1️⃣ Testing GET /api/v1/users")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/users", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Success! Found {data['total']} users")
            print(f"   Users on this page: {len(data['users'])}")
            if data['users']:
                print(f"   First user: {data['users'][0]['username']} ({data['users'][0]['email']})")
        else:
            print(f"[ERR] Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERR] Error: {e}")
    
    # Test 2: Get specific user
    print(f"\n2️⃣ Testing GET /api/v1/users/1")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/users/1", headers=headers)
        if response.status_code == 200:
            user = response.json()
            print(f"[OK] Success! User: {user['username']} ({user['email']})")
            print(f"   Role: {user['role']}")
            print(f"   Active: {user['is_active']}")
        else:
            print(f"[ERR] Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERR] Error: {e}")
    
    # Test 3: Test without token (should fail)
    print(f"\n3️⃣ Testing API without token (should fail)")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/users")
        print(f"[ERR] Expected failure: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERR] Error: {e}")

def test_token_expiration():
    """
    Step 3: Test token expiration
    """
    print(f"\n⏰ Testing token expiration...")
    
    # Get a token that expires in 5 seconds
    token = get_api_token(APP_ID, APP_SECRET, expires_in=5)
    if not token:
        return
    
    # Use token immediately (should work)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/v1/users", headers=headers)
    print(f"   Immediate use: {response.status_code} ({'[OK] Success' if response.status_code == 200 else '[ERR] Failed'})")
    
    # Wait for token to expire
    print(f"   Waiting 6 seconds for token to expire...")
    time.sleep(6)
    
    # Try to use expired token (should fail)
    response = requests.get(f"{BASE_URL}/api/v1/users", headers=headers)
    print(f"   After expiration: {response.status_code} ({'[ERR] Expected failure' if response.status_code == 401 else '⚠️ Unexpected'})")

def main():
    """
    Main demo function
    """
    print("[MIGRATE] FastAPI Token Demo")
    print("=" * 50)
    
    # Check if credentials are set
    if APP_ID == "app_example123" or APP_SECRET == "your_secret_here":
        print("[ERR] Please update APP_ID and APP_SECRET in this script!")
        print("   1. Go to: http://127.0.0.1:8000/admin/client-apps/")
        print("   2. Create a new client app")
        print("   3. Copy the App ID and App Secret")
        print("   4. Update this script with your credentials")
        return
    
    # Step 1: Get token
    token = get_api_token(APP_ID, APP_SECRET)
    if not token:
        print("[ERR] Cannot proceed without a valid token")
        return
    
    # Step 2: Test API endpoints
    test_api_endpoints(token)
    
    # Step 3: Test token expiration
    test_token_expiration()
    
    print(f"\n[SUMMARY] Demo completed!")
    print(f"\nNext steps:")
    print(f"   • View API documentation: {BASE_URL}/docs")
    print(f"   • Manage client apps: {BASE_URL}/admin/client-apps/")
    print(f"   • Check admin dashboard: {BASE_URL}/admin/")

if __name__ == "__main__":
    main()
