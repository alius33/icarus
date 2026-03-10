# GenAI Program Standup & Next Steps
**Date:** 2026-03-03
**Attendees:** Azmain Hossain, Richard Dosoo, BenVH (Speaker 3), Nikhil (Speaker 2), Chris M, Martin Davies (Speaker 1)
**Duration context:** Long (~37 minutes)
**Workstreams touched:** WS2 CLARA, WS4 Adoption Charter, WS6 Build in Five, App Factory / Infrastructure

## Key Points
- **Onboarding Nikhil and Chris**: This is the formal onboarding session for Nikhil and Chris onto the CLARA dev team. Richard framed it as load-balancing: Nikhil and Chris will help Azmain on CLARA for about a week to get familiar, then move to other workstreams (data pipeline, Salesforce agent).
- **Resource allocation agreed**: Chris will primarily focus on helping Azmain with CLARA. Nikhil will split time -- 50% helping BenVH with App Factory, remaining time on CLARA. This was approved by Stacy (who controls their allocation).
- **Nikhil and Chris's Cursor experience**: Nikhil has 6-7 months of Cursor experience and has built a multi-agent chatbot. Chris was introduced to Cursor three weeks ago but has built MCP servers and scraped developer websites. Both are still learning Claude skill files.
- **CLARA priority sequence agreed**: (1) Work through accumulated feedback/bugs, (2) Blocker intelligence with Bedrock API integration, (3) Adoption charters.
- **Adoption charter complexity**: Azmain showed the team what actual adoption charters look like -- complex Word documents with images, diagrams, and delivery plans. Richard clarified the intended data flow: CSMs enter data into CLARA, then CLARA generates the charter document (not the reverse). But Azmain raised the bidirectional problem: what happens when a customer marks up a charter and sends it back?
- **Bedrock API progress**: Nikhil confirmed he has it working locally using AWS Okta CLI tokens (no hardcoded keys). Deployment to AWS should be straightforward with proper IAM roles.
- **AWS cost allocation discussion**: BenVH raised the issue of multiple apps spinning up LLM workers on the same RMS AWS account with no cost segregation. Nikhil proposed using OU-specific IAM roles tied to Azure Active Directory to track costs per business unit. BenVH agreed this aligned with his thinking.
- **App Factory concerns**: BenVH expressed that he is stretched -- App Factory needs attention (four apps in the pipeline) but he is being pulled into LLM orchestration work. He described two priorities: (1) the input funnel (how apps get into the factory properly), and (2) the LLM agent framework. Azmain told BenVH to focus on App Factory foundations and stay away from CLARA LLM work unless specifically needed.
- **Solution blueprint**: Richard is working on the solution blueprint piece using Rhett's work, pushing it into dev. This is separate from Steve Gentilli's "solution fit matrix" which may become a separate app.
- **Git hygiene**: Azmain squashed 113 migration heads into one base level and pushed to staging. Plans to promote to production by end of day after also pushing reports functionality to staging.
- **Skills discussion**: Azmain added ~415 skills from three Git repos to his environment in one day. He admitted he does not know how to use them effectively yet but includes "use the appropriate skill" in prompts. Richard mentioned plans to build Moody's insurance consulting-specific skills as part of a future consulting AR platform workstream.

## Decisions Made
- Chris primarily on CLARA, Nikhil splits 50% App Factory / 50% CLARA -> Richard, agreed by team
- CLARA work priority: feedback first, then blockers, then adoption charters -> Azmain
- BenVH to focus on App Factory foundations, not CLARA LLM integration -> Azmain
- Adoption charter data flow: CLARA -> document (not reverse) as primary direction -> Richard
- Solution blueprint work continues separately under Richard -> Richard
- Promotion to production planned for end of day after staging validation -> Azmain/BenVH

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Consolidate all feedback into a list and share via group chat | Azmain | ASAP | Open |
| Set up Teams group chat for CLARA dev team | Azmain | ASAP | Open |
| Chris to focus on feedback/bug fixes | Chris | This week | Open |
| Nikhil to help BenVH with App Factory, then CLARA | Nikhil | This week | Open |
| Richard to send high-level slides on adoption tracker to team | Richard | ASAP | Open |
| Connect with Martin on Build in Five demo scenarios (exceedance) | Richard | Tomorrow/Thursday | Open |
| Push Rhett's solution blueprint work into dev | Richard | Today | Open |
| Validate staging builds and promote to production | Azmain/BenVH | End of day | Open |

## Stakeholder Signals
- **Nikhil** is technically capable and confident. Already talking about OU-based IAM roles and Azure AD integration. Risk: may step on BenVH's toes (flagged in other transcripts).
- **Chris** is methodical and cautious -- wants documentation and context before diving in. Good complement to Azmain's "just do it" approach.
- **BenVH** is clearly overwhelmed. He openly stated he has not had time to focus on App Factory to the degree he wants. His frustration about being pulled in multiple directions is palpable.
- **Richard** is trying to maintain strategic oversight while also doing hands-on work (solution blueprint). Still the bridge between vision and execution.
- **Azmain** is drowning in requests but delegating well. Acknowledged to the team that he has zero documentation -- everything is in his head and needs to be reverse-engineered.

## Open Questions Raised
- How to handle bidirectional adoption charter flow (customer marks up document -> how to get changes back into CLARA?)
- What is the governance for which apps go onto App Factory?
- Will the Bedrock API key work in the deployed AWS environment (works locally for Nikhil)?
- When will Chris and Nikhil have enough context to work independently on CLARA?

## Raw Quotes of Note
- "My goal was seriously... we need to get on a call, and I need to run you through it, because documentation..." -- Azmain, admitting CLARA has no formal documentation and exists in his head
