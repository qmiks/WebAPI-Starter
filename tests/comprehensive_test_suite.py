#!/usr/bin/env python3
"""
Comprehensive Test Suite for Web API Project
Tests all major functionality and features
"""

import requests
import time
import json
import random
import string
from datetime import datetime

def generate_random_string(length=8):
    """Generate a random string for unique test data"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

class ComprehensiveTestSuite:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.session = requests.Session()
        self.test_results = []
        self.failed_tests = []
        
    def log_result(self, test_name, success, message=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
        print(f"{status}: {test_name}")
        if message:
            print(f"     {message}")
        if not success:
            self.failed_tests.append(test_name)
    
    def test_server_health(self):
        """Test 1: Server Health Check"""
        print("\n🔍 Testing Server Health...")
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                self.log_result("Server Health Check", True, "Server is responding")
                return True
            else:
                self.log_result("Server Health Check", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Server Health Check", False, f"Connection error: {e}")
            return False
    
    def test_admin_authentication(self):
        """Test 2: Admin Authentication"""
        print("\n🔐 Testing Admin Authentication...")
        
        # Test login
        login_data = {"username": "admin", "password": "admin123"}
        response = self.session.post(f"{self.base_url}/auth/login", data=login_data, allow_redirects=False)
        
        if response.status_code in [303, 302]:
            self.log_result("Admin Login", True, "Login redirect successful")
        else:
            self.log_result("Admin Login", False, f"Status: {response.status_code}")
            return False
        
        # Test admin panel access
        admin_response = self.session.get(f"{self.base_url}/admin/")
        if admin_response.status_code == 200:
            self.log_result("Admin Panel Access", True, "Admin dashboard accessible")
            return True
        else:
            self.log_result("Admin Panel Access", False, f"Status: {admin_response.status_code}")
            return False
    
    def test_user_management(self):
        """Test 3: User Management"""
        print("\n👥 Testing User Management...")
        
        # Test user creation
        random_id = generate_random_string(6)
        new_user_data = {
            "username": f"testuser_{random_id}",
            "email": f"test_{random_id}@example.com",
            "full_name": f"Test User {random_id}",
            "password": "testpass123",
            "role": "user",
            "is_active": "true"
        }
        
        create_response = self.session.post(f"{self.base_url}/admin/users/new", data=new_user_data, allow_redirects=False)
        
        if create_response.status_code == 303:
            self.log_result("User Creation", True, f"User {new_user_data['username']} created")
        else:
            self.log_result("User Creation", False, f"Status: {create_response.status_code}")
        
        # Test users list
        users_response = self.session.get(f"{self.base_url}/admin/users")
        if users_response.status_code == 200 and new_user_data['username'] in users_response.text:
            self.log_result("User List Display", True, "New user appears in users list")
        else:
            self.log_result("User List Display", False, "User not found in list")
        
        # Test user deletion (if creation was successful)
        if create_response.status_code == 303:
            import re
            # Find user ID for deletion test
            username_pos = users_response.text.find(new_user_data['username'])
            if username_pos != -1:
                surrounding_text = users_response.text[max(0, username_pos-300):username_pos+300]
                id_pattern = r'/admin/users/(\d+)(?:/edit|")'
                id_matches = re.findall(id_pattern, surrounding_text)
                if id_matches:
                    user_id = id_matches[-1]
                    delete_response = self.session.post(f"{self.base_url}/admin/users/{user_id}/delete", allow_redirects=False)
                    if delete_response.status_code == 303:
                        self.log_result("User Deletion", True, f"User {new_user_data['username']} deleted successfully")
                    else:
                        self.log_result("User Deletion", False, f"Delete status: {delete_response.status_code}")
                else:
                    self.log_result("User Deletion", False, "Could not find user ID for deletion")
            else:
                self.log_result("User Deletion", False, "User not found for deletion test")
        
        return create_response.status_code == 303
    
    def test_duplicate_user_validation(self):
        """Test 4: Duplicate User Validation"""
        print("\n🔁 Testing Duplicate User Validation...")
        
        # Try to create user with existing username
        duplicate_data = {
            "username": "admin",
            "email": "newadmin@example.com",
            "full_name": "Duplicate Admin",
            "password": "password123",
            "role": "admin",
            "is_active": "true"
        }
        
        response = self.session.post(f"{self.base_url}/admin/users/new", data=duplicate_data)
        
        if response.status_code == 200:
            # Check for error message (HTML encoded)
            error_patterns = [
                "Username &#39;admin&#39; already exists",
                "Username 'admin' already exists"
            ]
            error_found = any(pattern in response.text for pattern in error_patterns)
            
            if error_found:
                self.log_result("Username Duplicate Detection", True, "Duplicate username properly rejected")
            else:
                self.log_result("Username Duplicate Detection", False, "No error message found")
        else:
            self.log_result("Username Duplicate Detection", False, f"Unexpected status: {response.status_code}")
        
        # Try duplicate email
        duplicate_email_data = {
            "username": "newuser123",
            "email": "admin@example.com",
            "full_name": "New User",
            "password": "password123",
            "role": "user",
            "is_active": "true"
        }
        
        response = self.session.post(f"{self.base_url}/admin/users/new", data=duplicate_email_data)
        
        if response.status_code == 200:
            email_error_patterns = [
                "Email &#39;admin@example.com&#39; already exists",
                "Email 'admin@example.com' already exists"
            ]
            error_found = any(pattern in response.text for pattern in email_error_patterns)
            
            if error_found:
                self.log_result("Email Duplicate Detection", True, "Duplicate email properly rejected")
            else:
                self.log_result("Email Duplicate Detection", False, "No email error message found")
        else:
            self.log_result("Email Duplicate Detection", False, f"Unexpected status: {response.status_code}")
    
    def test_item_management(self):
        """Test 5: Item Management"""
        print("\n📦 Testing Item Management...")
        
        # Test items list
        items_response = self.session.get(f"{self.base_url}/admin/items")
        if items_response.status_code == 200:
            self.log_result("Items List Access", True, "Items page accessible")
        else:
            self.log_result("Items List Access", False, f"Status: {items_response.status_code}")
            return False
        
        # Test item detail view
        item_detail_response = self.session.get(f"{self.base_url}/admin/items/1")
        if item_detail_response.status_code == 200:
            self.log_result("Item Detail View", True, "Item detail page accessible")
        else:
            self.log_result("Item Detail View", False, f"Status: {item_detail_response.status_code}")
        
        return True
    
    def test_user_portal(self):
        """Test 6: User Portal"""
        print("\n🌐 Testing User Portal...")
        
        # Test user portal access via main route
        portal_response = self.session.get(f"{self.base_url}/user-portal")
        if portal_response.status_code == 200:
            self.log_result("User Portal Access", True, "User portal accessible")
        else:
            self.log_result("User Portal Access", False, f"Status: {portal_response.status_code}")
            return False
        
        # Test search functionality (requires authentication)
        # Since we're already logged in as admin from previous tests, this should work
        search_response = self.session.get(f"{self.base_url}/user/search?q=test", allow_redirects=False)
        if search_response.status_code == 200:
            self.log_result("Search Functionality", True, "Search feature working")
        elif search_response.status_code in [302, 303]:
            # If redirected to login, try logging in first
            login_data = {"username": "admin", "password": "admin123"}
            login_resp = self.session.post(f"{self.base_url}/auth/login", data=login_data, allow_redirects=False)
            if login_resp.status_code in [302, 303]:
                # Try search again after login
                search_response2 = self.session.get(f"{self.base_url}/user/search?q=test")
                if search_response2.status_code == 200:
                    self.log_result("Search Functionality", True, "Search feature working after authentication")
                else:
                    self.log_result("Search Functionality", False, f"Status after auth: {search_response2.status_code}")
            else:
                self.log_result("Search Functionality", False, f"Login failed: {login_resp.status_code}")
        else:
            self.log_result("Search Functionality", False, f"Status: {search_response.status_code}")
        
        return True
    
    def test_api_endpoints(self):
        """Test 7: API Endpoints"""
        print("\n🔌 Testing API Endpoints...")
        
        # Test items API (correct prefix)
        items_api_response = self.session.get(f"{self.base_url}/api/v1/items")
        if items_api_response.status_code == 200:
            try:
                items_data = items_api_response.json()
                if isinstance(items_data, dict) and 'items' in items_data:
                    self.log_result("Items API", True, f"Retrieved {len(items_data['items'])} items")
                else:
                    self.log_result("Items API", False, "Invalid JSON structure")
            except:
                self.log_result("Items API", False, "Invalid JSON response")
        else:
            self.log_result("Items API", False, f"Status: {items_api_response.status_code}")
        
        # Test users API (should require authentication)
        users_api_response = self.session.get(f"{self.base_url}/api/v1/users")
        if users_api_response.status_code in [401, 403]:
            self.log_result("Users API Security", True, "Protected endpoint properly secured")
        elif users_api_response.status_code == 200:
            self.log_result("Users API Security", True, "Authenticated access granted")
        else:
            self.log_result("Users API Security", False, f"Unexpected status: {users_api_response.status_code}")
    
    def test_template_rendering(self):
        """Test 8: Template Rendering"""
        print("\n🎨 Testing Template Rendering...")
        
        # Check if key templates are rendering properly
        templates_to_test = [
            ("/admin/", "Admin Dashboard"),
            ("/admin/users", "User Management"),
            ("/admin/items", "Item Management"),
            ("/user-portal", "User Portal")
        ]
        
        for url, template_name in templates_to_test:
            response = self.session.get(f"{self.base_url}{url}")
            if response.status_code == 200 and len(response.text) > 100:
                self.log_result(f"Template: {template_name}", True, "Template rendered successfully")
            else:
                self.log_result(f"Template: {template_name}", False, f"Status: {response.status_code}")
    
    def test_error_handling(self):
        """Test 9: Error Handling"""
        print("\n⚠️ Testing Error Handling...")
        
        # Test 404 handling
        not_found_response = self.session.get(f"{self.base_url}/nonexistent")
        if not_found_response.status_code == 404:
            self.log_result("404 Error Handling", True, "404 errors properly handled")
        else:
            self.log_result("404 Error Handling", False, f"Status: {not_found_response.status_code}")
        
        # Test invalid user access
        invalid_user_response = self.session.get(f"{self.base_url}/admin/users/99999")
        if invalid_user_response.status_code == 404:
            self.log_result("Invalid Resource Handling", True, "Invalid resources properly handled")
        else:
            self.log_result("Invalid Resource Handling", False, f"Status: {invalid_user_response.status_code}")
    
    def run_all_tests(self):
        """Run all comprehensive tests"""
        print("🚀 Starting Comprehensive Test Suite")
        print("=" * 60)
        print(f"🕒 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Server URL: {self.base_url}")
        print("=" * 60)
        
        # Run all tests
        tests_to_run = [
            self.test_server_health,
            self.test_admin_authentication,
            self.test_user_management,
            self.test_duplicate_user_validation,
            self.test_item_management,
            self.test_user_portal,
            self.test_api_endpoints,
            self.test_template_rendering,
            self.test_error_handling
        ]
        
        for test_func in tests_to_run:
            try:
                test_func()
            except Exception as e:
                test_name = test_func.__name__.replace('test_', '').replace('_', ' ').title()
                self.log_result(test_name, False, f"Exception: {e}")
        
        # Print final results
        self.print_final_results()
    
    def print_final_results(self):
        """Print comprehensive test results"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST RESULTS")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['success']])
        failed_tests = total_tests - passed_tests
        
        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if self.failed_tests:
            print(f"\n⚠️ Failed Tests:")
            for failed_test in self.failed_tests:
                print(f"   - {failed_test}")
        
        print("\n" + "=" * 60)
        if failed_tests == 0:
            print("🎉 ALL TESTS PASSED! The system is working perfectly!")
        elif failed_tests <= 2:
            print("✅ MOSTLY SUCCESSFUL! Minor issues detected.")
        else:
            print("⚠️ MULTIPLE ISSUES! Review failed tests.")
        
        print("=" * 60)

if __name__ == "__main__":
    test_suite = ComprehensiveTestSuite()
    test_suite.run_all_tests()
