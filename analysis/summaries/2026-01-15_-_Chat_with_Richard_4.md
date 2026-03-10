# Chat with Richard 4
**Date:** 2026-01-15
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (Van Houten)
**Duration context:** Medium (~31 minutes)
**Workstreams touched:** WS2 (CLARA)

## Key Points
- BenVH has come online and is actively debugging. He fixed an ALB (Application Load Balancer) routing issue that was causing the earlier API failures -- the API was routing incorrectly and he resolved it.
- The front end deployed successfully with Azmain's changes but some backend issues persist: team members not found error, action plan fetch errors, blocker fetch errors. These are database schema mismatches -- columns referenced in code that do not exist in the production database.
- Root cause explained by BenVH: the deployment pipeline currently handles code changes but NOT database migrations. Cursor runs migrations locally (using Alembic) but these do not propagate to the production database automatically. BenVH is currently building the migration automation.
- Azmain has been working on a new branch with fixes -- he has populated the app with only real data (removed all dummy data) and fixed the schema field naming issues locally.
- They do another pull request and merge. The CICD pipeline kicks off but there are two duplicate deploy-to-ECR workflows (a naming conflict in workflow files). One always fails, one passes. BenVH notes this for fixing.
- After the new deployment, some issues persist. They decide to proceed to the advisory team demo using the deployed version for what works and falling back to localhost for what does not.
- Demo with Stacy/Liz/Christine/Steve is in one minute -- they jump to that call.

## Decisions Made
- Proceed to advisory team demo with deployed version where possible, localhost as fallback -> Richard
- BenVH to build database migration automation as priority -> BenVH
- Azmain to use real data only (no dummy data) for the deployed version -> Azmain (done)

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Build automated database migration into CICD pipeline | BenVH | Today/tonight | Open |
| Fix duplicate deploy-to-ECR workflow files | BenVH | Soon | Open |
| Align local and production database schemas | BenVH | Today | Open |

## Stakeholder Signals
- BenVH is methodical and knowledgeable about infrastructure but working alone as the only person who can deploy. Single point of failure risk is evident.
- The team is under time pressure with the advisory demo imminent but handling it pragmatically.

## Open Questions Raised
- How to ensure Alembic migrations run automatically on production after code merges?
- Why are there two duplicate workflow files causing confusion in GitHub Actions?

## Raw Quotes of Note
- "Anytime you see something like 'undefined column' -- that's basically saying the database that currently exists does not have this... it's not an issue with the front end or back end, it's saying the back end is referencing a column that doesn't exist in the database" -- BenVH, explaining the root cause
