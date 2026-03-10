# Ben Explains New Dashboard
**Date:** 2026-01-06
**Attendees:** Ben Brooks, Richard Dosoo, Azmain Hossain, Martin Davies
**Duration context:** Long (~36 minutes, transcript ~187 lines)
**Workstreams touched:** WS2 (CLARA/IRP Adoption Tracker), WS4 (Adoption Charter -- data model for charters discussed)

## Key Points
- Ben reveals the CLARA v1 prototype he built over Christmas 2025 using Cursor -- far exceeding the original dashboard scope
- Origin: Ben became frustrated in a pre-IFLT standup when the team could not answer basic account status questions, prompting him to build a process management system that evening
- The prototype includes: customer dashboards, use case management with RAG status, blockers with mandatory action plans, data quality enforcement screens, charter management, blueprint tracking, milestones, partner management, executive reporting, and a report suite
- Core design principle: if a use case is not green it MUST have a blocker, and if there is a blocker it MUST have an action plan -- the system forces process rigour
- Key data quality revelation: updating the golden source with actual CSM data moved completed migrations from 28 to 41 -- 12 previously unreported completions
- Ben introduces the migration vs adoption distinction: migration = turning off Risk Link/Risk Browser; adoption = increasing platform usage. Use cases can be tagged as "migration critical"
- Initial feedback from Josh and George in December was positive -- both willing to work with the tool
- Azure deployment has been blocked for three weeks by security constraints
- Martin discovers a potential Azure workaround: database creation now must happen separately through the web app creation pathway
- Ben raises critical credibility point: SSO is essential -- without it, CSMs will treat the tool as a "posh spreadsheet" and ignore it, as they did with IRP Navigator
- Ben admits he does not know collaborative development practices (git, branching, code check-in)
- Richard outlines technical path: nail data model, create database, pump with data, deploy, iterate
- Richard proposes the data model needs ~10 tables starting from clients/projects, with use cases, timelines, and project plans hanging off them

## Decisions Made
- Ben's prototype accepted as the basis for CLARA v1 -- far beyond original dashboard scope: implicit team agreement -> Ben/Richard
  - **Type:** implicit
  - **Confidence:** HIGH
- Data model to be simplified: collapse issues and plans into one table with view-based granularity: Richard proposed -> Richard
  - **Type:** explicit
  - **Confidence:** HIGH
- Need to establish proper dev management (source control, branching, CI/CD): Richard/Ben agreed -> BenVH
  - **Type:** explicit
  - **Confidence:** HIGH
- Deploy to Azure App Service as target, with AWS as fallback: Team consensus -> Richard
  - **Type:** explicit
  - **Confidence:** MEDIUM
