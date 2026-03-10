# Chat with Richard 1 -- Amalin Post-Mortem, UI Review, and Git Workflow
**Date:** 2026-01-15
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (Van Houten, briefly)
**Duration context:** long (~8000 words)
**Workstreams touched:** WS2 (CLARA), WS3 (Infrastructure/Deployment)

## Key Points
- Extended discussion about Amalin (difficult client project) as a cautionary tale -- systemic dysfunction including contractor incentives for project overruns, no strategic alignment, weak leadership, testing teams not incentivised to deliver
- Richard draws lesson: CLARA should make problems like Amalin visible early through proper tracking and status escalation
- Azmain shows improved local build: table-based customer view with pagination (10 rows default), pop-up modals for CRUD, improved UX for blockers, action items, milestones
- Richard reviews and provides feedback: table layout is better than tabs, pagination needed, wants a tooltip/hover showing use cases and blockers when hovering over a customer row
- Discussion about CICD pipeline: merge to main now triggers automated deployment via GitHub Actions; Richard and BenVH completed this the previous evening
- First time doing a push from Azmain's branch to GitHub -- cursor guides the git workflow (clone, branch, commit, push, PR, merge)
- Richard walks Azmain through creating a pull request and merging to main
- Azmain's changes deploy through the pipeline for the first time -- builds pass, front-end and back-end deploy to AWS ECS
- Discussion of multi-model AI strategy: using different LLMs for different tasks (Opus for reasoning, Sonnet for coding, ChatGPT for general purpose); Richard shares a GitHub repo for an LLM orchestrator tool
- Richard pushing to get enterprise Claude licences approved -- suggests getting Diya to greenlight a PO for 5 people at 500 GBP/month rather than waiting for enterprise negotiation
- Richard plans to chase developer laptop approvals for Azmain through Diya
- Discussion about AI's impact on junior engineers and training -- concern that AI tools will eliminate junior roles, creating a gap in the experience pipeline

## Decisions Made
- **Table view with pagination is the standard layout**: Replacing tab-based customer view -> Azmain (Richard approves)
  - **Type:** implicit
  - **Confidence:** HIGH
- **CICD pipeline operational**: Merge to main triggers full deploy -> BenVH/Richard
  - **Type:** explicit
  - **Confidence:** HIGH
- **Push for enterprise Claude licences via PO**: Rather than waiting for enterprise negotiation -> Richard to push with Diya
  - **Type:** implicit
  - **Confidence:** MEDIUM
- **Chase developer laptop approvals today**: Through Diya via Ben -> Richard
  - **Type:** explicit
  - **Confidence:** HIGH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Add hover tooltip for customer rows showing use cases/blockers | Azmain | 2026-01-16 | Open | MEDIUM |
| Push for enterprise Claude licences PO with Diya | Richard | 2026-01-20 | Open | MEDIUM |
| Chase developer laptop approvals through Diya/Ben | Richard | 2026-01-15 | Open | HIGH |
| Continue CRUD operations and local testing | Azmain | 2026-01-15 | In Progress | HIGH |
| Resolve merge conflicts between feature branch and main | Azmain | 2026-01-15 | Complete | HIGH |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Amalin client post-mortem | interpersonal | "no one wants another Amalin style project" -- Richard | MEDIUM |
| UI improvements and review | technical | "change the all customers bit to a table... tooltip when you highlight a customer" -- Richard | HIGH |
| First successful deployment through CICD | technical | "this is now we got the internet process. But normally this part Ben would be doing for you" -- Richard | HIGH |
| Multi-model AI strategy | operational | "a lot of what people are doing now is they're like, we'll have our own workflow orchestrator on top of four different LLMs" -- Richard | MEDIUM |
| Enterprise Claude licence push | governance | "maybe so let's say we've all bought licences now for a month... get Diya to greenlight" -- Richard | MEDIUM |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Richard Dosoo | Mentor, reviewer, coordinator | Teaching git workflow, reviewing UI, planning licence strategy | 55% |
| Azmain Hossain | Builder, learner | Showing progress, learning git, pushing first deployment | 40% |
| BenVH | Infrastructure support (brief) | Troubleshooting deployment issues | 5% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Richard | Teaching, invested | Stable | Team development | Patiently walking Azmain through git workflow |
| Azmain | Growing confidence, productive | Positive | Development velocity | Successfully deployed first changes through CICD |
| Diya (ref) | Needed for approvals | Stable | Licences/laptops | Multiple items requiring her sign-off |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Richard | Will chase developer laptop approvals today | 2026-01-15 | Diya/Ben responsive | HIGH |
| Richard | Will push for Claude licence PO | Next week | Diya available | MEDIUM |
| Azmain | Will continue building CRUD operations | 2026-01-15 | None | HIGH |

## Meeting Effectiveness
- **Type:** Working session / mentoring / deployment
- **Overall Score:** 70
- **Decision Velocity:** 0.5
- **Action Clarity:** 0.6
- **Engagement Balance:** 0.6
- **Topic Completion:** 0.5
- **Follow Through:** 0.6

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-030 | New | Azmain still on standard laptop, not developer-provisioned | MEDIUM | Stable | Resource | HIGH |
| R-014 | Continuing | Personal AI licence costs unsustainable -- team spending own money | MEDIUM | Escalating | Financial | HIGH |

## Open Questions Raised
- Will Diya approve the Claude licence PO quickly enough?
- When will developer laptops be provisioned?
- How to structure the updates/audit trail functionality (hierarchical vs. flat)?

## Raw Quotes of Note
- "no one wants another Amalin style project. No one wants to revisit that scenario" -- Richard
- "I'm telling you, man, we are screwed. This is way too good" -- Azmain, on Opus capabilities
- "we can't... it's not sustainable for us to all do that, because we're all... end up hitting the same thing" -- Richard, on personal AI subscriptions
- "the training ground, right for everyone... the question is, how does that happen now" -- Richard, on AI's impact on junior engineer career paths

## Narrative Notes
This is primarily a working session with a significant mentoring component -- Richard is teaching Azmain the git workflow, reviewing his UI improvements, and managing the first successful deployment through the CICD pipeline. The Amalin post-mortem, while a digression, serves a purpose: it contextualises why CLARA's early-warning capability matters (the "never again" narrative). The most operationally significant moment is Azmain's first successful merge-to-main deployment through GitHub Actions -- this removes a bottleneck and enables parallel development. Richard's discussion of multi-model AI strategy and LLM orchestration tools shows he's thinking beyond the immediate product to broader AI architecture questions, though this risks scope creep. The enterprise Claude licence push is tactically important: getting a PO approved through Diya bypasses the slow enterprise procurement process that has been frustrating the team for weeks.
