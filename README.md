# CRM & Inventory Management API

Flask-based REST API for managing customers, products, orders, and inventory with MSSQL database.

## Features

- Customer management (CRM)
- Product catalog management
- Order processing
- Inventory tracking
- Connection pooling for database efficiency
- RESTful API design
- CORS support

## Prerequisites

- Python 3.8+
- Microsoft SQL Server
- ODBC Driver 17 for SQL Server

## Installation

1. Clone the repository:
```bash
cd crm_inventory_api
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Setup database:
```bash
# Run the schema.sql file in your MSSQL server
sqlcmd -S localhost -U sa -P YourPassword -i database/schema.sql
```

## Configuration

Edit `.env` file with your settings:

```env
DB_SERVER=localhost
DB_PORT=1433
DB_NAME=crm_inventory_db
DB_USER=sa
DB_PASSWORD=YourStrongPassword123!
SECRET_KEY=your-secret-key-here
```

## Running the Application

Development mode:
```bash
python app.py
```

Production mode:
```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Endpoints

### Customers
- `GET /api/customers` - List all customers
- `GET /api/customers/<id>` - Get customer by ID
- `POST /api/customers` - Create new customer
- `PUT /api/customers/<id>` - Update customer
- `DELETE /api/customers/<id>` - Delete customer

### Products
- `GET /api/products` - List all products
- `GET /api/products/<id>` - Get product by ID
- `POST /api/products` - Create new product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Orders
- `GET /api/orders` - List all orders
- `GET /api/orders/<id>` - Get order by ID
- `POST /api/orders` - Create new order
- `PUT /api/orders/<id>` - Update order
- `DELETE /api/orders/<id>` - Cancel order

### Query Parameters
- `page` - Page number (default: 1)
- `limit` - Items per page (default: 50)
- `status` - Filter by status
- `category` - Filter products by category
- `customer_id` - Filter orders by customer

## Project Structure

```
crm_inventory_api/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/              # Data models
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic
│   └── utils/               # Database & helpers
├── config/
│   └── config.py            # Configuration
├── database/
│   └── schema.sql           # Database schema
├── app.py                   # Application entry point
├── requirements.txt         # Dependencies
└── .env.example            # Environment template
```

## Development

Run tests:
```bash
pytest
```

Code formatting:
```bash
black app/
```

Linting:
```bash
flake8 app/
```

## License

MIT
