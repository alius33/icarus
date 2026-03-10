# Sales Recon Pilot Kickoff — CS Team
**Date:** 2026-02-11
**Attendees:** Cara (Speaker 2), Idrees, Bernard (Speaker 4), Peter Kimes, and approximately 5 other CSM participants
**Duration context:** Medium (~32 minutes)
**Workstreams touched:** WS3 CS Agent (Sales Recon convergence)

## Key Points
- Cara launches the two-week Sales Recon zero pilot for the Customer Success team. Sales Recon zero is the internal version (Moody's is "customer zero"); a potential external version is out of scope for this pilot.
- Testing period: 11-24 February 2026. Post-pilot interviews will follow, potentially spilling into early March.
- Eight CSMs across the organisation are included. Most already have Salesforce access to Sales Recon. This is production, not a sandbox — all data entered is real and persistent.
- Three CS-relevant features to focus on during the pilot: (1) Account Intelligence — shared knowledge base sourced from Salesforce, Orbis, web research, and user interactions; (2) Meeting Preparation Agent — interactive agent to help prepare for client meetings with agenda, talking points, cheat sheets; (3) Share Knowledge Agent — upload meeting notes, updates, and documents to hydrate the account intelligence.
- Two additional features exist but are more sales-oriented: Account Planning (sales ops templates) and Lead Generation (pitch/conversation starters). CSMs can explore these but the focus is on the three CS-relevant features.
- A feedback tracker platform has been built specifically for the pilot. CSMs submit feedback (bugs, feature requests, positive experiences) to the CSM-specific area within the tracker.
- Known limitations: parent/subsidiary account analysis is limited to the specific Salesforce account selected (subsidiaries do not roll up to parents and vice versa). This is a frequent feedback item already being worked on. Product list is partial, so "active products" tab and total value figures are incomplete.
- Output is currently text/markdown only. HTML and PowerPoint export planned for mid-April release.
- Bernard asks about timeline — when will the first CS-specific version ship? Cara clarifies this beta is already the first released version in production; the pilot feedback will shape the roadmap for CS-specific enhancements.
- Peter Kimes asks about prompt libraries — none exist yet, but it is something that could be developed from the pilot findings.
- CSMs ask about parent/subsidiary rollup: selecting a subsidiary only analyses that subsidiary; selecting a parent does not discover subsidiary products. This is an account-level limitation inherited from Salesforce's data structure.

## Decisions Made
| Decision | Type | Made By | Confidence |
|----------|------|---------|------------|
| Pilot runs 11-24 Feb with 8 CSMs, using production environment | Process | Cara | High |
| CSMs should focus on 2-5 well-known accounts | Scope | Cara | High |
| Feedback goes to dedicated tracker platform (CSM-specific area) | Process | Cara | High |
| Do not use "create opportunity" or "schedule meeting" buttons (these write back to Salesforce) | Safety | Cara | High |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Test access to Sales Recon in Salesforce | All pilot CSMs | 2026-02-13 | Open | High |
| Follow 2-5 well-known accounts and test features | All pilot CSMs | 2026-02-24 | Open | Medium |
| Submit feedback via feedback tracker platform | All pilot CSMs | Ongoing | Open | Medium |
| Schedule post-pilot 1:1 interviews with each CSM | Cara | Late Feb / early Mar | Open | High |
| Explore prompt library creation based on pilot findings | Cara / Peter Kimes | Post-pilot | Open | Low |

## Theme Segments
| Time Range | Theme | Key Speakers |
|------------|-------|--------------|
| 0:00-8:00 | Pilot overview: objectives, timeline, feedback process | Cara |
| 8:00-14:00 | Five features overview, CS-relevant focus areas | Cara, Bernard |
| 14:00-22:00 | Live demo: following accounts, running analysis, meeting prep | Cara |
| 22:00-28:00 | Share knowledge agent, Q&A on parent/subsidiary, output formats | Cara, Peter Kimes, Bernard |
| 28:00-32:00 | Feedback tracker, prompt libraries, closing | Cara, Peter Kimes |

## Power Dynamics
- **Cara owns the room.** She is structured, clear, and prepared. The session runs like a product launch — objectives, caveats, demo, Q&A. She has thought through the pilot design.
- **Idrees plays the framing role.** He provides context for why the pilot matters and how it feeds into the broader roadmap. His interventions are brief but add strategic clarity.
- **Bernard probes on timelines.** His question about when the first CS version ships signals either impatience or scepticism. Cara's answer (this is already the first version) may not fully address his concern.
- **Peter Kimes thinks about knowledge management.** His prompt library question is consistent with his broader interest in structured knowledge systems (User Voice, documentation).

## Stakeholder Signals
- **Cara:** Competent and organised. She has built a feedback tracker, designed a phased pilot process, and prepared a clear demo. She manages expectations about limitations (parent/subsidiary, product list, output formats) proactively.
- **Bernard (Life team):** Probing on timelines — his question about when the first CS version ships reveals impatience or scepticism about delivery cadence.
- **Idrees:** Provides critical context framing. The pilot feeds into Anna's team (on Jamie's roadmap) who are already building CS-specific features in a sandbox.
- **Peter Kimes:** Thinking about knowledge management (prompt libraries) — consistent with his broader User Voice integration interests. He is a systems thinker, not just a feature requester.
- **CSM participants:** The parent/subsidiary question comes from multiple participants, suggesting this is a universal pain point in the CSM workflow.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| All pilot CSMs | Test access and use 2-5 accounts over two weeks | Cara | Medium |
| Cara | Schedule post-pilot 1:1 interviews | CSMs | Firm |
| Cara | Investigate prompt library development | Peter Kimes | Soft |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 5 | Objectives, timeline, focus areas all crystal clear |
| Decision quality | 4 | Well-structured pilot with appropriate constraints |
| Engagement balance | 3 | Mostly a presentation; Q&A was limited |
| Time efficiency | 4 | 32 minutes, well-paced |
| Follow-through potential | 3 | Depends on CSMs actually using Sales Recon over two weeks |

