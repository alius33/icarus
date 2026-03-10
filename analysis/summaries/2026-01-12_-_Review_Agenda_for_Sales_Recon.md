# Review Agenda for Sales Recon Executive Meeting
**Date:** 2026-01-12
**Attendees:** Richard Dosoo, Azmain Hossain, Jamie Stark (Sales Recon lead), Idris (Banking CS), Chiara, Conrad
**Duration context:** medium (~3500 words)
**Workstreams touched:** WS4 (Sales Recon Convergence), WS1 (Programme Governance), WS2 (CLARA)

## Key Points
- Pre-meeting to align agenda for the January 26 executive meeting with Mike Steele, Colin Holmes, Diya Sawhny, and Ari la Harvey
- Richard introduces Azmain to the Sales Recon team for the first time -- positioning him as both programme manager and active builder
- Diya wants the messaging clear: this is not a new initiative, but continuation of work started in June workshops in New York
- Jamie confirms Sales Recon is nearly ready for production release (end of this week) and plans to give CS people access for a pilot
- Jamie plans monthly feature drops aligned with business ops processes
- Idris (banking) has been working with copilot studio and Salesforce -- building an orchestrator agent with sub-agents (health scores, annual spend, Sales Recon queries) pushed into Teams via AD permissioning
- Key data quality issue flagged by Idris: Salesforce account rollup from child to parent causing hallucinations in AI outputs; Databricks ARR data feed may have fixed this
- Jamie proposes copilot agents accessible through Teams that link to Sales Recon content
- Meeting agenda for Jan 26 structured: (1) Jamie on Sales Recon update/roadmap, (2) Richard/Azmain on CS problem statement and 5 workstreams, (3) Idris on banking/insurance convergence, (4) Diya closes with priority decisions, (5) Richard on 90-day plan

## Decisions Made
- **Meeting structure for Jan 26**: Five-section agenda agreed -> Richard to coordinate
  - **Type:** explicit
  - **Confidence:** HIGH
- **CS pilot on Sales Recon**: Jamie to give handful of CS people access to live production environment -> Jamie
  - **Type:** explicit
  - **Confidence:** HIGH
- **No separate test environment for CS**: Sales Recon will build and test in live production, not separate pilot -> Jamie
  - **Type:** explicit
  - **Confidence:** HIGH
- **Consolidated insurance/banking requirements**: Present unified requirement to Sales Recon -> Richard/Idris
  - **Type:** explicit
  - **Confidence:** HIGH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Share storyboard slides with Jamie/Conrad/Chiara | Richard/Azmain | 2026-01-17 | Open | HIGH |
| Set up virtual review meeting for next week | Richard | 2026-01-17 | Open | HIGH |
| In-person meeting at Canary Wharf (Thursday) with Conrad/Chiara | Richard/Azmain | 2026-01-16 | Open | MEDIUM |
| Share prompt library with Jamie's team | Richard/Idris | 2026-01-17 | Open | MEDIUM |
| Provide list of CS users wanting Sales Recon access | Richard/Azmain | 2026-01-20 | Open | HIGH |
| Get Diya's support for CS pilot users to prioritise testing | Richard | 2026-01-20 | Open | MEDIUM |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Sales Recon CS pilot plan | strategic | "we'll just start slowly adding more and more features" -- Jamie | HIGH |
| Meeting positioning as continuation | governance | "this isn't a new initiative" -- Jamie relaying Diya's directive | HIGH |
| Account data quality causing AI hallucinations | technical | "the AI hallucinates and doesn't understand how the accounts roll up" -- Idris | HIGH |
| Copilot-to-Teams integration path | technical | "pre configured copilot agents that people can access through teams" -- Jamie | MEDIUM |
| Customer artefact ingestion | strategic | "a whole world of artefacts that we engage... from the customers" -- Richard | MEDIUM |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Richard Dosoo | Meeting organiser, bridge between CS and Sales Recon | Setting agenda, making introductions, proposing collaboration | 40% |
| Jamie Stark | Sales Recon authority, roadmap owner | Defining pace, managing expectations, offering integration paths | 30% |
| Idris | Banking CS representative | Raising data quality concerns, sharing copilot studio progress | 15% |
| Azmain Hossain | Programme manager (mostly listening) | Brief introduction, minimal speaking in external-facing meeting | 5% |
| Conrad | Sales Recon technical | Confirming data feed accuracy | 5% |
| Chiara | New addition (Jamie suggested inclusion) | Silent observer | 5% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Jamie Stark | Cooperative, measured | Positive | CS collaboration | Open to early CS access, monthly feature drops |
| Idris | Engaged, proactive | Stable | Banking requirements | Already prototyping with copilot studio |
| Diya (referenced) | Directive | Stable | Meeting messaging | Wants continuity narrative, not "new initiative" framing |
| Mike Steele (referenced) | Supportive | Positive | Sales Recon value | Gave positive feedback after using Sales Recon with General Ali CEO |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Jamie | Will give CS people access to Sales Recon live environment | End of Jan | Production release this week | HIGH |
| Jamie | Will add slides to the shared deck | Before Jan 26 | "slide light" contribution | HIGH |
| Richard | Will share slides by end of week | 2026-01-17 | Content from all parties | MEDIUM |
| Conrad | Will double-check Databricks ARR data accuracy | This week | Call with James | HIGH |

## Meeting Effectiveness
- **Type:** Cross-functional coordination / agenda alignment
- **Overall Score:** 78
- **Decision Velocity:** 0.7
- **Action Clarity:** 0.7
- **Engagement Balance:** 0.5
- **Topic Completion:** 0.8
- **Follow Through:** 0.6

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-015 | New | Salesforce account hierarchy causes AI hallucinations in Sales Recon | MEDIUM | Improving | Technical | HIGH |
| R-016 | New | Diya may attend Jan 26 in person -- raises stakes for presentation quality | LOW | Stable | Governance | MEDIUM |

## Open Questions Raised
- Has the Databricks ARR data feed fully resolved the account rollup/hallucination problem?
- When will Sales Recon's Gainsight integration be built? (Jamie says "this quarter")
- Will CS pilot require IDAM onboarding through business ops? (Jamie flagged process requirement)
- How quickly can Sales Recon add CS-specific features after pilot feedback?

## Raw Quotes of Note
- "this isn't a new initiative. This is something we started off... June" -- Jamie, relaying Diya's framing directive
- "the AI hallucinates and doesn't understand how the accounts roll up from child to parents" -- Idris, on data quality risk
- "we plan to drop features monthly" -- Jamie, on Sales Recon iteration cadence
- "if we can get the people to say, look, Andy Frappe is going to be going to speak to a client, and is going to be using the content here, you got to make sure your content is up to date" -- Jamie, on carrot-and-stick data quality incentive

## Narrative Notes
This is the first substantive coordination meeting between the insurance CS team and the Sales Recon platform team. Jamie Stark comes across as measured and willing to collaborate, but careful about pace -- monthly feature drops through business ops processes suggest bureaucratic constraints that could slow CS-specific features. The most significant revelation is Idris's copilot studio work in banking: an orchestrator agent architecture with sub-agents pushed into Teams via AD permissioning represents a more sophisticated technical approach than the insurance team's current Cursor-based prototyping. The meeting establishes the political framing for January 26 -- Diya wants continuity, not novelty, and Mike Steele's positive Sales Recon experience provides an executive champion. The data quality flag from Idris about account hierarchy hallucinations is a warning that needs addressing before any executive demo.
