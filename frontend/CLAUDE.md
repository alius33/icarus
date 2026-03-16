# Icarus Frontend

## Tech Stack

- **Next.js 14.2** (App Router) with TypeScript
- **Tailwind CSS 3.4** with `@tailwindcss/typography`
- **SWR 2.4** for data fetching/caching
- **Recharts 3.8** for charts and visualisations
- **@dnd-kit** for drag-and-drop (kanban boards)
- **lucide-react** for icons
- **react-markdown** + remark-gfm for markdown rendering

## Key Files

| File | Purpose |
|------|---------|
| `src/lib/api.ts` | `fetchApi<T>()` wrapper + all API endpoint functions (32 groups) |
| `src/lib/types.ts` | 50+ TypeScript interfaces for all entities |
| `src/lib/swr.ts` | 30+ SWR hooks (useDashboard, useTranscripts, useTasks, etc.) |
| `src/lib/utils.ts` | Helpers: cn, getStatusColor, formatDate, ragDotColor, severityColor, etc. |
| `src/lib/hooks/useToast.tsx` | Toast notification hook |
| `src/lib/markdown-extract.ts` | Markdown content extraction utilities |

## Data Flow

- **Server components** use `INTERNAL_API_URL` (default: `http://backend:8000` in Docker)
- **Client components** use `NEXT_PUBLIC_API_URL` (default: `http://localhost:8000` for dev)
- All data fetched via SWR hooks with auto-revalidation

## Component Patterns

- **ViewSwitcher** — toggles board/list/timeline views (decisions, tasks, threads)
- **DetailPanel** — slide-in side-sheet for entity details
- **CreateModal** — entity creation form modal
- **EntityModal** — generic wrapper for inline edit modals on dashboard
- **Skeletons** — `CardSkeleton`, `TableSkeleton`, `DetailSkeleton` for loading states

## Page Routes (~25 active)

`/` (dashboard), `/timeline`, `/transcripts`, `/transcripts/[id]`, `/upload`,
`/speaker-review`, `/analysis/summaries`, `/analysis/summaries/[id]`,
`/analysis/weekly`, `/analysis/weekly/[id]`, `/projects`, `/projects/new`,
`/projects/[id]`, `/stakeholders`, `/stakeholders/[id]`, `/decisions`,
`/tasks`, `/open-threads`, `/commitments`, `/action-items`, `/my-items`,
`/wins`, `/outreach`, `/weekly-plan`, `/glossary`, `/search`

## Deleted Pages

See `.claude/rules/deleted-features.md` for the full list of intentionally removed pages and models.

## Theme

- Dark-first design: `bg-gray-900` base
- Geist font family
- All components support dark mode

## Commands

```bash
npm run dev      # Dev server (port 3000, hot reload)
npm run build    # Production build
npm run lint     # ESLint
npx vitest       # Run tests (vitest + Testing Library)
```
