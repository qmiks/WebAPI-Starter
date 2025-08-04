#!/usr/bin/env python3
"""
Test Runner
Convenient script to run various test categories.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_test(test_file):
    """Run a single test file"""
    # Go up one directory from scripts to find tests
    project_root = Path(__file__).parent.parent
    test_path = project_root / "tests" / test_file
    if not test_path.exists():
        print(f"❌ Test file not found: {test_path}")
        return False
    
    print(f"🧪 Running: {test_file}")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, str(test_path)], 
                              cwd=project_root, 
                              capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return False

def list_tests():
    """List all available tests"""
    project_root = Path(__file__).parent.parent
    tests_dir = project_root / "tests"
    if not tests_dir.exists():
        print("❌ Tests directory not found")
        return
    
    test_files = sorted([f.name for f in tests_dir.glob("test_*.py")])
    
    print("📋 Available Tests:")
    print("=" * 40)
    
    categories = {
        "🔐 Authentication & Authorization": [
            "test_authorization_errors.py",
            "test_comprehensive_auth.py", 
            "test_login_error.py",
            "test_session_debug.py",
            "test_swagger_auth.py"
        ],
        "🔧 API Tests": [
            "test_api.py",
            "test_api_edge_cases.py",
            "test_api_token_error.py",
            "test_create_app_and_test.py",
            "test_end_to_end_api.py",
            "test_improved_api.py"
        ],
        "👥 User Interface": [
            "test_user_portal_admin_links.py",
            "test_user_portal_redirect.py",
            "test_user_search_access.py",
            "test_user_search_direct.py"
        ],
        "📊 Data Management": [
            "test_item_edit.py"
        ],
        "🎨 UI & Error Pages": [
            "test_error_page_preview.py"
        ],
        "🛠️ Admin Interface": [
            "test_admin.py",
            "test_admin_comprehensive.py",
            "test_admin_pages.py"
        ]
    }
    
    for category, tests in categories.items():
        print(f"\n{category}:")
        for test in tests:
            if test in test_files:
                print(f"  ✅ {test}")
            else:
                print(f"  ❓ {test} (not found)")
    
    # Show any tests not categorized
    uncategorized = set(test_files) - set([test for tests in categories.values() for test in tests])
    if uncategorized:
        print(f"\n❓ Other Tests:")
        for test in sorted(uncategorized):
            print(f"  • {test}")

def run_category(category):
    """Run all tests in a category"""
    categories = {
        "auth": [
            "test_authorization_errors.py",
            "test_comprehensive_auth.py", 
            "test_login_error.py",
            "test_session_debug.py",
            "test_swagger_auth.py"
        ],
        "api": [
            "test_api.py",
            "test_api_edge_cases.py",
            "test_api_token_error.py",
            "test_create_app_and_test.py",
            "test_end_to_end_api.py",
            "test_improved_api.py"
        ],
        "ui": [
            "test_user_portal_admin_links.py",
            "test_user_portal_redirect.py",
            "test_user_search_access.py",
            "test_user_search_direct.py",
            "test_error_page_preview.py"
        ],
        "admin": [
            "test_admin.py",
            "test_admin_comprehensive.py",
            "test_admin_pages.py"
        ],
        "data": [
            "test_item_edit.py"
        ]
    }
    
    if category not in categories:
        print(f"❌ Unknown category: {category}")
        print(f"Available categories: {', '.join(categories.keys())}")
        return False
    
    tests = categories[category]
    success_count = 0
    
    print(f"🧪 Running {category.upper()} tests...")
    print("=" * 60)
    
    for test in tests:
        if run_test(test):
            success_count += 1
        print()  # Add spacing between tests
    
    print(f"📊 Results: {success_count}/{len(tests)} tests passed")
    return success_count == len(tests)

def main():
    parser = argparse.ArgumentParser(description="Test Runner for Web API Application")
    parser.add_argument("--list", "-l", action="store_true", help="List all available tests")
    parser.add_argument("--test", "-t", help="Run a specific test file")
    parser.add_argument("--category", "-c", help="Run all tests in a category (auth, api, ui, admin, data)")
    parser.add_argument("--all", "-a", action="store_true", help="Run all tests")
    
    args = parser.parse_args()
    
    if args.list:
        list_tests()
    elif args.test:
        run_test(args.test)
    elif args.category:
        run_category(args.category)
    elif args.all:
        # Run all categories
        categories = ["auth", "api", "ui", "admin", "data"]
        for category in categories:
            print(f"\n{'='*60}")
            print(f"🏃 RUNNING {category.upper()} TESTS")
            print(f"{'='*60}")
            run_category(category)
    else:
        print("🧪 Web API Test Runner")
        print("=" * 30)
        print()
        print("Usage:")
        print("  python run_tests.py --list           # List all tests")
        print("  python run_tests.py --test <file>    # Run specific test")
        print("  python run_tests.py --category auth  # Run auth tests")
        print("  python run_tests.py --all            # Run all tests")
        print()
        print("Categories: auth, api, ui, admin, data")

if __name__ == "__main__":
    main()
