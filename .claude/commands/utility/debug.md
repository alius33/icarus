# Systematic Debugging

Debug an issue in the Icarus application using a structured 4-phase approach.

## Arguments
$ARGUMENTS = description of the bug or error

## Phase 1: Reproduce
1. Parse: "$ARGUMENTS"
2. Identify the layer (frontend, backend, database, import pipeline)
3. Find the relevant code files
4. Attempt to reproduce:
   - Backend: run the endpoint, check logs
   - Frontend: check console errors, network tab
   - Import: run import script, check output
5. Capture the exact error message and stack trace

## Phase 2: Isolate
1. Narrow down to the specific file and function
2. Trace the data flow:
   - What input triggers the bug?
   - Where does the data transform incorrectly?
   - What's the expected vs. actual behavior?
3. Check recent changes: `git log --oneline -10 -- <file>`
4. Read related code to understand dependencies

## Phase 3: Fix
1. Identify the root cause (not just the symptom)
2. Write a test that reproduces the bug (RED)
3. Apply the minimal fix
4. Run the test (GREEN)
5. Verify no regressions:
   - Run all related tests
   - Check TypeScript compiles (frontend)
   - Check imports work (backend)

## Phase 4: Verify
1. Reproduce the original scenario — bug should be gone
2. Check edge cases related to the fix
3. Review the fix for unintended side effects
4. Document: what was wrong, why, and how it was fixed

## Output
- Root cause identified
- Fix applied (file:line)
- Tests added/updated
- Verification results
