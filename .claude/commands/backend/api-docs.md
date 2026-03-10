# Generate API Documentation

Generate comprehensive API documentation for the Icarus backend.

## Steps

1. Read all routers in `backend/app/routers/`
2. Read all schemas in `backend/app/schemas/`
3. Read `backend/app/main.py` for app configuration

## Output Format

Generate documentation covering:

### Endpoint Reference
For each endpoint:
- **Method & Path**: `GET /api/projects`
- **Description**: What it does
- **Parameters**: Query params, path params
- **Request Body**: Schema with example
- **Response**: Schema with example
- **Status Codes**: 200, 400, 404, 500 etc.

### Authentication
- Current auth mechanism (if any)
- Which endpoints require auth

### Data Models
- All Pydantic schemas with field descriptions
- Relationships between models

### Quick Start
- How to run the backend
- Base URL configuration
- Example curl commands for common operations

## Verify
- Check that FastAPI's auto-generated docs are accessible at `/docs` and `/redoc`
- Verify all endpoints have proper `response_model` annotations
- Check that schema examples are realistic

Write output to `docs/api-reference.md` (or update if exists).
