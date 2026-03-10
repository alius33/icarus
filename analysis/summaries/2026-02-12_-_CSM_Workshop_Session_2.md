# CSM Workshop Session 2 — CLARA Hands-On Session
**Date:** 2026-02-12
**Attendees:** George Dyke (Speaker 1), Azmain Hossain, Miles (Speaker 2/5), Asha (Speaker 3), Philip (Speaker 4), Ashley (Speaker 6), Rachel Gillespie (Speaker 7), Liz Couchman (Speaker 8), Thomas Harrison (Speaker 9)
**Duration context:** Long (~75 minutes, hands-on session)
**Workstreams touched:** WS2 CLARA

## Key Points
- Azmain joins remotely for a dedicated CLARA hands-on session with George's team. He opens with a critical trust-rebuilding commitment: any updates made from yesterday onwards will be preserved. No more data wipes. This is explicitly stated to encourage CSMs to invest time in data entry.
- Azmain flips the conversation from top-down to bottom-up: instead of asking what executives need from the data, he asks what is helpful for the CSMs who are entering it. This is a deliberate change of approach, informed by Richard's coaching earlier in the week.
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
- Rhonda (first live account update in the tool): provided a real account update for Aeon, demonstrating the workflow works end-to-end.

## Decisions Made
| Decision | Type | Made By | Confidence |
|----------|------|---------|------------|
| Data preservation commitment: no more bulk updates that wipe CSM-entered data | Infrastructure | Azmain | High — public commitment |
| Bottom-up approach adopted: ask CSMs what they need, not just what executives want | Process | Azmain/George | High |
| Blocker taxonomy to be standardised as selectable list | Feature | Steve Gentilly/Catherine/Azmain | Medium |
| Implementation lead and PM dashboard views to be added | Feature | George's team request | Medium |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Fix parent/subsidiary rollup issue for dashboard metrics | Azmain | TBD | Open | Medium — architecturally complex |
| Schedule 1:1 sessions with each CSM to review their accounts | Azmain / Natalia's team | TBD | Open | Medium |
| Develop standard blocker taxonomy as selectable list | Steve Gentilly / Catherine / Azmain | TBD | Open | Medium |
| Add implementation lead and PM views to dashboard | Azmain | TBD | Open | Medium |
| Integrate Claude/OpenAI API for intelligent summaries and executive Q&A | Azmain | TBD | Open | Low |

## Theme Segments
| Time Range | Theme | Key Speakers |
|------------|-------|--------------|
| 0:00-5:00 | Data preservation commitment, bottom-up approach introduction | Azmain |
| 5:00-15:00 | Miles's dashboard walkthrough, weekly update workflow | Miles, Azmain |
| 15:00-25:00 | Parent/subsidiary problem, Asha's reciprocity question | Asha, George |
| 25:00-40:00 | Blocker analytics, AI-powered analysis, standardisation | Azmain, Asha |
| 40:00-55:00 | Dev environment features: multi-select, employee profiles, feedback pipeline | Azmain, Philip |
| 55:00-75:00 | Implementation views, Gainsight scepticism, Rhonda's live update | George, Philip, Rhonda |

## Power Dynamics
- **Azmain's data preservation commitment is a trust-rebuilding act.** By publicly promising that data will not be wiped again, he is making a personal guarantee that raises the stakes for any future deployment mishap.
- **George continues to model the behaviour he wants.** His story about pointing Liz McLagan to CLARA instead of answering manually is the most effective advocacy for the tool — it shows the tool replacing a real workflow, not adding to it.
- **Asha is the voice of CSM pragmatism.** Her question about what CSMs get back is the most important challenge raised. If the tool is perceived as one-directional (CSMs feed data upward), adoption will stall.
- **Philip is the technically sophisticated CSM.** His appreciation of the feedback-to-GitHub pipeline shows he understands the development process. His Gainsight scepticism is informed and pragmatic.

