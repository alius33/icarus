# IRP Priority Accounts Migration & Adoption Review
**Date:** 2026-02-02
**Attendees:** Natalia (Plant) (Speaker 1), Rhonda, Azmain Hossain, multiple CSMs, Josh Ellingson (implied from data loss discussion), Diya (mentioned)
**Duration context:** Long (~1 hour, first live Portfolio Review using CLARA)
**Workstreams touched:** WS2 CLARA

## Key Points
- First live Portfolio Review meeting using CLARA as the primary tool — a landmark session
- Natalia ran the inaugural review walking through nine priority accounts displayed in the portfolio review tab
- Rhonda gave the first live account update (Aeon): 4+ years on platform, North America team now migrating, one red use case is a legacy exposure add-on that's no longer relevant
- Data loss incident dominated the meeting: multiple CSMs reported that entries they made Friday through Monday morning disappeared after a deployment refresh
- Diya reportedly noted the data loss — CSMs entered data that vanished, causing significant trust damage
- George Dyke asked for a show of hands to gauge the scale of data loss across the team
- Azmain confirmed the issue and promised it wouldn't recur — structural changes had been made to the database that caused the refresh
- Despite the data loss, Natalia maintained the meeting structure — went through accounts one by one asking CSMs for updates
- The meeting demonstrated the value of the structured approach even with imperfect data — first time the organisation had a data-driven portfolio review

## Decisions Made
- Portfolio Review will continue weekly using CLARA despite data issues → Natalia
- Data loss issue to be resolved permanently — no more deployment refreshes that wipe user data → Azmain/BenVH
- CSMs who lost data asked to re-enter — scope assessed as manageable (primarily 2 account managers) → CSMs

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Ensure deployment process doesn't wipe user-entered data | Azmain/BenVH | Immediate | Open |
| CSMs to re-enter lost data | Philip/Naveen | This week | Open |
| Continue weekly Portfolio Review cadence | Natalia | Ongoing | Open |

## Stakeholder Signals
- Natalia is composed and process-driven — kept the meeting structured despite the data loss disruption
- Rhonda is the first CSM to give a live update — setting a positive precedent for engagement
- Diya's awareness of the data loss is concerning — trust damage at the executive level
- CSM sentiment is mixed: some engaged, some frustrated by data loss

## Open Questions Raised
- How to prevent future data loss during deployments — need proper dev/staging/prod separation
- Whether the data quality is sufficient for Monday reviews or if more cleanup time is needed
- How to handle the trust gap after CSMs see their work disappear

## Raw Quotes of Note
- "This is our very first meeting, and we started updating the data in the tool very, very recently" — Natalia, setting expectations with the team
