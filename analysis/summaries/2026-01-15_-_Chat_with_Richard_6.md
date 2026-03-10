# Chat with Richard 6
**Date:** 2026-01-15
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (Van Houten), Ben Brooks (briefly)
**Duration context:** Long (~49 minutes)
**Workstreams touched:** WS2 (CLARA), WS3 (Customer Success Agent), WS4 (Friday/Adoption Charter), WS6 (Build in Five)

## Key Points
- Post-demo debrief and planning session. Richard summarises the demo feedback: Stacy engagement is good, but Liz raised a critical point -- Josh and George need to provide feedback before Stacy starts pushing data entry to CSMs. Without their buy-in first, they will feel sidelined.
- Richard outlines the broader programme structure for the first time in detail to BenVH: six projects total. WS2 (CLARA/tracker) and WS4 (adoption charter) are being merged into one app. WS3 (CS Agent) is separate -- may be Copilot Studio or may pivot. WS6 (Build in Five) is Martin's app, which Ben Brooks wants kept separate from the tracker. They need to engage Idris (banking), Catherine, Kevin, and Alexandra for cross-functional input.
- BenVH explains the database migration problem in detail with a diagram: local development uses Alembic to manage schema changes, but these migrations are not being applied to the production database. He is building the automation to fix this. Until then, schema changes in local development cause deployment errors.
- Significant discussion about demo mode implementation. BenVH recommends against storing demo data in the database (flag overhead, cursor forgetting the flag in new contexts). Instead, he proposes using a static JSON file that mirrors the schema -- demo mode displays JSON data on the front end without touching the database. When demo mode is off, real database data flows through. CRUD operations are disabled in demo mode with a notification.
- BenVH creates a database schema markdown file as a shared source of truth that all developers can reference.
- Azmain raises a question about blockers vs action plans hierarchy -- Richard defers to Natalia, Diana, and Stacy for proper PMO structure on how to capture action items, blockers, issues, and risks.
- Richard is out Friday. BenVH flies to Amsterdam Friday evening for HighRox. Monday is MLK Day (US holiday). Josh may only be available Friday (before Monday holiday), complicating feedback timing. George and Josh feedback sessions pushed to Friday/Monday.
- Richard plans to document the five project workstreams with stakeholders, RACIs, and milestones in a spreadsheet tomorrow morning before he is unavailable.

## Decisions Made
- Demo mode will use static JSON files, not database flags -- CRUD disabled in demo mode with notification -> Azmain/BenVH
- BenVH to create database schema markdown file as shared source of truth -> BenVH (done in call)
- Get Josh and George feedback before rolling out to CSMs -- Liz's critical advice -> Richard/Azmain
- Martin's Build in Five app will need its own database within the same RDS instance -> BenVH to handle next week
- Richard to document all six workstreams with stakeholders/RACI/milestones -> Richard (tomorrow morning)

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Implement demo mode using static JSON (not database) | Azmain | This week | Open |
| Complete database migration automation | BenVH | Tonight | Open |
| Get feedback from Josh Ellingson | Azmain/Richard | Friday 16 Jan | Open |
| Get feedback from George Dyke | Azmain/Richard | Monday 19 Jan or later | Open |
| Document six workstreams with stakeholders/RACI/milestones | Richard | Tomorrow morning | Open |
| Set up Martin's Build in Five app with separate database | BenVH | Next week | Open |
| Add blocker-action plan hierarchy per PMO best practices (consult Natalia/Diana/Stacy) | Azmain | TBD | Open |

## Stakeholder Signals
- Liz's warning about Josh feeling sidelined is significant -- stakeholder management is critical for CSM rollout. Josh and George must be brought in before CSMs start using the tool.
- BenVH is thinking ahead (multiple environments, intake form for new apps) and is pragmatic about the migration automation timeline.
- Richard is stretched thin -- managing programme governance, stakeholder relationships, and hands-on development mentoring simultaneously.

## Open Questions Raised
- How will Martin's Build in Five app be deployed? Same infrastructure but separate database.
- When exactly will Josh and George provide feedback? Timing is tight with Friday departures and Monday US holiday.
- What is the proper PMO hierarchy for blockers, action items, action plans, issues, and risks?

## Raw Quotes of Note
- "Make sure you spend a good amount of time with George and Josh... there's definitely hints of him feeling a bit sidelined" -- Liz (via Richard's relay), on Josh Ellingson's positioning
