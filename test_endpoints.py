"""
Python script to test API endpoints
Run: python test_endpoints.py
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))

def test_api():
    """Test all API endpoints"""
    
    print("\n" + "="*60)
    print("  CRM & Inventory API - Endpoint Tests")
    print("="*60)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_response("1. Health Check", response)
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: Get all customers
    try:
        response = requests.get(f"{BASE_URL}/api/customers")
        print_response("2. GET /api/customers", response)
    except Exception as e:
        print(f"❌ Get customers failed: {e}")
    
    # Test 3: Get single customer
    try:
        response = requests.get(f"{BASE_URL}/api/customers/1")
        print_response("3. GET /api/customers/1", response)
    except Exception as e:
        print(f"❌ Get customer failed: {e}")
    
    # Test 4: Get all products
    try:
        response = requests.get(f"{BASE_URL}/api/products")
        print_response("4. GET /api/products", response)
    except Exception as e:
        print(f"❌ Get products failed: {e}")
    
    # Test 5: Get single product
    try:
        response = requests.get(f"{BASE_URL}/api/products/1")
        print_response("5. GET /api/products/1", response)
    except Exception as e:
        print(f"❌ Get product failed: {e}")
    
    # Test 6: Get all orders
    try:
        response = requests.get(f"{BASE_URL}/api/orders")
        print_response("6. GET /api/orders", response)
    except Exception as e:
        print(f"❌ Get orders failed: {e}")
    
    # Test 7: Get single order
    try:
        response = requests.get(f"{BASE_URL}/api/orders/1")
        print_response("7. GET /api/orders/1", response)
    except Exception as e:
        print(f"❌ Get order failed: {e}")
    
    # Test with different IDs
    print(f"\n{'='*60}")
    print("  Testing with different IDs")
    print(f"{'='*60}")
    
    for resource, id_val in [("customers", 42), ("products", 99), ("orders", 123)]:
        try:
            response = requests.get(f"{BASE_URL}/api/{resource}/{id_val}")
            print(f"\n✓ GET /api/{resource}/{id_val} - Status: {response.status_code}")
            print(f"  Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"❌ Failed: {e}")
    
    print(f"\n{'='*60}")
    print("  ✅ All tests completed successfully!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    test_api()
