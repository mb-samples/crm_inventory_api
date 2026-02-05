# CRM & Inventory Management API - Complete Documentation

## 📋 Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Interactive Documentation](#interactive-documentation)
4. [API Endpoints](#api-endpoints)
5. [Testing & Validation](#testing--validation)
6. [Response Examples](#response-examples)
7. [Error Handling](#error-handling)

---

## Overview

RESTful API for managing customers, products, orders, and inventory operations.

### Base URL
```
http://localhost:5000
```

### API Version
```
v1.0.0
```

### Content Type
```
application/json
```

---

## Getting Started

### 1. Start the Server

```bash
# Activate virtual environment
source venv/bin/activate

# Start server with Swagger documentation
python swagger_api.py
```

### 2. Access Documentation

- **Swagger UI**: http://localhost:5000/apidocs/
- **OpenAPI Spec**: http://localhost:5000/apispec.json
- **Health Check**: http://localhost:5000/health

---

## Interactive Documentation

### Swagger UI (Recommended)

Navigate to **http://localhost:5000/apidocs/** for:

✅ Interactive API testing  
✅ Request/response examples  
✅ Schema validation  
✅ Try-it-out functionality  
✅ Automatic code generation  

### How to Use Swagger UI

1. Open http://localhost:5000/apidocs/
2. Browse endpoints by category (Health, Customers, Products, Orders)
3. Click any endpoint to expand details
4. Click "Try it out" button
5. Fill in parameters or request body
6. Click "Execute" to test
7. View response with status code and data

---

## API Endpoints

### Health Check

#### GET /health
Check API health status

**Response 200**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

---

### Customers

#### GET /api/customers
Retrieve paginated list of customers

**Query Parameters**
- `page` (integer, optional): Page number (default: 1)
- `limit` (integer, optional): Items per page (default: 50)
- `status` (string, optional): Filter by status (active, inactive, pending)

**Response 200**
```json
{
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "status": "active"
    }
  ],
  "total": 100,
  "page": 1,
  "limit": 50
}
```

#### GET /api/customers/{customerId}
Get customer details by ID

**Path Parameters**
- `customerId` (integer, required): Customer ID

**Response 200**
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

#### POST /api/customers
Create a new customer

**Request Body**
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "555-9999",
  "company": "Tech Corp",
  "address": "456 Oak Ave"
}
```

**Response 201**
```json
{
  "id": 3,
  "message": "Customer created successfully",
  "data": { ... }
}
```

---

### Products

#### GET /api/products
Retrieve paginated list of products

**Query Parameters**
- `page` (integer, optional): Page number
- `limit` (integer, optional): Items per page
- `category` (string, optional): Filter by category

**Response 200**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Widget A",
      "price": 29.99,
      "stock": 100,
      "category": "Electronics"
    }
  ],
  "total": 50,
  "page": 1,
  "limit": 50
}
```

#### GET /api/products/{productId}
Get product details by ID

**Response 200**
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

#### POST /api/products
Create a new product

**Request Body**
```json
{
  "name": "Widget D",
  "price": 59.99,
  "stock": 200,
  "category": "Electronics",
  "description": "New product"
}
```

**Response 201**
```json
{
  "id": 4,
  "message": "Product created successfully"
}
```

---

### Orders

#### GET /api/orders
Retrieve paginated list of orders

**Query Parameters**
- `page` (integer, optional): Page number
- `limit` (integer, optional): Items per page
- `status` (string, optional): Filter by status (pending, processing, completed, cancelled)
- `customer_id` (integer, optional): Filter by customer

**Response 200**
```json
{
  "data": [
    {
      "id": 1,
      "customer_id": 1,
      "total": 299.99,
      "status": "completed",
      "order_date": "2024-02-01"
    }
  ],
  "total": 25,
  "page": 1
}
```

#### GET /api/orders/{orderId}
Get order details by ID

**Response 200**
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
  "shipping_address": "123 Main St",
  "payment_method": "Credit Card"
}
```

#### POST /api/orders
Create a new order

**Request Body**
```json
{
  "customer_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 2,
      "quantity": 1
    }
  ],
  "shipping_address": "789 Pine St",
  "payment_method": "Credit Card"
}
```

**Response 201**
```json
{
  "id": 5,
  "message": "Order created successfully",
  "total": 299.99
}
```

---

## Testing & Validation

### Automated Validation

Run comprehensive API validation:

```bash
python validate_api.py
```

This tests:
- ✅ All endpoint availability
- ✅ Response structure validation
- ✅ HTTP status codes
- ✅ Query parameter handling
- ✅ JSON response format

**Expected Output:**
```
Total Tests:  24
Passed:       24
Failed:       0
Pass Rate:    100.0%
```

### Manual Testing Scripts

**Bash Script**
```bash
./quick_test.sh
```

**Python Script**
```bash
python test_endpoints.py
```

### Using curl

```bash
# Health check
curl http://localhost:5000/health

