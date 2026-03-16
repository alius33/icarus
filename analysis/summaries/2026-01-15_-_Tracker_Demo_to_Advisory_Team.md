# Tracker Demo to Advisory Team -- First Stakeholder Demo with Feedback
**Date:** 2026-01-15
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brookes, Liz (Couchman), Stacy (Dixtra), Christine, Steve Gentilli
**Duration context:** long (~6000 words)
**Workstreams touched:** WS2 (CLARA), WS4 (Adoption Charter Generation)

## Key Points
- First demo of CLARA tracker to the advisory team (Liz, Stacy, Christine, Steve Gentilli) -- demoing from Azmain's localhost, not production
- Richard frames the session: tracker lifts work from spreadsheets into a web app; goal is to get feedback from Stacy primarily, then Liz and Christine, then deploy for CSMs to start populating data
- Azmain walks through: dashboard (bare bones, waiting for feedback on what to show), customer list (pulled from December golden source), use cases, blockers, action plans per customer
- Liz asks the scope question: existing customers only, or pipeline? Ben Brookes confirms: sold IRP customers only for now; pipeline tracking would "cause a mass freak out"
- Stacy raises the critical data quality concern: will there be guidance on what gets entered as blockers? "It doesn't make sense, that's not a blocker, or it's not worded appropriately" -- referencing Salesforce data quality problems
- Ben Brookes proposes: for v1, keep blockers free-form but add information icons with descriptions of what a good blocker looks like; for v2, use Anthropic API to validate blocker quality
- Steve Gentilli asks about drop-down categorisation for blockers to enable grouping/reporting -- HD could be "HD", "H-D", "high def" etc.
- Ben Brookes deliberately keeps blockers free-form initially: worried that pre-defined categories will make CSMs lazy ("they're blocked by HD as well, fuck it, I'll move on")
- Ben removes blocker owner field: owner belongs on the action plan, not the blocker itself; blockers are owned by the account
- Action plans link to one or multiple blockers; action items within plans can be checked off; action items have assignees
- Liz distinguishes action plans (tied to blockers) from action logs (general account activities not tied to blockers) -- Ben clarifies: this tool is migration-focused, not general account management; general action logs are a future/separate application
- Stacy pushes for mandatory action plans on blockers: "if we just have a blocker out there that has no action plan to it, it's worthless"
- Ben Brookes introduces "client verified" toggle for action plans: has the customer agreed that this action will unblock them?
- Christine raises internal vs. external blocker categorisation; Ben says the blocker type (product/client/enablement) already covers this
- Christine requests last-modified tracking at the account level: catch stagnant accounts where nobody has updated anything in weeks
- Liz suggests a "favourites" or "watch list" feature: non-CSM stakeholders (George, Josh) want to track specific accounts they're interested in without being the assigned CSM
- Azmain immediately embraces the idea: every entity has its own URL, so favouriting anything is straightforward
- Steve Gentilli asks about demo mode with complete dummy data -- Azmain confirms demo mode is in progress
- Steve raises multiple archetypes per account (multi-select needed) and the "what does region mean" definitional question (sales region vs. head office vs. CSM region)
- Liz gives strong positive feedback: "this is amazing... it's really good. Massive claps. It's clean, it's intuitive"
- Richard mentions getting Cursor running on Steve's laptop so advisory team can contribute to the codebase
- Next steps: v1 scope stops after team members and collaboration; Phase 2 is charters/blueprints/milestones; Phase 3 is partners
- Richard closes with: Azmain will continue building, reconnect with Stacy to prime CSMs for data entry, then revisit charters with Liz/Steve/Christine

## Decisions Made
- **V1 scope stops after team members tab**: Charters/blueprints/milestones deferred to Phase 2 -> Ben Brookes
  - **Type:** explicit
  - **Confidence:** HIGH
- **Blockers remain free-form in v1**: No drop-down categories yet; add guidance text for what a good blocker looks like -> Ben Brookes
  - **Type:** explicit
  - **Confidence:** HIGH
- **Remove blocker owner field**: Owner sits on the action plan, not the blocker; blocker belongs to the account -> Ben Brookes
  - **Type:** explicit
  - **Confidence:** HIGH
