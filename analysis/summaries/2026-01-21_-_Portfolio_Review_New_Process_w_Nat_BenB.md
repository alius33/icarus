# Portfolio Review — New Process with Natalia and Ben Brooks
**Date:** 2026-01-21
**Attendees:** Ben Brooks, Natalia (Plant), Azmain Hossain
**Duration context:** Medium (~32 minutes)
**Workstreams touched:** WS2 CLARA (portfolio review feature, dashboard design)

## Key Points
- Ben Brooks proposed a structured weekly portfolio review meeting built around four pillars: (1) Timeline/Priority by quarter, (2) Action Owners accountability, (3) Knowledge Gaps identification, and (4) Accelerate — pulling forward on-track accounts
- Ben had already prototyped a portfolio review page locally in Cursor using CLARA's codebase (not touching GitHub), showing a quarterly funnel view with discussion points flagged automatically
- Natalia pushed back on creating a separate portfolio review page, arguing that the existing dashboard, customers, and use cases tabs should be used during the meeting to encourage familiarity with the tool
- Compromise reached: the portfolio review page serves as pre-meeting prep (snapshot of what needs discussion), while the actual meeting uses existing app views to walk through specific accounts
- Natalia defined the meeting agenda priorities: always cover high-priority accounts regardless of status, then review all red accounts, then ambers as time allows, never discuss greens
- Agreed on 90-minute global session format, recording for absent attendees, with potential to split into regional sessions later if needed
- Ben raised the vision of multiple views for different personas: CSM view (day-to-day data entry), management portfolio review, solution architect view, executive view — each presenting the same data through different lenses
- Azmain provided input from PMs: they need to know what products underlie each use case, and they noticed small data issues in the live version
- Edit restriction not yet implemented because SSO mapping to person records is incomplete — BenVH being out delayed this
- Audit trail feature exists with visual timeline chart but needs SSO integration to attribute edits to specific users
- Monday meeting plan: short explanation of meeting purpose, describe running agenda, demonstrate tool usage

## Decisions Made
- **Portfolio review page as pre-meeting prep, existing views for actual discussion** (type: design, confidence: high) — Natalia's preference for using existing dashboards during the meeting was accepted as the primary approach
- **Meeting structure: high-priority always, then reds, then ambers, skip greens** (type: process, confidence: high) — Natalia's proposed prioritization was accepted
- **90-minute global session, weekly cadence** (type: process, confidence: high) — starting as a single global meeting covering North America and Europe
- **No live editing during portfolio review meetings** (type: process, confidence: high) — Natalia argued this wastes time and creates unclear ownership of updates
- **Portfolio review page should show quarterly funnel and migration-critical workflows** (type: feature, confidence: medium) — Ben's accelerate and knowledge gap concepts were endorsed

## Action Items
| Action | Owner | Deadline | Confidence |
|--------|-------|----------|------------|
| Send list of meeting agenda priorities and required views to Azmain | Natalia | 2026-01-21 | High |
| Test whether current dashboard can support meeting needs with existing filters | Azmain Hossain | 2026-01-22 | High |
| Conduct dry run of portfolio review meeting format | All three | 2026-01-23 afternoon | High |
| Share priority account list with the team | Natalia | 2026-01-22 | High |
| Add migration-critical workflow tag to use cases | Azmain Hossain | 2026-01-23 | Medium |
| Send screen grabs and specs for portfolio review page | Ben Brooks | 2026-01-22 | Medium |
| Get SSO identity mapping working with BenVH | Azmain Hossain | 2026-01-23 | Medium |

## Theme Segments
| Timestamp Range | Theme | Speakers | Tone |
|----------------|-------|----------|------|
| 0:00-3:30 | Personal banter, Claude/AI tool capabilities | Ben, Azmain | Enthusiastic, awed |
| 3:30-12:00 | Portfolio review structure proposal and Ben's prototype demo | Ben | Strategic, visionary |
| 12:00-20:00 | Natalia's pushback: use existing views, not separate page | Natalia, Ben | Constructive tension |
| 20:00-24:00 | Multi-persona view vision (CSM, management, SA, exec) | Ben | Ambitious, expansive |
| 24:00-28:00 | PM feedback, edit restrictions, audit trail status | Azmain, Ben | Practical, technical |
| 28:00-32:00 | Monday meeting plan, dry run scheduling | Natalia, Ben | Action-oriented |

