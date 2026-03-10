# Chat with Ben B -- Feature Planning and Whiteboard Review
**Date:** 2026-01-14
**Attendees:** Ben Brooks, Azmain Hossain, Richard Dosoo (partial)
**Duration context:** medium (~4000 words)
**Workstreams touched:** WS2 (CLARA/Adoption Tracker)

## Key Points
- Ben Brooks walks through a whiteboard/to-do list of feature priorities for CLARA in a Teams channel
- Key priorities identified: (1) user context -- app must know who is logged in and what teams they belong to, (2) edit permissions -- only team members on a project can edit it, (3) admin accounts for Ben/Richard
- Salesforce as source of truth debate: Ben clarifies data flows OUT of CLARA to Salesforce, not the other way; manual download once a week could work initially
- Ben senses Josh, Catherine, and Chanel gradually saying "Salesforce doesn't work, should we just give up?" -- considers this ideal for CLARA adoption
- Dashboard needs revamp -- current version is too plain; Ben had Opus improve it with one prompt
- Ben shares the story that triggered urgency: Mike Steele got an email saying a client (Travellers) was upset, but nobody had surfaced this proactively -- exactly the problem CLARA solves
- Team members mapping is the critical prerequisite for many other features (user context, permissions, personalised dashboards)
- Migration critical workflow flag needed per account -- Diya wants to see progress on this
- HD (High Definition models) flags needed at use case level to track whether HD is in production for a given use case
- Ben reveals HD adoption data is poor: they think the market is using HD when they may not be in production at all
- Action plan creation needs to be easier and more intuitive with help guidance
- Natalia already asking "when's this going to be deployed and we can use it?" -- stakeholder impatience growing
- Azmain shows his local build improvements: table view for all customers (replacing tab-based layout), pagination, pop-up modals for CRUD operations, click-to-expand functionality

## Decisions Made
- **Data flows FROM CLARA to Salesforce, not reverse**: CLARA is the system of record for migration tracking -> Ben Brooks
  - **Type:** explicit
  - **Confidence:** HIGH
- **Team members mapping is top priority**: Must be done before user context, permissions, or personalised views -> Ben Brooks
  - **Type:** explicit
  - **Confidence:** HIGH
- **HD flags at use case level**: Track whether HD models are in production per use case -> Ben Brooks
  - **Type:** explicit
  - **Confidence:** HIGH
- **Table view replaces tab-based customer layout**: Azmain's redesign accepted -> Azmain/Ben
  - **Type:** implicit
  - **Confidence:** HIGH
