# Chat with Richard 6 -- Programme Scope, Demo Mode Architecture, and Database Migrations
**Date:** 2026-01-15
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (Van Houten)
**Duration context:** long (~5000 words)
**Workstreams touched:** WS2 (CLARA), WS3 (Infrastructure/Deployment), WS4 (Sales Recon Convergence), WS6 (Build in Five)

## Key Points
- Richard maps out next steps post-advisory demo: get feedback from Stacy, but Liz raised the critical point that Josh's and George's feedback must be incorporated first -- otherwise stakeholders feel sidelined when their teams start using the tool
- Richard plans to create five project tabs in a spreadsheet with stakeholder RACI for each workstream: (1) PMO Dashboard/Adoption Tracker (CLARA), (2) Adoption Charter Generation, (3) Customer Success Agent (copilot studio), (4) Client Pipeline Development (separate AWS environment), (5) Navigator, (6) Cursor internal productivity
- Customer Success Agent workstream still undefined -- may be copilot studio, may not be; needs Catherine, Kevin, and Alexandra's input; Idris doing related Salesforce copilot work
- Azmain reveals he is building a demo mode with a demo database filled with synthetic data from Ben's Excel file
- BenVH proposes the correct architecture for demo mode: use a static JSON file that mirrors the database schema, displayed on the front-end only -- no database interaction in demo mode; CRUD operations disabled with a pop-up saying "you're in demo mode"
- Key architectural debate: database flag for demo data vs. static JSON display. BenVH argues the JSON approach is better because (1) cursor will forget about the demo flag in new contexts, (2) every stored procedure would need to filter by the flag, (3) JSON file serves as a schema reference document
- Richard agrees: "have a static version of the website that when someone clicks that button references this JSON file"
- BenVH explains database migration architecture with a whiteboard diagram: local backend changes -> migration -> schema update -> applied to production database. Currently, Cursor handles local migrations automatically but production schema updates are manual
- BenVH is actively implementing automated Alembic migrations so production schema updates happen on deployment
- BenVH pushes a database schema Markdown file to the repo as a source of truth for documentation
- Azmain clarifies the blocker/action plan hierarchy with Richard -- Richard redirects: ask Natalia, Diya, and Stacy (the PMO people) how they want blockers, issues, and risks captured, then implement that structure
- Richard's "soft power move" suggestion: get requirements from Diya/Natalia, implement them, then present it as "I implemented your feature" -- drives adoption through stakeholder ownership
- Monday is Martin Luther King Day (US holiday) -- Josh won't be available Monday, so feedback must happen Friday or be deferred
- BenVH flying to Amsterdam Friday evening for HiRox competition; races on 21st and 24th
- Martin Davies has a separate app -- BenVH confirms he can create a separate RDS database within the same infrastructure
- BenVH started working on multiple environments (dev/staging/prod) -- caused a brief 503 the previous night

## Decisions Made
- **Demo mode uses static JSON, not database flags**: Front-end displays JSON data when in demo mode; no CRUD operations allowed; pop-up notification for users -> BenVH (proposed), Richard (agreed)
  - **Type:** explicit
  - **Confidence:** HIGH
- **Get Josh and George feedback before deploying to CSMs**: Stakeholder buy-in required before wider rollout -> Richard/Liz
  - **Type:** explicit
  - **Confidence:** HIGH
- **Ask PMO stakeholders (Natalia/Diya/Stacy) for blocker/action item structure requirements**: Rather than the team defining it themselves -> Richard
  - **Type:** explicit
  - **Confidence:** HIGH
- **Martin's app gets separate RDS database**: Within the same infrastructure cluster -> BenVH
  - **Type:** explicit
  - **Confidence:** HIGH
- **Alembic migrations to be automated in deployment pipeline**: BenVH implementing automated schema updates -> BenVH
  - **Type:** explicit
  - **Confidence:** HIGH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Implement demo mode with static JSON (no DB interaction) | Azmain | 2026-01-16 | Open | HIGH |
