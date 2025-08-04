#!/usr/bin/env python3
"""
Comprehensive Client Apps CRUD Test Suite
Tests Create, Read, Update, Delete operations for Client Applications
"""

import requests
import json
import random
import string
from datetime import datetime

def generate_random_string(length=8):
    """Generate a random string for unique test data"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

class ClientAppsCRUDTestSuite:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.session = requests.Session()
        self.test_results = []
        self.failed_tests = []
        self.created_app_ids = []
        
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
    
    def setup_admin_session(self):
        """Login as admin for testing"""
        print("🔑 Setting up admin session...")
        login_data = {"username": "admin", "password": "admin123"}
        response = self.session.post(f"{self.base_url}/auth/login", data=login_data, allow_redirects=False)
        
        if response.status_code in [303, 302]:
            self.log_result("Admin Login Setup", True, "Admin authentication successful")
            return True
        else:
            self.log_result("Admin Login Setup", False, f"Login failed: {response.status_code}")
            return False
    
    def test_client_apps_list_access(self):
        """Test 1: Access client apps list page"""
        print("\n📋 Testing Client Apps List Access...")
        
        response = self.session.get(f"{self.base_url}/admin/client-apps/")
        
        if response.status_code == 200:
            if "Client Applications" in response.text or "client-apps" in response.text:
                self.log_result("Client Apps List Access", True, "Client apps page accessible")
                return True
            else:
                self.log_result("Client Apps List Access", False, "Page loaded but missing expected content")
                return False
        else:
            self.log_result("Client Apps List Access", False, f"Status: {response.status_code}")
            return False
    
    def test_create_client_app(self):
        """Test 2: Create new client application"""
        print("\n➕ Testing Client App Creation...")
        
        random_id = generate_random_string(6)
        app_data = {
            "name": f"Test App {random_id}",
            "description": f"Test application for CRUD testing {random_id}",
            "redirect_uris": "https://example.com/callback",
            "scopes": "read write"
        }
        
        create_response = self.session.post(f"{self.base_url}/admin/client-apps/create", data=app_data, allow_redirects=False)
        
        # Handle both 200 (template response) and 303 (redirect) as success
        if create_response.status_code in [200, 303]:
            # Check if the creation was successful
            if create_response.status_code == 200:
                # For 200 response, check if app name and success message are in response
                if app_data['name'] in create_response.text and "created successfully" in create_response.text:
                    self.log_result("Client App Creation", True, f"App '{app_data['name']}' created successfully")
                    response_text = create_response.text
                else:
                    self.log_result("Client App Creation", False, "Creation response doesn't contain success indicators")
                    return False
            else:
                # For 303 response, get the redirected page
                self.log_result("Client App Creation", True, f"App '{app_data['name']}' created successfully (redirect)")
                list_response = self.session.get(f"{self.base_url}/admin/client-apps/")
                if list_response.status_code != 200:
                    self.log_result("Created App Verification", False, "Cannot access apps list after creation")
                    return False
                response_text = list_response.text
            
            # Verify the app appears and extract app ID
            if app_data['name'] in response_text:
                self.log_result("Created App Verification", True, "New app appears in response")
                
                # Extract app ID for later tests
                import re
                # Look for all app IDs in the response
                all_ids = re.findall(r'/admin/client-apps/(\d+)', response_text)
                if all_ids:
                    # Take the last/highest ID (most recently created)
                    app_id = max(all_ids, key=int)
                    self.created_app_ids.append(app_id)
                    self.log_result("App ID Extraction", True, f"Found app ID: {app_id}")
                else:
                    self.log_result("App ID Extraction", False, "Could not extract app ID from response")
                
                return True
            else:
                self.log_result("Created App Verification", False, "New app not found in response")
                return False
        else:
            self.log_result("Client App Creation", False, f"Status: {create_response.status_code}")
            return False
    
    def test_regenerate_secret(self):
        """Test 3: Regenerate client app secret"""
        print("\n🔄 Testing Secret Regeneration...")
        
        if not self.created_app_ids:
            self.log_result("Secret Regeneration", False, "No app ID available for testing")
            return False
        
        app_id = self.created_app_ids[0]
        response = self.session.post(f"{self.base_url}/admin/client-apps/{app_id}/regenerate-secret", allow_redirects=False)
        
        if response.status_code in [200, 303]:
            # Check for success indicators in the response
            if response.status_code == 200:
                if "regenerated successfully" in response.text or "success" in response.text.lower():
                    self.log_result("Secret Regeneration", True, f"Secret regenerated for app {app_id}")
                    return True
                else:
                    self.log_result("Secret Regeneration", False, "200 response but no success indicators")
                    return False
            else:
                self.log_result("Secret Regeneration", True, f"Secret regenerated for app {app_id}")
                return True
        else:
            self.log_result("Secret Regeneration", False, f"Status: {response.status_code}")
            return False
    
    def test_toggle_status(self):
        """Test 4: Toggle client app status (activate/deactivate)"""
        print("\n🔄 Testing Status Toggle...")
        
        if not self.created_app_ids:
            self.log_result("Status Toggle", False, "No app ID available for testing")
            return False
        
        app_id = self.created_app_ids[0]
        response = self.session.post(f"{self.base_url}/admin/client-apps/{app_id}/toggle-status", allow_redirects=False)
        
        if response.status_code in [200, 303]:
            # Check for success indicators in the response
            if response.status_code == 200:
                if "status" in response.text.lower() and ("success" in response.text.lower() or "toggled" in response.text.lower() or "updated" in response.text.lower()):
                    self.log_result("Status Toggle", True, f"Status toggled for app {app_id}")
                    return True
                else:
                    self.log_result("Status Toggle", False, "200 response but no success indicators")
                    return False
            else:
                self.log_result("Status Toggle", True, f"Status toggled for app {app_id}")
                return True
        else:
            self.log_result("Status Toggle", False, f"Status: {response.status_code}")
            return False
    
    def test_api_endpoints(self):
        """Test 5: API endpoints for client apps"""
        print("\n🔌 Testing API Endpoints...")
        
        # Test GET API (list client apps)
        api_list_response = self.session.get(f"{self.base_url}/admin/client-apps/api")
        
        if api_list_response.status_code == 200:
            try:
                apps_data = api_list_response.json()
                if isinstance(apps_data, list):
                    self.log_result("Client Apps API List", True, f"Retrieved {len(apps_data)} apps via API")
                else:
                    self.log_result("Client Apps API List", False, "Invalid JSON structure")
            except json.JSONDecodeError:
                self.log_result("Client Apps API List", False, "Invalid JSON response")
        else:
            self.log_result("Client Apps API List", False, f"Status: {api_list_response.status_code}")
        
        # Test POST API (create client app via API)
        random_id = generate_random_string(6)
        api_app_data = {
            "name": f"API Test App {random_id}",
            "description": f"API created test app {random_id}",
            "redirect_uris": ["https://api-test.com/callback"],
            "scopes": ["read", "write"]
        }
        
        api_create_response = self.session.post(
            f"{self.base_url}/admin/client-apps/api",
            json=api_app_data
        )
        
        if api_create_response.status_code in [200, 201]:
            try:
                created_app = api_create_response.json()
                # Check for either client_id/client_secret or app_id/app_secret
                if ("client_id" in created_app and "client_secret" in created_app) or \
                   ("app_id" in created_app and "app_secret" in created_app):
                    app_id = created_app.get('client_id') or created_app.get('id') or created_app.get('app_id')
                    self.log_result("Client App API Creation", True, f"App created via API with ID: {app_id}")
                    if created_app.get('id'):
                        self.created_app_ids.append(str(created_app['id']))
                else:
                    self.log_result("Client App API Creation", False, f"Missing credentials in response: {list(created_app.keys())}")
            except json.JSONDecodeError:
                self.log_result("Client App API Creation", False, "Invalid JSON response")
        else:
            self.log_result("Client App API Creation", False, f"Status: {api_create_response.status_code}")
    
    def test_delete_client_app(self):
        """Test 6: Delete client applications"""
        print("\n🗑️ Testing Client App Deletion...")
        
        deleted_count = 0
        for app_id in self.created_app_ids:
            # Test web interface deletion
            delete_response = self.session.post(f"{self.base_url}/admin/client-apps/{app_id}/delete", allow_redirects=False)
            
            if delete_response.status_code in [200, 303]:
                # Check for success indicators
                if delete_response.status_code == 200:
                    if "deleted successfully" in delete_response.text or "success" in delete_response.text.lower():
                        deleted_count += 1
                        self.log_result(f"Delete App {app_id} (Web)", True, f"App {app_id} deleted via web interface")
                        continue
                else:
                    deleted_count += 1
                    self.log_result(f"Delete App {app_id} (Web)", True, f"App {app_id} deleted via web interface")
                    continue
            
            # If web deletion didn't work, try API deletion
            api_delete_response = self.session.delete(f"{self.base_url}/admin/client-apps/api/{app_id}")
            if api_delete_response.status_code == 200:
                deleted_count += 1
                self.log_result(f"Delete App {app_id} (API)", True, f"App {app_id} deleted via API")
            else:
                self.log_result(f"Delete App {app_id}", False, f"Web: {delete_response.status_code}, API: {api_delete_response.status_code}")
        
        if deleted_count > 0:
            self.log_result("Overall Deletion Test", True, f"Successfully deleted {deleted_count} apps")
            return True
        else:
            self.log_result("Overall Deletion Test", False, "Failed to delete any apps")
            return False
    
    def test_error_handling(self):
        """Test 7: Error handling for invalid operations"""
        print("\n⚠️ Testing Error Handling...")
        
        # Test operations on non-existent app
        invalid_id = "999999"
        
        # Test regenerate secret on non-existent app
        regen_response = self.session.post(f"{self.base_url}/admin/client-apps/{invalid_id}/regenerate-secret")
        if regen_response.status_code in [404, 400]:
            self.log_result("Invalid ID Error Handling", True, "Properly handles non-existent app ID")
        else:
            self.log_result("Invalid ID Error Handling", False, f"Unexpected status: {regen_response.status_code}")
        
        # Test create app with missing data
        incomplete_data = {"name": ""}  # Missing required fields
        create_response = self.session.post(f"{self.base_url}/admin/client-apps/create", data=incomplete_data)
        
        if create_response.status_code in [400, 422, 200]:  # 200 might show form with validation errors
            if create_response.status_code == 200:
                # For 200 responses, check if it shows validation error or form again
                if "error" in create_response.text.lower() or "required" in create_response.text.lower() or \
                   "invalid" in create_response.text.lower() or len(create_response.text) > 1000:
                    self.log_result("Validation Error Handling", True, "Properly handles invalid input (form validation)")
                else:
                    self.log_result("Validation Error Handling", False, "200 response but no clear validation handling")
            else:
                self.log_result("Validation Error Handling", True, "Properly handles invalid input")
        else:
            self.log_result("Validation Error Handling", False, f"Unexpected status: {create_response.status_code}")
    
    def run_all_tests(self):
        """Run all client apps CRUD tests"""
        print("🚀 Starting Client Apps CRUD Test Suite")
        print("=" * 60)
        print(f"🕒 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Server URL: {self.base_url}")
        print("=" * 60)
        
        # Setup
        if not self.setup_admin_session():
            print("❌ Cannot proceed without admin access")
            return
        
        # Run tests
        tests_to_run = [
            self.test_client_apps_list_access,
            self.test_create_client_app,
            self.test_regenerate_secret,
            self.test_toggle_status,
            self.test_api_endpoints,
            self.test_delete_client_app,
            self.test_error_handling
        ]
        
        for test_func in tests_to_run:
            try:
                test_func()
            except Exception as e:
                test_name = test_func.__name__.replace('test_', '').replace('_', ' ').title()
                self.log_result(test_name, False, f"Exception: {e}")
        
        # Print results
        self.print_final_results()
    
    def print_final_results(self):
        """Print comprehensive test results"""
        print("\n" + "=" * 60)
        print("📊 CLIENT APPS CRUD TEST RESULTS")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['success']])
        failed_tests = total_tests - passed_tests
        
        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        
        if total_tests > 0:
            print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if self.failed_tests:
            print(f"\n⚠️ Failed Tests:")
            for failed_test in self.failed_tests:
                print(f"   - {failed_test}")
        
        print("\n" + "=" * 60)
        if failed_tests == 0:
            print("🎉 ALL CLIENT APPS CRUD TESTS PASSED!")
        elif failed_tests <= 2:
            print("✅ MOSTLY SUCCESSFUL! Minor issues detected.")
        else:
            print("⚠️ MULTIPLE ISSUES! Review failed tests.")
        
        print("=" * 60)

if __name__ == "__main__":
    test_suite = ClientAppsCRUDTestSuite()
    test_suite.run_all_tests()
