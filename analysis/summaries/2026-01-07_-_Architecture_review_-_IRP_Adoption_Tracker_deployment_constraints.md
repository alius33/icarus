# Architecture Review - IRP Adoption Tracker Deployment Constraints
**Date:** 2026-01-07
**Attendees:** Richard Dosoo, Ben Brooks, Azmain Hossain, Martin Davies, Adrian (Speaker 1 -- M365/Digital Workplace), Thomas (Speaker 2 -- Cloud Identity/Graph API), BenVH (Speaker 3/4/5 -- infra engineer)
**Duration context:** Medium (~32 minutes, transcript ~220 lines)
**Workstreams touched:** WS2 (CLARA/IRP Adoption Tracker)

## Key Points
- First formal attempt to engage Moody's internal IT/security teams on the CLARA deployment problem
- Richard walks Adrian and Thomas through the architecture: Next.js frontend, Python FastAPI backend, SQL database targeting Azure App Service
- The team has been repeatedly blocked by Azure security constraints when trying to expose the application to internal VPN users
- Adrian (M365) and Thomas (Cloud Identity) both acknowledge the request is reasonable but redirect to Brandon Smith (cyber architect) and Charles Betancourt (cloud tower lead)
- Thomas explicitly states these questions are outside his scope -- he manages cloud identities and Graph API access only
- Ben raises the possibility of pivoting entirely to AWS, noting the team just needs to host an internal collaboration app
- Adrian argues Azure makes more sense (SSO, SQL, Microsoft ecosystem) but cannot provide security approval
- Richard articulates the aspirational goal: a standardised deployment pattern/template so any team member can deploy without touching Azure portal
- Meeting ends with no resolution -- rescheduling with Brandon Smith for next week is the primary outcome
- After IT team leaves, core team makes the decisive AWS pivot
- BenVH reveals he has CI/CD pipeline code from personal projects that can be adapted for AWS deployment
- Authentication compromise agreed: AWS Cognito (username/password) for now, swap to AD integration later
- Ben gets two external leads: Sayed (Azure hosting knowledge), Sirianzin (banking tech, suggests treating it as product development via existing Azure DevOps)
- Decision to use Docker containers for cloud portability
- The team explicitly notes MAP (Moody's Analytics Platform) as the eventual production home but deferred for now

## Decisions Made
- Reschedule with Brandon Smith (cyber architect) next week: Adrian suggested, Richard accepted -> Richard
  - **Type:** explicit
  - **Confidence:** HIGH
- Pivot to AWS for immediate deployment, continue Azure investigation in parallel: Richard proposed after IT dropped off -> Team
  - **Type:** explicit
  - **Confidence:** HIGH
- Use AWS Cognito for interim authentication with email-address-based user model: Richard/Ben agreed -> Richard
  - **Type:** explicit
  - **Confidence:** HIGH
- Dockerize application for portability between cloud environments: Team consensus -> BenVH
  - **Type:** explicit
  - **Confidence:** HIGH
- Defer MAP platform until app exits POC stage: Richard -> Richard
  - **Type:** explicit
  - **Confidence:** MEDIUM
- Email address as the portable identity key across all platforms: Ben/Richard -> Richard
  - **Type:** explicit
  - **Confidence:** HIGH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Reschedule call with Brandon Smith | Richard | Next week | Open | HIGH |
| Include Charles Betancourt in follow-up | Richard | Next week | Open | HIGH |
| Deploy CLARA to AWS behind basic login | BenVH | End of week (10 Jan) | Open | HIGH |
| Contact Sayed about Azure hosting | Ben Brooks | Tomorrow | Open | LOW |
| Contact Sirianzin about banking tech Azure approach | Ben Brooks | Tomorrow | Open | LOW |
| Set up collaborative dev workflow | Richard/BenVH | This week | Open | MEDIUM |
| Write up deployment approach in slides | Richard | This week | Open | MEDIUM |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Azure security blocking deployment | technical | "what we're coming up against is security constraints that have been implemented by design" -- Richard | HIGH |
| IT jurisdictional boundaries | governance | "this is a lot of architecture stuff, which is a little outside of the scope of what I do" -- Thomas | HIGH |
| AWS pivot decision | technical | "if we said today... Ben will have this happening tomorrow" -- Richard | HIGH |
| Standardised deployment vision | strategic | "standard pattern, standard architecture, standard tech stack... automate the deployment" -- Richard | HIGH |
| Authentication portability | technical | "we separate the authentication and the access into two separate bits" -- Richard | HIGH |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Richard Dosoo | Meeting driver, IT liaison, decision maker | Frames problem for IT, makes AWS pivot call after they leave | 50% |
| Ben Brooks | Technical authority, option generator | Raises AWS alternative, gets external contacts, pushes SSO importance | 25% |
| Adrian (M365) | Gatekeeper, redirector | Acknowledges value but routes to other teams | 10% |
| Thomas (Cloud Identity) | Scope boundary setter | Explicitly declares out of scope | 5% |
| BenVH | CI/CD implementer | Offers Docker deployment expertise from personal projects | 10% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Richard Dosoo | frustrated | DOWN | Azure deployment friction | "it's just frustrating because... we're not trying to do anything unreasonable" |
| Ben Brooks | pragmatic | STABLE | Platform flexibility | "I don't want to make it any more complicated than it needs to be" |
| Adrian | neutral | STABLE | Architecture review | "huge value in it, just to do a rinse and repeat" |
| Thomas | disengaged | STABLE | Not his domain | Out of scope declaration |
| BenVH | supportive | NEW | AWS deployment readiness | Has existing scripts to deploy quickly |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Richard | Reschedule with Brandon Smith and Charles Betancourt | Next week | They are available | MEDIUM |
| BenVH | Deploy CLARA to AWS | End of week | Code and data model ready | HIGH |
| Ben Brooks | Contact Sayed and Sirianzin | Tomorrow | None | LOW |

## Meeting Effectiveness
- **Type:** escalation
- **Overall Score:** 52
- **Decision Velocity:** 0.3
- **Action Clarity:** 0.5
- **Engagement Balance:** 0.3
- **Topic Completion:** 0.4
- **Follow Through:** 0.6

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-005 | OPEN | Azure deployment blocked with no clear internal champion | HIGH | ESCALATING | technical | HIGH |
| R-014 | OPEN | IT jurisdictional gaps -- no single team owns internal web app deployment pattern | MEDIUM | NEW | organisational | HIGH |
| R-015 | OPEN | AWS interim creates technical debt if Azure migration is delayed | MEDIUM | NEW | technical | MEDIUM |
| R-016 | OPEN | No AD integration on AWS -- reduced credibility with end users | MEDIUM | NEW | technical | HIGH |

## Open Questions Raised
- Who in Moody's actually owns the deployment architecture pattern for internal web apps?
- Is this deployment pattern common across Moody's, or genuinely novel?
- Could MAP be the right home instead of Azure App Service?
- What security requirements will Brandon Smith impose?

## Raw Quotes of Note
- "we keep hitting security issues that are by design when we're trying to expose either components of the stack" -- Richard, on Azure blockers
- "this is a lot of architecture stuff, which is a little outside of the scope of what I do here" -- Thomas, on jurisdiction
- "if we said today... Ben will have this happening tomorrow" -- Richard, on AWS speed
- "we just need to host an internal collaboration application with a front end back end of the database" -- Ben, on the simplicity of the actual requirement

## Narrative Notes
This meeting crystallises the deployment crisis. The team has spent weeks hitting Azure walls, finally gets supposed experts on a call, and discovers they cannot help -- they just redirect to more people. Neither Adrian (M365) nor Thomas (cloud identity) can evaluate or approve a web app deployment. The result is yet another week of waiting for the right person (Brandon Smith).

The real decision happens minutes after the IT people leave. Richard declares the AWS pivot with notable confidence in BenVH's ability to deliver quickly. The contrast is striking: weeks of Azure frustration versus BenVH's "I can deploy this tomorrow." The authentication compromise (Cognito vs AD) is pragmatic but carries the credibility risk Ben warned about. This meeting marks the point where the team stops asking for permission and starts building around organisational obstacles.
