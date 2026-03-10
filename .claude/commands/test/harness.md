# Generate Test Suite

Generate a comprehensive test suite for existing code.

## Arguments
$ARGUMENTS = file path or module to test

## Steps

1. Read the target file/module: "$ARGUMENTS"
2. Identify all public functions, classes, methods, and endpoints
3. Read existing tests (if any) to avoid duplication
4. Determine the testing framework:
   - Python (backend): pytest with async support
   - TypeScript (frontend): Jest or Vitest (check package.json)

## Test Categories

Generate tests in this order:

### Unit Tests
- Each public function/method gets at least 3 tests:
  - Normal input → expected output
  - Edge case → correct handling
  - Invalid input → proper error

### Integration Tests (if applicable)
- API endpoints: test request → response cycle
- Database operations: test CRUD with test fixtures
- Service layer: test business logic with mocked dependencies

### Regression Tests
- If fixing a bug, add a test that would have caught it

## Test Patterns

### Backend (pytest)
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_endpoint_returns_data(client: AsyncClient):
    response = await client.get("/api/endpoint")
    assert response.status_code == 200
    data = response.json()
    assert "key" in data
```

### Frontend (Jest/Vitest)
```typescript
import { render, screen } from '@testing-library/react'
import { ComponentName } from './ComponentName'

describe('ComponentName', () => {
  it('renders correctly', () => {
    render(<ComponentName prop="value" />)
    expect(screen.getByText('expected')).toBeInTheDocument()
  })
})
```

## Verification
- Run the generated tests
- All tests must PASS
- Report coverage gaps if possible

Report: number of tests generated, pass/fail results, files created.
