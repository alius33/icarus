# Partners Workflow Workshop -- Partner Management Requirements Discovery
**Date:** 2026-01-27
**Attendees:** Azmain Hossain, Speaker 2 (Rachel -- senior CSM with partner experience), Speaker 3 (Steve -- partner programme lead), Speaker 4 (Liz -- partner operations), Speaker 5 (Alexandra -- Life team partner tracking), Speaker 6 (Francois -- European partner lead), Speaker 7 (additional partner team member)
**Duration context:** Long (~1hr 10min)
**Workstreams touched:** WS2 CLARA (partner functionality), WS1 Data Quality (partner data gaps), WS6 Governance (partner engagement tracking)

## Key Points
- In-person workshop (London office) to define partner management requirements for CLARA, held immediately after the tracker next steps meeting
- Azmain walked the partner team through the current CLARA interface, showing customer tracking, blocker categories, use case progress, and account team structures
- The team identified that current Salesforce data is being enriched manually by Kathryn Palkovics Papavich -- partners want to eliminate this manual bottleneck just as the customer side does
- Partner-specific requirements emerged: (1) which customers have partners assigned, (2) partner engagement stage (introduced, proposal submitted, selected), (3) implementation progress through partner lens, (4) partner-specific blockers as a separate category
- Geography/region flagged as an important missing data point -- partners operate differently across North America, Europe, APAC, and the partner relationship network (e.g., Deloitte UK vs Deloitte US) has regional jurisdictions
- Blocker taxonomy needs expansion: current blockers are internal/product-focused, but partners surface external blockers (e.g., Duck Creek integration issues) that are not product blockers but implementation blockers
- The team discussed how partner-raised cases flow through the system: partners can log cases through the Moody's customer portal, but there is no systematic way to link partner-raised cases back to specific customer accounts in the tracker
- The PRM (Partner Relationship Management) tool was discussed -- it has been in selection for over a year, is in beta with the partner sales team (about 5 accounts), and is primarily designed for partner sales enablement (documentation, training, account mapping), not operational tracking
- Azmain committed to a timeline: this week finalise customer side, next week launch to CSMs, week after start building partner features, giving the partner team 7 working days to refine requirements
- Partner certification tracking was discussed but redirected to the PRM as more appropriate than the adoption tracker
- The group agreed on an MVP approach: start with a partner lens on existing customer data (which customers have which partners, what are the RAG statuses) without requiring manual input from the partner team
- Longer-term, the vision includes pushing clean data from CLARA into Gainsight, Moody's Salesforce, and Sales Recon -- partner data would flow through the same pipeline
- An "engagement ladder" concept was raised (from Gallagher experience) -- tracking the maturity and depth of partner relationships, not just operational issues
- Structured update questions (instead of free text) were proposed for partner team inputs, to ensure consistent data capture
- CSM workload concern raised: some CSMs pushing back on keeping track of implementation partner progress on top of their regular CSM duties
- The RMS Salesforce licence fee was highlighted as a waste -- Moody's paying the licence just for CSM weekly updates, everything else migrated
- Azmain explained the data flow vision: CLARA as the centralised clean data store, pushing structured data out to Gainsight, Sales Recon, and Moody's Salesforce when those systems are ready
- Only about 5 active partner implementations currently -- limited volume but strategic importance
- Azmain confirmed the call was being recorded and transcribed for notes capture

## Decisions Made
- Partner features to be built starting week after next (after CSM launch stabilises)
  - **Type:** explicit
  - **Confidence:** HIGH
- MVP partner view: read-only lens on customer data showing partner assignments and RAG status -- no manual input required initially
  - **Type:** explicit
  - **Confidence:** HIGH
- Partner-specific blocker category to be added as separate from product/internal blockers
  - **Type:** implicit (consensus)
  - **Confidence:** MEDIUM
- Certification tracking belongs in PRM, not CLARA
  - **Type:** implicit (redirected)
  - **Confidence:** MEDIUM
- Partner team has 7 working days to refine requirements before build starts
  - **Type:** explicit
  - **Confidence:** HIGH
- Geography/region field to be added at minimum as primary region (North America, European, APAC)
  - **Type:** implicit (agreed as useful)
  - **Confidence:** MEDIUM
- Manual partner-to-customer assignment as first step (either from Excel import or manual selection in UI)
  - **Type:** explicit
  - **Confidence:** HIGH
