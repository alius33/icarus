# Scaffold FastAPI Endpoint

Create a new API endpoint for the Icarus backend following project conventions.

## Arguments
$ARGUMENTS = endpoint description (e.g. "GET /api/reports — list all generated reports")

## Steps

1. Parse: "$ARGUMENTS" — extract HTTP method, path, and purpose
2. Read existing routers in `backend/app/routers/` to match patterns
3. Read `backend/app/main.py` to understand router registration
4. Read `backend/app/database.py` for session management patterns
5. Check `backend/app/models/` and `backend/app/schemas/` for existing types

## Endpoint Creation

### Model (if new entity)
Create SQLAlchemy model in `backend/app/models/`:
- Use `Base` from `backend/app/database.py`
- Include `id`, `created_at`, `updated_at` fields
- Add relationships where appropriate
- Register in `backend/app/models/__init__.py`

### Schema (Pydantic)
Create request/response schemas in `backend/app/schemas/`:
- `EntityCreate` — for POST body
- `EntityUpdate` — for PATCH body (all fields optional)
- `EntityResponse` — for API responses
- `EntityListResponse` — for list endpoints (with pagination if needed)

### Router
Create/modify router in `backend/app/routers/`:
- Use `APIRouter(prefix="/api/entity", tags=["entity"])`
- Follow async patterns: `async def endpoint(db: AsyncSession = Depends(get_db))`
- Include proper status codes and error handling
- Add response_model annotations

### Registration
- Add router to `backend/app/main.py`: `app.include_router(entity_router)`

### Migration (if new model)
```bash
cd backend && alembic revision --autogenerate -m "add entity table"
```

## Testing
- Test endpoint manually or write a test in `backend/tests/`
- Verify: `cd backend && python -c "from app.main import app; print('OK')"`

Report: endpoint path, method, request/response shapes, files created.
