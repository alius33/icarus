# IRP Adoption Call -- Portfolio Review Kickoff with CSM Team
**Date:** 2026-01-26
**Attendees:** Natalia (Plant), Ben Brooks, Azmain Hossain, Josh Ellingson, George Dyke, Stacey, Catherine, CSMs (Watson, Christine, others referenced), implementation leads
**Duration context:** Long (~60+ minutes, structured presentation with demo)
**Workstreams touched:** WS2 CLARA (launch/adoption), WS1 Data Quality (golden source), WS6 Governance (portfolio review process)

## Key Points
- This was the formal introduction of CLARA to the broader CSM team -- Natalia framed it as the new portfolio review mechanism, with Ben Brooks providing strategic context about the 12-month adoption acceleration journey
- Ben Brooks positioned CLARA as the next evolution after onboarding improvements, training, solution fit/blueprints, and adoption charters -- now the focus is on operational tracking and accountability
- The meeting established the weekly Monday portfolio review process: CSMs will use CLARA to track account health, blockers, action plans, and use case progress
- Natalia explicitly asked CSMs to start entering data, framing it as a transition from the golden source spreadsheet to CLARA
- Josh Ellingson's resistance surfaced again -- he questioned whether CSMs should use the tracker or Salesforce, leading Ben Brooks to become visibly frustrated
- Ben Brooks declared the golden source data cutoff: end of day Wednesday (Jan 28), with a fresh Salesforce extract loaded, followed by Thursday build/release, Friday for implementation leads to populate additional data, and Monday (Feb 2) as the first live portfolio review
- Key features prioritised for the week: role-based access control (RBAC), audit trail (field-level), data completeness, and employee/account team import
- Azmain proposed splitting work with Martin Davies: Azmain focuses on data and audit trail, Martin on RBAC with BenVH backend support
- The team discussed the tension between launching with imperfect data versus waiting for perfection -- Ben Brooks strongly favoured ripping the band-aid off
- Catherine Papavich's manual golden source enrichment process was explicitly identified as unsustainable -- the tracker is designed to replace her role as the human data-cleansing bottleneck
- Partner management functionality was acknowledged as a future need but explicitly deprioritised for this week
- LLM/AI features discussed: natural language querying, transcript-based gap analysis (compare what CSMs say in calls vs what they enter in the system), AI-assisted blocker descriptions, charter SWOT analysis
- AWS Bedrock Opus 4.5 access discovered -- Gustavo sent Richard instructions for getting API key from corporate AWS environment, potentially eliminating need for Max5 subscriptions
- Diya Sawhny spoke to position CLARA as critical to the insurance scorecard and Andy Frappe's visibility requirements

## Decisions Made
- End of day Wednesday (Jan 28): Salesforce golden source data cutoff
  - **Type:** explicit
  - **Confidence:** HIGH
- Thursday (Jan 29): build and release to production
  - **Type:** explicit
  - **Confidence:** HIGH
- Friday (Jan 30): implementation leads can start populating additional data
  - **Type:** explicit
  - **Confidence:** HIGH
- Monday (Feb 2): first live portfolio review using CLARA
  - **Type:** explicit
  - **Confidence:** HIGH
- RBAC must be in place before broader rollout
  - **Type:** explicit
  - **Confidence:** HIGH
- Audit trail: basic version (record-level) for launch, field-level granularity to follow
  - **Type:** explicit
  - **Confidence:** HIGH
- Partner functionality deferred to week after next (earliest)
  - **Type:** explicit
  - **Confidence:** HIGH
- Work split: Azmain on data + audit trail, Martin on RBAC
  - **Type:** explicit
  - **Confidence:** MEDIUM
- Pursue AWS Bedrock Opus 4.5 API key via Gustavo's instructions
  - **Type:** explicit
  - **Confidence:** HIGH
- Data entry approach: start with existing Salesforce extract, CSMs augment and correct in real-time rather than waiting for clean data
  - **Type:** explicit
  - **Confidence:** HIGH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Load fresh golden source data from Salesforce extract | Azmain + Catherine | Wed Jan 28 EOD | Open | HIGH |