- **Action plans should be mandatory for blockers**: A blocker without an action plan is worthless -> Stacy (proposed), Ben Brookes (agreed)
  - **Type:** explicit
  - **Confidence:** HIGH
- **Add "client verified" toggle on action plans**: Track whether customer has agreed the action will unblock them -> Ben Brookes
  - **Type:** explicit
  - **Confidence:** HIGH
- **Add favourites/watch list feature**: Allow non-CSM stakeholders to star/track specific accounts -> Liz (proposed), Azmain (agreed)
  - **Type:** explicit
  - **Confidence:** HIGH
- **Tool is migration-focused, not general account management**: Action logs for non-blocker activities are out of scope for now -> Ben Brookes
  - **Type:** explicit
  - **Confidence:** HIGH
- **Multiple archetypes per account (multi-select)**: Accounts can span multiple archetypes -> Steve Gentilli (raised), Azmain (agreed)
  - **Type:** implicit
  - **Confidence:** HIGH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Add guidance text/info icons for blocker descriptions | Azmain | 2026-01-20 | Open | HIGH |
| Remove blocker owner field from UI | Azmain | 2026-01-17 | Open | HIGH |
| Make action plan mandatory when blocker exists | Azmain | 2026-01-20 | Open | HIGH |
| Add "client verified" toggle to action plans | Azmain | 2026-01-20 | Open | MEDIUM |
| Add favourites/watch list feature for all entities | Azmain | 2026-01-24 | Open | MEDIUM |
| Add last-modified tracking at account level | Azmain | 2026-01-24 | Open | MEDIUM |
| Change archetype field to multi-select | Azmain | 2026-01-20 | Open | HIGH |
| Clarify and define "region" field meaning | Azmain/Ben Brookes | 2026-01-20 | Open | MEDIUM |
| Complete demo mode with full dummy data set | Azmain | 2026-01-17 | In Progress | HIGH |
| Reconnect with Stacy to prime CSMs for data entry | Richard/Azmain | 2026-01-22 | Open | HIGH |
| Get Cursor running on Steve Gentilli's laptop | Richard | 2026-01-24 | Open | LOW |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Blocker data quality and structure | strategic | "it doesn't make sense, that's not a blocker, or it's not worded appropriately" -- Stacy | HIGH |
| Migration focus vs. general account management | strategic | "I almost don't want to conflate it with adoption. This is focused on migration right now" -- Ben Brookes | HIGH |
| Favourites/watch list feature | technical | "there's certain hot ones... these the ones I'm particularly concerned about" -- Liz | HIGH |
| Demo mode for onboarding | operational | "that kind of brings it to life, isn't it? If you're clicking in for the first few times" -- Steve Gentilli | HIGH |
| Blocker categorisation debate | strategic | "I'm worried that it gets lazy so that the data entry becomes... they're blocked by HD as well, fuck it, I'll move on" -- Ben Brookes | HIGH |
| Data quality concerns in golden source | operational | "shit data is, Danton's are probably all over the golden source" -- Ben Brookes | MEDIUM |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Ben Brookes | Product owner, making scope decisions | Defining v1 boundaries, deciding blocker structure, removing owner field, setting migration focus | 25% |
| Liz (Couchman) | Senior stakeholder, asking sharp questions | Scope question (existing vs pipeline), favourites feature, noting Josh needs inclusion | 20% |
| Stacy (Dixtra) | Quality gate, PM perspective | Pushing for mandatory action plans, raising data entry quality concerns | 15% |
| Christine | Operational thinker | Last-modified tracking, internal vs external blockers, dependency vs blocker distinction | 15% |
| Steve Gentilli | Detail-oriented, definitional questions | Multi-select archetypes, region definition, demo mode data request | 10% |
| Azmain Hossain | Builder, demoing | Walking through the app, absorbing feedback, proposing solutions | 10% |
| Richard Dosoo | Framer, closer | Opening context, managing time, setting next steps | 5% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Liz | Impressed, engaged, politically aware | Very positive | Overall tool | "this is amazing... really good. Massive claps. It's clean, it's intuitive" |
| Stacy | Constructive, quality-focused | Positive | Data entry standards | Concerned about Salesforce-quality data creeping in |
| Christine | Thoughtful, process-oriented | Positive | Tracking and accountability | Wants stagnant accounts to be visible |
| Steve Gentilli | Detail-focused, supportive | Positive | Data definitions | Raising important definitional issues (archetypes, region) |
| Ben Brookes | Decisive, protective of v1 scope | Stable | Scope management | Deliberately limiting scope to migration; deferring everything else |
| Natalia (referenced) | Impatient for deployment | Escalating | Timeline | Already asking "when can we start giving feedback?" |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Azmain | Will add guidance text for blocker descriptions | Before CSM rollout | None | HIGH |
| Azmain | Will add favourites/watch list feature | Before wider deployment | None | MEDIUM |
| Azmain | Will complete demo mode | Before Josh/George feedback | None | HIGH |
| Richard | Will reconnect with Stacy to prime CSMs | After Josh/George feedback | Feedback incorporated | HIGH |
| Richard | Will revisit charter conversation with Liz/Steve/Christine | After v1 data entry is stable | None | MEDIUM |

