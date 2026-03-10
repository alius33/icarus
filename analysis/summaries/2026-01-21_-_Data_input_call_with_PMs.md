# Data Input Call with PMs
**Date:** 2026-01-21
**Attendees:** Azmain Hossain, Vlad (PM), Diana (PM), one other PM (Speaker 1/2)
**Duration context:** Medium (~30 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Azmain demonstrates the new data input hub he built overnight using Claude — a dedicated section for PMs and CSMs to fill in missing data directly in the app rather than via Excel
- The data input hub shows per-account data completeness: colour-coded indicators of what is missing (CSM assignment, use case details, blockers, action plans)
- Logic: anything not green needs blockers to explain why; any blocker needs an action plan for resolution
- 155 active accounts loaded from the December golden source. Priority accounts still need to be identified by Ben/Natalia
- Vlad asks about timelines — Azmain says priority accounts need defining by end of today, then they can assign work across PMs based on availability
- Diana raises important questions: how to distinguish between services Moody's is leading vs monitoring; how to track project quality — Azmain acknowledges this is a PM-specific need not yet built
- The platform is designed to be CSM-focused first; PM section will come later as a structured addition
- No Excel export intentionally — forces users to stay in the platform rather than defaulting back to spreadsheets
- Audit trail exists for all changes (who, when, what)
- Vlad has three accounts (Mafra, Star, AIG) he can start populating immediately as quick wins

## Decisions Made
- Azmain to confirm critical accounts and priority fields with Ben/Natalia by end of day → Azmain
- PMs will split accounts based on availability once list is ready → All PMs
- No data export for now — intentional to change user behaviour → Azmain
- If CSMs are unavailable, escalate to their manager first, then to Natalia/Ben → PMs

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Get list of critical accounts from Ben/Natalia | Azmain | End of day 21 Jan | Open |
| Identify most critical fields to populate first | Azmain / Natalia | End of day 21 Jan | Open |
| Test data entry by editing a field on a known account | Vlad | Today | Open |
| Fix "region" field from free text to dropdown | Azmain | Soon | Open |

## Stakeholder Signals
- Vlad is practical and willing to help but wants clear scope and timelines before committing
- Diana is thinking about PM-specific needs (project tracking, service quality) — signals future requirements pressure on CLARA
- The PMs are cautiously positive but need hand-holding on what exactly to do

## Open Questions Raised
- How do we track quality of Moody's services within CLARA (PM perspective)?
- What happens if CSMs are unavailable before month-end deadline?
- What is the actual deadline for the data completeness push?

## Raw Quotes of Note
- "Buy-in is not optional. This is what they have to do." — Ben Brooks (relayed by Azmain), on CSM adoption of CLARA
