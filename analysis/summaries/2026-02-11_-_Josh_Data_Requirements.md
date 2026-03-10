# Josh Ellingson Data Requirements Discussion
**Date:** 2026-02-11
**Attendees:** Josh Ellingson, Azmain Hossain, Richard Dosoo, Kathryn (Speaker 1)
**Duration context:** Medium (~21 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Azmain has pushed changes so everyone is now an editor — no more CSM-only restrictions. He has also pre-populated the last two weeks of transcript-sourced updates into individual customer records.
- Azmain reports findings from his session with Naveen: the status vs RAG status confusion is a universal issue. He is now focused on quality-of-life fixes rather than major functionality changes.
- Josh draws a clear line: CLARA is for managing IRP migration projects, not for day-to-day CSM work management. Gainsight will handle day-to-day work. He explicitly says not to replicate Gainsight functionality.
- Azmain pushes for identifying the most pertinent data points CSMs need to update on a regular basis — a checklist approach (e.g., leave an update, check the status, do X, Y, Z) rather than trying to maintain every field.
- Kathryn raises that the data imported from Salesforce has incorrect product/software values. Use case descriptions are wrong, duplicate products exist (e.g., "treaty pricing" appears twice), and the drop-down lists need correcting. She has screenshots and detailed feedback in a shared document that Azmain has not yet reviewed.
- Josh explains the historical complexity: they previously tracked by product, then switched to use cases (Jan 2025). A single use case (e.g., portfolio management) involves multiple products (Responder, Exposure IQ, Data Bridge, Risk Modeller), each with its own adoption status. CLARA currently only shows one product per use case.
- The team agrees that multiple products per use case, each with trackable status, is required. This is a significant schema addition.
- Kathryn needs to provide Azmain with the correct product list. Azmain proposes a 1:1 recorded session with Kathryn to go through each data issue in plain language.
- Josh reports that Ben Brooks has promised Mike Steele and Colin Holmes access to CLARA, increasing visibility pressure.
- Multi-select fields needed in several places: multiple CSMs per account, multiple implementation leads, multiple solution architects. These changes are planned for the week after the Monday call.
- Azmain is building a feedback-to-GitHub pipeline: when users submit bugs or feature requests, they go directly to GitHub issues where Claude can automatically attempt fixes.

## Decisions Made
- CLARA scope is IRP migrations only, not day-to-day CSM work (that is Gainsight's domain) -> Josh
- Multi-product-per-use-case tracking with individual product status to be built -> Azmain/Richard
- Feature changes frozen until after Monday call to give CSMs stability for data entry -> Azmain
- Azmain and Kathryn to have regular 1:1 sessions to work through data issues -> Azmain/Kathryn

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Send correct product/software list to Azmain | Kathryn | 2026-02-12 | Open |
| 1:1 recorded session to go through data issues | Azmain/Kathryn | 2026-02-12 | Open |
| Add multi-product tracking per use case | Azmain | Week of 2026-02-17 | Open |
| Add multi-select for account team roles (CSM, impl lead, SA) | Azmain | Week of 2026-02-17 | Open |
| Review Kathryn's feedback comments in shared document | Azmain | 2026-02-12 | Open |

## Stakeholder Signals
- Josh is increasingly engaged but firm about scope boundaries. His declaration that CLARA is for IRP migrations only, not Gainsight territory, is a defining moment for the tool's identity.
- Kathryn has been trying to get Azmain's attention on data issues for some time ("that's why I asked so many times"). There is a communication gap where written feedback is not getting reviewed. The 1:1 session format should help.
- Josh acknowledges the complexity Azmain is facing — "you're seeing the complexity" — and is becoming more of a partner than a gatekeeper.
- Ben Brooks promising executive access to CLARA (Mike Steele, Colin Holmes) without coordinating with the dev team creates pressure. Josh flags this without accusation but the implication is clear: the tool is being promoted faster than it is ready.

## Open Questions Raised
- How to handle the multiple-products-per-use-case schema addition without disrupting existing data?
- How are feature requests being prioritised across quick fixes vs. discussed items?
- How to manage the growing audience (Mike Steele, Colin Holmes) while the data is still being cleaned?

## Raw Quotes of Note
- "This is not meant to manage our day to day work. This is meant to manage the project related to IRP migrations." -- Josh, defining CLARA's scope
