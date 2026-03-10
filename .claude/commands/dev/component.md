# Scaffold React Component

Create a new React component for the Icarus frontend following project conventions.

## Arguments
$ARGUMENTS = component name and description

## Steps

1. Parse: "$ARGUMENTS" — extract component name and purpose
2. Read existing components in `frontend/src/components/` to match patterns
3. Read `frontend/src/lib/utils.ts` for available helpers (cn, formatDate, etc.)
4. Read `frontend/src/lib/types.ts` for existing TypeScript types

## Component Creation

Create the component file at the appropriate location:
- Shared components → `frontend/src/components/ComponentName.tsx`
- Feature-specific → `frontend/src/components/feature/ComponentName.tsx`
- Page-level → `frontend/src/app/route/page.tsx`

### Template Rules
- Use TypeScript with explicit prop interfaces
- Use `cn()` from `@/lib/utils` for conditional classes
- Default to server components — add `'use client'` only if the component uses:
  - `useState`, `useEffect`, `useRef`, or other hooks
  - Event handlers (onClick, onChange, etc.)
  - Browser APIs
- Follow existing Tailwind patterns (check 2-3 similar components)
- Include proper accessibility attributes (aria-labels, roles, semantic HTML)
- Use `fetchApi<T>()` from `@/lib/api` for data fetching

### Naming Conventions
- PascalCase for component files and exports
- camelCase for props and functions
- kebab-case for CSS class names (when needed)

## Verification
- Check TypeScript compiles: `cd frontend && npx tsc --noEmit`
- Verify component renders correctly if a dev server is available

Report what was created and any integration points.
