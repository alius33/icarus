# WS6: Build in Five (Cursor for Pipeline Sales)

## Overview

Build in Five is a framework for building demo applications on IRP's Risk Data Lake using Cursor during customer conversations. The core concept: a salesperson or CSM sits with a customer, and within five minutes can construct a working application that demonstrates the power of the IRP platform -- pulling real model data, visualising portfolios, and showing what is possible with Moody's data and APIs.

The workstream has two distinct tracks:
1. **Customer-facing / pre-sales tool** -- The primary focus. A modular UI where users can drag and drop IRP API modules (location, windstorm, hurricane, etc.), load dummy portfolios, and instantly generate dashboards showing Moody's data. This is what Martin Davies is building.
2. **Internal app factory pipeline** -- The backend infrastructure for taking locally-built prototypes and deploying them through the app factory. BenVH (Ben Van Houten) and Nicole are handling this separately.

The name "Build in Five" captures the aspiration: demonstrate to customers that modern AI-assisted tooling means they can reimagine their workflows and get to working solutions dramatically faster than 12 months ago.

## Status (as of 9 March 2026)

**ACTIVE -- Demo targeting exceedance event (originally March 21, now potentially May)**

Key developments from March transcripts:
- The **exceedance event timeline has shifted**. Originally targeting March 21 for a demo, but on 4 March Richard explained that while Ben's speaking panel at exceedance is in May, the content must be agreed and reviewed by April. Richard told Ben: "I'm not sure that exceedance timelines will work" and that Martin's estimates need review.
- Martin is **actively developing** the customer-facing pre-sales tool. He showed Azmain his prior Apollo dashboard work on 3 March -- a fully functional portfolio analysis dashboard with EDM data, country/peril breakdowns, and risk modeller integration. This serves as the reference implementation for what Build in Five should produce.
- The **MVP scope has been defined** (3 March): three IRP API modules with a foundation layer, each producing two views (raw data export and an intelligent dashboard), with drag-and-drop composition. No AI/LLM integration in the app itself (to avoid cost spiralling).
- Richard has **not committed** to the exceedance demo. He told Martin on 3 March: "I need to talk to you about this timeline and stuff first." The team agreed Martin should summarise the demo approach and send it to Ben for feedback on whether it meets exceedance requirements.

## Team

| Role | Person | Notes |
|------|--------|-------|
| Developer | Martin Davies | 12-week assignment. Building the customer-facing pre-sales tool. Previously built Apollo dashboards using IRP APIs. Nearly full-time on this ("canopies isn't too busy anyway, so pretty much my whole time will be on this"). |
| Vision / Concept | Richard Dosoo | Originated the concept on 6 Jan. Provides strategic direction and manages stakeholder expectations (especially Ben). |
| Programme | Azmain | Provided Martin with context documents. Defined MVP scope with Martin on 3 Mar. Managing programme-level coordination. |
| Stakeholder / Champion | Ben Brooks | Wants to use Build in Five for his innovation panel at the exceedance event. Driving the demo requirements. Has additional demo scenarios beyond the dashboard use case. |
| App Factory / Infrastructure | BenVH (Ben Van Houten) | Responsible for the deployment pipeline that Build in Five apps would flow through. Also building app factory input funnel. Nicole helping with 50% of her time. |
| Supporting | Nicole | 50% time allocated to help BenVH with app factory. Also onboarding to help with CLARA. |

## Timeline

