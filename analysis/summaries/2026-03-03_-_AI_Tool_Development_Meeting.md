# AI Tool Development Meeting
**Date:** 2026-03-03
**Attendees:** Azmain Hossain, Martin Davies
**Duration context:** Medium (~28 minutes)
**Workstreams touched:** WS6 Build in Five

## Key Points
- Azmain and Martin discussed the architecture and vision for the customer-facing pre-sales component of Build in Five, distinct from the internal app factory side that BenVH and Nikhil will work on.
- Martin showed his Apollo dashboard -- a working prototype that visualises EDM/RDM data by country, peril, and layer (location, AL, curves, RDS). This becomes the reference implementation for Build in Five.
- The agreed MVP concept: a modular UI where a pre-sales person drags and drops IRP API modules (e.g., windstorm, hurricane, location API) onto a foundation layer. Each module gets two tabs -- raw data (exportable as CSV) and an auto-generated intelligent dashboard.
- Phase 1 scope: three modules with a foundation layer and drag-and-drop UI. Phase 2: combined dashboards across modules.
- Azmain explicitly ruled out AI/LLM functionality in the app to avoid cost spiralling -- it should be a straightforward localhost app.
- Martin's Apollo dashboard already demonstrates the end-to-end workflow: drop a database file into a watch folder, the system identifies countries/perils, pulls appropriate models, generates results and displays a dashboard.
- Azmain advised Martin to start from a blank folder without cursor rules, to avoid context window bloat.
- Budget: Azmain's cursor budget reset March 1. He and Richard are paying 200 GBP/month personally for Claude. Martin has no Claude licence. Azmain's Anthropic API key via AWS is not working (IAM role issue).
- Azmain's dev approach: use Opus for planning/thinking, Sonnet for building. Do one big initial build, then fine-tune.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Build in Five pre-sales tool starts from scratch, not iterating existing code | Technical | High | Azmain |
| MVP scope: three modules + foundation layer + basic UI | Scope | High | Azmain, Martin |
| No AI/LLM integration in the app (cost control) | Technical/Financial | High | Azmain |
| Martin focuses exclusively on customer-facing pre-sales; internal app factory goes to BenVH/Nikhil | Resource allocation | High | Azmain |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Identify three initial API modules for MVP | Martin | TBD | Open | High |
| Build foundation layer and modular drag-and-drop UI | Martin | TBD | Open | High |
| Create assets folder with Moody's colours and logo | Azmain | TBD | Open | Medium |
| Show progress to Richard and Ben Brooks for feedback | Martin/Azmain | TBD | Open | High |

## Theme Segments
1. **Tooling and environment setup** (0:00-5:00) -- Discussion of Cursor, Claude, budget constraints, API keys
2. **Build in Five vision and scope** (5:00-10:00) -- Defining the pre-sales vs internal distinction, modular architecture
3. **Apollo dashboard reference** (10:00-22:00) -- Martin demonstrates prior work, establishes target for reverse-engineering
4. **Development approach and next steps** (22:00-28:00) -- How to prompt, budget management, model selection

## Power Dynamics
- **Azmain directs Martin's scope.** Despite Martin being more technically experienced (built Apollo dashboards at prior job), Azmain sets the vision, scope boundaries, and development approach. Martin accepts guidance readily.
- **Azmain positions himself as the programme gatekeeper** for what gets built and how, even for workstreams he is not directly executing.
- **Martin is deferential but competent.** He has substantive prior work that validates the concept but does not assert ownership over the direction.

## Stakeholder Signals
- **Azmain** -- Energised about the pre-sales concept, sees it as a "massive win." Managing budget anxiety. Comfortable giving direct technical and strategic guidance to Martin.
- **Martin** -- Eager, has directly relevant prior work (Apollo). Low cursor usage (1 request vs Azmain burning through budget). Willing to learn and follow Azmain's lead. No Claude licence -- a gap.

## Commitments Made
| Who | Commitment | To Whom | Context |
|-----|-----------|---------|---------|
| Martin | Build MVP with three modules from scratch | Azmain | Core Build in Five deliverable |
| Martin | Summarise approach and share with Ben Brooks | Richard (mentioned) | Exceedance demo planning |
| Azmain | Provide assets folder (logos, colours) | Martin | Design consistency |

## Meeting Effectiveness
| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 8 | Clear MVP scope and division of labour agreed |
| Decision quality | 7 | Good scope freeze, but timeline left entirely open |
| Participation balance | 6 | Azmain dominates; Martin mostly asks and receives |
| Action item specificity | 5 | Actions defined but no deadlines set |
| Strategic alignment | 7 | Aligns with Exceedance demo goal but timeline risk not addressed |

## Risk Signals
- **Martin has no Claude licence and no personal budget** -- dependency on Cursor alone limits his velocity
- **No timeline set for MVP delivery** -- Exceedance is in May with April content deadline, but no schedule discussed
- **Azmain's API key not working** -- broader IAM role issue that could block Bedrock integration
- **Budget burn rate** -- Azmain burning personal and corporate budget at unsustainable pace

## Open Questions Raised
- How do IRP model licences work in practice -- per-model or per-API?
- What should the three initial modules be?
- Will the Anthropic API key issue get resolved for Martin?

## Raw Quotes of Note
- "I don't want to put in AI stuff, because the moment you start putting that in, the costs just spiral." -- Azmain, on keeping the MVP simple
- "One of the asset management guys was like, No, you can downgrade to sonnet. And I was like, what am I, a peasant?" -- Azmain, on model selection philosophy

## Narrative Notes
This meeting establishes the creative and technical direction for Build in Five's customer-facing component. The most significant outcome is that Martin's Apollo dashboard -- a fully functional prototype from his previous role -- becomes the reference implementation, which dramatically de-risks the build. Rather than building from abstract requirements, Martin will reverse-engineer something he already created, essentially "cheating" the demo. The No-AI decision is pragmatic but also strategic: it keeps the app lightweight and avoids the cost governance problems plaguing other parts of the programme. The absence of any timeline discussion is concerning given the Exceedance deadline.
