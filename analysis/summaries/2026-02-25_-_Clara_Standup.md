# Clara Standup — Martin Onboarding and Programme Catch-up
**Date:** 2026-02-25
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH, Martin Davies, Ben Brookes (remote)
**Duration context:** Long (~44 minutes)
**Workstreams touched:** WS2 CLARA, WS6 Build in Five, WS1 Training

## Key Points
- Martin Davies returns from holiday and receives a comprehensive catch-up on everything that has changed. The scope of Building in Five has expanded significantly during his absence.
- Richard articulates the three interdependent workstreams: Building in Five (Martin), App Factory automation (BenVH), and the Consulting AI Platform (Azmain). All have dependencies on each other.
- Resource approval confirmed: 75% of Martin's time secured for 12 weeks. Beyond 12 weeks, a business case is needed. Dubai demo to Dimitri and Olga is the stretch ambition if Build in Five delivers by March 21.
- The CLARA flat-pack concept is articulated clearly: take the Clara architecture, turn it into a templatised deployment so other OUs can spin up their own instance. Azmain argues against multi-tenant (avoids Salesforce team political pushback) and for independent deployments that can later be merged.
- Diya's governance session results shared with Martin: Maps team now offering to help (previously refused), Life team demo planned with Christoph.
- Richard presents the six-layer consulting AI platform architecture (design, data/tools, deployment) and the four delivery mechanisms: (1) web front-end guided workflow, (2) Cursor/Claude Code prompt sets, (3) requirements shopping market (pre-built BRDs), (4) voice input via Whisper.
- Discussion of GSD framework adaptation for non-technical users: Azmain designed deliberate friction into the intake process. Nine questions instead of Martin's original five to six, starting with problem definition rather than solution specification.
- Azmain and Richard discuss the post-12-week business case: a dedicated team of 4-5 people including a rotating grad from April 7.
- Martin suggests 100% allocation rather than 75%. He is methodical and willing to push back on unclear scope.
- Azmain's token budget crisis continues: Claude Max cut off mid-build, $750 spent in three days on Cursor.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Martin allocated 75% to Building in Five for 12 weeks | Resourcing | High | Ben Brookes (sign-off pending Stacy) |
| CLARA flat-pack model for cross-OU reuse, not shared multi-tenant | Architecture | High | Azmain |
| Four delivery mechanisms for Building in Five intake | Design | Medium | Richard / Azmain |
| March 21 exceedance event remains the target for Build in Five demo | Timeline | Medium | Richard / Martin |
| Dubai demo to Dimitri/Olga as stretch goal | Strategic | Low | Richard / Ben |

## Action Items
| Action | Owner | Deadline | Confidence | Status |
|--------|-------|----------|------------|--------|
| Send all programme documents to Martin for onboarding | Richard | Today | High | Open |
| Set up project folder structure in SharePoint (separate from CLARA) | Azmain | This week | High | Open |
| Get Martin access to Claude Code (ServiceNow tickets, AWS CLI) | Richard | This week | High | Open |
| Deeper scoping session for Build in Five next week | Richard / Martin / Azmain | Next week | High | Open |
| Get Stacy sign-off on Martin's time allocation | Richard / Ben | Today | High | Open |
| Meet with Nikhil and Chris to begin onboarding | Richard | Next 2 weeks | Medium | Open |
| Schedule standup cadence for Martin, Azmain, Richard | Richard | This week | High | Open |

## Theme Segments
1. **Programme catch-up for Martin** (0:00-13:00) -- Three workstream dependencies, resource approval, scope expansion since holiday
2. **CLARA flat-pack vs multi-tenant debate** (13:00-18:00) -- Azmain argues for independent deployments to avoid Salesforce team conflict
3. **Consulting AI platform architecture** (18:00-30:00) -- Six layers, four delivery mechanisms, deliberate friction design
4. **Build in Five demo scenarios and timeline** (30:00-40:00) -- March 21 exceedance, Dubai stretch, onboarding logistics
5. **Personal discussion** (40:00-44:00) -- Dubai, food, personal updates

## Power Dynamics
- **Richard is the programme narrator.** He does most of the talking, framing the expanded scope for Martin. This is simultaneously helpful (Martin gets context) and risky (Richard's interpretation becomes the canonical version).
- **Azmain is the co-architect.** His flat-pack concept, deliberate friction design, and platform thinking elevate him from builder to strategic contributor.
- **Martin is the new entrant** who needs to be brought up to speed. He asks good clarifying questions (why deploy if it is a local demo?) and suggests 100% allocation -- a stabilising, pragmatic presence.
- **BenVH is present but quiet.** His infrastructure work is referenced but he contributes minimally to this discussion.

## Stakeholder Signals
- **Martin Davies:** Returned, engaged, methodical. Asks clarifying questions about scope. Suggests 100% allocation. A stabilising presence but needs significant onboarding time before he can build.
- **Richard Dosoo:** In full programme-manager mode. Articulate about the vision but also acknowledging the vision has outpaced the execution capacity.
- **Azmain Hossain:** Growing strategic voice. Flat-pack concept, deliberate friction, product thinking. Still frustrated by tooling constraints.
- **Diya (absent, referenced):** Her governance endorsement is now the foundation for all planning. The "what happens after 12 weeks" question is the defining strategic horizon.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Richard | Send all docs to Martin today | Martin | High |
| Richard | Get Martin Claude Code access via ServiceNow | Martin | High |
| Richard | Get Stacy sign-off on Martin's time | Ben | High |
| Azmain | Set up SharePoint project folder | Team | High |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of purpose | 4 | Clear onboarding and catch-up objective |
| Decision quality | 3 | Good direction but demo timeline not validated by Martin |
| Engagement | 3 | Richard dominated; Martin mostly listening |
| Follow-through setup | 4 | Clear actions and next steps identified |
| Time efficiency | 2 | 44 minutes with extended personal tangent; technical issues with Docker/slides |

## Risk Signals
- **March 21 deadline is aggressive.** Martin is still onboarding, has not yet seen expanded scope in detail, needs ServiceNow tickets and Claude Code access before he can start building.
- **Scope expansion without validation.** Ben added significant scope to Martin's original demo scenarios while Martin was on holiday. Martin has not yet validated feasibility.
- **Onboarding time is real.** Martin needs documents, tool access, and context before he can be productive. At least one week of ramp-up.
- **Dubai as motivation.** The team is using the Dubai trip as a carrot, but if the demo is not ready, it becomes a missed promise that damages morale.

## Open Questions Raised
- What are the exact three demo scenarios for exceedance event?
- Should Build in Five use Responder API instead of Underwriting IQ for some scenarios?
- Is 75% or 100% the right allocation for Martin?
- What does the requirements shopping market look like in practice?

## Raw Quotes of Note
- "If I get hit by a bus, then everything just stops." -- Azmain (repeated from Diya meeting, now in Martin's hearing)
- "I want to go to Dubai" -- the recurring motivational refrain across the team
- "Dia or other senior people, they don't like big programmes. Small little contained things that you could do in six to eight weeks, they love that." -- Azmain, on corporate appetite for scope

## Narrative Notes
This catch-up session reveals how much the programme has evolved during Martin's two-week absence. What started as a relatively contained "build demo apps in five minutes" scope has expanded into an interconnected system of three workstreams with shared dependencies. Martin is a stabilising, methodical presence -- his question about why deployment is needed for a local demo cuts through scope creep. The flat-pack concept is strategically important: it allows the team to scale CLARA's value proposition to other OUs without creating a multi-tenant platform that would trigger Salesforce team resistance. The Dubai stretch goal adds urgency but also pressure on an already aggressive timeline.
