# Database Seed Data

Manage seed data for the Icarus database.

## Arguments
$ARGUMENTS = "generate" | "import" | "reset"

## Operations

### Generate Seed Data
Create realistic test data for development:
1. Read all models in `backend/app/models/`
2. Generate seed data that:
   - Covers all entity types (transcripts, summaries, weekly reports, etc.)
   - Includes relationships between entities
   - Uses realistic names, dates, and content
   - Creates enough data to test pagination (20+ records per type)
3. Write seed script to `backend/scripts/seed_data.py`

### Import from Markdown
Trigger the standard Icarus import pipeline:
```bash
cd backend && python -m scripts.import_data --data-root .. --db-url "$DATABASE_URL"
```
This reads all markdown files from the project root and imports them into PostgreSQL.

### Reset Database
1. Drop all tables: `cd backend && alembic downgrade base`
2. Recreate: `cd backend && alembic upgrade head`
3. Re-import data: `cd backend && python -m scripts.import_data --data-root ..`

## Safety
- Reset requires explicit user confirmation
- Always verify DATABASE_URL is set before operations
- Never seed production databases

Report: what was done, record counts by entity type, any errors.
