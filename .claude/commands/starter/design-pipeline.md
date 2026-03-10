# Design Pipeline

A four-step pipeline that transforms a PRD into a reviewed interactive prototype. Produces user stories, a UX spec, a working prototype, and a design review — all prefixed with `pm-` for easy sharing with product managers.

## Usage

```
/design-pipeline <STORY_ID> <PRD_FILE_PATH> [simple|advanced]
```

**Arguments:**
- `STORY_ID` — e.g. `DS-01`
- `PRD_FILE_PATH` — path to the PRD file, e.g. `docs/requirements/DS-01-feature.md`
- Mode — `simple` (default) or `advanced`

**Parsing:**
- First token → STORY_ID
- Second token → PRD_FILE_PATH
- Third token → MODE (default `simple` if omitted)

**Output directory:** `docs/designs/<STORY_ID>/`

---

## Pipeline Execution

Run all four steps in sequence. Each step builds on the previous.

---

### Step 1 — Product Manager: Write User Stories

**Goal:** Convert the PRD into structured user stories with design-specific acceptance criteria.

**Instructions:**

1. Read the PRD at `<PRD_FILE_PATH>`.
2. If `docs/technical-specification.md` exists, read it for context — but do NOT include implementation or technical details in the output.
3. Write user stories in this format:

```
## Story <N>: <Title>

**As a** <user type>
**I want** <goal>
**So that** <value>

### Acceptance Criteria

**Scenario: <name>**
- **Given** <precondition>
- **When** <action>
- **Then** <outcome>

(repeat for each scenario)

### Notes

**Expected UI flows:**
- <numbered steps of how user moves through this feature>

**Key visual states:**
- <list: empty, loading, error, success, etc.>

**Interaction points:**
- <what needs to be clickable, submittable, navigable>
```

4. Write one story per major feature area in the PRD.
5. Do NOT include: architecture, API design, database decisions, component library choices, or implementation notes.
6. Save to `docs/designs/<STORY_ID>/pm-user-stories.md`.

---

### Step 2 — UX Designer: Create UX Spec

**Goal:** Translate user stories into a complete UX specification that the prototype builder can implement without guessing.

**Instructions:**

1. Read `docs/designs/<STORY_ID>/pm-user-stories.md`.
2. Produce the following sections:

**User Flows**
- One numbered flow per story
- Each step is a clear action: "User clicks X → sees Y"
- Include branching paths (error states, empty states, success paths)

**Screen Inventory**
- List every distinct screen, view, panel, or modal needed
- For each: name, purpose, when it appears

