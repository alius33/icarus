# Responsive Design Check

Verify the Icarus frontend works across all screen sizes.

## Breakpoints to Check
- Mobile: 375px (iPhone SE)
- Mobile Large: 428px (iPhone Pro Max)
- Tablet: 768px (iPad)
- Laptop: 1024px (small laptop)
- Desktop: 1280px (standard)
- Wide: 1536px (large monitor)

## Checks Per Breakpoint

### Layout
- Does the sidebar collapse/hide on mobile?
- Do data tables scroll horizontally or reflow?
- Are cards stacking properly on narrow screens?
- Is content readable without horizontal scrolling?
- Are touch targets at least 44x44px on mobile?

### Typography
- Is text readable at all sizes?
- Do headings scale down appropriately?
- Is line length comfortable (45-75 characters)?

### Navigation
- Is the nav accessible on mobile (hamburger menu or similar)?
- Are breadcrumbs truncated gracefully?
- Do tabs wrap or scroll on narrow screens?

### Tables
- Do data tables have a mobile-friendly alternative?
- Are action columns accessible on narrow screens?

### Forms
- Are inputs full-width on mobile?
- Are labels above inputs (not beside) on mobile?
- Is the submit button easily reachable?

### Images & Charts
- Do images scale with container?
- Are charts readable on mobile?

## Testing

If the dev server is running, use preview tools:
1. `preview_resize` with preset "mobile" → check layout
2. `preview_resize` with preset "tablet" → check layout
3. `preview_resize` with preset "desktop" → check layout
4. Take screenshots at each size

## Output
List issues by breakpoint and severity. Include Tailwind class suggestions for fixes.