## Meeting Effectiveness
- **Type:** Product demo / stakeholder feedback session
- **Overall Score:** 82
- **Decision Velocity:** 0.8
- **Action Clarity:** 0.7
- **Engagement Balance:** 0.8
- **Topic Completion:** 0.6
- **Follow Through:** 0.6

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-038 | New | Data quality in golden source is poor -- Danton/Alex Limford listed as CSMs but are sales | MEDIUM | Stable | Data Quality | HIGH |
| R-039 | New | 280 accounts displayed but actual IRP sold accounts likely much fewer -- data overcounting | MEDIUM | Stable | Data Quality | HIGH |
| R-040 | New | Definitional ambiguity: "region", "archetype", "blocker vs dependency" undefined across team | MEDIUM | Stable | Process | HIGH |
| R-028 | Continuing | Stakeholder impatience growing -- Natalia asking when she can provide feedback | MEDIUM | Escalating | Stakeholder | HIGH |

## Open Questions Raised
- What does "region" mean: sales region, head office, or CSM assignment region?
- When does an issue become a risk, and when does a risk become a blocker? (PMO nomenclature)
- Should there be a status field on accounts: not sold, not started, in flight, complete?
- Where do non-migration activities (renewals, general account actions) get tracked?
- How will the charter generation feature work -- track charter data or generate charter documents?
- Who will fill in migration criticality data for each account?

## Raw Quotes of Note
- "it doesn't make sense, that's not a blocker, or it's not worded appropriately, to know what the hell it even means" -- Stacy, on Salesforce data quality
- "I'm worried that it gets lazy so that the data entry becomes... they're blocked by HD as well, fuck it, I'll move on" -- Ben Brookes, on why he resists pre-defined blocker categories
- "this is amazing... really good. Massive claps. It's clean, it's intuitive" -- Liz, on the overall tool
- "we added in night mode before we added in favourites" -- Azmain, self-deprecating humour
- "that kind of brings it to life, isn't it? If you're clicking in for the first few times" -- Steve Gentilli, on demo mode value

## Narrative Notes
This is the most important stakeholder feedback session of Week 2. The advisory team (Liz, Stacy, Christine, Steve Gentilli) sees CLARA for the first time and the response is overwhelmingly positive -- Liz's "massive claps" comment is the strongest endorsement the team has received. The substantive feedback is gold: Stacy's insistence on mandatory action plans for blockers, Liz's favourites feature, Christine's stagnant-account detection, Steve's multi-select archetypes -- all are immediately actionable improvements. Ben Brookes demonstrates sharp product ownership by holding the v1 scope boundary: migration-focused only, no general account management, free-form blockers with guidance rather than rigid categories. His decision to remove the blocker owner field (owners sit on action plans, not blockers) shows attention to data model design. The one concerning signal is the golden source data quality: 280 accounts showing when the real number is likely much lower, and sales people (Danton, Alex Limford) incorrectly listed as CSMs. This data quality issue, if not addressed before CSM rollout, could undermine credibility with the very users CLARA needs to win over. The session also surfaces important definitional gaps (what "region" means, blocker vs. dependency, archetype as multi-select) that reflect the broader challenge of translating messy real-world insurance operations into clean data structures.
