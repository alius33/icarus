# Salesforce Integration Design
**Date:** 2026-03-11
**Attendees:** Azmain Hossain, BenVH, Richard Dosoo, Kathryn Palkovics
**Duration context:** Medium (~21 minutes)
**Primary project:** CLARA
**Secondary projects:** App Factory, Program Management

## Key Points
- Architecture decision: App Factory MCP server acts as middleware for all Salesforce integration. CLARA, Friday, and any future app consuming Salesforce data connects through this single integration point rather than point-to-point integrations
- BenVH explained: the MCP server is essentially a middleware API layer. Any app calls the MCP server, which handles Salesforce connectivity. This allows the integration to be built once and consumed by all
- Key decision: Salesforce integration is one-way only (read, no write back). Azmain argued that pushing data to Salesforce opens a "huge can of worms" given unknown Salesforce data structure
- Kathryn Palkovics joined and asked the critical framing question: what exactly are we building? She wanted to understand the specific use cases, not just the objects
- Four groups of people the Salesforce integration must solve for:
  1. **Bernard** — Customer sentiment analysis from real-time ticket information (cannot get this from Gainsight because it's not as up-to-date)
  2. **Courtney Spillers** — HD adoption blockers from support cases (2,000-3,000 cases)
  3. **Kevin Pern** — Ticket information plus possibly User Voice data
  4. **Azmain/CLARA** — Blocker intelligence synced from Salesforce
- Key Salesforce objects needed: Cases and Case Feed (not accounts, contacts, or success criteria — those go to Gainsight)
- Kathryn Palkovics clarified the CLARA/Gainsight relationship: CLARA is for IRP adoption/migration (interim), ongoing CSM activity goes to Gainsight. The App Factory approach makes sense because it pulls data from multiple sources for unique analytics
- Gainsight goes live March 30 (hard launch, confirmed by Kathryn Palkovics). Azmain concerned about immediate "does Clara sync with Gainsight?" questions
- Kathryn Palkovics reassured: no IRP adoption info expected in Gainsight at launch — it's for day-to-day CSM activities only
- Kathryn Palkovics raised NPS data as a potential addition — Voice of Customer surveys currently feed into Gainsight, could be brought directly into App Factory
- Rhett has been working on ticket and User Voice analysis independently — Kathryn Palkovics flagged potential duplication
- Next steps: Richard to tidy the design document, Azmain to align MCP approach with latest thinking, Kathryn Palkovics to share with wider team for tomorrow's meeting (Gainsight integration meeting)

## Decisions Made
- Salesforce integration one-way only (read, no write back) → All agreed
- Key data objects: Cases and Case Feed only (phase 1) → Richard/Kathryn Palkovics
- App Factory MCP server as the single integration middleware for all Salesforce-consuming apps → BenVH/Richard
- Gainsight API integration as phase 2 (after Salesforce cases) → Richard
- New account creation flow: auto-trigger from Gainsight when new client signed, with approval step in CLARA → Kathryn Palkovics/Azmain
- NPS data integration to be explored as future enhancement → Kathryn Palkovics suggestion

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Tidy Salesforce integration design document | Richard | Today (11 Mar) | Open |
| Align MCP approach with latest thinking (update design) | Azmain | Today (11 Mar) | Open |
| Share updated design with wider team for tomorrow's Gainsight meeting | Kathryn Palkovics/Richard | 11 Mar | Open |
| Check with Courtney and Kevin on specific data needs from Salesforce | Richard | Before tomorrow's meeting | Open |
| Follow up with Rhett on ticket/User Voice analysis to avoid duplication | Richard | This week | Open |
| Explore NPS/Voice of Customer data integration into App Factory | Richard/Kathryn Palkovics | TBD | Open |
| Investigate Gainsight API for new account auto-sync trigger | Azmain | After March 30 launch | Open |

## Stakeholder Signals
- **Kathryn Palkovics** — Most engaged she's been with the programme. Her question about philosophy ("is the App Factory a platform for analytics from multiple sources?") showed she grasps the strategic vision. Called the approach "breaking down siloed walls" — now a strong ally, not the potential detractor flagged earlier
- **BenVH** — Articulate about the MCP server architecture as middleware. Clear and confident in the technical direction
- **Azmain** — Pragmatic about Salesforce complexity. Rightly concerned about the Gainsight launch creating pressure. Aware of timeline risk
- **Richard** — Driving the strategic framing: the programme's original requirement #1 was getting real-time customer data to CS teams (Bernard, Kevin). Everything else grew from that

## Open Questions Raised
- Should CLARA auto-create new client records when triggered by Gainsight, or keep that manual?
- What format does Bernard need for customer sentiment analysis?
- Does Courtney need real-time ticket data or periodic extracts?
- How do we avoid duplicating Rhett's ticket/User Voice analysis work?
- Should NPS data come from Gainsight or directly from the Voice of Customer team?

## Raw Quotes of Note
- "It essentially breaks down the siloed walls, and that's going to be huge." — Kathryn Palkovics, on the App Factory approach to multi-source analytics
