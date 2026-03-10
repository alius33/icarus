# Sales Recon Pilot Kickoff — CS Team
**Date:** 2026-02-11
**Attendees:** Cara (Speaker 2), Idrees, Bernard (Speaker 4), Peter Kimes, and approximately 5 other CSM participants (Speakers 3, 5)
**Duration context:** Medium (~32 minutes)
**Workstreams touched:** WS3 CS Agent (Sales Recon convergence)

## Key Points
- Cara launches the two-week Sales Recon zero pilot for the Customer Success team. Sales Recon zero is the internal version (Moody's is "customer zero"); a potential external version is out of scope for this pilot.
- Testing period: 11-24 February 2026. Post-pilot interviews will follow, potentially spilling into early March.
- Eight CSMs across the organisation are included. Most already have Salesforce access to Sales Recon. This is production, not a sandbox — all data entered is real and persistent.
- Three features to focus on during the pilot: (1) Account Intelligence — shared knowledge base sourced from Salesforce, Orbis, web research, and user interactions; (2) Meeting Preparation Agent — interactive agent to help prepare for client meetings with agenda, talking points, cheat sheets; (3) Share Knowledge Agent — upload meeting notes, updates, and documents to hydrate the account intelligence.
- Two additional features exist but are more sales-oriented: Account Planning (sales ops templates) and Lead Generation (pitch/conversation starters). CSMs can explore these but the focus is on the three CS-relevant features.
- A feedback tracker platform has been built specifically for the pilot. CSMs submit feedback (bugs, feature requests, positive experiences) to the CSM-specific area within the tracker.
- Known limitations: parent/subsidiary account analysis is limited to the specific Salesforce account selected (subsidiaries don't roll up to parents and vice versa). This is a frequent feedback item already being worked on. Product list is partial, so "active products" tab and total value figures are incomplete.
- Output is currently text/markdown only. HTML and PowerPoint export planned for mid-April release.
- Bernard asks about timeline — when will the first CS-specific version ship? Cara clarifies this beta is already the first released version in production; the pilot feedback will shape the roadmap for CS-specific enhancements.
- Peter Kimes asks about prompt libraries — none exist yet, but it is something that could be developed from the pilot findings.

## Decisions Made
- Pilot runs 11-24 Feb with 8 CSMs, using production Sales Recon environment -> Cara
- CSMs should focus on 2-5 accounts they know well for the pilot -> Cara
- Feedback goes to the dedicated tracker platform (CSM-specific area, not the sales area) -> Cara

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Test access to Sales Recon in Salesforce | All pilot CSMs | 2026-02-13 | Open |
| Follow 2-5 well-known accounts and test features | All pilot CSMs | 2026-02-24 | Open |
| Submit feedback via feedback tracker platform | All pilot CSMs | Ongoing | Open |
| Schedule post-pilot 1:1 interviews with each CSM | Cara | Late Feb / early Mar | Open |
| Explore prompt library creation based on pilot findings | Cara / Peter Kimes | Post-pilot | Open |

## Stakeholder Signals
- Bernard (Life team) is probing on timelines — his question about when the first CS version ships reveals impatience or scepticism about delivery cadence. The answer that this is already the first version may not fully satisfy him.
- Idrees provides critical context framing for the group: the pilot feeds into Anna's team (on Jamie's roadmap) who are already building CS-specific features in a sandbox. This pilot validates requirements, not builds them.
- Peter Kimes is thinking about knowledge management (prompt libraries) — consistent with his broader User Voice integration interests.
- The parent/subsidiary limitation is a known pain point across the organisation, not just for Sales Recon.

## Open Questions Raised
- When will Gainsight data (health scores, risk drivers) be integrated into Sales Recon's account intelligence?
- Will parent/subsidiary account rollup be addressed in the next release cycle?
- Should CSMs avoid the "create opportunity" and "schedule meeting" buttons that write back to Salesforce?

## Raw Quotes of Note
- "Please do not make up examples or information, because it's going to be part of the actual knowledge." -- Cara, warning that this is a production environment
