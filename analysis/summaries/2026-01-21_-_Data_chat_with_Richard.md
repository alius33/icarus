# Data Chat with Richard
**Date:** 2026-01-21
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (briefly, in person)
**Duration context:** Long (~55 minutes)
**Workstreams touched:** WS2 CLARA (infrastructure, data), WS1 Training

## Key Points
- Richard discusses POC cost scoping — wants to reduce estimated cost by two-thirds and confirm with "Tim" that it is not production-level testing
- Azmain asks about "multiple migration heads" error in Alembic — they are both learning the system in real time
- Richard acknowledges the massive speed of feature delivery but warns about testing debt: the magnitude of changes demands more testing than they have been doing
- Discussion of using Claude Code's multi-agent capability — running parallel agents for dev, QA, and review simultaneously rather than using AI as "a glorified chat"
- Key concern from Azmain: data persistence when users start entering data. Richard confirms data is stored in AWS RDS within a VPC — only accessible via the API layer or Alembic migration scripts
- Critical rule established: from now on, any schema changes must ship with a data fix script to prime new tables/fields with data
- Richard starts a thread with Stephanie to get employee list data for the app, and raises an access request for Azmain to get AWS console access
- Discussion of Cursor token costs: someone burned through $750 in three days. Richard notes some people spending thousands
- Azmain describes his painful workflow for recording and transcribing meetings: records on Apple Watch, transfers to phone, uploads to Otter, then processes through Claude
- Richard mentions a call tomorrow with platform engineering about programmatic API access to LLMs
- Azmain has formally recognised the other five workstreams have had zero progress due to CLARA consuming all his time

## Decisions Made
- Any new schema changes must include data fix scripts in the Alembic migration → Azmain, Richard
- Deploy to production only at a weekly frequency once users are in the system → Richard, Azmain, BenVH
- Need to tie training programme back to OKRs and KPIs per group → Richard, Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Call Tim re POC cost scoping | Richard Dosoo | Tonight | Open |
| Start thread with Stephanie for employee data | Richard Dosoo | Today | Open |
| Raise AWS access ticket for Azmain | Richard Dosoo | Today | Open |
| Get employee list under Colin Holmes for the app | Azmain / Richard | This week | Open |
| Document Cursor best practices from hundreds of hours of use | Azmain | Ongoing | Open |

## Stakeholder Signals
- Azmain is stretched to breaking point — explicitly notes that all non-CLARA workstreams have stalled
- Richard is aware of the tech debt problem but continues to prioritise speed for the Monday deadline
- BenVH remains a single point of failure for infrastructure; his physical absence (racing in Amsterdam) causes real delays

## Open Questions Raised
- How to get meeting recording/transcription tools approved through Moody's security?
- How to establish multi-agent development workflows with Claude Code?
- When will Azmain get bandwidth to address the other five workstreams?

## Raw Quotes of Note
- "The amount of physical new features that we've shipped in the past couple like, that's that movie would take teams weeks to do." — Richard, on velocity of CLARA development