| Implement role-based access control (RBAC) | Martin + BenVH (backend) | Thu Jan 29 | Open | MEDIUM |
| Implement basic audit trail (record-level, then field-level) | Azmain | Thu Jan 29 | Open | MEDIUM |
| Implement weekly update feature with text entry | Azmain | Thu Jan 29 | Open | MEDIUM |
| Snapshot dev database and migrate to production | BenVH | Thu Jan 29 night | Open | HIGH |
| Chase Catherine, Natalia, Stacey for latest data | Azmain | Tue-Wed | Open | HIGH |
| Get AWS Bedrock Opus 4.5 API key | Richard | Mon Jan 27 | Open | MEDIUM |
| CSMs to register in the tool and begin updating their accounts | All CSMs | Fri Jan 30 | Open | MEDIUM |
| Prepare first live Portfolio Review using CLARA | Natalia | Mon Feb 2 | Open | HIGH |
| Ping Josh, George, Natalia, Stacey, Catherine about Monday readiness | Ben Brooks | This week | Open | HIGH |
| Post in Teams channel: end of day Wed is data cutoff | Ben Brooks | Mon-Tue | Open | HIGH |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| 12-month adoption acceleration context | Strategic/History | "We've been really focused on how do we try and accelerate the adoption process" -- Ben Brooks | HIGH |
| Weekly portfolio review process design | Governance/Process | "We just need to take out the excuses for not doing it" -- Ben Brooks | HIGH |
| Data quality vs launch timing | Strategy/Adoption | "I would launch the thing empty... start over" -- Ben Brooks | HIGH |
| RBAC and admin controls | Feature/Technical | "We must have the restrictions on edits and read only version for others" -- Ben Brooks | HIGH |
| Transcript-based gap analysis vision | AI/Innovation | "We pass that through an LLM, and then we do a gap analysis" -- Azmain | MEDIUM |
| Catherine's manual enrichment as bottleneck | Process/People | "It's ridiculous that someone has to go do that manually" -- Azmain | HIGH |
| AWS Bedrock API access | Infrastructure | "We can get a key for Opus from our AWS deployed environment" -- Richard | HIGH |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Natalia | Meeting host, process owner | Opened session, framed portfolio review purpose, structured agenda | 15% |
| Ben Brooks | Strategic driver, decision-maker | Set deadlines, overrode objections, pushed launch timeline, narrated demo | 30% |
| Azmain Hossain | Builder, demo presenter | Showed tracker, flagged data gaps, suggested AI features | 20% |
| Diya Sawhny | Executive sponsor | Positioned CLARA as critical to scorecard, encouraged CSM adoption | 5% |
| Josh Ellingson | Resistance voice | Questioned tracker vs Salesforce usage | 5% |
| Richard Dosoo | Supporting context | Mediated, referenced data sources | 10% |
| CSMs (Watson, Christine, others) | Audience, feedback providers | Watson raised double-entry concern, Christine raised blocker definition | 10% |
| Stacey, Catherine | Data owners | Referenced as key contacts for golden source | 5% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Ben Brooks | Impatient, forceful | Escalating frustration with resistance | Launch timeline | "Tell me what you think if he says one more time, please don't use this tracker. I'm going to fly over there and punch it" (about Josh) |
| Natalia | Structured, process-focused | Positive -- building sustainable cadence | Portfolio review | "What we want to talk today? Why this meeting?" |
| Diya Sawhny | Engaged, supportive | Active -- encouraging CSM adoption | Scorecard alignment | "There is both an expectation, but if I were you, I would really think about leaning in" |
| Azmain | Energised, practical | Positive -- clear on deliverables | Feature planning | "If we keep it simple... we just take the Word document, we just build those exact same fields" |
| Josh Ellingson | Cautious, resistant | Ongoing -- still questioning tracker adoption | CLARA vs Salesforce | "Should we use Salesforce, or should we use the tracker?" |
| Watson (referenced) | Resistant | Negative -- complaining about double entry | Charters | Ben noted Watson "whinging about double entry on charters" |
| Catherine | Key dependency | Stable -- her manual process is being replaced | Data enrichment | Referenced by Azmain as manual bottleneck |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Ben Brooks | Post in Teams channel about data cutoff timeline | This week | None | HIGH |
| Ben Brooks | Ping Josh, George, Natalia, Stacey, Catherine about readiness | This week | None | HIGH |
| Azmain | Chase data owners for golden source refresh | Tue-Wed | None | HIGH |
| Azmain | Build audit trail and update features | By Thursday | Martin handles RBAC | HIGH |
| BenVH | Snapshot and migrate database to prod | Thursday night | Data ready | HIGH |
| Richard | Pursue AWS Bedrock API key | Monday | Gustavo's instructions work | MEDIUM |
| Natalia | Run first portfolio review on Monday Feb 2 | Mon Feb 2 | Tool and data ready | HIGH |

