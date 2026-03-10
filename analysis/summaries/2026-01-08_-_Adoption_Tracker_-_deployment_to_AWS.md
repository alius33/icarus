# Adoption Tracker - Deployment to AWS
**Date:** 2026-01-08
**Attendees:** Richard Dosoo, Ben Brooks, Azmain Hossain
**Duration context:** Long (~50 minutes)
**Workstreams touched:** WS2 (CLARA / IRP Adoption Tracker), WS4 (Adoption Charter — data model discussion)

## Key Points
- Detailed data model planning session. The team agrees on the technical architecture for AWS deployment: Amazon RDS for SQL Server (fastest path), Fargate for hosting, CloudWatch for logging.
- Key decision: **use SQL Server on AWS RDS** rather than DynamoDB. This avoids schema changes and gets them running fastest. Can migrate to Postgres/DynamoDB later for cost savings.
- Richard walks through new project management tables: projects, project imports, tasks, adoption milestones, customer adoption milestones. These allow uploading project plans directly rather than manual entry.
- Significant data model debate about **acceptance criteria vs success criteria**: Ben argues acceptance criteria should be at the use case level (e.g., "instant event response") while success criteria are at the account/adoption level (e.g., "5x throughput across all schedules"). Richard resolves this by creating a single table with a column denoting what level the criteria applies to.
- Blueprints and partner tracking explicitly deferred to phase 2 by mutual agreement.
- The dashboard is reframed as "the result" — data model and data quality come first, dashboards are just queries on top.
- Ben wants to launch as a "stealth preview" with friendly users immediately, rather than waiting weeks for perfection. Plans weekly Monday calls (Europe and US) for structured pipeline management reviews with all adoption squad members.
- Richard clarifies the workflow: Azmain does data mapping from golden source to new schema, Ben pushes latest code to GitHub main, Richard and Azmain create a branch with new data model, BenVH deploys to AWS.
- Richard acknowledges they're doing this backwards (prototype first, architecture hardening later) but accepts the trade-off for speed. Plans one to two days of hardening the week after next.
- Richard mentions wanting Claude/Anthropic enterprise access and is pursuing it through Divya. Also explored MAP (Moody's Application Platform) with Michael Feldman — MAP strategy is changing and may support non-production workflows.

## Decisions Made
- Use SQL Server on AWS RDS for initial deployment (not DynamoDB) → Richard/BenVH
- Acceptance criteria to be a single table with level indicator column (use case level and adoption level) → Richard
- Blueprints and partner features deferred to phase 2 → Ben/Richard
- Ben to push latest code to main; Richard/Azmain to branch for data model changes → Immediate
- Target: have deployable version by end of 8 Jan or 9 Jan → Team
- Weekly Monday pipeline review meetings (EU and US) once app is live → Ben to set up

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Push latest code to GitHub main | Ben | Today (8 Jan) | Open |
| Map golden source data to new schema | Azmain | Today/Tomorrow | Open |
| Create branch with new data model and updated app | Richard/Azmain | Today | Open |
| Deploy to AWS once code and data ready | BenVH | 8-9 Jan | Open |
| Build pipeline report (by quarter and adoption status) as first dashboard | Azmain | After deployment | Open |

## Stakeholder Signals
- **Ben** is impatient to launch. Wants to start getting CSMs entering data immediately, even with imperfect data, to drive behaviour change. Acknowledges the risk ("we'd better hope it doesn't fall flat on its face").
- **Richard** is methodical beneath the urgency — insists on proper data model foundations even while accepting speed trade-offs. Thinking ahead to database views that insulate dashboards from schema changes.
- **Azmain** asks practical PM questions ("What's the time frame?") and is honest about not being confident doing the code refactoring alone.

## Open Questions Raised
- Should use cases expand beyond the current 15 predefined ones to include non-functional/adoption use cases like "single source of truth for all exposure data"?
- When does the existing code get rationalised and cleaned up? Richard says "week after next" but this is aspirational.
- How will the data be seeded — real golden source data or synthetic? (Both discussed; synthetic for demo, real for production)

## Raw Quotes of Note
- "The dashboard is just a bunch of queries on top of what we've then done." — Ben Brooks, clarifying that data model is the priority, not the UI
