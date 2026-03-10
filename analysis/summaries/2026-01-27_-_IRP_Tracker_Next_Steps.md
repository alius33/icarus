# IRP Tracker Next Steps
**Date:** 2026-01-27
**Attendees:** Richard Dosoo, Ben Brooks, Azmain Hossain, BenVH (Ben Van Houten), Martin Davies
**Duration context:** Long (~43 minutes)
**Workstreams touched:** WS2 CLARA, WS4 Friday (Adoption Charter), WS6 Build in Five

## Key Points
- Post-launch planning session — the tool went live yesterday, now deciding priorities for the next two weeks
- Richard flagged that Azmain has been 100% on CLARA with zero time for programme management — PID not finalised, stakeholder mapping incomplete
- Ben Brooks set the priority: CLARA first, with a curated data set within two weeks. Double down on tracker features before anything else.
- Key features needed this week: RBAC (role-based access control), audit trail, best possible data, admin controls
- Agreed timeline: End of day Wednesday = Salesforce data cutoff. Thursday = build and release. Friday = CSMs can start populating. Monday = first real Portfolio Review
- BenVH confirmed production environment is ready — will do RDS snapshot and migrate database on Thursday night
- Ben Brooks and Josh at loggerheads over release timing: Ben wants CSMs using it now despite imperfect data; Josh wants more control before release
- Discussion of Claude/Opus API access via AWS Bedrock — Gustavo sent Richard setup info, could change config to use Opus 4.5 from AWS environment
- Feature discussion: transcript upload for gap analysis (compare what CSMs say in meetings vs. what's in the database), LLM-assisted blocker descriptions, natural language querying
- Work split proposed: Azmain on data (chasing Catherine, Natalia, Stacy), Martin on RBAC with BenVH, then split audit trail and update feature between them
- Partner section flagged by Alexandra but deprioritised by Ben — not yet a priority

## Decisions Made
- Priority order: RBAC → best data → audit trail → charter functionality (pushed to next week) → partner section (later) → platform work (later) → Ben Brooks
- Data cutoff: End of Wednesday from Salesforce, Thursday build/release, Friday CSMs populate → Ben Brooks
- Martin to work on RBAC with BenVH support while Azmain handles data → Team
- Claude/Opus API access to be pursued via AWS Bedrock → Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Chase Catherine, Natalia, Stacy for clean data | Azmain | Wed 2026-01-28 | Open |
| Implement RBAC with BenVH | Martin/BenVH | Thu 2026-01-29 | Open |
| Get Claude API key via AWS Bedrock | Richard | ASAP | Open |
| Golden source data upload to prod | Azmain/BenVH | Thu night | Open |
| Finalise PID for the programme | Azmain | Next 2 weeks | Open |
| Ping George, Josh, Natalia, Stacy, Catherine for data alignment | Ben Brooks | This week | Open |

## Stakeholder Signals
- Ben Brooks is impatient and confrontational about Josh's resistance — wants to force adoption despite data quality objections
- Richard playing mediator — acknowledges both the need for speed and the need for project hygiene
- Azmain is stretched and aware of the technical debt accumulating — "we're building technical debt as we go, but we'll fix it"
- BenVH is methodical — wants proper deployment gates and environments before rushing to production

## Open Questions Raised
- How to handle the Cursor subscription compliance issue — usage has been noted and audited by Moody's
- Whether to fold partner management into CLARA or keep it separate
- How to architect field-level audit trail without performance overhead

## Raw Quotes of Note
- "If he says one more time, please don't use this tracker, I'm going to fly over there and punch it" — Ben Brooks, on Josh's resistance to launching CLARA
