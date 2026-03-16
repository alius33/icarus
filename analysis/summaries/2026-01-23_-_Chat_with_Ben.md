# Chat with Ben Brookes — Dashboard UI/UX Review
**Date:** 2026-01-23
**Attendees:** Ben Brookes, Azmain Hossain
**Duration context:** Short (~10 minutes)
**Workstreams touched:** WS2 CLARA (UI/UX, dashboard design)

## Key Points
- Ben walked through the main dashboard page and identified confusing visual elements: red backgrounds, multiple competing colour signals on the same account card (red box, orange top, amber status, red background), and a blue RAG pillbox that duplicated information
- The root cause was multiple people brain-dumping design ideas via Cursor prompts without coherent UX review — Azmain acknowledged they were "MacGyvering the shit out of this with multiple people"
- Agreed to strip background colours from account cards entirely — keep only the coloured top bar for RAG status and the pillbox for update recency
- Data completeness percentage (e.g. "45%") was identified as useful but needed labelling — hovering revealed what fields were missing, which Ben found very helpful
- Ben raised that his Cursor credits were blocked — team-level usage cap hit despite not using $1,000 worth of credits
- Azmain also blocked on Cursor — switching to getting Richard to run prompts on his behalf
- Ben requested a developer laptop from Diya, anticipating pushback about his focus on migrations vs tool development
- Edit context (restricting users to editing only their own accounts) not yet implemented — requires employee list completion and SSO mapping; BenVH has limited availability due to another race
- Developer laptops for Azmain and Richard approved and expected Tuesday

## Decisions Made
- **Strip background colours from dashboard account cards** (type: design, confidence: high) — keep coloured top bar for RAG status only, remove confusing red/green backgrounds
- **Remove blue RAG pillbox** (type: design, confidence: high) — redundant with top bar colour
- **Convert data completeness display to labelled pillbox** (type: design, confidence: medium) — show "Data Completeness 45%" instead of just "45"
- **Defer edit restrictions until employee mapping is complete** (type: prioritization, confidence: high) — cannot implement without SSO identity mapping

## Action Items
| Action | Owner | Deadline | Confidence |
|--------|-------|----------|------------|
| Remove background colours from dashboard account cards | Azmain Hossain | 2026-01-23 | High |
| Remove blue RAG pillbox from card design | Azmain Hossain | 2026-01-23 | High |
| Label data completeness percentage properly | Azmain Hossain | 2026-01-23 | Medium |
| Get employee list under Colin mapped into system | Azmain Hossain | 2026-01-24 | High |
| Request developer laptop approval from Diya | Ben Brookes | 2026-01-23 | Medium |

## Theme Segments
| Timestamp Range | Theme | Speakers | Tone |
|----------------|-------|----------|------|
| 0:00-3:30 | Dashboard visual confusion walkthrough | Ben, Azmain | Diagnostic, candid |
| 3:30-6:00 | Data completeness display and RAG simplification | Ben, Azmain | Constructive, collaborative |
| 6:00-7:30 | Quick updates panel and CSM filtering | Azmain, Ben | Practical |
| 7:30-8:30 | Cursor credits blocked, licence crisis | Ben, Azmain | Frustrated, resourceful |
| 8:30-10:00 | Edit restrictions, BenVH availability, developer laptops | Ben, Azmain | Pragmatic, wrap-up |

## Power Dynamics
- **Ben Brookes** showed product ownership by doing hands-on UX testing — he navigated the app, identified specific problems, and proposed solutions. His frustration was directed at the output, not the people, and his feedback was actionable.
- **Azmain Hossain** was receptive and transparent about the cause of the visual mess: multiple people prompting Cursor without UX coordination. His acknowledgement that "nobody's done UX testing on this" showed self-awareness about the development process.

## Stakeholder Signals
- **Ben Brookes** — Engaged as both a product owner and user. His request for a developer laptop signals he intends to continue hands-on building, despite the political risk of appearing unfocused on his core migration mandate. His comment about Diya "going for him" showed awareness of the tension.
- **Azmain Hossain** — Resource-constrained: blocked on Cursor, dependent on Richard and BenVH for critical operations. His admission that UX testing has been skipped entirely is an honest assessment of the development pace vs quality trade-off.
- **BenVH** (referenced) — Running another race in Amsterdam, providing limited availability. Becoming a single point of failure for database operations.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Azmain | Fix dashboard visual issues (strip backgrounds, fix RAG display) | Ben | High |
| Azmain | Map employees under Colin into the system | Ben | High |
| Ben | Submit developer laptop request | Diya | Medium |

## Meeting Effectiveness
- **Clarity of outcomes:** 9/10 — Very specific design decisions made with clear before/after
- **Decision quality:** 8/10 — Pragmatic fixes that address user confusion without scope creep
- **Engagement balance:** 8/10 — Ben led with observations, Azmain responded with solutions
- **Time efficiency:** 9/10 — Covered dashboard UX, credentials crisis, and edit restrictions in 10 minutes

## Risk Signals
| Risk | Severity | Signal |
|------|----------|--------|
| No UX review process exists for CLARA | MEDIUM | Multiple people prompting AI to add visual elements without coordination has created a confusing interface. Ben's review was the first structured UX feedback. |
| Cursor/Claude Code licence crisis | HIGH | Both Azmain and Ben blocked on Cursor. Team-level usage cap hit. Richard's personal account being shared as workaround. Entire development velocity at risk before Monday demo. |
| BenVH as single point of failure for database operations | MEDIUM | Running a race, limited availability. Any schema changes that break the database cannot be fixed quickly. |

## Open Questions Raised
- How will Cursor licencing be resolved before Monday?
- When will SSO identity mapping be complete so edit restrictions can be enforced?
- Should there be a formal UX review process before pushing visual changes to production?
- What is the logic behind the red side-bar on some accounts (blocker status vs update recency)?

## Raw Quotes of Note
- "We're MacGyvering the shit out of this with multiple people just brain dumping ideas" — Azmain Hossain, on the cause of the UI confusion
- "I think DIA is going to hit the roof. I've submitted a request for a developer laptop... Will you focus on fucking migrations? I am, dear. I'm just doing it in a technologically advanced way" — Ben Brookes, on the political risk of his tool-building

## Narrative Notes
This brief call was the first real UX feedback session for CLARA's dashboard, and it exposed a fundamental problem with AI-assisted development at speed: when multiple people prompt Cursor to add visual features without a coherent design system, the result is a confusing mess of competing colour signals. Ben's observation that a single account card could have a red box, orange top, amber status pillbox, and red background simultaneously was a perfect illustration of design-by-committee-via-AI. The quick resolution — strip everything back to a simple top bar for RAG status — was sensible and showed Ben's product instinct. The more concerning subtext was the licence crisis: both Azmain and Ben were blocked on Cursor, and the workaround of sharing Richard's personal Claude Code account raised obvious security and compliance questions. Going into the Monday demo with the primary developer unable to use development tools was a serious risk that would require immediate resolution.
