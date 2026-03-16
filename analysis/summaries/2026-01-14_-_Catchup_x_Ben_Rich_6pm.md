# Catchup x Ben Rich 6pm -- Deployment Progress and Programme Scope
**Date:** 2026-01-14
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brookes, BenVH (Van Houten)
**Duration context:** long (~5500 words)
**Workstreams touched:** WS2 (CLARA), WS3 (Infrastructure/Deployment), WS4 (Sales Recon Convergence), WS6 (Build in Five)

## Key Points
- AWS deployment is progressing -- the base version of the app is running on advisoryappfactory.com/irp-adoption-tracker, though the API is not returning data yet (front-end deployed, back-end connectivity issues)
- CICD pipeline partially working: GitHub Actions run on push, but deployment to ECR has issues; Ben/BenVH plan to finish automated deployment tonight
- Ben Brookes frames the upcoming meeting (likely Tuesday next week) as answering the question: "what can you show us to give confidence we'll achieve 35 migrations this year?"
- Ben wants the demo to focus on the process and workflow (contextualised dashboard, use cases, blockers, action plans) rather than individual tooling
- Ben proposes phased approach: Phase 1 = clean up first 5-7 entities (use cases, blockers, data issues, action plans, team members), Phase 2 = charters/blueprints/milestones
- Azmain starts branching off the golden repo to begin CRUD operations for the seven core entities
- Teams is blocking the advisoryappfactory.com URL as "harmful content" -- Ben has to send screenshots of the link instead
- Richard out on Friday; BenVH flying to Amsterdam Friday evening for HiRox competition
- CICD pipeline works: merge to main triggers GitHub Actions which builds Docker image and deploys to AWS ECS
- Richard maps out the broader programme: 5-6 workstreams including (1) PMO Dashboard/Adoption Tracker (CLARA), (2) Adoption Charter Generation, (3) Customer Success Agent (possibly copilot studio), (4) Client Pipeline Development (separate AWS environment), (5) Navigator, (6) Cursor internal productivity
- Martin Davies has a separate app that Richard initially thought would merge with CLARA but Ben wants kept separate
- BenVH confirms he can create a separate database in RDS for Martin's app within the same infrastructure

## Decisions Made
- **Demo focus on process, not data**: Show workflow visibility and management approach, not executive dashboard -> Ben Brookes
  - **Type:** explicit
  - **Confidence:** HIGH
- **Phase 1 scope**: CRUD operations for use cases, blockers, data issues, action plans, team members first -> Ben Brookes
  - **Type:** explicit
  - **Confidence:** HIGH
- **Phase 2 deferred**: Charters, blueprints, milestones come after Phase 1 is solid -> Ben Brookes
  - **Type:** explicit
  - **Confidence:** HIGH
- **Martin's app kept separate**: Not merged into CLARA -> Ben Brookes
  - **Type:** explicit
  - **Confidence:** HIGH
- **CICD pipeline: merge to main triggers deployment**: Azmain creates feature branches, PRs into main trigger auto-deploy -> BenVH/Richard
  - **Type:** explicit
  - **Confidence:** HIGH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Complete CICD pipeline automation (merge-to-main triggers deploy) | BenVH/Richard | 2026-01-14 evening | Open | HIGH |
