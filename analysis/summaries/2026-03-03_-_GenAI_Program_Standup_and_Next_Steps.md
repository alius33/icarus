# GenAI Program Standup & Next Steps
**Date:** 2026-03-03
**Attendees:** Azmain Hossain, Richard Dosoo, BenVH (Speaker 3), Nikhil (Speaker 2), Chris M, Martin Davies (Speaker 1)
**Duration context:** Long (~37 minutes)
**Workstreams touched:** WS2 CLARA, WS4 Adoption Charter, WS6 Build in Five, App Factory / Infrastructure

## Key Points
- This is the formal onboarding call for Nikhil and Chris onto the CLARA team. Richard set the frame: they will help Azmain with CLARA first, then move to other workstreams (data pipeline, Salesforce agent) after 1-2 weeks of familiarisation.
- Resource allocation agreed: Nikhil splits 50% CLARA / 50% App Factory (helping BenVH). Chris focuses primarily on CLARA. This was approved by Stacy.
- Azmain set the work priority: (1) feedback/bug fixes, (2) blocker intelligence via Bedrock API, (3) adoption charters. He will create a group chat and share the consolidated feedback list.
- Nikhil confirmed he has the Bedrock API key working on his local environment using IAM roles (not hard-coded keys). He explained the approach: OU-specific IAM roles so cost centres can be tracked per department. This is a significant technical contribution.
- BenVH raised concerns about App Factory foundations: four apps in the pipeline, but he has not had time to focus on the input funnel or LLM agent orchestration framework. He explicitly asked to be kept away from CLARA LLM work so he can focus on App Factory.
- Azmain agreed to shield BenVH from CLARA work -- he should focus on App Factory unless there is a deployment emergency.
- Adoption charter complexity emerged as a major issue. Azmain showed the team what actual adoption charters look like -- multi-page documents with embedded images and diagrams. Richard explained the data flow should be one-directional initially (CLARA -> document), not bi-directional.
- Rhett's Excel-based adoption charter work mentioned as a complication -- created confusion because it contradicts the agreed Word-to-app approach.
- CLARA has zero formal documentation. Chris found the READMEs are outdated and incomplete. Azmain admitted he has never looked at them and just tells Cursor to deploy locally.
- Git hygiene improved: Azmain squashed 113 migration heads to one, pushed to staging successfully.
- Martin's Build in Five discussed briefly -- Richard will connect with him and Ben Brookes about Exceedance demo timeline this week.
- Nikhil and BenVH had already discussed App Factory architecture the day before -- BenVH wants something like Replit for internal use.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Nikhil: 50% CLARA / 50% App Factory; Chris: primarily CLARA | Resource allocation | High | Richard, Stacy-approved |
| CLARA priority: bugs first, Bedrock second, adoption charters third | Prioritisation | High | Azmain |
| BenVH stays out of CLARA LLM work; focuses on App Factory | Resource allocation | High | Azmain |
| Adoption charter data flow: one-directional initially (CLARA -> document) | Technical architecture | High | Richard |
| Git migration heads squashed from 113 to 1 | Technical debt | High | Azmain |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Create group chat and share consolidated feedback list | Azmain | Today | Open | High |
| Work through bug/defect list first | Chris | This week | Open | High |
| Help BenVH with App Factory 50% of time | Nikhil | Ongoing | Open | High |
| Connect with Martin and Ben Brookes about Exceedance demo | Richard | This week | Open | High |
| Send high-level adoption tracker slides to group | Richard | Today | Open | High |
| Promote staging build to production | Azmain | End of day | Open | High |

## Theme Segments
1. **Programme overview and onboarding frame** (0:00-5:00) -- Richard sets the stage for Nikhil and Chris
2. **Cursor/AI experience check** (5:00-8:00) -- Both new devs confirm comfort with Cursor; skills discussion
3. **CLARA work prioritisation** (8:00-14:00) -- Azmain walks through feedback, bugs, Bedrock, adoption charters
4. **Bedrock API and IAM architecture** (14:00-20:00) -- Nikhil's working solution; BenVH's cost centre concerns
5. **Adoption charter complexity** (20:00-25:00) -- Reality check on what parsing these requires
6. **App Factory and BenVH concerns** (25:00-33:00) -- BenVH asks for focus time; four apps in pipeline
7. **Documentation gap and wrap-up** (33:00-37:00) -- READMEs outdated; no formal CLARA documentation

