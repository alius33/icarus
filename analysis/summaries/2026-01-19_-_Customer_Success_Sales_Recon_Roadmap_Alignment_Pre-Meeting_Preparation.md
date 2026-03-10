# Customer Success Sales Recon Roadmap Alignment — Pre-Meeting Preparation
**Date:** 2026-01-19
**Attendees:** Richard Dosoo, Jamie (Sales Recon lead), Idris (Banking CS), Conrad (Banking CS), Azmain Hossain, Kiara (Sales Recon team)
**Duration context:** Medium (~33 minutes)
**Workstreams touched:** WS2 CLARA, WS3 CS Agent, WS5 Sales Recon Convergence

## Key Points
- This was the final prep call before the Monday executive meeting with Colin, Ari, Mike, and other senior stakeholders
- Jamie shared Sales Recon's Q1 roadmap: Account Intelligence and Retention & Growth features are on the near-term horizon
- Intelligence Anywhere — a feature to surface Sales Recon data into Copilot via API — is on the Q1 roadmap, which could retire significant manual data pipeline work the team has been doing
- Jamie confirmed that each company analysis costs approximately $3 in OpenAI spend, which scales quickly across thousands of accounts
- Idris confirmed a monthly cross-OU standing meeting already exists (Diya from insurance, Rupert/Craig from Corp Gov, Matt Seymour from Asset Management, Dave Hickey from Christina's team, Mena/Irena from Banking)
- The team agreed to focus the Monday meeting on alignment and confidence-building rather than detailed requirements prioritization
- Richard flagged that CLARA was built out of necessity because Salesforce and Gainsight couldn't accommodate their short-term needs
- Idris built a banking CS agent in Copilot Studio that connects to AR data and provides spend/fund scoring without hallucination — offered to demo this Monday
- Jamie cautioned that Sales Recon cannot solve every problem and some functionality may belong in Gainsight or Salesforce

## Decisions Made
- **Remove the priorities/out-of-scope slide from Monday presentation** (type: strategic, confidence: high) — Jamie argued it was premature to discuss prioritization before completing the February pilot
- **Target a February pilot for CS team access to Sales Recon** (type: strategic, confidence: medium) — Jamie wants a small group of CS people to evaluate current capabilities and identify gaps
- **Requirements sharing to happen via a separate thread, not in the Monday meeting** (type: process, confidence: high) — Richard will share collated requirements with Jamie and Kiara for asynchronous review
- **30-day milestone: establish regular requirements check-in cadence** (type: governance, confidence: medium) — exact format TBD
- **60-day milestone: influence the Sales Recon roadmap with CS requirements** (type: strategic, confidence: medium) — aimed at monthly drops starting from March
- **90-day milestone: first round of rollout/testing** (type: strategic, confidence: low) — Conrad to coordinate with Jamie

## Action Items
| Action | Owner | Deadline | Confidence |
|--------|-------|----------|------------|
| Share existing requirements documentation with Jamie and Kiara | Richard Dosoo | 2026-01-20 | High |
| Grant edit access to presentation slides for all attendees | Richard Dosoo | 2026-01-19 | High |
| Iterate on slides and send updated version for feedback | Richard Dosoo | 2026-01-20 | High |
| Add Jamie's slides to the shared deck | Jamie | 2026-01-20 | High |
| Brief Diya on her speaking role for Monday | Richard Dosoo | 2026-01-20 | Medium |
| Follow up with Idris on banking requirements crossover vs divergence | Richard Dosoo | Next week | Medium |
| Email office manager (Joe) with guest access details for Monday's meeting | Richard Dosoo | 2026-01-20 | High |
| Demo banking CS agent (Copilot Studio) at Monday meeting | Idris | 2026-01-27 | High |

## Theme Segments
| Timestamp Range | Theme | Speakers | Tone |
|----------------|-------|----------|------|
| 0:00-3:30 | Slide logistics and access issues | Richard, Jamie, Idris | Administrative, casual |
| 3:30-7:00 | Meeting structure and storyboard | Richard, Jamie | Strategic, collaborative |
| 7:00-10:00 | Sales Recon capabilities and Q1 roadmap | Jamie | Informative, guarded |
| 10:00-16:00 | Cross-OU alignment and where CLARA fits | Richard, Idris, Jamie | Political, exploratory |
| 16:00-22:00 | Tactical CLARA work vs Sales Recon long-term | Richard, Jamie | Honest, slightly defensive |
| 22:00-28:00 | Cost model discussion and pilot planning | Jamie, Idris | Practical, forward-looking |
| 28:00-33:00 | Milestones and wrap-up | Richard, Jamie | Action-oriented |

## Power Dynamics
- **Jamie** controlled the narrative around Sales Recon scope and capabilities. Politely but firmly pushed back on premature prioritization discussions. Positioned Sales Recon as the long-term platform while acknowledging it cannot solve everything.
- **Richard** was deferential to Jamie while trying to ensure insurance CS requirements get adequate airtime. Navigated carefully between pushing for visibility and respecting Jamie's roadmap ownership.
- **Idris** brought a pragmatic cross-OU perspective. His awareness of the monthly standing meeting and his direct experience building a CS agent in Copilot Studio gave him credibility in the room.
- **Azmain** was largely silent, observing the political dynamics and noting points for follow-up.

## Stakeholder Signals
- **Jamie** — Protective of Sales Recon's roadmap but genuinely open to input. Her caution about prioritization suggests she is managing internal pressure from multiple OUs and does not want to over-commit. The February pilot is her controlled mechanism for managing expectations.
- **Idris** — Proactive and technically capable. His Copilot Studio agent demo could be a catalyst for showing what is possible with Sales Recon data. He raised the important point about being mindful of other OUs beyond insurance and banking.
- **Richard** — Slightly anxious about ensuring CLARA's needs are heard before Sales Recon's roadmap crystallizes. His repeated mentions of sharing requirements suggest he has a backlog of asks that have not yet been formally channeled.
- **Conrad** — Present but silent. Mentioned as the execution coordinator for the 90-day milestone.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Jamie | Kick off February pilot with small CS group | Richard/Idris | Medium |
| Jamie | Monthly feature drops starting March | All OUs | Medium |
| Richard | Share existing requirements with Jamie and Kiara | Jamie | High |
| Idris | Demo banking CS agent at Monday meeting | All | High |
| Richard | Brief Diya ahead of Monday | Diya | Medium |
| Richard | Email office manager for guest access | Jamie/Idris | High |

## Meeting Effectiveness
- **Clarity of outcomes:** 7/10 — Good alignment on what NOT to include Monday; milestones set but loosely defined
- **Decision quality:** 7/10 — Smart decision to focus Monday on alignment rather than detail; pilot approach is sound
- **Engagement balance:** 6/10 — Jamie and Richard drove most of the conversation; Idris contributed well; Azmain and Conrad were mostly silent
- **Time efficiency:** 7/10 — Ran slightly over but covered necessary ground

## Risk Signals
| Risk | Severity | Signal |
|------|----------|--------|
| Requirements never formally making it to Sales Recon roadmap | HIGH | Jamie said to share requirements asynchronously but no formal intake process exists. Risk of requirements being acknowledged but not acted upon. |
| February pilot timeline slipping | MEDIUM | No specific dates or participants named. Jamie hedged with language about understanding costs and details. |
| CLARA becoming permanent rather than transitional | MEDIUM | Jamie explicitly noted that some functionality may not belong in Sales Recon. If CLARA fills gaps that Sales Recon deprioritizes, it becomes a permanent parallel system. |
| OpenAI cost scaling concerns | MEDIUM | At $3 per company analysis, costs across 3000+ banking accounts alone would be significant. No clear budget allocation model yet. |
| Cross-OU politics delaying CS-specific features | MEDIUM | Multiple OUs competing for Sales Recon roadmap influence through the monthly standing meeting. Insurance CS needs could get diluted. |

## Open Questions Raised
- Where does CLARA functionality ultimately belong — Sales Recon, Gainsight, or standalone?
- How will the February pilot participants be selected?
- What is the formal intake process for getting CS requirements onto the Sales Recon roadmap?
- Who pays for the OpenAI costs when usage scales across OUs?
- Can Intelligence Anywhere's API access replace the manual data pipeline work the insurance team has been doing?

## Raw Quotes of Note
- "Sales recon can become anything we want it to be, because ultimately we're in charge, but we can't solve every problem there is in the organisation. Otherwise we'll never finish anything." — Jamie, setting realistic expectations
- "Moody's is paying quite a bit of money for Gainsight today... we have to be mindful of that as we think through it" — Idris, flagging the change management complexity

## Narrative Notes
This call surfaced the central strategic tension in the programme: CLARA was born out of necessity because neither Salesforce nor Gainsight could accommodate the insurance CS team's tracking needs, but Sales Recon is the anointed long-term platform. Jamie was diplomatically firm about not rushing prioritization, which is smart governance but leaves the insurance team in limbo — they have a working tool that needs ongoing investment, and the promise of Sales Recon absorption remains vague. The February pilot is the critical gating event: if it reveals that Sales Recon already covers many of CLARA's needs, the convergence path becomes clearer. If it exposes major gaps, the team faces a difficult investment decision. Idris emerged as a potentially important ally — his banking CS agent demonstrates what is possible with Sales Recon's data layer, and his practical awareness of cross-OU dynamics could help navigate the political landscape. Richard's anxiety about ensuring requirements are heard is well-founded; the history of enterprise platform teams deprioritizing individual OU needs in favour of common-denominator features is a real risk here.
