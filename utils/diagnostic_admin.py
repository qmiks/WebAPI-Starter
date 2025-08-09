#!/usr/bin/env python3
"""
Detailed admin page diagnostic
"""

import requests
import re

BASE_URL = "http://127.0.0.1:8000"

def login_as_admin():
    """Login as admin and return session"""
    session = requests.Session()
    login_data = {"username": "admin", "password": "admin123"}
    response = session.post(f"{BASE_URL}/auth/login", data=login_data, allow_redirects=False)
    return session if response.status_code in [302, 303] else None

def check_page_errors(session, url, page_name):
    """Check a specific page for errors"""
    print(f"\n🔍 Checking {page_name} ({url})...")
    
    response = session.get(f"{BASE_URL}{url}")
    content = response.text
    
    # Check for Jinja2 template errors
    jinja_errors = re.findall(r'UndefinedError|TemplateNotFound|TemplateSyntaxError', content, re.IGNORECASE)
    if jinja_errors:
        print(f"❌ Jinja2 errors found: {jinja_errors}")
    
    # Check for Python errors
    python_errors = re.findall(r'Traceback|KeyError|AttributeError|TypeError', content, re.IGNORECASE)
    if python_errors:
        print(f"❌ Python errors found: {python_errors}")
    
    # Check for missing variables
    undefined_vars = re.findall(r"'(\w+)' is undefined", content)
    if undefined_vars:
        print(f"❌ Undefined variables: {undefined_vars}")
    
    # Check for 500 errors
    if "500" in content and "Internal Server Error" in content:
        print("❌ 500 Internal Server Error detected")
    
    # Check for successful rendering
    if response.status_code == 200 and not jinja_errors and not python_errors:
        print("✅ Page renders successfully")
        
        # Check for data rendering
        if url == "/admin/items":
            if "Items Management" in content:
                print("   ✓ Items page title found")
            if "Total Items" in content:
                print("   ✓ Statistics section found")
        elif url == "/admin/users":
            if "Users Management" in content:
                print("   ✓ Users page title found")
        elif url == "/admin":
            if "Admin Dashboard" in content or "dashboard.admin_title" in content:
                print("   ✓ Dashboard title found")
    
    return response.status_code == 200 and not jinja_errors and not python_errors

def main():
    """Run detailed diagnostic"""
    print("🔍 Detailed Admin Page Diagnostic")
    print("=" * 50)
    
    session = login_as_admin()
    if not session:
        print("❌ Could not login as admin")
        return
    
    pages = [
        ("/admin", "Admin Dashboard"),
        ("/admin/users", "Users Management"), 
        ("/admin/items", "Items Management")
    ]
    
    all_good = True
    for url, name in pages:
        success = check_page_errors(session, url, name)
        if not success:
            all_good = False
    
    print(f"\n{'✅ All pages working correctly!' if all_good else '❌ Some pages have issues'}")

if __name__ == "__main__":
    main()
