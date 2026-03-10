# End-to-End Test

Run end-to-end verification of a feature across the full stack.

## Arguments
$ARGUMENTS = feature or user flow to test

## Steps

1. Parse: "$ARGUMENTS" — identify the user flow to test
2. Map the flow across layers:
   - Frontend: which pages/components are involved?
   - API: which endpoints are called?
   - Database: which tables are read/written?

## Backend Verification

1. Check the API endpoint responds correctly:
   ```bash
   cd backend && python -c "
   import asyncio
   from httpx import AsyncClient
   from app.main import app
   # Test endpoint
   "
   ```
2. Verify database state is correct after operations

## Frontend Verification

1. Check pages render without errors:
   ```bash
   cd frontend && npx tsc --noEmit
   ```
2. Check build succeeds: `cd frontend && npm run build`
3. If preview server is running, use preview tools to verify:
   - Page loads correctly
   - Data displays properly
   - Interactive elements work
   - No console errors

## Cross-Layer Checks

- API response shapes match frontend TypeScript types
- Error states are handled gracefully (404, 500, network errors)
- Loading states exist for async operations
- Empty states exist for zero-data scenarios

## Report
- Flow tested (step by step)
- Pass/fail at each layer
- Any issues found with reproduction steps
- Suggested fixes for failures
