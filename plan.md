# Icarus Refactoring Plan: Simplify & Deduplicate

## Overview
Aggressive refactoring of both frontend and backend to eliminate massive duplication.
Breaking API changes allowed. Estimated 35-45% code reduction across both sides.

---

## Phase 1: Backend CRUD Router Factory

**Goal:** Replace 15+ nearly identical CRUD routers with a factory pattern.

### 1a. Create `backend/app/routers/crud_factory.py`
- Generic `create_crud_router()` function that generates standard endpoints:
  - `GET /` — list with configurable filters, search, ordering
  - `GET /{id}` — detail
  - `POST /` — create with optional writeback hook
  - `PATCH /{id}` — update with optional writeback hook
  - `DELETE /{id}` — delete with DeletedImport tracking
- Parameters: model class, schema classes, prefix, filter config, writeback hooks, ordering
- Supports: text search (ILIKE), enum filters, project_id FK filtering, date range filtering

### 1b. Create `backend/app/routers/board_mixin.py`
- `add_board_routes()` function for kanban board endpoints:
  - `GET /board` — group by status field, return columns with counts
  - `PATCH /{id}/position` — drag-drop reordering
- Parameters: status field name, status config (label/color/order), entity name in response

### 1c. Create `backend/app/routers/timeline_mixin.py`
- `add_timeline_routes()` for date-sorted timeline endpoints
- Parameters: date field, timeline item schema

### 1d. Migrate simple routers first (lowest risk)
Convert these to use the factory (pure CRUD, no custom endpoints):
- `commitments.py`
- `glossary.py`
- `dependencies.py`
- `wins.py` (keep summary endpoint as manual addition)
- `adoption.py`
- `divisions.py`
- `resources.py`
- `scope.py`
- `sentiments.py`
- `contradictions.py`
- `influence_signals.py`
- `topic_signals.py`
- `meeting_scores.py`

### 1e. Migrate board routers (medium risk)
Convert these to use factory + board mixin:
- `decisions.py` (factory + board + timeline + writeback)
- `tasks.py` (factory + board + timeline + writeback + labels/complete endpoints)
- `open_threads.py` (factory + board + writeback)

### 1f. Consolidate schemas
- Create `backend/app/schemas/base.py` with generic `BoardColumn[T]` and `BoardResponse[T]` types
- Remove duplicate Board/Timeline response types from individual schema files
- Keep entity-specific Create/Update schemas (these have real differences)

### 1g. Remove ActionItem model (dead code)
- Delete `backend/app/models/action_item.py`
- Delete `backend/app/routers/action_items.py`
- Delete `backend/app/schemas/action_item.py`
- Remove from main.py router registration
- Create migration to drop action_items table

---

## Phase 2: Frontend Generic Components

**Goal:** Replace 21 near-identical entity components with 7 generic ones.

### 2a. Create generic types in `frontend/src/lib/types.ts`
- `BoardColumn<T>`, `BoardResponse<T>` generic interfaces
- `EntityConfig<T>` interface for component configuration
- Remove duplicate `DecisionBoardColumn`, `TaskBoardColumn`, `ThreadBoardColumn` etc.

### 2b. Create `frontend/src/components/generic/GenericBoard.tsx`
- Replaces: `DecisionBoard`, `TaskBoard`, `ThreadBoard` (3 files, ~630 lines → 1 file, ~220 lines)
- Config-driven: entity name, status field, status config map, card component, API callbacks
- Contains all dnd-kit logic once

### 2c. Create `frontend/src/components/generic/GenericCard.tsx`
- Replaces: `DecisionCard`, `TaskCard`, `ThreadCard` (3 files, ~330 lines → 1 file, ~120 lines)
- Config-driven: field mappings for identifier, status badge, tags, metadata row
- Uses `useSortable()` once

### 2d. Create `frontend/src/components/generic/GenericViewSwitcher.tsx`
- Replaces: `DecisionViewSwitcher`, `TaskViewSwitcher`, `ThreadViewSwitcher` (3 files, ~450 lines → 1 file, ~160 lines)
- Config-driven: view options, filter definitions

