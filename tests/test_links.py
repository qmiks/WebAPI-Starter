#!/usr/bin/env python3
"""
Link Test Script
Tests all navigation links in the application
"""

import requests
import sys
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:8000"

def test_url(path, description="", expected_status=200):
    """Test a URL and return success status"""
    url = urljoin(BASE_URL, path)
    try:
        response = requests.get(url, allow_redirects=False)
        success = response.status_code == expected_status or (expected_status == 200 and response.status_code in [200, 302])
        status_symbol = "✅" if success else "❌"
        print(f"{status_symbol} {path:<30} [{response.status_code}] {description}")
        return success
    except Exception as e:
        print(f"❌ {path:<30} [ERROR] {e}")
        return False

def test_all_links():
    """Test all important navigation links"""
    
    print("🔗 Testing Navigation Links")
    print("=" * 60)
    
    # Public pages
    test_url("/", "Landing page")
    test_url("/docs", "API Documentation")
    test_url("/auth/login", "Login page")
    
    print("\n🔒 Authentication Required Pages (expect 302 redirect)")
    print("=" * 60)
    
    # Admin routes (expect redirect to login)
    test_url("/admin", "Admin dashboard", 302)
    test_url("/admin/users", "Admin users page", 302)
    test_url("/admin/items", "Admin items page", 302)
    test_url("/admin/users/new", "Admin new user page", 302)
    test_url("/admin/items/new", "Admin new item page", 302)
    
    # User routes (expect redirect to login)
    test_url("/user/dashboard", "User dashboard", 302)
    test_url("/user/items", "User items page", 302)
    test_url("/user/items/new", "User new item page", 302)
    test_url("/user/profile", "User profile page", 302)
    
    print("\n🌐 Language Support")
    print("=" * 60)
    
    # Test language parameters
    test_url("/?lang=en", "English landing")
    test_url("/?lang=pl", "Polish landing")
    test_url("/auth/login?lang=pl", "Polish login")
    
    print("\n📊 Summary")
    print("=" * 60)
    print("All key navigation links tested!")
    print("Note: 302 redirects are expected for authenticated pages when not logged in.")

if __name__ == "__main__":
    test_all_links()
