# React Best Practices Audit

Audit the Icarus frontend React code for best practices and common anti-patterns.

## Checks

### Component Architecture
- Are components small and focused (single responsibility)?
- Is state lifted to the lowest common ancestor?
- Are render props or composition used instead of deep prop drilling?
- Do components have clear prop interfaces with TypeScript?

### State Management
- Is `useState` used for simple local state?
- Are derived values computed (not stored in state)?
- Is `useReducer` used for complex state logic?
- Are side effects properly contained in `useEffect`?

### Performance Patterns
- Are expensive computations wrapped in `useMemo`?
- Are callback functions wrapped in `useCallback` when passed as props?
- Are list items using stable, unique `key` props (not index)?
- Are large lists virtualized if >100 items?
- Is `React.memo` used for pure components that re-render often?
- Are lazy imports used for route-level code splitting?

### Hook Rules
- Are hooks called at the top level (not in conditions/loops)?
- Are custom hooks prefixed with `use`?
- Do `useEffect` dependencies include all referenced values?
- Are cleanup functions returned from effects that set up subscriptions?

### Anti-Patterns to Flag
- `useEffect` for derived state (should be computed during render)
- `useEffect` for event handling (should be in event handler)
- State synchronization between components (should lift state)
- `any` type usage (should be properly typed)
- Inline object/array creation in JSX props (causes re-renders)
- `console.log` left in production code

### Error Handling
- Are error boundaries in place for critical sections?
- Do async operations have try/catch with user-facing error messages?
- Are loading/error/empty states handled for all data fetching?

## Output
Categorize findings by: Bugs, Performance, Maintainability, Style.
Include code examples for each fix.