- Start with monitoring in-flight partner implementations, leave pipeline out of initial scope
  - **Type:** explicit
  - **Confidence:** HIGH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Import partner list into CLARA (from existing Excel) | Azmain | Week after next | Open | HIGH |
| Add partner assignment field to customer records | Azmain | Week after next | Open | HIGH |
| Build partner lens view (by partner: which customers, RAG statuses) | Azmain | Week after next | Open | HIGH |
| Add partner-specific blocker category | Azmain | Week after next | Open | MEDIUM |
| Define partner update questions/structured fields (not free text) | Partner team (Liz, Steve, Francois) | Within 7 working days | Open | MEDIUM |
| Investigate PRM API capabilities for future integration | Azmain + Steve | TBD | Open | LOW |
| Add geography/region field (at minimum primary region) | Azmain | TBD | Open | LOW |
| Determine case linking process -- partners to state which client when logging cases | Partner team | TBD | Open | MEDIUM |
| Share partner data requirements with Azmain in Excel format | Partner team | Within 7 working days | Open | MEDIUM |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Partner data requirements and gaps | Requirements/Discovery | "We don't want to duplicate efforts" -- Azmain | HIGH |
| Blocker taxonomy expansion for partners | Feature/Design | "We may need to add [blocker] type" -- Rachel | HIGH |
| Geography and regional partner dynamics | Data/Requirements | "From a partner perspective... you wouldn't want to take a US one to Deloitte where we don't have any relationship" -- Steve | MEDIUM |
| CSM-Partner-Implementation lead communication cadence | Process/Governance | "Whether it's weekly or fortnightly... something doesn't get lost in the ether" -- Rachel | MEDIUM |
| PRM vs CLARA scope boundaries | Architecture/Scope | "We don't want to duplicate... something that you guys will do in the PRM is not what we want to do in the tracker" -- Azmain | HIGH |
| Engagement ladder concept | Requirements/Innovation | "Tracking what you were trying to achieve with that client... creates a stickier partnership" -- Liz | MEDIUM |
| Gainsight data push strategy | Integration/Future | "Once RMS Salesforce is shut off... we're just going to push all this clean data into Moody's Salesforce and Gainsight" -- Azmain | HIGH |
| RMS Salesforce as legacy cost | Business Case | "Moody's is paying the RMS Salesforce licence fee because we use it for one thing and one thing only" -- Azmain | HIGH |
| Partner-raised case flow | Process/Gap | "How do we make sure it gets in this? Because at the moment... if the client reports it to the CSMs" -- Rachel | MEDIUM |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Azmain Hossain | Facilitator, builder, scope manager | Guided discussion, managed expectations, committed timelines | 30% |
| Rachel (Speaker 2) | Domain expert, requirements driver | Detailed partner workflow knowledge, raised governance needs | 25% |
| Steve (Speaker 3) | Partner programme lead | Provided PRM context, partner engagement stages, certification tracking | 15% |
| Liz (Speaker 4) | Partner operations | Engagement ladder concept, CSM awareness gaps | 10% |
| Francois (Speaker 6) | European partner perspective | Geography requirements, urgency framing, time management | 10% |
| Alexandra (Speaker 5) | Life team, tracker champion | Previous engagement with Azmain, partnership tracking interest | 5% |
| Speaker 7 | Additional partner team member | Minimal -- asked clarifying questions | 5% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Azmain | Diplomatic, protective of timeline | Engaged but boundary-setting | Scope management | "We can really think this through, discuss it, and then build it v1 v2 v3" |
| Rachel | Constructive, detail-oriented | Positive -- sees value, wants thoroughness | Blocker taxonomy | "One thing we need to think through is the blockers... we may need to add type" |
| Steve | Practical, PRM-aware | Stable -- wants to avoid duplication | Scope | "What's important is, is there a partner on there? Who is that partner? Are they implementing successfully?" |
| Liz | Enthusiastic, wants more | Positive -- sees broader relationship tracking need | Engagement ladder | "Something we just don't have... documenting where you are with that client" |
| Francois | Pragmatic, time-conscious | Engaged but wants to understand what is coming when | Timeline | "50 minutes left... can we somehow write down what are the next steps" |
| CSMs (referenced) | Pushback on workload | Negative -- some resisting tracking partner progress on top of CSM duties | Capacity | "How am I supposed to keep on top of these implementation projects" -- Liz relaying CSM feedback |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Azmain | Show partner team the partner view in the tracker | Week after next | Customer features stabilised | HIGH |
| Azmain | Import partner list from existing Excel | Week after next | Excel provided | HIGH |
| Azmain | Add partner assignment capability to customer records | Week after next | None | HIGH |
| Partner team | Define structured questions/fields for partner updates | Within 7 working days | None | MEDIUM |
| Partner team | Ensure partners state client name when logging cases | TBD | Process agreement | LOW |
| Francois | Will skip next week's meeting (away) but stay engaged | Next week | None | HIGH |

