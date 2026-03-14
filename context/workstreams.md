# Workstream Status Tracker

Last updated: 2026-03-13 (all transcripts through 13 March processed)

---

## WS1: Training & Enablement
**Lead:** Azmain (nominal) | Pietro, Stephanie, Colin (advisory)
**Status:** STALLED

- **Conceptual framework exists** — solution-focused training buckets, competency assessment survey, train-the-trainer approach (from 14 Jan session with Colin/Pietro/Stephanie)
- **No execution.** CLARA consumed all of Azmain's bandwidth.
- **Previous training:** Dec 2025, ~40 attendees from 80 registered
- **Week 3 (19 Jan):** George Dyke onboarded to Cursor by Richard in a multi-hour hands-on session — informal training that demonstrates the spec-driven development approach. This is ad hoc, not structured enablement.
- **Azmain flagged to Natalia (20 Feb):** Identified as "biggest/quickest win" but no time allocated
- **March update:** Two grads arriving April 7 may provide capacity. Pietro and Stephanie still engaged on framework but no execution resources assigned.
- **13 Mar (BREAKTHROUGH):** Banking Credit team shared their mature agent day framework — 4-tier model (awareness → autonomous), pre-work methodology, transit teachers (non-coders teaching AI skills), individual projects, bi-weekly follow-ups. Insurance team acknowledged their November training was too generic. Quarterly cross-OU touchpoint agreed. Richard committed to homework on skills repo and governance model before formalising collaboration. This is the first concrete methodology the insurance team can adopt for WS1 execution.
- **Next step needed:** Someone other than Azmain to own execution, or Azmain's workload must be redistributed. Grads could potentially own this. Banking's agent day model provides a ready-made framework to adopt.

---

## WS2: CLARA (IRP Adoption Tracker)
**Lead:** Azmain (dev) | Ben Brooks (product vision) | BenVH (infrastructure)
**Status:** LIVE — Stabilising

### Timeline
| Date | Milestone |
|------|-----------|
| Christmas 2025 | Ben builds v1 locally (SQLite) |
| 7 Jan | Azure blocked → pivot to AWS |
| 14 Jan | First AWS deployment |
| 15 Jan | Advisory team demo |
| 19 Jan | Deployed version broken — database schema out of sync. Debugging sessions with Claude Code. |
| 20 Jan | Azmain builds data input hub overnight using Claude. Programme origin story reframed for Diya. |
| 21 Jan | Data input hub demoed to PMs (Vlad, Diana). Portfolio Review process designed with Natalia/Ben. |
| 22 Jan | Diya misses priority call. George discovers account planner overlap with Sales Recon. |
| 23 Jan | Adoption charter folded into CLARA. Dress rehearsal for Monday exec meeting. Use case creation broken (500 errors). Claude Code paid for personally by Richard. |
| 26 Jan | First live Portfolio Review with full CSM team |
| 2 Feb | Data loss incident → trust damage |
| 9 Feb | Claude Code access secured |
| 12 Feb | CSM workshop hands-on sessions |
| 20 Feb | Andy Frappe demo |
| 23 Feb | Diya governance session, 8-week resource plan |
| 3 Mar | Nikhil (50%) and Chris formally onboarded. Bedrock API key working. |
| 3 Mar | Life SLT shown CLARA — template/flat-pack approach proposed for cross-OU reuse |
| 4 Mar | Two-week release cycle adopted. Azmain reports to Diana. |
| 4 Mar | New migration dashboard design session with Stacy/Natalia |
| 5 Mar | Richard showing signs of exhaustion. Team standup focused on scorecard tab. |
| 6 Mar | Gainsight integration meeting scheduled. Security audit findings being addressed by Chris. |