## Power Dynamics
- **Ben Brooks** came in with a fully prototyped vision and was willing to be redirected by Natalia. His willingness to build something in Cursor overnight showed both initiative and a tendency to lead with artifacts rather than discussion.
- **Natalia** exercised quiet but firm authority. Her pushback on the separate page was grounded in practical adoption concerns (why create a separate view when the dashboard already has the data?). She shaped the final approach more than anyone.
- **Azmain** played connector between the PM feedback he had gathered and the strategic discussion. He mediated effectively between Ben's vision and Natalia's pragmatism.

## Stakeholder Signals
- **Ben Brooks** — Visionary thinking but sometimes ahead of what the team can deliver. His prototype demonstrated capability but also revealed a tendency to build before aligning. His multi-persona view concept (CSM, management, SA, exec) is strategically sound but represents significant scope.
- **Natalia** — Pragmatic, operationally minded, and focused on adoption. Her insistence on using existing tools during meetings rather than creating separate views showed a user-first mindset. Her concern about time efficiency in meetings was well-placed.
- **Azmain** — Showed growing confidence in managing the product direction, pushing back gently on scope while accepting the core requirements. His mention of PM feedback showed he is actively gathering requirements from multiple user groups.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Natalia | Send priority list and meeting agenda requirements | Azmain | High |
| Natalia | Send meeting invitation for 90-minute global session | Team | High |
| Ben | Send screen grabs and specs for portfolio review prototype | Azmain | Medium |
| Azmain | Test current dashboard filters for meeting needs | Ben/Natalia | High |
| All | Conduct dry run Thursday afternoon | Each other | High |

## Meeting Effectiveness
- **Clarity of outcomes:** 8/10 — Clear agreement on meeting structure, page design approach, and Monday plan
- **Decision quality:** 9/10 — The compromise between Ben's prototype and Natalia's existing-view approach was excellent
- **Engagement balance:** 9/10 — All three contributed substantively; healthy disagreement resolved constructively
- **Time efficiency:** 8/10 — Covered significant ground in 32 minutes with minimal tangent

## Risk Signals
| Risk | Severity | Signal |
|------|----------|--------|
| Scope creep on CLARA views before core data quality is addressed | MEDIUM | Ben's multi-persona vision (CSM, management, SA, exec views) is compelling but each view is significant development work. Risk of building dashboards before the underlying data is reliable. |
| Portfolio review meeting fatigue | LOW | 90-minute weekly meeting with potentially 50 people could become unproductive if not tightly managed. Natalia's structure mitigates this but enforcement will be key. |
| SSO integration blocking edit accountability | MEDIUM | Without SSO mapping, audit trails cannot attribute edits to specific users, and edit restrictions cannot be enforced. This is a trust issue with early adopters. |

## Open Questions Raised
- How will the quarterly funnel view coexist with the existing dashboard?
- Should the portfolio review page show data that is not already available elsewhere?
- How will solution architects be brought into the CLARA ecosystem given their separate tracking spreadsheets?
- When will SSO identity mapping be complete so edit restrictions can be enforced?
- Will the Monday meeting be sufficient to get CSMs started, or will additional training be needed?

## Raw Quotes of Note
- "I'm not saying no to this, because that's maybe structuring exactly how we should have a conversation. But I feel that maybe from the better usability of the tracker, it would be easier to use the existing dashboard" — Natalia, on the portfolio review page
- "I wrote that whole of that IRP tracker in Auto... it wouldn't do us a disservice to rebuild the front end fairly soon" — Ben Brooks (referenced from the Account Planner call, consistent theme)

## Narrative Notes
This meeting was the most productive design conversation of Week 3. The constructive tension between Ben's prototype-first approach and Natalia's existing-view pragmatism produced a superior outcome: a prep-focused portfolio review page that complements rather than duplicates the main dashboard. Natalia's influence on the meeting structure was decisive and well-judged — her insistence on always covering priority accounts, never discussing greens, and avoiding live edits during meetings will be critical for keeping the weekly reviews efficient. Ben's multi-persona view concept, while ambitious, planted a seed for CLARA's evolution from a data entry tool to a collaboration platform. The fact that Ben could prototype a page overnight in Cursor underscored both the speed of AI-assisted development and the governance challenge it creates: anyone with Cursor access can build features faster than the team can review and integrate them. This tension between speed and coordination will be a recurring theme as the programme scales.
