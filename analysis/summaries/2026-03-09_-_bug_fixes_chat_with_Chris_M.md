# Bug Fixes Chat with Chris M
**Date:** 2026-03-09
**Attendees:** Azmain Hossain, Chris M
**Duration context:** Medium (~36 min)
**Primary project:** CLARA
**Secondary projects:** Program Management

## Key Points
- Chris has been working on a date input bug fix (S3 severity) — different browsers handle min/max date field boundaries differently, causing some users to see errors when entering dates
- **Root cause:** The CLARA app does not explicitly define min/max values on date fields, leaving it to browser defaults. Some browsers allow 5 or 6 digit years, others only 4 — causing entry errors when they clash with required formats
- **Date min limit to be set to 2022** — Ben Brookes requested this after discovering someone entered a 1999 date which broke the migration burndown chart (a 26-year gap then all data at the end)
- **Philosophical question:** Whether to set hard limits vs use calendar-only input. Azmain decided: push the fix as-is, enforce calendar picker usage rather than free-form typing, and let users report edge cases via the feedback form
- **Date format concern raised:** US (MM/DD) vs European (DD/MM) ordering — Chris to verify the database handles this correctly regardless of browser locale
- **939 tests** run at each stage of the CI pipeline (branch → develop → staging → main). Azmain walked Chris through the full deployment process for the first time
- **Chris cannot run full test suite** because he doesn't have prod database access — BenVH is working on getting that set up
- Chris found the documentation AI-generated ("so nicely ordered and so wordy") and had never been referenced by anyone
- **CSM frustration boiling point for Azmain:** Portfolio Review call users ask 17 messages of "where do I click?" after 4 weeks. Kathryn Palkovics keeps changing data requirements. Azmain is losing patience
- **Environment URLs:** dev.advisoryappfactory, staging.advisoryappfactory, and production (advisoryappfactory)
- Cat Accelerate comparison: "wild west" — just merge to main with 2 reviewers, no staging buffers. CLARA's three-environment pipeline is more rigorous

## Decisions Made
- Set date input min to 2022, max to defined year, across all date fields → Azmain/Chris
- Push current fix as-is; don't over-engineer the date input UX → Azmain, pragmatic
- Chris to verify date format ordering (US/EU) is handled correctly by the database → Chris
- Users should use the calendar picker, not type dates manually → Azmain, design intent

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Update date input fields with min=2022 and explicit max across all TSX files | Chris | This week | Open |
| Verify date format ordering (US vs EU) is handled correctly by database | Chris | This week | Open |
| Push bug fix branch through develop → staging → main | Chris | After tests pass | Open |
| Get prod database access for Chris from BenVH | BenVH / Chris | Ongoing (BenVH swamped) | Open |
| Add Chris as contributor to CLARA repo (done during call) | Azmain | Done | Completed |

## Stakeholder Signals
- **Chris M** — In the "honeymoon phase" with CLARA development. Methodical about testing and philosophical about change scope. Good instincts (flagged date format locale issue that Azmain hadn't considered). Adapting to the three-environment pipeline vs Cat Accelerate's Wild West approach
- **Azmain** — Frustrated with CSM behaviour ("it's been four weeks and you're an adult and it's 2026, I shouldn't have to teach you how to use a website"). Delegating small fixes to Chris to create brain space. Paying personally for Claude Code on his desktop. Building Friday to manage cross-project chaos. Getting elevated IT access slowly (had to lie to IT to get WSL installed)
- **BenVH** — Referenced as extremely swamped. Chris already talked to him about database access. No update yet. His CI/CD pipeline with 939 tests per stage described as "amazing" by both — and Azmain credits him entirely for the infrastructure

## Open Questions Raised
- Does the database correctly handle date formats when browser locale differs (US MM/DD vs EU DD/MM)?
- When will Chris get prod database access from BenVH?
- Can Azmain/BenVH push for cloud development environments so developers don't need $5K laptops?

## Raw Quotes of Note
- "It's been four weeks, and you're an adult and it's 2026, I shouldn't have to teach you how to use a website. Just click around, dude." — Azmain, on CSM support requests during Portfolio Review
