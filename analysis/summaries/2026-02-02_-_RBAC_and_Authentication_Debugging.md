# RBAC and Authentication Debugging
**Date:** 2026-02-02
**Attendees:** Richard Dosoo, BenVH (Ben Van Houten), Azmain Hossain, Martin Davies (briefly)
**Duration context:** Long (~50 minutes -- intensive technical debugging)
**Workstreams touched:** WS2 CLARA

## Key Points
- Deep technical debugging session that identified and resolved the root cause of RBAC failures
- **Root cause identified:** Azure AD returns the username (e.g., `vanhouB`) not the email alias (e.g., `ben.vanhouten@moodys.com`), but the employee table stores aliases -- the system could never match users to permissions
- BenVH connected directly to the RDS database to investigate -- found the `app_user_roles` table had 71 entries manually entered by Richard, but emails were in the wrong format
- The backend token extracted email, but Azure passed `username` not `email` -- a fundamental mismatch
- **Solution:** Richard added optional claims to the Azure AD app registration (email, family name, given name, preferred username, UPN) so the token returns correct identifiers
- BenVH updated the backend code to consume the new claims -- pushed fix to dev
- **Cursor compliance crisis:** Richard received a formal reprimand for using Cursor. Activity has been audited. All subscriptions must be cancelled by Feb 10. Richard's personal credit card is on Azmain's subscription.
- Discussion of Co-pilot limitations for extracting employee data from Active Directory -- it could not query on-prem directory
- Pagination needed urgently -- 4000+ employee records loading without pagination makes pages extremely slow
- Richard reflected on the significance of the Portfolio Review -- first time the insurance CS org had structured, data-driven portfolio management

## Decisions Made
- **Fix auth by adding optional claims to Azure AD token** | Type: Technical | Confidence: High | Owner: Richard/BenVH (done in session)
- **Cancel all Cursor subscriptions by Feb 10** | Type: Compliance | Confidence: High | Owner: Richard/Azmain
- **Update employee emails to match Azure AD format** | Type: Technical/Data | Confidence: High | Owner: BenVH
- **Shift to corporately approved tools only** | Type: Compliance | Confidence: High | Owner: All

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Add optional claims to Azure AD app registration | Richard | 2026-02-02 | Complete (in session) | High |
| Update backend code to use new token claims | BenVH | 2026-02-02 | Open | High |
| Get updated employee email list from Stephanie | Richard | ASAP | Open | Medium |
| Cancel Cursor subscriptions before Feb 10 | Richard/Azmain | 2026-02-10 | Open | High |
| Add pagination to employee/team member lists | Azmain | Next sprint | Open | Medium |
| Remove Richard's personal credit card from Azmain's subscription | Azmain | Immediate | Open | High |

## Theme Segments
1. **Opening / Post-Meeting Reflection (0:00-5:00)** -- Richard reflecting on the Portfolio Review's significance
2. **Database Investigation (5:00-20:00)** -- BenVH connecting to RDS, finding email mismatch
3. **Azure AD Token Fix (20:00-48:00)** -- Adding optional claims, testing token response
4. **Cursor Compliance Issue (16:00-18:00)** -- Richard's formal reprimand and cancellation requirement
5. **Resolution Path (48:00-52:00)** -- BenVH confirms he can fix it, Richard signs off

## Power Dynamics
- **BenVH** is the undisputed infrastructure authority -- the only person who can connect to the database and diagnose at this level
- **Richard** switches between strategist and hands-on participant -- he is the one navigating Azure AD portal while BenVH directs
- **Azmain** is more passive in this session -- BenVH and Richard are driving
- The dynamic reveals the team's dependency: without BenVH, this debugging would have been impossible

## Stakeholder Signals
- **Richard:** Under personal financial and professional risk. His personal credit card is on a Cursor subscription that Moody's has formally flagged. He received a reprimand. Despite this, he is pragmatic and focused on the fix.
- **BenVH:** Technically brilliant and efficient. His 20 years of experience are visibly the difference between this getting fixed in an hour vs. not getting fixed at all. His comment that RBAC is "actually the easiest" he has ever seen hints at his competence level.
- **Azmain:** Learning by observation. His relative quietness in this session shows the gap between his capability and BenVH's.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| BenVH | Fix the RBAC issue using new token claims | Team | Firm |
| Richard | Cancel Cursor and remove personal payment | Compliance | Firm (deadline Feb 10) |
| Richard | Get correct employee emails from Stephanie | Team | Moderate |

## Meeting Effectiveness
- **Clarity of purpose:** 9/10 -- Clear debugging objective
- **Decision quality:** 9/10 -- Root cause identified and solution implemented in-session
- **Follow-through potential:** 9/10 -- Technical fix already partially deployed
- **Stakeholder alignment:** 7/10 -- Team aligned; Josh/CSMs not present
- **Time efficiency:** 8/10 -- Some tangents but highly productive

## Risk Signals
- **Cursor compliance crisis** -- Formal reprimand issued. Personal credit cards used for corporate tooling. Audit trail exists. If this escalates, it could constrain development velocity for weeks. Severity: HIGH
- **BenVH single point of failure confirmed** -- This debugging session could not have happened without him. Severity: HIGH
- **Personal financial exposure** -- Richard's credit card on team subscriptions. Blurs personal/corporate boundaries. Severity: MEDIUM
- **Co-pilot limitations for data extraction** -- Cannot query on-prem Active Directory. Alternative data source needed. Severity: LOW

## Open Questions Raised
- How to get all employee email addresses in the correct format -- Copilot failed
- What tooling will replace Cursor after Feb 10? Claude Code via AWS Bedrock is the hoped-for replacement
- Database performance -- pagination urgently needed for any list with hundreds of entries

## Raw Quotes of Note
- "I got big bollocking this morning... our activity has already been noted and audited that we were using it and we shouldn't" -- Richard, on the Cursor compliance crisis
- "RBAC controls and authentication are usually the hardest things to programme in... this is actually the easiest so far, because at least we get to yell at an AI" -- BenVH, on debugging with AI tools
- "This was the first time I've seen on the meeting... let's go through the accounts in this order. This is the priority" -- Richard, reflecting on the significance of the Portfolio Review

## Narrative Notes
This is the session that actually fixed the RBAC problem. The root cause was elegantly simple -- a mismatch between how Azure AD identifies users (username) and how the app stores them (email alias). BenVH's ability to connect directly to the database and trace the failure end-to-end is what made the diagnosis possible. The Cursor compliance issue, dropped almost casually into the middle of the session, is a significant escalation risk for the programme: the team has been building a critical business tool using personally-funded, corporately-unapproved software, and Moody's has noticed. Richard's personal credit card being on Azmain's subscription adds a layer of personal financial risk to the professional one. The fact that the team is doing its best work under these conditions -- and simultaneously being reprimanded for the tools that enabled it -- is a tension that will define the programme's next phase.
