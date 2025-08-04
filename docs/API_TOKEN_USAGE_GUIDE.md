"""
API Token Usage Guide
====================

This document explains how to use API tokens with the FastAPI application.

## Step 1: Create a Client Application

1. Login as admin: http://127.0.0.1:8000/auth/login
   - Username: admin
   - Password: admin123

2. Go to Client Apps management: http://127.0.0.1:8000/admin/client-apps/

3. Create a new client app:
   - Fill in the form with app name and description
   - Save the App ID and App Secret (they will be shown only once!)

## Step 2: Get an API Token

Use your App ID and App Secret to get a JWT token:

### Using curl:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "app_id=your_app_id_here&app_secret=your_app_secret_here&expires_in=3600"
```

### Using Python requests:
```python
import requests

# Your client app credentials
app_id = "app_abc123def456..."
app_secret = "your_32_character_secret_key"

# Get token
response = requests.post("http://127.0.0.1:8000/api/v1/auth/token", 
    data={
        "app_id": app_id,
        "app_secret": app_secret,
        "expires_in": 3600  # 1 hour
    }
)

token_data = response.json()
access_token = token_data["access_token"]
print(f"Token: {access_token}")
```

### Response format:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600
}
```

## Step 3: Use the Token in API Calls

Add the token to the Authorization header as a Bearer token:

### Using curl:
```bash
# Get all users
curl -X GET http://127.0.0.1:8000/api/v1/users \
  -H "Authorization: Bearer your_jwt_token_here"

# Get specific user
curl -X GET http://127.0.0.1:8000/api/v1/users/1 \
  -H "Authorization: Bearer your_jwt_token_here"

# Get all items
curl -X GET http://127.0.0.1:8000/api/v1/items \
  -H "Authorization: Bearer your_jwt_token_here"
```

### Using Python requests:
```python
import requests

# Your JWT token from step 2
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

headers = {
    "Authorization": f"Bearer {token}"
}

# Get all users
response = requests.get("http://127.0.0.1:8000/api/v1/users", headers=headers)
users = response.json()
print(f"Users: {users}")

# Get specific user
response = requests.get("http://127.0.0.1:8000/api/v1/users/1", headers=headers)
user = response.json()
print(f"User: {user}")
```

### Using JavaScript/fetch:
```javascript
// Your JWT token
const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...";

// API call with token
fetch("http://127.0.0.1:8000/api/v1/users", {
    headers: {
        "Authorization": `Bearer ${token}`
    }
})
.then(response => response.json())
.then(data => console.log("Users:", data));
```

## Step 4: Token Management

### Token Expiration
- Default expiration: 1 hour (3600 seconds)
- Custom expiration: Set `expires_in` parameter when getting token
- When expired: Get a new token using the same app credentials

### Security Best Practices
1. **Store credentials securely**: Never hardcode App ID/Secret in client code
2. **Use environment variables**: Store credentials in env vars or secure config
3. **Regenerate secrets**: Periodically regenerate app secrets in admin panel
4. **Monitor usage**: Check admin dashboard for app activity

## Complete Example: Python Client

```python
import requests
import os
from datetime import datetime, timedelta

class APIClient:
    def __init__(self, app_id, app_secret, base_url="http://127.0.0.1:8000"):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = base_url
        self.token = None
        self.token_expires = None
    
    def get_token(self):
        """Get a new API token"""
        response = requests.post(f"{self.base_url}/api/v1/auth/token", 
            data={
                "app_id": self.app_id,
                "app_secret": self.app_secret,
                "expires_in": 3600
            }
        )
        response.raise_for_status()
        
        token_data = response.json()
        self.token = token_data["access_token"]
        self.token_expires = datetime.now() + timedelta(seconds=token_data["expires_in"])
        return self.token
    
    def ensure_token(self):
        """Ensure we have a valid token"""
        if not self.token or datetime.now() >= self.token_expires:
            self.get_token()
    
    def make_request(self, method, endpoint, **kwargs):
        """Make authenticated API request"""
        self.ensure_token()
        
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.token}"
        kwargs["headers"] = headers
        
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def get_users(self):
        """Get all users"""
        return self.make_request("GET", "/api/v1/users")
    
    def get_user(self, user_id):
        """Get specific user"""
        return self.make_request("GET", f"/api/v1/users/{user_id}")
    
    def get_items(self):
        """Get all items"""
        return self.make_request("GET", "/api/v1/items")

# Usage
if __name__ == "__main__":
    # Get credentials from environment variables
    app_id = os.getenv("API_APP_ID")
    app_secret = os.getenv("API_APP_SECRET")
    
    # Create client
    client = APIClient(app_id, app_secret)
    
    # Use the API
    try:
        users = client.get_users()
        print(f"Found {len(users['users'])} users")
        
        user = client.get_user(1)
        print(f"User 1: {user['username']}")
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
```

## Available Endpoints

Currently secured endpoints:
- `GET /api/v1/users` - Get all users
- `GET /api/v1/users/{id}` - Get specific user

## Error Handling

### Common HTTP Status Codes:
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: Valid token but insufficient permissions
- `404 Not Found`: Resource doesn't exist
- `422 Unprocessable Entity`: Invalid request parameters

### Example Error Response:
```json
{
    "detail": "Token has expired"
}
```

## Testing with Postman

1. **Get Token**:
   - Method: POST
   - URL: `http://127.0.0.1:8000/api/v1/auth/token`
   - Body: form-data
     - app_id: your_app_id
     - app_secret: your_app_secret
     - expires_in: 3600

2. **Use Token**:
   - Method: GET
   - URL: `http://127.0.0.1:8000/api/v1/users`
   - Headers: 
     - Authorization: Bearer your_jwt_token

## Troubleshooting

### "Authentication required" error:
- Check if Authorization header is present
- Verify Bearer token format: `Bearer token_here`
- Ensure token hasn't expired

### "Invalid client credentials" error:
- Verify App ID and App Secret are correct
- Check if client app is active in admin panel
- Ensure no extra spaces in credentials
"""
