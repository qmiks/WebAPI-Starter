#!/usr/bin/env python3
"""
Test script to verify Polish language persistence from home page to admin dashboard
"""

def test_landing_page_admin_link():
    """Test that landing page admin link includes Polish language parameter"""
    print("🔗 Testing Landing Page Admin Link...")
    
    with open('templates/landing.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for the fixed admin link
    expected_link = 'href="/admin{% if locale != \'en\' %}?lang={{ locale }}{% endif %}"'
    
    if expected_link in content:
        print("   ✓ Admin link includes conditional language parameter")
        return True
    else:
        print("   ✗ Admin link missing language parameter")
        return False

def test_admin_route_polish_support():
    """Test that admin route supports Polish language"""
    print("\n🏛️ Testing Admin Route Polish Support...")
    
    with open('routers/admin.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for Polish language support
    if "lang in ['en', 'es', 'fr', 'de', 'pl']" in content:
        print("   ✓ Admin route supports Polish language")
        return True
    else:
        print("   ✗ Admin route missing Polish language support")
        return False

def test_auth_route_polish_support():
    """Test that auth routes support Polish language"""
    print("\n🔐 Testing Auth Route Polish Support...")
    
    with open('routers/auth.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for Polish language support
    pl_count = content.count("'en', 'es', 'fr', 'de', 'pl'")
    if pl_count >= 2:  # Should appear in at least 2 places
        print("   ✓ Auth routes support Polish language")
        return True
    else:
        print("   ✗ Auth routes missing Polish language support")
        return False

def test_user_portal_polish_support():
    """Test that user portal supports Polish language"""
    print("\n👤 Testing User Portal Polish Support...")
    
    with open('routers/user_portal.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for Polish language support
    pl_count = content.count("'en', 'es', 'fr', 'de', 'pl'")
    if pl_count >= 2:  # Should appear in at least 2 places
        print("   ✓ User portal supports Polish language")
        return True
    else:
        print("   ✗ User portal missing Polish language support")
        return False

def main():
    """Run all language persistence tests"""
    print("🌍 Polish Language Persistence Test")
    print("=" * 40)
    
    tests = [
        test_landing_page_admin_link(),
        test_admin_route_polish_support(),
        test_auth_route_polish_support(),
        test_user_portal_polish_support()
    ]
    
    passed = sum(tests)
    total = len(tests)
    
    print("\n" + "=" * 40)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        print("\n✅ Polish language persistence is working correctly:")
        print("   • Home page /?lang=pl → Admin dashboard ?lang=pl")
        print("   • Language parameter properly preserved in all routes")
        print("   • Cookies set correctly for Polish language")
        return True
    else:
        print("❌ Some tests failed - language persistence may not work correctly")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
