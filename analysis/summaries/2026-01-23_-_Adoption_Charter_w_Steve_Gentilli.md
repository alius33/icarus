# Adoption Charter with Steve Gentilli — Field Mapping and Platform Consolidation
**Date:** 2026-01-23
**Attendees:** Azmain Hossain, Steve Gentilli
**Duration context:** Long (~52 minutes)
**Workstreams touched:** WS4 Friday (Adoption Charter), WS2 CLARA (data model, feature roadmap)

## Key Points
- Extended personal conversation at the start: Steve returning from two weeks of Christmas holiday, Azmain discussing life with a one-year-old — both establishing rapport before getting into work
- Steve had been maintaining a standalone Excel tracker for adoption charters since before Christmas; he contacted Azmain to see if the fields could be consolidated into CLARA rather than maintaining parallel systems
- Core exercise: Steve walked through his Excel columns while Azmain identified which were already in CLARA's database — approximately 15 of 20 columns already existed, with around 5 needing to be added
- Fields already in CLARA: region, sales manager, client director, client name, client ID, active status, sales stage (partial), solution architect, use case information, CSM assignment, blocker tracking
- Fields needing addition: MPNS (Model and Product Specialist), SAT requirement, implementation basis (client-led/partner-led/Moody's-led), adoption charter status (manual: in progress/under review/awaiting approval/approved), implementation lead handoff status
- Steve proposed implementation basis as a three-option field: client-led, partner-led, or Moody's-led — Azmain noted the partner section was being built separately with Alexandre
- Steve showed additional columns from the implementation team (added by Kate Grove) — these were marked for separate discussion with Kate
- Azmain demonstrated the adoption charter feature Ben had built: multi-stage process with success criteria, milestones, blueprints, use case linking, roles and responsibilities, and two workflow options (Word document upload or in-app creation)
- Steve saw the adoption charter feature for the first time and was immediately interested — he proposed adding manual status indicators at each stage (not automated from field counts) since one success criteria might be sufficient for some clients while 15 might be needed for others
- Live demo had issues: a page failed to load and customers temporarily disappeared — Azmain attributed this to BenVH's Alembic migration breaking things
- Steve offered to build a Cursor prototype of his vision but Azmain pushed back — foundation-level discussions needed to happen first before prototyping
- Both agreed the next step was for Steve to refine his column requirements with lookup values, and for Azmain to facilitate a broader discussion with Ben, Steve, Liz, and Kate after the Monday exec meetings
- Steve expressed strong alignment with the platform consolidation approach: "If we had 20 columns, you've already got 15 — let's just add these 5"
- Azmain revealed he had everyone under Andy Frapp (all 17,000 Moody's employees) in an Excel file and could map them into the system if needed

## Decisions Made
- **Consolidate Steve's adoption charter tracker into CLARA** (type: strategic, confidence: high) — no point maintaining parallel Excel; CLARA already has most fields
- **Approximately 5 new fields to be added to CLARA** (type: feature, confidence: high) — MPNS, SAT requirement, implementation basis, adoption charter status, and related fields
- **Adoption charter status should be manual, not algorithmic** (type: design, confidence: high) — Steve's recommendation that the number of success criteria needed varies by client makes automated status unreliable
- **Partner section fields (introduced/selected/rejection reason) to be discussed with Alexandre** (type: governance, confidence: medium) — Steve marked these yellow for cross-team discussion
- **Implementation team fields to be discussed with Kate Grove** (type: governance, confidence: medium) — Kate added these columns and should validate requirements
- **Defer all new fields until after Monday exec meetings** (type: timing, confidence: high) — no schema changes until BenVH can review

## Action Items
| Action | Owner | Deadline | Confidence |
|--------|-------|----------|------------|
| Refine column requirements document with lookup values | Steve Gentilli | 2026-01-24 (weekend) | High |
| Send notes from conversation to Steve | Azmain Hossain | 2026-01-23 | High |
| Facilitate discussion with Ben, Steve, Liz, Kate on charter fields | Azmain Hossain | Week of 2026-01-27 | Medium |
| Discuss partner section fields with Alexandre | Azmain Hossain | Week of 2026-01-27 | Medium |
| Add implementation lead field to CLARA | Azmain Hossain | 2026-01-27 | Medium |
| Add MPNS field with employee lookup | Azmain Hossain | TBD | Medium |
| Add adoption charter status (manual dropdown) | Azmain Hossain | TBD | Medium |

## Theme Segments
| Timestamp Range | Theme | Speakers | Tone |
|----------------|-------|----------|------|
| 0:00-5:30 | Personal catch-up: holidays, children, parenting | Steve, Azmain | Warm, relaxed |
| 5:30-10:00 | Context setting: Monday meeting, Sales Recon vision, IRP significance | Azmain | Informative, enthusiastic |
| 10:00-15:00 | Steve's Excel tracker background and consolidation proposal | Steve | Practical, forward-looking |
| 15:00-22:00 | Column-by-column field mapping exercise | Steve, Azmain | Detailed, collaborative |
| 22:00-30:00 | CLARA adoption charter feature demo and Ben's multi-stage design | Azmain | Demo, explanatory |
| 30:00-38:00 | Manual vs algorithmic status indicators discussion | Steve, Azmain | Design-focused, thoughtful |
| 38:00-45:00 | Implementation team fields, partner section, Kate Grove | Steve, Azmain | Cross-functional, planning |
| 45:00-52:00 | Next steps, broader discussion planning, wrap-up | Both | Aligned, energized |

## Power Dynamics
- **Steve Gentilli** came prepared with his Excel tracker and specific column requirements, showing someone who had been independently working on adoption charter process design for months. His proposal to consolidate into CLARA rather than maintain parallel systems was pragmatic and generous — he was willing to abandon his own tool if the central platform served the same purpose.
- **Azmain Hossain** played the role of product manager effectively, validating Steve's requirements against the existing data model in real time and deferring commitments where cross-team discussion was needed. His candour about the platform's limitations (live errors, BenVH dependency) maintained trust.

## Stakeholder Signals
- **Steve Gentilli** — A natural ally for CLARA adoption. His experience building databases and data models in previous roles gave him immediate credibility in discussing schema design. His "input, process, output — start at the end" philosophy aligned with Azmain's approach. His willingness to refine requirements over the weekend showed genuine engagement.
- **Azmain Hossain** — His revelation that George Dyke's account planner also overlapped with CLARA's data model established a pattern: multiple stakeholders building separate tools that could all be served by CLARA's centralized database. His framing of "how many people are going to want to know who's the implementation lead" was persuasive consolidation logic.
- **Ben Brookes** (referenced) — His adoption charter feature design (success criteria, milestones, blueprints, roles) was more ambitious than Steve's current Excel approach, showing long-term product thinking.
- **Alexandre** (referenced) — Needs to be consulted on partner section requirements before fields are finalized.
- **Kate Grove** (referenced) — Added implementation team columns to Steve's tracker; her requirements for downstream implementation tracking need to be captured.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Steve | Refine column document with lookup values | Azmain | High |
| Azmain | Send conversation notes | Steve | High |
| Azmain | Facilitate post-Monday discussion with Ben, Steve, Liz, Kate | Steve | Medium |
| Azmain | Add implementation lead field before Monday | Ben | Medium |

## Meeting Effectiveness
- **Clarity of outcomes:** 8/10 — Clear field-by-field mapping with specific gaps identified
- **Decision quality:** 9/10 — Consolidation decision avoided wasteful parallel development; manual status design was well-reasoned
- **Engagement balance:** 9/10 — Both contributed domain expertise from different perspectives
- **Time efficiency:** 6/10 — Extended personal conversation and demo issues consumed time, though the rapport-building was valuable

## Risk Signals
| Risk | Severity | Signal |
|------|----------|--------|
| Scope expansion through adoption charter consolidation | MEDIUM | Adding 5+ new fields, partner section, implementation team fields, and manual status indicators represents significant scope growth for CLARA. Each field requires schema changes, UI work, and data migration. |
| Multiple stakeholders building parallel tools that need consolidation | HIGH | Steve's Excel tracker, George's account planner, and the golden source spreadsheet all contain overlapping data that is being maintained separately. Consolidation into CLARA is the right direction but the migration effort is substantial. |
| Adoption charter feature untested with real users | MEDIUM | Ben's multi-stage design has not been validated with the people who will actually use it (Steve, Liz, Kate). The field mapping conversation revealed gaps that would have been caught earlier with user involvement. |
| Live demo instability during stakeholder meetings | LOW | Pages failing to load and customers disappearing during Steve's session could have damaged confidence. Azmain's transparency helped, but recurring instability erodes trust. |

## Open Questions Raised
- How will the adoption charter status interact with the sales stage — are these parallel or sequential?
- Should the partner section be part of the adoption charter or a separate module?
- When will Kate Grove's implementation team requirements be captured?
- How will the "IRP active" vs "existing client" distinction work for pipeline accounts that are new to IRP but existing Moody's clients?
- What lookup values does Steve need for the harmonized sales stages?

## Raw Quotes of Note
- "If we had 20 columns, you've already got 15 — so let's just add these 5" — Steve Gentilli, on the consolidation opportunity
- "This whole thing exists because I was lazy — they wanted a 60-page slide deck to give Diya a view of what's happening with migration. I'm like, why? Can't we just build a dashboard?" — Azmain Hossain, on CLARA's origin
- "What output do you want? Start at the end" — Steve Gentilli, on his approach to system design

## Narrative Notes
This was the longest and most substantively productive conversation of Thursday. Steve Gentilli emerged as a key ally — someone with both the domain knowledge of adoption charter processes and the technical understanding to discuss data models intelligently. The column-by-column mapping exercise was exactly the kind of requirement validation that should have happened weeks ago, and the fact that 15 of 20 fields already existed in CLARA validated the platform's data architecture. Steve's manual status indicator proposal was particularly insightful: in a world of varying client complexity, algorithmic determination of "is the adoption charter complete?" would produce more false signals than useful ones. The broader pattern this conversation revealed was that CLARA had become a gravitational centre for disparate data tracking needs across the organisation — Steve's adoption charter, George's account planner, the PMs' service quality tracking, and the golden source migration data all wanted to live in the same place. This convergence was both CLARA's greatest strength and its greatest risk: every consolidation request added complexity to the data model and scope to the development backlog. Azmain's instinct to defer all new fields until after Monday and facilitate a multi-stakeholder discussion was the right governance approach, but the pace of incoming requirements showed no signs of slowing.
