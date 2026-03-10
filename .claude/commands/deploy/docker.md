# Docker Configuration

Create or optimize Docker configuration for the Icarus application.

## Arguments
$ARGUMENTS = "create" | "optimize" | "audit"

## Architecture
The Icarus app has three services:
- **frontend**: Next.js 14 on port 3000
- **backend**: FastAPI on port 8000
- **db**: PostgreSQL on port 5432

## Create Docker Setup

### docker-compose.yml
```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: icarus
      POSTGRES_USER: icarus
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U icarus"]
      interval: 5s
      timeout: 3s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql+asyncpg://icarus:${DB_PASSWORD}@db:5432/icarus
      DATA_ROOT: /data
    volumes:
      - ./Transcripts:/data/Transcripts:ro
      - ./analysis:/data/analysis:ro
      - ./context:/data/context:ro
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      INTERNAL_API_URL: http://backend:8000
      NEXT_PUBLIC_API_URL: http://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  pgdata:
```

### Optimization Checklist
- Multi-stage builds (separate build and runtime stages)
- Alpine base images where possible
- `.dockerignore` for node_modules, __pycache__, .git
- Non-root user in containers
- Health checks on all services
- Proper signal handling (SIGTERM)
- Layer caching optimized (COPY package.json first, then install, then copy source)

## Output
Files created/modified, build verification, any issues found.
