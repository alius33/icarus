# Database Migration

Create and manage Alembic migrations for the Icarus PostgreSQL database.

## Arguments
$ARGUMENTS = migration description (e.g. "add reports table" or "run pending migrations")

## Operations

### Create a New Migration
1. Parse: "$ARGUMENTS"
2. Read existing models in `backend/app/models/` to understand current schema
3. If adding a new model:
   - Create the SQLAlchemy model in `backend/app/models/`
   - Register it in `backend/app/models/__init__.py`
4. Generate migration:
   ```bash
   cd backend && alembic revision --autogenerate -m "$ARGUMENTS"
   ```
5. Read the generated migration file and verify:
   - Correct table names
   - Correct column types and constraints
   - Foreign keys and indexes look right
   - `downgrade()` function properly reverses the `upgrade()`
6. Review for data safety:
   - Column drops should be confirmed with user
   - NOT NULL additions need default values or data migration
   - Index changes on large tables may lock

### Run Pending Migrations
```bash
cd backend && alembic upgrade head
```

### Check Migration Status
```bash
cd backend && alembic current
cd backend && alembic history --verbose
```

### Rollback Last Migration
```bash
cd backend && alembic downgrade -1
```

## Safety Rules
- NEVER drop columns without explicit user confirmation
- ALWAYS include a working downgrade function
- NEVER modify existing migrations that have been applied
- Check for data loss risks before running destructive migrations

Report: migration file created, what it does, any manual steps needed.
