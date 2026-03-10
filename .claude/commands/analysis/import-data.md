# Import Data to Database

Trigger the backend import pipeline to sync markdown files into PostgreSQL.

## Steps

1. Check if DATABASE_URL is set: `echo $DATABASE_URL`
2. Check if the backend is running: `curl -s http://localhost:8000/api/dashboard | head -c 100`

### If backend is running:
```bash
curl -X POST http://localhost:8000/api/import/trigger
```

### If backend is not running but DATABASE_URL is set:
```bash
cd backend && python -m scripts.import_data --data-root .. --db-url "$DATABASE_URL"
```

### If neither:
Tell the user to set DATABASE_URL or start the backend first.

## Post-Import Verification
- Check record counts: `curl -s http://localhost:8000/api/dashboard`
- Verify latest data appears: check most recent transcript/summary dates
- Report any import errors from logs

## Output
- Records imported by entity type
- Any errors or warnings
- Verification results
