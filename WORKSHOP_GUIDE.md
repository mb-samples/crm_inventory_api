# AWS Transform Custom Workshop: MSSQL to Aurora PostgreSQL Migration
## Python Flask Microservice Database Migration

**Duration:** 3 hours  
**Level:** Intermediate  
**Prerequisites:** Python/Flask experience, basic database knowledge, AWS account access

---

## Workshop Overview

This hands-on workshop guides you through migrating a Python Flask microservice from Microsoft SQL Server to Amazon Aurora PostgreSQL using AWS Transform Custom. You'll learn how to:

- Define custom transformations for database migrations
- Execute transformations using AWS Transform Custom CLI
- Validate migrated code against Aurora PostgreSQL
- Apply continual learning to improve transformation quality

### What You'll Build

You'll transform the **CRM & Inventory Management API** - a production-ready Flask application with:
- 39 REST API endpoints (CRUD + Analytics)
- 14 database models
- Complex multi-table joins
- Connection pooling
- Comprehensive test suite

---

## Table of Contents

1. [Prerequisites & Setup](#section-1-prerequisites--setup) (30 minutes)
2. [Understanding the Source Application](#section-2-understanding-the-source-application) (20 minutes)
3. [Creating the Transformation Definition](#section-3-creating-the-transformation-definition) (30 minutes)
4. [Executing the Transformation](#section-4-executing-the-transformation) (40 minutes)
5. [Testing & Validation](#section-5-testing--validation) (30 minutes)
6. [Review & Continual Learning](#section-6-review--continual-learning) (20 minutes)
7. [Wrap-up & Next Steps](#section-7-wrap-up--next-steps) (10 minutes)

---

## Section 1: Prerequisites & Setup
**Time: 30 minutes**

### 1.1 Required Tools & Access

**AWS Resources:**
- AWS account with Transform Custom access
- IAM permissions for Transform Custom operations
- Aurora PostgreSQL cluster (will provision if needed)
- AWS CLI configured with credentials

**Local Development:**
- Python 3.11+ installed (verify with `python3 --version`)
- Git installed
- Code editor (VS Code, PyCharm, etc.)
- Terminal/command line access


### 1.2 Install AWS Transform Custom CLI

**Note:** Detailed installation instructions will be provided by your workshop facilitator based on the AWS Transform Custom workshop setup guide.

```bash
# Verify installation
atx --version

# Configure AWS credentials if not already done
aws configure
```

### 1.3 Clone the Workshop Repository

```bash
# Clone the repository
git clone https://github.com/mb-samples/crm_inventory_api.git
cd crm_inventory_api

# Create a working branch for the workshop
git checkout -b workshop-migration
```

### 1.4 Set Up Python Environment

```bash
# Verify Python version (should be 3.11+)
python3 --version

# Clean up any previous failed venv attempts
rm -rf venv311

# Create virtual environment
python3 -m venv venv311

# If you get an error about missing python3.11, try this alternative:
pip3 install virtualenv
virtualenv -p python3 venv311

# Activate virtual environment
source venv311/bin/activate  # On Windows: venv311\Scripts\activate

# Upgrade pip to latest version
pip install --upgrade pip

# Install current dependencies (MSSQL version)
pip install -r requirements.txt
```

**Troubleshooting Virtual Environment Creation:**

If `python3 -m venv venv311` fails with "No such file or directory" error:

```bash
# First, clean up any partial/corrupted venv directory
rm -rf venv311

# Option 1: Install python3-venv package (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3.11-venv
python3 -m venv venv311

# Option 2: Use virtualenv instead
pip3 install virtualenv
rm -rf venv311  # Clean up first
virtualenv -p python3 venv311
source venv311/bin/activate

# Option 3: Use system Python without venv (not recommended for production)
# Skip venv creation and install directly (only for workshop testing)
pip3 install -r requirements.txt --user
```

**If you see "File exists" error:**
```bash
# Remove the corrupted venv directory and try again
rm -rf venv311
virtualenv -p python3 venv311
source venv311/bin/activate
```

### 1.5 Verify Source Application

```bash
# Ensure virtual environment is activated (you should see (venv311) in prompt)
# If not activated: source venv311/bin/activate

# Start the API with mock database (no real database required for initial testing)
export USE_MOCK_DB=true
python app.py
```

**Terminal-Based Verification (if browser not available):**

Open a new terminal window and run these commands to verify the API:

```bash
# Test 1: Health check endpoint
curl http://localhost:5000/health
# Expected: {"status":"healthy","database":"connected"}

# Test 2: List customers
curl http://localhost:5000/api/customers | python3 -m json.tool

# Test 3: List products
curl http://localhost:5000/api/products | python3 -m json.tool

# Test 4: Get a specific customer
curl http://localhost:5000/api/customers/1 | python3 -m json.tool

# Test 5: Get a specific product
curl http://localhost:5000/api/products/1 | python3 -m json.tool

# Test 6: List orders
curl http://localhost:5000/api/orders | python3 -m json.tool

# Test 7: Test analytics - Customer segmentation
curl http://localhost:5000/api/analytics/customer-segmentation | python3 -m json.tool

# Test 8: Test analytics - Sales performance
curl http://localhost:5000/api/analytics/sales-performance | python3 -m json.tool

# Alternative: Use the test scripts
python test_endpoints.py      # Tests basic CRUD endpoints
python test_analytics.py       # Tests all 11 analytics endpoints
```

**Browser-Based Verification (if browser available):**

The application includes a Swagger UI interface for interactive API testing:

1. Open browser to `http://localhost:5000/apidocs/`
2. Explore the available endpoints organized by category
3. Test a few API calls directly from the browser:
   - Try the health check endpoint
   - Test a customer GET endpoint
   - Try a product search
   - Execute an analytics query

**Example Tests to Try:**
- `GET /health` - Verify API is running
- `GET /api/customers` - List customers
- `GET /api/products` - List products
- `GET /api/orders` - List orders
- `GET /api/customers/1` - Get specific customer
- `GET /api/analytics/customer-segmentation` - Advanced analytics
- `GET /api/analytics/sales-performance` - Sales metrics

**Checkpoint:** You should see JSON responses with mock data for all endpoints, confirming the API is operational with 39 endpoints (including 11 analytics endpoints) ready for testing.


### 1.6 Workshop Approach: Mock Database

**Important:** This workshop uses a mock database layer for both MSSQL and Aurora PostgreSQL phases. This approach:
- Eliminates the need for actual database provisioning
- Focuses on code transformation patterns
- Allows rapid testing and validation
- Reduces workshop costs and complexity

**Mock Database Behavior:**
- Returns realistic sample data for all queries
- Simulates database responses without actual connections
- Validates that transformed queries are syntactically correct
- Demonstrates the transformation patterns clearly

**No database setup required!** The transformation will update connection strings and query syntax, and the mock layer will validate the changes work correctly.

### 1.7 Workshop Environment Checklist

- [ ] AWS Transform Custom CLI installed and configured
- [ ] Repository cloned and on `workshop-migration` branch
- [ ] Python 3.11+ verified (`python3 --version` shows 3.11+)
- [ ] Virtual environment created and activated (or virtualenv alternative working)
- [ ] Dependencies installed from requirements.txt
- [ ] Source application running with mock database
- [ ] Swagger UI accessible at http://localhost:5000/apidocs/
- [ ] AWS credentials configured
- [ ] Mock database verified working (no real database needed)

**Note:** If virtual environment setup fails, consult the troubleshooting section in 1.4.

---

## Section 2: Understanding the Source Application
**Time: 20 minutes**

### 2.1 Application Architecture Overview

The CRM & Inventory Management API is a Flask-based microservice with:

**Database Layer:**
- Connection pooling with pyodbc
- MSSQL-specific connection strings
- Raw SQL queries with T-SQL syntax
- Stored procedure support

**Key Files to Review:**
```
app/utils/db_connection.py          # Connection pooling & MSSQL driver
app/utils/advanced_data_layer.py    # Complex analytics queries
config/config.py                     # Database configuration
app/models/*.py                      # 14 data models
app/services/*.py                    # 14 service layers with queries
```

### 2.2 Identify MSSQL-Specific Code Patterns

**Exercise:** Open these files and identify MSSQL patterns:

1. **Connection Configuration** (`config/config.py`):
   - ODBC Driver specification
   - MSSQL connection string format
   - Port 1433 (MSSQL default)

2. **Database Connection** (`app/utils/db_connection.py`):
   - `pyodbc` driver usage
   - MSSQL-specific connection parameters
   - `SELECT @@VERSION` and `GETDATE()` in test queries

3. **Query Patterns** (search across `app/services/` and `app/utils/`):
   - Square brackets: `[table_name]`
   - `TOP N` clauses
   - `GETDATE()` function
   - `ISNULL()` function
   - String concatenation with `+`
   - `EXEC` for stored procedures


### 2.3 Review Sample Queries

**Example from `app/utils/advanced_data_layer.py`:**

```python
# MSSQL-specific patterns to transform:
query = """
    SELECT TOP 100 
        c.customer_id,
        c.company_name,
        ISNULL(SUM(o.total_amount), 0) as lifetime_value,
        DATEDIFF(day, MAX(o.order_date), GETDATE()) as days_since_last_order
    FROM [customers] c
    LEFT JOIN [orders] o ON c.customer_id = o.customer_id
    WHERE c.status = 'active'
    GROUP BY c.customer_id, c.company_name
"""
```

**What needs to change for PostgreSQL:**
- `TOP 100` → `LIMIT 100`
- `ISNULL()` → `COALESCE()`
- `DATEDIFF(day, ...)` → Date arithmetic
- `GETDATE()` → `NOW()` or `CURRENT_TIMESTAMP`
- `[table_name]` → `"table_name"` or remove brackets
- Connection string and driver

**Checkpoint:** Can you identify 5+ MSSQL-specific patterns in the codebase?

---

## Section 3: Creating the Transformation Definition
**Time: 30 minutes**

### 3.1 Understanding the Transformation Definition

The transformation definition already exists at `docs/transformation_definition.md`. Let's review its structure:

**Key Components:**
1. **Objective** - Clear goal statement
2. **Summary** - High-level approach and three-phase execution model
3. **Entry Criteria** - Prerequisites for transformation
4. **Implementation Steps** - Detailed transformation instructions (12 steps)
5. **Validation/Exit Criteria** - Success metrics

### 3.2 Review the Transformation Definition

```bash
# Open and review the transformation definition
cat docs/transformation_definition.md
```

**Key Sections to Note:**

**Three-Phase Execution Model:**
- Phase 1: Analyze all files
- Phase 2: Complete ALL changes in single commit
- Phase 3: Validate after all changes

**Critical Transformation Steps:**
1. Update database connection configuration
2. Convert T-SQL syntax to PostgreSQL
3. Transform JOIN syntax
4. Update data types
5. Modify string concatenation
6. Update named parameters
7. Transform ORM patterns
8. Handle transactions
9. Update error handling
10. Modify stored procedures
11. Update pagination
12. Test and validate


### 3.3 Publish Transformation to Registry

Now let's publish this transformation definition to your AWS Transform Custom registry:

```bash
# Navigate to project root
cd /path/to/crm_inventory_api

# Publish the transformation definition
atx custom def publish \
    -n mssql-to-aurora-postgres \
    --description "Migrate Python Flask microservice from MSSQL to Aurora PostgreSQL" \
    --sd docs/

# Verify publication
atx custom def list
```

**Expected Output:**
```
Transformation Name: mssql-to-aurora-postgres
Version: v1
Status: Published
Description: Migrate Python Flask microservice from MSSQL to Aurora PostgreSQL
```

### 3.4 Optional: Add Reference Materials

If you have additional reference materials (migration guides, code samples), add them:

```bash
# Create document_references folder if needed
mkdir -p docs/document_references

# Add reference materials (examples)
# - PostgreSQL migration guide
# - psycopg2 documentation
# - Before/after code examples

# Re-publish with references
atx custom def publish \
    -n mssql-to-aurora-postgres \
    --description "Migrate Python Flask microservice from MSSQL to Aurora PostgreSQL" \
    --sd docs/
```

**Checkpoint:** Transformation definition is published and visible in registry.

---

## Section 4: Executing the Transformation
**Time: 40 minutes**

### 4.1 Understanding the Mock Database Approach

**Important Context:**
- The application uses a mock database layer (`app/utils/mock_db.py`)
- No actual MSSQL or Aurora PostgreSQL connections are made
- The transformation updates code patterns, connection strings, and query syntax
- Mock responses validate that transformed code is syntactically correct

**What Gets Transformed:**
- Database driver imports (pyodbc → psycopg2)
- Connection string format (MSSQL → PostgreSQL)
- Query syntax (T-SQL → PostgreSQL)
- Parameter placeholders (? → %s)
- SQL functions (GETDATE() → NOW(), etc.)

**What Stays Mocked:**
- Actual database connections
- Query execution and results
- Data persistence

### 4.2 Execute Transformation (Interactive Mode)

**Option A: Interactive Execution (Recommended for Workshop)**

```bash
# Execute transformation with interactive mode
atx custom def exec \
    -n mssql-to-aurora-postgres \
    -p . \
    -c "python -m py_compile app/**/*.py"

# The agent will:
# 1. Analyze all Python files
# 2. Create an execution plan
# 3. Pause for your review
# 4. Execute transformations step-by-step
# 5. Allow you to provide feedback
```

**During Execution:**
- Review the execution plan when prompted
- Approve or provide feedback on proposed changes
- Monitor progress through each transformation step
- Interrupt if you see issues (Ctrl+C)


### 4.3 Review Execution Plan

The agent will present an execution plan. Review for:

**Expected Changes:**
1. ✅ `config/config.py` - PostgreSQL connection string
2. ✅ `app/utils/db_connection.py` - psycopg2 driver
3. ✅ `requirements.txt` - Add psycopg2-binary
4. ✅ All service files - Query syntax updates
5. ✅ `app/utils/advanced_data_layer.py` - Complex query transformations

**Sample Plan Output:**
```
Execution Plan:
==============
Phase 1: Analysis Complete
- Found 28 files requiring changes
- Identified 156 MSSQL-specific patterns
- Cataloged 89 query transformations needed

Phase 2: Transformation Steps
1. Update config/config.py (connection string)
2. Update app/utils/db_connection.py (driver)
3. Update requirements.txt (dependencies)
4. Transform queries in app/services/*.py (14 files)
5. Transform queries in app/utils/advanced_data_layer.py
6. Update error handling across all files

Proceed with transformation? (y/n):
```

### 4.4 Monitor Transformation Progress

As the transformation executes, you'll see:

```
[Step 1/6] Updating database configuration...
  ✓ Modified config/config.py
  ✓ Updated connection string to PostgreSQL format
  ✓ Changed default port to 5432

[Step 2/6] Updating database driver...
  ✓ Modified app/utils/db_connection.py
  ✓ Replaced pyodbc with psycopg2
  ✓ Updated connection parameters

[Step 3/6] Updating dependencies...
  ✓ Modified requirements.txt
  ✓ Added psycopg2-binary==2.9.9
  ✓ Removed pyodbc and pymssql

[Step 4/6] Transforming service layer queries...
  ✓ Modified app/services/customer_service.py (12 queries)
  ✓ Modified app/services/order_service.py (18 queries)
  ... (continues for all services)
```


### 4.5 Provide Feedback During Execution

If you notice issues or want to provide guidance:

**Example Interaction:**
```
Agent: I'm about to transform the DATEDIFF function. 
       Should I use AGE() or date arithmetic?

You: Use date arithmetic with CURRENT_DATE for consistency.

Agent: Understood. Applying date arithmetic pattern...
```

**Common Feedback Opportunities:**
- Naming conventions for new functions
- Specific PostgreSQL features to use
- Error handling approaches
- Transaction isolation levels

### 4.6 Review Changes After Execution

```bash
# View all changes made
git status

# Review specific file changes
git diff config/config.py
git diff app/utils/db_connection.py
git diff app/services/customer_service.py

# View summary of changes
git diff --stat
```

**Expected Changes Summary:**
```
config/config.py                          | 15 +++---
app/utils/db_connection.py                | 45 ++++++++--------
requirements.txt                          |  3 +-
app/services/customer_service.py          | 28 +++++-----
app/services/order_service.py             | 35 ++++++------
app/utils/advanced_data_layer.py          | 89 +++++++++++++++---------------
... (additional files)
```

**Checkpoint:** All transformations complete, changes reviewed.

---

## Section 5: Testing & Validation
**Time: 30 minutes**

### 5.1 Install PostgreSQL Dependencies

```bash
# Ensure virtual environment is activated
source venv311/bin/activate

# Install new dependencies
pip install psycopg2-binary==2.9.9

# Verify installation
python -c "import psycopg2; print(psycopg2.__version__)"
```

### 5.2 Verify Mock Database Configuration

```bash
# Ensure mock database is enabled
export USE_MOCK_DB=true

# Verify environment
echo $USE_MOCK_DB
```

### 5.3 Test Database Connection Layer

```bash
# Test that the connection layer works with PostgreSQL configuration
python -c "
from app.utils.db_connection import test_connection
result = test_connection()
print('Connection layer working!' if result else 'Connection layer failed!')
"
```

**Expected Output:**
```
INFO: Using MOCK database connection
Connection layer working!
```

**Note:** The mock database simulates PostgreSQL responses without actual connections.


### 5.4 Run Application Tests

**Test 1: Start the Application**
```bash
# Start Flask application with mock database
export USE_MOCK_DB=true
python app.py

# In another terminal, test health endpoint
curl http://localhost:5000/health
```

**Expected Output:**
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

**Test 2: Run Automated Test Suite**
```bash
# Run all endpoint tests (uses mock database)
python validate_api.py

# Run analytics tests
python test_analytics.py

# Run basic tests
python test_endpoints.py
```

**Expected Results:**
```
✓ Health Check: PASSED
✓ Customer Endpoints: PASSED (3/3)
✓ Product Endpoints: PASSED (3/3)
✓ Order Endpoints: PASSED (3/3)
✓ Analytics Endpoints: PASSED (11/11)

Total: 39/39 tests PASSED (100%)
```

**Note:** All tests use mock database responses, validating that the transformed code syntax is correct.


### 5.5 Test Complex Queries

**Test Analytics Endpoints (Complex Joins):**

```bash
# Test customer segmentation (complex multi-table join)
curl http://localhost:5000/api/analytics/customer-segmentation | python -m json.tool

# Test sales performance
curl "http://localhost:5000/api/analytics/sales-performance?period=month" | python -m json.tool

# Test inventory status
curl http://localhost:5000/api/analytics/inventory-status | python -m json.tool
```

**Verify Results:**
- Mock data returns without errors
- Result sets match expected structure
- Response times are fast (< 100ms with mock data)
- Transformed query syntax is validated by mock layer

### 5.6 Validation Checklist

Go through the exit criteria from the transformation definition:

- [ ] Database connection layer updated to PostgreSQL format
- [ ] All queries use PostgreSQL-compatible syntax
- [ ] Complex multi-table joins transformed correctly
- [ ] Data types are PostgreSQL-compatible
- [ ] String operations use PostgreSQL conventions
- [ ] Named parameters use psycopg2 syntax (%s instead of ?)
- [ ] All CRUD operations work without errors
- [ ] Mock database validates transformed code
- [ ] All tests pass (39/39 endpoints)
- [ ] Application functionality intact
- [ ] Code is ready for real PostgreSQL connection

**Checkpoint:** Application fully functional with transformed PostgreSQL code patterns.

---

## Section 6: Review & Continual Learning
**Time: 20 minutes**

### 6.1 Understanding Continual Learning

AWS Transform Custom automatically captures learnings from your execution to improve future transformations. After execution completes, the system extracts "knowledge items" based on:

- Feedback you provided during execution
- Code fixes or adjustments made
- Issues encountered and resolved
- Successful transformation patterns

### 6.2 Review Knowledge Items

```bash
# List knowledge items created from this execution
atx custom def list-ki -n mssql-to-aurora-postgres

# View details of a specific knowledge item
atx custom def get-ki -n mssql-to-aurora-postgres --id <knowledge-item-id>
```

**Example Knowledge Items:**
```
Knowledge Item #1:
- Pattern: DATEDIFF(day, date1, date2) conversion
- Learning: Use (date2::date - date1::date) for day differences
- Status: NOT_APPROVED
- Confidence: HIGH

Knowledge Item #2:
- Pattern: Connection string format for Aurora PostgreSQL
- Learning: Include sslmode=require for Aurora connections
- Status: NOT_APPROVED
- Confidence: MEDIUM
```

### 6.3 Approve Valuable Knowledge Items

Review and approve knowledge items that will improve future executions:

```bash
# Enable a knowledge item
atx custom def update-ki-status \
    -n mssql-to-aurora-postgres \
    --id <knowledge-item-id> \
    --status ENABLED

# Disable a knowledge item if not useful
atx custom def update-ki-status \
    -n mssql-to-aurora-postgres \
    --id <knowledge-item-id> \
    --status DISABLED
```


### 6.4 Configure Auto-Approval (Optional)

For trusted transformation patterns, enable auto-approval:

```bash
# Enable auto-approval for future knowledge items
atx custom def update-ki-config \
    -n mssql-to-aurora-postgres \
    --auto-enabled TRUE
```

**Warning:** Only enable auto-approval after validating the transformation produces high-quality results.

### 6.5 Export Knowledge Items

Export knowledge items for documentation or sharing with your team:

```bash
# Export to markdown
atx custom def export-ki-markdown -n mssql-to-aurora-postgres

# Review the exported file
cat mssql-to-aurora-postgres-knowledge-items.md
```

### 6.6 Discussion: Continual Learning Benefits

**Group Discussion Topics:**
1. What patterns did the system learn from your execution?
2. Which knowledge items would you approve for future use?
3. How could continual learning reduce manual effort in future migrations?
4. What feedback mechanisms were most valuable?

**Key Takeaways:**
- Continual learning improves with each execution
- Approved knowledge items enhance future transformations
- Team feedback creates organizational knowledge
- Quality improves over time without manual updates

---

## Section 7: Wrap-up & Next Steps
**Time: 10 minutes**

### 7.1 Commit Your Changes

```bash
# Review all changes one final time
git status
git diff --stat

# Commit the migrated code
git add .
git commit -m "Migrate from MSSQL to Aurora PostgreSQL using AWS Transform Custom

- Updated database driver from pyodbc to psycopg2
- Converted T-SQL syntax to PostgreSQL equivalents
- Transformed all queries in services and utils layers
- Updated connection configuration for Aurora
- All 39 endpoints tested and validated
- 100% test pass rate maintained"

# Push to your branch
git push origin workshop-migration
```

### 7.2 Workshop Summary

**What You Accomplished:**
✅ Set up AWS Transform Custom CLI and environment
✅ Analyzed MSSQL-specific code patterns in Flask application
✅ Published custom transformation definition to registry
✅ Executed transformation with interactive feedback
✅ Validated migrated application against Aurora PostgreSQL
✅ Reviewed and approved continual learning knowledge items
✅ Successfully migrated 39 API endpoints with 100% test coverage

**Key Metrics:**
- Files transformed: ~28 Python files
- Queries updated: 150+ SQL queries
- Test coverage: 100% (39/39 endpoints)
- Execution time: ~40 minutes
- Manual effort saved: Estimated 40-60 hours


### 7.3 Next Steps for Your Organization

**Immediate Actions:**
1. **Apply to Real Databases:**
   - Use this transformation on codebases with actual MSSQL connections
   - Provision Aurora PostgreSQL for production
   - Migrate database schema separately (using AWS DMS or manual migration)
   - Test with real database connections

2. **Validate with Real Data:**
   - Run comprehensive integration tests
   - Verify query performance with actual data volumes
   - Test transaction handling and error scenarios

3. **Team Enablement:**
   - Share transformation definition with team
   - Document organization-specific patterns
   - Train team on AWS Transform Custom

**Long-term Strategy:**
1. **Build Transformation Library:**
   - Create transformations for other common patterns
   - Document best practices
   - Share across teams

2. **Integrate with CI/CD:**
   - Automate transformation execution
   - Add validation gates
   - Track transformation metrics

3. **Leverage Continual Learning:**
   - Regularly review knowledge items
   - Approve high-quality patterns
   - Monitor transformation quality improvements

### 7.4 Additional Resources

**AWS Transform Custom Documentation:**
- CLI Reference Guide
- Transformation Definition Best Practices
- Continual Learning Deep Dive
- Security and IAM Configuration

**PostgreSQL Migration Resources:**
- Aurora PostgreSQL Best Practices
- Performance Tuning Guide
- Migration Patterns and Anti-patterns

**Community:**
- AWS Transform Custom User Forum
- Migration Success Stories
- Sample Transformation Definitions


### 7.5 Troubleshooting Common Issues

**Issue 1: Import Errors After Transformation**
```bash
# Ensure psycopg2 is installed
pip install psycopg2-binary

# Verify imports work
python -c "import psycopg2; print('OK')"
```

**Issue 2: Mock Database Not Working**
```bash
# Verify environment variable is set
export USE_MOCK_DB=true
echo $USE_MOCK_DB

# Check mock_db.py exists
ls -la app/utils/mock_db.py
```

**Issue 3: Query Syntax Errors in Transformed Code**
```bash
# Review transformation logs
atx --resume  # Resume conversation to fix issues
# Provide specific feedback on failed queries
```

**Issue 4: Tests Failing After Transformation**
```bash
# Check which specific tests fail
python validate_api.py -v

# Review the transformed query syntax in the failing service
# Provide feedback to transformation for correction
```

**Issue 5: Knowledge Items Not Appearing**
```bash
# Ensure you provided feedback during execution
# Check that -d flag was NOT used (disables learning)
# Wait a few minutes for processing
```

### 7.6 Workshop Feedback

**Please provide feedback on:**
- Workshop pacing and content
- AWS Transform Custom tool usability
- Transformation definition quality
- Documentation clarity
- Areas for improvement

**Survey Link:** [To be provided by facilitator]

---

## Appendix A: Workshop Approach - Mock Database

### Why Mock Database?

This workshop uses a mock database approach for several important reasons:

1. **Focus on Code Transformation:**
   - Eliminates database provisioning complexity
   - Focuses learning on transformation patterns
   - Reduces workshop setup time

2. **Cost Efficiency:**
   - No Aurora PostgreSQL charges
   - No data transfer costs
   - No MSSQL licensing needed

3. **Rapid Iteration:**
   - Instant feedback on code changes
   - No network latency
   - Fast test execution

4. **Simplified Environment:**
   - No VPC/security group configuration
   - No database credentials management
   - Works on any laptop

### Mock Database Implementation

The application includes `app/utils/mock_db.py` which:
- Simulates pyodbc and psycopg2 connection interfaces
- Returns realistic sample data for all queries
- Validates query syntax is correct
- Supports both MSSQL and PostgreSQL connection patterns

### Real-World Application

After the workshop, apply the same transformation to:
- Production codebases with real MSSQL connections
- Applications that will connect to actual Aurora PostgreSQL
- Use AWS DMS for schema and data migration
- Test with real data volumes and query patterns

---


## Appendix B: CLI Commands Quick Reference

### Transformation Management
```bash
# List transformations
atx custom def list

# Publish transformation
atx custom def publish -n <name> --description "<desc>" --sd <source-dir>

# Execute transformation (interactive)
atx custom def exec -n <name> -p <path>

# Execute transformation (non-interactive)
atx custom def exec -n <name> -p <path> -x -t

# Get transformation details
atx custom def get -n <name>

# Delete transformation
atx custom def delete -n <name>
```

### Knowledge Item Management
```bash
# List knowledge items
atx custom def list-ki -n <name>

# Get knowledge item details
atx custom def get-ki -n <name> --id <ki-id>

# Enable knowledge item
atx custom def update-ki-status -n <name> --id <ki-id> --status ENABLED

# Disable knowledge item
atx custom def update-ki-status -n <name> --id <ki-id> --status DISABLED

# Export knowledge items
atx custom def export-ki-markdown -n <name>

# Configure auto-approval
atx custom def update-ki-config -n <name> --auto-enabled TRUE
```

### Conversation Management
```bash
# Start interactive mode
atx

# Resume last conversation
atx --resume

# Resume specific conversation
atx --conversation-id <id>
```

### Utility Commands
```bash
# Check version
atx --version

# Update CLI
atx update

# View help
atx custom --help
```


## Appendix C: Sample Transformation Patterns

### Pattern 1: T-SQL to PostgreSQL Function Mapping

| MSSQL Function | PostgreSQL Equivalent | Example |
|----------------|----------------------|---------|
| `GETDATE()` | `NOW()` or `CURRENT_TIMESTAMP` | `SELECT NOW()` |
| `ISNULL(col, val)` | `COALESCE(col, val)` | `COALESCE(amount, 0)` |
| `LEN(str)` | `LENGTH(str)` | `LENGTH(company_name)` |
| `DATEDIFF(day, d1, d2)` | `(d2::date - d1::date)` | `(order_date::date - created_date::date)` |
| `TOP N` | `LIMIT N` | `SELECT * FROM orders LIMIT 100` |
| `CONVERT(type, val)` | `val::type` or `CAST(val AS type)` | `amount::numeric` |

### Pattern 2: Connection String Transformation

**Before (MSSQL):**
```python
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server},{port};"
    f"DATABASE={database};"
    f"UID={user};"
    f"PWD={password};"
)
```

**After (PostgreSQL):**
```python
connection_string = (
    f"host={server} "
    f"port={port} "
    f"dbname={database} "
    f"user={user} "
    f"password={password} "
    f"sslmode=require"
)
```

### Pattern 3: Query Parameter Syntax

**Before (MSSQL with pyodbc):**
```python
cursor.execute(
    "SELECT * FROM customers WHERE customer_id = ?",
    (customer_id,)
)
```

**After (PostgreSQL with psycopg2):**
```python
cursor.execute(
    "SELECT * FROM customers WHERE customer_id = %s",
    (customer_id,)
)
```


## Appendix D: Pre-Workshop Checklist

**For Workshop Facilitators:**

- [ ] AWS accounts provisioned for all participants
- [ ] IAM permissions configured for Transform Custom
- [ ] Aurora PostgreSQL clusters created (or CloudFormation template ready)
- [ ] Workshop repository forked/cloned for each participant
- [ ] AWS Transform Custom CLI installation guide distributed
- [ ] Network access verified (security groups, VPC configuration)
- [ ] Sample data loaded into Aurora PostgreSQL (optional)
- [ ] Backup slides prepared for AWS setup sections
- [ ] Troubleshooting guide ready
- [ ] Post-workshop survey prepared

**For Participants (Send 1 Week Before):**

- [ ] AWS account access confirmed
- [ ] AWS CLI installed and configured
- [ ] Python 3.11+ installed (verify with `python3 --version`)
- [ ] Git installed
- [ ] Code editor installed
- [ ] Terminal/command line familiarity
- [ ] Basic SQL knowledge refreshed
- [ ] Repository cloned locally
- [ ] Virtual environment tested with `python3 -m venv test_env`

**Day Before Workshop:**

- [ ] Test Aurora PostgreSQL connectivity
- [ ] Verify AWS Transform Custom CLI installation
- [ ] Run through workshop steps once
- [ ] Prepare questions for facilitator
- [ ] Review transformation definition document

---

## Appendix E: Cost Estimation

**Workshop Resources (Per Participant):**

| Resource | Configuration | Duration | Estimated Cost |
|----------|--------------|----------|----------------|
| AWS Transform Custom | Standard usage | 1 execution | $2.00 |
| Local Development | Laptop/workstation | Workshop | $0.00 |
| **Total per participant** | | | **~$2.00** |

**Cost Savings with Mock Database Approach:**
- No Aurora PostgreSQL charges (~$0.50/hour saved)
- No data transfer costs
- No MSSQL licensing or hosting
- Minimal AWS resource usage

**For Production Implementation:**
When applying to real databases, budget for:
- Aurora PostgreSQL cluster costs
- AWS DMS for schema/data migration
- Additional Transform Custom executions
- Testing and validation time

**Cleanup:**
No AWS resources to clean up after workshop (mock database only).

---

## Appendix F: Frequently Asked Questions

**Q: Can I use this transformation on other Python applications?**
A: Yes! The transformation definition is designed for any Python Flask application using MSSQL. You may need to adjust for application-specific patterns.

**Q: What if my application uses SQLAlchemy ORM instead of raw SQL?**
A: The transformation handles both raw SQL and ORM patterns. SQLAlchemy's dialect system makes PostgreSQL migration easier.

**Q: How long does a typical transformation take?**
A: For this workshop application (~28 files, 150+ queries), expect 30-45 minutes. Larger applications may take several hours.

**Q: Can I pause and resume a transformation?**
A: Yes! Use Ctrl+C to interrupt, then `atx --resume` to continue from where you left off (within 30 days).

**Q: What happens if the transformation makes a mistake?**
A: You can provide feedback during execution, and the agent will correct it. You can also manually fix issues and the system will learn from your corrections.

**Q: Do I need to provision Aurora PostgreSQL for this workshop?**
A: No! The workshop uses a mock database layer. No actual database provisioning is required. This keeps costs low and focuses on code transformation patterns.

**Q: Will the transformation work with real databases?**
A: Absolutely! The same transformation definition works with real MSSQL and Aurora PostgreSQL. After the workshop, apply it to production codebases with actual database connections.

**Q: How do I test with a real database after the workshop?**
A: Set `USE_MOCK_DB=false` in your environment, provide real database credentials, and the application will connect to actual Aurora PostgreSQL. You'll need to migrate the schema separately using AWS DMS or manual migration.

**Q: Can I run this in CI/CD pipelines?**
A: Absolutely! Use non-interactive mode (`-x -t` flags) for automated execution in pipelines.

**Q: How does pricing work for AWS Transform Custom?**
A: Pricing is based on execution time and complexity. Check AWS pricing page for current rates. This workshop execution costs approximately $2-3.

**Q: Can I share transformations across AWS accounts?**
A: Transformations are account-specific. You'll need to publish the transformation definition in each account.

**Q: What if I have stored procedures in MSSQL?**
A: The transformation can convert simple stored procedures to PostgreSQL PL/pgSQL or suggest refactoring into application logic for complex ones.

---

## Appendix G: Additional Exercises (Optional)

### Exercise 1: Add a New Endpoint
**Objective:** Test your understanding by adding a new endpoint that works with PostgreSQL.

**Task:**
1. Create a new analytics endpoint in `app/services/`
2. Write a complex query using PostgreSQL-specific features
3. Test the endpoint
4. Verify it follows PostgreSQL best practices

### Exercise 2: Performance Optimization
**Objective:** Optimize queries for PostgreSQL.

**Task:**
1. Use `EXPLAIN ANALYZE` on complex queries
2. Identify slow queries
3. Add appropriate indexes
4. Compare performance before/after

### Exercise 3: Create a Custom Transformation
**Objective:** Build your own transformation definition.

**Task:**
1. Identify a different migration pattern (e.g., Python 2 to 3)
2. Write a transformation definition
3. Test on sample code
4. Publish to registry

### Exercise 4: Bulk Migration
**Objective:** Apply transformation to multiple repositories.

**Task:**
1. Clone 2-3 similar Flask applications
2. Execute transformation on each
3. Compare results and learnings
4. Review accumulated knowledge items

---

## Conclusion

Congratulations on completing the AWS Transform Custom workshop! You've successfully:

✅ Migrated a production-ready Flask application from MSSQL to Aurora PostgreSQL
✅ Learned how to create and execute custom transformations
✅ Experienced the power of AI-driven code modernization
✅ Understood continual learning and knowledge accumulation
✅ Gained hands-on experience with AWS Transform Custom CLI

**Key Takeaways:**
- AWS Transform Custom dramatically reduces manual migration effort
- Custom transformation definitions enable repeatable, consistent migrations
- Continual learning improves quality with each execution
- Interactive mode provides control while maintaining automation benefits
- The tool scales from single applications to enterprise-wide transformations

**Thank you for participating!**

For questions, feedback, or support, contact your workshop facilitator or AWS support team.

---

**Workshop Guide Version:** 1.0  
**Last Updated:** February 2026  
**Repository:** https://github.com/mb-samples/crm_inventory_api  
**Transformation Definition:** docs/transformation_definition.md

