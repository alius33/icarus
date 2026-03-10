# Ben Explains New Dashboard
**Date:** 2026-01-06
**Attendees:** Ben Brooks, Richard Dosoo, Azmain Hossain, Martin Davies, BenVH (briefly mentioned)
**Duration context:** Long (~35 minutes)
**Workstreams touched:** WS2 (CLARA / IRP Adoption Tracker), WS4 (Adoption Charter — charter data model discussed)

## Key Points
- Ben demonstrates the app he built over Christmas using Cursor, driven by frustration with the team's inability to look up basic account data (e.g., the Gallagher incident before an ISLT call where nobody could answer simple status questions)
- The app breaks the golden source (O&M spreadsheet) into a proper data model with dashboards, use cases, blockers, action plans, data quality views, milestones, and team assignments
- Key conceptual distinction established: **migration** (turning off Risk Link) vs **adoption** (using IRP features more). Use cases can be tagged as "migration-critical" to calculate migration readiness
- Ben proposes natural language querying, a report builder, and contextual dashboards where users see only their assigned accounts
- Data quality is terrible: updating the baseline data from CSM entries moved completed migrations from 28 to 41 — 12 accounts had already finished but nobody had recorded it
- Ben has no Git knowledge and asks for help setting up collaborative development. Richard outlines a source code management strategy with main/dev branches
- Martin Davies explores Azure database deployment options during the call, finds a potential workaround for the networking restrictions by creating the SQL Server separately and linking it
- Richard proposes pivoting to AWS for faster deployment rather than fighting Azure security constraints
- Richard commits to refining the data model — specifically collapsing issues and plans into one table with granularity levels

## Decisions Made
- Pivot to AWS for initial deployment rather than waiting for Azure clearance → Richard/BenVH
- Use Ben's existing app as the baseline and iterate → Team
- Richard to refine the data model before deployment → Richard
- Blueprints and partner tracking deferred to phase 2 (implicitly, via Ben's feature-rich demo showing what's possible vs what's needed now)

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Refine data model (collapse issues/plans into one table) | Richard | 6 Jan evening | Open |
| Set up collaborative dev environment (Git, branches, CI/CD) | Richard/BenVH | Next week | Open |
| Get app deployed on AWS for demo next week | BenVH | Week of 12 Jan | Open |
| Explore Azure database workaround via separate SQL Server creation | Martin | Ongoing | Open |

## Stakeholder Signals
- **Ben Brooks** is fired up and impatient. Built the app over Christmas out of sheer frustration with the team's inability to manage data. Wants to demo next week and start getting CSMs to use it immediately.
- **Richard Dosoo** is acting as the technical bridge — sees the data model implications clearly and is already thinking about production readiness (source code management, branching strategy) while supporting Ben's urgency.
- **Azmain** is relieved: the app solves his biggest headache of chasing data across seven people and multiple spreadsheets. Enthusiastic but honest about needing guidance on the technical side.
- **Martin Davies** is proactive — independently explored Azure deployment options during the call without being asked.

## Open Questions Raised
- How to handle SSO authentication on AWS (Ben emphasises CSMs won't trust the app without proper login — cites the IRP Navigator precedent where CSMs refused to use a released product because they didn't believe the data was correct)
- Whether to use DynamoDB, Postgres, or SQL Server on AWS
- How to push data back into Salesforce as a back-end function so CSMs don't have to dual-enter

## Raw Quotes of Note
- "We went from 28 to 41 completed migrations just by updating the fucking data. And it makes me want to cry." — Ben Brooks, on the state of data quality
