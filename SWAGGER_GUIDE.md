# Swagger API Documentation & Testing Guide

## 🚀 Quick Start

The API server with Swagger documentation is now running!

### Access Points

- **API Server**: http://localhost:5000
- **Swagger UI**: http://localhost:5000/apidocs/
- **OpenAPI Spec (JSON)**: http://localhost:5000/apispec.json
- **OpenAPI Spec (YAML)**: `openapi.yaml` file in project root

## 📖 Using Swagger UI

### 1. Open Swagger UI

Navigate to: **http://localhost:5000/apidocs/**

You'll see an interactive API documentation interface with all endpoints organized by tags:
- Health
- Customers
- Products
- Orders

### 2. Test Endpoints Interactively

For each endpoint, you can:

1. **Click on the endpoint** to expand it
2. **Click "Try it out"** button
3. **Fill in parameters** (path params, query params, or request body)
4. **Click "Execute"** to send the request
5. **View the response** including status code, headers, and body

### Example: Testing GET /api/customers

1. Navigate to http://localhost:5000/apidocs/
2. Find "Customers" section
3. Click on `GET /api/customers`
4. Click "Try it out"
5. Optionally set query parameters:
   - `page`: 1
   - `limit`: 50
   - `status`: active
6. Click "Execute"
7. See the response with mock customer data

### Example: Testing POST /api/customers

1. Find `POST /api/customers` endpoint
2. Click "Try it out"
3. Edit the request body JSON:
```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "phone": "555-9999",
  "company": "Tech Corp",
  "address": "456 Oak Ave"
}
```
4. Click "Execute"
5. See the 201 Created response

## 🧪 Mock Validation Testing

### Available Test Scenarios

#### 1. Health Check
```bash
curl http://localhost:5000/health
```
Expected: `{"status": "healthy", "message": "API is running"}`

#### 2. Customer Operations

**List Customers**
```bash
curl "http://localhost:5000/api/customers?page=1&limit=10"
```

**Get Customer by ID**
```bash
curl http://localhost:5000/api/customers/1
```

**Create Customer**
```bash
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bob Smith",
    "email": "bob@example.com",
    "phone": "555-1234"
  }'
```

#### 3. Product Operations

**List Products**
```bash
curl "http://localhost:5000/api/products?category=Electronics"
```

**Get Product by ID**
```bash
curl http://localhost:5000/api/products/1
```

**Create Product**
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Widget D",
    "price": 59.99,
    "stock": 200,
    "category": "Electronics"
  }'
```

#### 4. Order Operations

**List Orders**
```bash
curl "http://localhost:5000/api/orders?status=completed"
```

**Get Order by ID**
```bash
curl http://localhost:5000/api/orders/1
```

**Create Order**
```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 2, "quantity": 1}
    ],
    "shipping_address": "789 Pine St",
    "payment_method": "Credit Card"
  }'
```

## 🔍 Validation Checklist

Use this checklist to validate the API:

### Endpoint Availability
- [ ] Health check returns 200 OK
- [ ] All GET endpoints return 200 OK
- [ ] All POST endpoints return 201 Created
- [ ] Invalid endpoints return 404 Not Found

### Response Format
- [ ] All responses are valid JSON
- [ ] Response structure matches OpenAPI schema
- [ ] Required fields are present
- [ ] Data types are correct (string, number, integer, etc.)

### Query Parameters
- [ ] Pagination works (page, limit)
- [ ] Filtering works (status, category, customer_id)
- [ ] Default values are applied when params omitted

### Request Validation
- [ ] POST requests accept valid JSON
- [ ] Required fields are enforced
- [ ] Optional fields work correctly

### HTTP Status Codes
- [ ] 200 for successful GET requests
- [ ] 201 for successful POST requests
- [ ] 400 for bad requests (future implementation)
- [ ] 404 for not found (future implementation)

## 📊 Automated Validation Script

Run the automated validation:

```bash
python validate_api.py
```

This script will:
1. Test all endpoints
2. Validate response schemas
3. Check HTTP status codes
4. Generate a validation report

## 🔧 Advanced Testing

### Using Postman

1. Import the OpenAPI spec:
   - Open Postman
   - Click "Import"
   - Select "Link" tab
   - Enter: `http://localhost:5000/apispec.json`
   - Click "Import"

2. Or import the collection:
   - Import `postman_collection.json` file

### Using Python Requests

```python
import requests

# Test health endpoint
response = requests.get('http://localhost:5000/health')
assert response.status_code == 200
assert response.json()['status'] == 'healthy'

# Test customer creation
customer_data = {
    "name": "Test User",
    "email": "test@example.com"
}
response = requests.post(
    'http://localhost:5000/api/customers',
    json=customer_data
)
assert response.status_code == 201
```

### Schema Validation

The OpenAPI spec (`openapi.yaml`) can be used with validation tools:

```bash
# Install validator
pip install openapi-spec-validator

# Validate the spec
openapi-spec-validator openapi.yaml
```

## 📝 Response Examples

### Customer Response
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "555-0123",
  "company": "Acme Corp",
  "address": "123 Main St, City, State 12345",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Product Response
```json
{
  "id": 1,
  "name": "Widget A",
  "price": 29.99,
  "stock": 100,
  "category": "Electronics",
  "description": "High-quality electronic widget",
  "sku": "WGT-A-001"
}
```

### Order Response
```json
{
  "id": 1,
  "customer_id": 1,
  "total": 299.99,
  "status": "completed",
  "order_date": "2024-02-01T14:30:00Z",
  "items": [
    {
      "product_id": 1,
      "product_name": "Widget A",
      "quantity": 2,
      "price": 29.99,
      "subtotal": 59.98
    }
  ],
  "shipping_address": "123 Main St, City, State 12345",
  "payment_method": "Credit Card"
}
```

## 🎯 Testing Best Practices

1. **Start with Health Check**: Always verify the API is running
2. **Test GET before POST**: Understand the data structure first
3. **Use Valid Data**: Follow the schema requirements
4. **Check Status Codes**: Verify expected HTTP responses
5. **Validate Response Schema**: Ensure responses match documentation
6. **Test Edge Cases**: Try different parameter combinations
7. **Test Error Scenarios**: Try invalid data (when implemented)

## 🔄 Continuous Testing

### Watch Mode Testing
```bash
# Run tests on file changes
pytest --watch
```

### Integration Testing
```bash
# Run full test suite
python -m pytest tests/
```

## 📚 Additional Resources

- **Swagger UI Docs**: https://swagger.io/tools/swagger-ui/
- **OpenAPI Specification**: https://swagger.io/specification/
- **API Testing Guide**: https://www.postman.com/api-testing/

## 🐛 Troubleshooting

### Swagger UI Not Loading
- Check server is running: `curl http://localhost:5000/health`
- Clear browser cache
- Try different browser

### Endpoints Not Responding
- Verify server is running
- Check port 5000 is not in use
- Review server logs

### Invalid Response Format
- This is a mock API - responses are simplified
- Full validation will be available with database connection

## 🚀 Next Steps

1. Test all endpoints using Swagger UI
2. Run automated validation script
3. Import OpenAPI spec into Postman
4. Create custom test scenarios
5. Document any issues or improvements needed

---

**Note**: This is a mock API for testing and validation. Once connected to a real database, all CRUD operations will be fully functional with proper validation and error handling.
