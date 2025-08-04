import requests
import json

def test_user_portal_redirect():
    """Test the /user-portal redirect route"""
    base_url = "http://localhost:8000"
    
    # First login as user
    login_data = {
        "username": "user123",
        "password": "userpass"
    }
    
    print("1. Logging in as user...")
    session = requests.Session()
    login_response = session.post(f"{base_url}/auth/login", data=login_data)
    print(f"   Login response: {login_response.status_code}")
    
    if login_response.status_code == 200:
        print("   Login successful!")
        
        # Test /user-portal redirect
        print("\n2. Testing /user-portal redirect...")
        try:
            portal_response = session.get(f"{base_url}/user-portal", allow_redirects=False)
            print(f"   /user-portal response: {portal_response.status_code}")
            
            if portal_response.status_code == 302:
                redirect_location = portal_response.headers.get('location', 'No location header')
                print(f"   Redirect location: {redirect_location}")
                
                # Follow the redirect manually
                print(f"\n3. Following redirect to: {redirect_location}")
                if redirect_location.startswith('/'):
                    redirect_url = f"{base_url}{redirect_location}"
                else:
                    redirect_url = redirect_location
                    
                final_response = session.get(redirect_url)
                print(f"   Final response: {final_response.status_code}")
                print(f"   Content length: {len(final_response.text)} chars")
                
                if final_response.status_code != 200:
                    print(f"   Error content: {final_response.text[:500]}")
                    
            else:
                print(f"   Unexpected status: {portal_response.status_code}")
                print(f"   Content: {portal_response.text[:500]}")
                
        except Exception as e:
            print(f"   Error accessing /user-portal: {e}")
            
    else:
        print(f"   Login failed: {login_response.status_code}")
        print(f"   Content: {login_response.text}")

if __name__ == "__main__":
    test_user_portal_redirect()
