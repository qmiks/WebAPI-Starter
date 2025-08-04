#!/usr/bin/env python3
"""
Test the actual error page experience
"""

import requests

def test_user_sees_nice_error_page():
    print("🎨 **Testing User Error Page Experience**")
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
    
    # Try to access admin area
    response = session.get(f"{base_url}/admin")
    
    print(f"\n🔍 **Response Details:**")
    print(f"   Status Code: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('content-type')}")
    print(f"   Content Length: {len(response.text)} characters")
    
    # Check if it's the error page
    if "Access Denied" in response.text:
        print(f"   ✅ Contains 'Access Denied' title")
    if "You don't have permission" in response.text:
        print(f"   ✅ Contains helpful error message")
    if "User Portal" in response.text:
        print(f"   ✅ Contains link back to User Portal")
    if "Back to Home" in response.text:
        print(f"   ✅ Contains link back to Home")
    
    # Save the error page for manual inspection
    with open("c:/Learn/Python2/docrag/error_page_sample.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"\n💾 **Error page saved as 'error_page_sample.html'**")
    print(f"   You can open this file in a browser to see how it looks!")

if __name__ == "__main__":
    test_user_sees_nice_error_page()
