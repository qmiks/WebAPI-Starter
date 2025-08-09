import requests
import json

# Test the new user-specific items API
BASE_URL = "http://127.0.0.1:8000"

print("=== TESTING USER ITEM MANAGEMENT ===")

# Test without authentication (should fail)
print("\n1. Testing items API without authentication:")
response = requests.get(f"{BASE_URL}/items/")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

print("\n2. Testing admin items API:")
# Login as admin first (would need session cookie for real test)
# For now just check the user dashboard endpoint

response = requests.get(f"{BASE_URL}/user/dashboard")
print(f"Status: {response.status_code}")
if response.status_code == 302:
    print(f"Redirected to: {response.headers.get('location', 'Unknown')}")

print("\n3. Testing API docs:")
response = requests.get(f"{BASE_URL}/docs")
print(f"Status: {response.status_code}")

print("\nTesting completed! Check the browser to login and test the user interface.")
