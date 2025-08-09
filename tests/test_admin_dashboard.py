#!/usr/bin/env python3
"""
Simple admin dashboard test to check rendering
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_admin_login():
    """Test admin login"""
    print("🔐 Testing Admin Login...")
    
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    session = requests.Session()
    response = session.post(f"{BASE_URL}/auth/login", data=login_data, allow_redirects=False)
    
    if response.status_code in [302, 303]:
        print("✅ Admin login successful")
        return session
    else:
        print(f"❌ Admin login failed: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        return None

def test_admin_pages(session):
    """Test admin pages for rendering issues"""
    print("\n📊 Testing Admin Pages...")
    
    pages = [
        ("/admin", "Admin Dashboard"),
        ("/admin/users", "Users Management"),
        ("/admin/items", "Items Management"),
    ]
    
    for url, name in pages:
        response = session.get(f"{BASE_URL}{url}")
        
        if response.status_code == 200:
            # Check if the page contains expected content
            if "<!DOCTYPE html>" in response.text and "<html" in response.text:
                print(f"✅ {name} page loads correctly")
                
                # Check for common errors
                if "error" in response.text.lower() and "500" in response.text:
                    print(f"⚠️  {name} may have server errors")
                elif "undefined" in response.text.lower():
                    print(f"⚠️  {name} may have undefined variables")
                else:
                    print(f"   ✓ No obvious errors detected")
            else:
                print(f"❌ {name} returned malformed HTML")
        else:
            print(f"❌ {name} failed to load: {response.status_code}")

def main():
    """Run admin dashboard tests"""
    print("🧪 Testing Admin Dashboard Rendering")
    print("=" * 50)
    
    session = test_admin_login()
    if session:
        test_admin_pages(session)
        print("\n✅ Admin dashboard tests completed!")
    else:
        print("\n❌ Could not test admin pages - login failed")

if __name__ == "__main__":
    main()