# Get customers
curl http://localhost:5000/api/customers

# Get customer by ID
curl http://localhost:5000/api/customers/1

# Create customer
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com"}'

# Get products with filter
curl "http://localhost:5000/api/products?category=Electronics"

# Create order
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"items":[{"product_id":1,"quantity":2}]}'
```

### Using Python

```python
import requests

# Get all customers
response = requests.get('http://localhost:5000/api/customers')
customers = response.json()

# Create new customer
customer_data = {
    "name": "Alice Johnson",
    "email": "alice@example.com"
}
response = requests.post(
    'http://localhost:5000/api/customers',
    json=customer_data
)
print(response.json())

# Get order details
response = requests.get('http://localhost:5000/api/orders/1')
order = response.json()
```

---

## Response Examples

### Success Response (200 OK)
```json
{
  "data": [...],
  "total": 100,
  "page": 1
}
```

### Created Response (201 Created)
```json
{
  "id": 5,
  "message": "Resource created successfully",
  "data": {...}
}
```

### Error Response (400 Bad Request)
```json
{
  "error": "Invalid input",
  "message": "The request body is missing required fields"
}
```

### Not Found Response (404 Not Found)
```json
{
  "error": "Not found",
  "message": "Resource with ID 999 not found"
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200  | OK - Request successful |
| 201  | Created - Resource created successfully |
| 400  | Bad Request - Invalid input data |
| 404  | Not Found - Resource not found |
| 500  | Internal Server Error - Server error |

### Common Error Scenarios

**Missing Required Fields**
```json
{
  "error": "Validation error",
  "message": "Missing required field: email"
}
```

**Invalid Data Type**
```json
{
  "error": "Validation error",
  "message": "Field 'price' must be a number"
}
```

**Resource Not Found**
```json
{
  "error": "Not found",
  "message": "Customer with ID 999 not found"
}
```

---

## Best Practices

### 1. Always Check Health First
```bash
curl http://localhost:5000/health
```

### 2. Use Pagination for Large Datasets
```bash
curl "http://localhost:5000/api/customers?page=1&limit=20"
```

### 3. Filter Results When Possible
```bash
curl "http://localhost:5000/api/orders?status=completed&customer_id=1"
```

### 4. Validate Request Data
Ensure all required fields are present before sending POST requests.

### 5. Handle Errors Gracefully
Always check response status codes and handle errors appropriately.

---

## Additional Resources

### Files in This Project

- `swagger_api.py` - API server with Swagger documentation
- `openapi.yaml` - OpenAPI 3.0 specification
- `validate_api.py` - Automated validation script
- `test_endpoints.py` - Python testing script
- `quick_test.sh` - Bash testing script
- `postman_collection.json` - Postman collection
- `SWAGGER_GUIDE.md` - Detailed Swagger usage guide
- `TESTING_GUIDE.md` - Manual testing guide

### Import into Tools

**Postman**
1. Open Postman
2. Click Import
3. Select "Link" and enter: `http://localhost:5000/apispec.json`

**Insomnia**
1. Open Insomnia
2. Import from URL
3. Enter: `http://localhost:5000/apispec.json`

---

## Support

For issues or questions:
- Check server logs
- Review validation report: `validation_report.json`
- Consult `SWAGGER_GUIDE.md` for detailed instructions

---

**Last Updated**: February 5, 2026  
**API Version**: 1.0.0  
**Status**: ✅ All systems operational
