# Blockers with P Kimes
**Date:** 2026-02-26
**Attendees:** Azmain Hossain, Peter Kimes, Stacy (Dixstra), Kevin (Chernelle) (Speaker 1)
**Duration context:** Short (~21 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Peter Kimes presents a request to improve blocker tracking in CLARA by adding fields that existed in the old Salesforce adoption records but are missing from CLARA: specifically a User Voice URL field, a JIRA ID field, and a case URL field.
- The distinction between User Voice entries and blockers is clarified: not all User Voice submissions are blockers. Some are enhancement requests or nice-to-haves. But when a User Voice item is a genuine adoption blocker, it needs to be trackable from within CLARA so leadership can see the full picture.
- Stacy raises a concern about pulling all User Voice data into CLARA: it would create duplicate data in two systems and increase administrative burden on CSMs. User Voice has a widget feature that groups related items together -- CLARA does not yet have that capability, and similar blockers across customers remain hard to reconcile.
- After discussion, the group agrees on an MVP approach: instead of importing User Voice data wholesale, simply add URL/link fields to the existing blocker form in CLARA. CSMs can paste in the User Voice URL and JIRA link, preserving the reference without duplicating data. This mirrors what they were already doing in Salesforce.
- Azmain initially proposes creating a separate object for User Voice entries and using the URL to pull data via API, but Peter pushes back -- for now, just a simple link field is sufficient. No need to pull information automatically.
- Peter also raises the question of blocker categories: the old Salesforce system had "software blocker" and "model blocker" as separate types. CLARA consolidated everything into product/client/enablement categories. Azmain acknowledges the original blocker system was auto-generated from Salesforce data and lacked context for these distinctions. They agree not to revert categories now but to add the missing fields.
- Stacy emphasises keeping the scope tight: there is too much changing in CLARA right now, and the team should hit the hot-topic items first rather than over-engineering the solution.
- Azmain commits to implementing the additional fields by the next morning so Peter can test before the Monday CSM call.

## Decisions Made
- Add User Voice URL, JIRA ID, and case URL fields to CLARA blocker form (MVP approach) -> Azmain
- Do NOT import full User Voice data into CLARA -- keep User Voice as source of record, CLARA links to it -> Stacy / Peter / Azmain
- Do NOT change blocker categories (product/client/enablement) back to software/model split -> Azmain / Peter
- Peter to be guinea pig for testing the new fields once deployed -> Peter

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Add User Voice URL, JIRA ID, and case URL fields to CLARA blocker form | Azmain | Tomorrow morning (27 Feb) | Open |
| Test new blocker fields once deployed | Peter Kimes | 27 Feb | Open |
| Communicate new fields to CSMs at Monday call | Peter / Stacy | Monday 3 Mar | Open |
| Continue discussions on deeper User Voice integration (future phase) | Peter / Stacy / Kevin | TBD | Open |

## Stakeholder Signals
- Peter Kimes is pragmatic and well-prepared: he sent an email outlining the gaps with screenshots comparing Salesforce fields to CLARA, and is willing to start small with an MVP.
- Stacy is the voice of caution, consistently pushing back on scope expansion and protecting CSMs from additional administrative burden. She frames every discussion around "let's not give CSMs more work than they already had."
- Kevin (Chernelle) raises the valid concern that User Voice data is messy: merged feedback from multiple customers means AI could hallucinate if it reads aggregated entries without proper context.
- Azmain is responsive and fast -- committing to overnight delivery -- but admits he had forgotten Peter's original email amid the volume of requests.

## Open Questions Raised
- How will CLARA eventually reconcile similar blockers across multiple customers (the grouping/widget problem)?
- Should the blocker categories be revisited once the User Voice integration matures?
- What is the long-term plan for User Voice data in the CLARA ecosystem -- separate object or deeper integration?

## Raw Quotes of Note
- "There's so much going on with Clara right now... let's hit the hot topic buttons." -- Stacy, on keeping scope tight
