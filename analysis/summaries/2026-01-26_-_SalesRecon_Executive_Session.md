# [IMP] Sales Recon -- Cross-Business Alignment Session
**Date:** 2026-01-26
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brookes, Jamie (Sales Recon lead), Ari Lahavi (Head of Applied AI), Speaker 1 (senior CS leader -- Divya's designee or Colin Holmes), Idrees (Banking CS), Craig (Corporate CS), Rupert, Irina, Matt (absent but joined late), Bernard, Mike Steele, Gustavo, others
**Duration context:** Long (~1hr 29min)
**Workstreams touched:** WS3 Sales Recon Convergence, WS2 CLARA, WS1 Data Quality, WS6 Governance

## Key Points
- Pivotal cross-functional alignment meeting bringing Insurance CS, Banking CS, Corporate CS, Life team, and the Sales Recon/Applied AI team together for the first time collectively
- Jamie presented the Sales Recon platform vision: a customer intelligence layer that aggregates Salesforce data, external intelligence, and interaction data into actionable insights for sales teams -- with conversation starters, gap analysis, and nudge-based data enrichment
- The Sales Recon team has been working on the platform for approximately a year; currently rolling out to sales ops teams with a UAT target for April
- Richard and Azmain presented CLARA (the IRP adoption tracker) as a complementary but distinct tool -- purpose-built for the IRP adoption problem, not a generic CRM replacement
- Ben Brookes framed CLARA as bespoke to insurance's IRP migration challenge, suggesting it should remain insurance-owned but with API integration points to Sales Recon
- Key strategic question emerged: should CLARA data feed into Sales Recon, or should Sales Recon provide APIs for CLARA to consume? Consensus leaned toward bidirectional integration via API, not consolidation
- Bernard demonstrated a Copilot-built customer insight agent pulling from Salesforce, Power BI, and Databricks usage data -- showing recurring support case themes and account health scoring
- Idrees confirmed Banking CS has a quantitative scoring model (five factors including support cases, severity, qualitative CSM input) that differs from Insurance's approach
- Craig (Corporate) highlighted CSM-driven lead identification (CSQL) as a gap -- wanting tools that help CSMs surface cross-sell opportunities naturally during customer conversations
- Jamie's team plans a pilot in February with users from each CS business unit
- The Sales Recon team offered to make their Salesforce connector available to internal agent builders, so teams do not have to build their own data extraction
- Gainsight integration remains blocked -- the Gainsight implementation team refuses to provide even read-only access until March
- Divya Sawhny was behind expanding this meeting's invite list, signalling executive sponsorship for cross-team coordination
- Ari articulated the core vision: Sales Recon as a guided system that knows what it needs to close deals, surfaces gaps, and nudges users for missing information -- not just a data dump

## Decisions Made
- CLARA and Sales Recon will remain separate tools with API integration rather than consolidation
  - **Type:** implicit (consensus direction, not formally ratified)
  - **Confidence:** MEDIUM
- Sales Recon will provide APIs/connectors so internal teams can access Salesforce data without building their own
  - **Type:** explicit (Jamie's offer)
  - **Confidence:** HIGH
- A regular check-in cadence will be established across CS business units and Sales Recon team
  - **Type:** explicit
  - **Confidence:** MEDIUM
- Pilot users from each CS team to be identified for February Sales Recon pilot
  - **Type:** explicit
  - **Confidence:** HIGH
- UAT and rollout planning for April needs to be coordinated with Conrad's team (sales ops)
  - **Type:** explicit
  - **Confidence:** MEDIUM

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Set up regular check-in cadence across CS teams and Sales Recon | Richard + Jamie | February 2026 | Open | MEDIUM |
| Plan key pilot users for February Sales Recon pilot across all CS units | Jamie + each CS lead | February 2026 | Open | HIGH |
| Consolidate CS requirements list and present to Jamie's group | Richard | February 2026 | Open | MEDIUM |
| Catalogue data input processes across CS teams (where data lives, what formats) | Jamie's team | February 2026 | Open | MEDIUM |
| Plan UAT and rollout coordination with Conrad for April | Richard + Jamie | March 2026 | Open | LOW |
| Decide who runs the April rollout (sales ops vs another team) | Jamie | TBD | Open | LOW |
| Share Copilot agent prompts/approach with Sales Recon team | Bernard + Richard | TBD | Open | LOW |
| Add Richard to Divya's cross-functional coordination group | Speaker 1 | Immediate | Open | HIGH |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Sales Recon platform overview and vision | Strategic/Product | "Everything we are doing is an excuse for [shared customer understanding] to happen" -- Ari | HIGH |
| CLARA demo and IRP-specific problem framing | Product/Demo | "Very deliberately designed around the specific problem... around IRP adoption" -- Ben Brookes | HIGH |
| Data quality and CRM fragmentation | Operational | "Salesforce data quality has been an issue for years" -- Mike | HIGH |
| Cross-sell opportunity identification (CSQL) | Strategic/Sales | "Can we use Sales Recon... for CSMs to identify potential use case questions" -- Craig | MEDIUM |
| Integration architecture (push/pull, APIs, agent-ready) | Technical/Architecture | "The answer to the questions... should be bridges and harmonisation of the experience" -- Ari | HIGH |
| Gainsight migration complications | Operational/Blocker | "We can't wait. We can't have that risk unmanaged" -- Richard | HIGH |
| Customer intelligence layer concept | Strategic/Vision | "I want us to have a shared understanding across the organisation of our customers" -- Ari | HIGH |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Richard Dosoo | Meeting chair, CS representative, presenter | Framed agenda, navigated time, positioned CLARA | 20% |
| Ari (Speaker 2) | Strategic authority, Sales Recon vision owner | Set vision, guided integration discussion, validated approaches | 20% |
| Jamie (Speaker 3) | Sales Recon product lead | Presented platform status, offered APIs, managed expectations | 18% |
| Ben Brookes | Strategic framer for CLARA | Positioned CLARA as insurance-owned, bespoke tool | 8% |
| Azmain Hossain | CLARA demo presenter | Showed tracker capabilities, explained data strategy | 10% |
| Idrees | Banking CS perspective | Provided banking context, validated data quality issues | 5% |
| Craig (Speaker 10) | Corporate CS perspective | Raised CSQL gap, Gainsight alignment | 5% |
| Mike (Speaker 4) | Senior stakeholder | Industry intelligence framing, cohort analysis concept | 5% |
| Bernard (Speaker 7) | Copilot agent builder | Demoed customer insight report | 4% |
| Gustavo (Speaker 5) | Applied AI technical | Explained agent conflict resolution logic | 3% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Ari | Visionary, receptive | Engaged -- sees CLARA as complementary, not competitive | Integration | "This whole notion of what we read and what we write is an area we could talk about" |
| Jamie | Pragmatic, cautious on scope | Stable -- offering APIs but not absorbing CLARA | Rollout | "We need to decide who's going to do that rollout" |
| Ben Brookes | Protective of CLARA ownership | Strong -- explicitly kept CLARA in insurance's domain | Positioning | "It does make sense for the insurance business to own this" |
| Mike | Impressed, wants more | Positive shift -- seeing value in integration | Demo reaction | "This is fantastic, having this all together" |
| Idrees | Collaborative, practical | Stable | Data quality | "A lot depends on who you are. You want a different view" |
| Craig | Constructive, raising gaps | Engaged -- wants CSQL functionality | Cross-sell | "One thing I noticed missing... initial identification of customer success qualified leads" |
| Matt (Speaker 9) | Uninformed, catching up | New -- wants to piggyback on rollout | Awareness | "Is there a plan already afoot that I can piggyback on?" |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Jamie | Make Sales Recon APIs/connectors available to internal agent builders | Q1 2026 | Technical feasibility | HIGH |
| Jamie | Run a February pilot including users from all CS teams | February 2026 | Users identified | HIGH |
| Richard | Consolidate CS requirements and present to Jamie's group | February 2026 | None | MEDIUM |
| Richard | Plan pilot users and rollout coordination | February-March 2026 | Jamie collaboration | MEDIUM |
| Jamie | Catalogue data input processes across CS teams | February 2026 | Team cooperation | MEDIUM |

## Meeting Effectiveness
- **Type:** Strategic alignment / cross-functional showcase
- **Overall Score:** 68
- **Decision Velocity:** 0.4
- **Action Clarity:** 0.5
- **Engagement Balance:** 0.7
- **Topic Completion:** 0.5
- **Follow Through:** 0.3

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-W4-07 | NEW | Tool proliferation -- CLARA, Sales Recon, Gainsight, Copilot agents all serving overlapping needs | HIGH | Escalating | Multiple speakers raised | HIGH |
| R-W4-08 | ONGOING | Salesforce data quality undermining all downstream tools | HIGH | Stable (known problem) | Jamie, Mike, Idrees | HIGH |
| R-W4-09 | ONGOING | Gainsight team blocking integration until March | MEDIUM | Stable | Azmain, Richard | HIGH |
| R-W4-10 | NEW | No clear owner for April UAT rollout | MEDIUM | New | Jamie flagged | MEDIUM |
| R-W4-11 | NEW | CS teams working in parallel without coordination (insurance, banking, corporate all building separately) | MEDIUM | Being addressed | Meeting purpose | HIGH |
| R-W4-12 | NEW | Double/triple data entry fatigue across CSMs -- CLARA, Salesforce, Gainsight | HIGH | Escalating | Multiple speakers | HIGH |

## Open Questions Raised
- Who owns the April UAT rollout for Sales Recon -- Conrad's sales ops team or someone else?
- How will Sales Recon handle the Salesforce-to-Gainsight migration in terms of data source switching?
- What is the right integration architecture between CLARA and Sales Recon -- API push, API pull, or bidirectional sync?
- Can Sales Recon's conversation starters and nudge-based enrichment model be adapted for CS use cases?
- How does Banking's quantitative health scoring model compare/integrate with Insurance's approach?

## Raw Quotes of Note
- "Everything we are doing is an excuse for [shared customer understanding] to happen" -- Ari, revealing the true strategic ambition behind Sales Recon
- "It does make sense for the insurance business to own this" -- Ben Brookes, asserting CLARA's independence from Sales Recon
- "We can't wait. We can't have that risk unmanaged" -- Richard, on why CLARA exists despite Gainsight being the long-term answer
- "I want us to have an understanding, a shared understanding, across the organisation of our customers" -- Ari, on the intelligence layer vision
- "Salesforce data quality has been an issue for years" -- Mike, on the elephant in the room

## Narrative Notes
This was the most strategically significant meeting of the week -- the first time Insurance's CLARA initiative was presented alongside the broader Sales Recon platform to a cross-functional audience including Banking, Corporate, Life, and Applied AI. The meeting revealed both alignment and tension: everyone agrees on the need for centralised customer intelligence, but the implementation paths are diverging across business units.

Ben Brookes's positioning of CLARA as bespoke and insurance-owned was deliberate and important. He prevented CLARA from being absorbed into Sales Recon's roadmap, preserving the team's autonomy and speed. Ari was receptive -- he sees value in the approach and is genuinely interested in API integration rather than consolidation. Jamie was more pragmatic, offering APIs but not taking on CLARA's requirements.

The elephant in the room is the tool proliferation problem: CLARA for IRP adoption, Sales Recon for sales intelligence, Gainsight for CS operations, Copilot agents for ad-hoc analysis, plus whatever Banking and Corporate are building independently. Multiple speakers circled this issue without fully confronting it. The double-entry fatigue -- CSMs being asked to input data into multiple systems -- was raised by nearly everyone and remains the most dangerous adoption risk across all initiatives. Divya's decision to expand this meeting's audience signals executive recognition that coordination is needed, but the actual coordination mechanisms remain undefined.
