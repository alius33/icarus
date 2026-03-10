# Developer Onboarding

Set up a new development environment for the Icarus project.

## Steps

### 1. Prerequisites Check
```bash
node --version    # Need 18+
python --version  # Need 3.11+
git --version
```

### 2. Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local  # if exists
```

Verify: `npm run build` should succeed.

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env  # if exists
```

Verify: `python -c "from app.main import app; print('OK')"` should succeed.

### 4. Database Setup
- Ensure PostgreSQL is running
- Create database: `createdb icarus`
- Set `DATABASE_URL` environment variable
- Run migrations: `cd backend && alembic upgrade head`
- Import data: `cd backend && python -m scripts.import_data --data-root ..`

### 5. Run Development Servers
- Backend: `cd backend && uvicorn app.main:app --reload --port 8000`
- Frontend: `cd frontend && npm run dev`
- Open: http://localhost:3000

### 6. Project Orientation
Key files to read first:
- `CLAUDE.md` — project architecture and conventions
- `context/glossary.md` — domain terminology
- `frontend/src/lib/api.ts` — all API endpoints
- `frontend/src/lib/types.ts` — all TypeScript types
- `backend/app/main.py` — backend entry point
- `backend/app/routers/` — all API routes

## Output
Report setup status, any issues encountered, and next steps.
