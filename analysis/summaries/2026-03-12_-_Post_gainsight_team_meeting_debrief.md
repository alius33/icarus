# Post Gainsight Team Meeting Debrief
**Date:** 2026-03-12
**Attendees:** Azmain Hossain, Richard Dosoo, Ben Brookes, BenVH
**Duration context:** Medium (~18 minutes)
**Primary project:** CLARA (IRP Adoption Tracker)
**Secondary projects:** Program Management, App Factory

## Key Points
- Immediate debrief after the Gainsight integration meeting — team is furious
- Consensus: Kathryn Palkovics blindsided them by not sharing the Gainsight team's presentation slides despite a prep meeting being held specifically for alignment
- Azmain messaged Natalia Plant during the call flagging the situation
- Richard: spent time the night before creating slides for the meeting, feels the prep work was wasted because Kathryn Palkovics did not share what the Gainsight team was going to present
- Team strategy crystallised: keep Clara as the UI layer, push all data Gainsight wants via API, let App Factory handle the integration middleware
- BenVH provided experienced perspective — has seen the Salesforce-to-Gainsight migration cycle four times before (Microsoft, GitHub, Bank of America) and predicts Gainsight will be replaced in 3-5 years. Clara should remain vendor-agnostic
- Ben Brookes advocated a passive-aggressive approach: send Gainsight team Clara's API spec and say "here's what we need to write — tell us where in Gainsight it goes"
- Team firmly agreed: the core team will not be pulled away from driving migrations to do integration work for Gainsight
- Kathryn Palkovics' Centre of Excellence (digital engagement programme) identified as a political threat — scope overlaps directly with the AI programme
- Azmain revealed Diana had warned him about Kathryn Palkovics potentially trying to absorb the AI programme under her COE
- Richard planning to discuss Kathryn Palkovics' actions with Diya when she's in London next week
- BenVH reported good progress on App Factory MCP server — pivoting to AWS Bedrock AI agents for the orchestration layer rather than building custom LLM orchestration. Hoping to have something by end of week

## Decisions Made
- Clara will remain the UI and reporting framework; Gainsight will be used as a data store → App Factory handles integration
- Team will write a charter with demanding business requirements that Gainsight team must meet — designed to slow down integration without explicitly refusing
- Richard to escalate Kathryn Palkovics' behaviour to Diya directly
- BenVH will use AWS Bedrock AI agents (not custom orchestration) for App Factory MCP server

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Write Gainsight integration charter with demanding business requirements | Azmain | This week | Open |
| Discuss Kathryn Palkovics' actions and COE overlap with Diya in London | Richard | Next week | Open |
| Share Kathryn Palkovics' COE slide with Richard and Ben Brookes | Azmain | Today | Open |
| Complete App Factory MCP server using Bedrock AI agents | BenVH | End of week (14 Mar) | Open |

## Stakeholder Signals
- Ben Brookes: most strategically aggressive — wants to "push back hard" on Gainsight integration, sees it as a waste of time. Protective of team's focus on migrations.
- BenVH: experienced and philosophical about vendor lock-in cycles. Channelling energy into MCP server as the long-term solution. Predicts Gainsight will be replaced.
- Richard: emotionally reactive about Kathryn Palkovics' blindside but strategically focused — will use Diya's London visit as the intervention point
- Azmain: caught between diplomacy and frustration. Messaged Natalia immediately. Collecting intelligence on Kathryn Palkovics' remit and senior backers.

## Open Questions Raised
- Will the charter approach successfully slow down Gainsight integration without creating political backlash?
- How will Diya react when Richard raises the Kathryn Palkovics issue?
- Can BenVH deliver the MCP server by end of week given everything else on his plate?

## Raw Quotes of Note
- "This is an epic waste of time. I don't know why we would buy a system to do this kind of shit anymore" — Ben Brookes, on the Gainsight integration
