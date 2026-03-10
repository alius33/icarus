# Adoption Tracker RBAC Permissions Debug
**Date:** 2026-02-02
**Attendees:** Richard Dosoo, BenVH (Ben Van Houten), Azmain Hossain, Philip Garner
**Duration context:** Medium (~30 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Live debugging session for RBAC permissions failure with Philip Garner as the test subject
- Philip could not save edits (executive summary field) -- received "insufficient permissions" error in the network console response
- BenVH walked Philip through browser dev tools to capture the error -- network tab showed 403 on the save endpoint
- Root cause investigation: permissions assigned via admin panel were not being applied to the user on login -- admin section not appearing in Philip's navigation
- Azmain had assigned Philip admin/editor roles but the changes did not propagate -- even after re-assignment and cache-clearing
- BenVH removed his own admin access temporarily to simulate the CSM experience for testing
- Discussion of AI tool limitations: Cursor/Claude helped build 80-90% of the application but started hallucinating on edge cases around RBAC
- Richard managed Josh's alarm about data loss in real-time via messaging -- narrowed the scope to only two account managers affected (Philip and Naveen)
- Philip offered continued testing help -- showed willingness and practical attitude despite the frustration

## Decisions Made
- **Philip confirmed as ongoing RBAC test user** | Type: Process | Confidence: High | Owner: Team
- **Data loss scope communicated as limited to 2 users** | Type: Communication/Framing | Confidence: High | Owner: Richard
- **Will reproduce the permissions issue without Philip** | Type: Technical | Confidence: Medium | Owner: BenVH/Azmain

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Fix RBAC permissions propagation on login | BenVH/Azmain | 2026-02-02 | Open | High |
| Communicate data loss scope to Josh -- only 2 users affected | Richard | 2026-02-02 | Done | High |
| Continue RBAC testing once fix deployed | Philip | Next day | Open | High |

## Theme Segments
1. **Opening / Test Setup (0:00-4:00)** -- Informal start, getting Philip on the call, banter about Cursor/AI misbehaviour
2. **Philip's Perspective on the Portfolio Review (4:00-7:00)** -- Philip gives substantive feedback on the meeting structure and product tracking gaps
3. **RBAC Debugging (7:00-28:00)** -- Console inspection, permissions investigation, discovery that roles are not propagating
4. **Data Loss Damage Control (24:00-27:00)** -- Richard messaging Josh to contain the narrative
5. **Wrap-up (28:00-30:00)** -- Philip offers continued help, BenVH commits to fixing

## Power Dynamics
- **Richard** is the communications strategist -- managing Josh's reaction to the data loss in real-time, choosing what to minimise and when
- **BenVH** holds technical authority -- he is the one who can actually diagnose and fix infrastructure-level issues
- **Philip** is the willing participant/guinea pig -- his positive attitude is being leveraged but also genuinely appreciated
- **Azmain** is somewhat passive here -- BenVH is leading the debugging, and Richard is leading the messaging

## Stakeholder Signals
- **Philip Garner:** Engaged, willing, constructive. His comment about wanting client-facing transparency dashboards shows forward-thinking. He is becoming an internal champion.
- **BenVH:** Pragmatic about AI limitations -- treats Cursor/Claude as a junior developer. Focused and competent under pressure.
- **Richard:** Politically astute in real-time. Immediately moves to contain Josh's reaction by narrowing the scope of the data loss. Dismissive of Naveen's complaints.
- **Josh (off-screen):** Reacting to data loss with alarm. Richard is working hard to prevent escalation.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| BenVH | Fix RBAC permissions issue | Team | Firm |
| Philip | Continue testing tomorrow | Team | Firm |
| Richard | Communicate data loss scope to Josh | Team | Done in real-time |

## Meeting Effectiveness
- **Clarity of purpose:** 8/10 -- Clear debugging session with specific goals
- **Decision quality:** 7/10 -- Good triage decisions, root cause still unclear at end
- **Follow-through potential:** 8/10 -- Specific next steps assigned
- **Stakeholder alignment:** 6/10 -- Josh not on the call, being managed via messaging
- **Time efficiency:** 7/10 -- Some banter but productive overall

## Risk Signals
- **RBAC complexity underestimated** -- The team built roles and permissions but the plumbing to connect them was broken. This is a foundational issue. Severity: HIGH
- **Data loss trust damage** -- Even limited to 2 users, the perception of unreliability now exists. Severity: MEDIUM
- **Josh's reaction unpredictable** -- Richard is managing him in real-time but there is a risk of escalation. Severity: MEDIUM

## Open Questions Raised
- Is the permissions issue a caching problem or a fundamental application logic issue?
- How much data did Naveen actually enter over the weekend? Richard was dismissive of his complaints.
- Will the fix need to touch the frontend, the backend, or both?

## Raw Quotes of Note
- "It's got us 80 to 90% of the way there. The problem is, now that we're here, it can't keep up with everything, so it starts hallucinating" -- BenVH, on Cursor/Claude limitations at the edge cases
- "It's me. The problem is, AI is winning the argument." -- BenVH, self-deprecating humour about debugging with AI
- "This is almost a saving grace, though, isn't it? Because it means humans are not yet obsolete." -- Philip, on AI limitations

## Narrative Notes
This session reveals the gap between "it works in demo" and "it works in production." The RBAC system was built by AI tools and appeared functional, but the connection between Azure AD authentication and in-app permissions was never properly validated with real users. BenVH's candid assessment of AI as "80-90% there" is an important data point for the programme -- it suggests the remaining 10-20% (security, edge cases, integration) requires genuine engineering expertise. Richard's instinct to immediately manage Josh's perception of the data loss -- rather than focus purely on the technical fix -- shows his political awareness and his understanding that CSM trust, once lost, is difficult to rebuild.