## Meeting Effectiveness
- **Type:** Requirements workshop / discovery
- **Overall Score:** 70
- **Decision Velocity:** 0.5
- **Action Clarity:** 0.6
- **Engagement Balance:** 0.8
- **Topic Completion:** 0.6
- **Follow Through:** 0.4

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-W4-26 | NEW | Partner requirements could expand CLARA scope significantly if not managed | MEDIUM | New | Workshop scope breadth | HIGH |
| R-W4-27 | NEW | PRM tool still in beta after a year of selection -- may not deliver partner management needs in reasonable timeframe | MEDIUM | Slow-moving | Steve's disclosure | HIGH |
| R-W4-28 | NEW | Partner-raised blockers have no systematic path into the tracker -- relies on CSM manual entry | MEDIUM | New | Workshop discussion | HIGH |
| R-W4-29 | NEW | Engagement ladder / relationship depth tracking -- desired but undefined requirement | LOW | New concept | Liz's proposal | MEDIUM |
| R-W4-30 | ONGOING | Gainsight team still blocking access for field-name alignment | MEDIUM | Stable | Azmain confirmed | HIGH |
| R-W4-31 | NEW | Only ~5 partner accounts with active implementations -- limited volume may not justify heavy investment now | LOW | Context | Steve's numbers | HIGH |
| R-W4-32 | NEW | CSM pushback on tracking partner implementation progress on top of regular duties | MEDIUM | New | Liz relaying feedback | HIGH |

## Open Questions Raised
- What structured questions should the partner update form contain?
- How will partner-raised cases be linked back to specific customer accounts systematically?
- When will the PRM be mature enough for the IRP partner team to use, and what data will it share?
- Should geography tracking be by contract entity, by implementation location, or by primary region?
- What is the minimum viable partner view that would be useful for the Monday weekly calls?
- How does the engagement ladder concept translate into data fields vs narrative tracking?
- Can CLARA push data into the PRM once it has API access?

## Raw Quotes of Note
- "This is a giant store of data, but it's also clean data" -- Azmain, selling the vision of centralised partner data
- "We can really think this through, discuss it, and then build it v1 v2 v3... we just keep improving it" -- Azmain, setting iterative expectations
- "Moody's is paying the RMS Salesforce licence fee because we use it for one thing and one thing only, CSM updates. It's an incredible waste of money" -- Azmain, on the legacy system cost
- "We don't want to duplicate efforts" -- Azmain, on CLARA vs PRM boundaries
- "How am I supposed to keep on top of these implementation projects? I can't do that on top of all my CSM work" -- Liz relaying CSM feedback on workload

## Narrative Notes
This workshop revealed both the opportunity and the danger of CLARA's growing scope. The partner team arrived with genuine enthusiasm and substantive requirements -- geography tracking, engagement ladders, structured update forms, partner-specific blocker categories, case linking workflows. Each of these is individually reasonable, but collectively they represent a significant expansion of CLARA's footprint beyond its core IRP adoption tracking mandate.

Azmain handled the scope management well, committing to an MVP partner lens (read-only view of customer data filtered by partner) as the first step, with a clear timeline (week after next) and a requirement-gathering window (7 working days) for the partner team. His repeated emphasis on avoiding PRM duplication shows awareness of the tool proliferation risk identified in the earlier Sales Recon meeting.

The PRM disclosure is notable -- the tool has been in selection for over a year and is still in beta with only 5 accounts. This suggests the corporate-level partner management solution is unlikely to materialise soon, which will increase pressure on CLARA to fill that gap. Steve's pragmatism about starting simple (is there a partner, who is it, are they implementing successfully) provides a sensible anchor against feature creep. The CSM workload concern -- relayed by Liz from direct feedback -- is a canary in the coal mine: if CSMs are already pushing back on tracking partner progress, adding more data entry requirements to the Monday review process could backfire. The real risk is that partner requirements, customer requirements, Sales Recon integration, Gainsight migration, and AI features all compete for Azmain's finite development bandwidth in the coming weeks.
