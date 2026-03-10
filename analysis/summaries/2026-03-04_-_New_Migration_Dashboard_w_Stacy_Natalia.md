# New Migration Dashboard with Stacy and Natalia
**Date:** 2026-03-04
**Attendees:** Azmain Hossain, Stacy (Dixtra), Natalia (Plant)
**Duration context:** Medium (~25 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Meeting focused on redesigning CLARA's migration tracking to align with the insurance scorecard that Diya sees. The existing dashboard was causing confusion due to inaccurate numbers and unclear logic.
- First request: remove the grey box from the portfolio review page entirely. The zero numbers and priority account counts are inaccurate and confusing. People should be directed to the dashboard for real numbers, not the portfolio review page.
- Hosting Plus to be consolidated under Risk Link; RBO under Risk Browser. The scorecard only mentions "Risk Link" and "Risk Browser" -- showing separate Hosting Plus/RBO categories could cause confusion. A note will indicate what is included.
- Year-to-date actuals need to be added to the dashboard. Ten migrations completed YTD; forecast is 24 more (total 34, but they are saying 36 including the problematic four).
- New "Scorecard" tab requested on the management dashboard, showing quarterly migration view (actuals YTD + forecast by quarter). This becomes the default tab that Diya sees.
- Credibility risk identified: four accounts (QBE, ROI, La Previsora, Ms Transverse) had migration dates pre-2026 but are being counted in 2026 targets. Stacy is having "heart palpitations" about someone asking for client names and finding that these completed before 2026.
- Azmain proposed a "reported year of completion" field to handle the four accounts. After debate, a simpler approach was agreed: either hard-code the four accounts or temporarily expose the field for Stacy to update, then hide it.
- Natalia suggested not counting them at all -- "those are not 2026 migrations." This was the most honest position but potentially problematic because they have already been communicated as part of the target.
- Reports builder has filter logic bugs -- Natalia demonstrated that multiple filters (contains, does not contain) do not work correctly when combined. Chris to investigate.
- Chris's arrival on the team was welcomed by Natalia: "fantastic that we have you on board because Azmain will be able to have some sleep."

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Remove grey box from portfolio review page | UI change | High | Azmain |
| Consolidate Hosting Plus under Risk Link, RBO under Risk Browser | Data model | High | Stacy/Azmain |
| Add Scorecard tab as default on management dashboard | Feature | High | Stacy/Azmain |
| Defer decision on four pre-2026 accounts -- Stacy to investigate further | Deferred | Medium | Stacy |
| Reports filter bugs to be investigated by Chris | Bug fix | High | Chris |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Remove grey box from portfolio review page | Azmain | Today | Open | High |
| Consolidate Hosting Plus/RBO into Risk Link/Risk Browser categories | Azmain | This week | Open | High |
| Build Scorecard tab with quarterly migration view | Azmain | This week | Open | High |
| Add YTD actuals to dashboard | Azmain | This week | Open | High |
| Investigate four pre-2026 completed accounts | Stacy | Today | Open | High |
| Fix reports filter logic (multi-filter combinations) | Chris | This week | Open | Medium |
| Check with Catherine on analytics tab usage | Stacy | TBD | Open | Low |

## Theme Segments
1. **Portfolio review page cleanup** (0:00-4:00) -- Remove confusing grey box
2. **Product category consolidation** (4:00-8:00) -- Hosting Plus -> Risk Link, RBO -> Risk Browser
3. **Scorecard tab design** (8:00-14:00) -- Quarterly view for Diya, actuals + forecast
4. **Migration number credibility** (14:00-20:00) -- The four pre-2026 accounts dilemma
5. **Reports bugs and testing** (20:00-25:00) -- Filter logic issues, Chris onboarding acknowledged

## Power Dynamics
- **Stacy drives the requirements.** She is the data/reporting expert and knows what Diya needs. She articulates the ask clearly and pushes back on solutions that create risk.
- **Natalia is the honest broker.** She takes the most direct position: "those are not 2026 migrations" -- the most honest but politically uncomfortable stance.
- **Azmain is the implementer.** He offers technical solutions (fields, hard-coding) and defers to Stacy and Natalia on what the numbers should say.
- **Diya looms over the conversation.** Her confusion about dashboard numbers is the driving force for all these changes. She has been asking about the scorecard regularly.

## Stakeholder Signals
- **Stacy** -- Anxious about data credibility. Her "heart palpitations" about client names being questioned is genuine concern about executive-level scrutiny. She is the programme's quality conscience.
- **Natalia** -- Pragmatic and honest. Willing to say uncomfortable things ("those are not 2026 migrations"). Focused on what Diya needs and how to deliver it cleanly.
- **Azmain** -- Technically accommodating but defers on data decisions. Admits the migration calculation broke because they removed the completion status field. Ready to implement whatever is decided.
- **Ben Brooks** (mentioned) -- Told the team to count the four pre-2026 accounts. His "count them" instruction created the credibility risk.

## Commitments Made
| Who | Commitment | To Whom | Context |
|-----|-----------|---------|---------|
| Azmain | Remove grey box today | Stacy/Natalia | Portfolio review cleanup |
| Azmain | Build scorecard tab this week | Stacy/Natalia | Diya's reporting needs |
| Stacy | Investigate four pre-2026 accounts today | Natalia/Azmain | Credibility resolution |
| Chris | Fix reports filter bugs | Natalia/Azmain | Reports functionality |

## Meeting Effectiveness
| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 8 | Very specific UI and data requirements agreed |
| Decision quality | 7 | Good on technical changes; migration numbers deferred but flagged |
| Participation balance | 8 | All three contribute meaningfully from different angles |
| Action item specificity | 8 | Clear actions with today/this week timelines |
| Strategic alignment | 8 | Directly addresses Diya's scorecard needs |

## Risk Signals
- **HIGH: Migration number credibility.** Four pre-2026 completions counted in 2026 targets. If anyone asks for client names and cross-references dates, this falls apart. Ben Brooks said "count them" but Stacy and Natalia are uncomfortable.
- **MEDIUM: Dashboard calculation logic.** The migration numbers broke because a status field was removed. This suggests fragile calculation logic that is not well-understood by anyone including the developer.
- **LOW: Reports builder still buggy.** Multi-filter combinations do not work. This limits usefulness for power users like Natalia.

## Open Questions Raised
- Should the four pre-2026 accounts be counted as 2026 migrations or held as buffer?
- What analytics tab content should be kept vs removed?
- How does the scorecard tab relate to the broader Power BI migration dashboard Andy Frappe wants?

## Raw Quotes of Note
- "I'm having heart palpitations going if somebody asks for these names." -- Stacy, on the four pre-2026 migration accounts
- "Those are not 2026 migrations." -- Natalia, taking the most honest position on the credibility issue

## Narrative Notes
This meeting crystallises the programme's data credibility problem. The core tension: Ben Brooks has told the team to count four pre-2026 completions in the 2026 target, which inflates the number from ~32 to ~36. Stacy and Natalia are visibly uncomfortable with this. Stacy's concern is specific and legitimate -- if Mike Steel or Colin Holmes ever ask for the client names, someone will scratch their head and say "QBE shut down a year and a half ago." Natalia's response is the most honest: do not count them. The fact that this credibility risk exists at all reveals how the programme's reporting has evolved faster than its governance. The technical work (removing grey boxes, consolidating product categories, building the scorecard tab) is straightforward and will improve Diya's experience. But the number question is a governance issue, not a technical one, and it remains unresolved.
