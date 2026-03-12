# App Factory Standup
**Date:** 2026-03-11
**Attendees:** BenVH, Azmain Hossain, Richard Dosoo
**Duration context:** Medium (~28 minutes)
**Primary project:** App Factory
**Secondary projects:** CLARA, Build in Five

## Key Points
- BenVH is pivoting App Factory core to an MCP server architecture — this is the most significant architectural decision in weeks. Rather than a UI-driven platform, the entire App Factory becomes a middleware MCP server that any application (Martin's Build in Five, CLARA, Slidey, etc.) can consume
- The Nikhil conflict has escalated significantly. BenVH described daily boundary-crossing: Nikhil attempting to deploy without permission, introducing App Factory tasks to the CAT team, going directly to Richard about centralised logging after BenVH explicitly told him it was out of scope, and scheduling deployment meetings 30 minutes after being told no
- Richard and BenVH met with Asia/Pacific teams (Singapore, Japan, Australia) — strong interest in App Factory, which increases urgency for the MCP server approach
- BenVH is putting Nikhil's UI work on the back burner entirely — the MCP server makes a standalone UI unnecessary
- Richard is planning a direct confrontation with Nikhil about repeated boundary violations and also intends to escalate to Ben Brooks
- Strategy to neutralise Nikhil: redirect him to the Salesforce integration or AIG project, away from App Factory entirely
- BenVH explicitly stated he would prefer to work overtime himself rather than have Nikhil interact with any App Factory app
- Azure app registration completed for Slidey authentication (BenVH and Richard working through Azure privilege management live)
- Azmain acknowledged he needs to be more assertive about his programme management role, noting that RMS people are "weirdly conscious of rank"
- Richard pushed back strongly: Azmain's seniority is irrelevant, the decision was made for him to run it, and anyone with a problem can raise it directly
- BenVH expects MCP server to be complete by end of week — Martin will be the first integration proof of concept
- Two grads arriving in ~30 days (early April) to help with capacity

## Decisions Made
- App Factory core architecture pivoting to MCP server → BenVH
- Nikhil's UI work put on back burner — MCP server is the critical path → BenVH
- Nikhil to be redirected away from App Factory to Salesforce integration or AIG → Richard
- Martin's app will be the initial MCP server proof of concept → BenVH/Martin
- Richard to have direct conversation with Nikhil about boundaries → Richard
- Richard to escalate to Ben Brooks about Nikhil's behaviour → Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Complete App Factory MCP server | BenVH | End of week (14 Mar) | Open |
| Have direct boundary conversation with Nikhil | Richard | This week | Open |
| Escalate Nikhil behaviour to Ben Brooks | Richard | This week | Open |
| Set up App Factory Town Hall/Lunch and Learn for wider visibility | Richard | Next 2 weeks | Open |
| Redirect Nikhil to Salesforce integration or AIG project | Richard | This week | Open |
| Set up presentation to Dennis Clement (MD Digital Content), Dubai, Asia-Pac for App Factory showcase | Richard | Next 2-3 weeks | Open |
| Integrate Martin's Build in Five app with MCP server | BenVH/Martin | Next 2 weeks | Open |

## Stakeholder Signals
- **BenVH** — Anger and frustration at an all-time high. Used phrases like "blood boiling" and "taking too much of my mental acuity." Stated he has stopped responding to Nikhil's messages and cancelled his meeting invitations. Clear morale crisis — but channelling frustration into the MCP server pivot, which is productive
- **Richard** — Fiercely protective of BenVH. Ready for direct confrontation with Nikhil. Framing strategy to go "above and around" the local politics by getting BenVH in front of senior leadership (Dennis Clement, Dubai, banking, life, Asia-Pac)
- **Azmain** — Supportive of BenVH but also self-aware about needing to assert his own authority more visibly. Noted colleagues like Bernard recognise the App Factory but don't know who built it

## Open Questions Raised
- How to tactfully redirect Nikhil without creating an adversarial relationship?
- Will the MCP server approach satisfy the Asia-Pac teams' timeline expectations?
- Should Nikhil be told about the MCP server direction, or kept in the dark to "run out of road"?

## Raw Quotes of Note
- "I'm tired of fighting him on this. I think personally, I would like to see his time allocated somewhere else away from what I'm working on." — BenVH, on Nikhil
- "He's only been here six weeks... trying to take liberties and take credit for Ben's work." — Richard, on Nikhil's behaviour
- "Someone else's disrespect here is not an invitation for you to have to prove yourself." — Richard, to BenVH
