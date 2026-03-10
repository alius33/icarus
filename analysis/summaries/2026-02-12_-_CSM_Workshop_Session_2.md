# CSM Workshop Session 2 — CLARA Hands-On Session
**Date:** 2026-02-12
**Attendees:** George Dyke (Speaker 1), Azmain Hossain, Miles (Speaker 2/5), Asha (Speaker 3), Philip (Speaker 4), Ashley (Speaker 6), Rachel Gillespie (Speaker 7), Liz Couchman (Speaker 8), Thomas Harrison (Speaker 9)
**Duration context:** Long (~75 minutes, hands-on session)
**Workstreams touched:** WS2 CLARA

## Key Points
- Azmain joins remotely for a dedicated CLARA hands-on session with George's team. He opens with a critical trust-rebuilding commitment: any updates made from yesterday onwards will be preserved. No more data wipes. This is explicitly stated to encourage CSMs to invest time in data entry.
- Azmain flips the conversation from top-down to bottom-up: instead of asking what executives need from the data, he asks what is helpful for the CSMs who are entering it. This is a deliberate change of approach.
- Miles is used as a guinea pig to walk through the CSM workflow live. His personal dashboard shows 6 customers. The "requires attention" section highlights accounts needing updates.
- Parent/subsidiary account issue identified: Asha reports that updates to subsidiary accounts do not roll up to the parent account. The dashboard shows her as not having updated, when she has — just on the subsidiary. This is a data architecture problem affecting CSM confidence in the tool.
- Asha asks what CSMs get back from the data they put in. She wants to see how blockers are being actioned — not just report them into a void. George reinforces this by sharing an example where Liz McLagan asked for account status on specific clients and he pointed her to CLARA instead of responding manually. The decreasing frequency of manual update requests is the measure of success.
- Azmain shows the blocker analytics feature: AI analysis groups blockers across customers, identifies patterns, and suggests generic recommendations. He explains the vision for integrating Claude/OpenAI API to read customer updates over time and generate intelligent summaries for executives.
- New features shown in dev environment: multi-select for account team roles (multiple CSMs, implementation leads, solution architects per account), employee profiles showing all assignments, and the feedback-to-GitHub pipeline where Claude automatically attempts fixes on submitted bugs.
- Asha asks about blocker standardisation — different CSMs describe the same issue differently. Azmain confirms a standard blocker taxonomy is being developed (with Steve Gentilly and Catherine Pavlovich) that will become a selectable list rather than free text.
- Internal vs external blocker distinction explained: internal = something Moody's can fix; external = on the client's side or a partner's side (e.g., Imaginera).
- Implementation lead and project management views requested as dashboard filters alongside the existing CSM view.
- Philip notes that the feedback workflow going straight to GitHub and being auto-triaged by Claude is impressive — 7 issues already auto-fixed, 10 attempted, 8 in human review.
- Discussion about Gainsight timeline: Philip expresses scepticism about how much of the Gainsight rollout will actually be delivered for insurance/RMS data, especially given Salesforce integration complexity.

## Decisions Made
- Data preservation commitment: no more bulk updates that wipe CSM-entered data -> Azmain
- Bottom-up approach adopted: ask CSMs what they need, not just what executives want reported -> Azmain/George
- Blocker taxonomy to be standardised as selectable list -> Steve Gentilly/Catherine/Azmain
- Implementation lead and PM dashboard views to be added -> Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Fix parent/subsidiary rollup issue for dashboard metrics | Azmain | TBD | Open |
| Schedule 1:1 sessions with each CSM to review their accounts | Azmain / Natalia's team | TBD | Open |
| Develop standard blocker taxonomy as selectable list | Steve Gentilly / Catherine / Azmain | TBD | Open |
| Add implementation lead and PM views to dashboard | Azmain | TBD | Open |
| Integrate Claude/OpenAI API for intelligent summaries and executive Q&A | Azmain | TBD | Open |

## Stakeholder Signals
- Azmain's data preservation commitment is a pivotal moment. CSMs had been burned before — entering data only to have it wiped by subsequent deployments. This explicit promise is an attempt to rebuild trust.
- Asha is the voice of CSM frustration: she wants reciprocity from the tool. If she puts data in, she wants to see it being used to help her, not just to serve management reporting.
- George continues to champion the tool by modelling behaviour — pointing Liz McLagan to CLARA rather than answering manual requests.
- Philip's scepticism about Gainsight delivery for RMS is a through-line concern: if Gainsight does not materialise for insurance, CLARA becomes even more critical.
- The feedback-to-GitHub-to-Claude pipeline is a genuine innovation that impressed the room. This is the kind of rapid iteration that builds credibility.

## Open Questions Raised
- How to solve the parent/subsidiary data rollup problem architecturally?
- When will the Claude/OpenAI API integration be live for intelligent blocker analysis and executive Q&A?
- What is the realistic Gainsight timeline for insurance/RMS data?
- How to measure the impact of CLARA on reducing manual update requests?

## Raw Quotes of Note
- "Any updates you make from yesterday onwards will be preserved. We're no longer going to do any big update to wipe things." -- Azmain, the trust-rebuilding commitment
