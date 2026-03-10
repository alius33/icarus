# Discussion with Ben VH (Part 2)
**Date:** 2026-03-03
**Attendees:** Azmain Hossain, BenVH (Speaker 1)
**Duration context:** Medium (~25 minutes)
**Workstreams touched:** WS2 CLARA (tangential), App Factory / Infrastructure

## Key Points
- This is a continuation of the Phantom Agent discussion. BenVH gave a more detailed technical walkthrough of what Phantom Agent does.
- Core capability: an MCP server that provisions AI agents in any specified environment (AWS, Azure, GCP, vCenter, Kubernetes, local). It connects through SSO so an IT admin can assign users to specific cost centres and environments.
- Key features demonstrated/described: role-based model access (e.g., Azmain gets Opus, Rhett gets a cheaper model), OU-based cost allocation, token usage monitoring, per-user spend limits, automatic model downgrade when budgets are exceeded, audit trail of what data was passed to AI agents.
- BenVH framed the security risk: Azmain runs Claude Code on cloud environments (anthropic/Friday cloud infrastructure) where Moody's proprietary data could be exposed. Phantom Agent would redirect that work to Moody's-controlled AWS accounts instead.
- Azmain revealed he burned $500 of cursor allowance in one day spinning up 30 agents to build the Friday project management app on a cloud environment. He acknowledges the security implications but says there is no customer data involved.
- Cost control pitch: BenVH argued that as AI adoption scales, costs will become astronomical and Anthropic will have lock-in leverage. Phantom Agent allows switching AI providers (e.g., from Anthropic to Gemini) across the entire organisation.
- Azmain advised BenVH to lead with the cost control use case rather than the provider-switching use case when pitching to executives.
- They agreed to set up a session (possibly Thursday) where BenVH walks Azmain through setting up Phantom Agent on Azmain's personal AWS environment for testing.

## Decisions Made
- Lead Phantom Agent pitch with cost control narrative, not vendor lock-in -> Azmain's advice to BenVH
- Set up a personal AWS environment for Azmain to test Phantom Agent -> Azmain/BenVH

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Set up a session to configure Phantom Agent on Azmain's personal AWS | BenVH | ~Thursday 2026-03-06 | Open |
| Guide Azmain through AWS account billing setup | BenVH | TBD | Open |
| Test Phantom Agent with Cursor and Claude Code integration | Both | TBD | Open |

## Stakeholder Signals
- **BenVH** is testing Phantom Agent with his personal Cursor environment and personal AWS. He is clearly far along in development but has no organisational visibility or sponsorship yet.
- **Azmain** sees the strategic value immediately and wants to use it. He is impatient with the lack of proper tooling and is spending personal money to work around corporate limitations.
- The security implications of running work on external cloud environments are real -- Azmain admits the claim that no proprietary information is involved is "wildly a lie" (this comes out in a later transcript).

## Open Questions Raised
- Will BenVH's Phantom Agent work with Moody's AWS infrastructure and SSO?
- How to handle the billing and cost centre setup for a test environment
- Timeline for broader introduction to the team

## Raw Quotes of Note
- "I'm hearing like, all these apps going, introducing into app factory, launching their own LLM workers... where are all these AI agents going to live, who's going to be monitoring them?" -- BenVH, on the governance gap
