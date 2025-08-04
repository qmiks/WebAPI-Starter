# 🔑 **How to Get Bearer Token - Complete Guide**

## 🚀 **Quick Start (3 Steps)**

### **Step 1: Create Client Application**
1. **Open Admin Panel**: http://127.0.0.1:8000/admin/client-apps/
2. **Login** with admin credentials
3. **Click "Create New App"**
4. **Fill in details** and submit
5. **SAVE** the App ID and App Secret (shown only once!)

### **Step 2: Get Bearer Token**
Use the **Token Endpoint** with your credentials:

**POST** `http://127.0.0.1:8000/api/v1/auth/token`

### **Step 3: Use Token in API Calls**
Add header: `Authorization: Bearer your_token_here`

---

## 📋 **Method 1: Using Swagger UI (Easiest)**

### **A. Get Client Credentials**
1. Go to: http://127.0.0.1:8000/admin/client-apps/
2. Create new client app
3. Copy the **App ID** and **App Secret**

### **B. Generate Token in Swagger**
1. Open: http://127.0.0.1:8000/docs
2. Find **"POST /api/v1/auth/token"** endpoint
3. Click **"Try it out"**
4. Fill in the form:
   ```
   app_id: your_app_id_here
   app_secret: your_app_secret_here
   ```
5. Click **"Execute"**
6. **Copy the access_token** from the response

### **C. Use Token in Swagger**
1. Click **"Authorize"** button (🔓 at top right)
2. Enter: `Bearer your_access_token_here`
3. Click **"Authorize"**
4. Now you can test all protected endpoints!

---

## 💻 **Method 2: Using curl Command**

```bash
# Step 1: Get Bearer Token
curl -X POST "http://127.0.0.1:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "app_id=your_app_id&app_secret=your_app_secret"

# Response:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer",
#   "expires_in": 3600
# }

# Step 2: Use Token in API Calls
curl -X GET "http://127.0.0.1:8000/api/v1/users/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## 🐍 **Method 3: Using Python**

```python
import requests

# Configuration
BASE_URL = "http://127.0.0.1:8000"
APP_ID = "your_app_id_here"
APP_SECRET = "your_app_secret_here"

# Step 1: Get Bearer Token
def get_bearer_token():
    url = f"{BASE_URL}/api/v1/auth/token"
    data = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Step 2: Use Token in API Calls
def call_api_with_token(token):
    url = f"{BASE_URL}/api/v1/users/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()

# Usage
token = get_bearer_token()
if token:
    print(f"Token: {token}")
    users = call_api_with_token(token)
    print(f"Users: {users}")
```

---

## 🌐 **Method 4: Using JavaScript/Fetch**

```javascript
// Configuration
const BASE_URL = "http://127.0.0.1:8000";
const APP_ID = "your_app_id_here";
const APP_SECRET = "your_app_secret_here";

// Step 1: Get Bearer Token
async function getBearerToken() {
    const response = await fetch(`${BASE_URL}/api/v1/auth/token`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `app_id=${APP_ID}&app_secret=${APP_SECRET}`
    });
    
    const data = await response.json();
    return data.access_token;
}

// Step 2: Use Token in API Calls
async function callApiWithToken(token) {
    const response = await fetch(`${BASE_URL}/api/v1/users/`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    return await response.json();
}

// Usage
getBearerToken().then(token => {
    console.log('Token:', token);
    return callApiWithToken(token);
}).then(users => {
    console.log('Users:', users);
});
```

---

## 🔧 **Method 5: Using Postman**

### **Step 1: Get Token**
1. **Create New Request**: POST `http://127.0.0.1:8000/api/v1/auth/token`
2. **Set Headers**: `Content-Type: application/x-www-form-urlencoded`
3. **Set Body** (x-www-form-urlencoded):
   - `app_id`: your_app_id
   - `app_secret`: your_app_secret
4. **Send Request**
5. **Copy access_token** from response

### **Step 2: Use Token**
1. **Create New Request**: GET `http://127.0.0.1:8000/api/v1/users/`
2. **Go to Authorization Tab**
3. **Select "Bearer Token"**
4. **Paste your token**
5. **Send Request**

---

## ⚠️ **Important Notes**

### **Token Security**
- 🔒 **Never share tokens** in public repositories
- ⏰ **Tokens expire** in 1 hour (default)
- 🔄 **Generate new tokens** when needed
- 🗑️ **Admin can disable** client apps anytime

### **Token Format**
- ✅ **Correct**: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- ❌ **Wrong**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (missing "Bearer ")

### **Common Errors**
| Error | Cause | Solution |
|-------|-------|----------|
| 401 Invalid client credentials | Wrong App ID/Secret | Check credentials in admin panel |
| 401 Token has expired | Token older than 1 hour | Generate new token |
| 403 Not authenticated | Missing/wrong Bearer token | Check Authorization header format |
| 401 Client application disabled | Admin disabled your app | Contact admin |

---

## 🎯 **Quick Test Script**

Save this as `get_token_test.py`:

```python
#!/usr/bin/env python3
import requests

def quick_token_test():
    """Quick test to get and use a Bearer token."""
    
    # Replace with your actual credentials
    APP_ID = "app_sample123"  # Replace with real App ID
    APP_SECRET = "secret456"   # Replace with real App Secret
    
    BASE_URL = "http://127.0.0.1:8000"
    
    print("🔑 Getting Bearer Token...")
    
    # Get token
    token_response = requests.post(
        f"{BASE_URL}/api/v1/auth/token",
        data={"app_id": APP_ID, "app_secret": APP_SECRET}
    )
    
    if token_response.status_code == 200:
        token = token_response.json()["access_token"]
        print(f"✅ Token received: {token[:50]}...")
        
        # Test API call
        api_response = requests.get(
            f"{BASE_URL}/api/v1/users/",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if api_response.status_code == 200:
            print("✅ API call successful!")
            print(f"Users: {api_response.json()}")
        else:
            print(f"❌ API call failed: {api_response.status_code}")
    else:
        print(f"❌ Token request failed: {token_response.status_code}")
        print(f"Error: {token_response.text}")

if __name__ == "__main__":
    quick_token_test()
```

---

## 🌟 **Summary**

1. **Create client app** in admin panel
2. **Use credentials** to get Bearer token from `/api/v1/auth/token`
3. **Add token** to `Authorization: Bearer <token>` header
4. **Make API calls** to protected endpoints

**🔗 Quick Links:**
- 🏢 Admin Panel: http://127.0.0.1:8000/admin/client-apps/
- 📖 Swagger UI: http://127.0.0.1:8000/docs
- 🔑 Token Endpoint: http://127.0.0.1:8000/api/v1/auth/token
