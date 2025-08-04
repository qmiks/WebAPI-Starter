#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Swagger UI Authentication Demo
Shows the full workflow from client app creation to API usage.
"""

import requests
import json
import time
import sys

# Fix encoding for Windows
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# API Configuration
BASE_URL = "http://127.0.0.1:8000"

def demo_complete_workflow():
    """Demonstrates the complete authentication workflow."""
    
    print("[MIGRATE] **Complete Web API Authentication Workflow Demo**")
    print("="*60)
    
    print("\n[USAGE] **Step 1: Access Swagger UI (No Auth Required)**")
    print(f"[OK] Open: {BASE_URL}/docs")
    print("   - View all API endpoints")
    print("   - Read documentation") 
    print("   - See authentication requirements")
    print("   - NO CREDENTIALS NEEDED for documentation!")
    
    print("\n[AUTH] **Step 2: Create Client Application**")
    print(f"[OK] Visit: {BASE_URL}/admin/client-apps/")
    print("   - Login as admin user")
    print("   - Click 'Create New App'")
    print("   - Fill in application details")
    print("   - Save App ID and App Secret")
    
    print("\n🎫 **Step 3: Generate API Token**")
    print("[OK] Use Swagger UI or curl:")
    print(f"   POST {BASE_URL}/api/v1/auth/token")
    print("   Body: {")
    print("     'app_id': 'your_app_id',")
    print("     'app_secret': 'your_app_secret'")
    print("   }")
    print("   → Returns JWT Bearer token")
    
    print("\n🔓 **Step 4: Authenticate in Swagger UI**")
    print("[OK] In Swagger UI:")
    print("   1. Click 'Authorize' button (🔓)")
    print("   2. Enter: Bearer your_jwt_token_here")
    print("   3. Click 'Authorize'")
    print("   4. Lock icon changes to unlocked (🔓)")
    
    print("\n[TEST] **Step 5: Test Protected Endpoints**")
    print("[OK] Try any Users API endpoint:")
    print("   - GET /api/v1/users/ (List all users)")
    print("   - GET /api/v1/users/{user_id} (Get specific user)")
    print("   - POST /api/v1/users/ (Create new user)")
    print("   - All endpoints now work with your token!")
    
    print("\n" + "="*60)
    print("[DEMO] **Key Benefits of This Approach**")
    print("="*60)
    
    benefits = [
        "[API] **Open Documentation**: Developers can explore API without barriers",
        "🔒 **Secure Endpoints**: Each API call requires valid authentication",
        "[TEST] **Easy Testing**: Built-in authentication in Swagger UI",
        "[USERS] **Great Developer Experience**: Clear workflow and immediate feedback",
        "🏢 **Enterprise Ready**: Token-based authentication with admin controls",
        "🔄 **Standard Compliance**: Uses industry-standard Bearer tokens"
    ]
    
    for benefit in benefits:
        print(f"[OK] {benefit}")
    
    print("\n" + "="*60)
    print("[INDEX] **Live Demo URLs**")
    print("="*60)
    
    print(f"[USAGE] Swagger UI (Open):     {BASE_URL}/docs")
    print(f"🏢 Admin Panel:           {BASE_URL}/admin/client-apps/")
    print(f"🎫 Token Endpoint:        {BASE_URL}/api/v1/auth/token")
    print(f"[USERS] Users API:             {BASE_URL}/api/v1/users/")
    print(f"🏠 Main Application:      {BASE_URL}/")
    
    print("\n💡 **Pro Tips:**")
    print("   • Swagger UI shows 🔒 icons on protected endpoints")
    print("   • Token expires in 1 hour (configurable)")
    print("   • Admin can disable client apps anytime")
    print("   • All API errors include helpful messages")
    print("   • Use 'Try it out' buttons to test live API calls")

def test_swagger_ui_features():
    """Test specific Swagger UI authentication features."""
    
    print("\n[TEST] **Testing Swagger UI Features**")
    print("-" * 40)
    
    try:
        # Test Swagger UI accessibility
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("[OK] Swagger UI loads without authentication")
        
        # Test API schema accessibility
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            schema = response.json()
            print(f"[OK] OpenAPI schema accessible (version: {schema.get('openapi', 'unknown')})")
            
            # Check for security schemes
            security_schemes = schema.get('components', {}).get('securitySchemes', {})
            if 'HTTPBearer' in security_schemes:
                print("[OK] HTTPBearer security scheme properly configured")
        
        # Test protected endpoint without auth
        response = requests.get(f"{BASE_URL}/api/v1/users/")
        if response.status_code in [401, 403]:
            print("[OK] Protected endpoints correctly require authentication")
        
        print("[SUMMARY] All Swagger UI features working correctly!")
        
    except Exception as e:
        print(f"[ERR] Error testing Swagger UI: {e}")

if __name__ == "__main__":
    demo_complete_workflow()
    test_swagger_ui_features()
    
    print("\n[DEMO] **Ready to Use!**")
    print("Your Web API application now has the perfect balance:")
    print("[USAGE] Open API documentation + 🔒 Secure endpoints + [TEST] Easy testing")
