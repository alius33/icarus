# Life Side SLT
**Date:** 2026-03-03
**Attendees:** Ben Brooks, Richard Dosoo (Speaker 1), Azmain Hossain, Christophe (Speaker 3), Jack (Speaker 5), Jason (Speaker 4), Alexandre (Speaker 2), Michelle (mentioned)
**Duration context:** Medium (~30 minutes)
**Workstreams touched:** WS2 CLARA, WS1 Training (tangential)

## Key Points
- This is a presentation of CLARA to the Life Side Senior Leadership Team, following a prior demo at the Insurance SLT meeting. Christophe invited the team to understand both the tool and the process of building it.
- **Ben Brooks gave the origin story**: Described the journey from dashboarding attempts in late 2025, discovering Cursor in November, building three iterations over Christmas week, realising the problem was data visibility (not dashboard quality), and pivoting to a system of record.
- **Richard demoed CLARA live**: Showed Azure AD authentication, role-based access control, portfolio summary, individual account views (e.g., AJ Gallagher), use case tracking with target dates, blocker management tied to use cases, action plans for remediation, and the portfolio review dashboard that replaced PowerPoint slides.
- **Key capability highlighted**: Using blockers with LLM integration (Copilot or other models) to identify themes, consistent blockers across the portfolio, and recommend strategies for maximum ROI on unblocking efforts.
- **Life team interest**: Jack asked about data security and hosting -- Richard confirmed they solved authentication via TSG Azure tenant integrated with AWS. Jack sees this as a reusable pattern across the organisation.
- **Gainsight positioning**: Jack compared CLARA to "Gainsight on steroids." Richard explicitly cautioned against this framing, stating CLARA is complementary to Gainsight, not a replacement. It serves a function Gainsight currently cannot deliver on their timeline.
- **Azmain proposed a template approach**: Strip out IRP-specific elements, turn CLARA into a flat-pack IKEA-style template that other teams (like Life) could deploy for their own migration/adoption tracking needs.
- **Life team use cases identified**: Jason mentioned pay-as-you-go glass conversion, key floor targeting, renewal tracking, hosting conversion. He emphasised data should flow back to Salesforce to avoid multiple instances.
- **Alexandre** (who has been tracking CLARA's development) highlighted the speed of development as the most impressive aspect -- Azmain can fix things in real-time during meetings using natural language prompts.
- **API integration vision**: Azmain described offering clean data to Gainsight/Salesforce via APIs, positioning CLARA as having done the data migration/cleanup work that Gainsight would have had to do anyway.

## Decisions Made
- Life team to be given read access to CLARA to explore -> Richard/Azmain
- Richard to set up infrastructure walkthrough with Jack -> Richard
- CLARA to be positioned as complementary to Gainsight in all communications -> Team agreement

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Share CLARA link with Life SLT for read-only exploration | Azmain/Richard | Immediate | Open |
| Set up infrastructure walkthrough with Jack | Richard | Next week | Open |
| Share slides and prompting/design process documentation | Richard | TBD | Open |
| Explore template approach for Life team migration tracking | Azmain | TBD | Open |

## Stakeholder Signals
- **Jack** is technically curious and sees the reusable infrastructure pattern as the key value. Asked the right questions about data security.
- **Jason** wants practical tracking tools for renewals and conversions but is concerned about data living outside Salesforce. Pragmatic perspective.
- **Alexandre** has been quietly following CLARA's development and is impressed by the speed. Specifically highlighted the real-time development capability.
- **Christophe** is open to adopting similar tools for Life team but wants to understand the end state and how it fits with Gainsight.
- **Ben Brooks** continues to push the narrative that the cost of getting things wrong is near zero with these tools -- encouraging experimentation over perfection.

## Open Questions Raised
- Does the Life team need a similar tool for their Axis Cloud and EGL deployments?
- What would a CLARA template look like stripped of IRP-specific elements?
- How would data flow back from custom apps to Salesforce/Gainsight?
- What is the long-term end state for CLARA relative to Gainsight?

## Raw Quotes of Note
- "The cost of getting this stuff wrong is practically zero in this working context. So we shouldn't be afraid of screwing stuff up and chucking it away and starting over." -- Ben Brooks, on the development philosophy