**Layout Specs**
- For each screen in the inventory, describe:
  - Page sections (header, sidebar, main content, footer, etc.)
  - What content appears in each section
  - Visual hierarchy (what's most prominent, secondary, tertiary)
  - Prose descriptions only — no ASCII art or diagrams

**Component Inventory**
- List all UI components needed (buttons, forms, cards, tables, modals, tabs, etc.)
- For each component: name, purpose, and its states (default, hover, active, disabled, error, empty, loading)

**Interaction Notes**
- What happens on each significant user action (click, submit, load, error)
- Transition descriptions (e.g., "modal slides in from right", "list refreshes in place")

**Content Notes**
- Placeholder text guidance for forms, empty states, loading messages
- Any copy that conveys important UX intent

3. Save to `docs/designs/<STORY_ID>/pm-ux-spec.md`.

---

### Step 3 — Prototype Builder: Build the Demo

**Goal:** Build a working interactive prototype that covers all flows and states from the UX spec.

**Instructions:**

1. Read `docs/designs/<STORY_ID>/pm-user-stories.md` and `docs/designs/<STORY_ID>/pm-ux-spec.md`.
2. Create `docs/designs/<STORY_ID>/prototype/` directory.

**If MODE is `simple` (default):**

Create a single file: `docs/designs/<STORY_ID>/prototype/index.html`

Requirements:
- Fully self-contained — must open by double-clicking, no server or build step
- All CSS in a `<style>` block (no external stylesheets or CDN links)
- All JS in a `<script>` block (no external scripts or CDN links)
- Vanilla JS only — no frameworks
- Design system: clean, neutral, professional
  - Font stack: `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
  - Muted color palette: `#f8f9fa` background, `#212529` text, `#0d6efd` primary, `#6c757d` secondary
  - Consistent spacing (8px grid), clear visual hierarchy
- Must implement: tab switching, modals, form state, loading states, error states using hardcoded/mock data
- Cover ALL screens listed in the UX spec
- Include ALL interaction states from the component inventory

**If MODE is `advanced`:**

Scaffold a Vite React project at `docs/designs/<STORY_ID>/prototype/`

Structure:
```
prototype/
├── index.html
├── package.json
├── vite.config.js
├── README.md
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── App.css
    └── components/
        └── (one file per screen/component from UX spec)
```

Requirements:
- `package.json` must include: `"react"`, `"react-dom"`, `"vite"`, `"@vitejs/plugin-react"` as dependencies/devDependencies
- Plain CSS modules — no PostCSS, no Tailwind, no external CSS libraries
- All data is hardcoded mock data — no backend required
- `README.md` must include: "Run with: `npm install && npm run dev`"
- Cover ALL screens and flows from the UX spec
- Include ALL interaction states from the component inventory

**Both modes:**
- Use hardcoded/mock data throughout — no real API calls
- Be complete enough for a stakeholder to understand the feature intent
- Show all states: loading, error, empty, success

---

### Step 4 — Design Reviewer: Review Against Acceptance Criteria

**Goal:** Evaluate the prototype against the acceptance criteria and UX spec, produce a verdict, and kick back to the responsible step if blocking gaps are found.

**Instructions:**

1. Read `docs/designs/<STORY_ID>/pm-user-stories.md` — these are the acceptance criteria.
2. Read `docs/designs/<STORY_ID>/pm-ux-spec.md` — these are the intended flows and components.
3. If MODE is `simple`: read `docs/designs/<STORY_ID>/prototype/index.html` in full.
   If MODE is `advanced`: scan all files in `docs/designs/<STORY_ID>/prototype/src/`.

4. Evaluate against these dimensions:

**Acceptance Criteria Coverage**
- Go through each Given/When/Then scenario
- Mark each: ✅ Covered / ⚠️ Partially covered / ❌ Missing

**Flow Completeness**
- Go through each user flow from the UX spec
- Can a user navigate the complete flow in the prototype?

**Component Completeness**
- Is every component from the component inventory present?
- Does each component show all its listed states?

**Interaction Fidelity**
- Do interactions behave as described in the Interaction Notes?

**Visual Clarity**
- Is the layout clear and understandable?
- Would a stakeholder grasp the intent within 60 seconds?

**Missing States**
- Are there any empty/error/loading/success states that were specified but not implemented?

5. Write the review in this format:

```markdown
# Design Review — <STORY_ID> (Revision <N>)

## Verdict: [Ready for Stakeholder Review | Needs Revision]

## What's Done Well
1. <strength>
2. <strength>
3. <strength>

## Gaps vs Acceptance Criteria (Blocking)
These must be fixed before stakeholder review:
- [ ] <gap> → **Owner: Step <N> (<role name>)**
- [ ] <gap> → **Owner: Step <N> (<role name>)**

## Polish Suggestions (Non-Blocking)
- <suggestion>
- <suggestion>

## Acceptance Criteria Checklist
| Scenario | Status | Notes |
|----------|--------|-------|
| <name> | ✅/⚠️/❌ | <note> |
```

6. **Assigning gaps to the right step:**
   For each blocking gap, determine who owns it:
   - **Step 3 (Prototype Builder)** — the spec was clear but the prototype didn't implement it (missing screen, broken interaction, missing state)
   - **Step 2 (UX Designer)** — the prototype couldn't be built correctly because the spec was ambiguous, incomplete, or contradictory
   - **Step 1 (Product Manager)** — the stories lacked the acceptance criteria or detail needed to spec the UX

7. **Revision loop — max 2 revision cycles:**

   After saving the review, check: are there any blocking gaps?

   **If yes AND revision count < 2:**
   - Announce: `"Revision <N> needed. Kicking back to Step <earliest owner step>: <role name>."`
   - Group all gaps by their owner step. Re-run from the **earliest** step that owns a gap, then re-run every step after it in sequence.
     - If any gap is owned by Step 1 → re-run Steps 1 → 2 → 3 → 4
     - If the earliest gap owner is Step 2 → re-run Steps 2 → 3 → 4
     - If all gaps are owned by Step 3 → re-run Steps 3 → 4
   - Each re-run step reads the reviewer's feedback from `pm-design-review.md` and addresses the gaps attributed to it before producing its revised output (overwriting the previous version of its file).
   - After the re-run, the reviewer runs again as a new revision (increment revision count).

   **If yes AND revision count = 2:**
   - Do NOT re-run any steps.
   - Print: `"Max revisions reached. Blocking gaps remain — human review required."`
   - Proceed to the Consolidated Readout.

   **If no blocking gaps:**
   - Proceed directly to the Consolidated Readout.

8. Verdict is **Ready for Stakeholder Review** only if there are zero blocking gaps.
9. Save to `docs/designs/<STORY_ID>/pm-design-review.md`.

---

## Consolidated Readout

After the pipeline finishes (all steps complete, or max revisions reached), print this summary:

```
=== Design Pipeline Complete ===

Story ID:  <STORY_ID>
PRD:       <PRD_FILE_PATH>
Mode:      <simple|advanced>
Revisions: <0 | 1 | 2> revision cycle(s) completed

1. User Stories     → docs/designs/<STORY_ID>/pm-user-stories.md
   <N> stories written with acceptance criteria

2. UX Spec          → docs/designs/<STORY_ID>/pm-ux-spec.md
   <N> screens defined, <N> user flows documented

3. Prototype        → docs/designs/<STORY_ID>/prototype/index.html (or prototype/)
   Mode: <simple — open index.html in a browser | advanced — run npm install && npm run dev>

4. Design Review    → docs/designs/<STORY_ID>/pm-design-review.md
   Verdict: <Ready for Stakeholder Review | Needs Revision | Max revisions reached>
   Blocking gaps remaining: <N>

Status: <Ready for stakeholder review | Needs human review — max revisions reached>
```
