# New Migration Dashboard with Stacy and Natalia
**Date:** 2026-03-04
**Attendees:** Azmain Hossain, Stacy (Dixtra), Natalia (Plant)
**Duration context:** Medium (~25 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- **Dashboard confusion cleanup**: The grey box on the portfolio review page showing priority account metrics is inaccurate and confusing. Stacy requested it be removed entirely -- migration numbers should only appear on the dedicated management dashboard. Azmain confirmed this is a quick removal.
- **Hosting Plus and RBO consolidation**: The scorecard only references "Risk Link" and "Risk Browser." To avoid confusion, Hosting Plus numbers should roll up under Risk Link, and RBO numbers under Risk Browser, with a footnote explaining the inclusion. Azmain confirmed this can be done in the backend.
- **Scorecard tab request**: A new "Scorecard" tab is needed on the management dashboard showing quarterly migration view (actuals year-to-date + forecast by quarter). The existing annual view stays on the current tab. Stacy wants the scorecard tab to become the default landing page for the management dashboard, as Diya checks it regularly.
- **Completed migration accounting problem**: There are 10 completed migrations year-to-date, but 4 of them (QBE, ROI, La Previsora, Ms Transverse) were technically completed before 2026. They were on the 2026 target list and counted in the 36 forecast, but their actual switch-off dates were pre-2026. This creates a credibility risk if anyone asks which specific clients migrated.
- **Proposed solution debate**: Azmain proposed a "reported year of completion" field that auto-fills for future completions but can be manually set for legacy ones. Natalia pushed back, calling it "a bit like hard coding" and questioned whether it was worth the complexity for just four accounts. Stacy was concerned it would raise confusing questions if visible to users.
- **Compromise approach**: Stacy will dig deeper into each of the four accounts today. RLI can be adjusted (12/31/25 to 1/1/26 -- one day difference). The others need more investigation. Azmain offered to either hard-code the four accounts in the backend or use a temporary hidden field.
- **Natalia's priority**: Getting the confusing counter off the portfolio review page is urgent because Diya asks about it regularly and gets confused by discrepancies.
- **Reports feature testing**: Azmain asked Stacy to test the reports builder, as she understands Salesforce reports and that is the model CLARA is cloning. Natalia tried building a report but encountered filter logic issues (multiple filters did not work as expected -- could not exclude "Exposure IQ" while including "TIQ" and "UIQ").
- **Bug fix workflow**: Chris will work on bugs and features. Azmain and Chris will have a session tomorrow to go through the issues. Azmain's goal is to get fixes done by Friday for the Monday call.
- **Chris onboarding acknowledged**: Natalia expressed relief that Chris is on board, saying Azmain will finally be able to get some sleep.

## Decisions Made
- Remove grey box from portfolio review page immediately -> Azmain
- Hosting Plus rolls into Risk Link, RBO rolls into Risk Browser (with footnote) -> Azmain
- New scorecard tab on management dashboard (quarterly view, actuals + forecast) -> Azmain
- Scorecard tab to be default landing page for management dashboard -> Azmain
- Stacy to investigate the four legacy completion accounts before deciding approach -> Stacy
- Bug fixes prioritised for completion by Friday -> Azmain/Chris

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Remove grey box from portfolio review page | Azmain | Immediately | Open |
| Roll Hosting Plus into Risk Link, RBO into Risk Browser | Azmain | This week | Open |
| Build scorecard tab with quarterly view on management dashboard | Azmain | This week | Open |
| Make scorecard tab the default on management dashboard | Azmain | This week | Open |
| Investigate the four legacy completed migrations (QBE, ROI, La Previsora, Ms Transverse) | Stacy | Today | Open |
| Test reports builder and provide feedback | Stacy | TBD | Open |
| Fix report filter logic (multiple filters, dropdown options) | Chris/Azmain | This week | Open |
| Send screenshot of analytics elements to remove | Stacy | TBD | Open |
| Check with Catherine on analytics tab usage | Stacy | TBD | Open |

## Stakeholder Signals
- **Stacy** is deeply concerned about data accuracy and credibility. She is having "heart palpitations" about the possibility of someone asking for specific migration client names and discovering pre-2026 completions counted as 2026. She is the programme's data conscience.
- **Natalia** is pragmatic -- she would rather not count the four legacy accounts at all than risk credibility damage. She is focused on what Diya needs and wants the scorecard confusion resolved quickly.
- **Azmain** is stretched but responsive. He can make immediate changes (removing the grey box) and is thoughtful about solutions (the "reported year" field approach) even if they get pushback.
- **Diya** (not present) is checking the dashboard regularly and getting confused by discrepancies -- this is creating urgency.

## Open Questions Raised
- How to properly account for the four pre-2026 completions without credibility risk
- Why the dashboard shows 24 when Stacy counted 26 in the raw data
- Which analytics tab elements should be removed vs kept
- How to fix the report filter logic for complex multi-condition queries

## Raw Quotes of Note
- "I'm sitting here going, like, having heart palpitations going if somebody asks for these names." -- Stacy, on the credibility risk of counting pre-2026 completions
