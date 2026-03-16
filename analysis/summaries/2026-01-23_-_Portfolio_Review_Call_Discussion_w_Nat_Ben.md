# Portfolio Review Call Discussion with Natalia and Ben
**Date:** 2026-01-23
**Attendees:** Natalia (Plant), Ben Brookes, Azmain Hossain
**Duration context:** Medium (~30 minutes)
**Workstreams touched:** WS2 CLARA (portfolio review, Monday demo preparation)

## Key Points
- Final preparation session for Monday's portfolio review launch meeting — walked through Natalia's slide deck and agreed speaking roles
- Ben articulated the overarching narrative: 12 months of building capabilities in isolation (onboarding, adoption charters, solution blueprints, hiring), now bringing everything together with visibility so teams can "go really fast together"
- Natalia structured the meeting: 15 minutes slides, 30 minutes demo, 15-20 minutes questions — Azmain argued for allowing questions during the demo rather than holding them to the end
- Key debate on messaging to CSMs: Ben wanted a "squad-based" approach where CSMs coordinate with implementation leads, solution architects, and PMs to populate data together, rather than placing the burden solely on CSMs
- Ben pushed back against framing it as more work for CSMs: "I don't think they have many responsibilities at all" — but acknowledged the perception of overload and proposed killing them with kindness
- Critical instruction agreed: tell CSMs the golden source data is already loaded, they are not starting from scratch — they are augmenting existing data with information no system currently captures
- Azmain proposed adding an update text box within each customer page — leveraging the weekly executive summary field as a place for CSMs to record weekly status updates
- Agreed on 4-6 week pilot period before evaluating regional split
- Teams channel to be created for ongoing questions and feedback
- Azmain demonstrated the data input hub and portfolio review features live — Natalia responded with "this looks really, really good"
- Natalia identified that CSM assignments were missing from golden source at account level (only use case level) — agreed to pull CSM from use case and assign to account level as a starting assumption
- Data accuracy concern: golden source showed 90 in-flight and 61 complete, but Natalia and Ben believed these numbers were wrong — the migration deck showed 78 in-flight
- Agreed to use January golden source (one week old) rather than December version, and acknowledged data inaccuracies would need to be corrected by CSMs
- Migration-critical workflow colour coding wrong: "No" showing as red, "Yes" as green — should be blue/grey (active/inactive) to avoid confusion with RAG traffic lights

## Decisions Made
- **Squad-based data entry, not CSM-solo** (type: process, confidence: high) — CSMs take accountability but coordinate with implementation leads, SAs, PMs for input
- **Questions allowed during demo, not held to end** (type: presentation, confidence: high) — priority is engaging live audience over recording quality
- **Use weekly executive summary field for CSM updates** (type: feature, confidence: medium) — relabel as "weekly executive summary" to set expectation of regular updates
- **Pull CSM assignments from golden source use-case level** (type: data, confidence: medium) — assume use-case CSM = account CSM as starting point
- **Change migration-critical workflow colours to blue/grey** (type: design, confidence: high) — avoid confusion with RAG traffic lights
- **Use January golden source, acknowledge data inaccuracies** (type: data, confidence: high) — tell CSMs "we know it's not perfect, that's why we need your help"
- **Create Teams channel for ongoing questions** (type: process, confidence: high) — central place for feedback, not random DMs

## Action Items
| Action | Owner | Deadline | Confidence |
|--------|-------|----------|------------|
| Update golden source data to January version | Azmain Hossain | 2026-01-24 | High |
| Pull CSM from golden source use-case level and assign to accounts | Azmain Hossain | 2026-01-24 | High |
| Change migration-critical colours from red/green to blue/grey | Azmain Hossain | 2026-01-24 | High |
| Add priority account flags | Azmain Hossain | 2026-01-24 | High |
| Create Teams channel for portfolio review questions | Natalia | 2026-01-27 | High |
| Prepare Slido for meeting engagement | Natalia | 2026-01-27 | Medium |
| Reconvene at 11:30 to review portfolio review feature | All | 2026-01-23 | High |

## Theme Segments
| Timestamp Range | Theme | Speakers | Tone |
|----------------|-------|----------|------|
| 0:00-1:00 | Meeting agenda and structure | Natalia | Organized, directive |
| 1:00-3:00 | Ben's narrative for Monday: 12 months of building, now convergence | Ben | Visionary, motivational |
| 3:00-5:00 | CSM accountability framing and squad approach | Ben, Natalia | Strategic, diplomatic |
| 5:00-8:30 | Golden source data pre-loaded, messaging to CSMs | Ben, Natalia, Azmain | Collaborative, practical |
| 8:30-12:00 | Demo flow discussion: CSM view vs portfolio review | Ben, Natalia, Azmain | Planning, engaged |
| 12:00-16:30 | Live demo walkthrough, questions during demo debate | Azmain, Natalia, Ben | Energized, hands-on |
| 16:30-18:00 | Teams channel and follow-up session planning | Natalia, Azmain | Action-oriented |
| 18:00-24:00 | Tool review, CSM assignment gap, data accuracy concerns | Natalia, Ben, Azmain | Detailed, concerned |
| 24:00-30:00 | Migration-critical colour fix, golden source update | Ben, Natalia, Azmain | Technical, decisive |

