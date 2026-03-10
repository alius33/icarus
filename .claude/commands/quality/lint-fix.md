# Lint and Fix

Run all linters and auto-fix issues across the Icarus codebase.

## Frontend

1. Check if ESLint is configured: look for `.eslintrc*` or `eslint.config.*`
2. Run linter: `cd frontend && npx next lint`
3. Auto-fix what's possible: `cd frontend && npx next lint --fix`
4. Check TypeScript: `cd frontend && npx tsc --noEmit`
5. Fix any type errors found
6. Check for unused imports and exports

## Backend

1. Check if ruff/flake8/pylint is configured
2. Run available linter:
   - `cd backend && python -m ruff check .` (preferred)
   - `cd backend && python -m flake8 .` (fallback)
3. Auto-fix: `cd backend && python -m ruff check . --fix` (if ruff)
4. Check type annotations: `cd backend && python -m mypy app/` (if mypy installed)
5. Sort imports: `cd backend && python -m isort . --check-only`

## General

1. Check for trailing whitespace in all files
2. Check for consistent line endings
3. Verify no merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
4. Check for debugger statements (`console.log`, `print()`, `breakpoint()`, `debugger`)

## Report

- Issues found by category
- Issues auto-fixed
- Issues requiring manual fix (with file:line and description)
- Clean bill of health or remaining items