- **Meet with Natalia/Catherine/Kevin before major schema changes**: Align data model with Gainsight integration plans -> Richard
  - **Type:** explicit
  - **Confidence:** MEDIUM

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Add team members mapping functionality | Azmain | 2026-01-17 | Open | HIGH |
| Add migration critical flag per account | Azmain | 2026-01-17 | Open | HIGH |
| Add HD enabled flag per use case | Azmain | 2026-01-17 | Open | MEDIUM |
| Convert customer view from tabs to table with pagination | Azmain | 2026-01-15 | Complete | HIGH |
| Get CSMs to update migration criticality data | Azmain | 2026-01-20 | Open | MEDIUM |
| Schedule alignment call with Natalia/Catherine/Kevin on data model | Richard | 2026-01-20 | Open | MEDIUM |
| Add updates/audit trail functionality to blockers and action plans | Azmain | 2026-01-24 | Open | MEDIUM |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| User context and permissions | technical | "this thing is not currently wired in to know who's on what teams" -- Ben Brooks | HIGH |
| Salesforce relationship | strategic | "Josh and Catherine and Chanel gradually say, okay, clearly Salesforce doesn't work" -- Ben Brooks | HIGH |
| HD adoption visibility gap | operational | "until we show the fact that nobody's actually using it in production... we won't do anything about the problem" -- Ben Brooks | HIGH |
| Travellers incident | interpersonal | "Mike Steele saying, Gary Nelson at Travellers is really pissed off. What's going on?" -- Ben Brooks | HIGH |
| Version control and audit trail | technical | "that's really important that we know when things are changed, who changed them" -- Azmain referencing Ben's requirement | MEDIUM |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Ben Brooks | Product owner, vision setter | Defining feature priorities, sharing the Travellers story to motivate, praising Opus | 45% |
| Azmain Hossain | Builder, showing progress | Demonstrating local build improvements, proposing UX solutions | 40% |
| Richard Dosoo | Connector, strategic thinker | Brief appearances, proposing Gainsight alignment meeting | 15% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Ben Brooks | Urgent, visionary | Escalating urgency | Demo readiness | Travellers incident shows exactly why CLARA is needed NOW |
| Azmain | Productive, growing confidence | Positive shift | Development velocity | Completed table view, pagination, pop-up modals |
| Natalia (ref) | Impatient | Escalating | Deployment timeline | "when's this going to be deployed?" |
| Josh/Catherine/Chanel (ref) | Moving away from Salesforce | Gradual shift | Tool preference | Signals openness to CLARA replacing Salesforce for this use case |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Azmain | Will add team members mapping | Before Tuesday demo | None | HIGH |
| Azmain | Will add migration critical flag | Before Tuesday demo | Someone provides data | MEDIUM |
| Richard | Will schedule Gainsight alignment meeting | Next week | None | MEDIUM |
| Ben Brooks | Will provide Valpers cultural commitments terminology for app | TBD | None | LOW |

## Meeting Effectiveness
- **Type:** Feature planning / build review
- **Overall Score:** 82
- **Decision Velocity:** 0.8
- **Action Clarity:** 0.7
- **Engagement Balance:** 0.7
- **Topic Completion:** 0.6
- **Follow Through:** 0.6

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-027 | New | HD adoption data fundamentally unreliable -- production usage unknown | HIGH | Stable | Data Quality | HIGH |
| R-028 | New | Natalia impatient for deployment -- expectation management needed | MEDIUM | Escalating | Stakeholder | HIGH |
| R-029 | New | Schema changes before Gainsight alignment could create integration debt | MEDIUM | Stable | Technical | MEDIUM |

## Open Questions Raised
- Should updates/version control be hierarchical (nested under parent) or flat table with foreign keys?
- When will the alignment meeting with Natalia/Catherine/Kevin happen?
- Who specifically will fill in migration criticality data for each account?
- How to reconcile CLARA's data model with Gainsight's schema before major changes?

## Raw Quotes of Note
- "until we show the fact that nobody's actually using it in production because everybody's bloody blocked, we won't do anything about the problem" -- Ben Brooks, on HD visibility gap
- "Mike Steele saying, Gary Nelson at Travellers is really pissed off. What's going on?" -- Ben Brooks, on why CLARA matters
- "Opus... it saved me so much time not having to make a separate plan than a separate build" -- Azmain, praising the model
- "I'm telling you, man, we are screwed. This is way too good" -- Azmain, on AI capabilities

## Narrative Notes
This is one of the most product-strategically significant meetings of the week. Ben Brooks's Travellers anecdote -- Mike Steele blindsided by client frustration because nobody surfaced it proactively -- perfectly encapsulates the CLARA value proposition. The HD visibility gap is a politically explosive finding: if the team can show that HD adoption in production is far lower than assumed, it forces product and leadership attention on a real problem. Ben's observation that Josh and others are "gradually saying Salesforce doesn't work" represents a potential inflection point -- if CLARA can capture that disillusionment and redirect it into active data entry in the new tool, adoption could accelerate. Azmain's growing velocity with Opus is notable: converting the entire customer view from tabs to tables with pagination in a short session shows the development approach is working. The tension between moving fast (Natalia wants deployment now) and aligning the data model with Gainsight (Richard's concern about integration debt) is a genuine strategic trade-off that hasn't been resolved.
