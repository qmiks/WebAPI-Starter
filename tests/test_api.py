"""
Test Script for Web API Application
This script demonstrates how to test the API endpoints.
"""

import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_get_users():
    """Test getting all users"""
    print("👥 Testing get users...")
    response = requests.get(f"{BASE_URL}/api/v1/users/")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total users: {data['total']}")
        print(f"Users returned: {len(data['users'])}")
        for user in data['users']:
            print(f"  - {user['username']} ({user['email']})")
    print("-" * 50)

def test_get_items():
    """Test getting all items"""
    print("📦 Testing get items...")
    response = requests.get(f"{BASE_URL}/api/v1/items/")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total items: {data['total']}")
        print(f"Items returned: {len(data['items'])}")
        for item in data['items']:
            print(f"  - {item['name']}: ${item['price']} (Status: {item['status']})")
    print("-" * 50)

def test_create_user():
    """Test creating a new user"""
    print("➕ Testing create user...")
    
    new_user = {
        "username": f"testuser_{datetime.now().strftime('%H%M%S')}",
        "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "role": "user"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/users/",
        json=new_user,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        user_data = response.json()
        print(f"Created user: {user_data['username']} (ID: {user_data['id']})")
        return user_data['id']
    else:
        print(f"Error: {response.text}")
        return None
    print("-" * 50)

def test_create_item(owner_id):
    """Test creating a new item"""
    print("➕ Testing create item...")
    
    new_item = {
        "name": f"Test Item {datetime.now().strftime('%H%M%S')}",
        "description": "This is a test item created by the test script",
        "price": 29.99,
        "status": "active",
        "owner_id": owner_id
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/items/",
        json=new_item,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        item_data = response.json()
        print(f"Created item: {item_data['name']} (ID: {item_data['id']})")
        return item_data['id']
    else:
        print(f"Error: {response.text}")
        return None
    print("-" * 50)

def test_get_user_by_id(user_id):
    """Test getting a user by ID"""
    print(f"🔍 Testing get user by ID ({user_id})...")
    response = requests.get(f"{BASE_URL}/api/v1/users/{user_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"Found user: {user_data['username']} - {user_data['full_name']}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_app_info():
    """Test the app info endpoint"""
    print("ℹ️ Testing app info...")
    response = requests.get(f"{BASE_URL}/info")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        info = response.json()
        print(f"App: {info['app_name']} v{info['version']}")
        print(f"Features: {', '.join(info['features'])}")
    print("-" * 50)

def run_all_tests():
    """Run all tests"""
    print("[MIGRATE] Starting Web API Application Tests")
    print("=" * 50)
    
    try:
        # Basic tests
        test_health_check()
        test_app_info()
        test_get_users()
        test_get_items()
        
        # Create a new user and use it for item creation
        user_id = test_create_user()
        if user_id:
            test_get_user_by_id(user_id)
            item_id = test_create_item(user_id)
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("[ERR] Error: Could not connect to the Web API application.")
        print("Make sure the application is running on http://127.0.0.1:8000")
        print("Run: python main.py")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    run_all_tests()
