# Next 2 Weeks Plan — Sprint Planning Session
**Date:** 2026-02-23
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brookes
**Duration context:** Long (~30 minutes)
**Workstreams touched:** WS2 CLARA, WS4 Friday (Adoption Charter), WS5 Navigator L1, WS6 Build in Five

## Key Points
- Sprint planning for the next two weeks following the Diya governance session. Richard proposes two builds (Wednesday drops) as capacity constraints.
- Azmain's Claude Max subscription expires today. He burned 75% of Cursor allowance ($750) in three days, with $200 left and 7 days in the cycle. Team scrambles for alternatives: Windsurf via Moody's SSO, OpenAI key fallback, Bedrock API access.
- Feedback management crisis: Azmain pushes back on treating all CSM feedback equally. Users submitting trivial issues (back button complaints) alongside genuine bugs. Need triage discipline and severity governance.
- Resource plan confirmed: Martin returning from holiday, Nikhil 50%, Chris 50%. Richard wants to defer onboarding until after initial two-week sprint to avoid slowing down.
- BenVH's App Factory automation identified as critical enabler: without pipeline automation, BenVH becomes manual deployment bottleneck. Four to five apps already queued (Idris, Rhett, Stacy, Eddie).
- Solution blueprints distinguished from adoption charters -- blueprints are implementation guidance documents, charters are success criteria and tracking. Both needed, separate scopes.
- Azmain proposes starting adoption charter work in week 2 using existing skeleton and Liz's documentation.
- Token budget crisis is concrete: Azmain switched to Windsurf mid-call using Moody's SSO, but team fundamentally unsustainable on current spend model.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Two builds in two weeks (Wednesday drops) as capacity constraint | Process | High | Richard / Azmain |
| Defer Chris/Nikhil onboarding until after initial two-week sprint | Resourcing | High | Richard |
| App Factory automation must be pushed up the priority list | Strategic | High | Richard / BenVH |
| Adoption charter work deferred to week 2 of sprint | Prioritisation | Medium | Azmain |
| Get OpenAI key first to show capability, then chase Anthropic key | Tactical | High | Richard / Azmain |
| Solution blueprints separate from adoption charters -- both needed | Scope clarification | High | Ben |

## Action Items
| Action | Owner | Deadline | Confidence | Status |
|--------|-------|----------|------------|--------|
| Triage UAT issues with Azmain | Richard / Azmain | Today | High | Open |
| Secure OpenAI API key as fallback | Richard | Today | High | Open |
| Chase Anthropic/Bedrock API key | Richard | This week | High | Open |
| Push UAT fixes from staging to production | Azmain | Today | High | Open |
| Start adoption charter expansion in week 2 | Azmain | Week 2 | Medium | Open |
| HD blocker intelligence on sprint plan | Azmain | Week 2 | Medium | Open |
| Solution blueprint scoping with Liz and Steve | Richard / Azmain | Next 2 weeks | Medium | Open |

## Theme Segments
1. **Sprint scope and priorities** (0:00-4:30) -- Richard outlines two-week plan: UAT fixes, API keys, enablement
2. **Feedback triage and severity governance** (4:30-8:00) -- Azmain pushes back on unfiltered CSM feedback; Ben agrees culturally
3. **BenVH app queue crisis** (8:00-13:00) -- Four apps queued, Steve's over-engineering, need automation before manual scale
4. **Solution blueprints vs adoption charters** (13:00-17:00) -- Scope clarification between Ben and Azmain
5. **Token budget crisis** (17:00-28:00) -- Claude Max expires, Windsurf SSO workaround, Bedrock as strategic solution

## Power Dynamics
- **Richard is the orchestrator** managing priorities, messaging external parties (Rhett, Stacy), protecting team bandwidth
- **Ben is the absent product voice** who has set strategic direction but is not present for operational chaos
- **Azmain is the overwhelmed builder** delivering despite tooling running out mid-build

## Stakeholder Signals
- **Richard Dosoo:** Managing competing demands (Idris, Rhett, Steve, Courtney) while protecting Azmain's build time. Frustrated by Steve's over-engineering and wasted weekend rewriting code.
- **Azmain Hossain:** At breaking point on tooling. Claude Max literally cut off mid-build at 5pm. Pragmatic about adoption charter timing. Advocates for triage discipline.
- **Ben Brookes:** Pushes for HD blocker intelligence and LLM integration as priorities. Clear on solution blueprint vs charter distinction. Relaxed about his MCP PowerPoint project timing.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Richard | Secure API keys (OpenAI first, then Anthropic) | Azmain | High |
| Azmain | Push UAT fixes to production today | Team | High |
| Richard | Tell Rhett his work is delayed to next week | Rhett | High |
| Azmain | Start adoption charter expansion in week 2 | Ben | Medium |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of purpose | 4 | Clear sprint planning |
| Decision quality | 4 | Good prioritisation and deferrals |
| Engagement | 4 | All three actively contributing |
| Follow-through setup | 3 | Actions identified but no formal tracking mechanism |
| Time efficiency | 3 | Productive but some tangential discussion on tools |

## Risk Signals
- **Token budget existential threat.** Azmain cannot build without AI tooling. Team juggling Cursor, Windsurf, personal subscriptions week to week. No sustainable funding model.
- **App Factory queue without automation = BenVH drowning.** Four to five apps queued, each requiring manual deployment.
- **Steve's over-engineering wastes Richard's time.** Richard spent a weekend rewriting code; Steve was simultaneously updating it with Rhett. Coordination failure.
- **Feedback deluge risks quality.** CSMs treating CLARA like enterprise product with severity-high on everything.

## Open Questions Raised
- How to gate what goes into the App Factory? What value criteria?
- Should Chris 50% be split between tracker maintenance and new features?
- When will Bedrock API access be properly provisioned?

## Raw Quotes of Note
- "I use 750 bucks in three days." -- Azmain, on Cursor spend
- "We are not putting stuff on spreadsheets. We can't do that." -- Azmain, refusing workarounds
- "These guys will go and build stuff that's a waste of time... they're just going to come to you and waste your time because they're stupid" -- Richard, on uncontrolled app proliferation

## Narrative Notes
This session exposes the operational reality beneath the governance veneer Diya just endorsed. The team has strategic approval for three pillars but is struggling with the most basic enablers: tooling budget, deployment automation, and feedback triage. Azmain's token exhaustion is a recurring weekly development blocker. Richard is stretched across a dozen relationships while protecting Azmain's build time. The App Factory bottleneck on BenVH is a ticking bomb. Steve's uncoordinated behaviour previews the chaos that will come when more people get Cursor access without governance.
