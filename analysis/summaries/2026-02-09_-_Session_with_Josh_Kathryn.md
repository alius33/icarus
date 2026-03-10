# Session with Josh and Kathryn — Data Review & CLARA Walkthrough
**Date:** 2026-02-09
**Attendees:** Richard Dosoo, Azmain Hossain, Josh Ellingson (Diya), Kathryn (Speaker 3)
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
- Remove CSM-only edit restriction — anyone can update any record, with audit trail tracking who made changes -> Azmain
- App data sourced from Salesforce only; golden source delta needs to be identified and filled in manually -> Kathryn/Azmain
- Thursday meeting to establish decision-making process and scope for CLARA -> Natalia to convene

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Fix action plan linkage display issue | Azmain/Richard | Before 3pm call | Open |
| Remove CSM-only editing restriction | Azmain | 2026-02-09 | Open |
| Provide delta of golden source data missing from CLARA | Kathryn | TBD | Open |
| Verify priority/accelerated adoption/Cat Accelerate tags are correctly applied | Azmain | Before portfolio review | Open |
| Thursday meeting on CLARA scope and decision process | Natalia | 2026-02-13 | Open |

## Stakeholder Signals
- Josh is cautious but constructive. He raised the question of who the decision maker is — a sign he wants clearer governance, not just ad hoc feedback loops.
- Kathryn is frustrated that features she had in Salesforce are being rebuilt from scratch in CLARA, but she explicitly does not want to recreate Salesforce. She recognises the tool needs to be different but is struggling with the data gaps.
- Josh publicly acknowledged the pressure Azmain faces from multiple stakeholders — a significant gesture of empathy and alignment.
- Azmain is transparent about the limits of his knowledge of the data model and openly asks stakeholders to guide him rather than expecting him to intuit business context.

## Open Questions Raised
- What does "high risk" mean as a field now that it is separated from Cat Accelerate?
- What account-level data from the golden source needs to be brought into CLARA?
- Who is the single decision maker for CLARA feature scope?

## Raw Quotes of Note
- "I recognise the pressure you're under. I recognise you have multiple voices coming into this, and it's hard for you to prioritise. I want that publicly stated." -- Josh, on Azmain's situation
