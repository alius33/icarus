# Tracker Next Steps
**Date:** 2026-02-04
**Attendees:** Richard Dosoo (Speaker 1), BenVH (Speaker 2), Azmain Hossain, Martin Davies
**Duration context:** Long (~35 minutes)
**Workstreams touched:** WS2 CLARA, WS6 Build in Five, WS4 Friday (Adoption Charter)

## Key Points
- BenVH pushed a build overnight but pull requests were going to main instead of develop — didn't want to break dev. Backend service logs showing import errors (cannot import `role_permissions`).
- BenVH fixed the backend issue during the call — restored the ECS service
- Richard brought Martin back into the loop with a comprehensive overview of all programme workstreams:
  - WS2 CLARA (IRP adoption tracker): the main focus, absorbing the adoption charter functionality
  - WS4 Adoption Charter: being folded into CLARA as another function rather than a separate app
  - WS3 CS Agent: sentiment analysis from Salesforce — Sales Recon will provide the data pipeline, the team just needs to build prompts and Azure workflow
  - WS6 Build in Five (Cursor for Pipeline): framework for non-technical users to scope, design, and deploy apps. Martin's primary assignment.
  - Account planning (George's request): 80% of data comes from same Salesforce source as CLARA, should fold in rather than be separate
  - Idris's banking app: separate application, needs auth integration and hosting
- Martin is going on holiday from Wednesday next week for two weeks — can only contribute Monday/Tuesday
- Azmain requested partner section as a quick-win addition (1 day of work) before the adoption charter
- Richard agreed: partner section quick win, then adoption charter when Ben finalises the format
- BenVH introduced staging environment concept: dev (playground) → staging (test/verify) → production
- Discussion of mobile-responsive design: sidebar not collapsible, cards not stacking — needs CSS work for CSMs using phones/tablets
- Azmain showed Moody's-branded UI redesign mockups — getting positive feedback on look and feel

## Decisions Made
- Partner section is a quick-win to do before adoption charter → Richard/Azmain
- Adoption charter waits for Ben Brooks to finalise format with Steve Gentilli and Liz Couchman → Ben Brooks
- Three-environment deployment: dev → staging → production → BenVH
- Martin to scope Build in Five and get estimates before holiday → Martin/Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Fix backend import error in dev | BenVH | 2026-02-04 (done) | Complete |
| Scope Build in Five project with estimates | Martin/Azmain | Before Martin's holiday | Open |
| Build partner section in CLARA | Azmain | Next week | Open |
| Set up staging environment | BenVH | This week | Open |
| Apply UX branding changes to dev | Azmain | This week | Open |

## Stakeholder Signals
- Martin is on the periphery due to his Canopus safeguarding commitments — now getting properly briefed for the first time
- Richard is trying to impose project discipline (scope, timeline, resources) onto what has been a "just build it" culture
- BenVH is methodically building proper infrastructure (staging, CICD) — the professional counterweight to the rapid iteration
- Martin's two-week holiday creates a gap — Build in Five scoping needs to happen in days, not weeks

## Open Questions Raised
- When will Ben Brooks finalise the adoption charter format?
- How to handle Idris's banking app — separate infrastructure or shared?
- Navigator L1 workstream — Richard said it needs a separate meeting, too complex for quick discussion

## Raw Quotes of Note
- "We haven't even like, as Azmain knows, no shade, we've been mad busy. But this is basically we need to treat these like projects in their own right" — Richard, on the programme management gap
