# Quick Start Guide

## Setup Steps

1. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup environment variables:**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. **Setup database:**
```bash
# Make sure SQL Server is running
# Run the schema file:
sqlcmd -S localhost -U sa -P YourPassword -i database/schema.sql
```

5. **Run the application:**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Test the API

Health check:
```bash
curl http://localhost:5000/health
```

Create a customer:
```bash
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -d '{
    "customer_code": "CUST001",
    "company_name": "Acme Corp",
    "customer_type": "business",
    "email": "contact@acme.com",
    "phone": "555-0100"
  }'
```

Get all customers:
```bash
curl http://localhost:5000/api/customers
```

## Troubleshooting

**Database connection issues:**
- Verify SQL Server is running
- Check credentials in `.env` file
- Ensure ODBC Driver 17 is installed

**Import errors:**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

**Port already in use:**
- Change port in `.env`: `PORT=5001`
- Or kill the process using port 5000
