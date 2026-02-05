"""
Automated API Validation Script
Tests all endpoints and validates responses against expected schemas
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class APIValidator:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.results = []
    
    def test(self, name, condition, message=""):
        """Test a condition and record result"""
        if condition:
            self.passed += 1
            status = f"{Colors.GREEN}✓ PASS{Colors.END}"
            self.results.append({"test": name, "status": "PASS", "message": message})
        else:
            self.failed += 1
            status = f"{Colors.RED}✗ FAIL{Colors.END}"
            self.results.append({"test": name, "status": "FAIL", "message": message})
        
        print(f"  {status} - {name}")
        if message:
            print(f"         {message}")
    
    def warn(self, name, message):
        """Record a warning"""
        self.warnings += 1
        print(f"  {Colors.YELLOW}⚠ WARN{Colors.END} - {name}")
        print(f"         {message}")
        self.results.append({"test": name, "status": "WARN", "message": message})
    
    def section(self, title):
        """Print section header"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    
    def validate_response_structure(self, response, expected_keys):
        """Validate response has expected keys"""
        data = response.json()
        missing = [key for key in expected_keys if key not in data]
        return len(missing) == 0, missing
    
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}TEST SUMMARY{Colors.END}")
        print(f"{Colors.BOLD}{'='*70}{Colors.END}")
        print(f"Total Tests:  {total}")
        print(f"{Colors.GREEN}Passed:       {self.passed}{Colors.END}")
        print(f"{Colors.RED}Failed:       {self.failed}{Colors.END}")
        print(f"{Colors.YELLOW}Warnings:     {self.warnings}{Colors.END}")
        print(f"Pass Rate:    {pass_rate:.1f}%")
        print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")
        
        return self.failed == 0

