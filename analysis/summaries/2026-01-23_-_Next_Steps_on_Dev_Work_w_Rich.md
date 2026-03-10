# Next Steps on Dev Work with Richard — Risk Management Before Monday
**Date:** 2026-01-23
**Attendees:** Richard Dosoo, Azmain Hossain
**Duration context:** Short (~8 minutes)
**Workstreams touched:** WS2 CLARA (infrastructure, risk management, schema governance)

## Key Points
- Richard walked through how to structure the people/role assignment: a lookup table linking client, role type (CSM/SA/implementation lead), and a reference to the employee list
- Azmain proposed an alternative: skip role filtering entirely and let users search the full employee database for any assignment — trusting users not to misassign
- The core tension: adding a role column to the employee table would be the "right" solution but requires a schema change that could break the database
- Azmain explicitly stated his priority was what was achievable by Monday, even working over the weekend — he was nervous about any schema changes on a field that was "absolutely crucial"
- Richard articulated the pattern: schema change leads to Alembic migration failure, which leads to 500 errors, which leads to hours of debugging with BenVH — they had seen this repeatedly
- Critical decision made: leave any high-risk schema changes to last, so if rollback is needed, there is a stable state to return to
- Azmain proposed a safer approach: write specs for the schema changes, post them on the IRP tracker channel, and wait for BenVH approval before executing — even if that means Monday morning
- Richard suggested he would jump on a call with BenVH to explain the changes if needed
- Both agreed: now that ongoing issues were fixed, hold off on new stuff and focus on stability

## Decisions Made
- **Hold off on risky schema changes until BenVH approves** (type: risk management, confidence: high) — write specs first, get approval, execute only when safe
- **Prioritise stability over new features before Monday** (type: strategic, confidence: high) — the demo must work; new features can wait
- **Write detailed specs for planned schema changes** (type: process, confidence: high) — Azmain to document what Cursor/Claude Code would do, post for review
- **Use the window between 2:30pm Monday call and 3:30pm CSM demo if needed** (type: tactical, confidence: medium) — Claude is fast enough to execute approved changes in that hour

## Action Items
| Action | Owner | Deadline | Confidence |
|--------|-------|----------|------------|
| Write specs for two major schema changes | Azmain Hossain | 2026-01-23 EOD | High |
| Post specs on IRP tracker Teams channel for BenVH review | Azmain Hossain | 2026-01-23 EOD | High |
| Review schema change specs when available | BenVH | 2026-01-24 (weekend) or 2026-01-27 AM | Medium |
| Jump on call with BenVH to explain changes if needed | Richard Dosoo | 2026-01-27 AM | Medium |

## Theme Segments
| Timestamp Range | Theme | Speakers | Tone |
|----------------|-------|----------|------|
| 0:00-2:30 | People table structure and role assignment approach | Richard, Azmain | Technical, collaborative |
| 2:30-4:00 | Schema change anxiety and database stability | Azmain, Richard | Nervous, cautious |
| 4:00-5:30 | Rollback concerns and prioritization strategy | Richard, Azmain | Serious, risk-aware |
| 5:30-7:00 | Spec-first approach and BenVH approval workflow | Azmain, Richard | Pragmatic, relieved |
| 7:00-8:00 | Agreement to hold off on new changes | Both | Aligned, calm |

## Power Dynamics
- **Azmain Hossain** drove this conversation from a position of hard-won experience — his caution about schema changes came from having personally dealt with the consequences of database failures earlier in the week. His willingness to push back against feature pressure showed growing maturity.
- **Richard Dosoo** supported Azmain's caution rather than pushing for more features, showing alignment on risk management. His offer to mediate with BenVH reflected his role as programme bridge between development and operations.

## Stakeholder Signals
- **Azmain Hossain** — His mild panic about database changes was proportionate to the actual risk. The spec-first approach he proposed was the most process-mature suggestion he had made all week — documenting changes before executing them was a significant step toward sustainable development practices.
- **Richard Dosoo** — His concern about schema changes was consistent with his "maintenance burden" theme from earlier calls. His suggestion to leave risky changes to last showed good programme management instinct — always have a fallback position.
- **BenVH** (referenced) — His race preparation and limited availability elevated the importance of the spec-first approach. If he could review specs asynchronously over the weekend, changes could be approved without requiring a live debugging session.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Azmain | Write and post schema change specs | BenVH/Richard | High |
| Azmain | Hold off on new schema changes before Monday | Richard | High |
| Richard | Mediate with BenVH on schema changes if needed | Azmain | Medium |

## Meeting Effectiveness
- **Clarity of outcomes:** 9/10 — Crystal clear decision: no risky changes before Monday, write specs first
- **Decision quality:** 9/10 — Excellent risk management that balanced delivery pressure with stability
- **Engagement balance:** 7/10 — Both contributed but Azmain led the risk assessment
- **Time efficiency:** 9/10 — Eight minutes to reach a critical governance decision

## Risk Signals
| Risk | Severity | Signal |
|------|----------|--------|
| Rollback procedure never tested | HIGH | Richard explicitly noted they have never tested a deployment rollback. If something breaks, they could leave the system in an unusable state. |
| Schema changes as single biggest technical risk | HIGH | Both Azmain and Richard independently identified schema changes as the most likely cause of system failure before the Monday demo. |
| No staging environment for testing changes | MEDIUM | All changes go directly to production. Richard mentioned wanting BenVH to "spin up dev environments" — this has not happened yet. |

## Open Questions Raised
- Has a deployment rollback procedure ever been tested?
- Can BenVH review the specs over the weekend?
- What exactly are the two major schema changes that need to be made?
- When will a staging environment be available so changes can be tested before production?

## Raw Quotes of Note
- "I get like a mild panic attack every time... please God, don't let bad things happen to good people" — Azmain Hossain (from a related call), on database instability
- "We're going to spend ages with Ben debugging why the code is up to date, model up to date, but the process failed" — Richard Dosoo, describing the recurring Alembic migration failure pattern

## Narrative Notes
This eight-minute call was arguably the most strategically important conversation of Thursday. The decision to halt schema changes before Monday and adopt a spec-first approach represented a maturation point for the programme's development practices. For the first time, the team chose stability over velocity — a choice that the deployment failures earlier in the week had made necessary. Azmain's proposal to write detailed specs and wait for BenVH's approval was the first instance of a proper change management process being applied to CLARA's development. The irony was not lost: it took repeated database failures and the loss of development tools to force the adoption of basic software engineering practices that should have been in place from the start. Richard's observation that they had never tested a rollback procedure was sobering — if Monday morning brought a database failure, their only option would be to debug live with 90 minutes until the demo.
