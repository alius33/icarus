# Full-Stack Feature Development

You are building a feature for the Icarus app (Next.js 14 + FastAPI + PostgreSQL). Follow this structured workflow.

## Arguments
$ARGUMENTS = feature description

## Phase 1: Requirements Analysis

1. Parse the feature description: "$ARGUMENTS"
2. Read the project CLAUDE.md for architecture context
3. Identify which layers are affected:
   - **Database** — new models, schema changes, migrations?
   - **Backend** — new/modified API endpoints, services, schemas?
   - **Frontend** — new pages, components, API client updates?
4. Create a brief implementation plan (max 10 bullet points)

## Phase 2: Backend First (if applicable)

### 2a. Database Layer
- Create/modify SQLAlchemy models in `backend/app/models/`
- Create Alembic migration: `cd backend && alembic revision --autogenerate -m "description"`
- Add Pydantic schemas in `backend/app/schemas/`

### 2b. API Layer
- Create/modify router in `backend/app/routers/`
- Register router in `backend/app/main.py` if new
- Add service logic in `backend/app/services/` if complex
- Follow existing patterns — check similar routers first

### 2c. Backend Tests
- Write tests in `backend/tests/` following existing patterns
- Run: `cd backend && python -m pytest tests/ -v`

## Phase 3: Frontend (if applicable)

### 3a. API Client
- Add endpoint functions to `frontend/src/lib/api.ts`
- Add TypeScript types to `frontend/src/lib/types.ts`

### 3b. UI Components
- Create components in `frontend/src/components/`
- Follow existing patterns (check similar components first)
- Use Tailwind CSS classes consistent with existing design
- Ensure responsive design (test mobile/desktop)

### 3c. Pages/Routes
- Add pages in `frontend/src/app/` following App Router conventions
- Use server components by default, client components only when needed
- Wire up to the API client

## Phase 4: Integration Test
- Run full build: `cd frontend && npm run build`
- Run backend: verify no import errors
- Test the feature end-to-end

## Phase 5: Cleanup
- Remove any debug code
- Ensure no TODO comments left unresolved
- Run linters if configured

Report what was built, files created/modified, and any follow-up items.
