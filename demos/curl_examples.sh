#!/bin/bash
# API Token Usage Examples with curl
# ==================================

# Configuration
BASE_URL="http://127.0.0.1:8000"

# IMPORTANT: Replace these with your actual client app credentials
# Get these from: http://127.0.0.1:8000/admin/client-apps/
APP_ID="your_app_id_here"
APP_SECRET="your_app_secret_here"

echo "🚀 FastAPI Token Demo with curl"
echo "==============================="

# Step 1: Get API Token
echo ""
echo "🔑 Step 1: Getting API token..."
TOKEN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "app_id=$APP_ID&app_secret=$APP_SECRET&expires_in=3600")

echo "Response: $TOKEN_RESPONSE"

# Extract token from response (requires jq)
if command -v jq &> /dev/null; then
    TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.access_token')
    echo "✅ Token extracted: ${TOKEN:0:50}..."
else
    echo "⚠️  jq not found. Please install jq or extract token manually."
    echo "   Token should be in the 'access_token' field of the response above."
    exit 1
fi

# Step 2: Test API endpoints
echo ""
echo "🧪 Step 2: Testing API endpoints..."

# Test 1: Get all users
echo ""
echo "1️⃣ GET /api/v1/users (Get all users)"
curl -s -X GET "$BASE_URL/api/v1/users" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq '.'

# Test 2: Get specific user
echo ""
echo "2️⃣ GET /api/v1/users/1 (Get user with ID 1)"
curl -s -X GET "$BASE_URL/api/v1/users/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq '.'

# Test 3: Test without token (should fail)
echo ""
echo "3️⃣ GET /api/v1/users (Without token - should fail)"
curl -s -X GET "$BASE_URL/api/v1/users" \
  -H "Content-Type: application/json"

echo ""
echo "🎉 Demo completed!"
echo ""
echo "Next steps:"
echo "• View API docs: $BASE_URL/docs"
echo "• Manage apps: $BASE_URL/admin/client-apps/"
echo "• Admin dashboard: $BASE_URL/admin/"
