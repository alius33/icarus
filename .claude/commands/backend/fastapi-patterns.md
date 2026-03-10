# FastAPI Best Practices Audit

Audit the Icarus backend for FastAPI + SQLAlchemy 2.0 + Pydantic V2 best practices.

## Checks

### Async Patterns
- All route handlers should be `async def` (not `def`)
- Database operations should use `AsyncSession`
- File I/O should use `aiofiles` or run in executor
- No blocking calls (`time.sleep`, synchronous HTTP) in async handlers

### Dependency Injection
- Database sessions via `Depends(get_db)`
- Shared logic extracted to dependencies
- No global mutable state

### Error Handling
- Custom exception handlers for common errors
- Proper HTTP status codes (not just 200/500)
- Structured error responses with detail messages
- No stack traces leaked in production responses

### Pydantic V2
- Using `model_config` instead of inner `Config` class
- Field validators using `@field_validator`
- Proper `model_dump()` instead of `.dict()`
- Response models on all endpoints

### SQLAlchemy 2.0
- Using `select()` statements (not legacy `session.query()`)
- Proper relationship loading strategies
- Session management via context managers
- No raw SQL without parameterization

### Security
- Input validation on all endpoints
- Proper CORS configuration
- Rate limiting considerations
- Authentication on protected endpoints

### API Design
- Consistent naming (plural nouns for collections)
- Proper HTTP methods (GET/POST/PATCH/DELETE)
- Pagination on list endpoints
- Filtering and sorting support

## Output
List findings with severity and code fixes.
