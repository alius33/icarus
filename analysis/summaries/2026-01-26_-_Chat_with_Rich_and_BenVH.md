# Chat with Rich & BenVH — Deployment Planning & Architecture Decisions
**Date:** 2026-01-26
**Attendees:** Richard Dosoo, Ben Van Houten (BenVH / Speaker 2), Azmain Hossain, Martin Davies
**Duration context:** Medium (~38 minutes)
**Workstreams touched:** WS2 CLARA (deployment), WS5 Platform/Infrastructure, WS4 Build in Five (Martin's RMB app)

## Key Points
- Morning coordination session before the afternoon Portfolio Review launch and Sales Recon executive session
- Azmain has been building locally because database migration changes carry risk of breaking production if deployed incorrectly; the team agreed to coordinate deployment together with BenVH
- Employee import plan and account team structure plan need to be executed in sequence -- employees first, then account team linking -- to ensure proper data relationships
- A naming mismatch between `customer.name` and `customer_name` in the schema was identified as a deployment risk; BenVH updated the account plan to fix this
- BenVH identified a SQL injection risk in the import plans, flagging it as a security concern non-developers cannot easily handle
- Richard decided Martin's RMB (Risk Maturity Benchmarking) app must be decoupled from the mono repo into its own separate repository, to minimise blast radius from cursor/AI tools fetching unrelated code
- BenVH is building a form-based app generator that auto-creates repos with CICD workflows, architecture spec, and deployment YAML -- a proto-platform play
- The team needs an Anthropic API key from the enablement team (not the MAP team, who only support customer-facing products); Richard is pursuing this
- Salesforce-to-Gainsight migration is blocking CRM integration; Gainsight team not ready until March to take requirements
- BenVH has everything in Terraform for lift-and-shift capability across cloud environments
- Three apps to demo at 2pm: Azmain's CLARA tracker, Richard's customer insights agent workflow, Bernard's Microsoft Copilot agent
- Next infrastructure priority after deployment: dev/test environment separation with proper release gates

## Decisions Made
- Employee import runs before account team import to ensure proper linking
  - **Type:** explicit
  - **Confidence:** HIGH
- Martin's RMB app to be decoupled into a separate repository (away from mono repo)
  - **Type:** explicit
  - **Confidence:** HIGH
- Separate repos for separate apps going forward (abandoning mono repo approach)
  - **Type:** explicit
  - **Confidence:** HIGH
- Schema field to be `customer_name` not `customer.name` -- standardised across the board
  - **Type:** explicit
  - **Confidence:** HIGH
- API key pursuit: enablement team route, not MAP team
  - **Type:** explicit
  - **Confidence:** MEDIUM

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Deploy employee import and account team changes to prod | Azmain + BenVH | 2026-01-26 (same day, before 2pm) | Open | HIGH |
| Fix account team plan to use `customer_name` instead of `customer.name` | BenVH | 2026-01-26 | Open | HIGH |
| Create separate repo for RMB app and push code there | Martin Davies | 2026-01-26 | Open | HIGH |
| Get Anthropic API key from enablement team | Richard Dosoo | 2026-01-27 | Open | MEDIUM |
| Pursue Salesforce/Gainsight integration with Natalia Plant | Richard + Azmain | Ongoing | Open | LOW |
| Plan infrastructure migration (AWS vs Azure vs MAP) | BenVH + Richard | TBD | Open | LOW |
| Build form-based app generator with CICD scaffolding | BenVH | Ongoing | Open | MEDIUM |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Database deployment risk management | Technical/Deployment | "We didn't want to run the risk of making a database unusable" -- Richard | HIGH |
| Mono repo vs multi-repo architecture | Architecture Decision | "If it's a mono repo... what if it changes code on another repo" -- BenVH | HIGH |
| Platform/app generator vision | Strategic/Infrastructure | "I can have us dynamically create a project, but using the foundation that we want" -- BenVH | MEDIUM |
| Salesforce-to-Gainsight migration blocker | Integration/CRM | "They're cock blocking us right now" -- Richard | HIGH |
| Infrastructure environment planning | DevOps | "Everything in Terraform, so it would just be a lift and shift" -- BenVH | MEDIUM |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Richard Dosoo | Operational orchestrator, meeting chair | Set agenda, directed actions, made architecture call on repos | 35% |
| BenVH | Technical authority on deployment/infra | Reviewed plans, identified risks, drove platform vision | 30% |
| Azmain Hossain | Builder/implementer | Explained build status, proposed sequencing, received direction | 25% |
| Martin Davies | Listener/executor | Accepted repo task, minimal pushback | 10% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| BenVH | Constructive, proactive | Stable -- continues to push platform vision | App generator, infrastructure | "I'm just kind of executing the form aspect... to get a proof of concept going" |
| Richard | Pragmatic, slightly overwhelmed | Stable -- juggling too many threads | Architecture, API keys, demos | "We need to workshop that... the five of us need to go in a room" |
| Azmain | Focused, constrained by tooling | Stable -- laptop performance issues noted | Deployment, data import | "Every time I run Claude, it just slows everything down" |
| Martin | Compliant, quiet | Stable | Repo creation | "Yep, already on it" |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| BenVH | Update account team plan with schema fixes | Same day | None | HIGH |
| Azmain | Complete employee import, push changes for deployment | Same day (before 2pm demo) | BenVH availability to help | HIGH |
| Martin | Create separate repo for RMB app, add Richard as admin | Same day | Has admin access | HIGH |
| Richard | Pursue API key from enablement team | Next day | Team availability | MEDIUM |
| Richard | Pull down Martin's repo and align look-and-feel with CLARA | After Martin pushes | Martin completes repo | MEDIUM |

## Meeting Effectiveness
- **Type:** Working session / technical coordination
- **Overall Score:** 72
- **Decision Velocity:** 0.8
- **Action Clarity:** 0.7
- **Engagement Balance:** 0.6
- **Topic Completion:** 0.6
- **Follow Through:** 0.5

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-W4-01 | NEW | Database schema mismatch could break production deployment | MEDIUM | Stable (being fixed) | Technical discussion | HIGH |
| R-W4-02 | NEW | SQL injection risk in import plans | MEDIUM | New | BenVH review | HIGH |
| R-W4-03 | ONGOING | Gainsight team blocking CRM integration until March | HIGH | Escalating | Richard frustration | HIGH |
| R-W4-04 | NEW | Azmain's laptop performance degrading development velocity | LOW | Stable | Observation | MEDIUM |
| R-W4-05 | NEW | Mono repo approach creating cross-contamination risk with AI tools | MEDIUM | Being resolved (decoupling) | Architecture discussion | HIGH |
| R-W4-06 | NEW | No dev/test environment separation -- all changes hitting prod | HIGH | New awareness | Richard flagged | HIGH |

## Open Questions Raised
- What is the right long-term infrastructure home -- stay on AWS, move to Azure, or try MAP environment?
- How will the Salesforce-to-Gainsight migration affect data integration timelines?
- When will the five-person workshop happen to align platform vision with business requirements?
- What naming conventions should new repos follow?

## Raw Quotes of Note
- "We didn't want to run the risk of making a database unusable" -- Richard, on why Azmain was building locally
- "Every time I run Claude, it just slows everything down" -- Azmain, on laptop constraints
- "They're cock blocking us right now" -- Richard, on Gainsight team blocking integration access
- "We need to workshop that... the five of us need to go in a room" -- Richard, acknowledging platform vision needs dedicated time
- "I don't want y'all to think that I'm forcing my idea on things" -- BenVH, diplomatically advancing platform strategy

## Narrative Notes
This was a tight operational coordination session focused on getting deployments ready for the afternoon's demo. The underlying tension is between tactical urgency (get Azmain's changes deployed before 2pm) and strategic debt accumulation (no dev/test separation, mono repo risks, no API key yet, no CRM integration path). Richard is juggling all of these threads and clearly feels the weight of it.

BenVH continues to quietly build toward a platform vision -- the app generator form, Terraform infrastructure, CICD standardisation -- without being heavy-handed about it. His comment about not wanting to force his ideas reveals awareness that the team is not yet aligned on the platform strategy. The decision to decouple Martin's RMB app into a separate repo is a small but meaningful architectural step that validates BenVH's multi-repo approach. The Gainsight blockage is becoming a recurring frustration that could delay the entire CRM integration roadmap.
