# Portfolio Review — New Process with Natalia and Ben Brooks
**Date:** 2026-01-21
**Attendees:** Ben Brooks, Natalia (Plant), Azmain Hossain
**Duration context:** Medium (~32 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Critical design meeting for the weekly Portfolio Review process. Ben proposes a meeting structure: timeline (by quarter) -> action owners -> knowledge gaps -> accelerate
- Natalia insists that the high priority accounts list (about 20 customers) should always be discussed regardless of status — they are a standing agenda item
- Ben built a local prototype of a Portfolio Review page in Cursor overnight, showing a pipeline view by quarter with blocker details and discussion points
- Natalia pushes back on having a separate Portfolio Review tab — prefers using existing dashboard/filters to demonstrate the tool's usability during the meeting. She does not want the team thinking there is a special dashboard that replaces regular tool usage
- Natalia explicitly says no editing during the meeting: "It takes too much time and makes it unclear who's responsible for updates"
- They agree on a compromise: Portfolio Review page as a launching point, but actual discussion uses the existing customer detail pages
- Ben articulates a broader vision: different functional lenses for different users (management, solution architects, implementation team, executives)
- Natalia will send the high priority account list and critical fields needed
- Meeting structure finalised: global 90-minute meeting, possibly splitting into regional sessions later
- CSM instruction agreed: "Set up a meeting with the people that have been involved, 20-minute meeting, fill out the data together"
- Ben wants golden source data to be pre-loaded so CSMs are not doing new data entry — just augmenting existing data
- Edit restrictions (can only edit your own accounts) not yet implemented due to BenVH being out and lack of user-to-account mapping from SSO
- Audit trail exists but needs SSO integration to know who is making edits

## Decisions Made
- High priority accounts always discussed in Portfolio Review regardless of status → Natalia
- No editing during Portfolio Review meetings → Natalia
- Use existing dashboard views during meetings, not a separate tab → Natalia (Ben conceded)
- Portfolio Review page will exist as prep/launching point, not as the meeting itself → Compromise
- Global meeting first, may split into regional later → Natalia
- Do a dry run tomorrow afternoon → All

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Send high priority account list | Natalia | Today | Open |
| Send critical fields list | Natalia | Today | Open |
| Implement priority account filtering in Portfolio Review | Azmain | Before Monday | Open |
| Implement SSO user recognition | Azmain | Before next week | Open |
| Add audit trail tied to authenticated user | Azmain | After SSO | Open |
| Dry run of Portfolio Review | All | Tomorrow afternoon | Open |

## Stakeholder Signals
- Natalia is process-focused and practical — pushes back constructively on Ben's feature ambitions to keep scope manageable
- Ben is visionary but accepts Natalia's constraints — healthy tension between speed and process
- Azmain is quietly managing the tension between what is requested and what is technically safe to implement

## Open Questions Raised
- How will the Solution Architect and Implementation team views eventually be built?
- When will SSO integration allow proper user-to-account mapping?

## Raw Quotes of Note
- "I would refrain from making any edits during the meeting. It usually takes too much time and makes it unclear who's responsible for updates." — Natalia, setting a key process rule
