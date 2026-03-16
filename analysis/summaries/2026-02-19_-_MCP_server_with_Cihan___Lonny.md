# MCP Server with Cihan & Lonny
**Date:** 2026-02-19
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brookes, Bala (Speaker 1 / new from banking/edfx), Cihan (Jihan / Speaker 2), Lonny (Speaker 5), Nikhil (Speaker 3)
**Duration context:** Long (~40 minutes)
**Workstreams touched:** WS5 IRP Navigator / L1 Automation, WS6 Build in Five (tangentially)

## Key Points
- This is the first cross-functional meeting between the CS Gen AI programme team (Richard, Azmain, Ben Brookes) and the product team (Cihan/Jihan, Lonny, Bala) on MCP server development for IRP.
- Richard introduces Bala (new hire from banking/edfx) and Nikhil (new tech consulting lead replacing Alex) to the product team. Both will be key interfaces going forward.
- Bala demos an integration agent he has been building for the incubator programme. It uses a graph-based memory built from ~18 Postman API collections and developer portal documentation. It can suggest workflows, generate Python boilerplate code, and execute API calls on behalf of users.
- Cihan proposes shipping the first GA (General Availability) version of the MCP server by June, positioning it as a free interface (like APIs and UIs) that drives consumption rather than a separate paid product.
- Ben Brookes is "super bullish" -- suggests the first GA release could target partners only (internal + partners) to control rollout while accelerating the prime onboarding process.
- Lonny reveals there are already production MCP deployment paths available (Docker and CloudFlare) with SSO/entitlements already integrated. GA is not blocked by infrastructure -- risk labs experimentation is blocked until April (Suman's team).
- Key architectural debate: MCP server as pure API translation layer vs. an orchestration layer. Azmain and Bala agree MCP should be strictly an API extension, with orchestration happening in layers above it (LLM, IRP Navigator, etc.).
- Cihan raises the question of whether IRP Navigator should become aware of the MCP server, which would allow users to ask operational questions and execute workflows from within the existing interface. This creates a tension with RDL (Risk Data Lake) code execution environments.
- Brief discussion of Cat Moss (AI tool from the AS team). Cihan wants it folded into product/engineering rather than remaining standalone, to avoid overlap with existing product roadmap.
- Richard proposes using the MCP server to wrap into the support workflow for answering L1 support cases. Lonny gives his blessing enthusiastically.
- Bala's integration agent has no repo yet -- Richard offers to create one.
- Follow-up meeting planned in a fortnight for Richard to present the sales-side use case for increasing close rates.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Target June for first GA release of MCP server | Strategic timeline | High | Cihan (product decision) |
| MCP server will be free -- positioned as another consumption interface, not a paid product | Pricing/packaging | High | Cihan / Ben Brookes |
| MCP server should be strictly an API translation layer, not an orchestration layer | Architecture | High | Azmain / Bala / Cihan |
| Cat Moss to be moved into product/engineering team, not remain as AS standalone | Organisational | Medium | Cihan |
| First GA release could be partners-only to control rollout | Go-to-market | Medium | Ben Brookes (suggestion, not finalised) |
| Get MCP server into employees' hands as fast as possible (support engineers priority) | Deployment strategy | High | Lonny |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Create GitHub repo for Bala's integration agent | Richard | This week | Open | High |
| Deploy MCP server for internal team testing | Bala / Lonny | ASAP | Open | Medium -- deployment path exists but setup needed |
| Follow-up meeting on sales-side MCP use case | Richard | ~2 weeks (~5 Mar) | Open | Medium |
| Discuss whether IRP Navigator should integrate with MCP server | Cihan / Lonny / Bala | Next meeting | Open | Medium |
| Evaluate Docker vs CloudFlare vs Risk Labs deployment paths | Lonny / Bala | Next meeting | Open | Medium |
| Wrap MCP server into support workflow for L1 case resolution | Richard / Bala | TBD | Open | Low -- early stage |
| Provide Bala document for local MCP server setup | Bala | Immediate | Open | High |

## Theme Segments
| Time Range | Theme | Key Participants |
|------------|-------|-----------------|
| 0:00-3:30 | Introductions: Bala and Nikhil to product team | Richard (facilitating) |
| 3:30-6:15 | Context setting: why CS team wants to build on IRP APIs for demos and pipeline | Richard, Ben Brookes |
| 6:15-11:00 | Bala demos integration agent and MCP server capabilities | Bala (dominant), Cihan |
| 11:00-14:50 | Architectural debate: MCP as API layer vs orchestration; Azmain's key intervention | Azmain, Bala, Cihan |
| 14:50-20:00 | Bala continues demo: web UI wrapper, context management, token compaction | Bala |
| 20:00-26:30 | Strategic product discussion: IRP Navigator integration, Cat Moss, product roadmap conflicts | Cihan, Ben Brookes, Richard |
| 26:30-33:30 | Deployment paths: risk labs, Docker, CloudFlare, GA feasibility | Lonny (authoritative), Cihan |
| 33:30-40:30 | Wrap-up: repo creation, support workflow use case, follow-up meeting | Richard, Lonny |

## Power Dynamics
- **Cihan (Jihan) holds product authority** -- he is the one setting the June GA target and making packaging decisions. His word carries clear weight with the group.
- **Ben Brookes operates as the commercial strategist** -- pushes for GA, frames it commercially (consumption driver), suggests partners-only rollout as risk management. His contributions are concise and high-impact.
- **Lonny provides infrastructure authority** -- he knows exactly what deployment paths exist and what is blocked. His "you have my blessing" on the support workflow integration is a genuine green light from someone who controls technical gates.
- **Bala is the technical demonstrator** -- most speaking time, showing capability. Eager to collaborate and explicitly states he needs this capability as much as anyone else.
- **Richard is the connector** -- introduces people, frames the CS use case, proposes concrete next steps. Not the decision-maker here but the facilitator between CS needs and product delivery.
- **Azmain makes a single but architecturally important point** -- MCP as strict API translation layer. Brief but influential intervention.
- **Nikhil asks probing technical questions** about MCP server scope (workflow APIs vs all APIs, client-side execution). Positioning himself as a technical contributor in a new team.

## Stakeholder Signals
- **Cihan:** Committed to shipping. Thinking carefully about product boundaries -- does not want Cat Moss overlapping with roadmap. Concerned about IRP Navigator's role in the agentic future. Decisive leadership.
- **Ben Brookes:** Commercially bullish. Sees MCP as consumption driver. Thinking about the fundamental question of what Moody's business model looks like in an agentic world -- people asking questions "because it's easy, rather than because they have to."
- **Lonny:** Supportive and action-oriented. Has been wanting MCP in employees' hands for six months. Not blocking -- actively accelerating. Infrastructure is further along than most in the meeting realised.
- **Bala:** Highly capable technically. Built something impressive from the incubator programme. Eager to collaborate and reduce duplication of effort. A genuine asset if properly integrated.
- **Richard:** Focused on the CS use case: demo velocity for pipeline conversion, support case automation. Positioning CS as a consumer and integrator of the MCP server, not a competitor.
- **Azmain:** Brief but aligned. His architectural point about MCP as a translation layer shows clear thinking about system boundaries. Notably less talkative than usual -- possibly saving energy for other discussions this week.

## Commitments Made
| Commitment | Who | To Whom | Specificity |
|------------|-----|---------|-------------|
| Target June for GA MCP server | Cihan | All present | Specific month |
| Create repo for Bala's integration agent | Richard | Bala | Implied immediate |
| Follow-up meeting in a fortnight on sales use case | Richard | Lonny / product team | ~2 weeks |
| Get MCP into support engineers' hands ASAP | Lonny | Richard | Urgency but no specific date |
| Provide document for local MCP setup | Bala | Nikhil | Immediate |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of purpose | 4 | Clear goal: align CS and product teams on MCP server direction |
| Decision quality | 4 | June GA target, pricing, architecture decisions all substantive and well-reasoned |
| Participation balance | 4 | Multiple voices contributing meaningfully; Bala and Cihan dominant but appropriately so |
| Action item specificity | 3 | Several actions but timelines vague beyond "June" and "fortnight" |
| Time efficiency | 3 | Ran over time, but content was substantive throughout |
| **Overall** | **3.6** | Productive cross-team alignment session that generated real decisions |

## Risk Signals
| Risk | Severity | Type |
|------|----------|------|
| MCP server GA by June is ambitious given infrastructure dependencies (risk labs not ready until April) | MEDIUM | Delivery |
| IRP Navigator integration question unresolved -- could become a product direction conflict | HIGH | Strategic |
| Cat Moss overlap with product roadmap creates organisational friction between AS and product teams | MEDIUM | Organisational |
| Bala's integration agent has no repo, no version control -- brilliant but fragile individual work | HIGH | Technical |
| CS team's support workflow integration is early-stage with no defined scope or resources | LOW | Scope |
| Code execution environments (RDL, sandboxes) for agentic workflows are architecturally unresolved | HIGH | Architecture |
| 70% of clients are not technically advanced enough to use MCP in IDE -- adoption barrier for GA | MEDIUM | Market |

## Open Questions Raised
- Should IRP Navigator become aware of the MCP server and enable operational execution from within?
- What is the right boundary between MCP server capabilities and RDL code execution?
- Should the first GA release target partners only or all customers?
- How does the MCP server interact with Cat Moss capabilities without creating product overlap?
- What happens when customers want to execute workflows (not just query data) through the MCP server -- who provisions the sandboxes?
- Can the web UI wrapper that Bala built become the delivery mechanism for less technical clients?

## Raw Quotes of Note
- "We should think of MCP servers as literally just another extension of the API layer." -- Azmain Hossain, establishing the architectural principle
- "I generally feel like we should be ready in June to be able to kind of push something out of your experiment." -- Cihan, setting the GA target
- "I want every support engineer to have this at their fingertips." -- Lonny, on the urgency of internal deployment
- "I don't think people gonna wait hours for models to run when you're talking to an agent to try and get an answer." -- Ben Brookes, on the fundamental shift in how the business model works in an agentic world
- "Necessity is the mother of invention, right?" -- Lonny, closing the meeting

## Narrative Notes
This is arguably the most strategically significant meeting of Week 7. It represents the first genuine convergence between the CS Gen AI programme and the product team on MCP server development. The alignment is remarkably clean: both sides agree on architecture (MCP as API translation layer), pricing (free), and urgency (June GA).

The real tension lies beneath the surface. Cihan's question about IRP Navigator's relationship to the MCP server reveals a product strategy fork that has not been resolved: if Navigator becomes MCP-aware, it becomes a general-purpose agent interface, which raises questions about execution environments, cost allocation, and product boundaries. Lonny's revelation that CloudFlare deployment paths already exist with SSO integration suggests the team has been underestimating how close they are to GA -- the blocker is not infrastructure but product decisions.

Ben Brookes's comment about what the business looks like "in an agentic universe" is a rare moment of strategic candour from a senior leader. He is grappling with the fundamental shift: when querying data becomes frictionless, consumption patterns change, and the monetisation model may need to change with it. His suggestion of partners-only GA is pragmatic risk management that also serves as a commercial wedge.

The Cat Moss discussion is a microcosm of a common enterprise problem: autonomous teams building overlapping capabilities. Cihan's firm stance on consolidating it under product/engineering is the right organisational move, but the political implications -- taking a tool away from the AS team and folding it under a different ownership structure -- are left unaddressed.

Bala emerges as a genuinely impressive technical contributor. His integration agent, built from 18 Postman collections, demonstrates the kind of rapid prototyping that the programme aspires to make routine. The fact that it has no repo and no version control is a familiar pattern in this programme -- brilliant individual work that is fragile and un-institutionalised. Getting it into a repo and into the hands of support engineers will be the test of whether this can scale beyond its creator.

The 70% figure Bala mentions -- that 70% of clients are not technically advanced enough to navigate an IDE -- is a critical market insight that should inform the GA rollout strategy. The web UI wrapper Bala built is not a nice-to-have; it may be the primary consumption interface for the majority of customers.
