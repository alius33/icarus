# Chat with Richard 3
**Date:** 2026-01-15
**Attendees:** Richard Dosoo, Azmain Hossain
**Duration context:** Short (~10 minutes)
**Workstreams touched:** WS2 (CLARA)

## Key Points
- Brief follow-up call to check on the deployed version after the earlier 503 error.
- The API is returning a 500 error with a specific message: "undefined column blockers.customer_id does not exist" -- a database schema mismatch between what the code expects and what exists in the production database.
- Richard shows Azmain how to use browser developer tools (Network console) to see API call failures -- a debugging skill transfer moment.
- They look at the AWS ECS console and see tasks are running but one Fargate task appears to still be provisioning.
- Richard adds Ben Brooks to the chat for help. Ben is expected to come online in about 30 minutes (he is training for HighRox, wakes up early).
- Pragmatic fallback plan: if the deployed version is not fixed in time for the advisory team demo, they will demo from Azmain's localhost.
- Azmain plans to send Ben Brooks the prompt needed to pull down the repo and run locally, so Ben can review changes before the demo.
- Richard suggests working on a parallel branch while the deployment issue is being resolved.

## Decisions Made
- Fallback plan: demo from localhost if deployed version is not fixed in time -> Richard
- Send Ben Brooks instructions to pull down and run locally -> Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Fix production database schema mismatch (customer_id column) | BenVH | ASAP (when he comes online) | Open |
| Send Ben Brooks the prompt to pull and deploy locally | Azmain | Now | Open |
| Start new branch for parallel development while deployment is debugged | Azmain | Today | Open |

## Stakeholder Signals
- Richard is calm under pressure -- immediately sets a fallback plan rather than panicking about the deployment issue.
- Ben Brooks is expected to fix things quickly once online -- the team relies heavily on his early-morning availability.

## Open Questions Raised
- Is the database schema mismatch caused by the migration scripts not running in production?

## Raw Quotes of Note
- "Worst case scenario, we can demo off your localhost for the meeting and then figure out the deployment after" -- Richard Dosoo, setting pragmatic expectations
