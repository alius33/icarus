# Chat with Ben B
**Date:** 2026-01-14
**Attendees:** Ben Brooks, Richard Dosoo, Azmain Hossain
**Duration context:** Medium (~23 minutes)
**Workstreams touched:** WS2 (CLARA)

## Key Points
- Ben Brooks walks Azmain through the to-do list / whiteboard he has created for rapid iteration priorities on the main app.
- Key priority items identified: (1) User context -- wiring in who is on what teams so the app knows the logged-in user; (2) Edit permissions -- only team members on a project can edit it, with admin accounts for overrides; (3) Executive summary per account -- a free text field updated weekly showing current status, with a last-updated date.
- The executive summary idea was sparked by a real incident: Mike Steele emailed Ben asking why Gary Nelson at Travellers was upset, and the answer had been buried in a 50-slide deck months ago with no easy way to surface it.
- Azmain notes that this weekly update is the sole reason they still use RMS Salesforce -- CSMs put their weekly updates there. If CLARA captures this, it saves Stacy significant time.
- Ben wants migration-critical workflow flags on use cases so they can identify which are blocking migration. Also wants HD (High Definition models) tracking at the use case level -- whether HD is in production for a given use case -- because the current assumption that the market is using HD is wrong; nobody is actually using it in production because they are all blocked.
- Ben wants a burn-down chart for migrations by quarter showing outstanding customer count -- "that would be amazing for next week."
- Discussion of general page improvement: blocker pages are poorly laid out, action plan creation needs help guidance, and Ben wants Valpers cultural commitments terminology embedded into the app's language.
- Ben asks Azmain to get someone (solution architects, implementation leads) to review and flag migration-critical use cases.
- Natalia has been asking when the app will be deployed and usable.
- Ben emphasises: target is something presentable by Tuesday next week that shows a reasonable picture of the account base and adoption programme.

## Decisions Made
- Salesforce will receive data from the tracker (not the other way around) -- tracker is the entry point, data flows out -> Ben Brooks
- Focus on making the first landing page optimised for CSMs, not executives -> Ben/Azmain
- Migration-critical workflow flags and HD-enabled flags to be added to use case level -> Azmain
- Get external people (solution architects) to do migration criticality review -> Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Add user context / team member mapping | Azmain | Before Tuesday demo | Open |
| Add executive summary field per account with last-updated date | Azmain | Before Tuesday demo | Open |
| Add migration-critical workflow flag to use cases | Azmain | Before Tuesday demo | Open |
| Add HD-enabled flag at use case level | Azmain | Next iteration | Open |
| Get solution architects to review migration criticality data | Azmain | This week | Open |
| Improve blocker pages, action plan creation UX | Azmain | Ongoing | Open |
| Create burn-down chart for migrations by quarter | Azmain | Target: next week | Open |

## Stakeholder Signals
- Ben Brooks is laser-focused on making the app useful for the Tuesday demo. He is thinking about what will resonate with leadership (burn-down charts, migration visibility).
- Ben is frustrated that HD adoption is being assumed when in reality nobody is using it in production -- wants the tracker to expose this truth.
- Natalia is actively asking when the app will be deployed, signalling genuine interest and impatience.

## Open Questions Raised
- Where is the most up-to-date migration target date data? Azmain has the December golden source but dates have large gaps. Catherine owns this data.
- Who should be asked to confirm HD enablement status per use case?
- How should the tracker relate to Salesforce going forward? (Josh and Catherine reportedly trending toward abandoning Salesforce)

## Raw Quotes of Note
- "Until we show the fact that nobody's actually using it in production because everybody's bloody blocked, we won't do anything about the problem" -- Ben Brooks, on HD model adoption tracking
