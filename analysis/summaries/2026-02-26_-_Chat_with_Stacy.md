# Chat with Stacy — Migration Dashboard and Scorecard Reporting
**Date:** 2026-02-26
**Attendees:** Azmain Hossain, Stacy Dixstra
**Duration context:** Short (~25 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Stacy scopes her reporting requirements for Andy Frappe's central migration dashboard. Banking has a full-time resource building a Power BI dashboard; insurance needs to feed into it.
- Key decision: monthly Excel export from CLARA is sufficient. No APIs, no automated feeds. Stacy will build a simple report, export it, and send it to the banking team for Power BI integration. This is pragmatic given how much is changing in CLARA.
- Azmain demos the reports functionality he built specifically with Stacy in mind, modelled exactly on Salesforce's report builder (choose data source, select columns, add related objects, export).
- Critical bug discovered: when a CSM manually updates a switch-off date, it is not overriding the golden source import date. Catherine found this discrepancy. Azmain has the fix ready to deploy.
- Reports functionality breaks when adding a second object (customer legacy products) -- needs debugging.
- Scorecard target: 34 legacy product switch-offs in 2026. But the target is built on shaky ground -- CSMs made up dates in December that are already shifting. Six clients already pushed out of 2026. Four retroactive wins discovered (products switched off years ago but never recorded).
- Strategic reporting decision: pace the reporting to match a linear trajectory against the 34 target. Do not reveal all wins early, or leadership will increase the target. Report wins on the exact week they should appear for a linear trajectory.
- Azmain proposes adding a "reported off date" field to capture retroactive wins credited to 2026 without falsifying actual dates in the system.
- Data cleanup ongoing: Stacy meeting with individual CSMs to clean up data quality. CSMs are nervous about deleting records. Gallagher is a mess in Salesforce, which carried over to CLARA.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Monthly Excel export from CLARA reports is sufficient for migration dashboard | Scope | High | Stacy / Azmain |
| Do not build APIs or automated feeds for Power BI at this time | Scope boundary | High | Stacy |
| Pace scorecard reporting to match linear trajectory against 34 target | Reporting strategy | High | Stacy |
| Add "reported off date" field for retroactive wins | Feature | High | Azmain |
| Fix date override bug before any exports are used for reporting | Quality gate | High | Azmain |

## Action Items
| Action | Owner | Deadline | Confidence | Status |
|--------|-------|----------|------------|--------|
| Deploy date override fix | Azmain | Today/tomorrow | High | Open |
| Add "reported off date" field to CLARA | Azmain | This week | High | Open |
| Fix reports bug when adding second object (customer legacy products) | Azmain | This week | High | Open |
| Notify Stacy when date fix is live so she can do clean export | Azmain | This week | High | Open |
| Continue individual CSM data cleanup meetings | Stacy | Ongoing | High | Open |
| Write requirements document for Power BI team using CLARA export format | Stacy | This week | High | Open |

## Theme Segments
1. **Migration dashboard requirements** (0:00-5:00) -- Andy Frappe's ask, banking's Power BI dashboard, Stacy scoping insurance data
2. **Reports functionality walkthrough** (5:00-12:00) -- Azmain demos Salesforce-style report builder, discovers object-add bug
3. **Scorecard politics and date integrity** (12:00-22:00) -- CSMs making up dates, retroactive wins, pacing strategy
4. **Date override bug and cleanup** (22:00-25:00) -- Catherine's discrepancy, fix deployment, CSM data nervousness

## Power Dynamics
- **Stacy is the political strategist for reporting.** Her decision to pace scorecard reporting to avoid target ratcheting shows sophisticated understanding of executive dynamics.
- **Azmain is the responsive builder.** Demos functionality built specifically for Stacy, commits to rapid fixes, proposes creative solutions (reported off date).

## Stakeholder Signals
- **Stacy Dixstra:** Political savvy about scorecard reporting. Doing the unglamorous work of individual CSM data cleanup meetings. Pragmatic about Excel over APIs. Worried about banking team's full-time dashboard resource -- "where do you guys get like" (the luxury).
- **Azmain Hossain:** Built reports feature with Stacy specifically in mind. Quick to identify and commit to fixing the date override bug. Creative problem-solver with the "reported off date" field.
- **Catherine (absent, referenced):** Found the date override discrepancy. In this context, her data quality attention is productive (unlike her chat complaints).
- **Andy Frappe (absent, referenced):** Wants all migrations on one central dashboard. Banking team has a full-time resource for Power BI. Insurance is apples to oranges (switch-offs vs pipeline).

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Azmain | Deploy date override fix | Stacy | High |
| Azmain | Add "reported off date" field | Stacy | High |
| Azmain | Fix reports second-object bug | Stacy | High |
| Stacy | Write Power BI requirements doc | Banking team | High |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of purpose | 5 | Stacy knew exactly what she needed |
| Decision quality | 5 | Pragmatic scope decisions, creative reporting strategy |
| Engagement | 4 | Good two-way collaboration |
| Follow-through setup | 5 | Clear actions with immediate timelines |
| Time efficiency | 4 | Efficient, minimal tangent |

## Risk Signals
- **Scorecard target of 34 is built on fabricated dates.** CSMs made up switch-off dates in December. Six already pushed out. Four retroactive wins discovered. The integrity of the migration tracking narrative is fragile.
- **Date override bug means exports are unreliable.** Manual updates not overriding golden source dates. Must be fixed before any reporting is credible.
- **Reports feature has a breaking bug** when adding a second object. Needs fixing before Stacy can self-serve.
- **Pacing strategy is risky.** Deliberately withholding progress to avoid target ratcheting could backfire if discovered.

## Open Questions Raised
- What does Andy Frappe actually want beyond the number? Will he want customer-level detail?
- How to handle the glass-to-EGL and access-to-access hosting migrations alongside Risk Link?
- When Diya meets Natalia tomorrow, will she add requirements to the reporting?

## Raw Quotes of Note
- "I don't even know how the number came about. Like, if they just were like, 34 sounds good." -- Stacy, on the scorecard target's origin
- "We're gonna take those as wins, even though they're false." -- Stacy, on retroactive switch-offs
- "Let's not tell anybody, because then they'll be like, 10 in two months at this trajectory, you'll be fantastic. Let's increase your target." -- Azmain, on pacing strategy

## Narrative Notes
This is the programme's unglamorous but critical data integrity conversation. Stacy's revelation that CSMs fabricated switch-off dates in December -- and that six clients have already been pushed out of 2026 -- undermines the entire scorecard narrative. The counter-revelation that four products were actually switched off years ago but never recorded provides a buffer, but the team's deliberate decision to pace reporting is a calculated risk. If leadership discovers they are withholding progress, trust erodes. If they report early, targets get ratcheted. Stacy navigates this dilemma with political skill. Meanwhile, the date override bug means the one system that should be the source of truth cannot be trusted for exports until the fix is deployed.