| Build CRUD operations for 7 core entities | Azmain | 2026-01-15 | Open | HIGH |
| Finish back-end API connectivity in AWS | BenVH | 2026-01-14 | Open | HIGH |
| Report Teams URL blocking to domain team | BenVH | 2026-01-15 | Open | MEDIUM |
| Create programme spreadsheet with 5 project tabs, stakeholder RACI | Richard | 2026-01-15 | Open | MEDIUM |
| Set up Idris meeting for Jan 26 prep | Richard | 2026-01-17 | Open | MEDIUM |
| Investigate separate RDS database for Martin's app | BenVH | 2026-01-20 | Open | LOW |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Demo strategy for 35-migration confidence | strategic | "what can you show us to give us confidence that we're going to achieve the 35 migrations" -- Ben Brookes | HIGH |
| CICD pipeline completion | technical | "whenever we check something into... the main branch, it would go through the deployment" -- Richard | HIGH |
| Programme scope with 5-6 workstreams | governance | "we've got about six projects that we're going to be running in parallel" -- Richard | HIGH |
| Teams URL blocking | operational | "there is somebody that is insistent we mustn't succeed here" -- Ben Brookes | MEDIUM |
| Phase 1 vs Phase 2 priorities | strategic | "v2 can happen next week. This is awesome" -- Ben Brookes, on speed of iteration | HIGH |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Ben Brookes | Product owner, setting priorities and phases | Defining demo narrative, phasing scope, deciding to keep Martin's app separate | 30% |
| Richard Dosoo | Programme coordinator | Mapping broader programme scope, managing logistics, bridging teams | 35% |
| Azmain Hossain | Builder, executing | Starting CRUD work, confirming development approach | 20% |
| BenVH | Infrastructure engineer | Completing CICD pipeline, troubleshooting AWS connectivity | 15% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Ben Brookes | Optimistic, pragmatic | Stable | Phase 1 focus | Excited about rapid iteration potential |
| BenVH | Determined, dealing with friction | Stable | Infrastructure | Fighting Teams URL blocks, security scrutiny |
| Azmain | Ready to deliver | Growing | Development | Starting CRUD operations immediately |
| Richard | Strategic, spread thin | Stable | Programme scope | Trying to map all 6 workstreams simultaneously |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| BenVH | Will complete CICD pipeline tonight | 2026-01-14 | None | HIGH |
| Azmain | Will build CRUD operations for 7 entities | 2026-01-15 | Repo available | HIGH |
| Richard | Will create programme project spreadsheet | Tomorrow morning | None | MEDIUM |
| Ben Brookes | Will prepare talking points for Tuesday demo | Next week | App stable | MEDIUM |

## Meeting Effectiveness
- **Type:** Technical coordination / programme planning
- **Overall Score:** 75
- **Decision Velocity:** 0.7
- **Action Clarity:** 0.7
- **Engagement Balance:** 0.6
- **Topic Completion:** 0.6
- **Follow Through:** 0.6

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-023 | New | AWS back-end API not returning data on deployed version | HIGH | Improving | Technical | HIGH |
| R-024 | New | Teams blocking advisoryappfactory.com as "harmful content" | MEDIUM | Stable | Infrastructure | HIGH |
| R-025 | New | Richard out Friday, BenVH away for weekend -- narrow window for progress | MEDIUM | De-escalating | Resource | HIGH |
| R-026 | New | Programme scope expanding to 6 parallel workstreams with limited team | HIGH | Escalating | Resource | HIGH |

## Open Questions Raised
- When is the exact date for the Tuesday demo with Diya/Andy Frappe's team?
- How will Martin's separate app be deployed alongside CLARA in the same infrastructure?
- When will the URL blocking be resolved for advisoryappfactory.com?
- Who are the stakeholders for the Customer Success Agent workstream?

## Raw Quotes of Note
- "what can you show us to give us confidence that we're going to achieve the 35 migrations we need this year" -- Ben Brookes, framing the exam question
- "there is somebody that is insistent we mustn't succeed here" -- Ben Brookes, on Teams URL blocking
- "v2 can happen next week. This is awesome" -- Ben Brookes, impressed by iteration speed
- "Azmain is on superpower dashboard duty tomorrow. That's awesome" -- Ben Brookes

## Narrative Notes
This evening session crystallises the team's near-term strategy: get Phase 1 (core 7 entities with CRUD operations) working and deployed, then show the process and workflow to stakeholders to build confidence in the 35-migration target. Ben Brookes's decision to keep Martin's app separate is pragmatic but adds infrastructure complexity. The CICD pipeline reaching completion is a genuine milestone -- the team can now iterate without manual deployment. However, Richard's mapping of 6 parallel workstreams with essentially 4 people (Richard, Azmain, Ben Brookes, BenVH) reveals a serious resource constraint that will become acute as multiple workstreams demand attention simultaneously. The Teams URL blocking is a constant irritant that symbolises the broader organisational friction the team faces.
