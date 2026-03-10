# Build in Five Standup
**Date:** 2026-03-10
**Attendees:** Azmain Hossain, Martin Davies, Richard Dosoo (joined late)
**Duration context:** Long (~7,200 words)
**Workstreams touched:** WS6 Build in Five, App Factory

## Key Points
- **Martin's dashboard builder has made extraordinary progress.** The demo revealed a near-complete drag-and-drop dashboard builder with:
  - Three modes per component: Data (table), Visual (predefined charts), Custom (AI-prompted)
  - Full white-labelling: themes, dark mode, logos, branding colours, custom fonts, corner radius
  - Drag-drop layout, resizable panels, customisable titles, show/hide borders
  - Tab containers for multi-view dashboards
  - Live Risk Modeller API connection for the data sources component
  - Save/load dashboard configurations
  - Preview mode for clean dashboard viewing
- Richard compared it to **Databricks Genie** — a capability the product team has but refuses to show customers, and Martin rebuilt it independently
- **Critical next step**: plug in the **Navigator MCP server** (that Nicole/Bala built) to complete the loop — giving the builder live API definitions so users can query any Risk Modeller endpoint
- Richard outlined the **stakeholder engagement sequence**: 1) Get MCP server → 2) Show to tech consulting team (Bala, Lonnie, Alicia) → 3) Get Ben's buy-in → 4) Show to Mike Bibo and Sam Gibson (demo team) → 5) Show to Dan Flemington (sales) → 6) Exceedance content factory (Evan et al)
- Azmain flagged credit attribution: "We want to take credit for this. Martin has done this. Our team built this using AI." — governance awareness growing
- Richard's key strategic insight: the biggest CLARA adoption blockers are UI/UX problems — this dashboard builder is a **turnkey solution** for that. Customers saying "dashboards don't do what I need" is no longer a valid objection.
- Discussion about the full round-trip: data ingestion → modelling → dashboard building → export — all demonstrable in five minutes vs an 18-month integration project
- BenVH and Nicole need to be brought in — BenVH for App Factory deployment, Nicole for the MCP server repo access

## Decisions Made
- Next priority: plug Navigator MCP server into the dashboard builder → Martin
- Stakeholder engagement to follow the sequence: tech consulting → demo team → sales → exceedance content → Martin / Richard
- Martin's builder to be deployed to App Factory → BenVH (needs scheduling)

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Get access to Navigator MCP server repo from Nicole | Richard | This week | Open |
| Wire up MCP server integration to replace JavaScript agent stub | Martin | Next 2 weeks | Open |
| Set up meeting with Bala, Lonnie, and Alicia to show dashboard builder | Richard | Next week | Open |
| Get meeting with Mike Bibo / Sam Gibson (demo team) | Richard | Before exceedance | Open |
| Connect with Dan Flemington to show sales use case | Richard | TBD | Open |
| Deploy dashboard builder to App Factory | BenVH | TBD | Open |
| Contact Exceedance content factory (Evan) about demo script | Richard / Azmain | April | Open |
| Engage Steve Gentilli, Liz, Rhett as secondary stakeholders | Richard | TBD | Open |

## Stakeholder Signals
- **Martin Davies** — Quietly delivering at an exceptional level. The dashboard builder exceeded expectations. Methodical, doesn't oversell. Has capacity (Canopy work is light). His 12-week clock is ticking but the output justifies the investment many times over.
- **Azmain** — Shifting into programme manager mode. Thinking about credit attribution, stakeholder analysis, and governance. Building transcript analysis into Friday.
- **Richard** — Energised by Martin's output. Immediately mapped out the full stakeholder cascade and the strategic implications for adoption blockers. Sees the exceedance panel as the culmination of Build in Five's value proposition.

## Open Questions Raised
- Can the MCP server provide live API definitions dynamically, or will it need static OpenAPI spec files as a first step?
- When can BenVH schedule App Factory deployment for Build in Five?
- How will the exceedance demo format work — pre-canned vs live building?
- What about Nikhil's dependency on Martin's work?

## Raw Quotes of Note
- "You've basically rewritten Databricks Genie on your own in like a day, which is fantastic" — Richard to Martin
- "I challenge anyone to come and question the value of this once you plug it into the MCP server" — Richard
- "We want to take credit for this. Martin has done this. We don't want it to be like, we give it to product and they're like, oh look at this cool thing we built" — Azmain