def main():
    validator = APIValidator()
    
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}CRM & Inventory API - Automated Validation{Colors.END}")
    print(f"{Colors.BOLD}Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}")
    
    # Test 1: Health Check
    validator.section("1. Health Check Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        validator.test(
            "Health endpoint responds",
            response.status_code == 200,
            f"Status: {response.status_code}"
        )
        
        valid, missing = validator.validate_response_structure(
            response, ['status', 'message']
        )
        validator.test(
            "Health response has required fields",
            valid,
            f"Missing: {missing}" if not valid else "All fields present"
        )
        
        data = response.json()
        validator.test(
            "Health status is 'healthy'",
            data.get('status') == 'healthy',
            f"Status: {data.get('status')}"
        )
    except Exception as e:
        validator.test("Health endpoint responds", False, str(e))
    
    # Test 2: Customer Endpoints
    validator.section("2. Customer Endpoints")
    
    # GET /api/customers
    try:
        response = requests.get(f"{BASE_URL}/api/customers", timeout=5)
        validator.test(
            "GET /api/customers returns 200",
            response.status_code == 200,
            f"Status: {response.status_code}"
        )
        
        valid, missing = validator.validate_response_structure(
            response, ['data', 'total', 'page']
        )
        validator.test(
            "Customer list has required fields",
            valid,
            f"Missing: {missing}" if not valid else "All fields present"
        )
        
        data = response.json()
        validator.test(
            "Customer list contains array",
            isinstance(data.get('data'), list),
            f"Type: {type(data.get('data'))}"
        )
        
        if data.get('data'):
            customer = data['data'][0]
            validator.test(
                "Customer has id field",
                'id' in customer,
                f"Fields: {list(customer.keys())}"
            )
    except Exception as e:
        validator.test("GET /api/customers", False, str(e))
    
    # GET /api/customers/{id}
    try:
        response = requests.get(f"{BASE_URL}/api/customers/1", timeout=5)
        validator.test(
            "GET /api/customers/1 returns 200",
            response.status_code == 200
        )
        
        data = response.json()
        required_fields = ['id', 'name', 'email']
        has_fields = all(field in data for field in required_fields)
        validator.test(
            "Customer detail has required fields",
            has_fields,
            f"Fields: {list(data.keys())}"
        )
    except Exception as e:
        validator.test("GET /api/customers/1", False, str(e))
    
    # POST /api/customers
    try:
        customer_data = {
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "555-TEST"
        }
        response = requests.post(
            f"{BASE_URL}/api/customers",
            json=customer_data,
            timeout=5
        )
        validator.test(
            "POST /api/customers returns 201",
            response.status_code == 201,
            f"Status: {response.status_code}"
        )
    except Exception as e:
        validator.test("POST /api/customers", False, str(e))
    
    # Test 3: Product Endpoints
    validator.section("3. Product Endpoints")
    
    # GET /api/products
    try:
        response = requests.get(f"{BASE_URL}/api/products", timeout=5)
        validator.test(
            "GET /api/products returns 200",
            response.status_code == 200
        )
        
        data = response.json()
        validator.test(
            "Product list has data array",
            isinstance(data.get('data'), list)
        )
        
        if data.get('data'):
            product = data['data'][0]
            required = ['id', 'name', 'price', 'stock']
            has_fields = all(field in product for field in required)
            validator.test(
                "Product has required fields",
                has_fields,
                f"Fields: {list(product.keys())}"
            )
    except Exception as e:
        validator.test("GET /api/products", False, str(e))
    
    # GET /api/products/{id}
    try:
        response = requests.get(f"{BASE_URL}/api/products/1", timeout=5)
        validator.test(
            "GET /api/products/1 returns 200",
            response.status_code == 200
        )
        
        data = response.json()
        validator.test(
            "Product has price field",
            'price' in data and isinstance(data['price'], (int, float))
        )
    except Exception as e:
        validator.test("GET /api/products/1", False, str(e))
    
    # POST /api/products
    try:
        product_data = {
            "name": "Test Product",
            "price": 99.99,
            "stock": 50,
            "category": "Test"
        }
        response = requests.post(
            f"{BASE_URL}/api/products",
            json=product_data,
            timeout=5
        )
        validator.test(
            "POST /api/products returns 201",
            response.status_code == 201
        )
    except Exception as e:
        validator.test("POST /api/products", False, str(e))
    
    # Test 4: Order Endpoints
    validator.section("4. Order Endpoints")
    
    # GET /api/orders
    try:
        response = requests.get(f"{BASE_URL}/api/orders", timeout=5)
        validator.test(
            "GET /api/orders returns 200",
            response.status_code == 200
        )
        
        data = response.json()
        if data.get('data'):
            order = data['data'][0]
            required = ['id', 'customer_id', 'total', 'status']
            has_fields = all(field in order for field in required)
            validator.test(
                "Order has required fields",
                has_fields,
                f"Fields: {list(order.keys())}"
            )
    except Exception as e:
        validator.test("GET /api/orders", False, str(e))
    
    # GET /api/orders/{id}
    try:
        response = requests.get(f"{BASE_URL}/api/orders/1", timeout=5)
        validator.test(
            "GET /api/orders/1 returns 200",
            response.status_code == 200
        )
        
        data = response.json()
        validator.test(
            "Order has items array",
            'items' in data and isinstance(data['items'], list)
        )
    except Exception as e:
        validator.test("GET /api/orders/1", False, str(e))
    
    # POST /api/orders
    try:
        order_data = {
            "customer_id": 1,
            "items": [
                {"product_id": 1, "quantity": 2}
            ]
        }
        response = requests.post(
            f"{BASE_URL}/api/orders",
            json=order_data,
            timeout=5
        )
        validator.test(
            "POST /api/orders returns 201",
            response.status_code == 201
        )
    except Exception as e:
        validator.test("POST /api/orders", False, str(e))
    
    # Test 5: Query Parameters
    validator.section("5. Query Parameter Validation")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/customers?page=2&limit=10",
            timeout=5
        )
        data = response.json()
        validator.test(
            "Pagination parameters accepted",
            response.status_code == 200 and data.get('page') == 2
        )
    except Exception as e:
        validator.test("Pagination parameters", False, str(e))
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/products?category=Electronics",
            timeout=5
        )
        validator.test(
            "Category filter parameter accepted",
            response.status_code == 200
        )
    except Exception as e:
        validator.test("Category filter", False, str(e))
    
    # Test 6: Response Format
    validator.section("6. Response Format Validation")
    
    try:
        response = requests.get(f"{BASE_URL}/api/customers", timeout=5)
        content_type = response.headers.get('Content-Type', '')
        validator.test(
            "Response is JSON",
            'application/json' in content_type,
            f"Content-Type: {content_type}"
        )
    except Exception as e:
        validator.test("JSON response format", False, str(e))
    
    # Print summary and save report
    success = validator.print_summary()
    
    # Save detailed report
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": validator.passed + validator.failed,
            "passed": validator.passed,
            "failed": validator.failed,
            "warnings": validator.warnings
        },
        "results": validator.results
    }
    
    with open('validation_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Detailed report saved to: validation_report.json\n")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
