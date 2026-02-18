# Migrate Python Flask Microservice Database Queries from MSSQL to Aurora PostgreSQL

## Objective
Transform Python Flask microservice database access code from MSSQL to Aurora PostgreSQL, focusing on SQL query syntax differences, join operations, data type mappings, and named query patterns to ensure compatibility with PostgreSQL while maintaining application functionality.

## Summary
This transformation updates database queries in a Python Flask microservice from MSSQL syntax to PostgreSQL syntax. The process involves converting T-SQL specific syntax to PostgreSQL equivalents, updating join syntax and patterns, modifying data type references, adjusting string concatenation and operators, updating named parameters and query formatting, and adapting both raw SQL queries and ORM expressions to PostgreSQL standards. Special attention is given to complex multi-table joins which require careful syntax translation between the two database systems. This transformation follows a three-phase execution model: (1) Analyze all files to identify required changes, (2) Complete ALL changes in a single commit, (3) Validate once at the end after all changes are applied.

## Entry Criteria
1. The codebase is a Python Flask microservice application
2. The application contains database access code connecting to MSSQL
3. The code includes a mix of raw SQL queries and ORM (such as SQLAlchemy) operations
4. Queries include SELECT, INSERT, UPDATE, and DELETE operations with multiple joins
5. The database schema has been or will be migrated to Aurora PostgreSQL
6. Named queries or parameterized queries are present in the codebase

## Implementation Steps

### EXECUTION APPROACH: Three-Phase Model

**Phase 1: Analysis**
- Scan and analyze all Python files in the codebase
- Identify all database queries, connection strings, and ORM configurations
- Catalog all required transformations across the entire codebase
- Document all files that require changes

**Phase 2: Complete ALL Changes in Single Commit**
- Apply all identified transformations across all files
- Make all changes atomically before committing
- Ensure consistency across the entire codebase

**Phase 3: Validation**
- After ALL changes are complete, perform comprehensive validation
- Execute all tests against Aurora PostgreSQL
- Verify query results and application functionality

### Detailed Transformation Steps

1. **Update database connection configuration**
   - Replace MSSQL connection strings with PostgreSQL connection strings
   - Update database driver from `pyodbc` or `pymssql` to `psycopg2` or `psycopg2-binary`
   - Modify SQLAlchemy engine configuration to use `postgresql://` dialect instead of `mssql://`
   - Update connection parameters (host, port, database name, credentials) to point to Aurora PostgreSQL endpoint

2. **Convert T-SQL specific syntax to PostgreSQL equivalents**
   - Replace square bracket identifiers `[table_name]` with double quotes `"table_name"` or remove if not needed
   - Convert `TOP N` clauses to `LIMIT N` at the end of queries
   - Replace `GETDATE()` with `NOW()` or `CURRENT_TIMESTAMP`
   - Convert `ISNULL(column, default)` to `COALESCE(column, default)`
   - Replace `LEN()` function with `LENGTH()` or `CHAR_LENGTH()`
   - Update `DATEDIFF()` syntax to PostgreSQL date arithmetic or `AGE()` function
   - Convert `CONVERT()` or `CAST()` functions to PostgreSQL equivalents where syntax differs

