#!/usr/bin/env python3
"""
Comprehensive Test for Authorization Error Handling
Test all admin routes to ensure consistent error handling.
"""

import requests

def test_all_admin_routes():
    print("🔐 **Comprehensive Admin Route Testing**")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    
    # Login as regular user
    session = requests.Session()
    login_data = {
        "username": "user",
        "password": "user123"
    }
    
    login_response = session.post(f"{base_url}/auth/login", data=login_data)
    print(f"✅ Logged in as regular user")
    
    # Test all admin-related routes
    admin_routes = [
        "/admin",
        "/admin/",
        "/admin/users",
        "/admin/users/",
        "/admin/client-apps",
        "/admin/client-apps/",
    ]
    
    print(f"\n🧪 **Testing Admin Routes for Proper Error Handling:**")
    
    results = {
        "html_error_pages": [],
        "json_errors": [],
        "accessible": [],
        "other_errors": []
    }
    
    for route in admin_routes:
        print(f"\n   🔍 Testing: {route}")
        try:
            response = session.get(f"{base_url}{route}")
            status = response.status_code
            content_type = response.headers.get('content-type', 'unknown')
            
            print(f"      Status: {status}")
            print(f"      Content-Type: {content_type}")
            
            if status == 403:
                if 'text/html' in content_type:
                    results["html_error_pages"].append(route)
                    print(f"      ✅ **HTML Error Page** (Good!)")
                elif 'application/json' in content_type:
                    results["json_errors"].append(route)
                    print(f"      ❌ **JSON Error** (Bad!)")
                    print(f"      Response: {response.text[:100]}")
                else:
                    results["other_errors"].append((route, status, content_type))
                    print(f"      ⚠️ **Other Error Type**")
            elif status == 200:
                results["accessible"].append(route)
                print(f"      ⚠️ **Accessible** (Security issue?)")
            else:
                results["other_errors"].append((route, status, content_type))
                print(f"      ❓ **Other Status**: {status}")
                
        except Exception as e:
            print(f"      ❌ **Exception**: {e}")
            results["other_errors"].append((route, "exception", str(e)))
    
    # Summary
    print(f"\n" + "=" * 60)
    print(f"📊 **SUMMARY:**")
    print(f"=" * 60)
    
    print(f"\n✅ **Routes with HTML Error Pages ({len(results['html_error_pages'])}):**")
    for route in results["html_error_pages"]:
        print(f"   • {route}")
    
    if results["json_errors"]:
        print(f"\n❌ **Routes with JSON Errors ({len(results['json_errors'])}) - NEED FIXING:**")
        for route in results["json_errors"]:
            print(f"   • {route}")
    
    if results["accessible"]:
        print(f"\n⚠️ **Routes Accessible to Regular Users ({len(results['accessible'])}) - SECURITY ISSUE:**")
        for route in results["accessible"]:
            print(f"   • {route}")
    
    if results["other_errors"]:
        print(f"\n❓ **Other Issues ({len(results['other_errors'])}):**")
        for route, status, details in results["other_errors"]:
            print(f"   • {route}: {status} - {details}")
    
    return results

def test_unauthenticated_access():
    print(f"\n🚫 **Testing Unauthenticated Access**")
    print("-" * 40)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test without login
    admin_routes = [
        "/admin",
        "/admin/users",
        "/admin/client-apps",
    ]
    
    for route in admin_routes:
        print(f"\n   🔍 Testing: {route} (no login)")
        try:
            response = requests.get(f"{base_url}{route}")
            status = response.status_code
            
            if status in [302, 303]:
                location = response.headers.get('location', 'No location')
                print(f"      ✅ Redirected to login: {location}")
            elif status == 200:
                print(f"      ⚠️ Accessible without login (security issue?)")
            else:
                print(f"      Status: {status}")
                
        except Exception as e:
            print(f"      ❌ Exception: {e}")

def main():
    results = test_all_admin_routes()
    test_unauthenticated_access()
    
    print(f"\n🎯 **FINAL VERDICT:**")
    if not results["json_errors"]:
        print(f"   ✅ **SUCCESS!** All admin routes return HTML error pages!")
        print(f"   🎉 No more raw JSON errors for users!")
    else:
        print(f"   ❌ Still {len(results['json_errors'])} routes returning JSON errors")
        print(f"   📝 These routes need to be updated with HTML error handling")

if __name__ == "__main__":
    main()
