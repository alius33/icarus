# Tech Debt Assessment

Scan the Icarus codebase for technical debt and create a prioritised remediation plan.

## Scan Areas

### Code Smells
- Files over 500 lines
- Functions over 50 lines
- Deeply nested logic (>3 levels)
- Duplicated code blocks (>10 lines appearing 2+ times)
- TODO/FIXME/HACK comments
- Disabled tests or skipped checks
- Any `# type: ignore` or `// @ts-ignore` annotations

### Architecture Debt
- Circular dependencies between modules
- Business logic in the wrong layer (routes doing DB queries directly, etc.)
- Missing abstractions (copy-pasted patterns)
- Over-abstractions (unused indirection)
- Inconsistent patterns across similar files

### Dependency Debt
- Outdated packages (check `npm outdated` and `pip list --outdated`)
- Deprecated APIs being used
- Multiple libraries solving the same problem
- Pinned versions that should be updated

### Testing Debt
- Untested critical paths
- Tests that test implementation details instead of behavior
- Missing error scenario tests
- Flaky or slow tests

### Documentation Debt
- Public APIs without documentation
- Outdated comments that don't match code
- Missing type annotations

## Output

Create a debt register:

| # | Category | Location | Description | Severity | Effort | Priority |
|---|----------|----------|-------------|----------|--------|----------|
| 1 | ... | file:line | ... | HIGH | EASY | P1 |

Priority scoring:
- P1: High severity + Easy effort (do now)
- P2: High severity + Hard effort (plan for)
- P3: Low severity + Easy effort (do when nearby)
- P4: Low severity + Hard effort (backlog)

End with: total debt items, estimated effort to clear P1s, recommended sprint plan.