### Current State
- Live on AWS with CI/CD pipeline (but deployment fragile — no tested rollback, Alembic migrations causing breakage)
- Used in weekly Portfolio Reviews (Natalia facilitates)
- 31 scorecard migration accounts = priority dataset
- RBAC implemented
- Data quality is the primary challenge (not features)
- **Week 3 additions:** Data input hub live (CSMs/PMs fill data in-app). Portfolio Review process designed. Adoption charter (WS4) formally folded in. 155 active accounts loaded from December golden source. Dashboard colour/RAG confusion identified and queued for fix. No data export by design (forces platform usage).
- **March additions:** Nikhil (50% CLARA / 50% App Factory) and Chris onboarded — Chris on bug fixes and security audit findings, Nikhil on scorecard tab and migration burndown. Bedrock API key now functional. Two-week structured release cycle replaces ad-hoc deploys. Template/flat-pack approach proposed for cross-OU scaling (Life team shown demo). Adoption charter data flow starts one-directional (bi-directional too complex due to customer-annotated Excel with diagrams). Gainsight architecture alignment meeting scheduled with Tina Palumbo, Nadim, Rajesh. Also pushing for Salesforce programmatic access.
- **12 Mar additions:** CLARA officially entering maintenance mode. Natalia Plant established fortnightly release governance with Tuesday prioritisation reviews. Two grads arriving April 7 (London + New York) for 100% CLARA maintenance. Ben Brooks restricted to sandbox. Analytics tab being removed from management dashboard. Scorecard tab and management dashboard moved higher in navigation for ISLT on Monday. Use case completion check added (software status must be "in production" first). Gainsight integration meeting held — bi-directional POC proposed but no timeline pressure (earliest May). Catherine's COE overlap with AI programme causing significant political friction.
- **13 Mar additions:** CLARA demoed to Cihan's entire product & technology team — biggest audience expansion since launch. Cihan personally endorsed CLARA as a daily tool. Azmain imported ~4,000-5,000 users under Andy Frappe hierarchy as SSO viewers. Product teams (Ollie, Julie) asked how to contribute. Call chat established as living feedback channel. Ben Brooks positioned CLARA's structured data as enabling product prioritisation via blocker theme analysis. Julie asked about CLARA vs Gainsight — distinguished as structured adoption data vs CRM health scoring.

### Feature Backlog
- Scorecard tab and migration burndown (in active development — Nikhil)
- User Voice integration (Peter Kimes requirements, 26 Feb)
- HD model data integration (Courtney, 26 Feb)
- Solution architecture / blueprint attachment flow
- Power BI migration dashboard (Andy Frappe ask)
- Parent/subsidiary account rollup
- Reports section (modelled on Salesforce)
- Gainsight integration (meeting scheduled, Gainsight hard launch March 30 confirmed by Catherine)
- Salesforce integration — one-way read decided (11 Mar). Cases and Case Feed only (phase 1). Four consumers: Bernard (sentiment), Courtney (HD), Kevin (tickets), CLARA (blockers). App Factory MCP server as middleware.

### Key Risks
- Azmain = single point of failure for features (partially mitigated by Nikhil/Chris onboarding)
- BenVH = single point of failure for infrastructure — burnout risk from Nikhil conflict (being addressed)
- Richard = key programme strategist — stable and committed
- Scope creep from multiple new integration requirements (User Voice, HD models, Gainsight, Salesforce, cross-OU templates)
- Token/budget constraints ($750 in 3 days, corporate budget $20K). Bedrock now working but personal Claude usage flagged by security audit.
- **Deployment fragility** — no tested rollback procedure. Team admitted attempting rollback could leave system completely unusable. Schema changes now require BenVH approval before execution.
- **Security/compliance** — Personal Claude accounts used for Moody's work caught by audit. Ben Brooks providing cover.

---

## WS3: Customer Success Agent
**Lead:** Kevin Pern
**Status:** MINIMAL PROGRESS

- Kevin built a Copilot Studio + Salesforce prototype
- No programme oversight or operational integration
- **Week 3:** Sales Recon exec meeting prep underway (19 Jan) — Jamie's team, Idris (banking), Richard aligning on CS requirements for Sales Recon. February pilot planned with key CS users. Bernard (Life team) built separate Copilot health dashboard. Idris raised hallucination concerns with LLMs for financial data. The CS Agent workstream is being partially addressed through the Sales Recon alignment, but Kevin's standalone work remains unconnected.
- Azmain told Natalia (20 Feb) it "needs engagement"
- **Next step needed:** Formal check-in with Kevin. Assess what exists, what's needed.

---

