# Chat with Rich Martin
**Date:** 2026-01-08
**Attendees:** Richard Dosoo, Azmain Hossain, Martin Davies, Ben Brooks (mentioned but not on the call — "work from home divorce" joke)
**Duration context:** Long (~48 minutes)
**Workstreams touched:** WS2 (CLARA / IRP Adoption Tracker)

## Key Points
- Technical troubleshooting session attempting to pull Ben's code from GitHub, run it locally, and update the data model. The session is characterised by repeated technical failures.
- **Azmain does not have Git installed on his machine.** This is a basic prerequisite that hasn't been set up. Martin steps in to clone the repo via VS Code.
- Richard attempts to pull the code via command line and fails. Martin clones it successfully in VS Code and gets the Swagger API docs running, but the front-end UI is broken (sidebar missing, import resolution errors).
- Azmain tries running a backup branch that Ben recommended (saying the main branch might not even run). Gets partial results — some UI renders but with errors.
- The team burns through Cursor premium token limits during debugging. Richard hits the "upgrade to Pro" gate repeatedly. They discuss the $10,000 Moody's budget across 1,200 users ($8/user/month average), which is grossly insufficient for power users.
- Richard mentions wanting to get Anthropic/Claude enterprise licences ($40/month) — Divya had reached out before the holidays but Richard was too busy to respond
- Azmain suggests using the powerful models for planning and cheaper ones for implementation. Richard (referencing Cursor's own guidance) says it's the opposite — powerful for planning, boilerplate models for implementation.
- The data model update from Richard's ChatGPT session is generating new Python files (parent account model, archetype customer model, etc.) but the process is painfully slow due to context window issues.
- No successful deployment achieved in this session. Decision to pick up with Ben at 9:30am tomorrow.

## Decisions Made
- Pick up deployment work with Ben tomorrow morning at 9:30 → Richard
- Azmain to continue trying to get the backup branch running locally → Azmain
- Richard to play with data model updates tonight if possible → Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Get Git installed on Azmain's machine | Azmain | Urgent | Open |
| Book 9:30am call with Ben to debug and deploy | Richard | 9 Jan | Open |
| Continue attempting local build from backup branch | Azmain | Tonight | Open |
| Pursue Claude/Anthropic enterprise licences via Divya | Richard | Next week | Open |

## Stakeholder Signals
- **Azmain** is learning on the job in real time — doesn't have Git, doesn't fully understand Ben's codebase, but is willing to grind through it. His honest admission ("I still don't fully understand everything Ben's built") shows self-awareness.
- **Richard** is frustrated by tooling constraints (Cursor limits, slow ChatGPT) but keeps pushing. Using personal Claude account to work around corporate limits — aware this isn't technically sanctioned.
- **Martin** is competent and helpful but has limited availability — full day of client meetings tomorrow, only free 9-10am and 12-2pm. Already juggling Canopus/holiday work.

## Open Questions Raised
- Which branch of Ben's code actually works? The main branch appears broken.
- How to resolve import resolution errors in the front-end build
- When will Cursor Pro/premium limits be resolved at the corporate level?

## Raw Quotes of Note
- "I'm gonna do all this shit, and I bet you it's gonna fail the build." — Richard Dosoo, on the data model update process
