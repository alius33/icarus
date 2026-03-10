# App Development with Rhett
**Date:** 2026-02-19
**Attendees:** Richard Dosoo, Azmain Hossain, Rhett (Speaker 1), Ben (BenVH / Speaker 2)
**Duration context:** Medium (~27 minutes)
**Workstreams touched:** WS6 Build in Five, WS2 CLARA (tangentially)

## Key Points
- Rhett is being onboarded to app development. He has a static HTML app that needs to be pushed to GitHub and ported into Ben's skeleton app framework.
- Ben created a repo for Rhett but Git integration through Cursor has been flaky; Richard recommends GitHub Desktop with Moody's Okta SSO instead.
- Richard explains the dual-purpose infrastructure vision: internal productivity apps AND customer-facing demo apps on IRP's Risk Data Lake, all sharing a common tech stack and automated deployment pipeline so Ben does not become a bottleneck.
- The skeleton app framework provides authentication (Active Directory integration), role-based access control, and Moody's branding out of the box. Developers just define screen-level permissions.
- Richard describes three delivery channels for app building: (1) Cursor with cursor rules for IDE-comfortable users, (2) a lightweight UI chatbot that guides non-technical users through a spec-building workflow, and (3) a solutions catalogue / requirements database where people can cherry-pick features from previously built apps.
- The long-term vision is a "consulting AI platform" with MCP servers, skills libraries, and a solutions database so teams don't start from scratch each time.
- Richard notes CLARA has consumed all bandwidth, and the other five workstreams have had no meaningful progress. Martin returning from holiday will pick up Build in Five; Chris may help with CLARA to free Azmain and Richard for other programme work.
- Rhett asks about Cursor skills vs Claude skills; Richard explains Cursor's skills framework is less sophisticated (no project-level scoping, always in context window), but they'll make the skills succinct to manage token usage.
- The timeline estimate for the full app factory / consulting platform is 12-16 weeks, which Richard acknowledges is too long and needs consolidation.

## Decisions Made
- Ben will manually port Rhett's code into the skeleton framework this one time, as the automated process isn't ready yet. -> Ben (BenVH)
- Idris's app is prioritised because he has already sold the benefits to his senior leadership and the team feels obligated to deliver. -> Ben / Richard
- Rhett's app will be deprioritised slightly after Idris's. -> Richard to communicate

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Upload static HTML app code to GitHub repo | Rhett | ASAP | Open |
| Port Rhett's code into skeleton app framework | Ben (BenVH) | After upload | Open |
| Install GitHub Desktop with Moody's Okta | Rhett | After call | Open |
| Investigate Cursor skills framework parity with Claude skills | Richard / Azmain | TBD | Open |

## Stakeholder Signals
- Rhett is engaged and eager but not yet technically self-sufficient with Git or the deployment pipeline.
- Richard is candid about resource constraints: five projects stalled while CLARA consumed all bandwidth. Diya is starting to ask questions about the other workstreams.
- Ben (BenVH) is willing to be hands-on temporarily but explicitly notes he is not scalable.

## Open Questions Raised
- When will the automated deployment pipeline be ready so Ben doesn't have to manually deploy each app?
- How do they consolidate the 12-16 week estimate for the full platform build?
- Can they get access to Claude via AWS Bedrock to reduce dependency on Cursor token budgets?

## Raw Quotes of Note
- "We can't scale Ben out. I mean, we could, but we we can't, right?" -- Richard Dosoo, on the bottleneck of having one person deploy everything
