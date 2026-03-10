# Tracker Stand Up
**Date:** 2026-02-20
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (Speaker 1)
**Duration context:** Short (~16 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Ben (Brooks) has dropped a surprise: he's meeting Andy Frappe (President of Moody's Analytics, one below the board) on Monday to demo CLARA. Richard and Azmain are scrambling to prepare.
- Critical data issues discovered: (1) Orphan records causing API failures, (2) Duplicate customer accounts created during the golden source data import -- happened only in production, not in dev/staging.
- Azmain discovers the blockers page was making 60+ individual API calls (one per action plan ID). He optimised this to a single batch query -- a significant performance fix.
- The team discusses the duplicate account problem. Richard proposes a soft-delete approach: add an inactive/dead status flag rather than hard-deleting records, which is safer and allows reconciliation later.
- BenVH will take a snapshot of production and restore it to staging so Azmain and Richard can test the fix safely before deploying to production on Monday.
- Richard raises the need for a proper regression test suite and performance testing using agents to simulate CSM usage at various throughput levels. Currently there's no systematic testing.
- Richard also mentions Idris (banking equivalent) wants to demo to his senior leadership and has been talking up the team's work -- they feel obligated to deliver his app.
- Richard suggests BenVH could visit the UK, offering to get Ben (Brooks) to approve travel.

## Decisions Made
- Use soft-delete approach for duplicate records rather than hard-delete -> Richard / Azmain
- BenVH to snapshot production and restore to staging for safe testing -> BenVH
- Fix to be tested Monday morning, deployed to prod before Andy Frappe demo -> Azmain / Richard
- Regression test suite to be set up as a Monday priority -> Richard / Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Snapshot production database and restore to staging | BenVH | Tonight (20 Feb) | Open |
| Implement soft-delete status for duplicate accounts | Azmain / Richard | Monday 23 Feb | Open |
| Deploy blocker page API optimisation (60 calls -> 1) to prod | Azmain | Monday 23 Feb | Open |
| Set up regression test suite and performance testing | Richard / Azmain | Next week | Open |

## Stakeholder Signals
- Richard is visibly alarmed by the Andy Frappe demo timing -- highest-stakes audience yet, with data quality issues still unresolved.
- Azmain is problem-solving efficiently under pressure, finding and fixing the API performance issue quickly.
- BenVH is collaborative and offers the right technical solution (database snapshot for safe testing).

## Open Questions Raised
- What time is Ben's meeting with Andy Frappe on Monday? (Need to know the hard deadline)
- Why did the import create duplicate records only in production and not in staging?
- When will the standardised data import process be built to prevent recurrence?

## Raw Quotes of Note
- "He's meeting with Andy fucking -- sorry, I'm swearing -- he's meeting with Andy Frappe on Monday to demo Clara." -- Richard Dosoo, on the surprise escalation
