# Deployment Troubleshooting & Database Connectivity Review
**Date:** 2026-01-19
**Attendees:** Richard Dosoo, Azmain Hossain
**Duration context:** Long (~65 minutes, with a break in the middle)
**Workstreams touched:** WS2 CLARA (infrastructure)

## Key Points
- Continuation of the earlier debugging session. Richard uses Claude Code to diagnose and push fixes directly to the GitHub repo
- Claude Code correctly identified that the app was running inside a Docker container (not accessible from local browser), diagnosed missing database tables, and attempted to fix 500 errors by creating missing tables
- Richard accidentally pushed changes directly to a new branch rather than main — had to create a PR through GitHub manually
- After deploying, the front end updated but the database remained out of sync — "no such table: customers" errors persist
- Richard discovered role/permission issues: the deployed version was checking Azure AD admin group membership, which was unexpected behaviour
- Richard could not get localhost to work on his machine due to VPN/networking issues — had to push directly to AWS to test
- BenVH was not available (running HighRox race in Amsterdam) — critical infrastructure support missing
- Richard raises a service ticket to get Azmain access to the tech consulting team and AWS infrastructure
- They discuss the need for API health checks and endpoint tests to prevent the debugging "doom loop"
- Richard highlights rapid tech debt accumulation: magnitude of changes with no testing is unsustainable

## Decisions Made
- Once users start entering production data, any schema changes must ship with data fix scripts → Richard, Azmain
- Need to get Azmain AWS access so he can debug infrastructure issues independently → Richard
- Wait for BenVH to return before making further major deployment changes

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Raise service ticket for Azmain's AWS access | Richard Dosoo | Today | Open |
| Add Azmain to tech consulting team on Teams | Richard Dosoo | Today | Open |
| Write API endpoint tests to prevent recurring debugging loops | Azmain | Next week | Open |
| Get developer laptops approved | Richard Dosoo | This week | Open |

## Stakeholder Signals
- Richard is concerned about the speed-vs-quality trade-off and is starting to articulate the need for proper release management
- Azmain explicitly voices worry about tech debt: front end looks great but buttons and data might not work

## Open Questions Raised
- Why is the Alembic migration creating "multiple migration heads"?
- How to establish a proper dev/test/prod environment split (currently everything deploys to one environment)

## Raw Quotes of Note
- "The amount of tech debt that builds up when you're just... we haven't, like, all the time, right? Because we've been going. Now, you can only do that for so long before it catches you up." — Azmain, on accumulating tech debt
