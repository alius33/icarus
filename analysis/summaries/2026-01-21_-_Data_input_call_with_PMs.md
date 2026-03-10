# Data Input Call with PMs
**Date:** 2026-01-21
**Attendees:** Azmain Hossain, Vlad (PM), Diana (PM), one other PM (Speaker 1/2)
**Duration context:** Medium (~29 minutes)
**Workstreams touched:** WS2 CLARA (data quality, user onboarding)

## Key Points
- Azmain walked the PMs through CLARA's new data input hub — a purpose-built page for CSM data entry that replaces the planned Excel-based approach
- The data input hub shows completeness percentages per account, flags missing fields, and allows in-line editing of use cases, blockers, and action plans across all accounts
- 155 active accounts loaded from the December golden source spreadsheet; inactive accounts excluded
- Critical data needs identified: (1) Which accounts are priority, (2) Within priority accounts what fields are most critical, (3) CSM assignments for each account
- Azmain manually added all people from Diya's org using the Moody's people directory — anyone assigned to projects must come from this list
- The PMs' role is facilitator, not data owner: they sit with CSMs, walk through accounts, demonstrate the tool, and create social pressure for data entry
- Diana raised PM-specific needs: tracking service delivery quality, project commitments, and distinguishing between customer-led and Moody's-led implementations. Azmain acknowledged these are needed but deferred to after the CSM-focused push.
- Vlad offered to start immediately with 3 accounts he manages directly (Mafra, Star, AIG) as a test
- Export functionality intentionally omitted to prevent users from downloading to Excel and abandoning the platform
- Audit trail functionality exists: every edit records who changed what and when

## Decisions Made
- **PMs to facilitate CSM data entry, not own the data themselves** (type: process, confidence: high) — CSMs are responsible for accuracy; PMs coordinate sessions and flag gaps
- **Defer PM-specific features to later phase** (type: prioritization, confidence: high) — PM views for project tracking and service quality are acknowledged but not built yet
- **No export functionality by design** (type: strategic, confidence: high) — prevents users from reverting to Excel-based workflows
- **Critical accounts and priority fields to be defined by Ben Brooks** (type: governance, confidence: high) — expected by end of day 2026-01-21
- **Vlad to test with 3 known accounts immediately** (type: tactical, confidence: high) — provides early validation that data persists correctly

## Action Items
| Action | Owner | Deadline | Confidence |
|--------|-------|----------|------------|
| Meet with Ben Brooks to identify critical/priority accounts | Azmain Hossain | 2026-01-21 EOD | High |
| Confirm deadline for data entry exercise with Natalia/Ben | Azmain Hossain | 2026-01-21 EOD | High |
| Share critical account list and priority field requirements with PMs | Azmain Hossain | 2026-01-22 | High |
| Test data entry on Mafra/Star/AIG accounts | Vlad | 2026-01-21 | High |
| Edit a health status field and verify data persists | Vlad | 2026-01-21 | High |
| Fix region field (should be dropdown, not free text) | Azmain Hossain | TBD | Medium |
| Fix blocker owner field (should be people lookup, not free text) | Azmain Hossain | TBD | Medium |
| Start collecting PM-specific requirements for future phase | Diana | TBD | Low |

## Theme Segments
| Timestamp Range | Theme | Speakers | Tone |
|----------------|-------|----------|------|
| 0:00-5:00 | Data input hub walkthrough and purpose | Azmain | Demo, enthusiastic |
| 5:00-10:00 | Scope: which accounts, how many, timeline questions | Vlad, Azmain | Practical, questioning |
| 10:00-14:00 | CSM assignment process and data source questions | Speaker 1, Azmain | Detailed, process-oriented |
| 14:00-20:00 | Diana's PM-specific needs: service quality, delivery tracking | Diana, Azmain | Exploratory, slightly frustrated |
| 20:00-25:00 | Blocker types, action plans, and feedback mechanisms | Azmain, Diana | Collaborative |
| 25:00-29:00 | Vlad's immediate test plan and availability discussion | Vlad, Azmain | Action-oriented |

