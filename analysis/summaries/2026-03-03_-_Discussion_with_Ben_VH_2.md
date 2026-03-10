# Discussion with Ben VH (Part 2)
**Date:** 2026-03-03
**Attendees:** Azmain Hossain, BenVH (Speaker 1), Ben Van Houten (briefly by name)
**Duration context:** Medium (~25 minutes)
**Workstreams touched:** App Factory / Infrastructure, Phantom Agent

## Key Points
- Continuation of the Phantom Agent discussion. BenVH provided a deeper technical walkthrough of what he has built -- an MCP server that orchestrates LLM workers anywhere with SSO integration, OU-based role assignment, budget controls, and model switching.
- Key capabilities demonstrated/described: (a) role-based access control per user or department for AI model tiers, (b) cost monitoring and token usage analytics per user/OU, (c) ability to switch the entire company from one AI provider to another with a configuration change, (d) budget limits that can downgrade models or stop provisioning when exceeded, (e) content monitoring (what data is being passed to agents).
- Azmain revealed that he runs Claude Code on a virtual environment (Anthropic infrastructure) and gives it full internet access. He described this as how he built Friday using 30 agents.
- BenVH flagged the security risk: Azmain's cloud environment is not in Moody's infrastructure, meaning proprietary data is being processed outside the company's control. This is exactly what Phantom Agent would solve.
- BenVH is testing Phantom Agent with his personal Cursor and personal AWS account. He offered to set up a test where Azmain can use it on a personal AWS account.
- Vendor lock-in concern raised: BenVH warned that building everything on Anthropic/Bedrock creates a dependency. At contract renewal, Anthropic has leverage. Phantom Agent enables provider-agnostic architecture.
- Azmain suggested downplaying the vendor lock-in argument and leading with cost control, as that is what senior executives are currently worried about.
- They agreed to set up a hands-on session (possibly Thursday) for Azmain to try Phantom Agent on a personal AWS environment.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Lead Phantom Agent pitch with cost control, not vendor lock-in | Strategic messaging | High | Azmain advising BenVH |
| Set up personal AWS test environment for Phantom Agent trial | Technical | High | BenVH |
| Azmain to start using Phantom Agent on personal environment | Exploration | Medium | Azmain |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Set up Phantom Agent test on personal AWS account | BenVH | Thursday (Mar 6) | Open | Medium |
| Walk Azmain through the setup and configuration | BenVH | Thursday (Mar 6) | Open | Medium |
| Guide Azmain on AWS account billing setup | BenVH | Same session | Open | Medium |

## Theme Segments
1. **Deep technical walkthrough** (0:00-8:00) -- Phantom Agent capabilities: SSO, OU-based roles, model assignment, monitoring
2. **Security and governance framing** (8:00-14:00) -- Why uncontrolled cloud environments are a risk; Azmain's Friday build as case study
3. **Cost control and vendor lock-in** (14:00-19:00) -- Strategic positioning of Phantom Agent value proposition
4. **Next steps and personal setup** (19:00-25:00) -- Planning the hands-on trial session

## Power Dynamics
- **BenVH shifts from pitch mode to demonstration mode.** He is more confident here, walking through his actual build rather than seeking permission.
- **Azmain continues as strategic advisor** but also becomes a potential user/customer for BenVH's product.
- **The dynamic is mutually reinforcing**: BenVH gets an internal champion, Azmain gets access to powerful tooling for his own work.

## Stakeholder Signals
- **BenVH** -- More confident in this session. Clearly proud of what he has built. The technical depth is impressive -- SSO integration, OU-based role management, budget controls. This is not vaporware.
- **Azmain** -- Shifts from advisor to enthusiast. Genuinely excited about using Phantom Agent. His desire for the tooling is personal (he is paying 200 GBP/month and burning Cursor budgets), which makes him an authentic champion.

## Commitments Made
| Who | Commitment | To Whom | Context |
|-----|-----------|---------|---------|
| BenVH | Set up test environment and walk Azmain through it | Azmain | Hands-on trial of Phantom Agent |
| Azmain | Set up personal AWS account for testing | Self/BenVH | Enable Phantom Agent trial |

## Meeting Effectiveness
| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 7 | Clear next step (Thursday session) agreed |
| Decision quality | 7 | Good strategic messaging alignment |
| Participation balance | 7 | More balanced than Part 1; BenVH leads technically |
| Action item specificity | 6 | Specific session planned but not confirmed |
| Strategic alignment | 8 | Directly addresses cost and governance gaps |

## Risk Signals
- **HIGH: Security exposure actively demonstrated.** Azmain confirms running Moody's work on Anthropic's uncontrolled cloud infrastructure with full internet access. This is exactly the kind of exposure the security audit caught.
- **MEDIUM: Personal AWS costs for testing.** BenVH will be paying for the test environment personally. More personal expenditure on corporate needs.
- **LOW: Vendor lock-in.** BenVH's concern about Anthropic dependency is legitimate but longer-term. Azmain correctly identifies cost as the more immediate lever.

## Open Questions Raised
- How will Phantom Agent integrate with Moody's existing AWS infrastructure vs. BenVH's personal setup?
- What is the deployment path from personal test to corporate adoption?
- How does this relate to the broader Moody's AI governance framework?

## Raw Quotes of Note
- "What if you had the option to, instead of clicking Friday, you click Moody's, and it auto provisions a resource in Moody's for you." -- BenVH, explaining Phantom Agent's core value proposition
- "Don't tell anybody. I run my Claude Code on a virtual environment. I give it full access to the internet." -- Azmain, revealing his development setup

## Narrative Notes
This Part 2 is the technical deep-dive that gives substance to Part 1's strategic discussion. What emerges is that Phantom Agent is genuinely impressive -- not a concept but a working prototype with SSO integration, role-based controls, budget management, and multi-cloud support. BenVH has been quietly building this for five years while being overlooked and under-credited. The irony is stark: Moody's has someone internally who has built exactly what the organisation needs for AI governance, but the corporate dynamics (Nikhil taking credit, Rhett getting visibility) threaten to render his contribution invisible. Azmain's admission about running Claude Code on uncontrolled cloud infrastructure with full internet access is the most concrete security exposure in the programme -- it validates everything the security audit flagged.
