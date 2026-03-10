# Next Steps — Data Strategy & Dev Workflow
**Date:** 2026-02-09
**Attendees:** Richard Dosoo (Speaker 1), Azmain Hossain, BenVH (Speaker 4)
**Duration context:** Medium (~22 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Richard sets the data strategy for the week: Catherine must take complicated accounts (complex reinsurer, complex primary, complex broker, complex global entity) and sense-check the data in CLARA against what she expects. Goal is to surface 80-90% of data mapping issues in one pass rather than picking them off incrementally.
- If no schema changes are needed, the plan is build to dev Monday, staging Thursday, prod Thursday. If schema changes are required, they handle them Wednesday.
- Azmain reports ongoing frustration with Catherine and Josh being surprised by data discrepancies each call despite having provided the original data. Catherine is described as reluctant to explore the app independently.
- Richard frames the engagement problem as people feeling dragged to the finish line rather than brought to the party. Shift in tactic: involve them in the process rather than trying to impress them with output.
- Azmain proposes emailing Catherine, Josh, Natalia, Richard, and Ben with a clear ask: go through complex accounts, document gaps in a Word doc by end of Tuesday US time, then a call Wednesday to start fixing.
- BenVH joins and walks through a local development setup for Azmain. Azmain cannot run local dev due to Windows Subsystem for Linux / Docker issues that IT has not resolved despite tickets. BenVH has built a workaround using PowerShell scripts.
- Azmain floats the idea of using Claude Code's cloud environment instead of local dev, referencing what Richard showed him.
- Diya wants analytics on the blockers — some aggregated view of blockers across all clients or by specific clients with statistics. Current blocker analytics are described as conceptual rather than based on real trend data.
- Blocker presentation needs to change from cards to a filterable table.

## Decisions Made
- Data strategy this week: Catherine sense-checks complex accounts, no other feature work until data is stable -> Richard
- Blockers page needs to be rebuilt with relevant analytics only, not conceptual placeholders -> Azmain
- Blocker display to shift from cards to filterable table -> Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Email Catherine/Josh/Natalia/Ben with data sense-check ask | Azmain | 2026-02-09 | Open |
| Catherine to sense-check complex accounts against CLARA data | Catherine | End of Tue 2026-02-11 | Open |
| Wednesday call to review data gaps and plan fixes | Team | 2026-02-12 | Open |
| Rebuild blockers page with real analytics, filterable table | Azmain | TBD | Open |
| Walk Azmain through local dev workaround | BenVH | 2026-02-09 | In Progress |

## Stakeholder Signals
- Richard is tactically reframing the engagement approach — moving from "show them the output" to "involve them in the process" to address Catherine and Josh's resistance.
- Azmain is visibly frustrated with the pace of stakeholder engagement, especially Catherine's reluctance to explore the app and repeated surprise about data she originally provided.
- BenVH is proactively building infrastructure improvements (local dev, guard rules) to reduce deployment friction.

## Open Questions Raised
- Will the complex-account sense-check reveal schema changes or just data fixes?
- Can Claude Code's cloud environment solve Azmain's local dev limitations?
- How to build genuine trend analysis on blockers when there is no week-over-week tracking mechanism yet?

## Raw Quotes of Note
- "If we don't tackle it holistically, all that's going to happen is every week there's a new schema change, a new data fix, and that's all we'll be doing." -- Richard, on the data strategy