| Date | Event | Significance |
|------|-------|-------------|
| 6 Jan | Richard explains the concept to Azmain | Workstream 6 identified: use Cursor in customer conversations to build apps on IRP live, demonstrating platform power as a sales tool |
| 8 Jan | Richard and Martin discuss technical approach | Early technical conversations about what the framework could look like |
| 19 Jan | George Dyke onboarded to Cursor | Richard walks George through building an account planner app -- demonstrates the "build it quickly" cultural shift |
| 5 Feb | Martin and Azmain discuss the framework | Both admit they don't fully understand the end goal. Need more input from Richard. Key question: what exactly is the deliverable? |
| 19 Feb | Rhett onboarded to app development | Rhett learning GitHub, being set up for the standard tech stack / automated deployment pipeline vision |
| 27 Feb | Martin returns from holiday, begins active work | Demo originally targeting March 21 exceedance event. Scope has expanded from original concept. |
| 3 Mar | Azmain and Martin define MVP scope | In-person session. Martin shows Apollo dashboard as reference. Three modules, foundation layer, drag-and-drop UI defined. No AI integration in MVP. |
| 3 Mar | Programme standup -- team allocation discussed | Martin confirmed on Build in Five. Nicole 50% on app factory with BenVH, 50% helping CLARA. Chris primarily on CLARA. Richard to connect with Martin and Ben on exceedance feasibility. |
| 4 Mar | Build in Five call with Richard, Martin, Azmain | Exceedance timeline may not work (content due April, event in May). Martin to summarise demo approach and send to Ben for feedback. Dependencies with app factory identified. Two additional analysts may be joining Azmain's team. |

## Concept and Scope

### The Vision (Richard, 6 Jan)

A framework where someone in a customer conversation can build a working application in real time. The customer sees IRP's Risk Data Lake brought to life through a custom app built in minutes, not months. This demonstrates the platform's power more effectively than any slide deck.

### The MVP (Azmain and Martin, 3 Mar)

The MVP is a **customer-facing pre-sales tool** with these components:

**Foundation Layer:**
- Sits behind the UI
- Handles connections to IRP APIs (location API, windstorm models, hurricane models, etc.)
- Knows which API to call based on module selection
- Manages data retrieval and formatting

**Modules (start with 3):**
- Each module represents an IRP API / data product (e.g., location, windstorm America, hurricane)
- User selects modules via drag-and-drop or multi-select
- Each module provides two views:
  - **Raw data tab** -- view the data, export as CSV
  - **Dashboard tab** -- intelligently structured visualisation (appropriate chart types for each data type)
- When multiple modules are selected, each gets its own dashboard

**UI:**
- Drag-and-drop interface for module selection
- Dummy portfolios of varying sizes (hundreds of thousands of lines) pre-loaded for demonstration
- Load a portfolio, select modules, get instant dashboards
- Light and dark mode themes
- Moody's branding (official light blue and dark blue colours, Moody's logo)

**Phase 2 (deferred):**
- Combined dashboards from multiple modules (merge into one unified view)
- Saving and sharing dashboards
- Custom prompt-based visualisation ("create your own" option)

**Explicitly excluded from MVP:**
- No AI/LLM integration within the app ("I don't want to put in AI stuff, because the moment you start putting that in, the costs just spiral" -- Azmain)
- No persistence / data saving ("It doesn't have to be persistent" -- Azmain)
- No security framework (Azure login, cursor rules, etc.) -- this is a prototyping tool
- No app factory integration initially -- runs locally on localhost

### The Demo Approach (Richard, 4 Mar)

Richard's proposed strategy: take Martin's existing Apollo dashboard, reverse-engineer it into a set of requirements and prompts, then demonstrate rebuilding it from scratch using the Build in Five framework. "You're cheating -- you already have built it -- but you're showing someone how they can get to that dashboard or a subset of it."

Three demo scenarios planned:
1. **Dashboard use case** (primary) -- Martin's Apollo-style portfolio dashboard. Reverse-engineer the spec, rebuild using the framework.
2. **Second scenario** -- Ben has additional requirements (not yet specified)
3. **Third scenario** -- Ben has additional requirements (not yet specified)

Martin tasked with summarising the demo approach and sharing with Ben for feedback on exceedance suitability.

### The Three-Tier Architecture (Richard, 4 Mar)

