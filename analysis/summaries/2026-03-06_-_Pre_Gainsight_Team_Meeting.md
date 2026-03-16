# Pre Gainsight Team Meeting
**Date:** 2026-03-06
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (Speaker 1), Chris M, Catherine (Kathryn)
**Duration context:** Medium (~23 minutes)
**Workstreams touched:** WS2 CLARA, WS3 CS Agent, App Factory / Infrastructure, Gainsight integration (new)

## Key Points
- Kathryn Palkovics set up a call with the Gainsight team for next Thursday. This pre-meeting was to align goals and prepare. The Gainsight team now understands that people will build their own tools to fill gaps, and they want to explore what integration with CLARA and other apps would look like.
- Gainsight team stakeholders identified: Nadim (works with Kathryn Palkovics on what should be built in Gainsight), Tina Palumbo (executive view on overall Gainsight strategy at Moody's), Rajesh (technical contact for data integration). Kathryn Palkovics is the insurance business-side advisor to this team.
- The key question for the Thursday meeting: does integration make sense? If so, what pieces? The goal is not to pull CLARA into Gainsight or vice versa, but to identify what CSMs need at their fingertips without duplicating work.
- Richard requested that the Thursday meeting also cover Salesforce programmatic access, since multiple projects need it (Bernard's customer sentiment from tickets, Courtney's HD models, Kevin Pern's CS Agent requirements). Kathryn Palkovics confirmed the business systems team now understands they need to "play nice with these apps."
- Gainsight integration was NOT in the 12-week resource plan created two weeks ago. If integration is expected, replanning is required. This is a scope expansion that the team is managing carefully.
- Account planning governance example: George is building an account planning app, Idris from banking is building one too. Richard cannot tell senior CSMs to stop innovating because it might overlap with the Gainsight roadmap. Kathryn Palkovics clarified she is not saying "do not build" -- she is saying "if it exists, how do we make sure it integrates so we are not creating silos."
- Kathryn Palkovics offered to serve as the gating checkpoint for whether an idea should be built as a custom app or already exists in enterprise tooling. She wants to help create a decision tree for the App Factory intake process. Her exact words: "you're speaking my love language."
- Azmain made a candid and strategically important statement: the team is exhausted, the fast pace is leading to things being done too quickly and incorrectly, and Gainsight governance provides a legitimate reason to slow down. He described this explicitly as a welcome development.
- Integration architecture approach: Azmain stated that CLARA will adapt its architecture to fit Gainsight, not the reverse. CLARA's IRP data is a small subset of overall customer health, which is Gainsight's purview.
- BenVH confirmed App Factory was designed with integration flexibility from the start. He wants to minimise data stored on their end. He echoed the governance need -- he is seeing people independently wanting the same things.
- Richard will send App Factory slides and CLARA documentation to the Gainsight team before Thursday so they come prepared with questions.
- Chris's next project after CLARA bugs: Richard flagged that Salesforce integration will be Chris and Nikhil's next assignment.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Thursday Gainsight meeting to also cover Salesforce programmatic access | Scope | High | Kathryn Palkovics to set expectation |
| Send App Factory and CLARA documentation as pre-reading | Process | High | Richard |
| CLARA architecture will adapt to Gainsight, not the reverse | Architecture | High | Azmain |
| Kathryn Palkovics to help design governance/decision tree for App Factory intake | Governance | High | Kathryn Palkovics/Richard |
| Chris and Nikhil's next assignment is Salesforce integration | Resource | High | Richard |
| Pace of programme to be deliberately slowed for governance | Strategic | High | Team consensus |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Send App Factory slides and CLARA documentation to Gainsight team | Richard | Before Thursday | Open | High |
| Set expectation with Gainsight team to include Salesforce in Thursday agenda | Kathryn Palkovics | Before Thursday | Open | High |
| Compile Salesforce requirements from Bernard, Courtney, and Kevin Pern | Richard | Before Thursday | Open | High |
| Get Bernard's detailed Salesforce requirements | Richard | Monday | Open | High |
| Forward Thursday meeting invite to Chris | Richard | ASAP | Open | High |
| Prepare CLARA-as-complementary-to-Gainsight positioning for Thursday | Azmain | Before Thursday | Open | Medium |
| Provide visibility into Gainsight roadmap for the team | Kathryn Palkovics | Ongoing | Open | Medium |

## Theme Segments
1. **Meeting purpose and Gainsight stakeholder mapping** (0:00-4:00) -- Kathryn Palkovics explains the Thursday call; identifies Nadim, Tina Palumbo, Rajesh
2. **Resource planning and scope acknowledgement** (4:00-6:00) -- Not in 12-week plan; replanning needed if integration expected
3. **Salesforce integration convergence** (6:00-10:00) -- Multiple projects need SFDC access; Kathryn Palkovics' team can help; combine with Thursday agenda
4. **Account planning governance example** (10:00-14:00) -- George and Idris building independently; not "do not build" but "integrate so no silos"
5. **Kathryn Palkovics' governance offer and pace discussion** (14:00-18:00) -- Decision tree for App Factory; team exhaustion acknowledged; governance as reason to slow down
6. **Architecture and pre-reading preparation** (18:00-23:00) -- CLARA adapts to Gainsight; App Factory docs; Chris's next assignment

## Power Dynamics
- **Kathryn Palkovics enters as a governance ally, not a blocker.** Her framing is consistently collaborative: "how do I help" not "how do I control." Her offer to participate in App Factory governance is the first external stakeholder to actively volunteer for programme support rather than demand features.
- **Richard is the strategic coordinator.** He sees the Thursday meeting as an opportunity to solve three problems at once: Gainsight integration, Salesforce access, and governance framework. His multi-project thinking is efficient and politically savvy.
- **Azmain is strategically using Gainsight as a brake.** His candid statement about exhaustion and wanting to slow down reveals that the team has been looking for a legitimate reason to push back on the constant demands for speed. Kathryn Palkovics' governance provides that reason.
- **BenVH is architecturally aligned.** His "less data on our end" philosophy and integration-first design of App Factory show he has been anticipating this conversation. His observation about seeing duplicate app requests validates the governance need.
- **Chris is absorbing context.** Self-described "fly on the wall" but being positioned for Salesforce integration as his next major assignment. His quiet presence is strategic -- he is building understanding before contributing.

## Stakeholder Signals
- **Kathryn Palkovics** -- CRITICAL NEW ALLY. She offers governance help, Gainsight roadmap visibility, and Salesforce access facilitation. She sits between the business and the enterprise tooling teams. Her enthusiasm for governance ("you're speaking my love language") is genuine. She could be the most important new stakeholder addition of the month.
- **Richard** -- Strategic and efficient. Combining Salesforce and Gainsight in one meeting shows good programme management instincts. His concern about resource replanning is legitimate -- Gainsight was not in the 12-week plan.
- **Azmain** -- Strategically candid. Admitting exhaustion publicly and framing governance as a welcome slowdown is politically sophisticated. His "Gainsight team could crush us" comment reveals genuine fear of being displaced.
- **BenVH** -- Consistent on architecture and governance. His observation about duplicate app requests from different people validates the need for a coordination layer.
- **Chris** -- Absorbing and learning. Being positioned for Salesforce integration shows Richard's confidence in his ability to handle a significant technical project.
- **Tina Palumbo** (new, not present) -- Executive-level Gainsight strategy owner. Her position on integration will be decisive.
- **Nadim** (new, not present) -- Kathryn Palkovics' technical counterpart on the Gainsight side. Will be key for determining what can be built within Gainsight vs. externally.
- **Rajesh** (new, not present) -- Technical integration contact. His assessment of API patterns and authentication will determine the integration approach.

## Commitments Made
| Who | Commitment | To Whom | Context |
|-----|-----------|---------|---------|
| Richard | Send App Factory and CLARA docs before Thursday | Gainsight team | Pre-reading for integration meeting |
| Kathryn Palkovics | Set Salesforce inclusion expectation for Thursday | Richard/team | Combined agenda |
| Richard | Get Bernard's detailed requirements by Monday | Team | Salesforce integration scope |
| Kathryn Palkovics | Provide Gainsight roadmap visibility to the team | Richard/Azmain | Governance enablement |
| Kathryn Palkovics | Help design governance/decision tree for App Factory | Richard/Azmain | Intake process |
| Azmain | Adapt CLARA architecture to fit Gainsight | Gainsight team | Integration approach |

## Meeting Effectiveness
| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 8 | Clear preparation plan for Thursday; roles and pre-reading agreed |
| Decision quality | 8 | Excellent strategic decisions: combining agendas, architecture adaptability, governance ally |
| Participation balance | 8 | All five participants contribute meaningfully; Kathryn Palkovics adds most new value |
| Action item specificity | 7 | Good specificity with Thursday-bounded deadlines; some items (governance framework) are longer-term |
| Strategic alignment | 9 | Directly addresses governance gap, Salesforce blocker, and sustainability concerns simultaneously |

## Risk Signals
- **HIGH: Gainsight could marginalise CLARA.** If the Gainsight team decides their roadmap already covers CLARA's functionality, the programme loses its flagship product. Azmain's "they could crush us" fear is well-founded. The mitigation is positioning CLARA as complementary (IRP-specific data feeding into Gainsight's broader customer health view).
- **HIGH: Scope expansion without resource adjustment.** Gainsight integration was not in the 12-week plan. Adding it without removing something else will stretch the already-exhausted team further. Richard flagged this explicitly.
- **MEDIUM: Governance framework is still conceptual.** Kathryn Palkovics' offer is valuable but the decision tree and intake process do not exist yet. Until they do, the current ad-hoc approach continues.
- **MEDIUM: Multiple stakeholders with different integration visions.** Tina Palumbo's executive view, Nadim's build-vs-integrate perspective, and Rajesh's technical constraints may not align. The Thursday meeting could reveal tensions.
- **LOW: Chris and Nikhil pairing for Salesforce.** Given the Nikhil friction documented elsewhere this week, putting Chris and Nikhil on the same project could either be productive (Chris is methodical) or create new tensions.

## Open Questions Raised
- What does Gainsight's authentication model look like? (Moody's SSO or separate login?)
- What REST services or APIs does Gainsight expose for integration?
- Is there a published Gainsight roadmap the team can see to avoid building what is already planned?
- How will the 12-week resource plan be adjusted to accommodate Gainsight integration?
- What governance framework will define which apps enter App Factory?
- How will George's and Idris's account planning apps integrate with Gainsight?

## Raw Quotes of Note
- "Mine and Richard's biggest fear is like Gainsight team could crush us. So we need to keep them on our good side." -- Azmain, on the political dynamics of Gainsight integration
- "You're speaking my love language, Ben." -- Kathryn Palkovics, when BenVH endorsed governance
- "We're exhausted, and it's leading to doing stuff too quick and it not being right... We need to do it right from the beginning, the fast but safe approach, even if that means there's a little bit of a slowdown." -- Azmain, on pace sustainability
- "I would prefer less and less data stored on our end." -- BenVH, on integration architecture philosophy

## Narrative Notes
This meeting is the most strategically significant of the week for the programme's long-term trajectory. Kathryn Palkovics' arrival as a willing governance ally transforms the programme's relationship with enterprise tooling from adversarial (or absent) to collaborative. Her offer to create a decision tree for App Factory intake, combined with her visibility into the Gainsight roadmap and Salesforce access, fills three governance gaps simultaneously. Richard's instinct to combine the Salesforce and Gainsight agendas into a single Thursday meeting is classic programme management efficiency -- solving multiple blockers through one stakeholder engagement. But the most important moment is Azmain's candid admission: the team is exhausted, the pace is leading to errors, and Gainsight governance provides a "perfect reason" to slow down. This is not a complaint -- it is a strategic move. By framing the slowdown as governance-driven rather than capacity-driven, the team avoids appearing weak while getting the breathing room it desperately needs. The risk is real: if the Gainsight team concludes that their roadmap already covers what CLARA does, the programme's flagship product could be marginalised. Azmain's positioning -- CLARA as a small IRP-specific component feeding into Gainsight's broader customer health view -- is the right defensive posture. BenVH's consistent architecture philosophy (minimise stored data, build integration patterns once) provides the technical foundation for whatever integration pattern emerges. The programme is entering a new phase: from building in isolation to coordinating with enterprise systems. This meeting sets the tone for how that coordination will work.
