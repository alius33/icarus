# Deployment Database Synchronization Debugging Session
**Date:** 2026-01-19
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brooks (absent but referenced)
**Duration context:** Medium (~22 minutes)
**Workstreams touched:** WS2 CLARA (infrastructure)

## Key Points
- CLARA's deployed version is failing — all APIs returning errors because the database schema is out of sync with the deployed code
- Azmain's front-end refactoring changes were checked in but did not fully merge via the pull request — some UI components are missing from the main branch
- The core problem: not all stack components deploy automatically. Azmain makes database schema changes locally, but the Alembic migration process does not propagate them to the AWS RDS production database
- Richard walks Azmain through debugging by examining the deployed version vs local, checking GitHub diffs, and looking at AWS CloudWatch logs
- BenVH had been working on a deployment script to automate schema changes alongside code deployment, but it is not yet complete
- Richard emphasises the need to "roll forward, not roll back" — fix the problem and push rather than reverting
- Strategy: Azmain should confirm local code matches what should be in main, then push any differences, then debug the deployment pipeline

## Decisions Made
- Roll forward with fixes rather than rolling back → Richard, Azmain
- Need to run a diff between local code and main branch to identify missing components → Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Compare local build to GitHub main and push any differences | Azmain | Today | Open |
| Get BenVH to help fix deployment/database sync issues | Richard | When BenVH is online | Open |
| Reach out to Cursor training contact (Michael) about Cursor issues | Richard | This week | Open |
| Check with Divya about token usage limits on Cursor | Richard | This week | Open |

## Stakeholder Signals
- Richard is patient and instructive, teaching Azmain debugging methodology in real time
- Azmain is learning Git and deployment workflows on the job — the learning curve is visible but he is making progress

## Open Questions Raised
- Why is the Alembic migration process not syncing schema changes to production?
- Is Cursor performance degradation due to token limits or a separate issue?

## Raw Quotes of Note
- None selected — this was a highly technical debugging session with limited quotable moments
