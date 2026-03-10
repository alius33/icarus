# Dependency Check

Audit dependencies for the Icarus project — check for outdated packages, security issues, and unused deps.

## Frontend (npm)

```bash
cd frontend && npm outdated
cd frontend && npm audit
```

Check for unused dependencies:
- Read `package.json` dependencies
- Grep the codebase for each package name
- Flag any that appear unused

## Backend (pip)

```bash
cd backend && pip list --outdated
cd backend && pip audit  # if pip-audit installed
```

Check for unused dependencies:
- Read `requirements.txt`
- Grep backend code for each import
- Flag any that appear unused

## Report

### Outdated Packages
| Package | Current | Latest | Breaking? |
|---------|---------|--------|-----------|
| ... | ... | ... | Yes/No |

### Security Vulnerabilities
| Package | Severity | CVE | Fix |
|---------|----------|-----|-----|
| ... | ... | ... | Upgrade to X |

### Unused Dependencies
| Package | Installed In | Last Used |
|---------|-------------|-----------|
| ... | frontend/backend | Never found |

### Recommendations
- Priority upgrades (security fixes)
- Safe upgrades (patch versions)
- Major upgrades requiring migration
- Dependencies to remove