## Meeting Effectiveness
- **Type:** Product launch / process kickoff
- **Overall Score:** 75
- **Decision Velocity:** 0.9
- **Action Clarity:** 0.7
- **Engagement Balance:** 0.5
- **Topic Completion:** 0.7
- **Follow Through:** 0.5

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-W4-13 | NEW | Aggressive timeline (Wed data cutoff, Thu build, Mon launch) with thin margin for error | HIGH | New | Ben Brooks's deadline | HIGH |
| R-W4-14 | ONGOING | Josh Ellingson actively questioning whether to use CLARA or Salesforce | HIGH | Stable/escalating | Ben Brooks's frustration | HIGH |
| R-W4-15 | NEW | Watson as bellwether user complaining about double entry -- adoption risk indicator | MEDIUM | New signal | Ben Brooks reference | HIGH |
| R-W4-16 | NEW | Martin's capacity split between Canopies and CLARA RBAC work | MEDIUM | New | Martin flagged | MEDIUM |
| R-W4-17 | ONGOING | Technical debt accumulating (audit trail, field-level granularity deferred) | MEDIUM | Escalating | Richard acknowledged | HIGH |
| R-W4-18 | NEW | Data quality of golden source extract may be poor -- "clean data is probably shit anyway" | HIGH | Known | Ben Brooks | HIGH |
| R-W4-19 | NEW | Josh told CSMs to "edit and play around" with data that won't be retained -- potential data mess | MEDIUM | New | Azmain raised | HIGH |

## Open Questions Raised
- Can AWS Bedrock Opus 4.5 access actually replace Max5 subscriptions?
- Will the golden source extract from Salesforce be usable or will it need significant manual cleanup?
- How will field-level audit trail be architected to avoid performance overhead?
- What happens if RBAC is not ready by Thursday -- does launch slip?
- Will Martin have enough bandwidth to deliver RBAC while managing Canopies work?
- How to handle double entry between Salesforce and CLARA during the transition period?
- What happens when CSMs find data errors -- process for flagging and correcting not yet defined?

## Raw Quotes of Note
- "For fuck sake, it's never going to get final if you don't rip the band aid off and start" -- Ben Brooks, on data perfection paralysis
- "Tell me what you think if he says one more time, please don't use this tracker. I'm going to fly over there and punch it" -- Ben Brooks, on Josh's resistance
- "There is both an expectation, but if I were you, I would really think about leaning in and being excited" -- Diya Sawhny, encouraging CSM adoption
- "It's ridiculous that someone has to go do that manually" -- Azmain, on Catherine's golden source enrichment process
- "I would launch the thing empty, and I would say, start over" -- Ben Brooks, on his preferred approach to data quality

## Narrative Notes
This was the most consequential meeting of the week for CLARA's trajectory. Ben Brooks is operating with the urgency of someone who knows the window for adoption is narrow -- if CSMs do not start using the tracker now, the institutional resistance (personified by Josh and Watson) will calcify into permanent rejection. His aggressive timeline (Wednesday cutoff, Thursday build, Friday data entry, Monday live review) is a forcing function designed to prevent the perfect-being-the-enemy-of-good cycle.

The tension between Ben Brooks and Josh Ellingson is the most important interpersonal dynamic in the programme right now. Ben's frustration is visceral -- his language about Josh is unfiltered and escalating. Josh's objection (use Salesforce vs the tracker) represents a legitimate concern about double entry, but Ben sees it as institutional inertia that will kill the project if indulged. This conflict will likely come to a head in the Monday portfolio review.

Diya Sawhny's active participation -- encouraging CSMs to lean in and linking CLARA to the insurance scorecard -- adds executive weight to the launch. Natalia's structured approach to the portfolio review process provides the governance scaffolding that could make this sustainable beyond the initial push. But the fundamental risk remains: if the data is visibly poor on Monday, or if RBAC is not in place, the sceptics (Josh, Watson) will have ammunition to argue for going back to spreadsheets. The team is racing against the clock and against institutional resistance simultaneously.
