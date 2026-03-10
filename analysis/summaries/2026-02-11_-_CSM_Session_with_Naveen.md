# CSM Session with Naveen — Individual Onboarding
**Date:** 2026-02-11
**Attendees:** Azmain Hossain, Naveen (Speaker 1)
**Duration context:** Short (~12 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Naveen is a CSM based in Little Rock, Arkansas. He is the only CSM who proactively reached out to have a one-on-one CLARA onboarding session — Azmain notes this with appreciation.
- Naveen's Salesforce name has three components but Salesforce only has two fields, causing a mismatch when data was pulled into CLARA. Naveen needs to reassign himself to his correct employee profile for each of his customers.
- When Naveen attempts to reassign himself, the system throws a "failed to assign CSM" error. Azmain discovers the employee profile is not linked to the customer. Naveen will send his customer list and Azmain will assign them manually.
- Azmain has pre-populated the last two weeks of portfolio review call updates into individual customer records from the meeting transcripts. The "executive summary" holds the first week's overview; subsequent updates are added as timestamped entries.
- Naveen tries editing a use case (portfolio management for Chubb) — changes health status to red and marks it "at risk." He identifies that the status field and RAG status field are confusingly redundant. Azmain acknowledges this is a recurring question but says senior stakeholders requested both fields.
- Naveen asks about "scope and criticality" fields (risk link critical, risk browser critical, in scope, in scope date). Azmain is transparent that Ben Brooks requested these but he does not fully understand the rationale. Suggests Naveen raise the question in the Monday meeting.
- Naveen commits to spending a couple of hours going through all his accounts to update data, then reporting back any issues or questions.
- Azmain commits to freezing changes after today — no more updates until after the Monday call, to give CSMs stability for data entry.

## Decisions Made
- No more CLARA changes until after the Monday portfolio review call, to provide stability for CSM data entry -> Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Send customer list to Azmain for manual assignment | Naveen | 2026-02-11 | Open |
| Go through all accounts and update data | Naveen | This week | Open |
| Raise "in scope" and scope/criticality questions at Monday meeting | Naveen | 2026-02-16 | Open |

## Stakeholder Signals
- Naveen is the most proactive CSM so far — the only one to request a 1:1 session. He spent time on a Sunday two weeks prior trying to get data ready. This is notable engagement from the field.
- Azmain is visibly grateful for any CSM who shows initiative. The contrast between Naveen's willingness and the broader resistance from others is a recurring theme.
- The status vs RAG status confusion is surfacing with every CSM who engages with the tool, suggesting a design decision that needs resolution.

## Open Questions Raised
- Why are there both a "status" and a "RAG status" field? What is the difference?
- What does "in scope" mean for a use case, and what is "in scope date"?
- Why does the CSM assignment fail for some employee profiles?

## Raw Quotes of Note
- "You're actually the only person that reached out and actually showed interest in having a session." -- Azmain, to Naveen
