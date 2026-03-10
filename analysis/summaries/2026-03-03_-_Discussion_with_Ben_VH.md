# Discussion with Ben VH
**Date:** 2026-03-03
**Attendees:** Azmain Hossain, BenVH (Speaker 1)
**Duration context:** Long (~32 minutes)
**Workstreams touched:** WS2 CLARA, WS4 Adoption Charter, WS3 CS Agent (tangential)

## Key Points
- BenVH pitched his personal project "Phantom Agent" to Azmain -- an MCP server he built that can orchestrate LLM workers across any environment (AWS, Azure, GCP, on-prem, Kubernetes, local). He describes it as a universal orchestration layer for AI agents.
- BenVH's core concern: multiple apps in the pipeline want to spin up LLM workers, but there is no governance over where they run, who pays, or how they are monitored. Currently everything runs through one RMS AWS account with no cost allocation.
- Azmain showed BenVH his multi-agent build setup in Cursor: a tiered system (PM -> team leads -> workers) with up to 30 agents. He ran this to build a project management app called "Friday" and burned through his entire $500 cursor budget in one day.
- The adoption charter challenge was discussed in detail. Azmain received an actual adoption charter from a CSM manager and was shocked by its complexity -- it contains images (delivery plan diagrams), complex layouts, and information that LLMs cannot easily parse sequentially.
- Azmain needs the app to spin up a team of agents for OCR, image-to-text, and document parsing to handle adoption charters. This is exactly what Phantom Agent could do.
- BenVH is anxious about Nikhil potentially building something similar and getting credit. He wants to introduce Phantom Agent before others attempt to solve the same problem less effectively.
- Azmain advised BenVH on strategy: do NOT introduce Phantom Agent yet. Let the team feel the pain of uncontrolled LLM agent costs first, build something that works but is painful, and then propose Phantom Agent as the solution. This creates a stronger business case.
- BenVH revealed he has a patent on Phantom Agent technology.
- The upcoming standup meeting will be about onboarding Nikhil and Chris onto CLARA, not about LLM orchestration. Azmain told BenVH not to bring up Phantom Agent in that context.
- Azmain mentioned he built a new project management app ("Friday") and hopes to deploy it on App Factory.

## Decisions Made
- Hold off introducing Phantom Agent to the wider team until there is felt pain from uncontrolled LLM costs -> Azmain, BenVH
- Keep the standup meeting focused on onboarding Nikhil and Chris for CLARA feedback work -> Azmain
- BenVH to create a test environment for Phantom Agent within App Factory -> BenVH

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Sync with Richard on how to position Phantom Agent to Ben Brooks | BenVH/Azmain | TBD | Open |
| Create a test environment for Phantom Agent in App Factory | BenVH | TBD | Open |
| Keep Phantom Agent discussion away from the onboarding standup | Azmain/BenVH | 2026-03-03 | Open |

## Stakeholder Signals
- **BenVH** is deeply protective of his work and anxious about Nikhil encroaching on App Factory territory. His Phantom Agent project is genuinely sophisticated (role-based access, cost monitoring, SSO integration, multi-cloud orchestration).
- **Azmain** is strategically savvy about how to position BenVH's tech -- he understands the politics of making people feel pain before offering solutions. He is also personally invested in BenVH succeeding because it serves his own programme management goals.
- Both are paying personally for AI tools (Azmain: 200 GBP/month Claude subscription; BenVH: personal AWS costs for testing).

## Open Questions Raised
- How to formally introduce Phantom Agent without it being co-opted or replicated internally
- Where will LLM workers for CLARA and other apps actually run and who pays?
- How to handle the adoption charter parsing problem technically (OCR, multi-agent document analysis)

## Raw Quotes of Note
- "You can't be giving this away for free... one thing about business people, you can't give them the solution too early. They don't value it. They got to feel the pain first, and then they value the solution." -- Azmain, advising BenVH on commercialisation strategy
