# Tracker Standup
**Date:** 2026-02-23
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (Speaker 1)
**Duration context:** Long (~39 minutes)
**Workstreams touched:** WS2 CLARA, WS6 Build in Five, WS1 Training

## Key Points
- Cursor budget crisis: Azmain used $750 in three days. Corporate budget was increased from $10K to $20K but Opus 4.6 is 3x more expensive than previous models. Banking OU had a hackathon consuming tokens. Azmain's Claude Max subscription also ran out (cut off mid-build at 5pm sharp).
- Azmain downgraded to Sonnet 4.5 to manage costs. Ben helps him log into Windsurf (Moody's-approved) as a backup on a different billing cycle.
- Richard updates on Diya meeting: she is now supportive and wants the team to talk to Maps team about infrastructure alignment. The Maps team, which previously refused to help ("you're not important enough"), is now offering assistance since they see the team is producing results.
- Richard presents a six-layer consulting AI platform architecture: (1) Design layer (voice input via Whisper, B5 Studio, solutions database, guided workflow), (2) Data and tools (consulting IP/knowledge, MCP servers, skills library, Claude MD policy), (3) Prompt library, (4) Cursor/VS Code as IDEs, (5) App factory for deployment, (6) Content platform for SharePoint/metadata integration.
- Azmain raises concern about Natalia's message about needing more resources. Natalia has spoken to Ben and Diya about it -- resources expected to come.
- Chris from the team could help with CLARA maintenance at 50% capacity, handling smaller requests while Azmain focuses on big features (LLM integration, adoption charter, solution blueprint).
- BenVH's priorities: Idris's app first (relationship obligation), then Rhett. Steve and Eddie's apps deprioritised.
- Governance concern raised: without proper governance on the app factory, it will be a nightmare as people build redundant or low-value apps. Steve and Rhett already working on overlapping things.
- Richard spent his weekend rewriting Steve's code, only to discover Steve was independently updating it with Rhett. Frustration about wasted effort and lack of coordination.
- Content platform idea: extracting metadata from SharePoint and Salesforce, feeding it into the consulting AI platform so it can surface relevant presentations and assets contextually. Richard has a call with a colleague who already does this for Sales Recon.

## Decisions Made
- Azmain to use Windsurf as backup when Cursor budget runs out -> Azmain
- Chris to be requested at 50% for CLARA maintenance work -> Richard to request
- Nikhil at 50% also requested -> Richard
- Idris's app prioritised over all others for BenVH -> Richard / BenVH
- Wednesday standup will present programme overview to Diya with resource estimates added -> Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Get Bedrock / Claude API access sorted | Richard | Today | Open |
| Secure Windsurf access for Richard | Richard | Today | Open |
| Share priority spreadsheet with team | Richard | Today | Open |
| Send CLARA overview slides to Christoph for Life team meeting | Azmain | Today | Open |
| Call with M about content platform / SharePoint metadata extraction | Richard | 15 min today | Open |
| Formalise plan with resource estimates for Wednesday Diya session | Richard | By Wednesday | Open |

## Stakeholder Signals
- Azmain is on the edge of burnout: token budgets running out, subscription cut off mid-build, constant small requests from users.
- Diya has shifted from sceptical to supportive -- a major programme moment. The Maps team offering help is a direct result.
- Natalia is actively advocating for resources behind the scenes with Ben and Diya.
- Richard is frustrated by wasted effort on Steve's duplicative work but channelling it into governance discussions.

## Open Questions Raised
- How to control AI agent spend as usage scales up?
- What are the gating criteria for the app factory to prevent low-value builds?
- Will the Maps team alignment force a migration of infrastructure to their platform?

## Raw Quotes of Note
- "I used 750 bucks in three days." -- Azmain Hossain, on the Cursor token crisis
