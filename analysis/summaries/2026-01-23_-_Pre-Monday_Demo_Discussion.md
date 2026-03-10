# Pre-Monday Demo Discussion
**Date:** 2026-01-23
**Attendees:** Richard Dosoo, Azmain Hossain, Idris (Banking CS), Bernard (Life team), Alexandra (Life team), George Dyke, Martin Davies
**Duration context:** Long (~60 minutes)
**Workstreams touched:** WS2 CLARA, WS3 CS Agent, WS6 Build in Five

## Key Points
- Dress rehearsal for Monday's executive meeting. Azmain demos the CLARA adoption tracker to Idris and Bernard (who have not seen it before)
- Idris is very impressed by CLARA — asks detailed questions about workflow, data flow, and architecture. Suggests it could serve as a "central source of data that feeds out into other systems"
- Azmain explains the architecture: golden source data imported, then the app becomes the new place for data input, eventually pushing back to Gainsight/Salesforce
- Idris mentions his team has a "Credit Lens 360 hub platform" for lending — sees parallels
- Bernard demos his Copilot health dashboard: extracted meeting data, case feeds from Salesforce, NPS data, and Mixpanel usage data into a SharePoint folder, pointed Copilot Lite at it, and prompted it to create HTML health assessments
- Idris raises hallucination concerns with Copilot/LLMs: his team found that if you challenge an SRB figure, Copilot will change it. They hard-coded rules in Copilot Studio to handle dollar amounts
- Bernard acknowledges hallucination risk but notes it is manageable with focused, specific prompts — complexity increases hallucination
- Alexandra raises concern about hallucination: wants to know how to protect against it in the Monday presentation
- Richard confirms the Salesforce API access is blocked — Natalia directed them to use Gainsight, but Gainsight implementation is not ready until end of March
- George confirms IRP migrations are on the MA scorecard — small number of projects but big revenue, high visibility
- Idris estimates three-quarters of the business unit revenue is related to IRP
- After others leave, Richard and Azmain set up a Claude Code Max subscription for Azmain using Richard's personal payment — workaround for the corporate Cursor block
- Martin Davies still has Cursor credits (335 out of 500) — not blocked yet

## Decisions Made
- Richard will pay for Azmain's Claude Code Max subscription out of pocket as a temporary workaround → Richard
- Refine CLARA demo with Azmain on Monday morning before the 2:30pm meeting → Richard, Azmain
- Bernard's slides from previous demo to be included in Monday deck → Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Refine CLARA demo on Monday morning | Azmain / Richard | Monday AM | Open |
| Get Claude Code working on Azmain's machine (restart, fix GitHub auth) | Azmain | Tonight/tomorrow | Open |
| Show customer insights / RMB demo on Monday morning (ran out of time today) | Richard / Azmain | Monday AM | Open |
| Raise AWS access ticket for Azmain (needed for back-end log access) | Richard | On his list | Open |

## Stakeholder Signals
- Idris is a strong ally — genuinely impressed and sees the potential for cross-OU scaling. His questions show strategic thinking
- Bernard is confident in his demo but Alexandra raises a valid concern about hallucination that needs addressing
- The workaround of Richard personally paying for Azmain's Claude Code subscription reveals the extent of the corporate tooling bottleneck
- Martin Davies (Build in Five, WS6) is present but barely speaks — his workstream has not had attention this week

## Open Questions Raised
- How to protect against LLM hallucination in executive demos?
- When will corporate Cursor/Claude Code licences be properly provisioned?
- Will Gainsight be ready by end of March as promised?

## Raw Quotes of Note
- "This is really cool... very impressive. Happy to see other groups doing this stuff." — Idris, reacting to the CLARA demo
