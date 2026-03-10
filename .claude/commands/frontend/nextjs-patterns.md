# Next.js Best Practices Check

Audit the Icarus frontend for Next.js 14 App Router best practices.

## Checks

### Server vs Client Components
- Scan all `.tsx` files in `frontend/src/`
- Flag client components (`'use client'`) that could be server components:
  - Components that only render data (no hooks, no event handlers)
  - Components that fetch data on the client but could use server components
- Flag server components that should be client components:
  - Components using browser APIs without `'use client'`
  - Components with event handlers without `'use client'`

### Data Fetching Patterns
- Check for client-side `useEffect` + `fetch` that could be server component fetches
- Verify `INTERNAL_API_URL` is used in server components (not `NEXT_PUBLIC_API_URL`)
- Check for proper error handling on API calls
- Verify loading states exist for async data

### Routing
- Check dynamic routes have proper `generateStaticParams` where applicable
- Verify `loading.tsx` files exist for routes with async data
- Check `error.tsx` boundaries are in place
- Verify `not-found.tsx` pages exist for dynamic routes

### Performance
- Check for `next/image` usage instead of `<img>`
- Verify `next/font` is used for custom fonts
- Check for `next/link` instead of `<a>` for internal navigation
- Look for large client-side bundles that could be split
- Check for proper Suspense boundaries

### Metadata
- Verify pages export proper `metadata` or `generateMetadata`
- Check for `title`, `description` at minimum

### Anti-Patterns
- `router.push()` in server components (should use `redirect()`)
- `window` or `document` access without client component guard
- Importing server-only code in client components
- Large `'use client'` boundaries that could be split

## Output
List all findings with severity (CRITICAL/HIGH/MEDIUM/LOW), file location, and fix suggestion.
