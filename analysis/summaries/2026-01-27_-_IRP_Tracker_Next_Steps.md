# IRP Tracker Next Steps -- Sprint Planning & Feature Prioritisation
**Date:** 2026-01-27
**Attendees:** Richard Dosoo, Ben Brooks, Azmain Hossain, BenVH (Speaker 2), Martin Davies (Speaker 1)
**Duration context:** Medium (~43 minutes)
**Workstreams touched:** WS2 CLARA (feature planning, data, deployment), WS5 Platform/Infrastructure (environments, API keys), WS4 Build in Five (Martin capacity)

## Key Points
- Following yesterday's demos and the portfolio review kickoff, this session focused on the critical next two weeks of CLARA development -- specifically what needs to be ready for the Monday Feb 2 launch
- Richard framed the core trade-off: double down on CLARA features vs split resources to advance platform infrastructure (BenVH's app builder, release pipeline, multi-environment setup)
- Ben Brooks firmly chose CLARA as the priority -- "fast and safe" -- agreeing that Martin and Azmain should work in parallel on tracker features rather than diverting Martin to platform work
- Key feature priorities confirmed for this week: (1) best possible data everywhere as a starting point, (2) role-based access control with admin controls, (3) audit trail everywhere, (4) weekly update feature for ongoing accountability
- The golden source data timeline was reconfirmed: end of day Wednesday Salesforce cutoff, Thursday build and release, Friday implementation leads populate data, Monday live review
- BenVH confirmed production environment is ready; he will take an RDS snapshot and migrate the database when given the green light -- targeting Thursday night after data cleanup
- Azmain proposed work split: he handles data chasing (Catherine, Natalia, Stacey) and audit trail; Martin handles RBAC with BenVH on backend
- Martin flagged capacity constraint -- he still has Canopies work -- but agreed to contribute to RBAC, with Azmain noting the audit trail discussion needs to happen first before Martin starts
- Ben Brooks wants Watson as the bellwether user -- if Watson adopts, everyone will follow; Watson was complaining about double entry on adoption charters
- Ben flagged charter functionality as important but agreed it could push to next week; charter entry should use adoption charter questions as structured form fields
- LLM API features discussed: AI-assisted blocker descriptions, natural language querying, transcript upload for gap analysis (compare what was said vs what was entered); all dependent on getting API key
- Richard received instructions from Gustavo about accessing Opus 4.5 via AWS Bedrock -- a potentially transformative infrastructure unlock
- Richard flagged need for project hygiene: PID, estimates, scope documentation -- Azmain acknowledged he does not have a finalised PID
- Alexandra (Life team) requested partner functionality and invited Azmain to a partner workflow workshop immediately after this meeting
- Ben Brooks acknowledged partner requests but explicitly deprioritised
- Infrastructure decision pending: stay on AWS, move to Azure, or migrate to MAP environment; Richard to introduce BenVH to Victor for definitive answer
- Ben Brooks insisted on human review/approval for any transcript-to-database writes -- no automatic updates

## Decisions Made
- Priority order: CLARA features first, platform infrastructure second
  - **Type:** explicit (Ben Brooks)
  - **Confidence:** HIGH
- Martin and Azmain to work in parallel on CLARA (not split between CLARA and platform)
  - **Type:** explicit
  - **Confidence:** HIGH
- Feature priority stack: (1) Data quality, (2) RBAC + admin, (3) Audit trail, (4) Weekly updates
  - **Type:** explicit
  - **Confidence:** HIGH
- Charter functionality deferred to next week
  - **Type:** explicit
  - **Confidence:** HIGH
- Partner functionality explicitly deprioritised
  - **Type:** explicit (Ben Brooks)
  - **Confidence:** HIGH
- End of day Wednesday data cutoff reconfirmed
  - **Type:** explicit
  - **Confidence:** HIGH
- Thursday build and release; BenVH to do RDS snapshot
  - **Type:** explicit
  - **Confidence:** HIGH
- No auto-write from transcript analysis to database -- Ben insists on human review/approval
  - **Type:** explicit
  - **Confidence:** HIGH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Chase Catherine, Natalia, Stacey for latest golden source data | Azmain | Wed Jan 28 | Open | HIGH |
| Implement RBAC with admin controls | Martin + BenVH | Thu Jan 29 | Open | MEDIUM |
| Implement audit trail (basic first, then field-level) | Azmain | Thu Jan 29 | Open | MEDIUM |
| Implement weekly update text entry feature | Azmain | Thu Jan 29 | Open | HIGH |
| RDS snapshot and production migration | BenVH | Thu Jan 29 night | Open | HIGH |
| Post in Teams channel about Wednesday data cutoff | Ben Brooks | Mon Jan 27 | Open | HIGH |
| Attempt to get AWS Bedrock Opus 4.5 API key | Richard | Mon Jan 27 | Open | MEDIUM |
| Distribute API key config to team once obtained | Richard | Mon Jan 27 | Open | MEDIUM |
| Introduce BenVH to Victor for MAP infrastructure decision | Richard + Ben Brooks | This week | Open | LOW |
| Set up project hygiene (PID, scope docs) | Azmain + Richard | Next two weeks | Open | LOW |
| Attend partner workflow workshop, guide but do not commit resources | Azmain | Mon Jan 27 (immediately after) | Open | HIGH |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Feature prioritisation and resource allocation | Planning/Strategy | "Priority number one has to be adoption tracker for a while longer" -- Ben Brooks | HIGH |
| Data quality and golden source timeline | Data/Operations | "End of tomorrow data is the data... every edge case can be mocked up by a CSM" -- Ben Brooks | HIGH |
| RBAC and admin controls | Feature/Technical | "We must have the restrictions on edits and read only version for others" -- Ben Brooks | HIGH |
| Transcript-based gap analysis | AI/Innovation | "We record and transcribe that call... we pass that through an LLM" -- Azmain | MEDIUM |
| AWS Bedrock API access | Infrastructure | "Apparently we can get a key for Opus from our AWS deployed environment" -- Richard | HIGH |
| Project hygiene and governance | Process | "We should have... plan, estimates, scope, all of those things" -- Richard | MEDIUM |
| Watson as bellwether user | Adoption/Strategy | "If we can get him to come along, everyone will follow" -- Ben Brooks (paraphrased) | HIGH |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Ben Brooks | Strategic decision-maker, priority setter | Chose CLARA over platform, set deadlines, overrode tangents | 30% |
| Richard Dosoo | Operational coordinator, pragmatist | Framed trade-offs, pursued API keys, flagged governance gaps | 25% |
| Azmain Hossain | Lead builder, scope definer | Proposed work split, flagged partner workshop, listed features | 25% |
| BenVH | Infrastructure readiness confirmator | Confirmed prod environment, clarified migration process | 10% |
| Martin Davies | Constrained resource | Accepted RBAC work, flagged Canopies constraint | 10% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Ben Brooks | Focused, decisive | Stable -- doubling down on tracker | Priorities | "Fast and safe, right? Priority number one has to be adoption tracker" |
| Richard | Pragmatic, stretched | Slight concern -- recognises governance gaps | Project hygiene | "We should have all the project stuff, plan, estimates, scope" |
| Azmain | Energised, multitasking | Positive -- clear work plan, but pulled toward partner workshop | Work split | "If me and Martin can split the work... I'm going to start chasing Catherine, Natalia, Stacey" |
| BenVH | Steady, professional | Stable -- ready to execute migration | Prod readiness | "The production environment is pretty much good to go" |
| Martin | Constrained but willing | Slight strain -- Canopies vs CLARA tension | Capacity | "My only slight issue with this is I've still got some Canopies" |
| Alexandra (referenced) | Eager | Positive -- wants partner features, pulling Azmain into workshop | Partner management | "Asked me to be involved so that from the get go, I can help shape" |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Ben Brooks | Post Wednesday data cutoff announcement in Teams | Today/tomorrow | None | HIGH |
| Azmain | Chase data owners and complete data preparation | By Wednesday | Catherine/Natalia cooperation | HIGH |
| Azmain | Build audit trail and update feature | By Thursday | Martin handles RBAC | HIGH |
| Martin | Build RBAC feature | By Thursday | BenVH backend support, Canopies management | MEDIUM |
| BenVH | Execute RDS snapshot and prod migration | Thursday night | Green light from team | HIGH |
| Richard | Get AWS Bedrock API key | Today | Gustavo's instructions + team availability | MEDIUM |
| Richard | Introduce BenVH to Victor | This week | None | LOW |
| Ben Brooks | Ping Josh, George, Natalia, Stacey, Catherine about Monday readiness | This week | None | HIGH |

## Meeting Effectiveness
- **Type:** Sprint planning / prioritisation
- **Overall Score:** 82
- **Decision Velocity:** 0.9
- **Action Clarity:** 0.8
- **Engagement Balance:** 0.7
- **Topic Completion:** 0.8
- **Follow Through:** 0.7

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-W4-20 | ONGOING | Aggressive Wed-Thu-Fri-Mon timeline with thin error margin | HIGH | Stable | Reconfirmed from yesterday | HIGH |
| R-W4-21 | ONGOING | Martin's split between Canopies and RBAC | MEDIUM | Stable | Martin flagged again | MEDIUM |
| R-W4-22 | NEW | Azmain being pulled into partner workshop at expense of core tracker work | LOW | New | Alexandra request | MEDIUM |
| R-W4-23 | NEW | No PID or project documentation -- governance gap | MEDIUM | New awareness | Richard raised | MEDIUM |
| R-W4-24 | ONGOING | Data integrity from Josh's "edit and play" instruction -- needs fresh load | MEDIUM | Needs fresh load | Azmain flagged | HIGH |
| R-W4-25 | NEW | Ben Brooks insists on human approval for all transcript-to-database writes -- limits AI automation potential | LOW | Philosophical difference | Ben vs Azmain | MEDIUM |

## Open Questions Raised
- Can the audit trail be made field-level granular in time for Thursday, or will it ship as record-level only?
- Will Martin have enough bandwidth to deliver RBAC while managing Canopies commitments?
- Can the AWS Bedrock API key be obtained today, or will it require waiting for MAP team to come online?
- What happens to the data Josh told people to play around with -- does it need a full wipe?
- How will the partner workshop outputs translate into tracker requirements without derailing the core timeline?

## Raw Quotes of Note
- "Fast and safe, right? So I think priority number one has to be adoption tracker for a while longer" -- Ben Brooks, setting the strategic direction
- "We're building technical debt as we go, but we'll fix it" -- Richard, on the pragmatic approach
- "If he says one more time, please don't use this tracker. I'm going to fly over there and punch it" -- Ben Brooks, on Josh's resistance to CLARA
- "It's just not a priority" -- Ben Brooks, on partner functionality requests
- "We were always gonna have to do a fresh" -- Azmain, on the need for a clean data load

## Narrative Notes
This was a disciplined sprint planning session that translated yesterday's strategic decisions into concrete work assignments. Ben Brooks's "fast and safe" principle is the governing philosophy: move quickly on features that remove adoption barriers (RBAC, audit trail, data quality) while deferring everything that does not directly enable the Monday launch. His explicit deprioritisation of partner functionality -- despite Alexandra's eagerness -- shows clear strategic focus.

The resource allocation question (double down on CLARA vs split for platform work) was the key trade-off, and Ben's answer was unambiguous. This means BenVH's platform vision (app builder, multi-environment, CICD standardisation) gets delayed further, which could create frustration if not managed. Richard's governance concern (no PID, no scope documentation) is valid but was brushed aside in favour of velocity -- a pattern that is becoming characteristic of this programme's operating style. The team is deliberately trading governance discipline for speed, betting that demonstrable progress will create the organisational support needed to formalise later.

The AWS Bedrock discovery is genuinely exciting for the team -- if they can access Opus 4.5 through corporate infrastructure, it eliminates a significant cost and access bottleneck for AI features. This could accelerate the transcript analysis, natural language querying, and AI-assisted data entry features that Ben Brooks envisions as CLARA's differentiators.
