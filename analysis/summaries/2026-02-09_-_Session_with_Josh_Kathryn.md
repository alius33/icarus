# Session with Josh and Kathryn — Data Review & CLARA Walkthrough
**Date:** 2026-02-09
**Attendees:** Richard Dosoo, Azmain Hossain, Josh Ellingson, Kathryn (Speaker 3)
**Duration context:** Medium (~29 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Action plans have been pushed to production and linked to the correct customers. Azmain walks Josh and Kathryn through the updated app.
- Kathryn's computer was upgraded, causing her to lose the CLARA link — a minor but symbolic sign of how fragile access continuity is.
- Blockers and action plans: the action plan linkage appears broken on the front end (action plans display as unlinked even though they are linked in the backend). Azmain identifies this as a quick fix.
- RBAC restriction raised: only the assigned CSM (e.g., Naveen) can edit a customer record. Josh firmly objects to this — anyone should be able to update records so managers or colleagues can cover during absences. The audit trail captures who made changes. Azmain agrees to remove the CSM-only restriction.
- Confusion over field definitions: "high risk" vs "Cat Accelerate" vs "priority" fields are unclear. Natalia previously said high risk should not equal Cat Accelerate, so a separate field was added. Nobody is clear on what "high risk" now means.
- The golden source data was not used — CLARA pulls only from Salesforce. Kathryn and Josh flag that account-level data from the golden source (e.g., risk link/risk browser on/off tags) is missing. Azmain requests a Delta: what is in the golden source that is not in the app.
- Natalia sent the list of 31 priority 2026 migration clients and 17 accelerated adoption clients. These are being tagged in the app.
- Josh frames the need for the tool to be easier than Salesforce for data entry. He publicly acknowledges the pressure Azmain is under with multiple voices providing conflicting requirements.
- Josh suggests a Thursday meeting (set up by Natalia) to discuss the decision process — what should and shouldn't be in the app, how to avoid giving Azmain contradictory feedback.
- Azmain proposes a layered approach: CSM perspective workshop (morning, George's team), then Josh/Kathryn-level perspective, then Natalia/Ben Brooks executive perspective.

## Decisions Made
| Decision | Type | Made By | Confidence |
|----------|------|---------|------------|
| Remove CSM-only edit restriction — anyone can update any record, with audit trail | Access Control | Josh, Azmain agreed | High |
| App data sourced from Salesforce only; golden source delta needs manual fill | Data Strategy | Azmain, Josh/Kathryn accepted | High |
| Thursday meeting to establish decision-making process and scope | Governance | Natalia to convene | Medium |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Fix action plan linkage display issue | Azmain/Richard | Before 3pm call | Open | High |
| Remove CSM-only editing restriction | Azmain | 2026-02-09 | Open | High |
| Provide delta of golden source data missing from CLARA | Kathryn | TBD | Open | Medium |
| Verify priority/accelerated adoption/Cat Accelerate tags are correctly applied | Azmain | Before portfolio review | Open | High |
| Thursday meeting on CLARA scope and decision process | Natalia | 2026-02-13 | Open | Medium |

## Theme Segments
| Time Range | Theme | Key Speakers |
|------------|-------|--------------|
| 0:00-6:00 | Action plans demo, blocker linkage issues | Azmain, Kathryn, Richard |
| 6:00-11:00 | RBAC restriction debate, field confusion (high risk vs Cat Accelerate) | Josh, Azmain |
| 11:00-18:00 | Golden source vs Salesforce data gap, priority client tagging | Kathryn, Josh, Azmain |
| 18:00-25:00 | Data entry process, decision-making governance, workshop proposal | Josh, Azmain |
| 25:00-29:00 | PM coverage gap for 30 priority clients, closing | Josh, Azmain |

## Power Dynamics
- **Josh shifts from gatekeeper to governance advocate.** His question "who is the decision maker?" signals he wants clearer authority structures, not just ad hoc feedback. This is a constructive move.
- **Kathryn is the frustrated domain expert.** She has deep knowledge of the data model and has been trying to communicate it but feels unheard. The suggestion to use a Word doc rather than the data model shows she understands that technical artifacts will not work for data alignment.
- **Azmain is transparent about his limitations.** He openly admits he does not understand some field definitions (high risk, in-scope date) and asks stakeholders to guide him. This vulnerability builds trust but also reveals the burden of building a tool without sufficient domain context.
- **Josh's public acknowledgment of Azmain's pressure** is a significant power dynamic shift — it establishes empathy and reduces the adversarial tone that has characterised some previous interactions.

## Stakeholder Signals
- **Josh Ellingson:** Cautious but constructive. He raised the question of who the decision maker is — a sign he wants clearer governance, not just ad hoc feedback loops. His public acknowledgment of Azmain's pressure is a significant gesture of empathy.
- **Kathryn:** Frustrated that features she had in Salesforce are being rebuilt from scratch in CLARA, but she explicitly does not want to recreate Salesforce. She recognises the tool needs to be different but is struggling with the data gaps. She wants a more involved working relationship with Azmain.
- **Azmain:** Transparent about the limits of his knowledge of the data model and openly asks stakeholders to guide him rather than expecting him to intuit business context. The layered approach proposal (CSM -> management -> executive) shows growing programme management sophistication.
- **Richard:** Relatively quiet in this session, playing facilitator rather than directing. He jumps in on technical questions (schema changes) but lets the Josh-Kathryn-Azmain dynamic play out.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| Azmain | Remove CSM-only edit restriction today | Josh | Firm |
| Azmain | Fix action plan linkage display before 3pm | Richard | Firm |
| Kathryn | Provide golden source delta | Azmain | Soft — no deadline set |
| Natalia (absent) | Convene Thursday decision-making meeting | Team | Medium — second-hand commitment |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 4 | RBAC decision clear, delta process defined |
| Decision quality | 4 | Removing CSM restriction was the right call |
| Engagement balance | 4 | Josh, Kathryn, and Azmain all contributed substantively |
| Time efficiency | 3 | Some repetition of known issues |
| Follow-through potential | 3 | Depends on Kathryn delivering the delta and Thursday meeting happening |

## Risk Signals
- **Field confusion is a governance failure, not a technical one.** The "high risk" field exists because nobody defined it before it was built. This pattern — build first, define later — recurs across the programme.
- **Golden source data gap is structural.** The golden source is too messy to import programmatically (Catherine uses manual X's, O's, and formulas inconsistently in the same column). This means account-level data will need to be manually reconciled, which is a significant labour overhead.
- **Multiple voices, no single decision maker.** Josh raises this explicitly. Until a governance structure is in place, Azmain will continue receiving conflicting requirements.

## Open Questions Raised
- What does "high risk" mean as a field now that it is separated from Cat Accelerate?
- What account-level data from the golden source needs to be brought into CLARA?
- Who is the single decision maker for CLARA feature scope?

## Raw Quotes of Note
- "I recognise the pressure you're under. I recognise you have multiple voices coming into this, and it's hard for you to prioritise. I want that publicly stated." -- Josh, on Azmain's situation

## Narrative Notes
This session marks a tonal shift in the Josh-Azmain relationship. Previous interactions had an adversarial edge — Josh as sceptical gatekeeper, Azmain as defensive builder. Here, Josh publicly validates Azmain's difficulty and asks constructive questions about governance. Kathryn's frustration is real but directed at the situation, not at Azmain personally. Her comment about "recreating things we've lost" captures the emotional cost of the Salesforce-to-CLARA transition: the old tool may have been clunky, but it held institutional knowledge that is now being rebuilt from scratch. The layered workshop proposal (CSM -> management -> executive) is Azmain's most sophisticated programme management idea yet — it shows he is learning to manage stakeholders, not just build features.
