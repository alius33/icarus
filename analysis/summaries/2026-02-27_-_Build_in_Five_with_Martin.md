# Build in Five with Martin -- First Substantive Scoping Post-Holiday
**Date:** 2026-02-27
**Attendees:** Richard Dosoo, Azmain Hossain, Martin Davies
**Duration context:** Short (~28 minutes)
**Workstreams touched:** WS6 Build in Five

## Key Points
- Martin's first detailed scoping session for Build in Five since returning from holiday. Richard confirms 75% time allocation approved for 12 weeks. Martin confirms the March 21 exceedance event as the target date.
- Dubai ambition reiterated: Azmain told Diya about Build in Five, and she responded with "if you guys can make it happen, we'll go." This is genuine motivational fuel but also adds pressure to an already aggressive timeline given Martin is still onboarding.
- Ben expanded the original three demo scenarios significantly while Martin was away. Still three scenarios but much broader in scope:
  1. **Data integration service** -- for customers claiming "your platform can't handle our data formats." Build CSV import, schema validation, and sandbox write. GSD template creates API, file upload endpoint, and validation logic.
  2. **Custom analytics views** -- React front-end querying Exposure IQ data with custom aggregation. Relatively straightforward compared to the others.
  3. **Webhook/notification integration** -- the most compelling scenario, based on a real lost deal. Golden Bear wanted to move to Guidewire's Policy Centre, which needs webhook notifications from the modelling platform. The team estimated six months; the customer would not pay. Build in Five could demonstrate this as a five-minute problem, proving the integration challenge is no longer a six-month problem.
- Martin raises a critical clarification question: is Build in Five producing pre-built prompts that sales teams follow step by step (scripted demo), or a live foundation that sales teams customise in real-time during customer meetings? Answer: the latter. A pre-configured foundation with API connections already wired, where the salesperson adds components (location analytics, specific data views) during the conversation based on customer needs.
- The GSD (Get Stuff Done) framework needs adaptation for non-technical users. Azmain redesigned the intake to start with "what problem are you trying to solve?" rather than "tell me what to build." The four-step guided process: (1) problem definition, (2) solution thinking, (3) recommended build, (4) detailed spec. Can take hours to days depending on user speed.
- Azmain intentionally designed friction into the process: if someone has a trivial problem, the structured question flow discourages them from wasting build resources. This is governance disguised as user experience. Only worthwhile problems survive the intake.
- Richard demos a web front-end he built for non-technical users to go through the guided requirement questions, which generates a brief detailed enough to fire directly at Cursor/Claude to build the app within architecture constraints. The demo is buggy and Richard struggles with Docker containers during the meeting.
- Four delivery mechanisms identified: (1) web front-end guided workflow, (2) set of prompts for Cursor/Claude Code, (3) requirements shopping market where pre-built BRDs can be combined into new specs, (4) a fourth mechanism that Richard forgot during the meeting and needs to document.
- Martin raises a valid point: two of the three demo scenarios use Underwriting IQ, so why not use Responder instead? Richard acknowledges these scenarios were Claude-generated and need validation with Rahul and other stakeholders for product relevance.
- Martin needs onboarding: Richard will send all programme documents, ServiceNow tickets for Claude Code access (requires admin rights, which Martin has), and AWS CLI setup instructions. A deeper scoping session planned for next week.
- Richard's laptop reboots during the meeting, Docker containers fail to start, and he cannot find mock-up files -- the pace of activity is outstripping his ability to stay organised.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Build in Five target remains March 21 exceedance event | Timeline | High | Martin / Richard / BenVH |
| Martin to first onboard and understand expanded scope before committing to timelines | Process | High | Martin |
| GSD framework to be adapted for non-technical user personas | Product | High | Azmain / Martin |
| Three demo scenarios to be validated with Rahul and other stakeholders | Scope | Medium | Martin |
| Programme documents to be moved to SharePoint, split from CLARA project folders | Operations | Medium | Azmain / Richard |
| Foundation approach chosen over scripted demo approach | Architecture | High | Richard / Martin |

## Action Items
| Action | Owner | Deadline | Confidence | Status |
|--------|-------|----------|------------|--------|
| Send all programme documents and updated scope to Martin | Richard | Today (27 Feb) | High | Open |
| Send ServiceNow tickets for Claude Code onboarding (AWS CLI + Claude Code install) | Richard | Today | High | Open |
| Set up deeper scoping session for Build in Five next week | Richard / Martin | Next week | High | Open |
| Create SharePoint folder structure for Build in Five (separate from CLARA) | Azmain | This week | Medium | Open |
| Validate demo scenarios with Rahul and other stakeholders | Martin | Next week | Medium | Open |
| Review expanded scope document and confirm understanding | Martin | Early next week | High | Open |
| Find and share mock-up UIs for shopping market delivery mechanism | Richard | Today | Medium | Open |
| Set up standup cadence for Martin, Azmain, and possibly BenVH | Azmain / Richard | Next week | High | Open |

## Theme Segments
1. **Casual opening and budget context** (0:00-2:00) -- Gambling banter, Richard apologises for laptop issues
2. **Programme status and timeline** (2:00-5:00) -- 75% allocation confirmed, 12 weeks, March 21 exceedance target, Dubai stretch goal
3. **Expanded demo scenarios** (5:00-12:00) -- Three scenarios from BenVH, Golden Bear webhook use case, data integration, custom analytics
4. **Framework design discussion** (12:00-20:00) -- GSD adaptation, four delivery mechanisms, web front-end demo, live vs scripted approach clarification
5. **Martin's onboarding and next steps** (20:00-28:00) -- Claude Code access, ServiceNow tickets, document sharing, scoping session next week