3. **Transform JOIN syntax and patterns**
   - Convert old-style MSSQL joins using comma-separated tables with WHERE conditions to explicit JOIN syntax
   - Replace `*=` (left outer join) and `=*` (right outer join) operators with `LEFT JOIN` and `RIGHT JOIN`
   - Ensure all multi-table joins use explicit `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, or `FULL OUTER JOIN` keywords
   - Verify JOIN conditions are properly placed in `ON` clauses rather than `WHERE` clauses
   - Review and test complex joins with multiple tables to ensure correct result sets
   - Update any MSSQL-specific join hints (e.g., `WITH (NOLOCK)`) to PostgreSQL equivalents or remove if not applicable

4. **Update data type references and conversions**
   - Replace `VARCHAR(MAX)` with `TEXT` or appropriate `VARCHAR(n)` size
   - Convert `NVARCHAR` to `VARCHAR` or `TEXT` (PostgreSQL uses UTF-8 by default)
   - Replace `BIT` data type with `BOOLEAN`
   - Update `DATETIME` and `DATETIME2` to `TIMESTAMP` or `TIMESTAMP WITH TIME ZONE`
   - Convert `UNIQUEIDENTIFIER` to `UUID`
   - Replace `MONEY` with `NUMERIC` or `DECIMAL`
   - Update `IMAGE` or `VARBINARY(MAX)` to `BYTEA`

5. **Modify string concatenation and operators**
   - Replace `+` operator for string concatenation with `||` operator or `CONCAT()` function
   - Update string comparison operators if case-sensitivity behavior differs
   - Convert `%` wildcard patterns in LIKE clauses (generally compatible but verify behavior)
   - Replace `'` + `'` empty string checks with appropriate PostgreSQL null/empty string handling

6. **Update named parameters and query formatting**
   - Convert MSSQL named parameters from `@parameter` to PostgreSQL style `%(parameter)s` for raw queries
   - Update parameterized queries to use appropriate placeholder syntax for the database driver
   - For psycopg2, use `%s` positional or `%(name)s` named parameter style
   - Ensure parameter binding in ORM queries follows PostgreSQL conventions
   - Review and update any dynamic SQL construction to prevent SQL injection

7. **Transform ORM-specific query patterns**
   - Update SQLAlchemy Column type definitions to PostgreSQL-compatible types
   - Replace MSSQL-specific SQLAlchemy types with PostgreSQL equivalents
   - Verify that SQLAlchemy relationships and lazy loading work correctly with PostgreSQL
   - Update any raw SQL executed through ORM session to use PostgreSQL syntax
   - Test ORM-generated queries for performance and correctness

8. **Handle transaction and isolation level differences**
   - Review transaction handling code for MSSQL-specific behavior
   - Update isolation level settings to PostgreSQL equivalents (READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE)
   - Replace `WITH (NOLOCK)` hints with appropriate transaction isolation levels
   - Verify autocommit behavior matches application requirements

9. **Update error handling and exception types**
   - Replace MSSQL-specific exception handling (e.g., `pyodbc.Error`) with PostgreSQL driver exceptions (e.g., `psycopg2.Error`)
   - Update error code checking to use PostgreSQL error codes instead of MSSQL codes
   - Verify that constraint violations and unique key errors are handled appropriately

10. **Modify stored procedure calls and functions**
    - If stored procedures exist, rewrite them in PostgreSQL PL/pgSQL or replace with application logic
    - Update function call syntax from `EXEC procedure_name` to `SELECT * FROM function_name()` or appropriate PostgreSQL syntax
    - Convert user-defined functions to PostgreSQL-compatible syntax
    - Replace MSSQL-specific system functions with PostgreSQL equivalents

11. **Update pagination and offset queries**
    - Convert `OFFSET X ROWS FETCH NEXT Y ROWS ONLY` to `LIMIT Y OFFSET X`
    - Ensure pagination logic accounts for PostgreSQL zero-based or one-based indexing behavior
    - Verify performance of LIMIT/OFFSET on large result sets

12. **Test and validate query results**
    - Execute transformed queries against Aurora PostgreSQL test environment
    - Compare result sets with MSSQL output to ensure data consistency
    - Verify that complex joins return expected number of rows and correct data
    - Performance test critical queries and optimize if needed using PostgreSQL-specific features (indexes, query plans)

## Validation / Exit Criteria

1. All database connection configurations point to Aurora PostgreSQL and successfully establish connections
2. All raw SQL queries use PostgreSQL-compatible syntax with no T-SQL remnants
3. Complex multi-table joins execute successfully and return correct result sets
4. All data type references and conversions are PostgreSQL-compatible
5. String concatenation and operators follow PostgreSQL conventions
6. Named parameters and query placeholders use appropriate PostgreSQL/psycopg2 syntax
7. ORM queries and models work correctly with PostgreSQL backend
8. All SELECT, INSERT, UPDATE, and DELETE operations execute without errors
9. Transaction handling and isolation levels behave as expected
10. Error handling catches and processes PostgreSQL-specific exceptions appropriately
11. All unit tests and integration tests pass with Aurora PostgreSQL
12. Application functionality remains intact with no regression in features
13. Query performance meets or exceeds previous MSSQL performance benchmarks