- Blueprints and partner tracking included in scope but may be deferred to v2: Ben suggested -> Ben
  - **Type:** deferred
  - **Confidence:** MEDIUM

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Refine data model -- collapse issues/plans table | Richard | Tonight | Open | HIGH |
| Try Azure deployment via web app create pathway | Martin | Tomorrow (between client meetings) | Open | MEDIUM |
| Get something deployed and demoable for next week | Team | Week of 12 Jan | Open | HIGH |
| Set up source code management and branching strategy | Richard/BenVH | Week of 12 Jan | Open | MEDIUM |
| Push latest code to GitHub main branch | Ben Brooks | Tomorrow | Open | HIGH |
| Call Arthur about Nicole's offer | Richard | Today | Open | HIGH |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| CLARA prototype reveal | technical | "I got really grumpy on the stand up that day" -- Ben | HIGH |
| Data quality crisis | operational | "We went from 28 to 41 completed migrations just by updating the fucking data" -- Ben | HIGH |
| Migration vs adoption distinction | strategic | "migration should mean when you turn off risk link and risk browser" -- Ben | HIGH |
| Azure deployment blocked | technical | "never ending hearing like promising leads and brick walls" -- Ben | HIGH |
| SSO as credibility requirement | strategic | "if people sign into this thing via SSO, they're going to think of it totally differently" -- Ben | HIGH |
| Dev collaboration gap | technical | "I haven't set anything up. I don't even know what you mean when you say, check code in and out" -- Ben | MEDIUM |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Ben Brooks | Product visionary, prototype owner | Dominates with demo walkthrough; sets product direction; exposes data quality narrative | 45% |
| Richard Dosoo | Technical strategist, architecture guide | Translates prototype to data model; proposes deployment path; manages timeline | 30% |
| Azmain Hossain | Observer, validates data quality relief | Notes that update button solves his biggest headache; limited engagement | 15% |
| Martin Davies | Technical explorer | Discovers Azure workaround mid-meeting; quiet but productive | 10% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Ben Brooks | champion | STABLE | CLARA vision and data quality | "we spent ages last year navel gazing... so I did it" |
| Richard Dosoo | champion | STABLE | Deployment urgency | "this should be like... it should just work for us" |
| Azmain Hossain | supportive | UP | Data quality solution | "you've solved the biggest thing that was a headache for me" |
| Martin Davies | supportive | NEW | Azure deployment | Actively troubleshooting during call |
| Josh (mentioned) | cautious | NEW | CLARA concept | "happy to lean into working with something like this" (December feedback) |
| George (mentioned) | supportive | NEW | CLARA concept | Positive in December preview |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Richard | Simplify data model | Tonight | None | HIGH |
| Ben Brooks | Push latest code to GitHub | Tomorrow | None | HIGH |
| Martin | Continue Azure web app exploration | Tomorrow (between meetings) | None | MEDIUM |

## Meeting Effectiveness
- **Type:** review
- **Overall Score:** 75
- **Decision Velocity:** 0.6
- **Action Clarity:** 0.6
- **Engagement Balance:** 0.4
- **Topic Completion:** 0.7
- **Follow Through:** 0.5

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-005 | OPEN | Azure deployment blocked by security constraints for three weeks | HIGH | ESCALATING | technical | HIGH |
| R-006 | OPEN | No collaborative development workflow in place | MEDIUM | NEW | process | HIGH |
| R-007 | OPEN | Ben sole builder with no code review or documentation | MEDIUM | NEW | resource | HIGH |
| R-008 | OPEN | CSM trust deficit -- may reject CLARA like they rejected IRP Navigator | HIGH | NEW | cultural | MEDIUM |
| R-009 | OPEN | Data quality in golden source -- 12 of 41 migrations were unreported | HIGH | NEW | data | HIGH |

## Open Questions Raised
- Can the Azure web app creation work without the deprecated experience?
- How to handle networking/VPC requirements that keep blocking deployment?
- Should blueprints and partner management be in v1 or deferred?
- How to get CSMs to trust and use the system?
- What is the right level of mandatory vs optional data entry?

## Raw Quotes of Note
- "I got really grumpy on the stand up that day and kind of said, like, why aren't we doing a proper programme, pipeline management process here" -- Ben Brooks, on the catalyst for building CLARA
- "We went from 28 to 41 completed migrations just by updating the fucking data. And it makes me want to cry." -- Ben Brooks, on data quality
- "if people sign into this thing via SSO, they're going to think of it totally differently to stumbling on what's essentially a posh spreadsheet on a network server" -- Ben Brooks, on credibility
- "essentially, you're taking O and M and you're basically breaking out into a data model" -- Richard Dosoo, translating Ben's vision

## Narrative Notes
This meeting is the first collective look at what Ben built over Christmas -- and it far exceeds expectations. What started as frustration in a standup has produced a structured adoption management system with enforced process rigour. The data quality revelation (12 unknown completed migrations) validates the entire thesis while exposing the cultural challenge ahead.

Three fragilities emerge. First, Azure deployment is completely blocked by corporate security constraints. Second, Ben openly admits he does not understand version control, meaning the codebase is unmanaged. Third, the IRP Navigator precedent -- CSMs refused to use a released product because they did not trust the data -- is a direct warning about adoption risk. Ben's insistence on SSO is not cosmetic; it is a lesson from that failure. The question now is whether the team can get something deployed and demoable fast enough to build momentum before bureaucratic friction kills it.