## Power Dynamics
- **Martin is methodical and grounded.** He asks the right clarifying questions about end goals before jumping in. His pushback on using Underwriting IQ vs Responder shows he is already thinking critically about product relevance. He wants to understand the full picture before committing to timelines.
- **Richard is the enthusiastic but disorganised leader.** Laptop rebooting, Docker failing, mock-ups lost -- the pace of activity is outstripping his ability to stay organised. His enthusiasm for the Dubai/exceedance opportunity is genuine but risks overpromising on an aggressive timeline.
- **Azmain provides the design philosophy.** His deliberate friction design (governance disguised as UX) and problem-first framing show strategic maturity. He shifts between programme management mode and design thinking fluidly.
- **BenVH is absent but his influence is felt.** He expanded the demo scenarios, has the exceedance panel slot, and is working on the deployment automation. He is the linchpin for whether the March 21 target is achievable.

## Stakeholder Signals
- **Martin Davies:** Methodical and cautious. Asks clarifying questions before committing. Comfortable pushing back (Responder vs IQ). Has admin rights on his machine, which accelerates onboarding. His question about scripted vs live demo shows he is thinking about practical sales team usage, not just technical capability.
- **Richard Dosoo:** Struggling with logistics -- laptop, Docker, missing files -- but enthusiastic about the opportunity. His decision to delay formal handover until Martin has reviewed all documents shows reasonable process discipline despite the timeline pressure.
- **Azmain Hossain:** Design philosophy is clear: deliberate friction, problem-first framing, governance through UX. His four-step intake process is a genuine innovation -- it filters out trivial requests while guiding non-technical users to actionable specifications.
- **Diya (absent, referenced):** Her "if you guys can make it happen, we'll go" about Dubai shows support but conditional commitment. She is not blocking but not driving either.
- **BenVH (absent, referenced):** Expanded demo scenarios and has the exceedance panel slot. His deployment automation work is a critical dependency for whether Build in Five demos deployed apps or localhost only.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Richard | Send all programme documents and scope to Martin today | Martin | High |
| Richard | Send ServiceNow tickets for Claude Code onboarding | Martin | High |
| Richard / Martin | Deeper scoping session next week | Both | High |
| Martin | Review expanded scope and confirm understanding | Richard | High |
| Martin | Validate demo scenarios with Rahul | Richard | Medium |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of purpose | 4 | Clear objective: onboard Martin to expanded Build in Five scope |
| Decision quality | 4 | Good decision to let Martin review before committing to timelines |
| Engagement | 4 | All three participants contributing; Martin asking good questions |
| Follow-through setup | 4 | Clear deliverables with immediate timelines (documents today, scoping next week) |
| Time efficiency | 3 | 28 minutes reasonable but laptop/Docker issues wasted some time |

## Risk Signals
- **March 21 timeline is aggressive.** Martin is still onboarding. He has not reviewed the expanded scope. Demo scenarios need validation with Rahul. Claude Code access requires ServiceNow tickets. The exceedance submission needs to go through an approval process. Three weeks is very tight.
- **Demo scenarios are Claude-generated, not validated.** Richard acknowledges the three scenarios were built by Claude from existing context. Martin correctly identifies that two use Underwriting IQ when Responder might be more appropriate. These need stakeholder validation before building.
- **BenVH's deployment automation is a critical dependency.** If Ben cannot get the CICD pipeline working, demos are limited to localhost -- which Richard acknowledges could "raise more questions" in a sales context.
- **Richard's organisational capacity is strained.** Laptop issues, Docker failures, inability to find mock-ups, documents stored on local machines instead of SharePoint. The programme's logistics are falling behind its ambition.
- **Fourth delivery mechanism forgotten.** Richard could not remember the fourth delivery mechanism during the meeting. If even the architect cannot recall the scope, how well-defined is it?

## Open Questions Raised
- Is the March 21 exceedance deadline realistic given Martin's onboarding time?
- Which of the four delivery mechanisms should be prioritised for the exceedance demo?
- Should the demo scenarios use IRP Responder APIs instead of Underwriting IQ, as Martin suggests for two of the three scenarios?
- What does the deployment side look like for demo apps -- localhost only, or does BenVH's automation need to be ready?
- What is the fourth delivery mechanism that Richard forgot?
- How does the exceedance submission approval process work and what is the lead time?

## Raw Quotes of Note
- "If you guys can make it happen, we'll go" -- Diya (via Azmain), on the Dubai opportunity tied to Build in Five
- "If the thing you're trying to build is not worth being diligent and planning it out, then it's not worth building" -- Azmain, on deliberate friction in the intake process
- "We told Golden Bear six months. It's like, no, it means five minutes" -- Richard, on the value proposition of the webhook demo scenario
- "I'm gonna have to Martin, check this in so you can see it somewhere" -- Richard, after Docker containers repeatedly failed to start

## Narrative Notes
This meeting marks Build in Five's transition from concept to execution, and the gap between ambition and readiness is immediately visible. Martin is methodical and grounded -- exactly the right disposition for turning an ambitious framework into a working demo. His clarifying question about scripted vs. live demos cuts to the heart of the product's identity. But three weeks to exceedance with a contractor still onboarding, demo scenarios needing validation, and deployment automation dependent on BenVH is extremely tight. Richard's enthusiasm is genuine but his organisational capacity is visibly strained -- the laptop rebooting, Docker failing, and mock-ups lost in local storage are symptoms of a programme moving faster than its coordination infrastructure. The Golden Bear webhook scenario is the strongest demo candidate because it is based on a real lost deal with quantifiable impact (six months reduced to five minutes). If the team can make that one scenario work convincingly, the exceedance demo could be a turning point for Build in Five's credibility. But the dependency on BenVH's deployment automation and the uncertainty about demo scenario relevance (Underwriting IQ vs Responder) mean the path to March 21 is narrow and fragile.
