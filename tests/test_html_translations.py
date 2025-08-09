#!/usr/bin/env python3
"""
Diagnostic to check if translation keys appear in HTML output
"""

import requests
import re

BASE_URL = "http://127.0.0.1:8000"

def login_as_admin():
    """Login as admin"""
    session = requests.Session()
    login_data = {"username": "admin", "password": "admin123"}
    response = session.post(f"{BASE_URL}/auth/login", data=login_data, allow_redirects=False)
    return session if response.status_code in [302, 303] else None

def check_translation_in_html():
    """Check if translation keys appear in HTML"""
    session = login_as_admin()
    if not session:
        print("❌ Could not login")
        return
    
    print("🔍 Checking Translation Keys in HTML Output")
    print("=" * 50)
    
    # Check admin dashboard
    response = session.get(f"{BASE_URL}/admin")
    content = response.text
    
    # Look for untranslated keys
    untranslated_keys = re.findall(r'dashboard\.table\.\w+', content)
    
    if untranslated_keys:
        print(f"❌ Found untranslated keys in admin dashboard:")
        for key in set(untranslated_keys):
            print(f"  - {key}")
            
        # Show context around the first occurrence
        first_key = untranslated_keys[0]
        pattern = f".{{50}}{re.escape(first_key)}.{{50}}"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            print(f"\nContext for '{first_key}':")
            print(f"  ...{match.group()}...")
    else:
        print("✅ No untranslated dashboard.table keys found in admin dashboard")
    
    # Check admin items page
    response = session.get(f"{BASE_URL}/admin/items")
    content = response.text
    
    # Look for untranslated keys
    untranslated_keys = re.findall(r'dashboard\.table\.\w+', content)
    
    if untranslated_keys:
        print(f"❌ Found untranslated keys in admin items:")
        for key in set(untranslated_keys):
            print(f"  - {key}")
    else:
        print("✅ No untranslated dashboard.table keys found in admin items")
    
    # Check admin users page  
    response = session.get(f"{BASE_URL}/admin/users")
    content = response.text
    
    # Look for untranslated keys
    untranslated_keys = re.findall(r'dashboard\.table\.\w+', content)
    
    if untranslated_keys:
        print(f"❌ Found untranslated keys in admin users:")
        for key in set(untranslated_keys):
            print(f"  - {key}")
    else:
        print("✅ No untranslated dashboard.table keys found in admin users")

if __name__ == "__main__":
    check_translation_in_html()
