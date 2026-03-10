# Safe Code Refactoring

Refactor code in the Icarus project with safety checks at every step.

## Arguments
$ARGUMENTS = what to refactor and why

## Phase 1: Understand

1. Parse: "$ARGUMENTS"
2. Read ALL files involved in the refactoring
3. Identify:
   - All call sites and dependencies
   - All imports that reference the target
   - Test files that cover this code
   - Any public API contracts that would break
4. Map the blast radius — list every file that will need changes

## Phase 2: Plan

Create a refactoring plan:
- What changes, in what order
- What breaks if we stop halfway (nothing should)
- What tests need updating
- Any temporary compatibility shims needed

## Phase 3: Execute

Apply changes in this order:
1. **Tests first** — update tests to expect new behavior (RED)
2. **Implementation** — make the actual changes
3. **Call sites** — update all references
4. **Cleanup** — remove dead code, unused imports

### Safety Rules
- NEVER rename without updating ALL references
- NEVER delete code without confirming it's unused (grep for it)
- NEVER change function signatures without updating all callers
- Keep each change small and atomic
- If a file exceeds 500 lines after refactoring, split it

## Phase 4: Verify

- Run TypeScript check: `cd frontend && npx tsc --noEmit` (if frontend)
- Run Python import check: `cd backend && python -c "from app.main import app"` (if backend)
- Run tests if available
- Grep for any remaining references to old names/patterns

Report: what was refactored, files changed, any remaining follow-ups.
