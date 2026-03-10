# SalesRecon Process Coordination
**Date:** 2026-02-04
**Attendees:** Richard Dosoo, Azmain Hossain, Bernard (Life team), George Dyke (mentioned)
**Duration context:** Medium (~25 minutes)
**Workstreams touched:** WS3 CS Agent

## Key Points
- Coordination session for Sales Recon UAT pilot: eight CSMs to be nominated across OUs
- Nominees identified: Julia Fuller (casualty), Bernard from Life, Kevin Pern (Hossa), Azmain from advisory side, plus solution architects
- George Dyke coordinating the overall nomination process
- Richard shared follow-up tasks from Jan 26 executive session: integration of support case monitoring, Gainsight data sharing, CS agent insights, pilot inclusion, regular check-ins, consolidation of CS requirements
- Sales Recon not yet widely available -- sales teams not using it yet either
- Need to get CS requirements documented before UAT starts, using existing agents as input
- Discussion of Salesforce data access: only 2000 rows via Power BI, field size limits, user permission controls needed
- Bernard raised authentication concern for CS agents accessing Salesforce -- machine user vs personal credentials
- Richard explained data access principle: agents must respect user-level permissions, not bypass them
- Brief discussion about reimagining the CSM role with new tooling -- Alexander wants broader thinking about what CS looks like
- Gainsight timeline concern: allegedly live end of Q1, but SRP data showing zeros due to new sales year

## Decisions Made
- **Eight CSM nominees confirmed for Sales Recon UAT across OUs** | Type: Process | Confidence: High | Owner: George coordinating
- **Richard to set up bi-weekly cadence with Sales Recon team** | Type: Process | Confidence: High | Owner: Richard
- **CS requirements to be formally documented before UAT** | Type: Governance | Confidence: Medium | Owner: Richard/Azmain

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Forward Sales Recon email to Bernard and set up next call | Richard | This week | Open | High |
| Arrange deep-dive session on CS agents with Sales Recon | Richard/Azmain | Next week | Open | Medium |
| Get UAT dates from Sales Recon team | Richard | This week | Open | Medium |
| Introduce Bernard to Natalie Clark (Gainsight) via Idris | Richard | Next week | Open | Medium |
| Set up cross-OU afternoon session on CSM role reimagining | Richard | Today | Open | High |

## Theme Segments
1. **Sales Recon UAT Nominations (0:00-5:00)** -- Identifying eight CSM nominees across OUs
2. **Executive Session Follow-Up (5:00-10:00)** -- Richard walking through action items from Jan 26
3. **Salesforce Data Access (10:00-15:00)** -- Technical constraints and authentication principles
4. **CSM Role Reimagining (15:00-23:00)** -- Alexander's broader vision discussion
5. **Gainsight Concerns (23:00-25:00)** -- Timeline and data quality issues

## Power Dynamics
- **Richard** is the programme spider -- connecting insurance, banking, life, and KYC into a coherent cross-OU narrative
- **Bernard** is thoughtful and sceptical -- asks good questions about authentication and timelines
- **Azmain** provides practical context -- his knowledge of who reports to whom and how teams are reorganised is valuable

## Stakeholder Signals
- **Bernard (Life team):** Sceptical but constructively so. Questions about Q1 delivery and authentication are legitimate. Built his own Copilot health dashboard.
- **Richard:** Building cross-OU coalition proactively -- connecting insurance, banking, KYC, and life teams through Sales Recon
- **Gainsight:** SRP data showing zeros due to new sales year -- a detail that reveals broader data governance issues. Confidence in end-of-March delivery is low.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| Richard | Forward email and set up call | Bernard | Firm |
| Richard | Get UAT dates | Team | Firm |
| Richard | Set up afternoon cross-OU session | Team | Firm |

## Meeting Effectiveness
- **Clarity of purpose:** 7/10 -- Good coordination but many threads
- **Decision quality:** 7/10 -- Nominations confirmed, process established
- **Follow-through potential:** 6/10 -- Depends on Sales Recon team responsiveness
- **Stakeholder alignment:** 7/10 -- Good within the room
- **Time efficiency:** 8/10 -- 25 minutes, efficient coverage

## Risk Signals
- **Sales Recon timeline dependency** -- End of Q1 target for UAT, but sales teams are not even using it yet. Risk of delay. Severity: MEDIUM
- **Gainsight data quality** -- SRP showing zeros is a trust issue. Severity: LOW
- **Salesforce data access constraints** -- 2000 row limit, field size limits could constrain what CS agents can do. Severity: MEDIUM

## Open Questions Raised
- When will the Sales Recon UAT actually start?
- How will data access permissions work across CS agent/Sales Recon integration?
- Is end-of-March Gainsight delivery realistic?

## Raw Quotes of Note
- "Especially that Idris showed us, it was like thousands of clients under 100k... How is an RM supposed to manage these?" -- Azmain, on the scale challenge for relationship managers

## Narrative Notes
This session is administrative but important for programme coordination. Richard is the glue connecting multiple OUs into a coherent strategy, and the Sales Recon UAT is the mechanism for doing so. The interesting subplot is the CSM role reimagining discussion -- Alexander wants to think bigger about what CS looks like with new tooling, but the practical reality (as Bernard and the team point out) is that CSM roles are highly product-specific, and the generalist vision may not map to how clients actually engage. The Gainsight timeline concern (SRP data showing zeros) is a small detail that hints at a larger problem: if the enterprise platform's data is unreliable, it strengthens the case for bespoke tools like CLARA -- but also makes the political positioning more delicate.
