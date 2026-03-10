# AI Licenses Request
**Date:** 2026-01-09
**Attendees:** Richard Dosoo, Azmain Hossain, Divya (Speaker 1 -- AI programme governance, US-based), Megan (Speaker 2 -- works for Divya)
**Duration context:** Short (~13 minutes, transcript ~97 lines)
**Workstreams touched:** WS2 (CLARA -- tooling dependency), WS1 (Training & Enablement -- broader rollout implications)

## Key Points
- Richard escalates the Cursor premium usage limit issue to Divya's team -- the "You hit your usage limit. Go to get cursor Pro" message is blocking development work
- The issue is NOT a budget/credit problem -- Richard's usage dashboard shows $0 of $500 used. It is an entitlement/plan gate on agent mode/advanced features
- Divya and Megan confirm this is the first time they have heard of this specific issue -- it is not Cloud Agents (background agents) which were recently approved
- Richard clarifies the team is using local agent workflows within Cursor, not cloud agents. Thomas (Azmain?) confirms cloud agents are greyed out and unavailable
- Megan sends an email to Michael (Cursor team contact) during the call, copying Richard and Azmain
- Richard raises the broader budget concern: $10,000 across 1,200+ users, with 70 new users being added from their group
- Divya confirms every business unit has made the same budget request -- finance call planned for Monday to determine how to increase the budget
- Divya mentions the Cursor "bump bot" feature is an additional cost that many insurance users want enabled
- Richard asks about Claude/Anthropic enterprise licences. Divya confirms Claude Code is accessible today through AWS (Anthropic/AWS partnership). Dennis Clement on the DCI team can help with setup
- Divya also mentions they are working on an MSA with Anthropic for direct first-party access
- Richard offers to have Diya or other senior leaders support the budget request if needed
- The call is short and productive -- Megan takes immediate action by emailing the Cursor team

## Decisions Made
- Megan to escalate Cursor Pro issue to Michael at Cursor: Divya -> Megan
  - **Type:** explicit
  - **Confidence:** HIGH
- Budget increase discussion happening Monday with finance: Divya confirmed -> Divya
  - **Type:** explicit
  - **Confidence:** MEDIUM
- Claude Code accessible via AWS today -- Richard to contact Dennis Clement: Divya -> Richard
  - **Type:** explicit
  - **Confidence:** HIGH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Email Michael at Cursor about premium limit issue (with screenshots) | Megan | Done during call | Open | HIGH |
| Richard to send notes/screenshots of Cursor Pro issue | Richard | Today | Open | HIGH |
| Budget increase discussion with finance | Divya | Monday | Open | MEDIUM |
| Contact Dennis Clement (DCI team) about Claude Code via AWS | Richard | Next week | Open | MEDIUM |
| Get enterprise Claude/Anthropic licences | Richard/Divya | In progress | Open | LOW |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Cursor Pro entitlement gate | technical | "it's a plan or entitlement gate. It's not really a budget issue" -- Richard | HIGH |
| Cursor budget constraints | operational | "every single business unit" has requested more budget -- Divya | HIGH |
| Claude/Anthropic access | operational | "Claude code, actually, you can access it today through AWS" -- Divya | HIGH |
| Tooling dependency for development | operational | "five members of the team that are kind of critical path... supposed to demo it next week" -- Richard | HIGH |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Richard Dosoo | Issue raiser, escalation driver | Frames the problem clearly, offers senior leadership support for budget | 50% |
| Divya (Speaker 1) | Governance lead, information provider | Provides context on budget process, Claude availability, bump bot | 30% |
| Megan (Speaker 2) | Action taker | Immediately emails Cursor team during call | 10% |
| Azmain Hossain | Clarifier | Confirms cloud agents are disabled, provides technical detail | 10% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Richard Dosoo | frustrated | DOWN | Tooling blockers | "five members of the team that are kind of critical path" |
| Divya | supportive | STABLE | Budget and tooling | "we are 100% in alignment with you. We just need to figure out how to move forward" |
| Megan | supportive | NEW | Immediate action | Emails Cursor team during the call |
| Azmain Hossain | supportive | STABLE | Technical context | Provides clarification on cloud vs local agents |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Megan | Email Cursor team about Pro issue | Done | None | HIGH |
| Divya | Have budget update by next week | Monday finance call | None | MEDIUM |
| Richard | Send screenshots/notes to Megan | Today | None | HIGH |
| Richard | Contact Dennis Clement for Claude via AWS | Next week | None | LOW |

## Meeting Effectiveness
- **Type:** escalation
- **Overall Score:** 80
- **Decision Velocity:** 0.8
- **Action Clarity:** 0.9
- **Engagement Balance:** 0.5
- **Topic Completion:** 0.9
- **Follow Through:** 0.8

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-023 | OPEN | Cursor Pro entitlement gate blocking agent mode for critical path developers | HIGH | ESCALATING | tooling | HIGH |
| R-024 | OPEN | Cursor budget ($10K/1200 users) insufficient -- every BU requesting increase | HIGH | STABLE | financial | HIGH |
| R-027 | OPEN | Finance approval needed for budget increase -- Monday call is critical | MEDIUM | NEW | governance | MEDIUM |

## Open Questions Raised
- Is the Cursor Pro issue a plan configuration error or a genuine feature gate?
- How quickly can Michael at Cursor resolve the issue?
- Will finance approve the budget increase and whose sign-off is needed?
- Can Claude Code via AWS fully substitute for Cursor Pro if the issue persists?

## Raw Quotes of Note
- "I've now hit this issue... I don't know how long for... five members of the team that are kind of critical path at the moment trying to build and deploy this app because we're supposed to demo it next week" -- Richard, on urgency
- "we are very well aware that the limit that we have is just not enough for the size of the group" -- Divya, on budget alignment
- "Claude code, actually, you can access it today through AWS" -- Divya, on Claude availability

## Narrative Notes
A brief but effective escalation meeting. Richard clearly articulates the Cursor Pro issue, Divya immediately confirms alignment on the budget problem, and Megan takes action by emailing the Cursor team during the call. The meeting reveals that the AI tooling budget constraint is not unique to this team -- every business unit at Moody's is hitting the same $10K ceiling. The Claude/Anthropic alternative emerging through AWS is a significant discovery that will become relevant in later weeks.

The underlying tension is that the team is trying to use AI-assisted development tools to build an AI-enabled application, but the enterprise tooling infrastructure is not scaled for intensive use. Richard has five critical-path developers who need to demo CLARA next week, and their primary development tool (Cursor) has locked them out. The contrast between the team's ambition and the enterprise's tooling posture is stark.
