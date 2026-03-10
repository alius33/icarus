# Moody's Virtual Environments with BenVH
**Date:** 2026-02-26
**Attendees:** Azmain Hossain, BenVH (Speaker 1)
**Duration context:** Long (~43 minutes)
**Workstreams touched:** WS6 Build in Five, WS2 CLARA

## Key Points
- BenVH presents Phantom Agent, his personally patented CICD orchestration solution repurposed for AI agent governance. The core problem it solves: as employees spin up AI agents on local machines or cloud instances, there is no way to control costs, enforce security, or track usage by team. Phantom Agent provides that orchestration and governance layer.
- Phantom Agent architecture: uses SSO/OIDC to authenticate employees, determines team membership, and allows IT admins to configure which cloud resources (AWS, Kubernetes, Azure, on-prem) each team has access to. When a user requests an AI agent, Phantom Agent provisions it in the team's designated environment with appropriate permissions and cost tracking.
- Key capabilities: (1) per-team cost control and capping, (2) dynamic scaling policies (pre-warmed agents on schedule or on-demand), (3) auto-injection of MCP servers, (4) agents run in isolated cloud environments rather than on employee laptops (solving the hardware limitation problem), (5) Phantom Agent itself is an MCP server, so any LLM can leverage it.
- BenVH has been working on this for five years in the CICD space. The AI agent use case is a natural extension because the same governance problems (cost allocation, security, environment provisioning) now apply to AI agents at scale.
- The personal ownership dilemma: BenVH wants Moody's to use Phantom Agent but does not want Moody's to own it. Azmain suggests the vendor model -- BenVH's company licenses it to Moody's, then can sell it to S&P, Fitch, and others. BenVH is excited by this but has never navigated this kind of corporate engagement.
- The "virtual environment for non-technical users" use case emerges: instead of giving every employee a $5,000 developer laptop to run Cursor/Claude locally, Phantom Agent can provision cloud-based development environments. At the cost of one dev laptop, the system could serve 1,000 users for a month.
- Azmain connects this to his own pain point: Copilot can access Microsoft Graph API data (emails, SharePoint, Teams) but is not very smart. Claude is smart but cannot access Microsoft data. Phantom Agent could bridge this: an orchestrator agent queries Graph API, sends raw data to a Claude instance spun up via Phantom, gets intelligent analysis back, and shuts down.
- BenVH has a meeting with Melinda Trigerino (risk governance) next week about the solution. Azmain advises delaying until he has a working demo using the Moody's AWS Bedrock API, rather than trying to explain the concept abstractly to a non-technical audience.
- Azmain commits to "planting seeds" with senior stakeholders: casually raising the problems Phantom Agent solves (laptop crashes, uncontrolled costs, security concerns) with Alexandre, Ben Brooks, and others so that when BenVH demos the solution, the audience already understands the need.
- AWS Bedrock API access issue surfaces: Azmain tried using Richard's API key but got an "unauthorised" error due to incorrect AWS role assignment. BenVH has the key but has not tested it with his solution yet.
- Both agree the team needs to be selective about who they bring on: enterprise employees who complain rather than contribute solutions would slow them down. Graduates with energy and no corporate baggage are preferred.
- Catherine Lady (from the IRP adoption chat) called out as actively undermining CLARA: she flags issues like "under construction" features and target dates passing, but never volunteers to fix anything or even do basic data entry herself. Stacy ends up doing the manual cleanup work instead.

## Decisions Made
- Phantom Agent demo to use Moody's AWS Bedrock API as proof point -> BenVH
- Delay Melinda Trigerino meeting until working demo is ready -> BenVH / Azmain
- Azmain to plant seeds with senior stakeholders about the problems Phantom Agent solves -> Azmain
- Microsoft Graph API integration to be explored as first use case (email/SharePoint/Teams through Claude) -> Azmain / BenVH
- Virtual environment for non-technical users to be the primary selling proposition -> Azmain / BenVH

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Build working Phantom Agent demo using Moody's AWS Bedrock API | BenVH | Before Melinda meeting | Open |
| Test AWS Bedrock API key with Cursor/Phantom Agent | BenVH | This week | Open |
| Plant seeds about AI cost control and virtual environments with senior stakeholders | Azmain | Next 1-2 weeks | Open |
| Give Azmain access to Atlas (Phantom Agent UI) for testing | BenVH | When ready | Open |
| Explore Microsoft Graph API -> Claude integration use case | Azmain / BenVH | Next few weeks | Open |

## Stakeholder Signals
- BenVH is deeply passionate about Phantom Agent -- it is a five-year personal project that he has patented and sees as potentially life-changing if adopted by Moody's. He is also vulnerable, admitting trust issues around sharing his ideas. The Moody's situation is uniquely aligned with what he built.
- Azmain is immediately strategic about how to sell this internally: he thinks in terms of senior stakeholder narratives, corporate politics, and gradual seed-planting rather than direct technical pitches. He instinctively frames benefits in terms leadership cares about (cost control, security, enabling innovation without expensive hardware).
- Both share frustration with enterprise employees who complain without contributing. The startup mentality they share creates a strong working bond but could also lead to blind spots about corporate process requirements.
- Catherine Lady is identified as an active detractor of CLARA: flagging problems, never volunteering solutions, and creating negative sentiment in the IRP adoption chat.

## Open Questions Raised
- How would the RFI/RFP process work if BenVH comes in as a vendor to Moody's?
- Can the Microsoft Graph API integration be done within existing security approvals, or does it need a separate governance process?
- What is the right timing for the Melinda Trigerino demo -- before or after broader seed-planting with senior leaders?
- How does Phantom Agent relate to or compete with Moody's existing Maps team infrastructure?

## Raw Quotes of Note
- "I built this. I would honestly love for Moody's to actually use it. I have no idea how to even get that conversation going." -- BenVH, on the Phantom Agent opportunity