## WS4: Friday (Project Management App)
**Lead:** Azmain (developer) | Diana (sponsor/manager)
**Status:** ACTIVE — Side project, gaining traction
**Predecessor:** Adoption Charter Workflow (folded into CLARA Jan 23)

### Adoption Charter Legacy
- 23 Jan: Decision to fold charter workflow into CLARA rather than build separately
- Steve's Excel tracker had ~75% field overlap with CLARA (15/20 columns already exist)
- v1 of adoption charter section built in CLARA (Ben's prior work)
- 3 Mar: Adoption charter data flow decided as one-directional to start (bi-directional too complex)

### Friday — The New WS4
- **What it is:** Internal PM app like Monday.com, built by Azmain using Claude Code in cloud environment
- **Named after:** The 1940 film "His Girl Friday"
- **First mentioned:** 4 Mar (Diana 1-1)
- **Relationship to CLARA:** Syncs bidirectionally with CLARA for IRP projects. Replaces the Adoption Charter workstream slot.
- **Sponsor:** Diana (Azmain's new manager as of 4 Mar). Plans to present Friday vision to Ben/Charlotte.
- **Resourcing:** Prashant to be allocated to help with development.
- **Cost concern:** Azmain burned $500 Cursor in one day building it.

### Key Risks
- Azmain's bandwidth already stretched across CLARA + programme management + five other workstreams
- Scope creep risk — Friday is a side project that could expand
- No formal budget or sanctioning — unclear if it's a skunkworks project or official
- **Next step needed:** Clarity on where Friday fits in programme priorities. Diana presenting to Ben/Charlotte for formal approval.

---

## WS5: IRP Navigator L1 Automation
**Lead:** Unclear (product team building MCP server)
**Status:** EARLY STAGE

- Concept: use Navigator's upcoming API support to auto-answer L1 tickets
- 19 Feb: MCP server discussion with Cihan and Lonny
- No CS-side build started
- Azmain told Natalia (20 Feb) he "doesn't fully understand it"
- **Next step needed:** Clarity on what CS needs to build vs what product team delivers

---

## WS6: Build in Five (Cursor for Pipeline Sales)
**Lead:** Martin Davies | Richard (vision)
**Status:** ACTIVE — Breakthrough progress, on track for May exceedance

- Concept: framework for building demo apps on IRP's Risk Data Lake using Cursor during customer conversations
- **Week 3 (19 Jan):** Richard onboarded George Dyke to Cursor in multi-hour session. Martin barely engaged this week.
- Martin back from holiday late Feb, actively developing
- **3 Mar:** Apollo dashboard as reference implementation. Three-tier vision articulated. MVP scope defined.
- **4 Mar:** Demo target shifted from March 21 to May exceedance.
- **10 Mar (BREAKTHROUGH):** Martin demoed a near-complete dashboard builder that exceeded all expectations:
  - Full drag-drop UI with data/visual/custom (AI) modes per component
  - White-labelling: themes, dark mode, logos, branding colours, fonts, corner radius
  - Live Risk Modeller API connection working
  - Tab containers, save/load dashboard configs, preview mode
  - Richard compared it to Databricks Genie. Ben Brooks positive.
- **Critical next step:** Wire up Navigator MCP server for live API definitions — this completes the demo loop
- **Stakeholder cascade defined:** Tech consulting (Bala/Lonnie/Alicia) → Demo team (Bibo/Gibson) → Sales (Flemington) → Exceedance content factory
- **Product positioning question opened:** Is this a Moody's product feature or a customer self-service tool?
- Martin's 12-week clock ticking but output justifies the investment many times over
- **11 Mar:** Nikhil saw the demo for the first time — genuinely impressed. Three-pronged convergence plan: Martin's dashboard + Nikhil's MCP work + Elliot's blueprint profiling agent. Azmain to create combined project plan. Elliot's grad rotation may be extended to support Martin. AIG intelligence revealed: strategic deals with Anthropic and Palantir, using MCP for underwriting — elevates Build in Five from demo tool to strategic client engagement vehicle. Chris Malhauser already has EDMS MCP profiling working. Martin to create new GitHub repo (ins-build-in-five naming).
