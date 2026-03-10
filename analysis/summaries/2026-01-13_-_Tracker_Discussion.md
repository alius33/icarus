# Tracker Discussion -- Data Strategy and Demo Planning
**Date:** 2026-01-13
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brooks (joins mid-call), BenVH (Van Houten)
**Duration context:** long (~7800 words)
**Workstreams touched:** WS2 (CLARA/Adoption Tracker), WS3 (Infrastructure/Deployment)

## Key Points
- Central debate: whether to demo with synthetic data or real (golden source) data; Ben Brooks worried synthetic data will cause CSMs to disengage
- Golden source data from Salesforce is incomplete -- many fields empty (customer adoptions, adoption charters entirely blank)
- Agreed strategy: (1) keep golden source accounts with real data untouched, (2) create separate test account with fake company name for demos, (3) implement demo/real toggle
- Ben Brooks reveals Josh Ellingson messaged him requesting the app be ready for a leadership call in 2.5 hours -- first sign of Josh's interest/impatience
- BenVH configuring Azure AD SSO -- changing redirect URIs from "web" to "single page application" in Entra ID; adding Richard as application owner
- BenVH purchased advisoryappfactory.com domain but firewall team immediately blacklisted it; had to get separate approval
- GitHub repo access being set up for BenVH -- service ticket approved but propagation delayed
- Azure tenant and client IDs retrieved for AWS Cognito integration
- Azmain suggests creating simple front-end connected to Excel file for CSM data entry; Ben Brooks vetoes this -- editing the deployed app is easier
- Ben Brooks demos Opus-generated account planning mockup for George -- created in two prompts, shows stakeholder mapping, health scores, success plans
- Azmain successfully clones the GitHub repo and begins local development for the first time

## Decisions Made
- **Demo data strategy**: Use real golden source data untouched; create synthetic test accounts with fake names for demos; implement toggle -> Ben Brooks/Azmain
  - **Type:** explicit
  - **Confidence:** HIGH
- **No Excel front-end**: Edit the deployed app directly rather than building intermediary Excel form -> Ben Brooks (overruling Azmain)
  - **Type:** explicit
  - **Confidence:** HIGH
- **Azure AD reconfigured**: Changed from "web" to "single page application" redirect URIs -> BenVH
  - **Type:** explicit (technical)
  - **Confidence:** HIGH
- **Richard added as Azure application owner**: For troubleshooting without Ben Brooks each time -> BenVH
  - **Type:** explicit
  - **Confidence:** HIGH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Create synthetic test customers with fake company names | Azmain | 2026-01-14 | Open | HIGH |
| Implement demo/real data toggle in app | Azmain/Ben Brooks | 2026-01-15 | Open | MEDIUM |
| Fix CICD pipeline from GitHub to AWS | BenVH/Richard | 2026-01-14 | Open | HIGH |
| Clone repo and begin local development | Azmain | 2026-01-13 | Complete | HIGH |
| Get BenVH's GitHub account propagated | Richard | 2026-01-13 | Open | HIGH |
| Set up call with Idris for Jan 26 prep | Richard | 2026-01-17 | Open | MEDIUM |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Data strategy for demos | strategic | "we're going to lose them" -- Ben Brooks on synthetic data risk | HIGH |
| Azure AD SSO configuration | technical | "I feel like I should maybe press a big fishing button right now" -- Ben Brooks | HIGH |
| Opus account planning mockup | operational | "two prompts... the depth of what it produces is insane" -- Ben Brooks | HIGH |
| Firewall blocking domain | technical | "the firewall team doesn't like any domains they don't know about" -- BenVH | HIGH |
| Josh's sudden interest | interpersonal | "no pressure. Josh has just sent me a message saying, will your app be finished by 7pm" -- Ben Brooks | HIGH |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Richard Dosoo | Coordinator, decision facilitator | Mediating between Ben's vision and Azmain's pragmatic suggestions | 35% |
| Ben Brooks | Product owner, quality gatekeeper | Vetoing synthetic data approach, setting demo standards, showing Opus mockup | 25% |
| Azmain Hossain | Builder, pragmatist | Proposing Excel front-end (overruled), cloning repo, starting work | 25% |
| BenVH | Infrastructure engineer | Configuring Azure AD, registering domains, troubleshooting deployment | 15% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Ben Brooks | Excited about Opus, protective of demo quality | Positive momentum | Product direction | Shows account planning mockup with genuine enthusiasm |
| Josh Ellingson (ref) | Suddenly interested/impatient | Shift from passive to active | App readiness | Asking if app will be ready for leadership call in 2.5 hours |
| BenVH | Diligent but frustrated | Stable | Infrastructure | Dealing with firewall blocks, Azure re-auth, GitHub propagation delays |
| Azmain | Eager to contribute, learning | Growing engagement | Development process | First time cloning the repo and setting up locally |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Azmain | Will create synthetic demo data with fake company names | Tomorrow | None | HIGH |
| BenVH | Will complete CICD pipeline configuration | Tonight/tomorrow | Azure AD issues resolved | MEDIUM |
| Richard | Will get BenVH GitHub access sorted | Today | Service Now ticket processes | MEDIUM |
| Ben Brooks | Will fix dashboard and blocker pages locally | This week | None | HIGH |

## Meeting Effectiveness
- **Type:** Technical working session / data strategy planning
- **Overall Score:** 68
- **Decision Velocity:** 0.6
- **Action Clarity:** 0.6
- **Engagement Balance:** 0.6
- **Topic Completion:** 0.5
- **Follow Through:** 0.5

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-017 | New | Golden source data has critical gaps -- adoptions and charters entirely empty | HIGH | Stable | Data Quality | HIGH |
| R-018 | New | Azure firewall blocking advisoryappfactory.com domain | MEDIUM | Improving | Infrastructure | HIGH |
| R-019 | New | Josh requesting app demo on very short notice (2.5 hours) | MEDIUM | Escalating | Stakeholder | HIGH |
| R-020 | New | Multiple Azure re-authentication issues slowing development | LOW | Stable | Infrastructure | HIGH |

## Open Questions Raised
- How many accounts need comprehensive demo data for first CSM presentation?
- When is the next IRP planning meeting where app will be shown with real data?
- Can CICD pipeline be fully automated by tomorrow?
- Will Josh's leadership call demo happen? (No confirmation by end of call)

## Raw Quotes of Note
- "we're going to lose them, right? Because... today, it doesn't resonate" -- Ben Brooks, on showing synthetic data to CSMs
- "I feel like I should maybe press a big fishing button right now. Three guys with their cameras off, it's being recorded, and log into Azure" -- Ben Brooks, on the absurdity of the situation
- "two prompts... the depth of what it produces is insane" -- Ben Brooks, on Opus capabilities
- "no pressure. Josh has just sent me a message saying, will your app be finished by 7pm because I have a leadership call" -- Ben Brooks

## Narrative Notes
This session marks a pivotal transition from local development to real deployment, with political stakes rising. Josh Ellingson's last-minute request signals word is spreading about CLARA, but also creates dangerous expectations. The data strategy debate -- synthetic vs. real -- reveals genuine tension: CSMs will disengage from fake data, but real data is embarrassingly incomplete. Ben Brooks's toggle solution adds scope but is pragmatic. The Azure SSO configuration session illustrates constant infrastructure friction BenVH faces -- firewall blocks, re-authentication timeouts, domain registration delays. Meanwhile, Azmain cloning the repo and getting set up locally represents the first step toward the team iterating collaboratively rather than through a single bottleneck (Ben Brooks). The Opus account planning mockup hints at where the product could go -- and generates genuine excitement.
