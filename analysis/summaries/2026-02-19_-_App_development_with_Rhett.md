# App Development with Rhett
**Date:** 2026-02-19
**Attendees:** Richard Dosoo, Azmain Hossain, Rhett (Speaker 1), Ben (BenVH / Speaker 2)
**Duration context:** Medium (~27 minutes)
**Workstreams touched:** WS6 Build in Five, WS2 CLARA (tangentially)

## Key Points
- Rhett is being onboarded to app development. He has a static HTML app that needs to be pushed to GitHub and ported into Ben's skeleton app framework.
- Ben created a repo for Rhett but Git integration through Cursor has been flaky; Richard recommends GitHub Desktop with Moody's Okta SSO instead.
- Richard explains the dual-purpose infrastructure vision: internal productivity apps AND customer-facing demo apps on IRP's Risk Data Lake, all sharing a common tech stack and automated deployment pipeline so Ben does not become a bottleneck.
- The skeleton app framework provides authentication (Active Directory integration), role-based access control, and Moody's branding out of the box. Developers just define screen-level permissions.
- Richard describes three delivery channels for app building: (1) Cursor with cursor rules for IDE-comfortable users, (2) a lightweight UI chatbot that guides non-technical users through a spec-building workflow, and (3) a solutions catalogue / requirements database where people can cherry-pick features from previously built apps.
- The long-term vision is a "consulting AI platform" with MCP servers, skills libraries, and a solutions database so teams don't start from scratch each time.
- Richard notes CLARA has consumed all bandwidth, and the other five workstreams have had no meaningful progress. Martin returning from holiday will pick up Build in Five; Chris may help with CLARA to free Azmain and Richard for other programme work.
- Rhett asks about Cursor skills vs Claude skills; Richard explains Cursor's skills framework is less sophisticated (no project-level scoping, always in context window), but they'll make the skills succinct to manage token usage.
- The timeline estimate for the full app factory / consulting platform is 12-16 weeks, which Richard acknowledges is too long and needs consolidation.
- Rhett mentions exploring Replit over the weekend; Richard notes external tools like Replit cannot deploy to Moody's own cloud, which is the key differentiator of the internal platform.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Ben will manually port Rhett's code into the skeleton framework this one time | Tactical workaround | High | BenVH |
| Idris's app is prioritised because he has already sold the benefits to his senior leadership | Prioritisation | High | Richard / BenVH |
| Rhett's app deprioritised slightly behind Idris's | Prioritisation | Medium | Richard |
| Cursor rules file will be the standard for the wider team (Claude Code too restricted in access) | Technical direction | Medium | Richard |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Upload static HTML app code to GitHub repo | Rhett | ASAP | Open | Medium -- Rhett has struggled with Git tooling |
| Port Rhett's code into skeleton app framework | BenVH | After upload | Open | High -- BenVH willing but bandwidth is a concern |
| Install GitHub Desktop with Moody's Okta | Rhett | After call | Open | High -- straightforward task |
| Investigate Cursor skills framework parity with Claude skills | Richard / Azmain | TBD | Open | Low -- acknowledged as low priority |
| Reach out to Idris to set expectations on his app delivery | Richard | Next week | Open | Medium |

## Theme Segments
| Time Range | Theme | Key Participants |
|------------|-------|-----------------|
| 0:00-3:49 | Git onboarding and code upload logistics | Richard, Rhett, BenVH |
| 3:49-8:50 | App factory vision: skeleton framework, deployment pipeline, three delivery channels | Richard (dominant), BenVH |
| 8:50-14:37 | Solutions catalogue and consulting AI platform vision | Richard (demo), Rhett (questions) |
| 14:37-24:18 | Cursor vs Claude skills, Replit, resource constraints on five stalled workstreams | Richard, Azmain |
| 24:18-27:29 | Immediate next steps: Rhett upload, BenVH port, Idris priority | All |

## Power Dynamics
- **Richard dominates the conversation (>60% of speaking time)**, steering both the strategic vision and tactical decisions. He is acting as architect, product owner, and programme manager simultaneously.
- **BenVH is deferential but firm** on his own constraints -- agrees to do the manual porting "for now" but explicitly notes he is not scalable.
- **Rhett is a passive consumer** -- asking clarifying questions but not pushing back or contributing independent ideas. His technical gap (cannot use Git) positions him as a dependent.
- **Azmain is mostly silent** -- notable given his centrality to the programme. He interjects only on specific technical points (Cursor vs Claude skills, Bedrock access). This may indicate fatigue or deliberate deferral to Richard on vision topics.

