# Account Planner Onboarding with George Dyke
**Date:** 2026-01-19
**Attendees:** Richard Dosoo, George Dyke, Ben Brookes, Martin Davies, Azmain Hossain
**Duration context:** Long (~56 minutes, multi-hour working session with live Cursor walkthrough)
**Workstreams touched:** WS6 Build in Five, WS1 Training, WS2 CLARA (infrastructure context)

## Key Points
- Richard walked George through his first Cursor session, creating a static HTML account planning application from a ChatGPT-generated prompt
- George is building an account planner tool for CSMs to drive intentional customer engagement and planning activities rather than reactive work
- Ben Brookes pushed for using Opus/Sonnet models over Auto for dramatically better output quality on first-pass mockups
- Richard outlined the deployment pipeline path: local development, GitHub, CI/CD via BenVH's app factory infrastructure (ECS on AWS)
- George acknowledged he will be the least technical Cursor user and will need continued support
- Discussion of shared Cursor token budget across advisory, banking, and KYC teams managed by Divya Harry
- Martin Davies confirmed Cursor can create folders and handle version management when asked
- Ben Brookes raised the potential to rebuild CLARA's front end using Opus rather than Auto, noting it was originally built entirely in Auto mode
- Richard flagged the longer-term plan to feed account planning requirements into Ari LaHavi's Sales Recon team so the platform can absorb these capabilities over 6-12 months

## Decisions Made
- **George to start with static HTML prototyping locally** (type: process, confidence: high) — rationale: lowest risk entry point before graduating to full app with backend/database
- **George's app to eventually join the shared app factory infrastructure** (type: technical, confidence: medium) — rationale: leverage existing CI/CD pipeline BenVH built, but timing depends on George reaching critical mass of features
- **Richard to raise GitHub account ticket for George** (type: administrative, confidence: high) — needed for version control and deployment pipeline
- **Use Opus/Sonnet models for initial mockups, cheaper models for iteration** (type: process, confidence: high) — Ben Brookes' recommendation based on experience with CLARA

## Action Items
| Action | Owner | Deadline | Confidence |
|--------|-------|----------|------------|
| Review account planner requirements and iterate on Cursor output | George Dyke | End of week | High |
| Create GitHub account ticket for George | Richard Dosoo | 2026-01-20 | High |
| Set up dedicated chat thread for account planner collaboration | Richard Dosoo | 2026-01-19 | High |
| Reconnect with George end of week or early next week on infrastructure integration | Richard Dosoo | 2026-01-24 | Medium |
| Share prompt and PRD template with broader group | Richard Dosoo | 2026-01-20 | Medium |

## Theme Segments
| Timestamp Range | Theme | Speakers | Tone |
|----------------|-------|----------|------|
| 0:00-5:00 | Introductions and Cursor setup | Richard, George, Ben | Collaborative, energetic |
| 5:00-18:00 | First prompt execution and PRD walkthrough | Richard, George | Instructional, patient |
| 18:00-27:00 | Account planner requirements deep-dive | George, Richard, Ben | Strategic, engaged |
| 27:00-38:00 | Deployment pipeline and infrastructure roadmap | Richard, George, Ben | Technical, forward-looking |
| 38:00-48:00 | Model selection, Opus vs Auto, and second iteration | Ben, Richard, George | Enthusiastic, comparative |
| 48:00-56:00 | Cursor licensing, Claude Code discussion, and wrap-up | Ben, Richard, Martin | Practical, excited |

## Power Dynamics
- **Ben Brookes** dominated the strategic framing, pushing hard for Opus models and positioning George's tool within the broader ecosystem. His language was directive and confident.
- **Richard Dosoo** acted as the patient enabler and technical bridge, walking George through each step methodically.
- **George Dyke** positioned himself clearly as a non-technical user needing guidance, but showed strong strategic clarity on what the account planner should achieve for CSMs.
- **Martin Davies** was quiet but contributed a useful correction about Cursor's folder creation capability.

