#!/usr/bin/env python3
"""
Test User Portal Admin Links
Reproduce the specific issue with regular user clicking admin links from user portal.
"""

import requests

def test_user_portal_admin_links():
    print("🔍 **Testing User Portal Admin Links**")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    # Login as regular user
    session = requests.Session()
    login_data = {
        "username": "user",
        "password": "user123"
    }
    
    login_response = session.post(f"{base_url}/auth/login", data=login_data)
    print(f"✅ Logged in as regular user")
    
    # Go to user portal first
    print(f"\n1️⃣ **Accessing User Portal**")
    user_portal_response = session.get(f"{base_url}/user-portal")
    print(f"   Status: {user_portal_response.status_code}")
    print(f"   Contains admin links: {'admin' in user_portal_response.text.lower()}")
    
    # Go to user dashboard
    print(f"\n2️⃣ **Accessing User Dashboard**")
    user_dashboard_response = session.get(f"{base_url}/user/dashboard")
    print(f"   Status: {user_dashboard_response.status_code}")
    admin_link_in_dashboard = 'href="/admin"' in user_dashboard_response.text
    print(f"   Contains admin links: {admin_link_in_dashboard}")
    
    # Check if there are any unprotected admin links
    admin_link_patterns = [
        'href="/admin"',
        'href="/admin/',
        'href="/admin/users"',
        'href="/admin/items"',
        'href="/admin/client-apps"'
    ]
    
    # Test all user portal pages
    user_pages = [
        ("/user-portal", "User Portal"),
        ("/user/search", "User Search"),
        ("/user/dashboard", "User Dashboard"), 
        ("/user/profile", "User Profile")
    ]
    
    print(f"\n3️⃣ **Scanning User Pages for Admin Links**")
    
    for url, name in user_pages:
        print(f"\n   🔍 Testing: {name} ({url})")
        try:
            response = session.get(f"{base_url}{url}")
            if response.status_code == 200:
                content = response.text
                
                # Look for admin links
                found_links = []
                for pattern in admin_link_patterns:
                    if pattern in content:
                        # Check if it's properly protected
                        # Look for the line containing the link
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if pattern in line:
                                # Check surrounding lines for role check
                                context_start = max(0, i-3)
                                context_end = min(len(lines), i+3)
                                context = '\n'.join(lines[context_start:context_end])
                                
                                is_protected = any([
                                    "current_user.role == 'admin'" in context,
                                    "if admin" in context.lower(),
                                    "role == 'admin'" in context
                                ])
                                
                                found_links.append({
                                    'link': pattern,
                                    'protected': is_protected,
                                    'line': line.strip(),
                                    'context': context
                                })
                
                if found_links:
                    print(f"      Found {len(found_links)} admin links:")
                    for link_info in found_links:
                        status = "✅ Protected" if link_info['protected'] else "❌ UNPROTECTED"
                        print(f"         {status}: {link_info['link']}")
                        if not link_info['protected']:
                            print(f"         Line: {link_info['line']}")
                else:
                    print(f"      ✅ No admin links found")
            else:
                print(f"      ❌ Error accessing page: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ Exception: {e}")
    
    # Test specific admin links that might be exposed
    print(f"\n4️⃣ **Testing Admin Link Clicks**")
    
    potential_problem_links = [
        "/admin",
        "/admin/users", 
        "/admin/items",
        "/admin/client-apps"
    ]
    
    for link in potential_problem_links:
        print(f"\n   🖱️ Clicking: {link}")
        try:
            response = session.get(f"{base_url}{link}")
            content_type = response.headers.get('content-type', 'unknown')
            
            print(f"      Status: {response.status_code}")
            print(f"      Content-Type: {content_type}")
            
            if response.status_code == 403:
                if 'application/json' in content_type:
                    print(f"      ❌ **JSON ERROR FOUND!**: {response.text}")
                else:
                    print(f"      ✅ HTML error page")
            elif response.status_code == 200:
                print(f"      ⚠️ Accessible (security issue?)")
            else:
                print(f"      Other status: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ Exception: {e}")

def main():
    test_user_portal_admin_links()
    
    print(f"\n" + "=" * 60)
    print(f"🎯 **Summary:**")
    print(f"Look for '❌ JSON ERROR FOUND!' - these are the problematic admin links")
    print(f"that regular users can click and get JSON responses instead of HTML pages.")

if __name__ == "__main__":
    main()