## Stakeholder Signals
- **Rhett:** Engaged and eager but not technically self-sufficient. Exploring tools independently (Replit) which shows initiative but also indicates he may go off-piste without guidance.
- **Richard:** Candid about resource constraints. Five projects stalled while CLARA consumed everything. Diya is starting to ask questions about the other workstreams -- sense of mounting pressure. Shows pride in the platform vision but frustration at inability to execute.
- **BenVH:** Collaborative but setting clear boundaries. Willing to be hands-on temporarily. His comment about not being scalable is both accurate and a soft warning.
- **Azmain:** Brief mention of Bedrock access and future state -- focused on removing the Cursor token budget bottleneck. His relative silence contrasts with his usual verbosity in other meetings.

## Commitments Made
| Commitment | Who | To Whom | Specificity |
|------------|-----|---------|-------------|
| Will upload code to GitHub | Rhett | Richard / BenVH | Vague ("after this call") |
| Will port Rhett's code into skeleton | BenVH | Rhett | Conditional on upload |
| Will be available in ~2 hours if scripts error | Richard | BenVH | Specific timeframe |
| Will connect with Idris on his app priorities | Richard | Team | Next week |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of purpose | 3 | Started as onboarding for Rhett, expanded into full platform vision pitch |
| Decision quality | 3 | Decisions made were practical but short-term; no strategic decisions on platform timeline |
| Participation balance | 2 | Richard dominated; Rhett was mostly passive; Azmain barely spoke |
| Action item specificity | 3 | Actions clear but deadlines vague |
| Time efficiency | 3 | ~15 minutes of useful platform context that was not strictly necessary for Rhett's immediate needs |
| **Overall** | **2.8** | Meeting drifted from tactical onboarding into strategic vision presentation |

## Risk Signals
| Risk | Severity | Type |
|------|----------|------|
| Rhett's technical gap may cause delays in getting his code into the pipeline | MEDIUM | Delivery |
| BenVH as single point of failure for all app deployments | HIGH | Organisational |
| 12-16 week estimate for app factory is "too long" per Richard but no plan to compress | HIGH | Strategic |
| Five workstreams stalled -- Diya asking questions | HIGH | Programme governance |
| Cursor token budget ($100 allocation running out by 15th) constraining development | MEDIUM | Resource |
| Idris has made promises to his leadership that the team has not delivered on | MEDIUM | Stakeholder |

## Open Questions Raised
- When will the automated deployment pipeline be ready so Ben does not have to manually deploy each app?
- How do they consolidate the 12-16 week estimate for the full platform build?
- Can they get access to Claude via AWS Bedrock to reduce dependency on Cursor token budgets?
- What is the timeline for Idris's app delivery?
- Does Cursor have sufficient skills framework parity with Claude for the team's needs?

## Raw Quotes of Note
- "We can't scale Ben out. I mean, we could, but we we can't, right?" -- Richard Dosoo, on the bottleneck of having one person deploy everything
- "Ben has been pushing us really, really hard on Clara. So there's like five other projects that me and Azmain and Ben and Martin are supposed to be looking at. This is one, and we haven't really had a lot of time to invest in it." -- Richard Dosoo, on resource strain
- "If you're not familiar with an IDE, as soon as people see a Terminal and Terminal commands, they're just like, bro, this is a bit too much for me." -- Richard Dosoo, on why a lightweight UI wrapper is needed

## Narrative Notes
This meeting reveals the widening gap between Richard's ambitious platform vision and the team's execution capacity. What begins as a practical onboarding session for Rhett quickly becomes a showcase of the three-tier delivery model (Cursor rules, chatbot UI, solutions catalogue) that Richard has been architecting. The vision is coherent and compelling -- a self-service app factory that democratises development -- but the honest assessment of 12-16 weeks to build it, combined with five stalled workstreams and a Diya who is beginning to ask uncomfortable questions, paints a picture of a team drowning in strategic ambition.

The Idris data point is telling: the team's work has been marketed to banking leadership before delivery is complete, creating external obligations that further compress an already overloaded backlog. Richard's casual mention that he will be "signing off" after about an hour and heading to the gym suggests a deliberate effort to maintain personal boundaries despite the pressure -- or possibly a sign of acceptance that the evening hours alone cannot solve the capacity problem.

BenVH's positioning is noteworthy. His agreement to manually port Rhett's code is generous but his explicit caveat about not being scalable is a boundary-setting moment that the team should heed. If every new app requires BenVH's hands-on involvement, the app factory vision is architecturally dependent on a single human bottleneck -- precisely the problem it claims to solve.
