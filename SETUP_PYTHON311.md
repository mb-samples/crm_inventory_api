# Python 3.11 Setup Guide

This project requires Python 3.11 for database driver compatibility (`pyodbc` and `pymssql`).

## Quick Setup

Run the automated setup script:

```bash
./setup.sh
```

## Manual Setup

### 1. Install Python 3.11

```bash
brew install python@3.11
```

### 2. Create Virtual Environment

```bash
python3.11 -m venv venv311
source venv311/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

## Running the Application

### Option 1: Mock API Server (No Database Required)

Perfect for development and testing:

```bash
source venv311/bin/activate
python app.py
```

Access at: http://localhost:5000/health

### Option 2: Real Application (Requires Database)

For production with actual MSSQL database:

```bash
source venv311/bin/activate
python app.py
```

## Why Python 3.11?

- Python 3.13+ and 3.14 have compatibility issues with `pyodbc` and `pymssql`
- These database drivers require C extensions that haven't been updated yet
- Python 3.11 is the latest stable version with full database driver support

## Troubleshooting

### Database Connection Errors

If you see database connection errors:

1. Ensure SQL Server is running
2. Check credentials in `.env` file
3. Verify ODBC Driver 17 is installed:
   ```bash
   brew install unixodbc
   ```

### Import Errors

If you see import errors:

1. Ensure you're in the correct virtual environment:
   ```bash
   source venv311/bin/activate
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
crm_inventory_api/
├── venv311/              # Python 3.11 virtual environment
├── app/                  # Application code
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   ├── services/        # Business logic
│   └── utils/           # Database connection & helpers
├── app.py               # Application entry point
├── requirements.txt     # Python dependencies
├── setup.sh             # Automated setup script
└── .env                 # Environment configuration
```

## Next Steps

1. For API testing: Use `app.py` with `USE_MOCK_DB=true`
2. For database setup: Follow `database/schema.sql`
3. For production: Configure `.env` and run `app.py`