Richard described the longer-term vision in three tiers:
1. **Idea capture** -- A web-based interface where users can store ideas, create application briefs, interact with models without needing to open an IDE (solving the barrier of people not using the IDE)
2. **Local build** -- Application brief feeds into Cursor as a prompt, builds locally in a Docker container, user tests and verifies
3. **App factory deployment** -- From local to Git to the app factory (BenVH's infrastructure), deployed and accessible via URL

Future aspiration: skip the local build step entirely -- go straight from idea to deployed app in the app factory. Richard acknowledged this requires significantly more automation from BenVH and is not feasible in the near term.

## Technical Details

| Component | Detail |
|-----------|--------|
| **Development tool** | Cursor (using Claude models -- Opus for thinking/planning, Sonnet for building) |
| **Target platform** | IRP Risk Data Lake APIs |
| **APIs involved** | Location API, windstorm models, hurricane models, and other IRP model APIs |
| **Data format** | EDM (Exposure Data Model) for input; RDM (Results Data Model) for output |
| **Reference implementation** | Martin's Apollo dashboards -- portfolio analysis with country/peril breakdowns, location-level data, aggregate loss curves, results display |
| **Runtime** | Local (localhost:3000/3001) for MVP; app factory deployment later |
| **Tech stack** | Not yet formalised for Build in Five specifically; the broader programme uses Python, Alembic, AWS |
| **No AI integration** | MVP explicitly avoids LLM API calls within the app to control costs |
| **Budget** | $1,000/month Cursor allocation. Azmain and Richard personally paying $200/month each for Claude Code licences. Martin has barely used his Cursor budget as of 3 Mar. |

## Key Decisions

| Date | Decision | Rationale | Key People |
|------|----------|-----------|------------|
| 6 Jan | Create "Cursor for Pipeline Sales" as workstream 6 | Demonstrate IRP platform power by building apps live in customer meetings | Richard |
| 5 Feb | Martin assigned to Build in Five | 12-week developer assignment. Needs dedicated focus away from CLARA. | Azmain, Richard |
| 27 Feb | Demo target: March 21 exceedance event | Ben wants to showcase innovation at the exceedance event | Ben, Richard |
| 3 Mar | MVP: 3 modules, foundation layer, two views per module, no AI | Keep scope tight. Avoid cost spiralling from LLM integration. Start simple. | Azmain, Martin |
| 3 Mar | No cursor rules or security framework for MVP | This is a prototyping tool -- security guidelines add unnecessary complexity and context overhead | Azmain |
| 3 Mar | Customer-facing pre-sales is Martin's focus; internal app factory is BenVH/Nicole | Clear separation of concerns. Martin should not be pulled into infrastructure work. | Azmain |
| 4 Mar | Exceedance timeline under review | Richard not committing until Martin's estimates are reviewed and Ben confirms scope requirements | Richard |
| 4 Mar | Reverse-engineer demo from existing dashboard | Use Martin's Apollo dashboard as the known-good target, decompose into requirements, rebuild using the framework | Richard |

## Risks

| Risk | Impact | Likelihood | Notes |
|------|--------|------------|-------|
| **Scope expansion** | High | High | Ben has "a couple other examples" beyond the dashboard. Richard flagged on 5 Feb that scope was already expanding. Ben will "want to pour more on it and add more." |
| **Exceedance deadline may not be achievable** | High | Medium | Content must be agreed by April for the May event. Richard explicitly said the timelines may not work. Martin needs to provide estimates. |
| **Unclear end goal persists** | Medium | Medium | As of 5 Feb, both Martin and Azmain admitted they didn't fully understand the end goal. The 3 Mar session clarified the MVP, but the broader vision (idea capture to app factory pipeline) is still aspirational. |
| **App factory dependency** | Medium | Medium | The full vision depends on BenVH's app factory infrastructure, which is also under-resourced. BenVH flagged on 3 Mar that he hasn't had time to focus on app factory to the degree he wants. Four other apps are already in the pipeline. |
| **Budget constraints** | Medium | Low | Cursor budget is $1,000/month. Martin has barely used his. But heavy building with Opus could burn through quickly (Azmain burned $750 in 3 days previously). |
| **Martin's assignment is time-limited** | High | Certain | 12-week assignment. Clock is ticking. If scope keeps expanding, key deliverables may not land within the window. |
| **No formal requirements or PRD** | Medium | High | Azmain acknowledged on 3 Mar: "I don't have detailed documents... we need to get on a call and I need to run you through it." Documentation is being reverse-engineered from prompts and conversations. |

## Dependencies

| Dependency | Owner | Status | Impact on Build in Five |
|------------|-------|--------|------------------------|
| App factory deployment pipeline | BenVH | Under-resourced; BenVH split across multiple demands | Blocks transition from local prototype to deployed app |
| IRP API access for demo | Martin / product team | Martin has prior experience from Apollo; API access appears available | Foundation layer depends on working API connections |
| Exceedance event requirements from Ben | Ben Brooks | Pending -- Martin to send summary for Ben's feedback | Determines whether exceedance demo is in scope or deferred |
| Nicole 50% time on app factory | Nicole / Richard | Agreed 3 Mar | Helps unblock BenVH but competes with CLARA support work |
| Nikhil supporting BenVH on app factory | Nikhil | Referenced by Richard on 4 Mar | Additional capacity for infrastructure work |

## Open Questions

1. **Has the exceedance demo been confirmed or deferred?** Richard said timelines may not work. Martin was asked to summarise and send to Ben. What was Ben's response?
2. **What are Ben's second and third demo scenarios?** Only the dashboard use case has been defined. Ben's additional requirements are unknown.
3. **Is Martin on track?** He has the prior Apollo work as a head start, but no estimates have been shared.
4. **What IRP APIs will the three MVP modules use?** Location API is confirmed. The other two need to be identified.
5. **How does the idea capture layer work?** Richard described a web-based interface for non-IDE users. Who builds this? When?
6. **Will two additional analysts materialise?** Richard mentioned on 4 Mar that Azmain is getting two analysts. Unclear if they could support Build in Five or are purely for CLARA.
7. **What happens when Martin's 12-week assignment ends?** Who maintains and extends Build in Five? Is there a handoff plan?
8. **Does the app factory need to be ready before Build in Five can demo?** Richard said the first version is "probably good enough for them to build it locally first" -- but the full value proposition requires deployment.

## Transcript References

| Date | Transcript | Relevance |
|------|-----------|-----------|
| 6 Jan | `06-01-2026_-_AI_PM_Discussion_w_Richard.txt` | Richard identifies "Cursor for Pipeline Sales" as workstream 6. Explains concept to Azmain. |
| 8 Jan | `08-01-2026_-_Chat_with_Rich_Martin.txt` | Early technical discussion between Richard and Martin about the approach |
| 19 Jan | `19-01-2026_-_Account_Planner_w_George_D.txt` | George onboarded to Cursor. Demonstrates cultural resistance to rapid iteration. Relevant to the "just build it" mindset that Build in Five embodies. |
| 19 Feb | `2026-02-19_-_App_development_with_Rhett.txt` | Rhett onboarded to app development. Richard explains dual-purpose infrastructure: internal productivity apps AND customer-facing demo apps on IRP's Risk Data Lake. Standard tech stack and automated deployment pipeline is the goal. |
| 5 Feb | `2026-02-05_-_Programm_call_x_Martin__1_.txt` | Martin and Azmain discuss the framework. Both admit unclear on end goal. Concept: non-technical users scope, design, and deploy apps on IRP's Risk Data Lake using Cursor in a controlled environment. |
| 27 Feb | `2026-02-27_-_Build_in_Five_with_Martin.txt` | Martin back from holiday. Begins active development. Demo targeting exceedance event. |
| 3 Mar | `2026-03-03 - AI Tool Development Meeting.txt` | Critical session. Martin shows Apollo dashboard to Azmain. MVP scope defined: three modules, foundation layer, drag-and-drop UI, two views per module. No AI integration. No security framework. Start from scratch, lean and fast. |
| 3 Mar | `2026-03-03 - GenAI Program Standup & Next steps.txt` | Team allocation: Martin on Build in Five, Nicole 50% app factory / 50% CLARA, Chris on CLARA, BenVH on app factory. Richard to connect with Martin and Ben on exceedance feasibility. BenVH raises app factory being under-resourced. |
| 4 Mar | `2026-03-04 - Build in 5 Discussion.txt` | Exceedance timeline may not work (content due April, event in May). Martin to summarise demo approach for Ben. Reverse-engineer demo from existing dashboard. Three demo scenarios. App factory dependencies. Two analysts potentially joining. |
