# Blockers with Peter Kimes — User Voice Integration Requirements
**Date:** 2026-02-26
**Attendees:** Azmain Hossain, Peter Kimes, Stacy (Dixstra), Kevin (Chernelle)
**Duration context:** Short (~21 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Peter Kimes presents detailed requirements for User Voice integration into CLARA's blocker tracking, coming from a pre-meeting with Stacy, Kevin, and Chernelle.
- The core ask: CSMs need to track whether blockers are also tracked in User Voice (the product feedback/feature request system), and have visibility into JIRA IDs and case URLs associated with blockers -- parity with what existed in Salesforce.
- Key distinction drawn: not all User Voice items are blockers (most are nice-to-haves), but when something IS a blocker AND is in User Voice, that connection needs to be visible in CLARA.
- Stacy holds the line on scope: do NOT import all User Voice data into CLARA. That would create duplicate data, administrative burden, and the same deduplication problems that already plague blocker entries. Just add URL/link fields to the blocker form.
- Kevin explains User Voice data complexity: feedback is merged across customers, which means AI analysis could hallucinate and attribute one customer's feedback to another.
- Pragmatic MVP agreed: add three fields to CLARA's blocker form -- User Voice URL, JIRA ID, and Case URL. No data import, no API integration. Just links.
- Azmain commits to overnight delivery: fields will be in production by tomorrow morning for Peter to test.
- Previous blocker categories (software vs model) will NOT be reverted to from the current product/client/enablement split -- there was a reason for the change.
- Peter volunteers to be the guinea pig for testing the new fields.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Add User Voice URL, JIRA ID, and Case URL fields to blocker form | Feature scope | High | Azmain |
| Do NOT import User Voice data wholesale into CLARA | Scope boundary | High | Stacy / Peter |
| Do NOT revert blocker categories from product/client/enablement back to software/model | Scope boundary | High | Peter / Azmain |
| User Voice remains the system of record for feature requests | Architecture | High | Kevin / Stacy |
| Start with MVP fields, revisit in 1-3 months for deeper integration | Phased approach | High | All |

## Action Items
| Action | Owner | Deadline | Confidence | Status |
|--------|-------|----------|------------|--------|
| Add User Voice URL, JIRA ID, and Case URL fields to blocker form | Azmain | Tomorrow morning | High | Open |
| Test new fields once deployed | Peter Kimes | Tomorrow | High | Open |
| Announce new fields at Monday portfolio call to CSMs | Peter / Stacy | Monday | High | Open |
| Continue discussions on deeper User Voice integration with Kevin and Chernelle | Peter / Stacy | 1-3 months | Medium | Open |

## Theme Segments
1. **Requirements overview** (0:00-3:00) -- Peter outlines the Salesforce-to-CLARA gap and the pre-meeting context
2. **Data architecture debate** (3:00-11:00) -- Import vs link, duplicate data risks, User Voice complexity, Kevin's API/merger warnings
3. **Stacy's scope discipline** (11:00-14:00) -- Holding the line on not adding administrative burden to CSMs
4. **MVP agreement and implementation** (14:00-21:00) -- Three fields, overnight delivery, testing plan

## Power Dynamics
- **Peter Kimes is well-prepared and pragmatic.** He came with screenshots, a pre-meeting brief, and a clear articulation of the gap. He is a constructive voice.
- **Stacy is the scope guardian.** She repeatedly pulls the conversation back from "import everything" to "add what we need." Her concern about CSM administrative burden is well-grounded.
- **Kevin provides the technical reality check** about User Voice data complexity and merged feedback risks.
- **Azmain is the responsive builder.** Commits to overnight delivery without hesitation. His MVP instinct is strong.

## Stakeholder Signals
- **Peter Kimes:** Emerged as a pragmatic, well-prepared stakeholder. Sent pre-meeting documentation with screenshots comparing Salesforce to CLARA. Willing to be guinea pig. Constructive voice.
- **Stacy Dixstra:** Consistently the voice of scope discipline. Pushed back on importing User Voice data. Insisted on keeping CSM burden low. Worried about running fast and stepping back.
- **Kevin (Chernelle):** Technical contributor. Raised valid concern about User Voice data merger causing hallucination risk for AI analysis. Confirmed APIs exist but cautioned about data complexity.
- **Azmain Hossain:** Responsive and solution-oriented. Commits to overnight delivery. Recognises the existing blocker form was auto-generated from Salesforce data without User Voice context.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Azmain | Add three fields to blocker form by tomorrow morning | Peter | High |
| Peter | Test new fields once deployed | Azmain | High |
| Peter / Stacy | Announce new fields at Monday CSM call | CSMs | High |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of purpose | 5 | Very clear requirements session with prepared materials |
| Decision quality | 5 | Pragmatic MVP with explicit scope boundaries |
| Engagement | 4 | All four participants contributing meaningfully |
| Follow-through setup | 5 | Clear deliverables, testing plan, and announcement strategy |
| Time efficiency | 5 | 21 minutes, all essential, no waste |

## Risk Signals
- **Blocker deduplication problem persists.** Multiple blockers across multiple customers use different verbiage for the same underlying issue. Stacy flagged this explicitly. No solution yet.
- **User Voice data merger means AI analysis could hallucinate.** Kevin's warning about merged feedback across customers is a real risk for any future automated analysis.
- **CSM administrative burden is a constant tension.** Every new field, every new tracking requirement risks CSMs feeling like CLARA adds work rather than removing it.

## Open Questions Raised
- Should User Voice entries eventually become a separate object in CLARA?
- How to reconcile blockers across customers (deduplication)?
- When a product release closes a blocker, how to automatically close all associated blockers in CLARA?
- What frequency should User Voice data be refreshed if integrated?

## Raw Quotes of Note
- "I just want to be really careful with the extra work that could come on to all CSMs" -- Stacy, holding the scope line
- "I can get this added in tomorrow, so that on Monday's call, you know, it's already in production" -- Azmain, on overnight delivery commitment

## Narrative Notes
This is the best-run meeting of the week. Peter came prepared, Stacy provided scope discipline, Kevin offered technical reality checks, and Azmain committed to fast delivery. The MVP decision is exactly right: add link fields now, defer deeper integration until the team has bandwidth and the data quality issues are resolved. Stacy's insistence on not adding administrative burden to CSMs reflects hard-won understanding of adoption dynamics -- every extra field is potential resistance. Peter's emergence as a constructive, well-prepared stakeholder is a positive signal for the programme.
