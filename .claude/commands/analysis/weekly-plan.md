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
3. **Transcript list with IDs**: `GET /api/transcripts?limit=50` — you need the `id` field for each transcript to populate `source_transcript_id` on actions. Note which transcript IDs correspond to which meetings.
4. Current deliverables + milestones: `GET /api/programme-deliverables`
5. Previous week's plan: `GET /api/weekly-plans` (check for existing plans)
6. Open risks from `analysis/trackers/risk_register.md` (tail, last 50 lines)
7. Recent action items from `analysis/trackers/action_items.md` (tail, last 50 lines)
8. `context/open_threads.md` — unresolved questions
9. `context/decisions.md` — recent decisions (tail, last 30 lines)
10. Current programme wins: `GET /api/wins` — recent wins for context and to identify win-worthy actions
11. Current outreach contacts: `GET /api/outreach` + `GET /api/divisions` — pipeline status, stale contacts needing follow-up

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

## Step 4: Review Carryforward (MANDATORY)

**Every incomplete action from the previous week MUST be accounted for.** Fetch the previous week's plan:
```
GET /api/weekly-plans/{previous_plan_id}
```

For each action with status PENDING or IN_PROGRESS:

1. **Default: Carry forward** — create a new action in the new plan with:
   - `carried_from_week` set to the original week (preserve the earliest week, not just last week)
   - Same `source_transcript_id` and `context` from the original action (copy them over)
   - Updated title/description if the situation has evolved
   - Same or adjusted priority based on how long it's been unresolved (items carried 2+ weeks should escalate in priority)

2. **Exception: Drop** — ONLY if you can provide specific evidence that the action was:
   - **Completed in a different form** (cite which action/event resolved it)
   - **Superseded** by a specific newer action (cite the action ID)
   - **No longer relevant** due to a programme change (cite the decision/event)

**You MUST output reasoning for every dropped action.** Unexplained drops are not acceptable — incomplete actions don't just disappear.

Also check ALL previous weeks (not just the immediately preceding one) for actions that were IN_PROGRESS but never carried forward. These represent dropped balls that need to be picked up.

## Step 5: Generate New Actions

Create actions in four categories:

### Deliverable Strategic (2-4 actions)
High-level moves aligned to Diya's expectations. These should address programme-level deliverable goals.

### Deliverable Tactical (4-8 actions)
Specific tasks for the coming week that advance deliverables. Each should reference a specific deliverable_id.

### Programme Strategic (1-3 actions)
Broader programme moves — governance, stakeholder engagement, cross-OU coordination.
- Review outreach pipeline (from Step 2, item 11): identify contacts who haven't been contacted in 2+ weeks (stale), contacts approaching `next_step_date`, and divisions with no engagement. Generate follow-up actions for these.
- If recent transcripts mentioned new cross-divisional opportunities, create actions to initiate contact.

### Programme Tactical (2-4 actions)
Concrete programme tasks — meetings to schedule, reports to prepare, follow-ups to chase.
- For each outreach contact with an upcoming `next_step_date` in the coming week, create a specific follow-up action.
- For contacts where `meeting_count` increased in the past week, create a post-meeting follow-up action.

Each action needs: title, description, priority (HIGH/MEDIUM/LOW), category, and optionally deliverable_id + owner.

### Source & Context (REQUIRED for every action — no exceptions)

Every action MUST have both `source_transcript_id` and `context`. These appear in a dropdown panel on each action in the UI, allowing the user to recall exactly why this action exists and what key terms mean.

**`source_transcript_id`** — the transcript ID from which this action was derived. Use the IDs from `GET /api/transcripts` (loaded in Step 2). If the action comes from a deliverable assessment rather than a specific transcript, use the most relevant recent transcript that discusses that deliverable.

**`context`** — a detailed explanation (3-8 sentences, markdown supported) that answers: *"Why does this action exist and what do the key terms mean?"*

Context quality bar — each context MUST:
1. **Define key concepts** — if the action title mentions a system, model, framework, or acronym, explain what it is
2. **Name the people involved** — who said what, who owns what, who is blocking
3. **Explain why it matters now** — what's the urgency, deadline, or dependency
4. **Reference specific evidence** — cite what was said in the meeting, not generic descriptions

Example — action title: "Coordinate with Banking Credit team on Agent Day framework for Training & Enablement":
```
**Agent Days** are full-day in-person AI adoption events run by the Banking Credit team
(Wasim and Nils). Their framework is directly relevant to Training & Enablement
deliverables (D4/D5).

**Four-tier agent model:**
1. **Copilot Light** — basic chat interface
2. **Copilot Studio** — low-code workflow builder
3. **Cursor coding agents with MCPs** — developer tools
4. **Custom-built agents** — full autonomy

**Critical success factors:** pre-work (surveys weeks before), "transit teachers" —
4+ trained multipliers pre-briefed on each participant's project, all technical setup
completed before the day, every participant builds their own agent.
```

Example — action title: "Resolve Kathryn Palkovics' COE overlap with AI programme scope":
```
**Kathryn Palkovics' Centre of Excellence (COE)** has three pillars: digital engagement,
enablement, and Gainsight/SFDC retirement. The **first pillar (digital engagement)
directly overlaps** with the AI programme's scope.

Key incidents: Kathryn Palkovics organised the Gainsight team meeting **without consulting
the CLARA team**, blindsiding them. She finds trivial CLARA issues every two days,
claims CSMs complained (they haven't). Her objectives were **approved by Natalia
Orzechowska and signed off by Diya**.

**Strategy**: Frame "digital enablement" (Kathryn Palkovics' domain) as distinct from "AI
enablement" (Azmain's domain). Diana Kazakova-Ivanova to discuss with Natalia O. Richard to raise
with Diya during London visit. Risk R#045.
```

Do NOT write generic context like "This action relates to the programme's strategic goals." Every context should contain specific names, dates, systems, or decisions from transcripts.

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
      "carried_from_week": N or null,
      "source_transcript_id": N or null,
      "context": "Detailed markdown explanation of key concepts (3-8 sentences)"
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

🤝 OUTREACH PIPELINE
────────────────────────────────────────
  Committed: N contacts
  Engaged: N contacts
  Interested: N contacts
  Initial Contact: N contacts
  ⚠️ Stale (no contact 2+ weeks): [names]
  📅 Next steps this week: [names + actions]

⏩ CARRIED FORWARD (from Week N-1)
  Action title (reason for carry)
  ...

❌ DROPPED
  Action title — reason
  ...

✅ Plan saved. View at: /weekly-plan
═══════════════════════════════════════════════════
```
