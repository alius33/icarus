# Demo and Feedback from Josh E
**Date:** 2026-01-16
**Attendees:** Josh Ellingson, Azmain Hossain, Ben Brooks
**Duration context:** Medium (~26 minutes)
**Workstreams touched:** WS2 (CLARA)

## Key Points
- Critical stakeholder engagement. Josh Ellingson's core concern is data interpretation accuracy -- he does not want Andy Frappe seeing incorrectly interpreted data that then becomes an immovable belief. He is explicitly supportive of the tool's direction but cautious about release timing.
- Josh frames his concern carefully: the display is great, but the underlying data interpretation matters more. If a data point is displayed incorrectly, it leads to incorrect conclusions. He does not expect Azmain to understand what the data represents -- that requires CSM domain knowledge.
- Josh is bullish on the tool's potential: he sees it as a way to stop doing data entry in Salesforce (a "big win for everybody"), to quickly capture new types of information that leadership requests, and to enable squad-based collaboration across CSMs, implementation leads, and partners.
- Josh and Ben have "slight disagreements" on release timing. Josh wants more CSM review before release; Ben wants to move faster. Ben frames it as data visibility (not data quality) and argues that a humming system will make Gainsight integration arguments moot.
- Azmain proposes replacing the AI chatbot with a feedback button that captures screenshots of what the user is looking at, so feedback is contextual and visual. Josh likes this.
- Josh suggests a CSM-wide demo session before opening for feedback -- people need to see the tool in action before they can give useful feedback, otherwise they will ask basic questions or not engage.
- Josh proposes champions: 2-3 CSMs per region who collate feedback from peers and bring it back to the team. Ben refines this: champions collect and triage, while the tool still gets released broadly. This avoids slowing things down while ensuring quality feedback.
- Gainsight conflict raised: banking CSM goals include Gainsight activity metrics. Josh is concerned that if CSMs are measured on Gainsight usage but entering data in CLARA, there is a conflict. Ben dismisses this ("nobody's going to give a fuck about Gainsight if we've got 50 migrations done"), but Josh notes the consequences of losing that argument fall on CSMs, not Ben.
- Azmain explains the Gainsight API situation: security breach investigation is ongoing, API access blocked until cleared. Estimated timeline not clear.
- Josh gives data quality specifics: 40% of accounts in the database have Salesforce IDs (the rest were not mapped during the manual import). Account naming inconsistencies are a known problem (Hartford vs The Hartford vs Hartford Insurance).
- Josh raises a strategic scope question: which use cases go in CLARA vs Gainsight for post-migration/evergreen adoption tracking? No answer yet, but important for avoiding dual entry.
- Ben's key reframe: this is about data visibility, not data quality. The messaging to CSMs should be about collaboration and cross-functional visibility, not about fixing bad data.

## Decisions Made
- Replace AI chatbot with a feedback button that captures screenshots -> Azmain
- Hold a CSM-wide demo session before opening for feedback -> Josh/Azmain/Richard
- Appoint 2-3 CSM champions per region for feedback collation -> Josh/Ben
- Frame messaging as "data visibility" not "data quality" -> Ben Brooks
- Schedule demo with Natalia's portfolio review team early next week, then broader CSM demo Wednesday/Thursday -> Azmain/Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Replace AI chatbot with feedback button (screenshot capture) | Azmain | Before CSM demo | Open |
| Schedule CSM-wide demo session (with recording) | Azmain/Richard/Natalia | Next week | Open |
| Identify 2-3 CSM champions per region | Josh | After demo session | Open |
| Schedule demo for portfolio review team (Natalia) | Azmain/Richard | Early next week | Open |
| Resolve Gainsight vs CLARA scope question for post-migration tracking | Josh/Ben | TBD | Open |
| Complete Salesforce ID mapping for remaining 60% of accounts | TBD | TBD | Open |

## Stakeholder Signals
- Josh is the gatekeeper for CSM adoption. He is supportive but will not let the tool go live until he is confident the data will not be misinterpreted. His concern is specifically about Andy Frappe: one wrong data point shown to the president could permanently damage credibility.
- Josh is coming around -- he sees real value in the tool and is providing substantive, constructive feedback. His engagement level has increased.
- Ben and Josh have a productive tension: Ben pushes speed, Josh gates for quality. Both are right in their own domain. Ben's reframe to "data visibility" is a smart move to align them.
- Josh is worried about the Gainsight metrics conflict -- CSMs will be caught between two systems if not handled carefully.
- Azmain handles the meeting well -- he does not oversell, acknowledges the data gaps honestly, and proposes practical solutions (feedback button, phased rollout).

## Open Questions Raised
- At what point do CSMs stop entering data in Salesforce and start entering in CLARA? This is the critical cutoff that has not been defined.
- How to handle the Gainsight activity metrics vs CLARA data entry conflict for CSM goals?
- Which use cases are migration-specific (CLARA) vs evergreen (Gainsight)?
- When will the Gainsight API security investigation be completed?

## Raw Quotes of Note
- "I don't want Andy Frappe seeing one piece of data that's interpreted incorrectly and we can't get them off of it" -- Josh Ellingson, his defining concern about the tracker
