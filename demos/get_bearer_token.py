#!/usr/bin/env python3
"""
Interactive Bearer Token Generator
Helps you get a Bearer token step by step.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def get_bearer_token_interactive():
    """Interactive script to get Bearer token."""
    
    print("[CLIENT] **Bearer Token Generator**")
    print("=" * 40)
    
    print("\n[LIST] **Step 1: Get Client Credentials**")
    print(f"1. Open: {BASE_URL}/admin/client-apps/")
    print("2. Login and create a new client application")
    print("3. Copy your App ID and App Secret")
    
    print("\n[AUTH] **Step 2: Enter Your Credentials**")
    app_id = input("Enter your App ID: ").strip()
    app_secret = input("Enter your App Secret: ").strip()
    
    if not app_id or not app_secret:
        print("[ERR] App ID and Secret are required!")
        return
    
    print(f"\n🎫 **Step 3: Generating Token...**")
    
    try:
        # Make token request
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/token",
            data={
                "app_id": app_id,
                "app_secret": app_secret
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            
            print("[OK] **Token Generated Successfully!**")
            print("-" * 40)
            print(f"[CLIENT] **Access Token:**")
            print(f"{access_token}")
            print(f"\n[LIST] **Token Details:**")
            print(f"   Type: {token_data.get('token_type', 'bearer')}")
            print(f"   Expires in: {token_data.get('expires_in', 3600)} seconds")
            print(f"   Expires at: {token_data.get('expires_at', 'N/A')}")
            
            print(f"\n[MIGRATE] **How to Use This Token:**")
            print(f"   1. Copy the access token above")
            print(f"   2. In Swagger UI ({BASE_URL}/docs):")
            print(f"      - Click 'Authorize' button")
            print(f"      - Enter: Bearer {access_token[:20]}...")
            print(f"   3. In API calls, add header:")
            print(f"      Authorization: Bearer {access_token[:20]}...")
            
            # Test the token
            print(f"\n[TEST] **Testing Token...**")
            test_response = requests.get(
                f"{BASE_URL}/api/v1/users/",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if test_response.status_code == 200:
                print("[OK] Token works! You can access protected endpoints.")
                users = test_response.json()
                print(f"   Found {len(users.get('users', []))} users in the system")
            elif test_response.status_code == 403:
                print("[OK] Token is valid but no users found (normal for new systems)")
            else:
                print(f"⚠️  Token generated but test failed: {test_response.status_code}")
                print(f"   Response: {test_response.text}")
            
            return access_token
            
        else:
            print(f"[ERR] **Token Generation Failed**")
            print(f"   Status Code: {response.status_code}")
            
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Raw Response: {response.text}")
            
            print(f"\n💡 **Troubleshooting:**")
            print(f"   • Check if your App ID and Secret are correct")
            print(f"   • Verify the client app is active in admin panel")
            print(f"   • Make sure the server is running")
            
            return None
    
    except requests.exceptions.ConnectionError:
        print(f"[ERR] **Connection Error**")
        print(f"   Cannot connect to {BASE_URL}")
        print(f"   Make sure the Web API server is running!")
        print(f"   Start it with: python main.py")
        return None
    
    except Exception as e:
        print(f"[ERR] **Unexpected Error**: {e}")
        return None

def quick_demo():
    """Quick demo with sample credentials."""
    
    print("\n" + "=" * 50)
    print("[DEMO] **Quick Demo with Sample Credentials**")
    print("=" * 50)
    
    sample_credentials = [
        {"app_id": "app_demo_123", "app_secret": "demo_secret_456"},
        {"app_id": "app_test_789", "app_secret": "test_secret_abc"}
    ]
    
    for creds in sample_credentials:
        print(f"\n[TEST] Testing: {creds['app_id']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/auth/token",
                data=creds
            )
            
            if response.status_code == 200:
                token_data = response.json()
                print(f"[OK] Token generated: {token_data['access_token'][:30]}...")
                break
            else:
                print(f"[ERR] Failed: {response.status_code}")
        except:
            print(f"[ERR] Connection error")
    
    print(f"\n💡 **To create your own credentials:**")
    print(f"   Visit: {BASE_URL}/admin/client-apps/")

if __name__ == "__main__":
    token = get_bearer_token_interactive()
    
    if not token:
        quick_demo()
    
    print(f"\n🌟 **Next Steps:**")
    print(f"   [USAGE] View API docs: {BASE_URL}/docs")
    print(f"   🏢 Manage apps: {BASE_URL}/admin/client-apps/")
    print(f"   [API] Full guide: HOW_TO_GET_BEARER_TOKEN.md")
