# App Factory Discussion
**Date:** 2026-03-11
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH
**Duration context:** Medium (~22 minutes)
**Primary project:** App Factory
**Secondary projects:** CLARA (IRP Adoption Tracker), Build in Five

## Key Points
- BenVH demoed the App Factory MCP server architecture — every application (CLARA, Slidey, Build in Five) will connect to a central MCP server instead of building their own AI/LLM pipelines
- The MCP server manages AI worker lifecycle: apps request a worker, App Factory spins it up and returns a connection. Apps stay "inherently dumb" and focus on their core function
- Inter-app communication solved: e.g., CLARA builds an MD file, sends it to Slidey via App Factory, Slidey generates the PowerPoint. Azmain flagged this as critical and BenVH asked him to write it up
- Any user with Cursor can connect to the App Factory MCP server, say "create a new project," and get a skeleton application with pre-baked Cursor rules spun up immediately
- BenVH acknowledged this is architecturally very similar to Phantom Agent — the LLM worker orchestration is the core overlap
- Richard proposed a SharePoint knowledge layer: PowerShell scripts to catalogue 10 years of consulting documents, intelligent tagging via Purview, vector database with MCP server on top for RAG queries
- The SharePoint pipeline would profile document trees, tag metadata, apply permissions, and let Slidey pull real consulting IP instead of generating content from scratch
- Cost concern raised by Azmain about analysing 10 years of documents — Richard clarified the pipeline breaks into stages (profiling, tagging, MCP navigation) that don't all need LLM compute
- BenVH noted the MCP server enables cross-OU adoption: any OU can pick up and use App Factory, which is the biggest selling point
- Planning a meeting next Wednesday with senior people to launch App Factory publicly — Richard wants Ben (Brooks) to present the MCP server there
- Richard is working on Slidey changes tonight, deploying locally before pushing
- BenVH plans to make existing per-app AI workers easy to lift-and-shift onto the centralized MCP server, including API key management per app
- Azmain raised the question of getting Phantom Agent adopted by Moody's — BenVH sees a path where App Factory becomes an MCP client of Phantom Agent for enterprise-wide AI agent governance

## Decisions Made
- App Factory MCP server is the central middleware for all apps — no more per-app LLM pipelines (BenVH/Richard/Azmain, unanimous)
- Any reusable process should be moved from individual apps into the App Factory MCP server to increase cross-app and cross-OU reusability (BenVH, explicit)
- SharePoint knowledge cataloguing is the next major data initiative: profile documents, tag, vector DB, MCP on top (Richard, proposed)
- Wednesday meeting next week to publicly launch App Factory with senior stakeholders (Richard, explicit)
- Inter-app communication (CLARA-to-Slidey flow) to be written up and prioritised (BenVH requested from Azmain)

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Write up inter-app communication requirements (CLARA → Slidey flow) | Azmain | This week | Open |
| Complete App Factory MCP server for Martin integration | BenVH | End of week | Open |
| Make per-app AI workers easy to migrate to centralized App Factory MCP | BenVH | Ongoing | Open |
| Work on Slidey changes and deploy locally | Richard | Tonight (11 Mar) | Open |
| Schedule Wednesday meeting for App Factory launch with senior stakeholders | Richard | 12 Mar | Open |
| Reach out to George and other CS contacts for Wednesday meeting | Azmain | 12 Mar | Open |

## Stakeholder Signals
- **BenVH** — Energised and articulate when presenting the MCP architecture. Clearly in his element when talking technical architecture. The Phantom Agent connection shows he sees App Factory as a stepping stone to his broader vision. Productively channelling the Nikhil frustration into technical output.
- **Azmain** — Grasping the implications immediately. His inter-app communication insight (CLARA → Slidey) was the most commercially relevant idea in the conversation. His second-order thinking about cloud costs shows growing maturity. Excited about the possibilities.
- **Richard** — Thinking strategically about the SharePoint knowledge layer as consulting IP monetisation. His framing of the Wednesday meeting as the opportunity to "cut out the bullshit" and establish App Factory publicly shows political sophistication. Already working on Slidey himself.

## Open Questions Raised
- How much cloud credit will it cost to analyse 10 years of SharePoint documents? (Azmain — partially answered by Richard's staged approach)
- Can Phantom Agent be slid into the Moody's governance framework via App Factory? (Azmain)
- What's the Purview/MDM solution for SharePoint document tagging? (Richard — conceptual, not yet selected)
- How to handle API key management per app through the centralized MCP server? (BenVH — in progress)

## Raw Quotes of Note
- "Every app goes to the app factory for whatever it needs." — BenVH, on the MCP server vision
