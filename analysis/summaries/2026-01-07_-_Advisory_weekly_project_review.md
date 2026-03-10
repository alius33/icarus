# Advisory Weekly Project Review
**Date:** 2026-01-07
**Attendees:** Diana (chair), Billy (Speaker 1), Prashant (Speaker 2), Casey/Kate (Speaker 3), Stacy (Speaker 5), Amit, Emily (Speaker 6), Azmain Hossain, and others
**Duration context:** Medium (~24 minutes, transcript ~163 lines)
**Workstreams touched:** None directly -- Advisory team project portfolio review providing context on the broader consulting operation

## Key Points
- Routine weekly advisory project review covering client delivery projects, not directly about the Gen AI programme
- True project (Billy): development progressed from 10% to 25%, on track, Amber status due to an internal Moody's functionality issue expected to resolve by mid-next week
- Morgan Stanley (Prashant): targeting stochastic milestone delivery by Jan 21, hit timeout issues in Cat Accelerate (fix applied), portfolio model runs completed QA, state/country/location model runs still in progress, work order amendment with Morgan's legal
- Golden Bear (Casey): UAT support calls planned Jan 14 through Mar 18. Surprise: Golden Bear's legal team sent follow-up email Dec 29 reiterating demands -- now with Moody's legal team
- Aspen: deployed to production Dec 19, UAT in progress, key sign-off person out until Jan 15
- AXA (Casey): three new high-priority defects found, resource shift from Suma to Ye (stretched across projects), project end date likely to slip to mid-late January
- AXA Safeguarding: both workshops completed, weekly support calls underway, targeting end of January wrap-up, client accepted revised scope/fee
- GCNC Underwriting IQ: API support on track (week 3), concern about Capgemini resource capacity for March deadline
- Patron/Atrium: changed to RED -- second workshop outstanding with no clear focus, QuickStart expired end of December
- Survey Monkey: access partially restored but old surveys/data not migrated to new Moody's account
- Several projects completed: Acorn, Life, Big Green China

## Decisions Made
- Skip January monthly report; run report on Jan 17 or 20 instead: Stacy/team -> Stacy
  - **Type:** explicit
  - **Confidence:** HIGH
- Add target migration date field to monthly status template: Stacy -> Stacy
  - **Type:** explicit
  - **Confidence:** HIGH
- Patron/Atrium: discuss with Martin on today's tech standup before next steps: Stacy -> Stacy
  - **Type:** deferred
  - **Confidence:** MEDIUM

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Check Aspen environment for actual testing activity | Emily | Today | Open | HIGH |
| Talk to Martin about Patron/Atrium on tech standup | Stacy | Today | Open | HIGH |
| Chase Survey Monkey for data migration | Stacy | Ongoing | Open | LOW |
| Update AXA project end date based on Ye availability | Casey | Next week | Open | MEDIUM |
| Touch base with Amit/Brian on AXA safeguarding status | Casey | This week | Open | HIGH |
| Run adoption status report for Jan 20 | Stacy | Jan 20 | Open | HIGH |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Client delivery portfolio status | operational | N/A -- structured status updates | HIGH |
| Resource constraints | operational | "Suma has transitioned to other projects" -- Casey | HIGH |
| Legal risk (Golden Bear) | governance | "received a bit of a surprise when an email was forwarded to us by sales" -- Casey | HIGH |
| Data infrastructure gaps | operational | "I still don't have access to all of our surveys and all of our results" -- Stacy | MEDIUM |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Diana | Chair, time keeper | Drives through agenda, asks clarifying questions | 25% |
| Casey (Speaker 3) | Multi-project lead | Reports on Golden Bear, AXA, AXA Safeguarding | 25% |
| Stacy | Reporting/data backbone | Manages reporting cadence, data access, multiple project admin | 25% |
| Prashant | Project lead | Morgan Stanley status | 10% |
| Amit | Technical support | Safeguarding workshop input | 5% |
| Others | Various | Brief contributions | 10% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Diana | neutral | STABLE | Portfolio oversight | Standard facilitation |
| Stacy | frustrated | STABLE | Reporting burden and data access | Chasing Survey Monkey, managing multiple data streams |
| Casey | cautious | STABLE | Client risk management | Proactively flagging defects, legal issues, resource gaps |
| Prashant | supportive | STABLE | Morgan Stanley delivery | Optimistic despite timeout setback |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Emily | Check Aspen testing environment | Today | None | HIGH |
| Stacy | Discuss Patron/Atrium with Martin | Today | None | HIGH |
| Casey | Update AXA project end date | Next weekly call | After Ye availability assessment | MEDIUM |
| Stacy | Send updated reporting assignments | This week | None | HIGH |

## Meeting Effectiveness
- **Type:** status_update
- **Overall Score:** 68
- **Decision Velocity:** 0.4
- **Action Clarity:** 0.6
- **Engagement Balance:** 0.6
- **Topic Completion:** 0.8
- **Follow Through:** 0.5

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-010 | OPEN | Golden Bear legal escalation -- surprise Dec 29 demand | MEDIUM | NEW | legal | HIGH |
| R-011 | OPEN | AXA resource gap -- Suma left, Ye spread across projects | MEDIUM | NEW | resource | HIGH |
| R-012 | OPEN | Patron/Atrium QuickStart expired, unclear client direction | LOW | ESCALATING | client | MEDIUM |
| R-013 | OPEN | GCNC Capgemini resource capacity for March deadline | LOW | NEW | vendor | LOW |

## Open Questions Raised
- What to do about Patron/Atrium given expired QuickStart?
- Will Morgan Stanley state/country/location model runs complete for Jan 21 milestone?
- Could AXA UAT uncover more defects beyond the current three?

## Raw Quotes of Note
- "received a bit of a surprise when an email was forwarded to us by sales on December 29 in which Golden Bear's legal team sent a follow up email reiterating their demands" -- Casey, on legal risk
- "it's called Quick Start for a reason. It's to get people started, not to drag on forever" -- Stacy, on Patron/Atrium

## Narrative Notes
This advisory review provides essential context for the Gen AI programme's resource environment. The same people Richard needs for CLARA development (Martin, Stacy) are tied up in client delivery across True, Morgan Stanley, Golden Bear, Aspen, AXA, GCNC, and Patron/Atrium. Stacy, who maintains the 300-slide account status deck that CLARA aims to replace, is simultaneously managing monthly reporting cadence changes, Survey Monkey migrations, and data quality chases. This meeting demonstrates exactly why CLARA is needed (manual process burden) and why building it is hard (the people who understand the domain are already fully committed to client work).
