# Chat with Richard 2
**Date:** 2026-01-15
**Attendees:** Richard Dosoo, Azmain Hossain
**Duration context:** Short (~27 minutes)
**Workstreams touched:** WS2 (CLARA)

## Key Points
- Debugging session focused on failed GitHub Actions build. 180 of 186 API tests passed, but 6 failed due to database schema mismatches -- tables/columns referenced in code that do not exist in the deployed database.
- Richard identifies the root cause: Azmain's broad prompt to Cursor ("make all buttons uniform universally") caused unintended changes to partner performance metric schema and other areas, creating mismatches between the local database and the deployed schema.
- Azmain is learning to manage Cursor permissions (auto-approve vs ask for each file change). Richard advises keeping the "ask" setting as a safety measure, despite it being annoying.
- They discuss context window management: stitching context windows together when they fill up, and why Claude's larger context window makes it superior for development and deep thinking tasks compared to ChatGPT.
- The build eventually passes all tests after Cursor auto-fixes the schema issues. Azmain successfully pushes to his feature branch, creates a pull request, and merges into main.
- The CICD pipeline kicks in automatically upon merge to main -- this is a milestone. Richard walks Azmain through watching the deployment in AWS ECS (showing the Fargate tasks spinning up).
- However, the deployed version initially shows a 503 error, then goes blank. They decide to give it a few minutes and reconvene.
- Richard plans to get Azmain access to the AWS console for troubleshooting visibility, even though normally BenVH handles infrastructure.
- Richard needs to step away for a call with Martin (Build in Five workstream).

## Decisions Made
- No major decisions -- this is a debugging/deployment working session

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Get Azmain AWS console access | Richard | Today | Open |
| Debug the 503/blank page issue on deployed version | Richard/BenVH | Today | Open |
| Chase developer laptop approvals | Richard | Today | Open |

## Stakeholder Signals
- Azmain is growing more comfortable with Git, CICD, and deployment workflows but still needs hand-holding. This is a real-time learning arc.
- Richard is patient and investing significant time in mentoring Azmain through development processes.

## Open Questions Raised
- Why is the deployed version showing 503/blank after a successful build?
- Is the database schema in production aligned with the latest code changes?

## Raw Quotes of Note
- "The first time is the hardest, right? But once we've done it once, it then gets progressively easier" -- Richard Dosoo, encouraging Azmain through the deployment process