## Power Dynamics
- **Azmain** ran the session with confidence, demonstrating the tool and fielding questions effectively. He managed expectations well (deferring PM features, being honest about gaps).
- **Vlad** was the most engaged questioner — practical, deadline-focused, and immediately offered to test. His questions about CSM availability and escalation paths showed operational maturity.
- **Diana** brought the PM perspective that the tool does not yet serve. Her questions about service delivery quality and project tracking were important signals of unmet needs, and she accepted the deferral gracefully.
- **Speaker 1/2** (unidentified PM) asked relevant but fewer questions about data backup and export.

## Stakeholder Signals
- **Vlad** — Proactive and willing to start immediately. His direct management of 3 accounts makes him a natural early tester. His question about CSM availability showed awareness of the human bottleneck.
- **Diana** — Slightly frustrated that the tool does not yet support PM workflows, but professional about it. Her needs (project tracking, service quality monitoring, distinguishing customer-led vs Moody's-led work) represent a real feature gap that will need addressing.
- **Azmain** — Showed product ownership maturity by deferring PM features rather than promising them. His awareness of the blocker type categorization (client, product, sales, etc.) showed he has thought about reporting needs.
- **Ben Brooks** (referenced) — His directive that "buy-in is not optional" for CSMs sets the tone. He is the authority figure whose prioritization decisions will determine the data entry push scope.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Azmain | Define critical accounts and priority fields by EOD | PMs | High |
| Azmain | Confirm data entry deadline | PMs | High |
| Vlad | Test with 3 known accounts immediately | Azmain | High |
| Vlad | Edit a health status field as persistence test | Azmain | High |
| Diana | Start collecting PM-specific requirements | Self/Azmain | Low |

## Meeting Effectiveness
- **Clarity of outcomes:** 8/10 — Clear roles, clear next steps, clear timeline for getting started
- **Decision quality:** 8/10 — Good balance of pragmatism (start now with what we have) and governance (wait for Ben's priority list)
- **Engagement balance:** 8/10 — All PMs participated actively with substantive questions
- **Time efficiency:** 8/10 — Covered all necessary ground within 29 minutes

## Risk Signals
| Risk | Severity | Signal |
|------|----------|--------|
| CSM adoption resistance | MEDIUM | Vlad asked whether CSMs were informed and willing. Azmain confirmed they have been briefed but acknowledged the real challenge is getting them to actually do the data entry. |
| Data quality from golden source import | MEDIUM | The December golden source data is acknowledged as potentially inaccurate. CSMs will need to verify and correct during sessions. |
| PM frustration with tool not serving their needs | LOW | Diana's questions about PM-specific features signal unmet expectations. Continued deferral could erode PM engagement in the data entry exercise. |
| Free text fields creating inconsistent data | LOW | Region and blocker owner are currently free text when they should be constrained dropdowns. Small data quality issue that compounds at scale. |

## Open Questions Raised
- How many of the 155 active accounts will be tagged as critical/priority by Ben Brooks?
- What is the realistic deadline for the initial data entry push — end of January or later?
- How will CSM managers (Josh Ellingson, George Dyke) be involved in the assignment confirmation process?
- When will PM-specific features (project tracking, service quality) be built into CLARA?
- Should there be a "light" version of the data entry for small/low-priority accounts?

## Raw Quotes of Note
- "Buy-in is not optional. This is what they have to do." — Azmain Hossain, quoting Ben Brooks on CSM adoption
- "The thinking is also to change people's behaviour, because if you can export something into Excel, they're just going to do that" — Azmain Hossain, on the deliberate omission of export functionality

## Narrative Notes
This was one of the most operationally effective meetings in Week 3. Azmain demonstrated genuine product management skills: showing the tool, managing expectations, deferring features that were not ready, and creating a clear action plan for the data entry push. The data input hub concept — replacing a painful Excel exercise with an in-app guided workflow — shows the kind of user-centric thinking that could drive real adoption. The deliberate omission of export functionality was a particularly shrewd decision, forcing a behavioral shift away from the Excel-centric culture that has historically undermined data consistency. Diana's PM-specific needs represent the next major feature frontier, and how quickly these are addressed will determine whether PMs remain engaged allies or drift into frustrated observers. Vlad's immediate willingness to test with real accounts is the best kind of validation — someone who sees the tool and wants to use it right now.
