# Portfolio Review with Natalia
**Date:** 2026-02-05
**Attendees:** Natalia (Plant), Azmain Hossain, Sneha (mentioned)
**Duration context:** Long (~42 minutes, detailed requirements session)
**Workstreams touched:** WS2 CLARA

## Key Points
- Critical requirements redefinition session: Natalia redefining what "priority" means in CLARA
- Previous definition was arbitrary "high priority" — new definition: the 31 accounts on the 2026 migration timeline (aligned to scorecard target of 30 migrations)
- The 17 "accelerated" accounts are a subset needing special attention within the 31
- Natalia wants to rotate meeting focus: one week priority accounts, next week accelerated accounts
- Detailed tab restructuring requested:
  - Priority tab: shows all 31 migration customers tagged as priority
  - Accelerated tab: shows the 17 accelerated customers
  - Non-priority reds/ambers tab: with filter buttons (not separate tabs — less tabs is better)
  - Timeline tab: kept for quarterly target date views
- Key distinction: **status** = RAG (red/amber/green); **stage** = adoption stage (not started, in flight, complete). These have been conflated in the current UI — multiple fields all labelled "status"
- Natalia wants portfolio review tabs to be operational (for running the meeting) — separate from a management dashboard (for Diya/leadership)
- Management dashboard should replicate the manual PowerPoint reports currently produced: cumulative migration status by product (Risk Link, Risk Browser), in-flight RAG breakdown, overall portfolio health
- CSM dashboard (landing page) should be personalised — when Jeff signs in, he sees his accounts
- Management dashboard should be for senior users (Natalia, Stacy, Ben, Diya) — different landing page
- CSM Manager view should be separate: shows data completeness by CSM, action owners, gaps — not part of portfolio review
- Client health status must be manual (CSM input), not algorithmically derived from use case RAG statuses
- Natalia referenced the existing PowerPoint reporting as the minimum standard for what the management dashboard must show
- Discussion of Diya's engagement: presentations must be two slides, 15 minutes maximum. No feedback, just thumbs up/thumbs down.

## Decisions Made
- Priority = 2026 migration customers (31 accounts) aligned to scorecard → Natalia
- Separate views: Portfolio Review (operational), Management Dashboard (executive), CSM Manager View (people management) → Natalia/Azmain
- Status vs Stage naming must be corrected across the entire UI → Azmain
- Client health RAG is CSM-entered, not algorithmically derived → Natalia

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Redesign portfolio review tabs per Natalia's specifications | Azmain | Before Monday meeting | Open |
| Create management dashboard replicating PowerPoint metrics | Azmain | Next 2 weeks | Open |
| Fix status vs stage naming across all screens | Azmain | This sprint | Open |
| Get Sneha's Excel data for historical migration charts | Azmain | This week | Open |
| Separate CSM Manager view from Portfolio Review | Azmain | Later sprint | Open |

## Stakeholder Signals
- Natalia is the most structured requirements thinker on the team — she knows exactly what she needs and can articulate the distinction between operational, executive, and management views
- She is diplomatically critical of Ben's approach: he's adding too many features to one screen in one meeting, creating confusion
- Diya remains hard to reach and harder to read — Natalia and others can't tell whether she has understood or agreed
- Sneha is the data backbone for the manual PowerPoint reports — her Excel data is the source of truth for historical trends

## Open Questions Raised
- How to handle historical data in the dashboard — CLARA doesn't have historical records, may need to manually import from previous monthly reports
- What does "migration complete" mean precisely — when Risk Link/Risk Browser is switched off?
- Should the management dashboard be a separate URL or a role-gated view within the same app?

## Raw Quotes of Note
- "Sometimes, I'm not sure you know... I have people coming, what do you think she wants?" — Natalia, on the difficulty of interpreting Diya's communications
