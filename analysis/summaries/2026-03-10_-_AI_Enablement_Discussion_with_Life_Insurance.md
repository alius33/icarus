# AI Enablement Discussion with Life Insurance (Jack Cheyne & Christian Curran)
**Date:** 2026-03-10
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brookes (late), Jack Cheyne, Christian Curran
**Duration context:** Long (~6,600 words)
**Workstreams touched:** WS2 CLARA, WS6 Build in Five, App Factory

## Key Points
- Richard walked Jack and Christian through the **Native Modelling Engine (NME)** on IRP — the capability for customers to deploy their own models inside Docker containers on the platform, benefiting from IRP's job execution framework, security, and application layer
- Jack drew a comparison to **CAP (Collaborative Analytics Platform)** in Moody's banking — a collaborative platform supporting Python and R where clients can deploy code, connect to banking solutions like EDF X, and share analytics. Different philosophy: CAP is open-ended collaboration, NME is more surgical/controlled integration
- Richard offered to introduce Jack and Christian to **Derek Neil**, the NME product owner in California, for a deeper dive with customers who've already used it
- Ben Brookes (arriving late) presented the **App Factory** concept — the infrastructure for hosting internally-developed apps on AWS
- This meeting was Diya's ask — bringing insurance and other OUs together to explore collaboration opportunities
- Christian raised SSO and role-based access control questions — Richard confirmed all of that comes out of the box with the IRP platform
- The session served dual purpose: educating Life insurance team on IRP capabilities AND exploring what App Factory could do for their use cases

## Decisions Made
- Richard to introduce Jack and Christian to Derek Neil for NME deep-dive → Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Set up intro call with Derek Neil (NME product owner) for Life team | Richard | Next 2 weeks | Open |
| Life team to assess internal use cases for NME (MATLAB/Python models) | Jack / Christian | TBD | Open |
| Follow up on App Factory hosting options for Life team tools | Ben Brookes | TBD | Open |

## Stakeholder Signals
- **Jack Cheyne** — Technically curious and engaged. Asked sharp questions about Docker model execution, data interfaces, and job triggers. Already aware of CAP in banking, drawing useful comparisons. Receptive but needs time to digest use cases.
- **Christian Curran** — Quieter but focused on practical concerns: SSO, security, role-based access. Has context from a prior conversation with Richard about the customer engagement tools.
- The Life team's awareness of IRP capabilities was limited before this session — they had concepts but no detail. This was a successful education session.

## Open Questions Raised
- Would NME be useful for Life team's own modelling workflows? Needs use case assessment.
- How does NME compare/complement CAP for cross-OU use cases?
- What are the specific Life team models that could be containerised?

## Raw Quotes of Note
- "My imagination is good enough to imagine you've got a data layer and all this stuff that connects everything together. But I've not seen it" — Jack, on his pre-session IRP knowledge
