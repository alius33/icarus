# Review Agenda for Sales Recon
**Date:** 2026-01-12
**Attendees:** Richard Dosoo, Azmain Hossain, Jamie (Sales Recon lead), Chiara, Idris, Conrad
**Duration context:** Medium (~28 minutes)
**Workstreams touched:** WS2 (CLARA), WS3 (Customer Success Agent), WS4 (Friday/Adoption Charter)

## Key Points
- First meeting between the insurance CS team and Sales Recon leadership (Jamie, Chiara, Conrad). Purpose: align on agenda for the 26 Jan executive meeting with Ari Lahavi, Colin Holmes, Mike Steele.
- Richard introduces Azmain as programme manager and app builder, and outlines the six Gen AI initiatives in insurance CS. Central theme: Salesforce is pivotal but the team faces data capture, reporting, and interaction challenges.
- Jamie confirms Sales Recon is finishing its current release (for sales kickoff) and is starting to think about CS requirements. Plans to give a small number of CS people access to the live Sales Recon environment for a pilot within 3-4 weeks.
- Jamie describes a potential approach: pre-configured Copilot agents accessible through Teams that link to Sales Recon content -- essentially providing a Teams-based interface to Sales Recon data.
- Idris reveals he already has a POC in Copilot Studio with an orchestrator agent pattern: sub-agents for annual spend, health scores, querying Sales Recon, all pushed into Teams via AD permissioning. This is more advanced than insurance's current position.
- Jamie emphasises the importance of getting knowledge out of people's heads into the system so information flows across silos (e.g., so Mike Steele does not have to call 12 people before a client meeting).
- Agenda for 26 Jan structured: Jamie does Sales Recon update/roadmap, then insurance CS presents problem statement and five project bodies of work, then Idris presents banking/insurance convergence, then Diya closes with priority decisions, then next 90 days.
- Richard commits to sharing slides by end of week for a review meeting the following week.
- Jamie will be in Edinburgh next week so the review will be virtual; Conrad available Thursday in London.

## Decisions Made
- Agenda structure for 26 Jan executive meeting agreed: Sales Recon update -> Insurance CS problem statement & projects -> Banking/insurance convergence -> Priority decisions -> Next 90 days -> Richard/Jamie
- Sales Recon to run a CS pilot with a handful of people once the current release ships (end of this week) -> Jamie
- Insurance team to provide consolidated requirement list rather than banking and insurance presenting separately -> Richard/Idris

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Share storyboard slides with Sales Recon team | Richard/Azmain | End of week (17 Jan) | Open |
| Set up virtual review meeting with Jamie for content alignment | Richard | Next week | Open |
| Provide list of insurance CS people wanting Sales Recon access | Richard/Azmain | Before pilot launch | Open |
| Share prompt library for CS use cases with Jamie/Chiara | Richard/Idris | Soon | Open |
| Visit Canary Wharf office for in-person session with Conrad/Chiara | Richard/Azmain | Thursday next week | Open |

## Stakeholder Signals
- Jamie is supportive and pragmatic -- framing this as a continuation of work started in June, not a new initiative. Wants to make sure Diya sees it the same way.
- Jamie is willing to release features broadly once CS team confirms usefulness -- no artificial gatekeeping.
- Idris is further ahead than expected with Copilot Studio POC; already thinking about orchestrator agent patterns.
- Conrad is engaged and helpful on data quality questions (Databricks ARR data, white space report).

## Open Questions Raised
- Has the annual spend / relationship data been corrected in Sales Recon? (Conrad to verify with James)
- What does the Gainsight integration look like from Sales Recon's side? (Jamie says minor integration now, better one coming this quarter)
- When exactly will Sales Recon production be ready for CS pilot users?

## Raw Quotes of Note
- "If we can get the people to say, look, Andy Frappe is going to be using the content here, you got to make sure your content is up to date. It might give them a carrot and a stick to update it" -- Jamie, on executive usage driving data quality
