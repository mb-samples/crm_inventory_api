# AWS Transform Custom Workshop - Quick Summary

## Workshop Details
- **Duration:** 3 hours
- **Topic:** Migrate Python Flask Microservice from MSSQL to Aurora PostgreSQL
- **Repository:** https://github.com/mb-samples/crm_inventory_api
- **Transformation Definition:** `docs/transformation_definition.md`

## Time Breakdown

| Section | Duration | Activities |
|---------|----------|------------|
| 1. Prerequisites & Setup | 30 min | AWS setup, CLI install, repo clone, Aurora provision |
| 2. Understanding Source App | 20 min | Review architecture, identify MSSQL patterns |
| 3. Creating Transformation | 30 min | Review definition, publish to registry |
| 4. Executing Transformation | 40 min | Interactive execution, provide feedback, review changes |
| 5. Testing & Validation | 30 min | Install deps, test connection, run tests, validate |
| 6. Continual Learning | 20 min | Review knowledge items, approve learnings |
| 7. Wrap-up & Next Steps | 10 min | Commit changes, discuss next steps |

## Workshop Approach

**Mock Database Strategy:**
- No actual MSSQL or Aurora PostgreSQL databases required
- Uses mock database layer (`app/utils/mock_db.py`) throughout
- Focuses on code transformation patterns and syntax changes
- Validates transformed code is syntactically correct
- Reduces costs and complexity for learning environment

**What Gets Transformed:**
- Database driver imports (pyodbc → psycopg2)
- Connection strings (MSSQL format → PostgreSQL format)
- Query syntax (T-SQL → PostgreSQL)
- SQL functions (GETDATE() → NOW(), ISNULL() → COALESCE(), etc.)
- Parameter placeholders (? → %s)

**Real-World Application:**
After the workshop, apply the same transformation to production codebases with actual database connections.

---

## Key Learning Objectives

1. ✅ Understand AWS Transform Custom capabilities and workflow
2. ✅ Create and publish custom transformation definitions
3. ✅ Execute transformations with interactive feedback
4. ✅ Validate migrated applications against target platform
5. ✅ Leverage continual learning for quality improvement

## What Participants Will Accomplish

- Migrate 39 API endpoints from MSSQL to PostgreSQL
- Transform ~28 Python files with 150+ SQL queries
- Achieve 100% test pass rate post-migration
- Create reusable transformation definition
- Build knowledge items for future migrations

## Prerequisites Checklist

**AWS Resources:**
- [ ] AWS account with Transform Custom access
- [ ] IAM permissions configured
- [ ] AWS CLI installed and configured

**Local Environment:**
- [ ] Python 3.11+ installed
- [ ] AWS Transform Custom CLI installed
- [ ] Repository cloned
- [ ] Virtual environment created

**Note:** No database provisioning required - workshop uses mock database layer.

## Key Commands

```bash
# Publish transformation
atx custom def publish -n mssql-to-aurora-postgres \
    --description "Migrate Flask from MSSQL to Aurora PostgreSQL" \
    --sd docs/

# Execute transformation (interactive)
atx custom def exec -n mssql-to-aurora-postgres -p .

# List knowledge items
atx custom def list-ki -n mssql-to-aurora-postgres

# Test application
python validate_api.py
```

## Success Metrics

- All 39 endpoints functional with transformed PostgreSQL code
- 100% test coverage maintained (using mock database)
- Zero manual code changes required
- Knowledge items captured for future use
- Code ready for real PostgreSQL database connection
- Estimated 40-60 hours of manual effort saved

## Files Included

1. **WORKSHOP_GUIDE.md** - Complete detailed guide (main document)
2. **docs/transformation_definition.md** - Transformation logic (already exists)
3. **WORKSHOP_SUMMARY.md** - This quick reference

## Next Steps After Workshop

1. Apply to production codebase
2. Optimize PostgreSQL performance
3. Share transformation with team
4. Build transformation library
5. Integrate with CI/CD pipelines

---

**For Questions:** Contact workshop facilitator or AWS support
