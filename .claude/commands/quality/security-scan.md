# Security Scan

Perform a security audit of the Icarus application.

## Scan Scope

Audit both frontend and backend for OWASP Top 10 and common vulnerabilities.

## Backend Checks

### Authentication & Authorization
- Check all endpoints have proper auth guards
- Verify no endpoints are accidentally public
- Check for hardcoded credentials or API keys
- Scan for secrets in code: `grep -rn "password\|secret\|api_key\|token" backend/ --include="*.py" | grep -v "__pycache__" | grep -v ".pyc"`

### Injection
- SQL injection: search for raw SQL, string formatting in queries
- Command injection: search for `os.system`, `subprocess` with user input
- Template injection: search for unsafe string formatting in responses

### Data Exposure
- Check API responses don't leak sensitive fields
- Verify error messages don't expose internal details
- Check logging doesn't include sensitive data

### Dependencies
- Check for known vulnerabilities: `cd backend && pip audit` (if pip-audit installed)
- Review requirements.txt for outdated packages

## Frontend Checks

### XSS
- Search for `dangerouslySetInnerHTML`
- Check that user input is properly escaped
- Verify Content-Security-Policy headers

### Data Handling
- Check no secrets in client-side code
- Verify API keys aren't exposed in frontend bundle
- Check `.env` files aren't committed

### Dependencies
- Check for known vulnerabilities: `cd frontend && npm audit`

## Configuration Checks

- CORS configuration (is it too permissive?)
- Check for debug mode in production configs
- Verify `.gitignore` includes `.env`, `*.pem`, `*.key`
- Check Docker configs don't run as root

## Report

For each finding:
```
[SEVERITY] Category — Location
Description
Remediation steps
```

Summary: total findings by severity, risk score (1-10), top 3 priority fixes.
