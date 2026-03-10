# Search Codebase

Search the Icarus codebase for patterns, usages, or definitions.

## Arguments
$ARGUMENTS = what to search for

## Steps

1. Parse: "$ARGUMENTS" — determine search type:
   - **Definition**: looking for where something is defined (class, function, component)
   - **Usage**: looking for where something is used (imports, calls, references)
   - **Pattern**: looking for a code pattern (e.g. "all API endpoints", "all useState hooks")

2. Search strategy:
   - Use Grep for text patterns
   - Use Glob for file patterns
   - Search both `frontend/src/` and `backend/app/`

3. Present results grouped by:
   - File path
   - Line numbers
   - Context (3 lines around each match)

## Common Searches

- "Find all API endpoints" → grep for `@app.get\|@app.post\|@router.get\|@router.post` in backend
- "Find all components" → glob for `frontend/src/components/**/*.tsx`
- "Find all types" → grep for `interface\|type ` in `frontend/src/lib/types.ts`
- "Find all usages of X" → grep for the term across both frontend and backend
- "Find all TODO comments" → grep for `TODO\|FIXME\|HACK\|XXX`

## Output
Results with file paths, line numbers, and surrounding context.
Total matches found.
