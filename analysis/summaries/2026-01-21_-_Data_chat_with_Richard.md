# Data Chat with Richard
**Date:** 2026-01-21
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (briefly, in person)
**Duration context:** Long (~52 minutes, in-office session)
**Workstreams touched:** WS2 CLARA (infrastructure, data), WS1 Training, WS6 Build in Five

## Key Points
- In-office working session covering deployment safety, tech debt, training programme strategy, AWS access, and employee data needs
- 219 deployments and 105 commits from a tiny team — Richard noted this output level normally requires much larger teams, reflecting both achievement and risk
- Critical data safety discussion: once CSMs start entering production data, every schema change must ship with a data fix script via Alembic migrations. The team cannot just add tables/columns without priming them with data.
- Richard explained the VPC architecture: the database is inside a private network, accessible only via API or through Alembic scripts that run inside the VPC during deployment. No direct database access exists for the team.
- Azmain raised the recurring Alembic "multiple migration heads detected" error — Cursor had auto-fixed it previously but the root cause was unclear
- Training programme strategy discussion: Richard proposed tying training to OKRs and KPIs rather than delivering generic training. The approach would be: identify Diya's org objectives, map job roles to those objectives, determine which AI capabilities support each role, then design targeted training per persona.
- Richard planned to get Stephanie's employee list (everyone in Diya's org) and use it to inform both the training programme and CLARA's people directory
- Azmain identified that CLARA needs employee data beyond just Diya's direct reports — anyone who could be assigned to projects or accounts needs to be in the system
- Richard formally invited Azmain to the tech consultant Teams channel and initiated an AWS access request (ServiceNow ticket)
- Brief appearances from BenVH in person (confirming he would be in the office Thursday/Friday)
- Extended personal conversations about: work-life balance (Azmain's daughter), recording meetings covertly, the workflow pain of transcript processing (watch to phone to Otter to Claude)

## Decisions Made
- **Every schema change must include a data fix script** (type: process, confidence: high) — critical for data integrity once users are entering production data
- **Weekly production deployments only** (type: process, confidence: high) — dev environment can have frequent deploys, but prod should be gated to once per week
- **Training programme to be OKR-driven, not generic** (type: strategic, confidence: high) — tie every training track to specific business objectives and job personas
- **Use Stephanie's employee list as basis for CLARA people directory** (type: data, confidence: high) — get the source endpoint, not just a static export
- **Raise AWS access request for Azmain** (type: administrative, confidence: high) — ServiceNow ticket submitted

## Action Items
| Action | Owner | Deadline | Confidence |
|--------|-------|----------|------------|
| Start a thread with Stephanie to get employee data source/endpoint | Richard Dosoo | 2026-01-22 | High |
| Submit AWS access request via ServiceNow for Azmain | Richard Dosoo | 2026-01-21 | High |
| Get developer laptops approved (check with Diya) | Richard Dosoo | 2026-01-22 | Medium |
| Investigate and fix the Alembic multiple migration heads issue | Azmain Hossain | TBD | Medium |
| Map Diya's OKRs to training needs and job personas | Richard/Azmain | 2026-01-24 | Medium |
| Get Diya's full org employee list with job types | Richard Dosoo | 2026-01-22 | High |
| Document the transcript processing workflow for automation | Azmain Hossain | TBD | Low |
| Attend meeting with Bernard/Alexandra re: Life team demos | Richard/Azmain | 2026-01-22 | High |

## Theme Segments
| Timestamp Range | Theme | Speakers | Tone |
|----------------|-------|----------|------|
| 0:00-2:00 | Cost discussion (POC scoping) and commercial context | Richard, Speaker 1 | Business, practical |
| 2:00-7:00 | Alembic migration issues and tech debt concerns | Richard, Azmain | Anxious, reflective |
| 7:00-12:00 | Data safety: schema changes must include data fixes | Richard | Urgent, instructional |
| 12:00-19:00 | Deployment frequency, VPC architecture, AWS access request | Richard, Azmain | Technical, administrative |
| 19:00-25:00 | Work-life balance, Azmain's daughter, leaving office | Both | Personal, warm |
| 25:00-35:00 | Cursor/AI tool management, recording meetings workflow | Both | Frustrated, creative |
| 35:00-52:00 | Training programme strategy: OKR-driven approach, employee data | Richard | Strategic, energized |

## Power Dynamics
- **Richard** was in full mentoring/operations lead mode, covering infrastructure, governance, training strategy, and administrative tasks. He demonstrated both strategic thinking (OKR-driven training) and operational attention to detail (data fix scripts, VPC architecture).
- **Azmain** shifted between technical contributor (Alembic issues, app features) and programme analyst (training strategy, employee data needs). His frustration with the manual transcript processing workflow was a window into his daily operational burden.

## Stakeholder Signals
- **Richard Dosoo** — Showed the breadth of his responsibilities: commercial scoping, infrastructure governance, training strategy, administrative access, and Cursor licensing. The weight of these simultaneous concerns is visible.
- **Azmain Hossain** — His comment about "context switching between programme level conversations and debug level conversations makes your brain hurt" was a direct expression of cognitive overload. His recording workflow (watch to phone to Otter to Claude) revealed how much manual effort goes into maintaining programme context.
- **BenVH** — Briefly present in office; confirmed availability Thursday/Friday. His physical presence (rather than remote from Amsterdam) was reassuring.
- **Stephanie** — Referenced as the holder of employee data from Salesforce. A key data source for both the training programme and CLARA.
- **Diya Sawhny** — Referenced as the approver for developer laptops and the person whose OKRs will drive the training programme.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Richard | Submit AWS access ServiceNow ticket | Azmain | High |
| Richard | Start thread with Stephanie for employee data | Azmain | High |
| Richard | Get developer laptops approved | Azmain | Medium |
| Azmain | Investigate Alembic migration issues | Richard | Medium |
| Both | Map OKRs to training agenda | Diya (indirectly) | Medium |

## Meeting Effectiveness
- **Clarity of outcomes:** 7/10 — Good coverage of multiple topics with clear action items on each
- **Decision quality:** 8/10 — The data safety and deployment governance decisions were sound and important
- **Engagement balance:** 7/10 — Genuine back-and-forth, though Richard drove most strategic points
- **Time efficiency:** 5/10 — Covered many topics but with significant tangential discussion

## Risk Signals
| Risk | Severity | Signal |
|------|----------|--------|
| Tech debt accumulation from rapid development | HIGH | Richard explicitly noted the magnitude of change vs. testing done: "all the time... you can only do that for so long before it catches you up." 219 deployments with minimal testing. |
| Alembic migration instability | HIGH | "Multiple migration heads detected" error not root-caused. If migration scripts fail silently, schema changes will continue to cause deployment issues. |
| Azmain's cognitive overload | MEDIUM | Context switching between programme management and debugging, combined with manual transcript processing, is unsustainable. |
| No direct database access for the dev team | MEDIUM | The VPC architecture means all database interactions must go through Alembic or API calls. This makes debugging and data fixes cumbersome. |
| Employee data scope uncertainty | MEDIUM | Azmain needs everyone under Colin Holmes in the system, but the current data only covers Diya's direct org. Scope expansion could be complex. |

## Open Questions Raised
- Where does Stephanie get the employee data — Salesforce, HR system, or manual compilation?
- Can the team get the API endpoint rather than a static export?
- What are Diya's specific OKRs for 2026 that would drive the training programme?
- How should the training programme handle non-advisory teams (ILS, SAT) that may also benefit?
- Can Azmain's transcript processing workflow be automated using available APIs?

## Raw Quotes of Note
- "The magnitude of change that we're doing, the amount of testing we should be doing, oh my god, we haven't... you can only do that for so long before it catches you up" — Richard Dosoo, on tech debt risk
- "Context switching between programme level conversations and debug level conversations makes your brain hurt" — Azmain Hossain, on cognitive load
- "We gave everyone the tooling and didn't give them the process" — Richard Dosoo, on the training programme's approach

## Narrative Notes
This in-office session was the most operationally rich conversation of Week 3. The data safety discussion marked a maturity inflection point: Richard's insistence on data fix scripts accompanying every schema change represented the team formally acknowledging that CLARA had crossed from prototype to production system. The training programme strategy was equally significant — tying training to OKRs rather than delivering generic AI literacy is the kind of structured thinking that Diya's organisation needs to see to take the programme seriously. But the underlying tension remained: the team was simultaneously trying to stabilize infrastructure, prepare for a Monday exec demo, design a training programme, and manage daily programme communications, all with essentially two people (Richard and Azmain) carrying the entire load. Richard's observation that they had done the work of a much larger team was both pride and warning. The manual transcript processing workflow that Azmain described (recording on a watch, transferring to phone, uploading to Otter, processing through Claude) is a perfect microcosm of the programme's broader challenge: brilliant people doing impressive work through sheer manual effort, without the supporting systems that would make it sustainable.
