# Next 2 Weeks Plan
**Date:** 2026-02-23
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brooks
**Duration context:** Long (~30 minutes)
**Workstreams touched:** WS2 CLARA, WS4 Friday (Adoption Charter), WS6 Build in Five

## Key Points
- Priority planning for the next two sprints. First two weeks: finish CLARA features (solution architecture/blueprint attachment flow), address CSM feedback (Chanel's issues from last week), and platform infrastructure.
- Azmain pushes back on treating all feedback equally: the team needs to distinguish genuine blockers from cosmetic requests that users submit simply because they can.
- Build cadence established: one build this week (Wednesday), another next week. No more resource commitment beyond Azmain and Richard for these two weeks.
- Ben's app factory automation is becoming urgent: he's getting inundated with requests from the team to migrate apps, but can't scale until automation is done. This must be pushed up the priority list.
- Adoption charter work discussed: Liz confirmed templates are defined and in use. Azmain to start building basic adoption charter functionality when he gets time in the next two weeks, using the existing skeleton in the app.
- Solution blueprint is different from adoption charter: blueprints describe how to implement products end-to-end for a given use case. Both need to happen in parallel.
- API key crisis: need to get an OpenAI or Microsoft Copilot key to enable LLM integration in CLARA, while also chasing the Anthropic key through Bedrock. The team from "Cihan's lab experiment" is being difficult about providing an Anthropic key.
- Resource requests formalised: Nikhil 50%, Chris 50%, Martin (returning from holiday). Chris and Nikhil to be onboarded after the initial two-week sprint.
- Blocker intelligence around HD models identified as a priority for the next sprint.
- Steve Gentilli's solution-fit app is criticised: over-engineered, wants it as a separate standalone app with API integration to other apps rather than building it into CLARA. Richard spent his weekend rewriting Steve's code, only to find Steve had also been updating it independently.

## Decisions Made
- Two builds in next two weeks: Wednesday this week, another next week -> Azmain / Richard
- App factory automation pushed up priority list to unblock Ben -> Richard / Ben
- UAT issues and regression test pack are this week's deliverables -> Azmain / Richard
- Solution blueprint, HD blocker intelligence, and adoption charter work deferred to week 2 -> Azmain
- Idris's app prioritised over Rhett's and others due to relationship obligation -> BenVH

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Triage UAT issues from CSM feedback | Azmain / Richard | Today | Open |
| Get OpenAI / Copilot API key for CLARA LLM integration | Richard | This week | Open |
| Chase Anthropic key via Bedrock | Richard | This week | Open |
| Set up regression test pack and release notes process | Azmain / Richard | This week | Open |
| Communicate timeline to Rhett (pushed to next week) | Richard | Today | Open |
| Prepare slides for Christoph (Life team) overview | Azmain | Today/tomorrow | Open |

## Stakeholder Signals
- Ben Brooks wants adjacent teams (George's, Courtney's) to contribute resources when they benefit from the work, rather than everything falling on the core team.
- Azmain is exasperated by low-quality feedback from users (e.g., Asha demanding bulk edits for five items).
- Richard is frustrated by Steve's over-engineering and lack of coordination.

## Open Questions Raised
- What is the gating criteria for what goes into the app factory vs what gets rejected?
- How do they manage governance as more people start building apps independently?
- When will the Anthropic API key be resolved?

## Raw Quotes of Note
- "We need to draw a line between this is needed and people just giving feedback because it's in-house and they can just change stuff." -- Azmain Hossain, on feedback triage