## Stakeholder Signals
- **George Dyke** — Engaged and enthusiastic but realistic about his technical limitations. His vision for the account planner is clear: intentional engagement planning, not reactive work. He wants strategic and standard account templates with gap-flagging mechanisms.
- **Ben Brookes** — Highly energized about AI tooling potential. Openly suggested rebuilding CLARA's front end in Opus. His frustration with organisational inertia surfaced when discussing training adoption barriers.
- **Richard Dosoo** — Balancing enablement with governance. Already thinking about standardizing Cursor settings, managing token budgets, and creating training pipelines.
- **Martin Davies** — Present but minimally vocal. Positioned as a technical resource who can support George.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Richard | Raise GitHub account ticket for George | George | High |
| Richard | Create chat thread for account planner collaboration | Team | High |
| Richard | Reconnect with George by end of week on infrastructure | George | Medium |
| George | Review requirements and iterate on Cursor output | Self/Team | High |
| Ben Brookes | Offered to review outputs and support iteration | George | Medium |

## Meeting Effectiveness
- **Clarity of outcomes:** 7/10 — Clear next steps for George, but infrastructure timeline remained vague
- **Decision quality:** 6/10 — Practical decisions made but deferred the key question of long-term ownership (Sales Recon vs standalone)
- **Engagement balance:** 6/10 — Ben and Richard dominated; George participated well but mostly in receiving mode
- **Time efficiency:** 5/10 — Extended Cursor build time consumed significant meeting time; could have been pre-prepared

## Risk Signals
| Risk | Severity | Signal |
|------|----------|--------|
| Overlap between account planner and CLARA capabilities | MEDIUM | George's tool covers customer planning; CLARA tracks adoption. The boundary is unclear and could cause confusion or duplication. |
| Token budget exhaustion | MEDIUM | Shared Cursor budget across multiple teams with no clear allocation model. Ben acknowledged this as a real constraint. |
| George operating without version control | LOW | Local-only development with manual folder versioning until GitHub access is provisioned. Risk of lost work. |
| Scope creep on account planner before Sales Recon alignment | MEDIUM | George could build significant functionality that overlaps with Sales Recon's planned capabilities, creating a retirement problem later. |

## Open Questions Raised
- How will George's account planner data integrate with CLARA's customer data?
- What is the formal handoff process for moving a local prototype to the shared infrastructure?
- Will Sales Recon's customer success capabilities make the standalone account planner redundant?
- How should the shared Cursor token budget be allocated across teams?
- Can Cursor settings files be automatically enforced for all new users?

## Raw Quotes of Note
- "I'm going to be as non-technical a user probably as Cursor interacts with" — George Dyke, setting expectations honestly
- "If 100 people spend 10 grand, I would call that success" — Ben Brookes, on the token budget question
- "I wrote that whole of that IRP tracker in Auto. It wouldn't do us a disservice to rebuild the front end fairly soon" — Ben Brookes, candidly acknowledging CLARA's front-end quality debt

## Narrative Notes
This session marked George Dyke's entry into the AI-assisted development world, and it revealed both the promise and the governance gaps in the programme's approach to tool enablement. Richard was characteristically thorough in his walkthrough, but the session exposed a recurring pattern: the team is moving fast on tooling adoption without the supporting infrastructure (GitHub accounts, standardized settings, version control processes) being ready. Ben Brookes' enthusiasm was infectious but also slightly destabilizing -- his suggestion to rebuild CLARA's front end, dropped casually mid-conversation, hints at an underlying dissatisfaction with the current build quality that could surface as a priority conflict. George's strategic clarity on what CSMs actually need (intentional planning over reactive firefighting) was the most valuable insight from the call, and it maps cleanly to the gap that both CLARA and Sales Recon are trying to fill. The tension between building something quickly for tactical value versus feeding requirements to Sales Recon for long-term platform alignment remains the central unresolved question for this workstream.
