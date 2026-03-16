---
globs: backend/alembic/**
---

# Migration Safety Rules

- Never modify an existing migration file — always create a new one
- Create migrations with: `cd backend && alembic revision --autogenerate -m "description"`
- Apply with: `cd backend && alembic upgrade head`
- The sync DB URL uses `postgresql://` (not `postgresql+asyncpg://`) — Alembic needs sync
- Add new columns as nullable first. Populate data, then add NOT NULL constraints in a separate migration if needed.
- Migration numbering: use `NNN_` prefix matching the sequence (current: 020)
- Always test migration against a fresh database: `docker compose down -v && docker compose up -d db backend`
