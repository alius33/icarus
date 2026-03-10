# Clara Standup
**Date:** 2026-03-05
**Attendees:** Azmain Hossain, Richard Dosoo, Chris M
**Duration context:** Medium (~20 minutes)
**Workstreams touched:** WS2 CLARA, WS4 Adoption Charter

## Key Points
- **Work allocation for the day**: Richard walked Azmain through a specific prompt for the scorecard playground -- creating a migration burndown tab based on Risk Link and Risk Browser switch-off dates (new fields), mirroring the existing use case burndown structure but with two rows per client (Risk Link and Risk Browser). Azmain confirmed he can build this.
- **Rhett's adoption charter work -- a source of friction**: Richard spent a full day integrating Rhett's Excel-based adoption charter work into the playground, and it went badly. He asked Claude to migrate Rhett's code into his app, but it integrated instead of migrating, forcing him to reverse-engineer Rhett's app into a PRD, create new prompts, and then discover half the spec was missing. He is now re-testing every feature manually.
- **Rhett acting independently**: Azmain raised that Rhett has not consulted anyone about his approach. The agreed plan was Word document to app (and back), but Rhett created an Excel-based approach without talking to Liz Couchman or any CSMs about adoption charters. Richard admitted Rhett probably did not get consensus but said he just wants to get it done and move on.
- **Azmain's frustration with Rhett**: He wanted to raise it with Ben Brooks, but Richard explicitly warned him against it: Rhett is "Ben's favourite," and challenging him would not be to Azmain's benefit. Richard advised to just push through, finish the work, and move past it.
- **Prior wasted effort**: Richard already spent his weekend rebuilding Steve Gentilli's app, only to have Steve go ahead and rebuild it himself anyway. This pattern of duplicated/wasted effort is wearing on Richard.
- **Chris's local setup**: Chris has CLARA's frontend running but the backend is not connecting (database/SQLAlchemy issues). Azmain told him not to debug manually -- just tell the AI agent to deploy it locally. Chris is methodically trying to follow READMEs which are outdated.
- **Documentation generated**: Azmain generated a full user-facing knowledge base for CLARA at 2am, currently in dev. The intent is to use it as context for a future CLARA AI chatbot assistant that can answer user questions about the app.
- **Daily work split**: Chris focuses on bugs/defects, Richard looks at feature/change requests (once he finishes Rhett's work), Azmain works on data model changes for migration burndown and new management dashboard.
- **Cursor model advice**: Azmain told Chris to switch from Sonnet 4.50 to Opus 4.6 for better results. Chris was using the default model to save budget.
- **Cost management**: Azmain acknowledged that BenVH has a cost-saving solution ready (Phantom Agent / OU-based allocation) but noted that Ben Brooks is not thinking about costs right now, so they should take advantage of the best models while they can.
- **Two rotating grads joining in April**: Azmain confirmed he was supposed to get them in March but they are delayed to April. Bug fixes will be a good onboarding path for them.

## Decisions Made
- Chris to focus on bugs/defects using the consolidated feedback list -> Azmain
- Richard to finish Rhett's adoption charter work and then review feature requests -> Richard
- Azmain to build migration burndown and scorecard dashboard changes -> Azmain
- Do not escalate Rhett issue to Ben Brooks -> Richard's advice to Azmain
- Chris to use Opus 4.6 instead of Sonnet 4.50 -> Azmain's advice

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Build migration burndown tab in playground (Risk Link/Risk Browser) | Azmain | Today | Open |
| Finish testing and deploying Rhett's adoption charter work | Richard | Today | Open |
| Get CLARA running locally (tell AI to deploy, skip manual README) | Chris | Today | Open |
| Work through bug/defect list from feedback analysis | Chris | This week | Open |
| Review feature/change requests after Rhett work is done | Richard | This week | Open |
| Push CLARA documentation/knowledge base from dev | Azmain | TBD | Open |
| Write script to periodically sync production and staging databases | BenVH | TBD | Open |

## Stakeholder Signals
- **Richard** is exhausted and frustrated. He explicitly said "I'm tired. I don't even want to argue anymore." The combination of Rhett's uncoordinated work, Steve's duplicated effort, and the general pace is wearing him down. He mentioned in other transcripts that he is looking at positions in New York.
- **Chris** is careful and systematic. He tries to follow documentation before diving in, which contrasts with the team's "just tell the AI to do it" approach. He is adapting quickly though.
- **Azmain** is frustrated with Rhett but accepting Richard's political advice. His exhaustion is showing (working at 2am, running through budgets in a day).

## Open Questions Raised
- Did Rhett actually consult any CSMs about his Excel-based adoption charter approach?
- When will the two April grads actually arrive and who are they?
- What happens when Rhett's work does not align with how CSMs actually use adoption charters?

## Raw Quotes of Note
- "I'm tired. I'm tired. I don't even want to argue anymore. I just want to get it done." -- Richard, on the Rhett situation
