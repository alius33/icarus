# Test-Driven Development Cycle

Run a TDD cycle (RED → GREEN → REFACTOR) for new functionality.

## Arguments
$ARGUMENTS = what to implement

## RED Phase — Write Failing Tests

1. Parse: "$ARGUMENTS"
2. Determine test location:
   - Frontend: `frontend/src/__tests__/` or co-located `*.test.tsx`
   - Backend: `backend/tests/`
3. Read existing tests to match style and conventions
4. Write tests that describe the desired behavior:
   - Happy path (expected inputs → expected outputs)
   - Edge cases (empty, null, boundary values)
   - Error cases (invalid input, missing data)
5. Run tests — confirm they FAIL: `cd backend && python -m pytest tests/ -v` or `cd frontend && npm test`

## GREEN Phase — Minimal Implementation

1. Write the MINIMUM code to make tests pass
2. Don't optimise, don't refactor — just make it work
3. Run tests — confirm they PASS
4. If any test still fails, fix the implementation (not the test)

## REFACTOR Phase — Clean Up

1. Review the implementation for:
   - Duplicated code
   - Unclear naming
   - Overly complex logic
   - Missing type annotations
2. Refactor while keeping tests green
3. Run tests after EACH refactoring step
4. Stop when the code is clean and all tests pass

## Report
- Tests written (count and descriptions)
- Implementation files created/modified
- Final test results (all green)
- Any concerns or follow-ups
