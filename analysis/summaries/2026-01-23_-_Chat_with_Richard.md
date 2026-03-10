# Chat with Richard
**Date:** 2026-01-23
**Attendees:** Richard Dosoo, Azmain Hossain
**Duration context:** Short (~12 minutes)
**Workstreams touched:** WS2 CLARA (data, team assignments)

## Key Points
- Richard rushed through adding new employees to the CLARA database before Friday prayers — acknowledges the data mapping was not properly reviewed
- Discussion about adding solution architects and implementation leads: they need a new "role" field in the employee data model, not just reporting structure
- Azmain proposes a simpler approach for Monday: make the CSM/SA/IL assignment fields pull from the entire employee database (search and select anyone) rather than filtering by role — trusts users not to assign Colin Holmes as a CSM
- Richard warns against schema changes: "We're gonna add a field, the database migration thing's gonna break, we're gonna spend ages with Ben debugging"
- Azmain agrees to defer all schema changes — will just map CSMs from the golden source use case data to account level
- They discuss sharing Claude Code credentials as a workaround for Azmain's Cursor block — cannot share due to Google SSO authentication
- Richard heading to Jummah (Friday prayers) — will reconnect at 2pm
- Azmain's main task from Ben: get CSM-to-account assignments in before Monday using information from Josh/Miles/George
- Ben is on a separate call about portfolio review — Azmain needs to collate all of Ben's requests

## Decisions Made
- Defer all schema changes (new fields) until after Monday demo → Azmain
- Map CSMs to accounts from golden source data as a quick win → Azmain
- Assignment fields will be open (search from full employee list) rather than role-filtered → Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Map CSMs from golden source use case data to accounts | Azmain | Before Monday | Open |
| Get CSM account assignments from Josh/Miles/George | Azmain | Today | Open |
| Reconnect at 2pm to work through remaining items | Richard / Azmain | Today 2pm | Open |
| Start Teams thread with Jamie, Bernard, Alexandra for Monday prep | Richard | After Jummah | Open |

## Stakeholder Signals
- Both Richard and Azmain are acutely aware of the fragility of the deployment — operating in fear of breaking the database before Monday
- Richard's warning about schema changes reflects hard-learned lessons from the week

## Open Questions Raised
- How to add a "role" field to employee data without breaking the database?
- Can Cursor/Claude Code licence blocks be resolved before Monday?

## Raw Quotes of Note
- "We're gonna add a field, the database migration thing's gonna break, we're gonna spend ages with Ben debugging." — Richard, predicting deployment pain from schema changes
