# Clara Feedback Cadence
**Date:** 2026-03-12
**Attendees:** Azmain Hossain, Natalia Plant, Stacy Dixtra, Catherine
**Duration context:** Medium (~29 minutes)
**Primary project:** CLARA (IRP Adoption Tracker)
**Secondary projects:** Program Management

## Key Points
- Meeting called by Natalia Plant to establish governance over Clara feature requests and releases — she described being "lost" by the volume of recent changes
- Stacy explained the rush: monthly report needed correct numbers, plus ISLT preparation. Expects the rapid-fire pace to stop going forward
- Clara officially transitioning from Build Mode to Maintenance Mode
- Moving to structured fortnightly release cycle with Tuesday review meetings for prioritisation
- Chris maintaining a feedback Excel tracking all requests and their status. Working through them properly (plan, build, test, push)
- Two grads arriving April 7 — one in London, one in New York — 100% dedicated to Clara maintenance. Azmain interviewing them now.
- Until April 7, proposed release schedule: skip next week, release on 27 March, then grads take over
- Ben Brooks governance concern: he bypasses the process by building things himself. Agreed solution: Ben can use the sandbox freely but must not push to user-facing production
- ISLT next week will use Clara directly (no slides) except for AIG. Scorecard tab in management dashboard is ready for this.
- Analytics tab to be removed from management dashboard — confusing for Diya if she clicks around
- Management dashboard and Portfolio Review to be moved higher in sidebar navigation (above reports/playground)
- Validation check agreed: CSMs cannot mark a use case as "complete" if the software status fields are still open. Not automated — a blocking check that forces them to update software status first.
- Navigation UX fix needed: back button loses scroll position, forcing users to scroll from top after viewing a record. Azmain to fix.
- Software status counting bug fixed: Risk Link Off + Hosting Plus Off were being counted as one instead of two
- Catherine raised feature governance concern about changes being made without wider review or consideration of downstream effects
- Natalia acknowledged no formal product manager or release notes process exists — not enough manpower. But proposed a weekly governance review as first step.

## Decisions Made
- Skip next week's release entirely → next release 27 March
- Tuesday prioritisation review meetings starting next week (Azmain, Natalia, Stacy, Catherine)
- Fortnightly release cadence going forward (at least until grads join and things stabilise)
- Ben Brooks can use sandbox but not push to production outside the release cycle
- Analytics tab to be removed from management dashboard
- Management dashboard moved higher in sidebar navigation (before Monday's ISLT)
- Use case completion check: software status must be "in production" before use case can be marked complete
- Catherine/Stacy to have visibility into the feedback request list for governance
- Azmain to fix back-button scroll position issue

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Give Catherine/Stacy/Natalia access to the feedback request list | Azmain | Before Tuesday | Open |
| Get Chris's feedback Excel with status of all items | Azmain | Before Tuesday | Open |
| Add priority field to feedback form | Azmain | Before Tuesday | Open |
| Set up Tuesday prioritisation review meeting (recurring, fortnightly) | Natalia | This week | Open |
| Move management dashboard and portfolio review higher in sidebar | Azmain | Before Monday ISLT | Open |
| Remove analytics tab from management dashboard | Azmain | Next release (27 Mar) | Open |
| Implement use case completion check (block if software status not complete) | Chris | Next release (27 Mar) | Open |
| Fix back-button scroll position loss | Azmain | TBD | Open |

## Stakeholder Signals
- Natalia Plant: clearly stepping into governance role. Concerned about Azmain's bandwidth. Wants structured process before ISLT.
- Stacy: pragmatic — explains why the rush happened, acknowledges it cannot continue. Wants proper cadence. Will use Clara live at ISLT on Monday.
- Catherine: raising valid governance points (unintended downstream effects from changes) but tone is monitoring/controlling. Referenced a removed field that broke dashboard calculations.
- Azmain: relieved about grads joining April 7. Candid about not being a front-end or back-end engineer. Focused on getting through the next 3 weeks.

## Open Questions Raised
- Should completed use cases auto-update software status, or is the check/block approach sufficient?
- What happens when Ben Brooks builds something in sandbox that the team doesn't want in production?
- How will release notes be communicated without dedicated product management resource?
- Is the Canada Life request (already migrated customer record) something the team wants to maintain?

## Raw Quotes of Note
- "We've proven even last week that we went through and said, oh this isn't right, and it's just because you mess up one thing, you start messing up the logic" — Stacy, on the risks of rapid releases
