# AI Infrastructure — Technical Planning Session
**Date:** 2026-02-26
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH, Rahul, Nikhil, Chris Moorhouse
**Duration context:** Long (~33 minutes, partial transcript)
**Workstreams touched:** WS2 CLARA, WS3 CS Agent, WS5 Navigator L1

## Key Points
- Dual-purpose session: (1) Cat Accelerate tech debt decisions, and (2) enabling AI infrastructure (Bedrock, Claude Code access) for the team.
- Cat Accelerate tech debt surfaced: no separate non-prod AWS account, CDK deployment is fragile and monolithic, step functions created manually with no backup or traceability. Nicole proposes separate AWS account for non-prod as top priority.
- BenVH raises the critical testing gap: no proper unit tests or integration tests for Cat Accelerate. Verification relies on ad-hoc Postman collections of uncertain currency. This has been a four-year problem.
- Rahul proposes a prioritisation framework for tech debt: value delivered and risk mitigation, overlaid with capacity constraints. He and Nikhil will produce a first-pass priority list.
- Richard presents the three-pillar programme overview to Nikhil and Chris for the first time: IRP portfolio governance, platform embedded intelligence, internal productivity and revenue acceleration.
- L1 ticket automation concept explained in detail: agents managing Salesforce queue, answering via Navigator, routing to customers if confidence threshold met, escalating to humans if not. OpenClaw or Copilot Studio identified as potential agent frameworks.
- Automated fixer agent concept raised for Cat Accelerate: agents debugging issues using CloudWatch logs and GitHub repos, submitting PRs for human review (never auto-approving). BenVH designed his approach to be flexible enough for any application workflow.
- Sales Recon data pipeline confirmed as disappointing: Bernard's UAT revealed missing parent-to-child hierarchy, wrong date query results, outdated SSO SAML status. Team now building their own interim pipeline.
- Nikhil and Chris formally onboarded to the programme: Nikhil to help with platform embedded intelligence, Chris on bug fixes and testing.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Separate non-prod AWS account as top priority for Cat Accelerate | Infrastructure | High | Nikhil / Richard |
| Evaluate CDK vs simple CloudFormation for Cat Accelerate deployment | Architecture | Medium | Nikhil / BenVH |
| Stay on AWS for Cat Accelerate (no Azure migration) given decommission timeline | Infrastructure | High | Nikhil |
| Prioritise tech debt by value delivered and risk mitigation | Process | High | Rahul / Nikhil |
| AI agents must only submit PRs, never auto-approve | Governance | High | BenVH |
| Build interim data pipeline from Salesforce/Mixpanel since Sales Recon UAT failed | Tactical | High | Richard |

## Action Items
| Action | Owner | Deadline | Confidence | Status |
|--------|-------|----------|------------|--------|
| Produce first-pass tech debt priority list with risk assessment | Rahul / Nikhil | Next week | High | Open |
| Schedule 30-min call with Richard to present tech debt rationale | Rahul / Nikhil | Next week | High | Open |
| Get capacity view from Stacy for team bandwidth overlay | Rahul | Next week | High | Open |
| Send CLARA GitHub repo and app link to Chris | Richard / Nikhil | Today | High | Open |
| Enable Bedrock Claude models in AWS environment | BenVH / Richard | This week | High | Open |
| Give team members access to Claude Code via Bedrock | Richard / BenVH | This week | High | Open |
| Scope L1 ticket automation: agent framework selection, throughput testing | Chris / Nikhil | Next 2-4 weeks | Medium | Open |

## Theme Segments
1. **Cat Accelerate tech debt** (0:00-15:00) -- AWS accounts, CDK fragility, testing gap, prioritisation framework
2. **Programme overview for new team members** (15:00-27:00) -- Three pillars, CLARA context, data pipeline requirements
3. **L1 automation and agent concepts** (27:00-33:00) -- Navigator agent, automated fixer agent, security considerations

## Power Dynamics
- **Rahul is a structured, action-oriented new voice.** His prioritisation framework (value + risk mitigation + capacity) brings engineering discipline to what has been ad-hoc.
- **BenVH is the infrastructure authority.** His testing gap admission is significant -- it means every infrastructure change is high-risk. His flexible agent design thinking is impressive.
- **Nikhil is being positioned as the tech debt lead** for Cat Accelerate. He and Chris are the first formal additions to the team's capacity.
- **Richard provides programme context** but defers to technical leads on implementation decisions.

## Stakeholder Signals
- **Rahul:** Structured and action-oriented in first significant appearance. Proposed clear framework for tech debt prioritisation. A useful addition to engineering governance.
- **BenVH:** Honest about the testing gap that has plagued Cat Accelerate for four years. Passionate about his agent governance approach. Wants AI agents to never auto-approve -- humans must review PRs.
- **Nikhil:** Engaged, proactive. Already caught up with BenVH independently. Taking ownership of tech debt analysis.
- **Chris Moorhouse:** Quieter but contributed knowledge about existing library-level testing. Has not seen CLARA yet but willing to engage.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Rahul / Nikhil | First-pass tech debt priority list | Richard | High |
| Rahul | Get Stacy's capacity view | Team | High |
| Richard | Send CLARA repo and link to Chris | Chris | High |
| BenVH | Enable Bedrock and Claude Code access | Team | High |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of purpose | 4 | Two clear objectives: tech debt and AI infrastructure |
| Decision quality | 4 | Good framework for tech debt; clear AI agent governance |
| Engagement | 4 | Good participation from all attendees |
| Follow-through setup | 4 | Clear actions with owners identified |
| Time efficiency | 3 | Some repetition in programme overview for new members |

## Risk Signals
- **Cat Accelerate has no test infrastructure.** BenVH admitted it -- no unit tests, no integration tests, ad-hoc Postman only. Any infrastructure change is high-risk.
- **AI governance process is opaque and slow.** BenVH warns the intake form went unanswered for two weeks. The team has not yet submitted CLARA's form.
- **Sales Recon data pipeline failure.** Forces the team to build their own interim Salesforce/Mixpanel pipeline -- adding unplanned work.
- **Agent auto-approval risk.** BenVH explicitly designs against this, but the temptation to skip human review under time pressure will grow.

## Open Questions Raised
- Which agent framework: OpenClaw, Copilot Studio, or something else?
- How to ring-fence the L1 automation environment for testing?
- What is the decommission timeline for Cat Accelerate?
- Will Bedrock Claude deployment require a separate AWS account?

## Raw Quotes of Note
- "I'm not aware of proper unit testing or integration testing... the only way we verify it works is Postman collections that are kind of floating around" -- BenVH, on Cat Accelerate's testing gap
- "These agents will only ever submit PRs and we need humans to review and not just auto approve" -- BenVH, on agent governance
- "One of the top priorities... having some form of API monitoring so we know something failed before the customer comes back to us" -- Nikhil, on observability

## Narrative Notes
This session marks the formal expansion of the programme's engineering capacity. Nikhil and Chris are onboarded, Rahul brings structured thinking, and the Cat Accelerate tech debt finally gets a prioritisation framework. BenVH's admission about the testing gap is significant -- it has been a known problem for four years, now meeting AI-driven acceleration of changes. His agent governance philosophy (agents submit PRs, humans review) is the right instinct but will be tested under delivery pressure. The Sales Recon data pipeline failure is a setback that forces unplanned work, but it also validates the team's decision to build their own capabilities rather than depending on external tools.
