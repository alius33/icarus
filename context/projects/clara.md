# WS2: CLARA (IRP Adoption Tracker)

## Overview

CLARA is a web-based dashboard and data management application that tracks customer adoption and migration status across Moody's Analytics Insurance Division's IRP (Intelligent Risk Platform) portfolio. It replaced a manual process where Stacy Dixtra maintained 300-slide PowerPoint decks and five people scraped data from spreadsheets to answer questions about account health.

The core problem CLARA solves: the team was collecting data to answer questions rather than structuring data to be queried. Before CLARA, finding the status of a single account required fire drills across multiple Excel sheets and the "golden source" O&M spreadsheet. Senior leadership (Andy Frappe, Diya Sawhny) needed real-time visibility into migration progress against the insurance scorecard target of 30+ migrations in 2026, and had no reliable way to get it.

CLARA is the flagship project of the Customer Success Gen AI Programme and the only workstream with meaningful delivery to date. It is formally designated as an interim solution; the agreed end-state is migration into Sales Recon by end of FY26, but standalone investment continues because Sales Recon cannot absorb CS requirements in the near term.

The name "CLARA" was crowd-sourced from the CSM team during the January 2026 rollout.

---

## Status

**As of 9 March 2026: LIVE -- Stabilising, with active feature development**

- Deployed on AWS with CI/CD pipeline across dev/staging/prod environments
- Used weekly in Portfolio Reviews facilitated by Natalia
- Management Dashboard being rebuilt with new migration burn-down and scorecard tab (active work as of 5 March)
- Chris M onboarded as dedicated CLARA developer handling bug fixes and feedback triage
- Nikhil providing 50% time, split between CLARA and app factory infrastructure work
- Two rotating graduates arriving in April for ongoing bug fix and maintenance work
- Gainsight integration conversation formally initiated -- first meeting with Gainsight team scheduled for week of 10 March
- Bedrock API key now working (confirmed ~6 March), unblocking LLM integration features
- Scorecard dashboard requirements being refined with Stacy and Natalia (migration burn-down, quarterly view, actuals vs forecast)
- Portfolio Review grey box with inaccurate priority account counter being removed (Natalia/Diya priority)
- Reports functionality being tested by Stacy (modelled on Salesforce reports structure)
- Analytics tab under review by Stacy and Kathryn Palkovics to remove confusing/outdated metrics
- Full user-facing documentation and knowledge base generated (in dev, pending promotion)
- 113 Alembic migration heads squashed to one base level (in staging as of 3 March)

---

## Team

| Role | Person | Notes |
|------|--------|-------|
| Product Owner / Visionary | Ben Brookes | Built v1 over Christmas 2025. Drives speed and adoption. "Kill CSMs with kindness." |
| Programme / Operational Owner | Richard Dosoo | Technical bridge. Manages stakeholders up/across/down. Carries deployment knowledge. Handles solution blueprint integration and Rhett's adoption charter Excel work. |
| Programme Manager & Lead Developer | Azmain | 100% consumed by CLARA since Jan. Learning Git/CI/CD on the job. Single point of failure for features. |
| Infrastructure Engineer | BenVH (Van Houten) | AWS deployment, CI/CD pipeline, security, app factory. Single point of failure for infrastructure. Created patented CICD orchestration tool. Building automated prod-to-staging sync. |
| Developer (Bug Fixes & Feedback) | Chris M | Onboarded early March 2026. Working through consolidated feedback list. Getting familiar with codebase via bug fixes. |
| Developer (50% time) | Nikhil | New tech consulting lead (replaced Alex). Split between CLARA and app factory. Reports to Richard. |
| Developer (Build in Five) | Martin Davies | 12-week assignment. Primarily on WS6 but part of wider CLARA standup team. |
| Azmain's Manager (until 31 March) | Natalia Orzechowska | Senior Director. Runs weekly Portfolio Reviews using CLARA. Defined priority account framework (31 scorecard migrations). Owns Gainsight relationship. Engaged on charter (14 Mar). Diana Kazakova-Ivanova takes over 1 April. |
| Gainsight Governance / CLARA Release Lead | Natalia Plant | Established fortnightly CLARA release cadence (12 Mar). Tuesday governance reviews. DIFFERENT person from Natalia Orzechowska. |
| Executive Sponsor | Diya Sawhny | Engaged properly since 23 Feb governance session. Regularly checks scorecard numbers. Impatient with detail. |
| President, Moody's Analytics | Andy Frappe | Saw CLARA demo Feb 20. Wants centralised migration reporting in Power BI. |
| CSM Leadership (Gatekeeper) | Josh Ellingson | Conservative on release timing. Key concern: data interpretation accuracy reaching Andy Frappe. Coming around. |
| CSM Leadership (Workshop Lead) | George Dyke | Organised Feb workshops. Building separate account planner. Pragmatic. |
| Data & Reporting | Stacy Dixtra | Defines reporting requirements. Writing insurance migration BRD. Reviewing analytics tab. Testing reports. Prefers Excel exports. |
| Data Alignment / COE Lead | Kathryn Palkovics (referred to as "Catherine" in earlier audio transcripts) | Sense-checking complex accounts (reinsurer, primary, broker, global entity). Working with Gainsight team. Key contact for enterprise tools integration. COE lead — digital engagement, enablement, Gainsight/SFDC. 14 Mar: Asserted COE authority on Gainsight integration charter, requested to join project team. |
| User Voice Integration | Peter Kimes | Detailed requirements captured 26 Feb for integrating User Voice data into CLARA. |
| HD Models Analysis | Courtney | Analysed 2000-3000 HD support cases. Exploring how to surface adoption barrier themes in CLARA. |
| Adoption Charter Process | Steve Gentilli | Owns adoption charter workflow. Being folded into CLARA (WS4). Solution fit matrix may be separate app. |
| Solution Architecture Feedback | Liz Couchman | Provides tracker feedback on specific accounts and usability. |
| Rhett | Adoption Charter (Excel route) | Built Excel-based adoption charter tool independently. Not coordinated with agreed Word-to-app approach. Richard integrating his work. |
| Rotating Graduate (London) | Alvin | Arriving Q2 2026 (April 7 target). Interviewed and chosen by Azmain specifically for AI/CLARA work. |
| Rotating Graduate (New York) | Sam | Arriving Q2 2026 (April 7 target). Interviewed and chosen by Azmain specifically for AI/CLARA work. Different person from Samuel Gibson. |

