#!/usr/bin/env python3
"""
Improved API Test with Better Credential Extraction
"""

import requests
import re
from bs4 import BeautifulSoup

def extract_credentials_from_html(html):
    """Extract app credentials from HTML using BeautifulSoup"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all credential values
        credential_values = soup.find_all('code', class_='credential-value')
        
        if len(credential_values) >= 2:
            app_id = credential_values[0].get_text().strip()
            app_secret_partial = credential_values[1].get_text().strip()
            
            print(f"   Found App ID: {app_id}")
            print(f"   Found Secret (partial): {app_secret_partial}")
            
            # The secret is truncated in display, we need the full one
            # Look for the full secret in the onclick handlers
            onclick_pattern = r"generateTestToken\('([^']+)',\s*'([^']+)',\s*'[^']+'\)"
            onclick_matches = re.findall(onclick_pattern, html)
            
            if onclick_matches:
                full_app_id, full_secret = onclick_matches[0]
                print(f"   Full App ID: {full_app_id}")
                print(f"   Full Secret: {full_secret[:10]}...")
                return full_app_id, full_secret
            
            # Fallback: use what we found (might be truncated)
            return app_id, app_secret_partial.replace('...', '')
        
        return None, None
        
    except Exception as e:
        print(f"   Error parsing HTML: {e}")
        return None, None

def run_complete_api_test():
    """Complete API test with improved credential extraction"""
    print("🚀 **Complete API Test with Improved Extraction**")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    
    # Step 1: Admin login
    print("   Step 1: Admin login...")
    session = requests.Session()
    login_data = {"username": "admin", "password": "admin123"}
    
    login_response = session.post(f"{base_url}/auth/login", data=login_data)
    print(f"   Login: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print(f"   ❌ Login failed")
        return
    
    # Step 2: Create client app
    print("   Step 2: Creating client app...")
    app_data = {
        "name": "Complete Test App", 
        "description": "Test app for complete API testing"
    }
    
    create_response = session.post(f"{base_url}/admin/client-apps/create", data=app_data)
    print(f"   Create app: {create_response.status_code}")
    
    if create_response.status_code == 500:
        print(f"   ❌ **INTERNAL SERVER ERROR during app creation!**")
        print(f"   Response: {create_response.text}")
        return
    elif create_response.status_code != 200:
        print(f"   ❌ App creation failed: {create_response.status_code}")
        return
    
    print(f"   ✅ App created successfully")
    
    # Step 3: Extract credentials from the response (it should contain the new app)
    print("   Step 3: Extracting credentials...")
    
    # The create response should contain the updated page with our new app
    app_id, app_secret = extract_credentials_from_html(create_response.text)
    
    if not app_id or not app_secret:
        print(f"   Trying apps list page...")
        apps_response = session.get(f"{base_url}/admin/client-apps/")
        if apps_response.status_code == 200:
            app_id, app_secret = extract_credentials_from_html(apps_response.text)
    
    if not app_id or not app_secret:
        print(f"   ❌ Could not extract credentials")
        return
    
    print(f"   ✅ Credentials extracted successfully")
    
    # Step 4: Test token generation
    print("   Step 4: Testing token generation...")
    token_data = {
        "app_id": app_id,
        "app_secret": app_secret,
        "expires_in": 3600
    }
    
    token_response = requests.post(f"{base_url}/api/v1/auth/token", data=token_data)
    print(f"   Token response: {token_response.status_code}")
    
    if token_response.status_code == 500:
        print(f"   ❌ **INTERNAL SERVER ERROR in token generation!**")
        print(f"   Response: {token_response.text}")
        
        # Let's check what's in the server logs
        print(f"   📋 Debugging token generation...")
        print(f"   App ID sent: '{app_id}'")
        print(f"   Secret sent: '{app_secret[:10]}...'")
        return
        
    elif token_response.status_code != 200:
        print(f"   ❌ Token generation failed: {token_response.status_code}")
        print(f"   Response: {token_response.text}")
        return
    
    token_info = token_response.json()
    token = token_info.get('access_token')
    print(f"   ✅ Token generated: {token[:50]}...")
    
    # Step 5: Test API endpoints
    print("   Step 5: Testing API endpoints...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    endpoints_to_test = [
        ("/api/v1/users/", "Users"),
        ("/api/v1/items/", "Items")
    ]
    
    for endpoint, name in endpoints_to_test:
        print(f"   Testing {name} API ({endpoint})...")
        
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            print(f"   {name} response: {response.status_code}")
            
            if response.status_code == 500:
                print(f"   ❌ **INTERNAL SERVER ERROR in {name} API!**")
                print(f"   Error response: {response.text}")
                print(f"   Headers: {dict(response.headers)}")
                
                # This is what we're looking for!
                break
                
            elif response.status_code == 200:
                print(f"   ✅ {name} API successful")
                try:
                    data = response.json()
                    items_key = name.lower()
                    count = len(data.get(items_key, []))
                    print(f"   {name} count: {count}")
                except:
                    print(f"   Response length: {len(response.text)} chars")
                    
            elif response.status_code == 401:
                print(f"   ❌ Unauthorized - token issue")
                print(f"   Response: {response.text}")
                
            else:
                print(f"   ⚠️ Unexpected {name} status: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ Error calling {name} API: {e}")
    
    print(f"\n   🏁 Complete API test finished!")

if __name__ == "__main__":
    # Check if BeautifulSoup is available
    try:
        from bs4 import BeautifulSoup
        run_complete_api_test()
    except ImportError:
        print("❌ BeautifulSoup not available. Installing...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
        from bs4 import BeautifulSoup
        run_complete_api_test()
