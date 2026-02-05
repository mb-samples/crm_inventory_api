"""
Test script for Analytics API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_endpoint(name, url):
    """Test an endpoint and display results"""
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"{'='*70}")
    
    try:
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response type: {type(data)}")
            if isinstance(data, list):
                print(f"Number of items: {len(data)}")
                if data:
                    print(f"\nFirst item:")
                    print(json.dumps(data[0], indent=2))
            else:
                print(json.dumps(data, indent=2))
            print("✓ PASS")
        else:
            print(f"✗ FAIL - Status {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ ERROR: {e}")

def main():
    print("\n" + "="*70)
    print("ANALYTICS API ENDPOINTS TEST")
    print("="*70)
    
    # Test all analytics endpoints
    endpoints = [
        ("Customer Analytics", f"{BASE_URL}/api/analytics/customers"),
        ("Customer Analytics (filtered)", f"{BASE_URL}/api/analytics/customers?customer_id=1"),
        ("Inventory Status", f"{BASE_URL}/api/analytics/inventory-status"),
        ("Sales Performance", f"{BASE_URL}/api/analytics/sales-performance"),
        ("Sales Performance (by quarter)", f"{BASE_URL}/api/analytics/sales-performance?period=quarter"),
        ("Product Performance", f"{BASE_URL}/api/analytics/product-performance"),
        ("Product Performance (top 10)", f"{BASE_URL}/api/analytics/product-performance?top_n=10"),
        ("Order Fulfillment", f"{BASE_URL}/api/analytics/order-fulfillment"),
        ("Customer Segmentation", f"{BASE_URL}/api/analytics/customer-segmentation"),
        ("Payment Collection", f"{BASE_URL}/api/analytics/payment-collection"),
        ("Warehouse Utilization", f"{BASE_URL}/api/analytics/warehouse-utilization"),
        ("User Activity", f"{BASE_URL}/api/analytics/user-activity"),
        ("Supplier Performance", f"{BASE_URL}/api/analytics/supplier-performance"),
        ("Revenue Forecast", f"{BASE_URL}/api/analytics/revenue-forecast"),
        ("Revenue Forecast (6 months)", f"{BASE_URL}/api/analytics/revenue-forecast?months_ahead=6"),
    ]
    
    passed = 0
    failed = 0
    
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                passed += 1
                print(f"✓ {name}")
            else:
                failed += 1
                print(f"✗ {name} - Status {response.status_code}")
        except Exception as e:
            failed += 1
            print(f"✗ {name} - Error: {e}")
    
    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}")
    print(f"Total: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"{'='*70}\n")
    
    # Show detailed test for one endpoint
    test_endpoint(
        "Customer Segmentation (Detailed)",
        f"{BASE_URL}/api/analytics/customer-segmentation"
    )

if __name__ == "__main__":
    main()