## Stakeholder Signals
- **Azmain:** His data preservation commitment is the pivotal moment. CSMs had been burned before — entering data only to have it wiped by deployments. This explicit promise is an attempt to rebuild trust. The bottom-up approach flip is Richard's coaching manifesting in practice.
- **Asha:** The voice of CSM frustration. She wants reciprocity: if she puts data in, she wants to see it being used to help her, not just to serve management reporting. This is the key adoption barrier.
- **George:** Continues to champion the tool by modelling behaviour — pointing Liz McLagan to CLARA rather than answering manual requests. He is the most effective CSM leader in the programme.
- **Miles:** Guinea pig for the live demo. His willingness to be walked through the workflow publicly sets the tone for the group.
- **Philip:** Technically sophisticated. His Gainsight scepticism is a through-line concern: if Gainsight does not materialise for insurance, CLARA becomes even more critical.
- **Rhonda:** Provided the first live account update (Aeon) during the session. A concrete demonstration that the workflow works end-to-end.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| Azmain | Data entered from 11 Feb onwards will never be wiped | All CSMs | Firm — public commitment |
| Azmain | Build blocker taxonomy as selectable list | Steve Gentilly, CSMs | Medium |
| Azmain | Add implementation lead and PM dashboard views | George's team | Medium |
| George | Continue pointing stakeholders to CLARA for account status | Team | Firm — already doing this |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 4 | Several feature requests captured, data commitment made |
| Decision quality | 4 | Bottom-up approach and data preservation are the right moves |
| Engagement balance | 5 | Multiple CSMs contributed, genuine Q&A |
| Time efficiency | 3 | 75 minutes is long, but the content justified it |
| Follow-through potential | 3 | Many action items without concrete deadlines |

## Risk Signals
- **Parent/subsidiary rollup is an architectural debt.** This is not a bug — it is a fundamental data model limitation. Fixing it properly requires rethinking how accounts relate to each other in the database, which could be a significant undertaking.
- **Asha's reciprocity challenge is existential.** If CSMs perceive CLARA as a reporting tool for management rather than a tool that helps them, they will enter the minimum data required and disengage. The blocker analytics and AI summaries are the answer, but they are not yet functional.
- **Gainsight uncertainty.** Philip's scepticism is shared by others. If Gainsight never properly incorporates RMS data, CLARA's scope may need to expand beyond IRP migrations — directly contradicting Josh's scope declaration from the same day.
- **Blocker taxonomy depends on Steve Gentilly and Catherine.** Both are external to the core dev team. If they do not deliver, the free-text blocker problem persists and analytics remain unreliable.

## Open Questions Raised
- How to solve the parent/subsidiary data rollup problem architecturally?
- When will the Claude/OpenAI API integration be live for intelligent blocker analysis and executive Q&A?
- What is the realistic Gainsight timeline for insurance/RMS data?
- How to measure the impact of CLARA on reducing manual update requests?

## Raw Quotes of Note
- "Any updates you make from yesterday onwards will be preserved. We're no longer going to do any big update to wipe things." -- Azmain, the trust-rebuilding commitment

## Narrative Notes
This is the most important CLARA session of the week — the moment the tool is tested by actual users in a live, hands-on setting. Azmain's data preservation commitment is the headline: after weeks of trust damage from deployment wipes, he draws a line and promises it stops here. The bottom-up approach — asking CSMs what helps them rather than telling them what to enter — is a maturation of the programme's product thinking. But the session also reveals the depth of the gap between current capability and user expectations. Asha's question ("what do I get back?") is the question the programme must answer. The blocker analytics and AI-powered summaries are the intended answer, but they are in dev, not prod. George's story about redirecting Liz McLagan to CLARA is the best proof of concept: the tool is already replacing a manual workflow for at least one person. If that pattern can be replicated across the CSM team, adoption will follow. Rhonda's live account update for Aeon is a small but significant milestone — the first time a CSM has updated a real account in a workshop setting. The feedback-to-GitHub pipeline impresses Philip and others. It is a small but symbolic innovation: user complaints becoming automated fix attempts within the same day. This is the kind of responsive iteration that builds tool credibility.
