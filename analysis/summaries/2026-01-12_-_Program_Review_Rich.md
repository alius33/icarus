# Program Review - Rich
**Date:** 2026-01-12
**Attendees:** Richard Dosoo, Azmain Hossain
**Duration context:** Medium (~28 minutes)
**Workstreams touched:** WS2 (CLARA), WS4 (Friday/Adoption Charter), WS3 (Customer Success Agent)

## Key Points
- Richard and Azmain discuss how to frame the programme's ROI for the executive meeting on 26 Jan. Two framings emerge: Ben's value-at-risk model (30+ implementations at risk without governance tooling) and Azmain's CSM capacity unlock (30-40%).
- Gainsight integration discussed as critical dependency. Natalia Plant's team has blocked API access pending security review; March 2026 is the earliest possible engagement date. Decision is to build standalone and plan convergence later.
- Richard explains the approach: build their own data model now, signal to Natalia's team for March integration timeline, and then do the API/schema alignment work after March.
- Azmain confirms Natalia already flagged the Gainsight API block when told about the plan. Strategy is to keep everything in-house and push a chunk of data to Gainsight when it is ready to receive.
- Richard raises the need to get consensus from Natalia, Kevin, and others before the 26 Jan meeting to avoid pushback.
- Idris (banking CS equivalent) has been 4-5 months ahead -- he has been prototyping apps in Cursor locally and presenting them to Ari Lahavi's team, but lacks infrastructure (no CICD pipeline, no AWS deployment). His requirements overlap with insurance in some areas (meeting prep, at-risk accounts) but diverge in others (no adoption charter process, different product depth).
- Richard and Azmain plan to compare insurance and banking requirements with Idris when he visits London (week of 26 Jan) to produce a consolidated requirement set for Jamie's team.
- Richard emphasises the need for a stakeholder map and RACI across all workstreams. Azmain suggests recording a call to map it via AI rather than manually writing it out.
- Brief discussion of AI models: Azmain using Opus for planning and Sonnet for building, as Richard suggested. Richard impressed by Opus output quality compared to ChatGPT. Both burning through personal credits at an unsustainable rate.

## Decisions Made
- Build standalone tracker without Gainsight/Salesforce integration for now; plan convergence for post-March when API access may be unlocked -> Richard/Azmain
- Present consolidated insurance + banking requirements to Sales Recon team at 26 Jan meeting -> Richard/Azmain/Idris
- Create a stakeholder map and RACI across all six workstreams -> Richard (to dictate), Azmain (to document via AI)

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Signal to Natalia Plant's team re: March Gainsight integration timeline | Richard | Before 26 Jan | Open |
| Get consensus from Natalia, Kevin, others before 26 Jan executive meeting | Richard | Before 26 Jan | Open |
| Reconcile insurance vs banking requirements with Idris during London visit | Richard/Azmain | Week of 26 Jan | Open |
| Create stakeholder map / RACI across all workstreams | Richard/Azmain | Next week | Open |
| Set up prep meeting with Jamie/Conrad/Chiara for 26 Jan content review | Richard | End of week | Open |

## Stakeholder Signals
- Richard is managing upward carefully -- wants no surprises at the 26 Jan executive meeting, prefers to build consensus first.
- Bernard (Life team) is sceptical about Gainsight -- after 3 years of pushing adoption he is only at 50%, has pivoted to using Copilot agent with Salesforce extracts instead.
- Natalia is process-focused and immediately flagged the Gainsight API block as a concern when told the programme plan.
- Idris is proactive and ahead of insurance in prototyping but lacks infrastructure support.

## Open Questions Raised
- When exactly will Gainsight API access be available? March is the earliest estimate but could slip.
- How will the programme demonstrate value if Gainsight integration is delayed past March?
- Where do insurance and banking requirements truly converge vs diverge?

## Raw Quotes of Note
- "Without this governance, without this process, you're actually at risk... the commercial impact and the relational impacts of those things not being well managed" -- Richard Dosoo, on framing ROI
