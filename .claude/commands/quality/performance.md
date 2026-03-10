# Performance Audit

Audit the Icarus application for performance issues across all layers.

## Backend Performance

### Database Queries
- Read all routers and services for database queries
- Identify N+1 query patterns (loading relations in loops)
- Check for missing indexes on frequently queried columns
- Look for `SELECT *` where specific columns would suffice
- Check for unbounded queries (missing LIMIT/pagination)
- Verify eager loading is used for known relation access patterns

### API Response Times
- Check for synchronous blocking operations in async handlers
- Identify endpoints that could benefit from caching
- Look for unnecessary serialization overhead
- Check for redundant database calls in single requests

### Memory
- Check for large data structures held in memory
- Look for file operations without streaming
- Verify database connections are properly pooled and released

## Frontend Performance

### Bundle Size
- Check for large imports that could be tree-shaken
- Look for client-side libraries that could be replaced with lighter alternatives
- Identify components that should be lazy-loaded
- Check for duplicate dependencies

### Rendering
- Identify unnecessary re-renders (missing useMemo, useCallback)
- Check for expensive computations in render paths
- Look for missing React.memo on pure components
- Verify lists have proper `key` props

### Data Fetching
- Check for waterfall request patterns (sequential when parallel is possible)
- Verify server components are used where possible (no unnecessary client-side fetching)
- Look for missing loading states and suspense boundaries
- Check for redundant API calls

### Assets
- Check image optimization (proper formats, sizes, lazy loading)
- Verify fonts are preloaded or using `next/font`
- Check for render-blocking resources

## Report

Group findings by impact (HIGH/MEDIUM/LOW) and effort (EASY/MODERATE/HARD).
Prioritize: High Impact + Easy Effort first.
Include before/after expectations where possible.
