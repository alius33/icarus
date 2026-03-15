Generate the weekly plan for Diya's AI Acceleration Programme deliverables. Follow these steps precisely.

## Step 0: Preflight Check

Verify the backend API is reachable:
```bash
curl -sf http://localhost:8000/api/programme-deliverables > /dev/null && echo "API OK" || echo "API UNREACHABLE"
```
If unreachable, tell the user to run `docker compose up -d db backend` first and stop.

## Step 1: Calculate Week Context

- Programme start: Monday 23 February 2026
- Calculate today's date and determine:
  - Which week just ended (Mon–Fri)
  - Which week starts next Monday
- If it's a weekend: assess the week that just ended, generate plan for the coming week
- If it's a weekday: assess the current week so far, generate plan for the current or next week

## Step 2: Load Context

Read these files/API endpoints to understand current state:

1. The **most recent weekly summary** in `analysis/weekly/` — critical for continuity
2. All transcript summaries from the past week in `analysis/summaries/`
3. Current deliverables + milestones: `GET /api/programme-deliverables`
4. Previous week's plan: `GET /api/weekly-plans` (check for existing plans)
5. Open risks from `analysis/trackers/risk_register.md` (tail, last 50 lines)
6. Recent action items from `analysis/trackers/action_items.md` (tail, last 50 lines)
7. `context/open_threads.md` — unresolved questions
8. `context/decisions.md` — recent decisions (tail, last 30 lines)

## Step 3: Assess Deliverable Progress

For each of the programme deliverables (from `GET /api/programme-deliverables`):

1. Cross-reference transcript summaries and the weekly report for evidence of progress
2. Determine appropriate RAG status:
   - GREEN: On track, evidence of progress
   - AMBER: Some concerns, slipping, or blocked dependencies
   - RED: Significantly behind, blocked, or at risk
3. Check milestones — identify any that should be marked COMPLETED or IN_PROGRESS based on evidence
4. Write a brief narrative note explaining the current state (2-3 sentences)
5. Progress auto-calculates from milestone completion

For each deliverable that needs updating:
```
PATCH /api/programme-deliverables/{id}
Body: { "rag_status": "GREEN|AMBER|RED", "notes": "narrative text" }
```

For milestones that changed status:
```
PATCH /api/programme-deliverables/milestones/{id}
Body: { "status": "COMPLETED|IN_PROGRESS|BLOCKED", "completed_week": N, "evidence": "what proves this" }
```

## Step 4: Review Carryforward

If a previous week's plan exists, check incomplete actions (PENDING or IN_PROGRESS):

For each incomplete action, assess:
- Is it still relevant? → Carry forward with `carried_from_week` set
- Is it no longer needed? → Drop it and explain why
- Has it been superseded? → Drop it

Output reasoning for any dropped actions.

## Step 5: Generate New Actions

Create actions in four categories:

### Deliverable Strategic (2-4 actions)
High-level moves aligned to Diya's expectations. These should address programme-level deliverable goals.

### Deliverable Tactical (4-8 actions)
Specific tasks for the coming week that advance deliverables. Each should reference a specific deliverable_id.

### Programme Strategic (1-3 actions)
Broader programme moves — governance, stakeholder engagement, cross-OU coordination.

### Programme Tactical (2-4 actions)
Concrete programme tasks — meetings to schedule, reports to prepare, follow-ups to chase.

Each action needs: title, description, priority (HIGH/MEDIUM/LOW), category, and optionally deliverable_id + owner.

## Step 6: Write to API

Create the weekly plan atomically. **IMPORTANT**: Both summary fields must use structured markdown (rendered by the frontend). Follow these formats:

### `deliverable_progress_summary` format:
```markdown
**Programme Week N** — one-line theme.

### Key Developments
- **Bold lead-in** for each major development (2-5 bullets)

### Milestones Completed (if any this week)
| Milestone | Deliverable | Significance |
|-----------|-------------|-------------|
| M##: Name | D## | What it means |

### Emerging Risks (or Critical Risks / Deliverable Concerns)
- **Risk name** — brief detail with risk ID if applicable
```

### `programme_actions_summary` format (retrospective weeks):
```markdown
### Week N Outcome Summary

| # | Priority | Result |
|---|----------|--------|
| 1 | Action description | **ACHIEVED** / **UNRESOLVED** / **ESCALATED** — detail |
```

### `programme_actions_summary` format (forward-looking weeks):
```markdown
### Week N Priorities

| # | Priority | Action | Origin |
|---|----------|--------|--------|
| 1 | **CRITICAL** | Action description | Carried from Week N / New |
```

Use headers (###), bold (**), bullet lists, and tables. Do NOT write dense paragraph blocks.

```
POST /api/weekly-plans
Body: {
  "week_number": N,
  "week_start_date": "YYYY-MM-DD",  (Monday)
  "week_end_date": "YYYY-MM-DD",    (Friday)
  "deliverable_progress_summary": "Structured markdown (see format above)...",
  "programme_actions_summary": "Structured markdown (see format above)...",
  "actions": [
    {
      "category": "deliverable_strategic|deliverable_tactical|programme_strategic|programme_tactical",
      "title": "...",
      "description": "...",
      "priority": "HIGH|MEDIUM|LOW",
      "owner": "name or null",
      "deliverable_id": N or null,
      "position": 0,
      "is_ai_generated": true,
      "carried_from_week": N or null
    }
  ],
  "snapshots": [
    {
      "deliverable_id": N,
      "week_number": N,
      "rag_status": "GREEN|AMBER|RED",
      "progress_percent": 0-100,
      "milestones_completed": N,
      "milestones_total": N,
      "narrative": "Brief progress note"
    }
  ]
}
```

## Step 7: Output Summary

Print a structured summary to the terminal:

```
═══════════════════════════════════════════════════
  WEEKLY PLAN — Week N (DD Mon – DD Mon YYYY)
═══════════════════════════════════════════════════

📊 DELIVERABLE PROGRESS
────────────────────────────────────────
Pillar 1: IRP Portfolio Governance
  🟢/🟡/🔴 Deliverable title — NN% (N/N milestones)

Pillar 2: Platform-Embedded Customer Intelligence
  ...

Pillar 3: Internal Productivity & Revenue Acceleration
  ...

📋 ACTIONS FOR THE WEEK
────────────────────────────────────────
DELIVERABLE STRATEGIC
  [HIGH] Action title — owner
  ...

DELIVERABLE TACTICAL
  [MED]  Action title — owner — re: Deliverable Name
  ...

PROGRAMME STRATEGIC
  ...

PROGRAMME TACTICAL
  ...

⏩ CARRIED FORWARD (from Week N-1)
  Action title (reason for carry)
  ...

❌ DROPPED
  Action title — reason
  ...

✅ Plan saved. View at: /weekly-plan
═══════════════════════════════════════════════════
```
