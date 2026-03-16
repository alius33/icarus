# Adoption Tracker - Deployment to AWS
**Date:** 2026-01-08
**Attendees:** Richard Dosoo, Ben Brookes, Azmain Hossain, BenVH (Speaker 3, referenced for deployment)
**Duration context:** Long (~50 minutes, transcript ~466 lines)
**Workstreams touched:** WS2 (CLARA/IRP Adoption Tracker), WS4 (Adoption Charter -- data model for charters, blueprints, acceptance criteria discussed)

**Note:** This transcript is identical to "Chat with Ben Rich" from the same date -- same meeting recorded under two names.

## Key Points
- Deep technical session focused on data model design and AWS deployment planning
- Azmain asks key question: if using DynamoDB on AWS, does the data structure need flattening? Richard says no -- they can use SQL Server on AWS via RDS for minimal changes
- AWS deployment confirmed as demo-only: "just to shop it around, show it to people, get feedback"
- Richard proposes checking with MAP (Moody's Analytics Platform) team as the strategy is changing -- may support non-production workflows now
- Richard wants to reconcile Azmain's existing dashboard work with Ben's expanded prototype -- the delta needs identifying
- Ben clarifies the priority hierarchy: data model and data collection first, dashboard is the output/result layer built on top
- Detailed data model discussion: new tables for projects, project imports, tasks, adoption milestones, customer adoption milestones
- Richard proposes database views as an abstraction layer: build reports against views so underlying schema changes do not break dashboards
- Acceptance criteria debate: Ben argues for use case level AND account level criteria. Resolution: one table with a column denoting the level (use case vs adoption/account), functioning as two logical tables
- Decision to defer blueprints and partner tracking to phase two
- Richard plans to use Amazon RDS for SQL Server, host in Fargate VMs, use CloudWatch for logging
- Ben needs to push his latest code to GitHub main branch so Richard/Azmain can create a new branch with updated data model
- Ben notes Azmain should build the first report: a pipeline report by quarter and adoption status, then detailed per-client views
- Ben envisions weekly Monday pipeline review meetings (Europe + US) with structured account review
- Azmain expresses uncertainty about refactoring Ben's expanded codebase: "I still don't fully understand everything Ben's built"
- Richard plans to walk Azmain through the development process as a learning exercise
- Timeline pressure: Richard wants data model, sample data, and AWS deployment done today or tomorrow -- time-boxed approach
- Richard mentions using ChatGPT for data model work but hitting performance issues with long context windows
- Richard seeking Claude/Anthropic enterprise licences (costs $40/month) as better coding tool -- Divya was supposed to provide access pre-holiday

## Decisions Made
- Use SQL Server on AWS via RDS to minimise changes: Richard -> Richard
  - **Type:** explicit
  - **Confidence:** HIGH
- Data model priority: get schema up first, populate with data later: Richard/Azmain -> Azmain
  - **Type:** explicit
  - **Confidence:** HIGH
- Acceptance criteria at use case level AND account level via single table with level column: Richard/Ben -> Richard
  - **Type:** explicit
  - **Confidence:** HIGH
- Defer blueprints and partner management to phase two: Ben agreed, Richard -> team
  - **Type:** explicit
  - **Confidence:** HIGH
- Database views as abstraction layer for dashboards: Richard -> Richard
  - **Type:** explicit
  - **Confidence:** HIGH
- First report to build: pipeline by quarter and adoption status: Richard -> Azmain
  - **Type:** explicit
  - **Confidence:** HIGH
- Weekly Monday pipeline review meetings (Europe + US): Ben -> Ben
  - **Type:** explicit
  - **Confidence:** MEDIUM

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Push latest code to GitHub main | Ben Brookes | Today | Open | HIGH |
| Create new branch with updated data model | Richard/Azmain | Today | Open | HIGH |
| Map golden source data to new data model (data mapping exercise) | Azmain | Today | Open | HIGH |
| Deploy application on AWS | BenVH | Today/tomorrow | Open | HIGH |
| Populate new data model with sample data from golden source | Azmain | Today | Open | MEDIUM |
| Refactor app UI to use new data model | Richard/Azmain | Today/tomorrow | Open | MEDIUM |
| Meeting with Chaucer at 2:30pm today | Richard/Martin | Today | Open | HIGH |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Data model design | technical | "once we've started to pump some data through this, we may just create what we call a view" -- Richard | HIGH |
| Acceptance criteria architecture | technical | "one table but a table can function as two different things" -- Richard | HIGH |
| AWS deployment plan | technical | "Amazon RDS for SQL Server... host inside VMs on Fargate... CloudWatch for logging" -- Richard | HIGH |
| Dashboard as output not input | strategic | "the dashboard is just a bunch of queries on top of what we've then done" -- Ben | HIGH |
| Pipeline review vision | strategic | "structured, prioritised way, so the call might be okay, let's look at the overall q1 migration completion accounts" -- Ben | HIGH |
| Azmain's capability gap | interpersonal | "I still don't fully understand everything Ben's built" -- Azmain | MEDIUM |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Richard Dosoo | Architecture lead, mentor | Drives data model decisions, plans deployment, mentors Azmain | 45% |
| Ben Brookes | Product owner, vision setter | Defines priority (data first, dashboard second), envisions pipeline meetings | 35% |
| Azmain Hossain | Learner, data mapper | Asks questions, expresses uncertainty, takes on data mapping task | 20% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Richard Dosoo | champion | STABLE | Technical delivery | Driving urgency on data model and deployment |
| Ben Brookes | champion | STABLE | Product vision | "data visibility problem is really urgent now" |
| Azmain Hossain | supportive | STABLE | Data mapping role | Eager but acknowledges skill gap on codebase |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Ben Brookes | Push code to GitHub main | Today | None | HIGH |
| Azmain | Do data mapping from golden source to new data model | Today | Receives data model schema | HIGH |
| Richard | Finalise data model changes | Today | ChatGPT performance permitting | MEDIUM |
| BenVH | Deploy to AWS | Today/tomorrow | Code and schema provided | HIGH |
| Richard | Walk Azmain through development process | Today (before 2pm Chaucer meeting) | None | MEDIUM |

## Meeting Effectiveness
- **Type:** planning
- **Overall Score:** 72
- **Decision Velocity:** 0.7
- **Action Clarity:** 0.7
- **Engagement Balance:** 0.5
- **Topic Completion:** 0.7
- **Follow Through:** 0.6

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-019 | OPEN | Azmain's capability gap on Ben's expanded codebase | MEDIUM | NEW | resource | HIGH |
| R-020 | OPEN | ChatGPT performance degradation slowing data model work | LOW | NEW | tooling | HIGH |
| R-021 | OPEN | Golden source data quality -- "massive gaps" in mapping to new schema | MEDIUM | NEW | data | HIGH |

## Open Questions Raised
- Should MAP be the long-term deployment target instead of Azure?
- How to build a natural language query interface for the executive dashboard?
- Where does resource management fit in the data model (deferred)?
- How to handle the migration-vs-adoption distinction at the use case level consistently?

## Raw Quotes of Note
- "the dashboard is just a bunch of queries on top of what what we've then done" -- Ben, on priority ordering
- "we have one table, but a table can function as two different things" -- Richard, on acceptance criteria architecture
- "I still don't fully understand everything Ben's built. It's like a massive enhanced version from what I had" -- Azmain, on capability gap
- "data visibility problem is really urgent now" -- Ben, on urgency

## Narrative Notes
This is a deep technical working session where the team gets into the weeds of data model design. The most important decision is the priority inversion: data collection and structure first, dashboards second. Ben's framing is clear -- the dashboard is just SQL queries, the hard part is getting structured data from CSMs. The acceptance criteria discussion reveals growing sophistication in the data model, with account-level success criteria and use-case-level acceptance criteria needing to coexist.

Azmain's honest admission about not understanding Ben's expanded codebase is significant. He has gone from owning a simple dashboard to being asked to work on a full-stack application. Richard's response -- offering to walk him through it as a learning exercise -- is generous but also reveals the team has no one who fully understands the whole system. Ben built it solo over Christmas, Richard can navigate the data model, but nobody has end-to-end knowledge. This is a classic bus factor problem.
