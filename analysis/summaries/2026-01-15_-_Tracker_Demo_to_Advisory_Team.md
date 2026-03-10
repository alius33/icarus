# Tracker Demo to Advisory Team
**Date:** 2026-01-15
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brooks, Liz (Couchman), Stacy (Dixtra), Christine, Steve Gentilli
**Duration context:** Long (~42 minutes)
**Workstreams touched:** WS2 (CLARA), WS4 (Friday/Adoption Charter)

## Key Points
- First external demo of the CLARA tracker to the advisory team. Richard frames it: the app lifts work from spreadsheets into a web app, deployed on AWS infrastructure. Next steps are getting feedback and then having Stacy prime CSM data entry.
- Azmain walks through the app: landing dashboard (bare bones, waiting for feedback), customer views with use cases pulled from the December golden source, blocker creation, action plans linked to blockers, and data issues.
- Liz asks the first critical question: is this existing (sold) customers only? Ben confirms: sold IRP customers only. No sales pipeline tracking -- "that would cause a mass freak out."
- Stacy raises data quality concerns: there is no guidance on what constitutes a good blocker description. Without structure, the data will be as messy as Salesforce. Ben proposes information icons with example descriptions for v1, and for v2, running blockers through an Anthropic API to validate quality.
- Steve Gentilli asks for dropdown categorisation on blockers to enable grouping and reporting (e.g., HD could be spelled multiple ways). Ben resists templating for now -- worried it will make data entry lazy ("they're blocked by HD as well, fuck it, move on"). Decides on free-form with good description guidance for v1, categorisation for later.
- Ben decides against having an owner field on blockers -- the owner is on the action plan, and the blocker is on the account. He does not want people putting product team names in blocker ownership.
- Discussion of action plans: linked to one or multiple blockers, with individual action items that can be assigned to people. Stacy suggests blocker-action plan linkage should be mandatory (no orphan blockers).
- Ben proposes client-verified action plans: a toggle for whether the customer has agreed that the action plan will resolve the blocker.
- Christine asks about internal vs external blocker categorisation (already handled via product/client/enablement type field).
- Liz raises a dependencies question: when does a known dependency (e.g., product feature on roadmap) become a blocker? Ben says Amber = at risk with dependency, Red = screaming halt.
- Steve Gentilli asks for a demo mode with complete fake data so people can see the target state. Azmain confirms he is building this.
- Liz makes a critical stakeholder management point: get Josh and George's feedback before rolling out to CSMs. Josh must feel consulted before CSMs start using it, otherwise he will feel sidelined.
- Liz also suggests watchlist/favourites functionality so non-CSM stakeholders can track accounts they care about without being assigned.
- Steve Gentilli suggests different persona-based views (CSM detail entry vs management overview).
- Ben's phasing: v1 stops after team members/collaboration tab. Get it right, get it populated. Charters/blueprints next. Partners third wave.

## Decisions Made
- Sold IRP customers only for now; no sales pipeline tracking -> Ben Brooks
- Blockers: free-form descriptions with guidance for v1; categorisation/templates for v2 -> Ben Brooks
- No owner field on blockers (owner goes on action plan, not blocker) -> Ben Brooks
- Action plans must be linked to blockers (mandatory) -> Stacy/Ben
- Add client-verified toggle to action plans -> Ben Brooks/Azmain
- v1 scope: dashboard through team members/collaboration. Charters/blueprints in v2 -> Ben Brooks
- Demo mode with complete fake data for people to explore -> Azmain
- Get Josh and George feedback before CSM rollout -> Liz's advice, accepted

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Add information icons with blocker description guidance | Azmain | v1 | Open |
| Build demo mode with complete fake data | Azmain | Before CSM demo | Open |
| Add watchlist/favourites feature | Azmain | Next iteration | Open |
| Get Josh Ellingson feedback before CSM rollout | Richard/Azmain | This week/next | Open |
| Get George Dyke feedback | Richard/Azmain | Monday or after | Open |
| Engage Stacy for CSM data priming once build is stable | Richard | After Josh/George feedback | Open |
| Review charter process with Liz/Christine/Steve (separate session) | Richard/Azmain | When ready | Open |
| Add client-verified toggle to action plans | Azmain | v1 or v2 | Open |

## Stakeholder Signals
- Liz is engaged and providing sharp, strategic feedback. She immediately identifies the Salesforce data quality problem and asks how this tool will avoid repeating it. Also catches that sales people (Danton, Alex Limford) are incorrectly listed as CSMs in the golden source data.
- Stacy is cautious but supportive -- her main concern is data quality and preventing the Salesforce mess from migrating to a new tool.
- Steve Gentilli is practical and thinking about usability (dropdowns for grouping, demo mode, persona-based views).
- Christine is thinking about audit trails and staleness detection (last modified dates at various levels).
- Ben Brooks is decisive about scoping: firmly keeping sales pipeline out, resisting premature categorisation, and phasing features clearly.
- Liz's warning about Josh is the most important stakeholder signal in this meeting.

## Open Questions Raised
- What is the proper definition of archetype? Multi-select needed because clients span multiple business classes.
- What does "region" mean in this context -- head office, sales region, or CSM region?
- How to distinguish blockers from dependencies? Ben suggests RAG status handles this (Amber = at risk/dependency, Red = halted).
- When will the charter process be discussed? Liz asks for a separate session when the team is ready.

## Raw Quotes of Note
- "I don't want people to come away with the incorrect interpretation, because with Andy Frappe that sticks and we can't get them off of it" -- Liz, foreshadowing Josh's exact concern the next day