## Risk Signals
- **Parent/subsidiary limitation could undermine pilot credibility.** If CSMs cannot see the full picture of their accounts because Salesforce structures them as separate entities, the intelligence will feel incomplete and untrustworthy.
- **Pilot is production, not sandbox.** Data entered is real and persistent. If CSMs accidentally hit "create opportunity" or "schedule meeting," it writes back to Salesforce. This is a real risk for unfamiliar users.
- **Low engagement risk.** Eight CSMs were selected but the level of active testing over two weeks will vary. Without check-ins during the pilot period, some CSMs may not use it at all.
- **Gainsight data absence is a known gap.** The CS-relevant value of Sales Recon depends on health scores and risk drivers from Gainsight, which are not yet integrated. The pilot may underwhelm because the data foundation is incomplete.

## Open Questions Raised
- When will Gainsight data (health scores, risk drivers) be integrated into Sales Recon's account intelligence?
- Will parent/subsidiary account rollup be addressed in the next release cycle?
- Should CSMs avoid the "create opportunity" and "schedule meeting" buttons that write back to Salesforce?

## Raw Quotes of Note
- "Please do not make up examples or information, because it's going to be part of the actual knowledge." -- Cara, warning that this is a production environment

## Narrative Notes
This is the most polished session of the week — a proper product pilot kickoff with clear objectives, structured phases, and a purpose-built feedback mechanism. Cara runs it like she has done this before. The contrast with CLARA's organic, fire-fighting development process is stark. Sales Recon is a professionally managed product with a roadmap; CLARA is a grassroots tool being built in real-time by a stretched programme manager. The parent/subsidiary limitation is the most significant technical gap raised, because it mirrors the same problem in CLARA — the Salesforce data model does not capture the complexity of how CSMs think about their accounts. The pilot's success will depend on whether CSMs can get meaningful intelligence from accounts they already know well. If the intelligence is generic or wrong, the tool loses credibility regardless of how well it is presented.
