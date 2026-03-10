# Monday Tracker Standup
**Date:** 2026-02-09
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brooks, BenVH (Speaker 1), Martin Davies
**Duration context:** Medium (~30 minutes)
**Workstreams touched:** WS2 CLARA, WS6 Build in Five

## Key Points
- Richard confirms Claude Code access secured via AWS pilot. They will connect Claude Code to the AWS environment rather than using the desktop interface. Both Richard and Azmain running out of personal Claude subscriptions (Azmain's expires ~13 Feb).
- Action plans have been pushed to prod successfully after BenVH resolved the EC2 instance issue. A front-end filter was blocking action plans from displaying — one of the PRs addresses this.
- Azmain has two PRs with merge conflicts: PR #38 (removes demo mode functionality + fixes) supersedes PR #33. BenVH resolves one conflict; Claude resolves the other by creating a new PR.
- BenVH announces a new staging environment, giving three environments total (dev, staging, prod). Staging is a clone of the production database, enabling proper QA before promoting to prod.
- Ben Brooks pushes for CSM usability features as the top priority — specifically transcript upload to auto-populate customer updates. Argues this will drive adoption faster than adding partner management or solution architecture tracking.
- Richard wants to prioritise the partner management piece (for Alexandra and Liz McLagan). Ben disagrees on sequencing — partners can tolerate a spreadsheet for two more weeks, but losing CSM engagement momentum is costly given the 40-migration target this year.
- Natalia has been briefed on the portfolio review screen layout: start with 2026 scorecard migration priority clients (31), then non-priority reds/ambers, then accelerated adoption. She also wants a management dashboard that could replace the PowerPoint deck Diya currently receives.
- Ben Brooks envisions embedding LLM capabilities (via AWS Bedrock) into CLARA: (1) transcript triage to pre-populate fields with human-in-the-loop before save, (2) executive chat window to ask questions about implementations.
- Richard reports the asset management team (Amanda Fleming) has independently built a similar but more advanced app with LLM integration and NPS categorization. Natalia advised against replicating what Amanda has done to avoid antagonizing the Gainsight team.
- Martin Davies leaves Wednesday for two weeks. Richard wants to walk through Martin's Build in Five plan before he goes.
- Richard raises whether they should prepare demos for the Exceedance event, noting Martin's work could overlay nicely.

## Decisions Made
- CSM usability (transcript upload, ease of data entry) prioritised over partner management features -> Ben Brooks, agreed by team
- PR #33 cancelled, PR #38 is the canonical fix -> Azmain/BenVH
- Three-environment workflow adopted (dev -> staging -> prod) -> BenVH

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Get Claude Code API keys and environment access set up | Richard | 2026-02-09 | Open |
| Get PRs merged and ready for Josh/Catherine review this afternoon | Azmain | 2026-02-09 | Open |
| Walk through Martin's Build in Five plan before Wednesday departure | Richard/Martin | 2026-02-11 | Open |
| Schedule conversation about Exceedance demos | Ben Brooks/Richard | TBD | Open |
| Compare Amanda's PRD against CLARA features | Richard | TBD | Open |

## Stakeholder Signals
- Ben Brooks is laser-focused on CSM usability as the adoption lever. Impatient with feature requests that don't directly drive migration tracking engagement. His instinct is always speed and simplicity.
- Richard is trying to balance multiple stakeholder demands (partners, Natalia's dashboard, Ben's usability vision) while keeping the team focused.
- Martin Davies is about to go on two weeks' leave, creating a gap in Build in Five progress.
- Natalia is shaping the portfolio review to be structured and scorecard-aligned, resisting unnecessary complexity.

## Open Questions Raised
- Should they prepare IRP demos for the Exceedance event this year?
- Can the Amanda Fleming PRD be used to accelerate CLARA features without stepping on Gainsight's toes?
- When will Claude Code API keys be available for embedding LLM in the app?

## Raw Quotes of Note
- "If we hammer usability for the CSMs, implementations, SAT teams and then execs as well for visibility, so that we're really crunching down on everybody to use this thing because the visibility is forcing it, then I would go to partners after that." -- Ben Brooks, on prioritisation
