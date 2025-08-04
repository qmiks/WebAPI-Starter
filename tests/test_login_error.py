#!/usr/bin/env python3
"""
Test Login Process
Simulate a login request to identify the Internal Server Error.
"""

import requests
import sys

def test_login():
    print("🧪 **Testing Login Process**")
    print("=" * 40)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test 1: Get login page first
    print("\n1️⃣ **Getting Login Page**")
    try:
        response = requests.get(f"{base_url}/auth/login?redirect_url=/user-portal")
        print(f"   Status: {response.status_code}")
        if response.status_code != 200:
            print(f"   Error: {response.text}")
            return
        print("   ✅ Login page loaded successfully")
    except Exception as e:
        print(f"   ❌ Error getting login page: {e}")
        return
    
    # Test 2: Submit login form
    print("\n2️⃣ **Submitting Login Form**")
    login_data = {
        "username": "user",
        "password": "user123",
        "redirect_url": "/user-portal"
    }
    
    try:
        response = requests.post(
            f"{base_url}/auth/login", 
            data=login_data,
            allow_redirects=False  # Don't follow redirects to see what happens
        )
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 303 or response.status_code == 302:
            redirect_url = response.headers.get('location', 'No location header')
            print(f"   ✅ Redirect to: {redirect_url}")
            
            # Test 3: Follow the redirect
            print("\n3️⃣ **Following Redirect**")
            try:
                if redirect_url.startswith('/'):
                    redirect_url = base_url + redirect_url
                
                # Get cookies from login response
                cookies = response.cookies
                
                redirect_response = requests.get(redirect_url, cookies=cookies)
                print(f"   Status: {redirect_response.status_code}")
                
                if redirect_response.status_code == 500:
                    print(f"   ❌ **INTERNAL SERVER ERROR FOUND!**")
                    print(f"   Response: {redirect_response.text[:500]}...")
                elif redirect_response.status_code == 200:
                    print(f"   ✅ Successfully accessed redirect target")
                    print(f"   Title: {extract_title(redirect_response.text)}")
                else:
                    print(f"   ⚠️ Unexpected status: {redirect_response.status_code}")
                    print(f"   Response: {redirect_response.text[:200]}...")
                    
            except Exception as e:
                print(f"   ❌ Error following redirect: {e}")
                
        elif response.status_code == 500:
            print(f"   ❌ **INTERNAL SERVER ERROR IN LOGIN!**")
            print(f"   Response: {response.text[:500]}...")
        else:
            print(f"   ⚠️ Unexpected login response: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ Error submitting login: {e}")

def extract_title(html):
    """Extract title from HTML"""
    try:
        start = html.find('<title>') + 7
        end = html.find('</title>')
        if start > 6 and end > start:
            return html[start:end]
    except:
        pass
    return "Could not extract title"

def test_admin_login():
    print("\n🔄 **Testing Admin Login**")
    print("-" * 30)
    
    base_url = "http://127.0.0.1:8000"
    login_data = {
        "username": "admin",
        "password": "admin123",
        "redirect_url": "/admin"
    }
    
    try:
        response = requests.post(
            f"{base_url}/auth/login", 
            data=login_data,
            allow_redirects=False
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code in [302, 303]:
            redirect_url = response.headers.get('location', 'No location')
            print(f"   Redirect: {redirect_url}")
            
            # Follow redirect
            if redirect_url.startswith('/'):
                redirect_url = base_url + redirect_url
            
            cookies = response.cookies
            redirect_response = requests.get(redirect_url, cookies=cookies)
            print(f"   Final Status: {redirect_response.status_code}")
            
            if redirect_response.status_code == 500:
                print(f"   ❌ **ADMIN LOGIN ALSO HAS ERROR!**")
            else:
                print(f"   ✅ Admin login works fine")
                
    except Exception as e:
        print(f"   ❌ Error testing admin login: {e}")

def main():
    test_login()
    test_admin_login()
    
    print("\n🔍 **Analysis:**")
    print("If Internal Server Error occurs during redirect,")
    print("the issue is likely in the target page (/user-portal or /user/search)")
    print("rather than in the login process itself.")

if __name__ == "__main__":
    main()