| Complete automated Alembic migration in CICD pipeline | BenVH | 2026-01-17 | In Progress | HIGH |
| Push database schema Markdown file to repo | BenVH | 2026-01-15 | Complete | HIGH |
| Create programme spreadsheet with 5 project tabs and RACI | Richard | 2026-01-16 | Open | MEDIUM |
| Get Josh feedback on tracker (before Monday holiday) | Azmain | 2026-01-16 | Open | HIGH |
| Schedule George feedback session for Monday | Azmain/Richard | 2026-01-20 | Open | HIGH |
| Set up separate RDS database for Martin's app | BenVH | 2026-01-24 | Open | LOW |
| Get blocker/action item structure requirements from Natalia/Diya/Stacy | Azmain | 2026-01-20 | Open | MEDIUM |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Demo mode architecture (JSON vs DB flag) | technical | "don't talk... let's avoid communicating of like, hey, it needs to do something with production because it doesn't understand" -- BenVH on Cursor limitations | HIGH |
| Database migration automation (Alembic) | technical | "the migration is something separate because... I'm currently fixing that right now, so that it's fully automated" -- BenVH | HIGH |
| Stakeholder feedback sequencing | strategic | "make sure Josh's feedback and George's feedback is in... otherwise they feel like they left out" -- Richard paraphrasing Liz | HIGH |
| Programme scope: 5-6 workstreams | governance | "five project chart... not documents, but just like tabs in a spreadsheet" -- Richard | MEDIUM |
| Soft power move for adoption | interpersonal | "get a requirement from Diya Natalia, put it in the app and be like, oh hey guys, I implemented your feature" -- Richard | HIGH |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| BenVH | Technical architect, decision-maker on infrastructure | Defining demo mode architecture, explaining migration approach, pushing schema documentation | 40% |
| Richard Dosoo | Programme coordinator, stakeholder strategist | Mapping 5 workstreams, sequencing feedback, suggesting soft power tactics | 35% |
| Azmain Hossain | Builder, asking clarifying questions | Building demo mode, seeking clarity on blocker hierarchy, planning Josh/George sessions | 25% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| BenVH | Technically authoritative, proactive | Positive | Infrastructure maturity | Already started multi-environment setup, pushing schema docs |
| Richard | Strategic, thinking about politics | Stable | Stakeholder management | Conscious of Josh feeling sidelined, planning soft power moves |
| Azmain | Learning rapidly, occasionally naive | Growing | Architecture understanding | Didn't know what Alembic was, but absorbing migration concepts |
| Liz (referenced) | Politically astute | Stable | Stakeholder inclusion | Raised critical point about Josh/George feedback before rollout |
| Josh (referenced) | Potentially feeling sidelined | At risk | Engagement | Liz flagged need to include him before wider deployment |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| BenVH | Will complete migration automation | Tonight/tomorrow | None | HIGH |
| BenVH | Will be available Friday (flies to Amsterdam 8pm EST) | 2026-01-17 | None | HIGH |
| Richard | Will be available for about an hour Friday morning UK time | 2026-01-17 | Before cinema | MEDIUM |
| Azmain | Will get Josh feedback Friday (MLK Monday = no Josh) | 2026-01-16 | Josh available | MEDIUM |
| Azmain | Will build demo mode with JSON approach | 2026-01-16 | None | HIGH |

## Meeting Effectiveness
- **Type:** Technical architecture discussion / programme planning
- **Overall Score:** 72
- **Decision Velocity:** 0.7
- **Action Clarity:** 0.6
- **Engagement Balance:** 0.7
- **Topic Completion:** 0.6
- **Follow Through:** 0.6

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-035 | New | Josh potentially feeling sidelined -- Liz flagged need for his feedback before rollout | MEDIUM | Escalating | Stakeholder | HIGH |
| R-036 | New | Cursor lacks production infrastructure context -- can make naive deployment-impacting changes | MEDIUM | Stable | Technical | HIGH |
| R-037 | New | Monday MLK holiday narrows feedback window -- Josh only available Friday | MEDIUM | De-escalating | Schedule | HIGH |
| R-031 | Continuing | Schema drift between local and production databases | HIGH | Improving | Technical | HIGH |
| R-026 | Continuing | Programme scope expanding to 6 parallel workstreams with limited team | HIGH | Stable | Resource | HIGH |

## Open Questions Raised
- How should blockers, issues, and risks be structured in CLARA? (Deferred to Natalia/Diya/Stacy)
- What is the hierarchy between action plans and action items?
- How will the Customer Success Agent workstream be implemented -- copilot studio or something else?
- When will Gainsight API access be restored after the security breach?
- Where does Martin's separate app deploy -- same infrastructure or separate?

## Raw Quotes of Note
- "don't talk... let's avoid communicating of like, hey, it needs to do something with production because it doesn't understand. It doesn't have context of our infrastructure" -- BenVH, on Cursor's limitations
- "get a requirement from Diya Natalia, put it in the app and be like, oh hey guys, I implemented your feature, and they will definitely..." -- Richard, on stakeholder adoption tactics
- "cursor is a very powerful tool, but it's still like, the thing that I will always say is, like, it just doesn't have the context that the human brain does" -- BenVH
- "I'm telling you, man, we are screwed. This is way too good" -- Azmain (referenced from earlier), on AI capabilities

## Narrative Notes
This is the most architecturally significant session of the day. BenVH's whiteboard explanation of the migration pipeline (local changes -> Alembic versioned migration -> production schema update) demonstrates genuine infrastructure maturity -- he understands the root cause of the schema drift that has plagued deployments all week and is systematically addressing it through automated migrations. His demo mode architecture decision (static JSON over database flags) is the correct call for rapid iteration -- it avoids polluting production data, eliminates the overhead of flag-checking in every query, and provides a clean schema reference document as a side benefit. Richard's stakeholder management instincts are sharp: Liz's warning about Josh feeling sidelined is politically important, and Richard's "soft power move" strategy (get requirements from senior stakeholders, implement them, then present as their feature) shows sophisticated organisational navigation. The MLK Day holiday creates an unexpected scheduling constraint -- Josh feedback must happen Friday or wait until Tuesday, which delays the CSM rollout timeline. The broader programme scope discussion reveals Richard is trying to manage six workstreams with four people, and the Customer Success Agent workstream remains entirely undefined in terms of technology and stakeholders.
