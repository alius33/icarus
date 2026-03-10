# Pre Gainsight Team Meeting
**Date:** 2026-03-06
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (Speaker 1), Chris M, Catherine (Kathryn)
**Duration context:** Medium (~23 minutes)
**Workstreams touched:** WS2 CLARA, WS3 CS Agent, App Factory / Infrastructure, Gainsight integration

## Key Points
- **Gainsight meeting next Thursday**: Catherine set up a call with the Gainsight team for the following Thursday. This pre-meeting was to align goals and prepare. The Gainsight team now understands that people will build their own tools to fill gaps, and they want to explore what integration with CLARA (and other apps) would look like.
- **Gainsight team stakeholders identified**: Nadim (works with Catherine on what should be built), Tina Palumbo (executive view on overall Gainsight strategy at Moody's), Rajesh (technical contact for data integration). Catherine works with them as the insurance business-side advisor.
- **Key question for the meeting**: Does integration make sense? If so, what pieces? The goal is not to pull CLARA into Gainsight or vice versa, but to identify what CSMs need at their fingertips without duplicating work.
- **Salesforce integration to be included**: Richard requested that the Thursday meeting also cover Salesforce programmatic access, since multiple projects need it (Bernard's customer sentiment from tickets, Courtney's HD models, Kevin Pern's CS Agent requirements). Catherine confirmed the business systems team now understands they need to "play nice with these apps" and can help with Salesforce access.
- **Resource planning gap**: Gainsight integration was not in the 12-week resource plan created two weeks ago because they did not know it was possible. If integration is expected, replanning will be needed.
- **Account planning governance example**: Richard raised that George is building an account planning app and Idris (banking) is building one too. He cannot tell senior CSMs to stop innovating because it might overlap with the Gainsight roadmap. Catherine clarified she is not saying "don't build" -- she is saying "if it exists, how do we make sure it integrates so we aren't creating silos."
- **Catherine's governance offer**: She offered to serve as the gating checkpoint for whether an idea should be built as a custom app or already exists in enterprise tooling (Gainsight, Salesforce, etc.). She wants to help create a decision tree for the App Factory intake process.
- **Azmain's candid statement**: He acknowledged that the team is exhausted and that the fast pace is leading to things being done too quickly and incorrectly. He welcomed Gainsight governance as a legitimate reason to slow down. He also stated directly that their biggest fear is the Gainsight team "crushing them" and they need to stay on their good side.
- **Integration architecture approach**: Azmain said they would adapt their architecture to fit Gainsight, not expect Gainsight to adapt to them. CLARA's IRP data is a small subset of overall customer health (Gainsight's purview).
- **BenVH's perspective**: He wants to minimise data stored on their end. He has been thinking about integration patterns from the beginning of App Factory. He echoed the governance need -- he is seeing people wanting the same things independently.
- **Pre-reading for Thursday**: Richard will send App Factory slides and CLARA documentation to the Gainsight team before the meeting so they come prepared with questions.
- **Chris's next project**: Richard flagged that Salesforce integration will be Chris and Nikhil's next project after CLARA bug work.

## Decisions Made
- Thursday Gainsight meeting will also cover Salesforce programmatic access -> Catherine to set expectation
- Richard to send App Factory and CLARA documentation as pre-reading -> Richard
- CLARA architecture will adapt to Gainsight, not the reverse -> Azmain
- Catherine to help design governance/decision tree for App Factory intake -> Catherine
- Chris and Nikhil's next assignment after CLARA is Salesforce integration -> Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Send App Factory slides and CLARA documentation to Gainsight team | Richard | Before Thursday | Open |
| Set expectation with Gainsight team to include Salesforce in Thursday agenda | Catherine | Before Thursday | Open |
| Compile Salesforce requirements from Bernard, Courtney, and Kevin Pern | Richard | Before Thursday | Open |
| Get Bernard's detailed requirements | Richard | Monday | Open |
| Forward Thursday meeting invite to Chris | Richard | ASAP | Open |
| Prepare CLARA-as-complementary-to-Gainsight positioning for Thursday | Azmain | Before Thursday | Open |

## Stakeholder Signals
- **Catherine** is a critical new ally. She sits between the business and the Gainsight/enterprise tooling team and wants to help rather than block. Her offer to participate in governance and provide visibility into Gainsight's roadmap could prevent significant duplication of effort. She is enthusiastic about governance ("you're speaking my love language").
- **Azmain** is using the Gainsight meeting as an opportunity to legitimately slow down the programme's pace. This is a strategic move -- the team is exhausted and needs a credible reason to push back on the constant demands for speed.
- **BenVH** is aligned on governance and integration from the start. His consistent message is: minimise data duplication, build integration patterns once.
- **Richard** is thinking about this as a multi-project coordination problem. He sees the Thursday meeting as a chance to solve Salesforce access, Gainsight integration, and governance in one go.
- **Tina Palumbo**, **Nadim**, and **Rajesh** on the Gainsight team are new stakeholders who will become important going forward.

## Open Questions Raised
- What does Gainsight's authentication model look like? (Moody's domain SSO or separate login?)
- What REST services or APIs does Gainsight expose for integration?
- Is there a published Gainsight roadmap the team can see to avoid building what is already planned?
- How will the 12-week resource plan be adjusted to accommodate Gainsight integration work?
- What governance framework will define which apps enter App Factory?

## Raw Quotes of Note
- "Mine and Richard's biggest fear is like Gainsight team could crush us. So we need to keep them on our good side." -- Azmain, on the political dynamics of Gainsight integration
