# Dark Mode Implementation

Add or audit dark mode support for the Icarus frontend.

## Steps

### 1. Audit Current Theme
- Check if `dark:` Tailwind variants are used
- Check for any theme context or provider
- Read `tailwind.config.ts` for `darkMode` setting
- Check `globals.css` for CSS custom properties

### 2. Implementation Strategy

#### Using Tailwind `dark:` variant
```typescript
// tailwind.config.ts
module.exports = {
  darkMode: 'class', // or 'media' for system preference
  // ...
}
```

#### Theme Toggle Component
Create a client component for theme switching:
- Store preference in localStorage
- Default to system preference
- Apply `dark` class to `<html>` element
- Avoid flash of wrong theme on load

### 3. Apply Dark Styles
For each component, add `dark:` variants:
- Backgrounds: `bg-white dark:bg-gray-900`
- Text: `text-gray-900 dark:text-gray-100`
- Borders: `border-gray-200 dark:border-gray-700`
- Cards: `bg-white dark:bg-gray-800`
- Sidebar: appropriate dark variant
- Tables: alternating row colors for dark mode
- Status badges: ensure contrast in both modes

### 4. Verify
- Test all pages in dark mode
- Check contrast ratios meet WCAG AA
- Verify charts/graphs are readable
- Check no hard-coded colors bypass the theme

## Output
Files modified, components updated, any accessibility issues found.
