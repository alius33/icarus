# Code Review

Perform a thorough multi-perspective code review.

## Arguments
$ARGUMENTS = file path(s) or "recent changes" to review git diff

## Perspectives

Review from these 5 angles:

### 1. Correctness
- Does the code do what it claims to?
- Are there logic errors, off-by-one errors, race conditions?
- Are edge cases handled (null, empty, boundary values)?
- Do error paths work correctly?

### 2. Security
- SQL injection risks (raw queries, string interpolation)?
- XSS vectors (unescaped user input in HTML)?
- Authentication/authorization gaps?
- Sensitive data exposure (secrets in code, logs, responses)?
- Path traversal vulnerabilities?
- CORS misconfigurations?

### 3. Performance
- N+1 query patterns?
- Missing database indexes for common queries?
- Unnecessary re-renders in React components?
- Large bundle imports that could be lazy-loaded?
- Unbounded data fetching (missing pagination/limits)?

### 4. Maintainability
- Files over 500 lines?
- Functions over 50 lines?
- Unclear naming?
- Missing type annotations?
- Dead code or unused imports?
- Duplicated logic that should be extracted?

### 5. Architecture
- Does it follow existing project patterns?
- Is the responsibility in the right layer (model/service/router/component)?
- Are dependencies flowing in the right direction?
- Will this be easy to test?

## Output Format

For each issue found:
```
[SEVERITY] Category — file:line
Description of the issue
Suggested fix (if applicable)
```

Severities: CRITICAL (must fix), HIGH (should fix), MEDIUM (nice to fix), LOW (nitpick)

End with a summary: total issues by severity, overall assessment, top 3 priorities.
