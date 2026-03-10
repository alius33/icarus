# RBAC & Authentication Debugging
**Date:** 2026-02-02
**Attendees:** Richard Dosoo (Speaker 1), BenVH (Speaker 2), Azmain Hossain (Speaker 3/5), Martin Davies (Speaker 4/6)
**Duration context:** Long (~50 minutes, deep technical debugging)
**Workstreams touched:** WS2 CLARA

## Key Points
- Intensive technical debugging session to resolve the root cause of RBAC failures discovered in the earlier session
- Root cause identified: Azure AD returns the username (e.g., `vanhouB`) not the email alias (e.g., `ben.vanhouten@moodys.com`), but the employee table stores aliases — so the system can't match users to their permissions
- BenVH connected directly to the RDS database to investigate — found the `app_user_roles` table had 71 entries (manually entered by Richard) but emails were in the wrong format
- The backend token extracts email, but Azure passes `username` not `email` — fundamental mismatch
- Solution: Add optional claims to the Azure AD app registration (email, family name, given name, preferred username, UPN) so the token returns the correct identifiers
- Richard went into Azure portal and added the optional claims to the token configuration
- Separate issue: Richard received a formal reprimand for using Cursor — their activity has been audited and noted. Cursor subscriptions must be cancelled by Feb 10. Need to shift to corporately approved tools only.
- Richard told Azmain to cancel his subscription and remove payment details (Richard's personal credit card)
- Discussion of pagination need — 4000+ employee records loading without pagination makes pages extremely slow

## Decisions Made
- Fix authentication by adding optional claims (email, preferred_username) to Azure AD token → BenVH/Richard
- Cancel all Cursor subscriptions by Feb 10 — shift to approved tooling only → Richard/Azmain
- Update employee table emails to match Azure AD usernames as interim fix → BenVH
- Once token returns correct email, RBAC should work for all users → BenVH

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Add optional claims to Azure AD app registration | Richard | 2026-02-02 (done in session) | Complete |
| Update backend code to use new token claims for user matching | BenVH | 2026-02-02 | Open |
| Get updated employee email list from Stephanie | Richard | ASAP | Open |
| Cancel Cursor subscriptions before Feb 10 renewal | Richard/Azmain | 2026-02-10 | Open |
| Add pagination to employee/team member lists | Azmain | Next sprint | Open |

## Stakeholder Signals
- Cursor licence issue is a serious compliance problem — Moody's has formally noted the unauthorised usage. This constrains future development velocity.
- BenVH is the critical infrastructure person — only one who can debug at this level. Confirms his single-point-of-failure status.
- Richard is frustrated by the bureaucratic friction but pragmatic — acknowledges the need to comply
- The team's resourcefulness in solving Azure AD issues live on-call is impressive but also reveals the fragility of the setup

## Open Questions Raised
- How to get all employee email addresses in the correct format — Copilot couldn't query on-prem Active Directory
- What tooling will replace Cursor after the Feb 10 deadline? Claude Code via AWS Bedrock is the hoped-for replacement
- Database performance — pagination is needed urgently for any list with hundreds of entries

## Raw Quotes of Note
- "I got big bollocking this morning... our activity has already been noted and audited that we were using it and we shouldn't" — Richard, on the Cursor compliance issue
