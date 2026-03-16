# Moody's Virtual Environments with BenVH — Phantom Agent Deep Dive
**Date:** 2026-02-26
**Attendees:** Azmain Hossain, BenVH (Ben Van Houten)
**Duration context:** Long (~43 minutes)
**Workstreams touched:** WS6 Build in Five, WS2 CLARA, Infrastructure/Governance

## Key Points
- BenVH reveals Phantom Agent -- his personal, patented CICD orchestration solution that has been five years in development. He has now adapted it for AI agent governance, which he sees as a much larger opportunity than its original CICD purpose.
- Phantom Agent's core capability: dynamically provision isolated environments (AWS EC2, ECS, Kubernetes) for AI agents based on team membership (via SSO). IT admins can control which resources each team can access, set cost caps per team, and monitor usage per agent/team/user.
- Key problems it solves: (1) cost control for AI agent spend, (2) security governance -- agents run in controlled environments, not on developer laptops, (3) developer hardware bottleneck -- non-developer laptops cannot handle heavy AI workloads, (4) audit trail for what agents are doing and spending.
- Phantom Agent is itself an MCP server, meaning any LLM (Cursor, Claude, etc.) can invoke it to provision environments dynamically.
- BenVH is emotionally invested. He describes it as potentially life-changing if Moody's adopts it, but he does not want Moody's to own it -- he wants to be a vendor/licensor.
- Azmain immediately sees the value proposition: instead of buying $5K dev laptops for everyone, use Phantom Agent to provision cloud environments at a fraction of the cost. Sell it as "the cost of one laptop can run this for 1,000 people for a month."
- Azmain proposes a seeding strategy: plant questions with decision-makers about AI cost control and developer hardware limitations, then reveal the solution weeks later when the questions have percolated.
- BenVH has a meeting scheduled with Melinda Trigerino (AI governance lead). Azmain advises delaying until there is a working demo using Moody's AWS Bedrock API as proof point.
- Discussion of Moody's Claude wrapper -- Azmain wants to build a non-technical user interface (like Claude Code for Desktop but using Bedrock). BenVH's Phantom Agent would handle the cloud environment provisioning behind it.
- Microsoft Graph API integration discussed: connecting to Outlook, SharePoint, Teams via SSO to give Claude access to Moody's internal data -- something Copilot does poorly.
- Kathryn Palkovics Lady called out again as an active CLARA detractor -- flagging issues, never volunteering solutions. Stacy ends up doing manual cleanup work that Kathryn Palkovics should be doing.
- BenVH warns about bringing wrong people onto the team: enterprise employees who complain rather than build will slow everything down.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Delay Melinda Trigerino meeting until working Bedrock demo ready | Tactical | High | BenVH / Azmain |
| Use Moody's AWS Bedrock API as Phantom Agent proof point | Strategic | High | BenVH |
| Seed questions about AI cost control with decision-makers before revealing solution | Political | Medium | Azmain |
| Build non-technical Claude wrapper using Bedrock (long-term) | Product | Low | Azmain |

## Action Items
| Action | Owner | Deadline | Confidence | Status |
|--------|-------|----------|------------|--------|
| Test Bedrock API key with Phantom Agent | BenVH | This week | High | Open |
| Build working Phantom Agent demo using Moody's Bedrock | BenVH | Next 2 weeks | Medium | Open |
| Start planting seed questions with decision-makers about AI cost control | Azmain | Next week | Medium | Open |
| Give Azmain access to Atlas (Phantom Agent UI) for testing | BenVH | When ready | Medium | Open |
| Explore Microsoft Graph API MCP server for email/SharePoint access | BenVH / Azmain | Future | Low | Open |

## Theme Segments
1. **Phantom Agent reveal** (0:00-14:00) -- BenVH demonstrates the solution, explains SSO integration, team provisioning, cost control
2. **Value proposition for Moody's** (14:00-22:00) -- Cost of laptops vs cloud environments, security governance, audit trail
3. **Go-to-market strategy** (22:00-32:00) -- Seeding questions, delaying Melinda meeting, working demo as proof point
4. **Claude wrapper and Graph API** (32:00-38:00) -- Non-technical interface, Copilot replacement, Bedrock as backend
5. **Team culture and detractors** (38:00-43:00) -- Kathryn Palkovics Lady behaviour, enterprise hiring risks, graduate strategy

