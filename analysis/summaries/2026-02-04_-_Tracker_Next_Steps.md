# Tracker Next Steps
**Date:** 2026-02-04
**Attendees:** Richard Dosoo, BenVH (Ben Van Houten), Azmain Hossain, Martin Davies, Alexandra (briefly)
**Duration context:** Long (~35 minutes)
**Workstreams touched:** WS2 CLARA, WS4 Adoption Charter, WS6 Build in Five

## Key Points
- BenVH pushed a build overnight but pull requests were going to main instead of develop -- stopped to avoid breaking production. Backend showing import errors (`role_permissions`).
- BenVH fixed the backend issue during the call -- restored ECS service
- Richard gave Martin a comprehensive programme overview for the first time -- all five workstreams plus emerging projects
- WS2 CLARA: absorbing adoption charter functionality; WS4 charter is now a CLARA function, not a separate app
- WS3 CS Agent: Sales Recon will provide the data pipeline; team builds prompts and Azure workflow on top
- WS6 Build in Five: two dimensions clarified -- internal (framework for non-technical staff) and external (live demos for client meetings at exceedance event)
- Martin admitted he was confused by "Cursor for Pipeline" naming -- thought it was a pipeline OF cursor projects, not using cursor FOR pipeline demos
- Azmain's partner section identified as quick-win (1 day work) before adoption charter
- BenVH introduced dev/staging/production environment separation -- explained the proper deployment flow
- Mobile responsiveness issues flagged: sidebar not collapsible, cards not stacking on small screens
- Azmain showed Moody's-branded UI redesign mockups -- positive reception
- Martin going on holiday from Wednesday next week for two weeks -- scoping must happen Monday/Tuesday
- Harry Lawrence (George's team) identified as a Build in Five guinea pig -- has apps but cannot get them hosted

## Decisions Made
- **Partner section is the next quick-win before adoption charter** | Type: Prioritisation | Confidence: High | Owner: Richard/Azmain
- **Adoption charter waits for Ben Brookes to finalise format with Steve Gentilli/Liz** | Type: Dependency | Confidence: Medium | Owner: Ben Brookes
- **Three-environment deployment: dev, staging, production** | Type: Technical/Process | Confidence: High | Owner: BenVH
- **Martin to scope Build in Five and produce directional estimates before holiday** | Type: Planning | Confidence: Medium | Owner: Martin/Azmain
- **Diya pitch planned: 2 slides, 15 minutes, all workstreams** | Type: Strategic | Confidence: High | Owner: Richard

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Fix backend import error in dev | BenVH | 2026-02-04 | Complete | High |
| Scope Build in Five project with directional estimates | Martin/Azmain | Before Martin's holiday (Feb 11) | Open | Medium |
| Build partner section in CLARA | Azmain | Next week | Open | High |
| Set up staging environment | BenVH | This week | Open | High |
| Apply UX branding changes to dev | Azmain | This week | Open | Medium |
| Prepare 2-slide pitch for Diya on all workstreams | Richard/Azmain | Next week (while Diya in London) | Open | High |

## Theme Segments
1. **Build Issues (0:00-6:00)** -- PR routing to main, backend import errors
2. **Programme Overview for Martin (6:00-22:00)** -- Richard walking through all five workstreams plus George and Idris requests
3. **Partner Section / Adoption Charter (13:00-15:00)** -- Quick-win prioritisation
4. **Build in Five Scoping (20:00-30:00)** -- Martin's project, timeline compression
5. **Infrastructure and UX (30:00-35:00)** -- Staging environment, mobile responsiveness, branding

## Power Dynamics
- **Richard** is the programme narrator -- synthesising everything for Martin's benefit, which also reveals how much he carries in his head
- **BenVH** is the infrastructure backbone -- fixing things live while others talk strategy
- **Martin** is being onboarded and is somewhat overwhelmed -- the naming confusion ("Cursor for Pipeline") reveals he has been working in the dark
- **Azmain** is the hands-on builder with practical instincts -- his partner section suggestion is a good prioritisation call

## Stakeholder Signals
- **Martin Davies:** Finally properly briefed. The "Cursor for Pipeline" naming genuinely confused him -- it was not poor attention, it was poor labelling. Now oriented but about to disappear for two weeks.
- **Richard:** Trying to impose project discipline on what has been a "just build it" culture. His comment about needing scope, timeline, resources, and a PM for each workstream is a significant shift.
- **BenVH:** Methodically building proper infrastructure (staging, CI/CD) -- the professional counterweight to rapid iteration. His deployment flow explanation is textbook engineering practice.
- **Alexandra:** Brief appearance -- her partner tracking needs are acknowledged but not yet being served.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| BenVH | Set up staging environment | Team | Firm |
| Martin | Produce Build in Five scope/estimates | Richard | Moderate (holiday compressed) |
| Azmain | Build partner section | Alexandra/Liz | Firm |
| Richard | Pitch to Diya next week | Team | Firm |

## Meeting Effectiveness
- **Clarity of purpose:** 8/10 -- Good combination of firefighting and strategic planning
- **Decision quality:** 8/10 -- Partner section prioritisation and staging environment are correct calls
- **Follow-through potential:** 7/10 -- Martin's holiday creates a gap for Build in Five
- **Stakeholder alignment:** 7/10 -- Team aligned; external stakeholders not present
- **Time efficiency:** 7/10 -- Some off-topic but generally productive

## Risk Signals
- **Martin's holiday creates a two-week gap for Build in Five** -- March 21 exceedance event is the target. Martin leaves Feb 12, returns late Feb. Approximately three weeks to build and demo after return. Severity: HIGH
- **PR routing confusion** -- Pull requests going to main instead of develop reveals process immaturity. One wrong merge could break production. Severity: MEDIUM
- **Azmain's bandwidth** -- He is now carrying CLARA features, data quality, Natalia's redesign, partner section, Build in Five scoping with Martin, cross-OU coordination, and Diya pitch prep. Severity: HIGH
- **Programme management gap** -- Richard's admission that they need to "treat these like projects in their own right" confirms that programme governance has been absent. Severity: MEDIUM

## Open Questions Raised
- When will Ben Brookes finalise the adoption charter format?
- How to handle Idris's banking app -- separate infrastructure or shared?
- Navigator L1 workstream -- needs a separate meeting, too complex for quick discussion
- How to get non-technical users building apps safely (the Build in Five challenge)

## Raw Quotes of Note
- "We haven't even, like, as Azmain knows, no shade, we've been mad busy. But this is basically, we need to treat these like projects in their own right" -- Richard, on the programme management gap
- "Don't worry about me, just getting some enjoyment of your plans" -- Richard, on Martin's Caribbean cruise vs his workload

## Narrative Notes
This session serves as a programme reset -- Richard using Martin's onboarding as an opportunity to articulate the full scope for the first time. The revelation that Martin was confused by the "Cursor for Pipeline" naming is a telling detail: if the people assigned to deliver the workstreams do not understand what they are building, the naming and communication need work. The partner section decision is a smart prioritisation call -- it is a genuine quick-win that serves a real user need while the more complex adoption charter work gets properly scoped. BenVH's introduction of staging environments marks a quiet but important maturation of the programme's engineering practices. The looming Diya pitch (2 slides, 15 minutes) is a high-stakes moment that will determine whether the broader programme gets executive air cover or is left to fend for itself.
