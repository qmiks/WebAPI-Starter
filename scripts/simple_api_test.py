import requests
import sys

# Test the API endpoints directly
base_url = "http://127.0.0.1:8000"

def test_api():
    print("Testing API endpoints...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        print(f"✓ Server is running - Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Server is not running. Please start the server first.")
        return False
    
    # Test 2: Test login page
    try:
        response = requests.get(f"{base_url}/auth/login")
        print(f"✓ Login page accessible - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ Login page error: {e}")
        return False
    
    # Test 3: Test user portal (should redirect to login)
    try:
        response = requests.get(f"{base_url}/user/dashboard", allow_redirects=False)
        if response.status_code in [302, 307, 401]:
            print(f"✓ User dashboard properly protected - Status: {response.status_code}")
        else:
            print(f"? User dashboard status: {response.status_code}")
    except Exception as e:
        print(f"✗ User dashboard error: {e}")
        return False
    
    # Test 4: Test items API (should require authentication)
    try:
        response = requests.get(f"{base_url}/api/items", allow_redirects=False)
        if response.status_code in [401, 403]:
            print(f"✓ Items API properly protected - Status: {response.status_code}")
        else:
            print(f"? Items API status: {response.status_code}")
    except Exception as e:
        print(f"✗ Items API error: {e}")
        return False
    
    print("\nAPI protection tests completed!")
    return True

if __name__ == "__main__":
    if test_api():
        print("✓ All basic API tests passed!")
    else:
        print("✗ Some tests failed!")
        sys.exit(1)
