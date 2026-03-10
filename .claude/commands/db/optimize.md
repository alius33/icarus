# Database Query Optimization

Analyse and optimize database queries in the Icarus backend.

## Steps

### 1. Identify Slow Queries
- Read all routers and services in `backend/app/routers/` and `backend/app/services/`
- Look for these anti-patterns:
  - **N+1 queries**: Loading relations in loops instead of eager loading
  - **SELECT ***: Fetching all columns when only a few are needed
  - **Missing indexes**: Columns used in WHERE/JOIN/ORDER BY without indexes
  - **Unbounded queries**: Missing LIMIT on list endpoints
  - **Redundant queries**: Same data fetched multiple times per request
  - **Unoptimized JOINs**: Cartesian products, unnecessary joins

### 2. Analyze Schema
- Read all models in `backend/app/models/`
- Check for:
  - Missing indexes on foreign keys
  - Missing composite indexes for common query patterns
  - Inefficient column types (e.g. TEXT where VARCHAR would do)
  - Missing relationship configurations (lazy vs eager loading)

### 3. Generate Fixes
For each issue found:
- Explain the problem and its impact
- Provide the optimized code
- If new indexes needed, create an Alembic migration

### 4. Optimization Patterns for SQLAlchemy 2.0

```python
# Eager loading (avoid N+1)
stmt = select(Parent).options(selectinload(Parent.children))

# Specific columns (avoid SELECT *)
stmt = select(Model.id, Model.name).where(...)

# Pagination
stmt = select(Model).offset(skip).limit(limit)

# Efficient counting
stmt = select(func.count()).select_from(Model)
```

## Report

| Query | Location | Issue | Fix | Impact |
|-------|----------|-------|-----|--------|
| ... | file:line | N+1 | selectinload | HIGH |

Summary: total issues found, estimated performance improvement, migrations needed.
