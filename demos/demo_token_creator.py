#!/usr/bin/env python3
"""
Demo Client App Creator & Token Generator
Creates a demo client app and gets a Bearer token automatically.
"""

import requests
import json
from data.database import client_app_crud, generate_app_id, generate_app_secret
from data.models import ClientAppCreate

def create_demo_client_app():
    """Create a demo client app for testing."""
    print("[STRUCT] **Creating Demo Client App...**")
    
    try:
        # Generate new credentials
        app_id = generate_app_id()
        app_secret = generate_app_secret()
        
        # Create client app data
        app_data = ClientAppCreate(
            name="Demo Testing App",
            description="Automatically generated demo app for Bearer token testing"
        )
        
        # Use the CRUD function to create the app
        client_app = client_app_crud.create_client_app(app_data)
        
        if client_app:
            print("[OK] **Demo Client App Created Successfully!**")
            print(f"[LIST] **App ID:** {client_app['app_id']}")
            print(f"[CLIENT] **App Secret:** {client_app['app_secret']}")
            return client_app['app_id'], client_app['app_secret']
        else:
            print("[ERR] Failed to create demo client app")
            return None, None
            
    except Exception as e:
        print(f"[ERR] Error creating demo app: {e}")
        return None, None

def get_bearer_token(app_id, app_secret):
    """Get Bearer token using app credentials."""
    print("\n🎫 **Generating Bearer Token...**")
    
    try:
        response = requests.post("http://127.0.0.1:8000/api/v1/auth/token", 
            data={
                "app_id": app_id,
                "app_secret": app_secret,
                "expires_in": 3600
            }
        )
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            
            print("[OK] **Bearer Token Generated Successfully!**")
            print("=" * 60)
            print(f"🎫 **Your Bearer Token:**")
            print(f"Bearer {access_token}")
            print("=" * 60)
            
            return access_token
        else:
            print(f"[ERR] Token generation failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"[ERR] Error getting token: {e}")
        return None

def test_token(token):
    """Test the Bearer token with API call."""
    print("\n[TEST] **Testing Bearer Token...**")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("http://127.0.0.1:8000/api/v1/users/", headers=headers)
        
        if response.status_code == 200:
            users_data = response.json()
            print("[OK] **Token Works Perfect!**")
            print(f"[DATA] API Response: {len(users_data.get('users', []))} users found")
            return True
        else:
            print(f"⚠️ Token test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[ERR] Error testing token: {e}")
        return False

def show_usage_examples(token):
    """Show how to use the Bearer token."""
    print("\n[LIST] **Usage Examples:**")
    print("-" * 40)
    
    print("\n**[WEB] Swagger UI:**")
    print("1. Go to: http://127.0.0.1:8000/docs")
    print("2. Click 'Authorize' button 🔓")
    print(f"3. Enter: Bearer {token}")
    print("4. Click 'Authorize'")
    print("5. Try any endpoint!")
    
    print("\n**💻 Command Line (curl):**")
    print(f'curl -H "Authorization: Bearer {token}" \\')
    print('     http://127.0.0.1:8000/api/v1/users/')
    
    print("\n**[PYTHON] Python Code:**")
    print("```python")
    print("import requests")
    print()
    print(f'token = "{token}"')
    print('headers = {"Authorization": f"Bearer {token}"}')
    print()
    print('# Get all users')
    print('response = requests.get(')
    print('    "http://127.0.0.1:8000/api/v1/users/",')
    print('    headers=headers')
    print(')')
    print('users = response.json()')
    print('print(f"Found {len(users[\'users\'])} users")')
    print("```")

def main():
    print("[MIGRATE] **Demo Bearer Token Generator**")
    print("=" * 50)
    print("This script will:")
    print("1. Create a demo client app automatically")
    print("2. Generate a Bearer token")
    print("3. Test the token")
    print("4. Show you how to use it")
    print()
    
    # Create demo client app
    app_id, app_secret = create_demo_client_app()
    
    if not app_id or not app_secret:
        print("[ERR] Could not create demo client app")
        return
    
    # Get Bearer token
    token = get_bearer_token(app_id, app_secret)
    
    if not token:
        print("[ERR] Could not generate Bearer token")
        return
    
    # Test the token
    if test_token(token):
        # Show usage examples
        show_usage_examples(token)
        
        print("\n[SUMMARY] **Success!** Your Bearer token is ready to use!")
        print("\n🔗 **Quick Links:**")
        print(f"[API] Swagger UI: http://127.0.0.1:8000/docs")
        print(f"🏢 Admin Panel: http://127.0.0.1:8000/admin/client-apps/")
        
    else:
        print("[ERR] Token test failed")

if __name__ == "__main__":
    main()
