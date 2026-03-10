# Architecture Review - IRP Adoption Tracker Deployment Constraints
**Date:** 2026-01-07
**Attendees:** Richard Dosoo, Ben Brooks, Azmain Hossain, Martin Davies, Adrian Thomas (security/infra, M365/digital workplace), BenVH (Speaker 3/4 — infra engineer), Brandon Smith (mentioned, cyber architecture — not present)
**Duration context:** Long (~32 minutes)
**Workstreams touched:** WS2 (CLARA / IRP Adoption Tracker)

## Key Points
- Formal architecture review call with security/infrastructure teams to clear Azure deployment blockers for CLARA
- Richard frames CLARA as an internal-only tool that enhances Salesforce — a stopgap to manage client adoption while corporate applications catch up. Needs front end, Python API, SQL database behind SSO on Moody's VPN.
- The team has been hitting security restrictions "by design" when trying to expose components or the application to the web within Azure. These are not misconfiguration issues — they are deliberate security constraints.
- Adrian Thomas (M365/digital workplace) acknowledges the request is reasonable but cannot resolve it — this needs **Brandon Smith** from cyber architecture and possibly **Charles Betancourt** (cloud team tower lead). Neither is on the call.
- Ben raises the possibility of pivoting to AWS entirely if Azure continues to block progress. Adrian agrees Azure makes logical sense (SSO, SQL native) but cannot speak to security requirements.
- The aspirational end state Richard describes: a standardised architecture pattern with automated CI/CD pipeline so the broader team can deploy apps without logging into Azure portal and managing networking manually. Currently, the deployment process is too complex for non-infrastructure people.
- After Adrian and the security folks drop off, the core team (Richard, Ben, Azmain, Martin, BenVH) makes the **pivotal decision to deploy on AWS immediately** rather than wait for Azure clearance
- Authentication workaround for AWS: use AWS Cognito with username/password initially (not SSO), keyed on Moody's email addresses so it can be swapped to AD integration later. This mirrors what was done on the data archiving project.
- BenVH confirms he has a personal patented CI/CD orchestration project and has experience porting AWS pipelines to Azure — offers to help with future Azure migration
- Ben gets tips from contacts: Sirian (banking tech) suggests treating this like product development and using existing Azure via the Life team's DevOps (Suman). Another contact says Hosting Plus is on Azure.

## Decisions Made
- **Pivot to AWS for immediate deployment** — this is the week's most consequential decision. Azure remains the long-term target, but AWS gets them a demo next week. → Richard/BenVH
- Use AWS Cognito for interim authentication with Moody's email addresses as identifiers → Richard
- Containerise with Docker for portability between AWS and Azure → BenVH
- Reschedule the architecture review with Brandon Smith (cyber architecture) for next week → Richard
- Add Charles Betancourt (cloud team) to the thread → Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Deploy CLARA to AWS (behind Cognito login) | BenVH | End of this week | Open |
| Reschedule architecture review with Brandon Smith | Richard | Next week | Open |
| Add Charles Betancourt to the thread | Richard | Today | Open |
| Reach out to Suman (Life team DevOps) about existing Azure deployment | Richard | Tomorrow | Open |
| Ping Sirian (banking tech) about Azure deployment patterns | Ben | Today | Open |
| Richard to refine data model and work with Azmain on updates | Richard/Azmain | Tonight | Open |
| Get Martin time booked for 9:30am tomorrow to check in with Ben | Richard | Tomorrow | Open |

## Stakeholder Signals
- **Adrian Thomas** is helpful but clearly out of scope — this is a cyber architecture problem, not an M365 problem. He's honest about not being able to resolve it and redirects appropriately.
- **Richard** is frustrated but diplomatic. The line "we're not trying to do anything unreasonable, deploying a web app and a database" captures his feeling that the infrastructure should support them, not block them.
- **Ben** is pragmatic — immediately suggests AWS pivot when Azure looks stuck. Also concerned about SSO credibility (CSMs won't trust a tool without proper login).
- **BenVH** is quietly confident — already has deployment scripts and experience. Single point of failure acknowledged.

## Open Questions Raised
- Is there a standard pattern within Moody's for deploying internal web apps on Azure? Nobody on the call knows.
- Could MAP (Moody's Application Platform) be used instead of raw Azure/AWS? Richard deliberately avoided MAP because it's for production workflows and support might be limited. But MAP strategy may be changing.
- Will Brandon Smith's cyber architecture review next week unblock Azure, or is it a dead end?

## Raw Quotes of Note
- "It's just frustrating because, like, we're not trying to do anything unreasonable, deploying a web app and a database. It should just work for us. The infrastructure should support us, but it's not." — Richard Dosoo, on the Azure deployment struggle
