# CSM Dashboard Permissions & Testing Review
**Date:** 2026-02-03
**Attendees:** Richard Dosoo, BenVH (Speaker 2), Azmain Hossain, Philip Garner (Speaker 4/5), Sneha (Speaker 5, testing)
**Duration context:** Long (~38 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Philip Garner asked about client-facing transparency dashboard — can they share a live view with customers showing defect/feature tracking progress?
- Richard explained the product alignment challenge: Alicia (PM) is open to requirements traceability from workflow to use case to product feature, linked to JIRA tickets
- Once features ship, the system could generate a monthly report showing impact to each client — but CSMs would still need to manually update clients
- Testing continued with RBAC — BenVH removed himself from admin to simulate CSM experience, then restored permissions
- BenVH merged dev branch to production and pushed fixes — all RBAC fixes now in production
- Sneha tested the system: could save edits on accounts assigned to her but got "insufficient permissions" on accounts not assigned — this is working as designed (CSMs can only edit their own accounts)
- The "insufficient permissions" error on unassigned accounts was not a bug but correct RBAC behaviour — however, the error UX was poor (no helpful popup)
- Azmain tested the "my customers" dashboard view — when signed in, a CSM should see only their assigned customers
- Sneha found that updates save correctly but the dashboard "last updated" timestamp doesn't reflect blocker updates, only account-level edits
- CSM feedback: need better navigation between accounts (currently refreshes to dashboard), and blocker/action plan timestamps should show on the dashboard
- Richard was not invited to the CSM workshops happening this week (Liz organised them) — expressed frustration but chose not to engage; told Azmain to focus on the build

## Decisions Made
- RBAC confirmed working correctly: CSMs can only edit their assigned accounts → Team
- Need better error handling with user-friendly popups instead of generic 403 errors → Azmain
- Richard deliberately staying out of the workshops he wasn't invited to — focusing on delivery → Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Add friendly popup for permission errors | Azmain | Next sprint | Open |
| Fix dashboard timestamps to reflect blocker/action plan updates | Azmain | Before Monday review | Open |
| Deploy production fixes for RBAC | BenVH | 2026-02-03 (done) | Complete |
| Get another CSM to test (beyond Philip) | Azmain | Today | Open |

## Stakeholder Signals
- Philip wants to go further — asking about client-facing dashboards shows forward-thinking engagement
- Richard is openly frustrated about being excluded from CSM workshops by Liz — but channelling it into delivery focus rather than political engagement
- Sneha is providing hands-on testing — good sign of broader engagement beyond the core team
- Richard is candid about the dysfunctional dynamics: Josh and Ben at loggerheads, Liz gatekeeping workshops, people without work creating noise

## Open Questions Raised
- When will the Jira API integration for product feature traceability be ready?
- How to handle the CSM workshops that Azmain wasn't included in — should he attend to gather feedback?
- Timeline for adoption charter functionality — Steve Gentilli and Liz Couchman need to agree on the format first

## Raw Quotes of Note
- "This is the first time I've seen on the meeting, like, Okay, let's go through the accounts in this order. This is the priority" — Richard, on the value of the Portfolio Review structure
