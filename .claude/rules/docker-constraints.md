---
globs: docker-compose*, backend/Dockerfile, frontend/Dockerfile
---

# Docker & Infrastructure Constraints

- Backend MUST run in Docker — local Python is 3.14, but pydantic-core requires <=3.13
- Frontend should NOT run in Docker for local dev — use `npm run dev` directly for hot reload
- Docker frontend requires full rebuild on every code change (no HMR)
- Backend Docker image uses Python 3.12-slim with multi-stage build
- Frontend Docker image uses Node 20-alpine with multi-stage build
- Production compose (`docker-compose.prod.yml`) sets AUTH_ENABLED=true and memory limits
