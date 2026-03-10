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
| Decision | Type | Made By | Confidence |
|----------|------|---------|------------|
| Data strategy this week: Catherine sense-checks complex accounts, no other feature work until data is stable | Priority | Richard | High |
| Blockers page needs to be rebuilt with relevant analytics only, not conceptual placeholders | Technical | Azmain/Richard | High |
| Blocker display to shift from cards to filterable table | UX | Azmain | Medium |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Email Catherine/Josh/Natalia/Ben with data sense-check ask | Azmain | 2026-02-09 | Open | High |
| Catherine to sense-check complex accounts against CLARA data | Catherine | End of Tue 2026-02-11 | Open | Medium — depends on Catherine's engagement |
| Wednesday call to review data gaps and plan fixes | Team | 2026-02-12 | Open | High |
| Rebuild blockers page with real analytics, filterable table | Azmain | TBD | Open | Medium |
| Walk Azmain through local dev workaround | BenVH | 2026-02-09 | In Progress | High |

## Theme Segments
| Time Range | Theme | Key Speakers |
|------------|-------|--------------|
| 0:00-4:00 | Catherine/Josh engagement problem and data strategy | Richard, Azmain |
| 4:00-9:00 | Holistic data validation plan, golden source vs Salesforce | Richard, Azmain |
| 9:00-13:00 | Diya's blocker analytics requirement, dashboard rebuild | Richard, Azmain |
| 13:00-22:00 | BenVH joins — local dev setup, guard rules, cloud environment discussion | BenVH, Azmain |

## Power Dynamics
- **Richard is the strategist and mentor.** He reframes Azmain's frustration with Catherine into a tactical engagement problem and proposes a solution. The tone is patient and coaching — not directive.
- **Azmain vents but accepts guidance.** His frustration with Catherine is palpable but he channels it productively once Richard provides the reframe.
- **BenVH operates independently.** He has already built guard rules and dev scripts without being asked. He joins the call with solutions, not questions.

## Stakeholder Signals
- **Richard:** Tactically reframing the engagement approach — moving from "show them the output" to "involve them in the process" to address Catherine and Josh's resistance. Shows strategic patience.
- **Azmain:** Visibly frustrated with the pace of stakeholder engagement, especially Catherine's reluctance to explore the app and repeated surprise about data she originally provided. Wants to move fast but is blocked by social friction.
- **BenVH:** Proactively building infrastructure improvements (local dev, guard rules) to reduce deployment friction. His contribution is entirely self-directed.
- **Catherine (discussed, not present):** Described as scared to explore the app. Richard attributes this to the broader engagement dynamic, not a personal failing. The golden source spreadsheet she maintains is too messy to import programmatically.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| Azmain | Send email to Catherine/Josh/Natalia/Ben with data ask | Richard | Firm |
| Richard | Jump on a call with Catherine if needed to help navigate | Azmain | Conditional |
| BenVH | Walk through local dev scripts with Azmain | Azmain | In progress |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 4 | Data strategy clear, dev workflow improving |
| Decision quality | 4 | Holistic sense-check is the right approach |
| Engagement balance | 3 | Two-person conversation until BenVH joins |
| Time efficiency | 3 | Some repetition of frustrations already voiced |
| Follow-through potential | 3 | Depends heavily on Catherine's willingness to engage |

## Risk Signals
- **Catherine engagement risk:** If Catherine does not complete the sense-check by Tuesday, the Wednesday fix session cannot happen, and the weekly cycle slips again. Richard's reframe is good strategy but depends on execution.
- **Local dev blockers:** Azmain still cannot run local dev. IT has not resolved WSL/Docker tickets. BenVH's PowerShell workaround may help but the underlying issue persists.
- **Blocker analytics are vaporware.** The current dashboard numbers are not based on real trend analysis. If Diya or other executives look at them, they could be misleading.

## Open Questions Raised
- Will the complex-account sense-check reveal schema changes or just data fixes?
- Can Claude Code's cloud environment solve Azmain's local dev limitations?
- How to build genuine trend analysis on blockers when there is no week-over-week tracking mechanism yet?

## Raw Quotes of Note
- "If we don't tackle it holistically, all that's going to happen is every week there's a new schema change, a new data fix, and that's all we'll be doing." -- Richard, on the data strategy

## Narrative Notes
This is a strategy and therapy session combined. Richard's reframe of the Catherine problem — from "she won't engage" to "we need to change our approach" — is the most important moment. Azmain is carrying genuine frustration from weeks of stakeholder friction, and Richard absorbs it and redirects it into a concrete plan. BenVH's contribution is characteristically independent: he shows up with solutions already built, walks through them, and leaves. The tension between Azmain's desire to move fast and the reality of stakeholder readiness is the defining dynamic of this phase of the programme.
