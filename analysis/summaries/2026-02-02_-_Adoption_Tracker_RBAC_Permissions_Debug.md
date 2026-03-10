# Adoption Tracker RBAC Permissions Debug
**Date:** 2026-02-02
**Attendees:** Richard Dosoo (Speaker 1), BenVH (Speaker 2/3), Azmain Hossain, Philip Garner (Speaker 4)
**Duration context:** Medium (~30 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Debugging session for RBAC (role-based access control) — Philip Garner used as a test subject for permissions
- Philip could not save edits (executive summary field) — got "insufficient permissions" error in the network console response
- BenVH walked Philip through browser dev tools (network tab, console) to capture the error
- Root cause investigation: BenVH suspected either a caching problem on Philip's device or permissions not being applied to the user on login
- Azmain had assigned Philip admin and editor roles, but the permissions weren't propagating — the admin section wasn't appearing in the left-hand navigation
- BenVH removed his own admin access to simulate the CSM experience for testing
- Discussion of AI tool limitations: Cursor/Claude got them 80-90% of the way but started hallucinating at the edge cases, particularly around RBAC
- Richard reassured Josh (via message) that data discrepancies were from only two account managers (Philip and Naveen) who entered data over the weekend — not widespread
- Philip offered to continue testing tomorrow if needed, provided useful feedback on the process

## Decisions Made
- Philip confirmed as ongoing test user for RBAC validation → Team
- Team will reproduce the permissions issue without Philip present (BenVH can simulate it) → BenVH/Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Fix RBAC permissions propagation on login | BenVH/Azmain | 2026-02-02 | Open |
| Communicate data loss scope to Josh — only 2 users affected | Richard | 2026-02-02 | Open |
| Continue RBAC testing once fix deployed | Philip | Next day | Open |

## Stakeholder Signals
- Philip is willing and engaged — providing substantive testing help and practical feedback
- BenVH pragmatic about AI limitations: treats it as a junior developer that needs supervision
- Richard is managing Josh's concerns in real-time — minimising the perceived severity of the data loss

## Open Questions Raised
- Is the permissions issue a caching problem or a fundamental application logic issue?
- How much data did Naveen actually enter over the weekend? (Richard dismissive of his complaints about lost work)

## Raw Quotes of Note
- "It's got us 80 to 90% of the way there. The problem is, now that we're here, it can't keep up with everything, so it starts hallucinating" — BenVH, on Cursor/Claude limitations