## Power Dynamics
- **Richard sets the frame** but then defers to Azmain for specifics. Richard is the authority figure but Azmain runs the meeting operationally.
- **Nikhil makes a strong technical entrance.** Having Bedrock working locally with proper IAM role architecture is a legitimate contribution. His OU-based approach for cost allocation is exactly what BenVH was also thinking.
- **BenVH is defensive about his territory.** He explicitly asks to be kept away from CLARA so he can protect App Factory. The subtext (from earlier conversations) is that he does not want Nikhil encroaching.
- **Chris is humble and methodical.** Less experienced with Cursor (3 weeks vs Nikhil's 6-7 months) but has already built useful things (API library with 1,335 endpoints from the developer website).
- **Martin is peripheral.** Barely speaks; his Build in Five work is acknowledged but deprioritised in this meeting.

## Stakeholder Signals
- **Nikhil** -- Technically confident. Already thinking about Cat Accelerate migration plans, skill files, and Bedrock architecture. Wants to learn CLARA context documents and prompts. This is the first direct observation of him in a meeting -- he comes across as competent and eager, not malicious.
- **Chris** -- Methodical, willing to ask for help. Tried to set up CLARA locally by reading READMEs (which Azmain never does). Good complement to Azmain's "tell AI to do it" approach.
- **BenVH** -- Stressed about being spread thin. Explicitly said he wants to focus on App Factory foundations and the input funnel. Four apps in pipeline and he is one person.
- **Richard** -- Authoritative but concise. Delegates well. Mentions Exceedance demo but hedges on whether timelines will work.
- **Azmain** -- Overwhelmed but energised by having help. Admits to zero documentation, 2am work sessions. Setting up governance (group chat, consolidated list) to manage the expanded team.

## Commitments Made
| Who | Commitment | To Whom | Context |
|-----|-----------|---------|---------|
| Azmain | Share consolidated feedback list and create group chat | Chris, Nikhil | Onboarding |
| Chris | Focus on bugs/defects as primary task | Azmain | CLARA stabilisation |
| Nikhil | Split time 50/50 between CLARA and App Factory | Richard, BenVH | Resource agreement |
| Richard | Send adoption tracker slides and set up Build in Five sync | Team | Context sharing |
| BenVH | Focus on App Factory foundations (not CLARA LLM) | Azmain | Scope protection |

## Meeting Effectiveness
| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 8 | Clear roles, priorities, and next steps for new team members |
| Decision quality | 8 | Pragmatic prioritisation; manages expectations well |
| Participation balance | 7 | Good contributions from most; Martin quiet |
| Action item specificity | 7 | Actions clear with implicit (this week) timelines |
| Strategic alignment | 7 | Focused on near-term execution; longer-term planning deferred |

## Risk Signals
- **HIGH: Zero CLARA documentation.** Azmain never looked at READMEs. Chris found them outdated. Knowledge is entirely in Azmain's head. If Azmain is unavailable, no one can maintain CLARA independently.
- **HIGH: BenVH is a single overloaded point of failure.** Four apps in pipeline, App Factory foundations not built, and he is the only person who can deploy. He explicitly said he has not had time to focus on foundations.
- **MEDIUM: Nikhil/BenVH overlap on architecture thinking.** Both independently arrived at OU-based IAM role architecture for cost allocation. This is either productive convergence or the beginning of a territorial conflict.
- **MEDIUM: Rhett's uncoordinated adoption charter work.** Richard mentions it as something he is dealing with but does not flag the full extent of the wasted effort (revealed more in March 5 standup).

## Open Questions Raised
- How will the four other pipeline apps handle LLM agent needs?
- When will the Exceedance demo scope be confirmed?
- How should CLARA documentation be created and maintained?
- What is the integration pattern for Salesforce data access?

## Raw Quotes of Note
- "With requests, feedback, thoughts, ideas, dreams, wishes coming through at such a fast pace, I'm kind of drowning." -- Azmain, on being overwhelmed
- "I don't have detailed documents. I don't even have any... my goal was, seriously, this is -- we need to get on a call, and I need to run you through it." -- Azmain, on CLARA documentation

## Narrative Notes
This is the meeting where the programme formally scales from Azmain-solo to a four-person dev team (Azmain, Chris, Nikhil, BenVH). The most revealing moment is Nikhil's Bedrock API contribution -- he has something working that Azmain and the team have been struggling with. His OU-based IAM architecture is technically sound and aligns with what BenVH was independently designing. From a pure technical perspective, Nikhil is adding value. The tension between this contribution and the political dynamics (BenVH's credit-taking anxiety, Azmain's wariness) creates a complex picture. The documentation gap is alarming -- Azmain admitted he has never read the READMEs and cannot explain CLARA's architecture in writing. This is the programme's single largest knowledge risk.