---

## Timeline & Milestones

| Date | Milestone | Significance |
|------|-----------|-------------|
| Christmas 2025 | Ben Brookes builds v1 locally | SQLite database, built in Cursor over holiday evenings. Dashboard, use cases, blockers, action plans, data quality views. Proof of concept. |
| Dec 2025 | Steerco establishes programme | Richard presents five (later six) workstreams. Training elevated to own workstream. |
| 6 Jan 2026 | Ben demos tracker to Azmain and Richard | First internal showing. Key concepts established: migration vs adoption, migration-critical workflows, RAG status. Richard recognises potential to break golden source into proper data model. |
| 6 Jan 2026 | Richard frames programme for Azmain | Six projects laid out. CLARA positioned as career growth vehicle for Azmain. North Star: full customer journey system. |
| 7 Jan 2026 | Azure deployment blocked | Architecture review with security/infra. Azure networking and security restrictions unresolvable in meeting. |
| 7 Jan 2026 | **Decision: Pivot to AWS** | Unblocked deployment. Without this, app would have remained local-only for weeks. |
| 8-9 Jan 2026 | Technical troubleshooting begins | Azmain new to Git. Missing files, import errors. Cursor premium limits hit. Richard creates updated data model. |
| 9 Jan 2026 | SQL Server on AWS RDS chosen | Speed of setup. Can migrate to Postgres/DynamoDB later. |
| 12 Jan 2026 | Standalone-first architecture decided | Build independently of Gainsight/Salesforce. Planned convergence later. Gainsight API blocked until March. |
| 13 Jan 2026 | **Decision: Real data over synthetic** | Ben insists CSMs will fixate on errors in fake data. Painful but forced early data quality confrontation. |
| 14 Jan 2026 | **First AWS deployment** | BenVH gets CI/CD pipeline working. Advisory app factory URL established. |
| 15 Jan 2026 | Advisory team demo | First external demo to Stacy, Liz, Christine, Steve Gentilli. Feedback: dropdown categorisation for blockers, data quality guidance needed. |
| 16 Jan 2026 | Josh Ellingson feedback session | Critical stakeholder engagement. Josh cautious about data interpretation accuracy. Proposes CSM-wide demo before opening for feedback. |
| 21 Jan 2026 | Data input hub built | Shift from "fill in Excel" to "fill in the app directly." Azmain builds overnight using Claude. |
| 21 Jan 2026 | Portfolio Review structure designed | Natalia insists on using existing dashboard, not separate tab. No editing during meetings. CSMs instructed to fill data in 20-minute squad sessions. |
| 23 Jan 2026 | **Decision: Fold adoption charter into CLARA (WS4)** | Rather than building a separate system, absorb charter functionality into the tracker. |
| 23 Jan 2026 | Tool name solicitation launched | Eventually named "CLARA" by CSM team. |
| 26 Jan 2026 | **FIRST LIVE PORTFOLIO REVIEW** | Landmark session. Natalia presents running agenda. Ben gives overview. Diya speaks -- positions as critical to scorecard. Azmain demos with Ben narrating. First time broader CSM team sees the tool. |
| 26 Jan 2026 | Sales Recon executive session | Meeting with Ari Lahavi, Jamie, Colin Holmes, Mike Steele, Diya. CLARA presented as interim solution. End-state: CS workflow migration to Sales Recon by end of FY26. |
| 27 Jan 2026 | Resource constraints flagged | Azmain 100% on CLARA, no time for programme management. Need for dev/staging/prod environments now urgent. |
| 2 Feb 2026 | **DATA LOSS INCIDENT** | CSM-entered data lost over weekend due to deployment refresh. Multiple CSMs report entries disappeared. Significant trust damage. Diya notes the issue. |
| 2 Feb 2026 | First live Portfolio Review with Natalia | Nine priority accounts reviewed. Rhonda gives first live account update (Aeon). Data loss dominates discussion. |
| 3 Feb 2026 | RBAC implemented and tested | Philip Garner used as test subject. Authentication debugging resolved by BenVH. |
| 5 Feb 2026 | **Priority redefined: 31 scorecard migration accounts** | Natalia reframes from arbitrary "high priority" to the accounts on the 2026 migration timeline. 17 "accelerated" accounts are a subset. |
| 5 Feb 2026 | Status vs stage distinction requested | Natalia identifies filter/search gaps in UI. Wants rotating focus: priorities one week, accelerated the next. |
| 9 Feb 2026 | Claude Code access secured | Via AWS Bedrock pilot. Not desktop interface -- connecting to AWS environment. |
| 9 Feb 2026 | **Decision: Holistic data fix** | Richard: "If we don't tackle it holistically, all that's going to happen is every week there's a new schema change." Kathryn Palkovics to sense-check complex accounts. |
| 12 Feb 2026 | **CSM Workshop hands-on sessions** | George's London workshop. Azmain commits: "Any updates from yesterday onwards will be preserved." Parent/subsidiary rollup issues discovered. Miles used as workflow guinea pig. |
| 12 Feb 2026 | **Decision: Data preserved going forward** | Explicit commitment to CSMs. No more wipe-and-reload deployments. |
| 20 Feb 2026 | **Andy Frappe demo** | Ben demos to President of Moody's Analytics. Highest visibility moment. Azmain scrambles to fix orphan data and duplicate records. Discovers blockers page making 60+ individual API calls; optimises to single batch call. |
| 20 Feb 2026 | Azmain formally raises bandwidth constraint | Tells Natalia the other five workstreams have had zero progress. |
| 23 Feb 2026 | **Diya governance session** | Three pillars formalised: (1) IRP portfolio governance, (2) Customer intelligence / Sales Recon alignment, (3) Platform enablement. Resource plan for next 8 weeks. |
| 23 Feb 2026 | Cursor budget crisis | Azmain used $750 in 3 days. Corporate budget $10K to $20K but Opus 4.6 is 3x more expensive. Downgraded to Sonnet 4.5 to manage costs. |
| 26 Feb 2026 | User Voice integration requirements | Peter Kimes session. Separate data object proposed (not appended to blockers). API integration preferred. |
| 26 Feb 2026 | HD Models discussion with Courtney | 2000-3000 support cases analysed. Thematic patterns for product prioritisation rather than per-account data. |
| 26 Feb 2026 | Power BI migration dashboard ask | Andy Frappe wants all migrations reported centrally. Stacy writing insurance requirements into banking BRD template. |
| 26 Feb 2026 | AI Infrastructure planning | Bedrock/Claude model enablement discussed. CDK vs CloudFormation debate. Non-prod account needed. |
| 1 Mar 2026 | Cursor budget reset | Monthly budget replenished. Azmain back on Opus within Cursor. |
| 3 Mar 2026 | **Team expansion: Chris & Nikhil onboarded** | GenAI Program standup. Chris assigned primarily to CLARA bug fixes/feedback. Nikhil 50% CLARA / 50% app factory. BenVH freed to focus on app factory infrastructure. |
| 3 Mar 2026 | 113 migration heads squashed | Alembic migration heads consolidated to single base. Pushed through dev to staging without breakage. |
| 3 Mar 2026 | Priorities confirmed: feedback > blockers > adoption charters | Azmain sets sequence: (1) consolidated feedback triage, (2) blocker intelligence with Bedrock API, (3) adoption charter parsing. |
| 4 Mar 2026 | **Migration dashboard requirements session with Stacy & Natalia** | Hosting Plus rolls into Risk Link numbers; RBO rolls into Risk Browser. Grey box removed from Portfolio Review. Scorecard tab to become default on Management Dashboard. Quarterly view added. "Reported year of completion" field proposed for 4 pre-2026 completions. Actuals year-to-date to be shown alongside forecast. |
| 4 Mar 2026 | Analytics tab review initiated | Stacy to coordinate with Kathryn Palkovics on what to keep/remove. Archetype data and outdated metrics flagged for removal. |
| 5 Mar 2026 | **CLARA standup: Work allocation confirmed** | Chris on bug fixes/defects. Richard testing Rhett's adoption charter Excel integration. Azmain building migration burn-down and management dashboard changes. Richard reviewing feature requests for feasibility. |
| 5 Mar 2026 | User documentation generated | Full knowledge base for CLARA created at 2am by Azmain. In dev, pending promotion. Intended to power future AI assistant chatbot within CLARA. |
| ~6 Mar 2026 | **Bedrock API key confirmed working** | Nikhil has it working locally via IAM role-based authentication. No hard-coded keys. Unblocks LLM integration into CLARA for blocker intelligence. |
| 6 Mar 2026 | **Pre-Gainsight team meeting** | Kathryn Palkovics, Richard, Azmain, BenVH, Chris align before Thursday meeting with Gainsight team. Agreed: CLARA is a small part of overall customer health (Gainsight's purview). CLARA will adapt its architecture to fit Gainsight, not vice versa. Also agreed to include Salesforce integration requirements in same meeting. Governance framework for app factory discussed. |
| 6 Mar 2026 | BenVH working on automated staging sync | Script to periodically sync production database to staging (once weekly target). |
| 6 Mar 2026 | Chris working through feedback backlog | Using Cursor to analyse resolved vs unresolved items. Starting with most recent feedback first. Most early-Feb items already fixed. |
| 7 Apr 2026 (planned) | Two rotating graduates join | One New York, one London. Will take over bug fix and maintenance work from Chris. |

---

## Architecture & Infrastructure

### Tech Stack
- **Front end:** Web application (React-based, details inferred from deployment discussions)
- **Back end:** Python API (FastAPI implied from SQLAlchemy and Alembic usage)
- **Database:** SQL Server on AWS RDS (chosen 9 Jan for speed; migration to Postgres/DynamoDB possible later)
- **ORM / Migrations:** SQLAlchemy + Alembic (source of significant deployment sync issues; 113 migration heads accumulated by March, squashed to one)
- **Authentication:** SSO with RBAC (role-based access control). Implemented Feb 2026. Admin, CSM, and management roles.
- **AI Integration:** AWS Bedrock (Claude models via IAM role-based authentication, no hard-coded keys). Working as of ~6 March. Planned for blocker intelligence and in-app AI assistant.

### Deployment
- **Cloud:** AWS (after Azure was blocked on 7 Jan due to security/networking restrictions)
- **CI/CD:** Pipeline built and maintained by BenVH. Automated build, test, deploy. 186 API tests in the suite (6 failures noted in mid-January, subsequently resolved).
- **Environments:** Dev, Staging, Production. Staging is a clone of production (weekly sync being automated by BenVH). Staging used for testing before prod promotion.
- **Load Balancer:** AWS ALB (Application Load Balancer). Caused routing issues early on, resolved.
- **Hosting:** Advisory team's AWS account ("app factory" infrastructure). Cost centre is RMS consulting.

### Infrastructure Concerns
- CDK vs CloudFormation debate unresolved (26 Feb). Cat Accelerate has tech debt: manual Step Function deployment, no backup, no traceability.
- Non-prod AWS account needed but not yet provisioned.
- LLM worker orchestration architecture under discussion: per-OU IAM roles for cost allocation, dynamic agent provisioning. BenVH's phantom agent project proposed as potential solution for agent orchestration across apps.
- Security audit flagged use of personal Claude accounts for Moody's work. Now mitigated by Bedrock API access.

---

## Feature Status

| Feature | Status | Notes |
|---------|--------|-------|
| Dashboard (account overview) | Live | Core functionality. RAG status, migration status, team assignments. |
| Use Cases tracking | Live | Per-account use case status and details. |
| Blockers tracking | Live | Per-account blockers. 60+ API calls optimised to single batch (Feb). |
| Action Plans | Live | Action plan creation and tracking. Orphan data issues identified and fixed. |
| Data Input Hub | Live | CSMs enter data directly in app rather than Excel. Built 21 Jan. |
| Portfolio Review view | Live | Used weekly by Natalia. Grey box with inaccurate counter being removed (Mar). |
| Management Dashboard | Live (being rebuilt) | Tabs for different views. Scorecard tab being added as default. Migration burn-down being built. |
| Migration Burn-down (new) | In Progress | Based on Risk Link and Risk Browser switch-off dates. Separate from adoption burn-down. Being built by Azmain (5 Mar). |
| Scorecard Tab | In Progress | Quarterly view, actuals YTD vs forecast, 2026 migration target tracking. Requirements from Stacy/Natalia (4 Mar). |
| RBAC (Role-Based Access Control) | Live | Admin, CSM, management roles. Implemented Feb. |
| Team Member Assignment | Live | Added without database field changes to avoid breaking deployment (Jan). |
| Reports Section | Live (testing) | Modelled on Salesforce reports structure. Multi-object support. Filter logic has bugs (multi-filter queries breaking). Stacy testing. |
| Analytics Tab | Live (under review) | Recreation of golden source Excel dashboard. Stacy/Kathryn Palkovics reviewing to remove confusing metrics (archetype data, outdated production stats). |
| Adoption Charter (WS4) | Partially built | v1 section exists in CLARA but needs modification. Complexity: actual charters are large Word documents with embedded images, diagrams, delivery plans. Parsing requires OCR/multi-modal AI. Bi-directional flow needed (app to document, document back to app). Rhett built separate Excel-based version without consensus. Richard integrating Rhett's work. |
| Solution Blueprint attachment flow | Planned | Richard working on it. Steve Gentilli's "solution fit matrix" may be separate app. |
| Blocker Intelligence (AI analysis) | Planned (next priority) | Use Bedrock/Claude API to validate blocker quality, extract insights, identify patterns. Bedrock key now working. Second priority after feedback triage. |
| User Voice Integration | Planned | Separate data object (not appended to blockers). API integration preferred over Excel dumps. Peter Kimes requirements captured 26 Feb. |
| HD Model Data Integration | Planned | Thematic adoption barrier patterns from Courtney's 2000-3000 case analysis. Not per-account but aggregate themes for product prioritisation. |
| HD Model Bulk Update (Use Case Matrix) | Proposed (16 Mar) | CSMs demanding bulk update for HD model data points. Ben Brookes proposed matrix UI: use cases on rows, HD models across columns, status grid (not licensed/implementing/validating/in production). Default all HD models to "implementing" for in-scope use cases. Requirements call with Chernell being set up. Tied to Diya deliverable (60-90% manual effort reduction). |
| Power BI Migration Dashboard | Planned | Andy Frappe ask. Stacy writing requirements into banking BRD template. Excel exports from CLARA as interim. |
| Parent/Subsidiary Account Rollup | Known Issue | Updates to subsidiary don't roll up to parent. Makes it look like CSM hasn't updated. Identified at Feb workshop. Fix status unknown. |
| In-App AI Assistant / Chatbot | Planned | User guide / knowledge base generated to power it. Users would ask natural language questions about how to update CLARA. Concept described 5 Mar standup. |
| Gainsight Integration | Early Planning | First formal meeting week of 10 March. Clara will adapt architecture to fit Gainsight. Integration pattern TBD (REST, SSO, API keys). Small POC likely first step. |
| Salesforce Integration | Early Planning | To be discussed in same Gainsight meeting. Previously blocked ("no programmatic access to Salesforce"). Requirements from Bernard and Courtney. Kevin Pern also has requirements. |
| "Reported Year of Completion" field | Proposed | Patch for 4 accounts completed pre-2026 but counted in 2026 scorecard. Stacy investigating whether to include them. May be hidden field or hard-coded. |
| Hosting Plus / RBO roll-up | In Progress | Hosting Plus numbers to roll into Risk Link; RBO into Risk Browser. Notes to explain the inclusion. Requested 4 Mar. |
| Filter/search improvements | Backlog | Status vs stage distinction. Dropdown options for filter values instead of free-text. Multi-filter logic fixes. |
| Data quality validation | Backlog | Ben proposed v2 feature: run blockers through Anthropic API to validate quality. Now feasible with Bedrock access. |

---

## Data

### Data Model
- Designed by Richard (Week 1) with acceptance criteria, projects, action plans, blockers, milestones
- Azmain mapped December golden source to new schema
- Key entities: Accounts, Use Cases, Blockers, Action Plans, Team Members, Migration Status, RAG Status
- Adoption charter data model still being defined (complexity of parsing Word documents with images)
- User Voice proposed as separate data object with traceability to blocker-tagged items

### Golden Source Migration
- The "golden source" was the O&M spreadsheet -- single source of truth before CLARA
- Golden source data loaded into CLARA as baseline
- CSMs instructed not to re-enter data but to validate and supplement what was imported
- Analytics tab was a direct recreation of the golden source Excel dashboard

### Data Quality Issues (Ongoing)
- **Root problem:** CSMs historically entered unstructured, inconsistent data. Blockers lacked categorisation. Statuses were ambiguous.
- **Data loss incident (2 Feb):** Deployment refresh wiped CSM-entered data over a weekend. Trust damage was significant. Explicit commitment made: data preserved from that point forward.
- **Orphan data:** Action plans and other records becoming detached from parent accounts. Front-end filters blocking display. Identified and partially resolved.
- **Duplicate records:** Discovered during Andy Frappe demo prep (20 Feb).
- **Parent/subsidiary mismatch:** Updates to subsidiaries don't roll up, creating false impression of inactivity.
- **Salesforce name mismatches:** Three names in reality vs two fields in system. CSM confusion.
- **Pre-2026 completions:** 4 accounts (QBE, ROI, La Previsora, Ms Transverse) completed migration before 2026 but were on 2026 target list. Stacy investigating how to count them. Natalia inclined not to count them. Decision pending.
- **Status field confusion:** "Stage" field (not started / in flight / completed) was removed, breaking migration count calculations. Being rebuilt with new logic.

### Scorecard Accounts
- 31 accounts on the 2026 migration timeline (scorecard target: 30 migrations)
- 17 "accelerated" accounts are a subset needing special attention
- 10 completions year-to-date (6 with 2026 dates, 4 with pre-2026 dates -- under review)
- Forecasting 36 total (including the 4 questionable ones as buffer)
- Migration = switching off Risk Link and/or Risk Browser

---

## Key Decisions

| # | Date | Decision | Rationale |
|---|------|----------|-----------|
| 1 | 7 Jan | Deploy on AWS instead of Azure | Azure networking/security restrictions blocked progress. Couldn't resolve in architecture review. AWS enabled immediate deployment. |
| 2 | 9 Jan | Use SQL Server on AWS RDS | Speed of setup. Can migrate to Postgres/DynamoDB later. |
| 3 | 12 Jan | Build standalone, plan Gainsight convergence later | Gainsight API access blocked until March at earliest. Waiting would stall everything. |
| 4 | 13 Jan | Use real data for demos, not synthetic | Ben argued CSMs would fixate on errors in fake data. Painful but forced early data quality confrontation. |
| 5 | 21 Jan | Portfolio Review uses existing dashboard, not a separate tab | Natalia's insistence: demonstrate the tool's usability by using it live. No editing during meetings. |
| 6 | 21 Jan | CSMs fill data in the app, not Excel | Data input hub built. Shift from "fill in Excel and we'll import" to "fill in the app directly." |
| 7 | 23 Jan | Fold adoption charter workflow into CLARA (WS4) | Rather than building a separate system, absorb charter functionality into the tracker. |
| 8 | 26 Jan | CLARA is interim; target end-state is Sales Recon | Agreed at executive session with Ari, Jamie, Diya. CS workflow should migrate to Sales Recon by end of FY26. |
| 9 | 5 Feb | Priority = 31 scorecard migration accounts | Natalia reframed from arbitrary "high priority" list to the accounts on the 2026 migration timeline. 17 "accelerated" accounts are a subset. |
| 10 | 9 Feb | Holistic data fix, not incremental patches | Richard: "If we don't tackle it holistically, all that's going to happen is every week there's a new schema change." Kathryn Palkovics to sense-check complex accounts. |
| 11 | 12 Feb | Data preserved from "yesterday onwards" | After data loss incident, explicit commitment to CSMs that entered data will persist. No more wipe-and-reload deployments. |
| 12 | 23 Feb | Three programme pillars formalised at Diya governance session | (1) IRP portfolio governance (CLARA + account planner), (2) Customer intelligence / Sales Recon alignment, (3) Platform enablement. |
| 13 | 23 Feb | 8-week resource plan | Nikhil 50%, Martin (back from holiday), Chris 50%. Priorities: finish CLARA features, address CSM feedback, platform infrastructure. |
| 14 | 26 Feb | User Voice as separate data object, not appended to blockers | Not all User Voice entries are blockers. Separate object with traceability to blocker-tagged items. |
| 15 | 3 Mar | Chris on CLARA bugs, Nikhil split, BenVH freed for app factory | Load balancing team resources. BenVH not needed on CLARA unless CI/CD breaks. |
| 16 | 4 Mar | Hosting Plus rolls into Risk Link; RBO rolls into Risk Browser on dashboard | Scorecard says "Risk Link" and "Risk Browser" only. Sub-products consolidated to avoid confusion. Notes to explain inclusion. |
| 17 | 4 Mar | Remove grey box from Portfolio Review; add Scorecard tab as default on Management Dashboard | Inaccurate numbers confusing Diya. Scorecard becomes the landing page for executives. |
| 18 | 6 Mar | CLARA will adapt architecture to fit Gainsight, not vice versa | Gainsight is the enterprise platform. CLARA covers a small part of overall customer health. Integration must respect Gainsight's architecture. |

---

## Stakeholder Map

### Who cares about CLARA and why

**Diya Sawhny (Executive Sponsor)**
- Cares because CLARA underpins the insurance scorecard migration tracking that Andy Frappe sees
- Regularly checks Management Dashboard numbers; gets confused by discrepancies
- Engaged properly since 23 Feb governance session
- Risk: if she sees bad data, programme loses executive credibility
- Approach: elevator pitches only, make Scorecard tab the default view

**Andy Frappe (President, Moody's Analytics)**
- Saw demo 20 Feb. Wants centralised Power BI migration dashboard across insurance and banking
- Any misinterpreted data point at this level could damage programme credibility permanently
- One level below the board. Highest-stakes audience.

**Ben Brookes (Product Owner)**
- Built v1 and is emotionally invested in CLARA's success
- Pushes speed over caution. Runs 5am training sessions for CSMs.
- Strategy: shopping CLARA around internally (e.g., Life MD) to create independent demand
- Tension with Josh on release timing. Wants CSMs to self-serve more aggressively.
- Currently focused on blockers as top priority, adoption charters second

**Natalia Plant (CS Lead)**
- CLARA is how she runs her weekly Portfolio Reviews
- Redefined "priority" from arbitrary to scorecard-aligned 31 accounts
- Sees CLARA as potentially reusable beyond IRP (EGL, Hosted programmes)
- Concern: CSM workload perception -- CLARA must not feel like more work
- Owns Gainsight relationship; key voice in integration decisions

**Josh Ellingson (CSM Leadership)**
- Gatekeeper for CSM adoption. Conservative.
- Key concern: data interpretation accuracy reaching Andy Frappe
- Coming around over time but maintains healthy scepticism
- Tension with Ben on when to let CSMs loose

**Stacy Dixtra (Data & Reporting)**
- Defines what the numbers mean. Writing insurance migration BRD.
- Cautious: warns about "running fast and stepping back"
- Prefers Excel exports because "too much is changing"
- Currently reviewing analytics tab, testing reports section, and refining scorecard requirements

**Kathryn Palkovics (Data Alignment / COE Lead, referred to as "Catherine" in earlier transcripts)**
- Sense-checking complex accounts against Clara data
- Key contact for Gainsight team integration
- Can help with enterprise tools governance and reducing duplication

**George Dyke (CSM Leadership)**
- Organised Feb workshops where CLARA got hands-on CSM exposure
- Distinguishes CLARA scope (IRP migration) from Gainsight scope (overall health)
- Building separate account planner app -- related but distinct

**Peter Kimes (User Voice)**
- Wants User Voice data integrated into CLARA
- Detailed requirements captured. API integration preferred.

**Courtney (HD Models / Specialist)**
- Rich data on adoption barriers from 2000-3000 support case analysis
- Exploring how to surface aggregate themes in CLARA for product prioritisation

---

## Risks & Issues

### Active Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Azmain as single point of failure** | High | Chris onboarded for bug fixes. Nikhil at 50%. Two graduates arriving April. But Azmain still the only person who understands the full data model and feature architecture. No documentation existed until March user guide. |
| **BenVH as single point of failure for infrastructure** | High | CI/CD pipeline is stable. BenVH freed to focus on app factory. But if he's unavailable, no one else can deploy or fix infrastructure issues. Automating staging sync helps. |
| **Scope creep from integration requirements** | High | User Voice, HD models, Power BI, Gainsight, Salesforce, adoption charters -- all landing simultaneously. No formal prioritisation framework. Ben's wants vs Stacy's caution vs Natalia's process. |
| **Data quality undermining executive trust** | High | Scorecard numbers must be accurate. Four pre-2026 completions still unresolved. Stacy investigating. One wrong number reaching Andy Frappe or Diya could damage programme. |
| **Budget / token costs** | Medium | $750 in 3 days (Azmain, late Feb). Corporate budget $20K. Opus 4.6 is 3x more expensive. Budget reset 1 March but sustainable trajectory unclear. BenVH's phantom agent proposed for cost control. |
| **Gainsight could crush CLARA** | Medium | Gainsight team now engaged. If they decide CLARA functionality belongs in Gainsight, political dynamics shift. Azmain's explicit position: "they could crush us, so keep them on our good side." CLARA to adapt to Gainsight architecture, not vice versa. |
| **Sales Recon convergence timeline unclear** | Medium | Agreed end-state is migration to Sales Recon by end of FY26. But Jamie's team is small. CLARA investment may need to continue longer than planned. |
| **Internal team dynamics / credit attribution** | Medium | Nikhil perceived as overwriting BenVH's work on app factory. Rhett building adoption charter Excel without consensus. Multiple people presenting others' work. Could affect morale and retention. Richard reportedly exploring opportunities outside Moody's. |
| **Security concerns from personal accounts** | Low (mitigated) | Previously using personal Claude/Cursor accounts for Moody's work. Security audit flagged it. Bedrock API access now available. Personal account usage should be phased out. |

### Historical Issues (Resolved or Mitigated)

| Issue | Date | Resolution |
|-------|------|------------|
| Azure deployment blocked | 7 Jan | Pivoted to AWS |
| Cursor premium token limits | 8-9 Jan | Corporate budget increased; Bedrock access secured |
| Build failures (6 of 186 tests failing) | 15 Jan | Resolved by BenVH |
| ALB routing issues | 15 Jan | Resolved by BenVH |
| Data loss incident | 2 Feb | Commitment to preserve data. Backup process improved. |
| Blockers page making 60+ API calls | 20 Feb | Optimised to single batch call |
| 113 Alembic migration heads | Mar 2026 | Squashed to one base level (in staging) |

---

## Open Questions

1. **Pre-2026 completions:** Should QBE, ROI, La Previsora, and Ms Transverse count in 2026 scorecard numbers? Stacy investigating. Natalia inclined not to count them. Decision needed before scorecard goes live.

2. **Gainsight integration scope:** First meeting week of 10 March. What does a small POC look like? What data flows where? Does CLARA maintain its own data store or feed into Gainsight? Authentication model (SSO, REST, API keys)?

3. **Salesforce programmatic access:** Previously blocked. Being raised in same Gainsight meeting. Required for Bernard's and Courtney's projects as well as Kevin Pern's CS Agent.

4. **Adoption charter parsing approach:** How to handle Word documents with embedded images, diagrams, delivery plans. OCR / multi-modal AI needed. Rhett's Excel approach not coordinated with agreed Word-to-app flow. Richard integrating but complexity remains.

5. **Andy Frappe follow-up:** Demo happened 20 Feb. What was the specific reaction? Any new mandates beyond Power BI dashboard?

6. **CDK vs CloudFormation:** Infrastructure-as-code debate unresolved. Affects who can deploy and deployment reliability.

7. **Parent/subsidiary rollup fix:** Issue identified at Feb workshop. Fix status unknown.

8. **Long-term resourcing:** Azmain stretched across programme management and development. Promotion being held over his head. Richard reportedly exploring opportunities outside Moody's. If either leaves, programme faces significant knowledge loss.

9. **App factory governance:** Who approves what goes into app factory? Azmain raised need for approval board. Kathryn Palkovics offered to help with governance framework. No formal process yet.

10. **LLM worker architecture:** How will multiple apps (CLARA, Stacy's app, Amanda's, Rhett's, others) spin up AI agents? Per-OU IAM roles proposed for cost allocation. BenVH's phantom agent solution under discussion but not yet introduced to leadership.

---

## Transcript References

All transcripts that touch CLARA, organised chronologically with brief relevance notes.

### January 2026

| Date | Transcript | CLARA Relevance |
|------|-----------|-----------------|
| 6 Jan | `06-01-2026_-_Ben_explains_new_dashboard.txt` | Ben's original demo of the Christmas build. Foundational. |
| 6 Jan | `06-01-2026_-_AI_PM_Discussion_w_Richard.txt` | Richard frames the programme; CLARA is project 2. |
| 7 Jan | `07-01-2026_-_Architecture_review_-_IRP_Adoption_Tracker_deployment_constraints.txt` | Azure blocked. Pivot to AWS decided. |
| 7 Jan | `07-01-2026_-_IRP_Admin_Support_-_PM_Touchpoint.txt` | Migration target dates, reporting cadence. Context for CLARA's data model. |
| 8 Jan | `08-01-2026_-_Chat_with_Rich_Martin.txt` | Technical setup discussions. Azmain learning Git. |
| 8 Jan | `08-01-2026_-_Chat_with_Ben_Rich.txt` | Deployment debugging and planning. |
| 8 Jan | `08-01-2026_-_Adoption_Tracker_-_deployment_to_AWS.txt` | AWS deployment work begins. |
| 9 Jan | `09-01-2026_-_AWS_Deployment_of_Adoption_tracker.txt` | Continued deployment debugging. |
| 9 Jan | `09-01-2026_-_AI_Licenses_Request.txt` | Cursor budget and Claude Code access discussion. |
| 9 Jan | `09-01-2026_-_Chat_with_Richard.txt` | Data model and deployment planning. |
| 12 Jan | `12-01-2026_-_Program_Review_-_Rich.txt` | ROI framing, standalone architecture, Gainsight blocked. |
| 13 Jan | `13-01-2026_-_Tracker_Discussion.txt` | Real data vs synthetic decision. Data strategy debate. |
| 14 Jan | `14-01-2026_-_Catchup_x_Ben_Rich_6pm.txt` | App deployed to AWS. Demo planning. Feature phasing. |
| 15 Jan | `15-01-2026_-_Chat_with_Richard_1.txt` through `_6.txt` | Multiple debugging sessions. Build failures, schema mismatches, ALB routing. |
| 15 Jan | `15-01-2026_-_Tracker_demo_to_advisory_team.txt` | First external demo. Stacy, Liz, Christine, Steve Gentilli feedback. |
| 16 Jan | `16-01-2026_-_Demo_and_Feedback_from_Josh_E.txt` | Josh Ellingson's critical feedback. Data accuracy concerns. |
| 19 Jan | `19-01-2026_-_Deployment_Database_Synchronization_Debugging_Session.txt` | Database sync issues. Alembic migrations not propagating. |
| 19 Jan | `19-01-2026_-_Deployment_Troubleshooting_Database_Connectivity_Review.txt` | Continued deployment debugging. |
| 20 Jan | `20-01-2026_-_Programme_Alignment_and_Stakeholder_Readiness_Meeting.txt` | Diya prep. Elevator pitch strategy. |
| 21 Jan | `21-01-2026_-_Data_chat_with_richard.txt` | Data model and schema discussions. |
| 21 Jan | `21-01-2026_-_Data_input_call_with_PM_s.txt` | Data input hub explained to PMs (Vlad, Diana Kazakova-Ivanova). |
| 21 Jan | `21-01-2026_-_Portfolio_Review_-_new_process_w_Nat_BenB.txt` | Portfolio Review structure designed with Natalia and Ben. |
| 22 Jan | `22-01-2026_-_Chat_with_Rich_-_Diya_s_priorities.txt` | Diya's priorities sought. Sales Recon convergence question. |
| 23 Jan | `23-01-2026_-_chat_with_ben.txt` | UI cleanup before launch. |
| 23 Jan | `23-01-2026_-_chat_with_richard.txt` | Team member assignment. Database migration risks. |
| 23 Jan | `23-01-2026_-_portfolio_review_contd.txt` | Continued review meeting prep. |
| 23 Jan | `23-01-2026_-_Portfolio_review_call_discussion_w_Nat_Ben.txt` | Natalia reviews deck. Data entry instructions finalised. Name solicitation launched. |
| 23 Jan | `23-01-2026_-_Next_steps_on_dev_work_w_RIch.txt` | Development priorities and planning. |
| 23 Jan | `23-01-2026_-_Pre-Monday_Demo_Discussion.txt` | Prep for Portfolio Review launch. |
| 23 Jan | `23-01-2026_-_Adoption_charter_w_Steve_Gentilli_.txt` | Adoption charter discussion. Decision to fold into CLARA. |
| 26 Jan | `26-01-2026_-_Chat_with_Rich___BenVH__2_.txt` | Database changes before launch. Dev/staging/prod need. |
| 26 Jan | `26-01-2026_-_IRP_Adoption_call_-_Intro__2_.txt` | FIRST LIVE PORTFOLIO REVIEW. Landmark session. |
| 26 Jan | `26-01-2026_-__IMP__SalesRecon__1_.txt` | Executive session. CLARA presented as interim solution. |
| 27 Jan | `27-01-2026_-_IRP_Tracker_next_steps__2_.txt` | Resource constraints. Azmain stretched. Dev environment needs. |

### February 2026

| Date | Transcript | CLARA Relevance |
|------|-----------|-----------------|
| 2 Feb | `02-02-2026_-_Adoption_Tracker_RBAC_Permissions_Debug.txt` | RBAC debugging. |
| 2 Feb | `02-02-2026_-_IRP_Priority_Accounts_Migration___Adoption_Review.txt` | First portfolio review. Data loss incident. |
| 2 Feb | `02-02-2026_-_RBAC___Authentication_Debugging.txt` | Authentication fixes. |
| 3 Feb | `03-02-2026_-_CSM_Dashboard_Permissions___Testing_Review.txt` | Dashboard permissions testing. Philip as test subject. Client-facing dashboard idea. |
| 3 Feb | `03-02-2026_-_Workshop_discussion_with_George__1_.txt` | George plans workshop. Clara hands-on sessions. CLARA vs Gainsight scope. |
| 4 Feb | `2026-02-04_-_Tracker_next_steps.txt` | Tracker feature planning. |
| 5 Feb | `2026-02-05_-_Portfolio_review_with_Natalia__1_.txt` | Priority redefined to 31 scorecard accounts. Filter/search requirements. |
| 5 Feb | `2026-02-05_-_Tracker_discussion_with_Josh.txt` | Josh/Kathryn Palkovics data alignment. CSM update requirements. |
| 5 Feb | `2026-02-05_Chat_with_Rich.txt` | Development planning. |
| 9 Feb | `2026-02-09_-_Monday_Tracker_Standup.txt` | Claude Code access. Data strategy reset. Dev/staging/prod plan. |
| 9 Feb | `2026-02-09_-_session_with_Josh_Kathryn.txt` | Action plans pushed to prod. Orphan data issues. |
| 11 Feb | `2026-02-11_13-30-56.txt` through `2026-02-11_16-33-16.txt` | CSM session with Naveen. Josh/Azmain data requirements. Sales Recon pilot. Divya governance. |
| 12 Feb | `2026-02-12_-_CSM_Workshop_Session_1.txt` | George's workshop. Broader collaboration discussion. |
| 12 Feb | `2026-02-12_-_CSM_Workshop_Session_2.txt` | Hands-on CLARA session. Data preservation commitment. Parent/subsidiary issues found. |
| 20 Feb | `2026-02-20_-_Chat_w_Liz__tracker_feedback_.txt` | Liz's usability feedback. |
| 20 Feb | `2026-02-20_-_Natalia_1-1.txt` | Azmain raises bandwidth constraint. Other workstreams stalled. |
| 20 Feb | `2026-02-20_-_tracker_stand_up.txt` | Andy Frappe demo prep. Orphan data fixes. API call optimisation. |
| 23 Feb | `2026-02-23_-_Meeting_with_Diya.txt` | Diya governance session. Three pillars. Resource plan. |
| 23 Feb | `2026-02-23_-_next_2_weeks_plan.txt` | 8-week priorities. Cursor budget crisis. |
| 23 Feb | `2026-02-23_-_tracker_standup.txt` | Standup and planning. |
| 25 Feb | `2026-02-25_-_Clara_Standup.txt` | Clara standup and feature discussion. |
| 26 Feb | `2026-02-26_-_AI_Infrastructure.txt` | Bedrock/Claude enablement. CDK vs CloudFormation. Non-prod account. |
| 26 Feb | `2026-02-26_-_Blockers_with_P_Kimes.txt` | User Voice integration requirements. |
| 26 Feb | `2026-02-26_-_Chat_with_Stacy.txt` | Migration dashboard. Power BI. Excel exports. Reports section. Data cleanup. |
| 26 Feb | `2026-02-26_-_HD_Models.txt` | HD model adoption barriers. How to surface in CLARA. |
| 26 Feb | `2026-02-26_-_Moodys_v_env_s_with_BenVH.txt` | BenVH's CICD orchestration. Deployment tooling. |

### March 2026

| Date | Transcript | CLARA Relevance |
|------|-----------|-----------------|
| 3 Mar | `2026-03-03 - GenAI Program Standup & Next steps.txt` | Chris and Nikhil onboarded. Work allocation: Chris on CLARA feedback/bugs, Nikhil 50% CLARA / 50% app factory. Feedback triage > blockers > adoption charters priority sequence. Bedrock API discussion. |
| 3 Mar | `2026-03-03 - Discussion with Ben VH.txt` | BenVH's phantom agent. LLM worker architecture for CLARA. Adoption charter complexity (images, diagrams). Multi-agent orchestration discussion. Team dynamics (Nikhil concerns). |
| 3 Mar | `2026-03-03 - Discussion with Ben VH 2.txt` | Phantom agent capabilities deep-dive. Cost control for LLM workers. Role-based agent provisioning. Not directly CLARA feature work but infrastructure that enables CLARA's AI integration. |
| 3 Mar | `2026-03-03 - AI Tool Development Meeting.txt` | Martin and Azmain discuss Build in Five, not directly CLARA. But touches on Cursor budget, model usage, and general development approach. |
| 4 Mar | `2026-03-04 - New migration dashboard w Stacy Natalia (1).txt` | Key CLARA session. Scorecard tab requirements. Hosting Plus / RBO consolidation. Grey box removal. Actuals YTD. Quarterly view. Pre-2026 completions debate. Reports filter bugs. Analytics tab review. Chris joining for bug fixes. |
| 5 Mar | `2026-03-05 - Clara standup (1).txt` | Work allocation: Chris on defects, Richard testing Rhett's adoption charter work, Azmain on migration burn-down and management dashboard. Chris getting CLARA running locally. User documentation generated. CI/CD walkthrough planned. |
| 6 Mar | `2026-03-06 - Chat with Chris.txt` | Chris working through feedback backlog. Most early-Feb items already fixed. Bug fixes are "nice to have" -- critical items already done. Two graduates arriving April for ongoing maintenance. Bedrock API key working. Personal Claude accounts flagged by security audit. |
| 6 Mar | `2026-03-06 - Chat with BenVH.txt` | BenVH concerns about Nikhil. App factory protection. Automated staging sync script. Friday repo deployment. Team dynamics and credit attribution. |
| 6 Mar | `2026-03-06 - Pre Gainsight team meeting.txt` | Kathryn Palkovics, Richard, Azmain, BenVH, Chris pre-align before Gainsight meeting. CLARA to adapt to Gainsight architecture. Salesforce access to be raised. Governance framework discussion. |
