# Deployment Checklist

Run a pre-deployment verification for the Icarus application.

## Pre-Flight Checks

### Code Quality
- [ ] All tests pass: `cd backend && python -m pytest` + `cd frontend && npm test`
- [ ] TypeScript compiles: `cd frontend && npx tsc --noEmit`
- [ ] No lint errors: `cd frontend && npx next lint`
- [ ] No debug code (console.log, print, debugger, breakpoint)
- [ ] No TODO/FIXME comments in critical paths

### Security
- [ ] No hardcoded secrets in source code
- [ ] `.env` files in `.gitignore`
- [ ] CORS configured for production domains only
- [ ] Debug mode OFF in production config
- [ ] Dependencies audited: `npm audit` + `pip audit`

### Database
- [ ] All migrations applied: `alembic current` matches `alembic heads`
- [ ] No pending migration conflicts
- [ ] Seed/import data verified

### Build
- [ ] Frontend builds successfully: `cd frontend && npm run build`
- [ ] Backend starts without errors: `cd backend && python -c "from app.main import app"`
- [ ] Docker images build (if applicable)

### Configuration
- [ ] Environment variables documented
- [ ] `INTERNAL_API_URL` configured for production
- [ ] `NEXT_PUBLIC_API_URL` configured for production
- [ ] `DATABASE_URL` configured for production
- [ ] CORS origins updated for production

### Performance
- [ ] Frontend bundle size reasonable
- [ ] Database queries optimized (no N+1)
- [ ] Static assets optimized

## Output
Pass/fail for each check with details on failures.