### 2e. Create `frontend/src/components/generic/GenericList.tsx`
- Replaces: `DecisionList`, `TaskList` (2 files, ~420 lines → 1 file, ~200 lines)
- Config-driven: column definitions, sort/group keys, row renderer

### 2f. Create `frontend/src/components/generic/GenericTimeline.tsx`
- Replaces: `DecisionTimeline`, `TaskTimeline` (2 files, ~370 lines → 1 file, ~190 lines)
- Extract shared date utilities to `src/lib/date-utils.ts`

### 2g. Create `frontend/src/components/generic/GenericDetailPanel.tsx`
- Replaces: `DecisionDetailPanel`, `TaskDetailPanel`, `ThreadDetailPanel` (3 files, ~745 lines → 1 file, ~250 lines)
- Config-driven: field definitions (type, label, required, options), action buttons
- Handles dirty state, save/delete/cancel, backdrop close

### 2h. Create `frontend/src/components/generic/GenericCreateModal.tsx`
- Replaces: `DecisionCreateModal`, `TaskCreateModal`, `ThreadCreateModal` (3 files, ~340 lines → 1 file, ~130 lines)
- Config-driven: field definitions, validation, API callback

### 2i. Create entity config files
- `frontend/src/config/decisions.ts` — all decision-specific config (status values, colors, field mappings, API endpoints)
- `frontend/src/config/tasks.ts` — all task-specific config
- `frontend/src/config/threads.ts` — all thread-specific config
- These are small (~50-80 lines each) pure data files

### 2j. Refactor entity pages to use generic components
- `app/decisions/page.tsx` → uses generic components + decision config
- `app/tasks/page.tsx` → uses generic components + task config
- `app/open-threads/page.tsx` → uses generic components + thread config
- Could eventually become a single `useEntityPage()` hook + config

---

## Phase 3: API & SWR Layer Simplification

### 3a. Create `frontend/src/lib/entity-api.ts`
- Generic `createEntityAPI<T, Create, Update>(basePath)` factory
- Returns typed object with: `list()`, `detail()`, `board()`, `create()`, `update()`, `updatePosition()`, `delete()`
- Replace 40+ individual API functions with ~10 factory instances

### 3b. Create `frontend/src/lib/entity-swr.ts`
- Generic `createEntityHooks<T>(name, api)` factory
- Returns: `useList()`, `useDetail()`, `useBoard()`
- Replace 30+ individual SWR hooks with factory instances

### 3c. Clean up `api.ts` and `swr.ts`
- Keep non-entity endpoints (dashboard, search, timeline, import, auth)
- Remove all entity CRUD functions that are now handled by factories

---

## Phase 4: Cleanup & Validation

### 4a. Delete replaced files
- Remove all entity-specific Board/Card/List/ViewSwitcher/DetailPanel/CreateModal files
- Remove empty component directories if applicable

### 4b. Update imports across the app
- All pages and components that imported old components → import generic + config

### 4c. Test
- Run `npm run build` to verify no type errors
- Run `vitest` for frontend tests
- Run `pytest` for backend tests
- Manual smoke test of board drag-drop, CRUD operations, detail panels

---

## Expected Outcome

| Metric | Before | After | Reduction |
|--------|--------|-------|-----------|
| Backend router files | 15+ files, ~3000 lines | Factory + 3 configs, ~800 lines | ~73% |
| Frontend entity components | 21 files, ~4000 lines | 7 generic + 3 configs, ~1400 lines | ~65% |
| API/SWR layer | ~800 lines | ~300 lines | ~62% |
| Total LoC reduction | — | — | ~2500-3000 lines |

## Risk Mitigation
- Phase 1d starts with simplest routers (pure CRUD) to validate the factory pattern
- Phase 2 creates generic components alongside existing ones, then swaps
- Each phase ends with build + test validation before proceeding
- Breaking API changes are coordinated (backend + frontend change together)
