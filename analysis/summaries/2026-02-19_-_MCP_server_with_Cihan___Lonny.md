# MCP Server with Cihan & Lonny
**Date:** 2026-02-19
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brooks, Bala (Speaker 1 / new from banking/edfx), Cihan (Speaker 2), Lonny (Speaker 5), Nicole (Speaker 3)
**Duration context:** Long (~40 minutes)
**Workstreams touched:** WS5 Navigator L1, WS6 Build in Five

## Key Points
- Bala is introduced as the new tech consulting lead replacing Alex, joining from banking/edfx. Nikhil is also new on the team. Both will be key collaborators going forward.
- Bala demos his MCP server prototype, built as part of an incubator programme. It uses a graph constructed from ~18 Postman collections and developer portal documentation. It can suggest workflows, generate Python boilerplates for API calls, and execute APIs on behalf of users.
- Cihan pushes for the MCP server to reach GA (general availability) by June, viewing it as simply another interface (like APIs and UIs) that should be free and drive consumption.
- Ben Brooks is supportive of the GA target, suggesting a phased approach: partners-only first release, then broader rollout.
- The group debates whether the MCP server should be integrated into IRP Navigator or remain standalone. Cihan raises the question of Navigator becoming aware of the MCP server, which could lead to users wanting to operate everything from Navigator.
- Lonny identifies existing paths to GA: Docker deployment or CloudFlare (already set up with entitlements and SSO). Risk Labs is another option but not ready until April.
- Richard sees a key use case in wrapping the MCP server into the support workflow to answer support cases automatically -- Lonny enthusiastically endorses this.
- Azmain clarifies the architectural principle: MCP servers are strictly an API translation layer for LLMs; orchestration sits on top. The team aligns on this.
- Discussion of Cat Moss (AI dev tool) and its overlap with product roadmap -- Cihan wants to keep it scoped to avoid competing with other product teams.

## Decisions Made
- Target GA for MCP server by June 2026: agreed by all present -> Cihan / Lonny / Bala to drive
- MCP server should be free and treated as another interface, not a separately priced product -> Cihan
- Bala to get internal teams access to MCP server as fast as possible for experimentation -> Bala / Lonny
- Follow-up meeting in a fortnight for Richard to show what the CS team is doing on the sales side -> Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Get MCP server code into a GitHub repo | Bala / Richard | This week | Open |
| Deploy MCP server for internal team testing | Bala / Lonny | ASAP | Open |
| Set up follow-up meeting on sales demo use case | Richard | ~2 weeks | Open |
| Evaluate Docker vs CloudFlare vs Risk Labs deployment paths | Lonny / Bala | Next meeting | Open |

## Stakeholder Signals
- Cihan is pushing hard for productisation -- wants MCP server in customers' and support engineers' hands quickly.
- Lonny is pragmatic about deployment paths and wants speed over perfection.
- Ben Brooks is bullish on MCP as a driver of consumption and partner enablement.
- Bala is energetic and collaborative, keen to reduce duplication of effort across teams.

## Open Questions Raised
- Should IRP Navigator become aware of the MCP server, and what are the implications of that for product strategy?
- What happens with Cat Moss -- does it stay scoped or expand into product?
- How does the MCP server relate to the RDL execution environment?

## Raw Quotes of Note
- "Get it in our employees' hands as fast as you possibly can." -- Lonny, on the MCP server rollout urgency
