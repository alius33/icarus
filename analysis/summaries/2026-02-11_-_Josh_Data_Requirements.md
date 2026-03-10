# Josh Ellingson Data Requirements Discussion
**Date:** 2026-02-11
**Attendees:** Josh Ellingson, Azmain Hossain, Richard Dosoo, Kathryn (Speaker 1)
**Duration context:** Medium (~21 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Azmain has pushed changes so everyone is now an editor — no more CSM-only restrictions. He has also pre-populated the last two weeks of transcript-sourced updates into individual customer records.
- Azmain reports findings from his session with Naveen: the status vs RAG status confusion is a universal issue. He is now focused on quality-of-life fixes rather than major functionality changes.
- Josh draws a clear and defining line: CLARA is for managing IRP migration projects, not for day-to-day CSM work management. Gainsight will handle day-to-day work. He explicitly says not to replicate Gainsight functionality.
- Azmain pushes for identifying the most pertinent data points CSMs need to update on a regular basis — a checklist approach (e.g., leave an update, check the status, do X, Y, Z) rather than trying to maintain every field.
- Kathryn raises that the data imported from Salesforce has incorrect product/software values. Use case descriptions are wrong, duplicate products exist (e.g., "treaty pricing" appears twice), and the drop-down lists need correcting. She has screenshots and detailed feedback in a shared document that Azmain has not yet reviewed.
- Josh explains the historical complexity: they previously tracked by product, then switched to use cases (Jan 2025). A single use case (e.g., portfolio management) involves multiple products (Responder, Exposure IQ, Data Bridge, Risk Modeller), each with its own adoption status. CLARA currently only shows one product per use case.
- The team agrees that multiple products per use case, each with trackable status, is required. This is a significant schema addition.
- Kathryn needs to provide Azmain with the correct product list. Azmain proposes a 1:1 recorded session with Kathryn to go through each data issue in plain language.
- Josh reports that Ben Brooks has promised Mike Steele and Colin Holmes access to CLARA, increasing visibility pressure.
- Multi-select fields needed in several places: multiple CSMs per account, multiple implementation leads, multiple solution architects. These changes are planned for the week after the Monday call.
- Azmain is building a feedback-to-GitHub pipeline: when users submit bugs or feature requests, they go directly to GitHub issues where Claude can automatically attempt fixes.

## Decisions Made
| Decision | Type | Made By | Confidence |
|----------|------|---------|------------|
| CLARA scope is IRP migrations only, not day-to-day CSM work (Gainsight territory) | Scope | Josh | High — defining declaration |
| Multi-product-per-use-case tracking with individual product status to be built | Feature | Azmain/Josh/Richard | High |
| Feature changes frozen until after Monday call for CSM stability | Stability | Azmain | High |
| Azmain and Kathryn to have regular 1:1 sessions for data alignment | Process | Azmain/Kathryn | High |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Send correct product/software list to Azmain | Kathryn | 2026-02-12 | Open | High |
| 1:1 recorded session to go through data issues | Azmain/Kathryn | 2026-02-12 | Open | High |
| Add multi-product tracking per use case | Azmain | Week of 2026-02-17 | Open | Medium |
| Add multi-select for account team roles (CSM, impl lead, SA) | Azmain | Week of 2026-02-17 | Open | Medium |
| Review Kathryn's feedback comments in shared document | Azmain | 2026-02-12 | Open | High |

## Theme Segments
| Time Range | Theme | Key Speakers |
|------------|-------|--------------|
| 0:00-3:00 | RBAC removal, pre-populated updates, quality-of-life focus | Azmain |
| 3:00-8:00 | Josh defines CLARA scope (IRP only, not Gainsight), CSM checklist approach | Josh, Azmain |
| 8:00-14:00 | Data quality issues: wrong products, duplicates, multi-product need | Kathryn, Josh, Azmain |
| 14:00-18:00 | Historical context for multi-product tracking, schema implications | Josh, Richard |
| 18:00-21:00 | Ben's executive access promises, feedback pipeline, closing | Josh, Azmain |

## Power Dynamics
- **Josh's scope declaration is the defining moment.** By saying CLARA is for IRP migrations only, he draws a boundary that protects the tool from feature creep and also protects the Gainsight team's territory. This is governance through definition.
- **Kathryn pushes harder for attention.** Her comment about having asked "so many times" signals that written feedback has been lost in the noise. The 1:1 session format is a direct response to this communication failure.
- **Josh is increasingly a partner, not a gatekeeper.** His understanding of the schema complexity ("you're seeing the complexity — that's what we built in Salesforce") shows he appreciates the technical challenge Azmain faces.
- **Ben Brooks (absent) is creating executive pressure.** Josh flags that Ben has promised Mike Steele and Colin Holmes access. This is not accusatory but the message is clear: the tool is being promoted to executives while the data is still being cleaned.

## Stakeholder Signals
- **Josh Ellingson:** Increasingly engaged and firm about scope boundaries. His declaration that CLARA is for IRP migrations only is a defining moment for the tool's identity. He is becoming more of a partner than a gatekeeper.
- **Kathryn:** Has been trying to get Azmain's attention on data issues for some time. There is a communication gap where written feedback is not getting reviewed. The 1:1 session format should help.
- **Azmain:** Open to feedback but struggling with the volume of it. His proposal for a recorded 1:1 shows he understands that written communication is not working for data alignment.
- **Ben Brooks (mentioned):** Promising executive access to CLARA without coordinating with the dev team creates pressure. The tool's audience is expanding faster than its data quality is improving.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| Kathryn | Send correct product list tomorrow | Azmain | Firm |
| Azmain | 1:1 recorded session with Kathryn | Kathryn | Firm |
| Azmain | Build multi-product tracking next week | Josh | Firm |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 5 | Josh's scope definition, multi-product agreement, 1:1 process |
| Decision quality | 5 | The scope declaration is the most important decision this week |
| Engagement balance | 4 | All four participants contributed meaningfully |
| Time efficiency | 4 | 21 minutes for significant decisions |
| Follow-through potential | 4 | Concrete actions with near-term deadlines |

## Risk Signals
- **Multi-product-per-use-case is a significant schema addition.** This will require database migration, UI changes, and re-import of data. The week-after-Monday timeline may be optimistic.
- **Ben's executive access promises.** Mike Steele and Colin Holmes looking at CLARA with unclean data is a reputational risk. Josh flags this subtly but clearly.
- **Kathryn's feedback backlog.** She has screenshots and detailed comments in a shared document that have not been reviewed. This means some of the "fixes" pushed to production may not address her actual concerns.
- **Feedback-to-GitHub pipeline is innovative but untested.** Claude auto-attempting fixes from user bug reports is ambitious. If it introduces bugs, it could erode trust faster than manual triaging.

## Open Questions Raised
- How to handle the multiple-products-per-use-case schema addition without disrupting existing data?
- How are feature requests being prioritised across quick fixes vs. discussed items?
- How to manage the growing audience (Mike Steele, Colin Holmes) while the data is still being cleaned?

## Raw Quotes of Note
- "This is not meant to manage our day to day work. This is meant to manage the project related to IRP migrations." -- Josh, defining CLARA's scope

## Narrative Notes
Josh's scope declaration is the single most important statement made during Week 6. By defining CLARA as an IRP migration tool and explicitly excluding day-to-day CSM work, he gives the programme a defensible boundary against both feature creep and Gainsight political conflict. This is the moment CLARA gets its identity. The multi-product-per-use-case discussion reveals the genuine complexity of the IRP adoption tracking domain — what looks like a simple table in Salesforce is actually a multi-dimensional matrix of products, use cases, statuses, and criticalities. Azmain is now seeing this complexity for the first time, and to his credit, he is not overwhelmed — he is asking for a 1:1 to understand it properly. The feedback-to-GitHub-to-Claude pipeline is a small innovation that deserves attention: it turns user complaints into automated fix attempts, closing the loop between feedback and action faster than any human process could.
