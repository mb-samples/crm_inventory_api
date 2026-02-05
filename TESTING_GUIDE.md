# API Testing Guide

The mock CRM & Inventory API is now running at **http://localhost:5000**

## Quick Test Methods

### 1. Using curl (Command Line)

```bash
# Health check
curl http://localhost:5000/health

# Get all customers
curl http://localhost:5000/api/customers

# Get specific customer
curl http://localhost:5000/api/customers/1

# Get all products
curl http://localhost:5000/api/products

# Get specific product
curl http://localhost:5000/api/products/1

# Get all orders
curl http://localhost:5000/api/orders

# Get specific order
curl http://localhost:5000/api/orders/1
```

### 2. Using Browser

Simply open these URLs in your browser:

- http://localhost:5000/health
- http://localhost:5000/api/customers
- http://localhost:5000/api/customers/1
- http://localhost:5000/api/products
- http://localhost:5000/api/products/1
- http://localhost:5000/api/orders
- http://localhost:5000/api/orders/1

### 3. Using Python requests

```python
import requests

# Health check
response = requests.get('http://localhost:5000/health')
print(response.json())

# Get customers
response = requests.get('http://localhost:5000/api/customers')
print(response.json())

# Get specific customer
response = requests.get('http://localhost:5000/api/customers/1')
print(response.json())
```

### 4. Using Postman or Insomnia

Import these endpoints:
- GET http://localhost:5000/health
- GET http://localhost:5000/api/customers
- GET http://localhost:5000/api/customers/{id}
- GET http://localhost:5000/api/products
- GET http://localhost:5000/api/products/{id}
- GET http://localhost:5000/api/orders
- GET http://localhost:5000/api/orders/{id}

## Expected Responses

### Health Check
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

### Customers List
```json
{
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane@example.com"
    }
  ],
  "total": 2,
  "page": 1
}
```

### Single Customer
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "555-0123",
  "company": "Acme Corp"
}
```

### Products List
```json
{
  "data": [
    {
      "id": 1,
      "name": "Widget A",
      "price": 29.99,
      "stock": 100
    },
    {
      "id": 2,
      "name": "Widget B",
      "price": 49.99,
      "stock": 50
    }
  ],
  "total": 2,
  "page": 1
}
```

### Single Product
```json
{
  "id": 1,
  "name": "Widget A",
  "price": 29.99,
  "stock": 100,
  "category": "Electronics"
}
```

### Orders List
```json
{
  "data": [
    {
      "id": 1,
      "customer_id": 1,
      "total": 299.99,
      "status": "completed"
    },
    {
      "id": 2,
      "customer_id": 2,
      "total": 149.99,
      "status": "pending"
    }
  ],
  "total": 2,
  "page": 1
}
```

### Single Order
```json
{
  "id": 1,
  "customer_id": 1,
  "total": 299.99,
  "status": "completed",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": 29.99
    }
  ]
}
```

## Testing with Different IDs

You can test with any ID number:
- http://localhost:5000/api/customers/123
- http://localhost:5000/api/products/456
- http://localhost:5000/api/orders/789

The mock API will return data with the ID you requested.

## Stopping the Server

To stop the server, press `Ctrl+C` in the terminal where it's running.

## Next Steps

Once you have a working MSSQL database:
1. Update the `.env` file with your database credentials
2. Install the database drivers: `pip install pyodbc pymssql`
3. Run the full application: `python app.py`
4. The real API will connect to your database and provide full CRUD operations
