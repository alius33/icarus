# Chat with Rich
**Date:** 2026-02-05
**Attendees:** Richard Dosoo (Speaker 1), Azmain Hossain, BenVH (Speaker 2, briefly)
**Duration context:** Medium (~17 minutes)
**Workstreams touched:** WS2 CLARA, WS4 Friday (Adoption Charter)

## Key Points
- Richard proposed a data validation process: create a canonical data model in Excel, map it to the web UI tables, send to Catherine for sign-off before loading into the database — standard data migration practice
- Azmain wants to bypass the formal sign-off and just load data using Claude, addressing Josh/Catherine's feedback directly — he wants Monday's Portfolio Review to be noticeably better than the previous one
- Azmain's plan for before Monday: address Josh/Catherine's feedback, redesign portfolio review tabs per Natalia's requirements, load corrected data — that's it
- Natalia's Gainsight warning: the Gainsight team is already asking "what the hell is Clara?" — Catherine got summoned to a meeting. The Gainsight team sees CLARA as encroaching on their scope.
- George's suggested positioning: CLARA is a small IRP migration-specific tool, a subset of overall customer health. Gainsight is the master. CLARA feeds data upward, not replacing anything.
- Amanda's tool (from yesterday's cross-OU session) would be a much bigger problem for Gainsight alignment — it's a full CS management platform, exactly what Gainsight does
- Richard and Azmain agreed: the stakeholder management/alignment piece has been neglected while they focused on building. Next week needs more attention to positioning CLARA correctly.
- Natalia's operating style: cautious, process-driven, wants right people engaged. Ben's style: just go. Both are needed.
- Quick wins: partner section can be done in a day. Adoption charter has a base already but needs Ben to finalise the format with Steve Gentilli and Liz Couchman.
- Action to set up a cross-OU Teams channel and send Amanda the prompt for generating a functional spec of her app

## Decisions Made
- Partner section is the next quick-win after Monday's Portfolio Review improvements → Azmain
- Adoption charter waits for Ben Brooks to agree format with Steve/Liz → Ben
- Stakeholder alignment with Gainsight team is now urgent — need proactive positioning → Richard/Natalia
- Data loading will proceed without formal Catherine sign-off — Claude will handle the ETL → Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Address Josh/Catherine data feedback | Azmain | Before Monday | Open |
| Redesign portfolio review tabs per Natalia specs | Azmain | Before Monday | Open |
| Set up cross-OU Teams channel | Richard | Today | Open |
| Send Amanda the functional spec generation prompt | Azmain | Before Amanda flies Friday | Open |
| Schedule Natalia alignment call for tomorrow (1-to-1) | Azmain | 2026-02-06 | Open |

## Stakeholder Signals
- The Gainsight team is now aware of CLARA and potentially hostile — Catherine was "summoned" to explain it. This is a real political risk.
- Natalia is the political navigator — she understands the need to position CLARA carefully and manage stakeholders proactively
- Josh and Catherine continue to push back on data quality — Azmain is frustrated but choosing to just fix things rather than fight
- The gap between building and governing is becoming acute — the team has been heads-down on delivery and the political flank is exposed

## Open Questions Raised
- How will the Gainsight team respond to CLARA long-term? Is there a risk of being shut down?
- Can the adoption charter format be agreed before Ben returns next week?
- How to balance speed of delivery with stakeholder alignment needs?

## Raw Quotes of Note
- "If we threaten Gainsight team, they're just going to crush us" — Azmain, on the political stakes of CLARA's positioning
