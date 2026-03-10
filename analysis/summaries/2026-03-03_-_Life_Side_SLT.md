# Life Side SLT
**Date:** 2026-03-03
**Attendees:** Ben Brooks, Richard Dosoo (Speaker 1/6), Azmain Hossain, Christophe (Speaker 3), Jack (Speaker 5), Jason (Speaker 4), Alexandre (Speaker 2), Michelle (mentioned), Kelly (mentioned, absent)
**Duration context:** Medium (~30 minutes)
**Workstreams touched:** WS2 CLARA, Cross-OU scaling, Gainsight relationship

## Key Points
- CLARA was demoed to the Life Side Senior Leadership Team at Christophe's invitation, following a prior presentation at the insurance ISLT meeting.
- Ben Brooks set the narrative frame: the journey from dashboards to system of record, driven by the realisation that the problem was data visibility, not visualisation. He described building three iterations over Christmas week in Cursor.
- Richard demonstrated CLARA live: authentication (Moody's SSO), RBAC, account portfolio view, product-level metrics (Risk Link, Risk Browser adoption), individual customer breakdowns (use cases, blockers, action plans), and the portfolio review dashboard.
- Jack raised the key infrastructure question: how did they handle customer data security and hosting? Richard confirmed AWS hosting with TSG Azure tenant for SSO authentication, role-based access control. Jack wants a follow-up session to understand the pattern for replication.
- Jack compared CLARA to "Gainsight on steroids" -- Richard immediately cautioned that CLARA is complementary to Gainsight, not a replacement. He has been told several times to frame it this way.
- Azmain proposed the template/flat-pack approach: strip out IRP-specific elements and create a reusable foundation that other teams can deploy for their own migration/adoption tracking.
- Alexandre noted the speed of development -- Azmain demonstrated live code changes in plain English, promoting from dev to test to production. This visibly impressed the Life SLT.
- Jason wanted Salesforce integration and data flowing back into Salesforce/Gainsight as the system of record. This aligns with existing plans.
- Jack identified value for light-touch tools beyond Gainsight capabilities but emphasised that data must flow back to central repositories for cross-OU visibility.
- Christophe confirmed the demo was useful and suggested the next step was for the Life team to play with the app and reconvene to discuss what it could mean for their use cases (pay-as-you-go conversion, glass conversion, hosting, renewals).

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| CLARA is complementary to Gainsight, not a replacement | Strategic positioning | High | Richard (reinforced multiple times) |
| Template/flat-pack approach proposed for cross-OU reuse | Architecture | Medium | Azmain |
| Life team to get read-only access to explore the app | Access | High | Azmain |
| Follow-up session with Jack on infrastructure patterns | Process | High | Richard |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Set up infrastructure walkthrough session with Jack | Richard | TBD | Open | High |
| Share CLARA link and slides with Life SLT | Richard | Today | Open | High |
| Life team to explore CLARA and identify potential use cases | Christophe, Jack, Jason | TBD | Open | Medium |
| Reconvene to discuss Life team applicability | All | TBD | Open | Medium |

## Theme Segments
1. **Ben Brooks narrative** (0:00-7:00) -- Journey from dashboards to system of record; iterative Cursor development
2. **Live CLARA demo** (7:00-16:00) -- Authentication, portfolio view, metrics, blockers, action plans, portfolio review
3. **Gainsight positioning debate** (16:00-22:00) -- Jack's "on steroids" comment; Richard's careful correction; Azmain's template pitch
4. **Cross-OU applicability discussion** (22:00-30:00) -- Life team use cases; data flow back to Salesforce/Gainsight

## Power Dynamics
- **Ben Brooks commands attention** even from a car with no camera. His narrative framing (Christmas build, iterative discovery, data visibility problem) is compelling and sets the tone.
- **Richard runs the demo confidently** and manages the Gainsight messaging carefully. He has clearly been coached on this positioning.
- **Azmain provides the technical vision** (template approach, live development demonstration) and positions himself as the execution engine.
- **Jack is the most engaged Life SLT member.** He asks the sharpest questions (data security, infrastructure patterns) and sees the infrastructure as the real value.
- **Alexandre plays the champion role** -- he has seen CLARA development firsthand and vouches for the speed. He is the internal sponsor for cross-OU interest.
- **Jason focuses on data integration** -- his concern is Salesforce as the central repository, reflecting a traditional enterprise data governance mindset.
- **Christophe chairs efficiently** -- frames the meeting, manages time, sets next steps.

## Stakeholder Signals
- **Life SLT** -- Newly engaged audience. Impressed by development speed and the RBAC/authentication story. Jack sees reusable infrastructure patterns. Jason wants Salesforce integration. Alexandre is already an advocate. This is a potential expansion opportunity but also a scope creep risk.
- **Ben Brooks** -- Continues to shop CLARA around to generate independent demand. This is his "kill them with kindness" strategy -- create enough cross-OU interest that CLARA becomes politically untouchable.
- **Richard** -- Precise on Gainsight messaging. He has clearly been burned by positioning CLARA as a competitor to Gainsight and is now very disciplined about saying "complementary."
- **Azmain** -- The template/flat-pack concept is new and well-received. He is thinking beyond IRP-specific needs toward platform-level reusability.

## Commitments Made
| Who | Commitment | To Whom | Context |
|-----|-----------|---------|---------|
| Richard | Infrastructure walkthrough session for Jack | Jack | Replication of authentication/hosting pattern |
| Richard | Share slides and CLARA link | Life SLT | Follow-up |
| Life SLT | Explore CLARA and identify use cases | Richard/Azmain | Potential adoption |

## Meeting Effectiveness
| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 7 | Clear next steps (explore app, follow-up call) |
| Decision quality | 7 | Gainsight positioning well handled; no premature commitments |
| Participation balance | 8 | Good engagement from multiple Life SLT members |
| Action item specificity | 6 | Follow-ups agreed but not time-bound |
| Strategic alignment | 8 | Creates cross-OU interest without overcommitting |

## Risk Signals
- **MEDIUM: Scope creep via cross-OU expansion.** If the Life team wants their own CLARA instance, it adds significant work to an already overloaded team. The template approach mitigates this but is not yet built.
- **MEDIUM: Gainsight relationship fragility.** Jack's "on steroids" comment shows how easily CLARA's positioning can slide toward "Gainsight replacement" in stakeholder minds, despite careful messaging.
- **LOW: Impression management risk.** Ben Brooks framing the Christmas build as a compelling origin story, combined with Azmain's live demo, creates high expectations that may be difficult to sustain as the team scales.

## Open Questions Raised
- What specific Life team use cases would benefit from a CLARA-style template?
- How would the template approach work technically -- separate database, shared infrastructure?
- What is the Gainsight roadmap for features that CLARA currently fills?

## Raw Quotes of Note
- "I've been told several times that this is complementary to Gainsight. It's not -- it's serving a function that Gainsight currently can't do for us." -- Richard, carefully walking the positioning line
- "The speed at which you can have something flexible is very impressive, which means that if we need something similar, we could probably have something in a matter of less than a month." -- Alexandre, on the template approach

## Narrative Notes
This is the first time CLARA has been presented to a non-insurance leadership audience, and the reception is overwhelmingly positive. The most strategically interesting moment is Jack's "Gainsight on steroids" comment, which reveals how naturally CLARA's capabilities invite comparison with the enterprise platform. Richard's immediate, almost reflexive correction -- "I've been told several times that this is complementary" -- shows how sensitive this positioning is. The template/flat-pack concept proposed by Azmain is potentially the most significant long-term idea to emerge this week: if CLARA's architecture can be genuinely modularised and made reusable, it transforms from a single-programme tool into an internal platform. But the gap between that vision and the current reality (zero documentation, one overloaded developer, no formal template architecture) is vast.