## Power Dynamics
- **BenVH is vulnerable in this conversation.** He is sharing a deeply personal, five-year passion project with someone relatively junior. The trust dynamics are significant.
- **Azmain becomes the strategic adviser.** He immediately sees the go-to-market angle, proposes the seeding strategy, and frames the value proposition in terms leadership would understand.
- **The power balance has shifted** from BenVH-as-infrastructure-authority to a more collaborative peer dynamic. Azmain's product thinking complements BenVH's technical depth.

## Stakeholder Signals
- **BenVH:** Passionate, vulnerable, five years of personal investment in Phantom Agent. Trust issues around sharing IP. Wants Moody's to use it but not own it -- vendor/licensor model. This is personally and financially significant to him.
- **Azmain Hossain:** Immediately grasps the strategic value. Proposes the political seeding strategy. Frames the cost argument in terms executives understand. Growing into a strategic partner role.
- **Melinda Trigerino (absent, referenced):** AI governance lead. BenVH reached out after hearing her name in the Edward/Amanda meeting. Key gatekeeper for any AI tool adoption.
- **Kathryn Palkovics Lady (absent, referenced):** Called out again as a detractor who creates problems without contributing solutions.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| BenVH | Test Bedrock API with Phantom Agent | Azmain | High |
| BenVH | Build working demo for internal pitch | Azmain | Medium |
| Azmain | Plant seed questions with decision-makers | BenVH | Medium |
| BenVH | Give Azmain access to Atlas for testing | Azmain | Medium |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of purpose | 3 | Started as environment discussion, evolved into Phantom Agent pitch |
| Decision quality | 4 | Good strategic decisions about demo-first approach |
| Engagement | 5 | Both deeply engaged, building on each other's ideas |
| Follow-through setup | 3 | Actions identified but timelines loose |
| Time efficiency | 2 | 43 minutes with significant tangential discussion |

## Risk Signals
- **BenVH retention risk is real.** Five years of personal investment in Phantom Agent. If Moody's does not recognise or compensate this, and if Nikhil continues taking credit for his other work (App Factory), BenVH could leave. He is the only person who can deploy.
- **IP ownership ambiguity.** BenVH built Phantom Agent personally and patented it. If Moody's claims it as work product, the relationship could sour. The vendor/licensor model needs careful legal navigation.
- **Phantom Agent demo dependency.** If the Bedrock API key does not work with Phantom Agent, the demo strategy collapses and the Melinda meeting becomes premature.
- **AI governance process is opaque.** BenVH's previous intake form went unanswered for two weeks. Melinda only responded when contacted directly.

## Open Questions Raised
- How does Phantom Agent integrate with Moody's existing security and compliance frameworks?
- What is the licensing/vendor model for BenVH's personal IP within Moody's?
- Can the Microsoft Graph API be used via MCP server to replace Copilot functionality with Claude?
- Will Moody's ever approve Claude for Desktop or Claude Co-work for enterprise use?

## Raw Quotes of Note
- "I built this. I patented it... I would honestly love for Moody's to actually use it... but I don't want Moody's to own it" -- BenVH, on Phantom Agent's personal significance
- "This would frankly change my life" -- BenVH, on Moody's becoming a customer for Phantom Agent
- "The cost of one person's laptop, like five grand, you can run this whole system for like 1,000 people for a month" -- Azmain, framing the value proposition
- "She is maliciously trying to just undermine everything" -- Azmain, on Kathryn Palkovics Lady (repeated from tracker standup)

## Narrative Notes
This is the most personally significant conversation of the week. BenVH opens up about Phantom Agent -- a five-year passion project that he has now adapted from CICD orchestration to AI agent governance. His vulnerability is palpable: he trusts Azmain enough to share something he has not shared widely. The solution addresses real problems the programme faces (cost control, security governance, developer hardware limitations), and Azmain's immediate grasp of the go-to-market strategy shows his growing strategic maturity. The vendor/licensor question is delicate -- BenVH wants compensation for his IP without Moody's claiming ownership. If handled well, this could become a genuine innovation story. If handled badly, BenVH has another reason to leave, and the programme loses its only infrastructure person. The seeding strategy (plant questions about cost control, then reveal the solution) is politically savvy but requires patience that the programme may not have.
