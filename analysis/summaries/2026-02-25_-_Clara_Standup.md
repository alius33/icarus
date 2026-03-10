# Clara Standup
**Date:** 2026-02-25
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (Speaker 2), Martin Davies (Speaker 1/5)
**Duration context:** Long (~44 minutes)
**Workstreams touched:** WS2 CLARA, WS6 Build in Five, WS1 Training

## Key Points
- Martin is back from holiday and receives a comprehensive catch-up on everything that changed while he was out. Scope of Build in Five has expanded significantly: it now has dependencies on the app factory (Ben's automated deployment pipeline) and the consulting AI platform (Azmain's six-layer architecture).
- Three interconnected workstreams explained to Martin: (1) Build in Five for customer demos, (2) App factory for deployment infrastructure, (3) Consulting AI platform for leveraging accumulated IP and assets.
- The value compounding concept: every app built through Build in Five generates a BRD that goes into a requirements database. Future apps can draw from that database rather than starting from scratch -- a "shopping market" for pre-built features.
- 12-week resource plan confirmed: Martin at 75% (pending Stacy sign-off), BenVH at 50%, Chris, Nikhil, and a rotating grad from April 7. Richard needs to formalise sign-off with Stacy and get Ben to reinforce the message.
- Diya meeting recap shared with Martin: she is now supportive, Maps team offering help, three-pillar programme structure endorsed. Post-12-week case for dedicated resources (small team of 3-5) needs to be built.
- CS Agent workstream explained to Martin/BenVH: automated resolution of L1 support tickets using IRP Navigator API, with OpenClaw or Copilot Studio as potential agent frameworks. Needs scoping for throughput testing, API access, and environment ring-fencing.
- Sales Recon data pipeline disappointing: Bernard's UAT revealed parent-to-child hierarchy missing, simple date queries returning wrong data, SSO SAML status outdated. Team now needs to build their own data pipeline from Salesforce and Mixpanel as interim solution.
- BenVH pitches his Phantom Agent solution: a CICD orchestration platform (his own patent) repurposed for AI agent governance. It can spin up agents in appropriate AWS/Kubernetes environments with team-based cost allocation, shared API keys, and security governance via SSO.
- Richard sees the Phantom Agent concept as applicable to SRE automation, bug resolution, and Cat Accelerate issue resolution -- a permanent agent team with self-improvement loops.
- Cross-OU expansion ambition: if Build in Five is ready by March 20, Richard wants to demo to Dimitri and Olga in Dubai to drive cross-OU collaboration. This becomes a motivational target for the team.
- CLARA as an IKEA flat-pack: Azmain proposes turning Clara into a deployable template that other OUs (Life, Banking) can spin up with their own Salesforce extracts, rather than putting everyone on one shared deployment (which would look too much like building Salesforce and invite political pushback).
- Cursor rules file already built: encodes the team's AWS stack, front-end components, API standards, back-end, ECS container deployment -- ensuring all apps built to the same standards.
- Context window issues: Richard discovers Claude truncates project plans when context gets too large, losing previously stored content. Azmain notes Cursor handles compaction better than native Claude.

## Decisions Made
- Martin assigned to Build in Five at 75% capacity for next 12 weeks -> Richard / Stacy to formalise
- CS Agent scope to include automated Salesforce data pipeline (Chris and Nikhil) -> Richard
- Phantom Agent concept to be expanded and run through end of programme -> Richard / BenVH
- Clara to be templatised as flat-pack for cross-OU reuse rather than shared multi-tenant deployment -> Azmain
- Build in Five target: March 20, with aim to demo at exceedance event and potentially in Dubai -> Martin / Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Send all programme documents to Martin for onboarding | Richard | Today (25 Feb) | Open |
| Get Stacy sign-off on Martin's 75% allocation | Richard / Ben | This week | Open |
| Set up standup cadence for Build in Five (Martin, Azmain, Richard) | Azmain | This week | Open |
| Call with Nikhil and Christopher about CS Agent scope | Richard | Today | Open |
| Expand Phantom Agent task scope through end of programme | Richard | This week | Open |
| Follow up with Maps team about infrastructure alignment | BenVH | TBD | Open |

## Stakeholder Signals
- Martin is willing and eager to start immediately, even suggesting 100% allocation rather than the proposed 75%.
- BenVH is passionate about Phantom Agent and sees it as a transformative capability for Moody's, though he is cautious about the Maps team potentially forcing a premature infrastructure migration.
- Azmain is strategically savvy about corporate politics: advising against a single shared platform (invites Salesforce team pushback) and instead recommending the flat-pack approach that plays into cross-OU collaboration narratives senior leaders want to hear.
- Richard is energised by the momentum -- multiple presentations delivered, cross-team interest growing, Diya now supportive -- but still scrambling to formalise resource commitments.

## Open Questions Raised
- Will the Maps team alignment force a migration of infrastructure to their platform, and how soon?
- What agent framework (OpenClaw, Copilot Studio, or custom) will be used for the CS Agent?
- Can the team realistically deliver Build in Five demo quality by March 20 for exceedance?
- How will the consulting AI platform's content layer (SharePoint/Salesforce metadata extraction) be resourced?

## Raw Quotes of Note
- "Give me a team of four and watch me make miracles happen." -- Azmain Hossain, on the post-12-week ambition
