# Tracker Discussion with Josh
**Date:** 2026-02-05
**Attendees:** Richard Dosoo (Speaker 1), Azmain Hossain, BenVH (Speaker 2/3), Martin Davies (Speaker 4)
**Duration context:** Long (~33 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Richard spoke to Josh and Catherine the previous night — relay of their feedback to the team
- Key data issue: action plans not migrated. Azmain clarified that next steps data IS in the database but isn't being surfaced in the frontend — needs a UI fix
- Design disagreement: Josh/Catherine want every blocker to automatically generate an action plan with one action item ("path to green"). Azmain argues this creates bloatware — every blocker would have a single-line action plan, not a structured plan.
- Ben Brooks aligned with Azmain: Josh isn't thinking structurally, just wants it to look like Salesforce
- Separate data issue: product adoption table has duplicate rows — same use case appearing multiple times with different PAT (Product Adoption Tracking) numbers. Salesforce stores all historical rows but only displays the latest. Import needs to aggregate and keep only the latest row per product per customer.
- BenVH has direct database access now — can run queries and stored procedures to clean duplicate data
- Azmain's plan: address Josh/Catherine's feedback items, then focus on Natalia's portfolio review redesign — both must be done before Monday
- Martin properly briefed on Build in Five: two things — internal productivity framework and external client-facing demo capability
- Richard assigned Martin to work with Azmain on scoping Build in Five, create a skeleton project plan before Martin's holiday
- Discussion of the cross-OU AI session from yesterday — BenVH noted Amanda's tool lacks authentication, which is a concern for any tool storing Moody's data
- Azmain observed that non-developers building AI tools don't think about UX, security, or scalability — a recurring pattern that Build in Five needs to address with guardrails
- BenVH's vision: a project management conversation step before app creation, producing HTML mockups before any real code — ensures requirements are captured properly

## Decisions Made
- Next steps data to be surfaced in the blocker view UI — fix the frontend → Azmain
- Duplicate product adoption rows to be cleaned — keep only latest per product per customer → BenVH/Azmain
- Action plans stay as designed (structured plans, not auto-generated from blockers) — push back on Josh → Azmain to communicate
- Build in Five scope to be drafted Mon-Tue by Martin/Azmain → Team

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Surface next steps data in blocker frontend view | Azmain | Before Monday | Open |
| Clean duplicate product adoption rows in database | BenVH/Azmain | Before Monday | Open |
| Communicate action plan design rationale to Josh | Azmain | Today | Open |
| Apply Natalia's priority/tab changes to portfolio review | Azmain | Before Monday | Open |
| Draft Build in Five skeleton project plan | Martin/Azmain | Mon-Tue next week | Open |
| Make app responsive/mobile-friendly | BenVH | Background task | Open |

## Stakeholder Signals
- Josh and Catherine continue to push for Salesforce-like behaviour — they want the familiar, not the improved. Azmain's frustration is growing but he's choosing diplomacy.
- Martin is now properly oriented — understanding the full programme scope for the first time
- BenVH raised a critical observation about Amanda's tool: non-developers building with AI don't think about authentication, UX, or governance. This validates the need for Build in Five guardrails.
- Richard is playing the strategic layer while Azmain executes tactically — both are needed but the load is unsustainable

## Open Questions Raised
- Will Josh accept the action plan design as-is, or will this become a larger conflict?
- How to handle the data quality issues that originated in Salesforce's own messy records?
- What is the right level of prototyping before Build in Five generates real apps?

## Raw Quotes of Note
- "I don't know how many times you can tell the same thing to people, especially the person that gave you the data" — Azmain (referenced in debrief), on Josh/Catherine's pushback on data they themselves provided
