#!/usr/bin/env python3
"""
Quick test to verify search functionality is working
"""
import requests

def test_search():
    """Test the search functionality"""
    print("🔍 Testing Search Functionality")
    print("=" * 50)
    
    # Test basic search
    try:
        response = requests.get("http://localhost:8000/search?query=test")
        print(f"Basic search status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Basic search working")
        else:
            print("❌ Basic search failed")
    except Exception as e:
        print(f"❌ Search test failed: {e}")
    
    # Test search with price parameters
    try:
        response = requests.get("http://localhost:8000/search?query=test&min_price=10&max_price=100")
        print(f"Price search status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Price search working")
        else:
            print("❌ Price search failed")
    except Exception as e:
        print(f"❌ Price search test failed: {e}")
    
    # Test search with empty price parameters (the bug we fixed)
    try:
        response = requests.get("http://localhost:8000/search?query=test&min_price=&max_price=")
        print(f"Empty price search status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Empty price search working (bug fixed!)")
        else:
            print("❌ Empty price search failed")
    except Exception as e:
        print(f"❌ Empty price search test failed: {e}")

if __name__ == "__main__":
    test_search()