## Power Dynamics
- **Natalia** drove the meeting structure with clarity, assigning speaking roles and time blocks. Her insistence on recording quality vs live engagement showed someone who thinks about multiple audiences simultaneously.
- **Ben Brookes** provided the motivational narrative layer — his pep talk about bringing teams together was polished and ready for Monday. His pushback on CSM workload perception ("I don't think they have many responsibilities at all") was bold but potentially tone-deaf.
- **Azmain Hossain** was the technical enabler, demonstrating features live and negotiating between Natalia's structure and Ben's vision. His suggestion to allow questions during the demo showed user-first thinking.

## Stakeholder Signals
- **Natalia** — Her positive reaction to the tool ("this looks really, really good") was significant — she had been the most consistently pragmatic voice about what CLARA should and should not try to do. Her concern about data accuracy was well-placed and led to the important framing decision.
- **Ben Brookes** — His squad-based approach showed he understood that CSMs would resist if they felt singled out. His frustration about the AIG meeting where 45 minutes of discussion went unrecorded revealed a pattern he was trying to break with CLARA.
- **Azmain Hossain** — His willingness to update the golden source data and pull CSM assignments before Monday showed commitment, but the cumulative task list was growing rapidly with only a weekend to deliver.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Natalia | Create Teams channel and Slido | Team | High |
| Azmain | Update golden source to January version | Ben/Natalia | High |
| Azmain | Pull CSM assignments from use-case level | Ben/Natalia | High |
| Azmain | Fix migration-critical colours | Ben | High |
| All | Reconvene at 11:30 for portfolio review walkthrough | Each other | High |

## Meeting Effectiveness
- **Clarity of outcomes:** 8/10 — Clear demo plan, speaking roles, and messaging agreed
- **Decision quality:** 8/10 — Squad-based approach and data accuracy framing were smart
- **Engagement balance:** 9/10 — All three contributed substantively from different angles
- **Time efficiency:** 7/10 — Covered significant ground but ran to the wire; Natalia had a hard stop

## Risk Signals
| Risk | Severity | Signal |
|------|----------|--------|
| Data accuracy problems visible during Monday demo | HIGH | Golden source numbers do not match migration deck (90 vs 78 in-flight). If CSMs spot discrepancies, trust in the tool could be damaged from day one. |
| CSM resistance to perceived additional workload | MEDIUM | Ben acknowledged the "overloaded" perception even while dismissing it. Messaging will need to be carefully calibrated. |
| Too many tasks for Azmain before Monday | HIGH | Golden source update, CSM assignment pull, priority flags, colour fixes, employee mapping, schema specs — all for one developer with blocked tools over a weekend. |

## Open Questions Raised
- Will the January golden source data match the migration deck numbers?
- How will CSMs who do not attend Monday's meeting be onboarded?
- Should the Teams channel be used for both questions and bug reports, or should these be separated?
- When will implementation leads and solution architects be assignable in the tool?
- How will the weekly executive summary data be used downstream?

## Raw Quotes of Note
- "Guys, you've just spent 45 minutes talking about AIG, none of this shit is written down anywhere. How does anybody know what's going on?" — Ben Brookes, on why CLARA's data capture matters
- "I don't think they have many responsibilities at all, but whatever" — Ben Brookes, on CSM workload perception
- "We've done the boring bit for you" — Ben Brookes, on the messaging about pre-loaded golden source data

## Narrative Notes
This session crystallized the Monday demo plan into a coherent story: 12 months of isolated capability building, now converging into a single system with visibility for all. Natalia's structural instincts (15-15-30 time split, recording for absentees, Slido engagement) combined with Ben's motivational narrative and Azmain's technical delivery to create a credible plan. The most important decision was the data accuracy framing — rather than trying to fix all the numbers before Monday, they would tell CSMs that the data needs their help to become accurate. This was both honest and strategic: it turned a weakness (bad data) into a call to action. Ben's AIG story — 45 minutes of unrecorded discussion that no one could reference later — was exactly the kind of concrete example that would resonate with CSMs who had experienced the same frustration. The concern was Azmain's task list: with Cursor blocked and BenVH unavailable, delivering all the changes needed for Monday while also preparing the demo itself was a significant ask for one person over a weekend.
