# Review AI Powered Dashboards for Customer & Model Success Teams
**Date:** 2026-03-13
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (Ben Van Houten), Lucia (Customer & Model Success team), Joel (Customer & Model Success team), Bernard
**Duration context:** Medium (~27 minutes)
**Primary project:** CLARA (IRP Adoption Tracker)
**Secondary projects:** App Factory

## Key Points
- Meeting with the Customer & Model Success team (under Courtney) to demonstrate CLARA's capabilities and the App Factory hosting platform
- Lucia's team is facing a wave of dashboarding requests across multiple sub-teams; the Cape team specifically needs a Tableau replacement by September 2026 (Tableau being sunsetted)
- Richard walked through CLARA as a case study of how the team built a full application from an LLM-assisted approach, emphasising the blocker analysis and Salesforce integration pipeline
- BenVH presented the App Factory MCP server architecture: a central platform where any app can request data access, LLM workers, and authentication — non-technical users just ask the MCP server for what they need
- Joel clarified his involvement is more around Matt Allen's resource allocation and case management work than IRP Navigator; he's working with Pat's team while Matt is on paternity leave
- Lucia confirmed the team uses R and Streamlit for dashboarding currently, with no desire to continue with Power BI — prefers custom solutions
- Lucia and Joel both offered to help test Salesforce integration when ready (both have Salesforce access) — first external test volunteers for the pipeline
- Azmain revealed that Diana's team has a painful monthly file-collection and dashboard-creation workflow that Friday (PM app) will address; Lucia's team has already automated the data cleaning step in R
- Lucia maintaining a Confluence page with notes on dashboarding needs; will share with Carlin (who would be very interested in App Factory)
- BenVH noted App Factory documentation is still in progress — he's heads down on the MCP server and many teams want their apps hosted
- Richard proposed sending standardised Cursor rules files so any dashboard apps built are consistent and deployable on App Factory
- Next steps: Lucia to gather requirements from Carlin and Courtney, Azmain to follow up in 1-2 weeks

## Decisions Made
- Customer & Model Success team to join App Factory pipeline for dashboard hosting → Richard/BenVH
- Manual Salesforce data exports as interim until programmatic access granted → Richard
- Lucia's team to serve as early Salesforce integration testers → Lucia/Joel

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Share CLARA presentation slides and App Factory overview with Lucia's team | Richard | Next week | Open |
| Gather dashboard requirements from Carlin and Courtney's priorities | Lucia | 2 weeks | Open |
| Follow up with Lucia's team on dashboarding collaboration | Azmain | 1-2 weeks | Open |
| Create App Factory documentation/Confluence page | BenVH | TBD | Open |
| Share Confluence notes on dashboarding requirements with team | Lucia | Immediate | Open |
| Send standardised Cursor rules file for consistent app development | Richard | TBD | Open |

## Stakeholder Signals
- **Lucia** — Engaged and proactive. Immediately saw the value of App Factory as a solution to her team's hosting problem. Offered Salesforce testing help unprompted. Has good data governance instincts (maintained Confluence docs, clean data processes). A natural ally for programme expansion.
- **Joel** — Currently filling in for Matt Allen. Less directly involved in the IRP track but engaged on the Salesforce/case management front. Cooperative.
- **BenVH** — Confident when presenting App Factory architecture. Transparent about documentation gaps and current workload. His vision for the MCP server resonated immediately with Lucia's needs.
- **Azmain** — Connecting dots across teams (Diana's reporting workflow, Lucia's dashboarding, Friday's capabilities). Honest about his bandwidth constraints ("I might go radio silent for a bit").

## Open Questions Raised
- How many dashboards does the Customer & Model Success team actually need, and are they one app with many pages or separate apps?
- Can the App Factory MCP server connect to Power BI as a downstream consumer?
- What is the timeline for Cape team's Tableau replacement (September 2026 deadline)?

## Raw Quotes of Note
- "Is your goal to kind of create a path for various data accesses?" — Lucia, immediately grasping the App Factory value proposition
