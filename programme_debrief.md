# Customer Success Gen AI Programme — Comprehensive Debrief

**Period covered:** 6 January 2026 – 27 February 2026  
**Total transcripts analysed:** 85  
**Prepared for:** Claude Code project onboarding  

---

## Table of Contents

1. [Programme Genesis & Context](#1-programme-genesis--context)
2. [Week-by-Week Chronology](#2-week-by-week-chronology)
3. [Workstream Evolution Summary](#3-workstream-evolution-summary)
4. [Key Stakeholder Map & Dynamics](#4-key-stakeholder-map--dynamics)
5. [Critical Decisions & Turning Points](#5-critical-decisions--turning-points)
6. [Unresolved Threads & Open Questions](#6-unresolved-threads--open-questions)

---

## 1. Programme Genesis & Context

The programme originated from Azmain being asked to create a 30-slide presentation for Diya — one slide per customer — summarising adoption status across the portfolio. Rather than building it manually from the various Excel sheets, Azmain used Cursor to generate a dashboard that surfaced all the data for senior leadership in one place. That single act of automation became the proof point that something much bigger was possible. It snowballed into Copilot Studio experiments, Cursor training sessions, and eventually a formal programme with six workstreams.

Ben Brooks independently built the first version of what became CLARA over Christmas 2025 — he spent evenings in Cursor building a process management system because the existing approach (Stacy managing 300-slide PowerPoint decks, fire drills to find account statuses, five people scraping data from spreadsheets) was unsustainable. His core insight: the team was collecting data to answer questions rather than structuring data to be queried.

The formal programme structure was established at the December 2025 steerco, where Richard presented the five (later six) workstreams. The steerco feedback was that training should be elevated to its own workstream, making it six total.

---

## 2. Week-by-Week Chronology

### Week 1: 5–9 January 2026

**Key files:** `06-01-2026_-_Ben_explains_new_dashboard.txt`, `06-01-2026_-_AI_PM_Discussion_w_Richard.txt`, `07-01-2026_-_Architecture_review_-_IRP_Adoption_Tracker_deployment_constraints.txt`, `07-01-2026_-_Advisory_weekly_project_review.txt`, `07-01-2026_-_IRP_Admin_Support_-_PM_Touchpoint.txt`, `08-01-2026_-_Chat_with_Rich_Martin.txt`, `08-01-2026_-_Chat_with_Ben_Rich.txt`, `08-01-2026_-_Adoption_Tracker_-_deployment_to_AWS.txt`, `09-01-2026_-_AWS_Deployment_of_Adoption_tracker.txt`, `09-01-2026_-_AI_Licenses_Request.txt`, `09-01-2026_-_Chat_with_Richard.txt`

**What happened:**

- **Ben Brooks demos the tracker to Azmain and Richard (6 Jan).** Ben walks through the app he built over Christmas: dashboard, use cases, blockers, action plans, data quality views. Richard recognises this as breaking the golden source (O&M spreadsheet) into a proper data model. Key concepts established: migration vs adoption distinction, migration-critical workflows, RAG status, the "Let's Go" culture prompt. Ben proposes natural language querying and a report builder.

- **Richard frames the programme for Azmain (6 Jan).** Six projects laid out: (1) Training & Enablement, (2) PMO Dashboard / Tracker, (3) Customer Success Agent (Kevin Pern's Copilot Studio work), (4) Adoption Charter Workflow, (5) IRP Navigator L1 Automation, (6) Cursor for Pipeline Sales. Richard explicitly positions this as a career growth vehicle for Azmain — getting elevation, visibility with Colin Holmes, building PM competencies. The North Star is a full customer journey system from prospect to renewal.

- **Azure deployment hits brick wall (7 Jan).** Architecture review call with security/infra teams. The app needs a front end, Python API, and SQL database behind SSO. Azure networking and security restrictions block progress. Adrian Thomas and the cyber architecture team (Brandon Smith) are unable to resolve in the meeting. Decision made to pivot: deploy on AWS immediately rather than wait for Azure clearance. BenVH begins AWS deployment work.

- **Advisory weekly project review (7 Jan).** Diana runs through active advisory projects — Treaty IQ, Morgan Stanley, Golden Bear, Aspen, AXA. Unrelated to CLARA directly but gives context of the broader advisory workload. Stacy mentions losing SurveyMonkey access.

- **IRP Admin Support PM Touchpoint (7 Jan).** Sneha/Stacy discuss reporting cadence — skipping January report, running next report on the 20th. Migration target dates being added to templates for the Moody's scorecard. Adoption charter tracking going to bi-weekly. Assignments being updated after CSM departures (Matt Novak, Philip Oliver to advisory, Christina Panola returning).

- **Technical troubleshooting sessions (8-9 Jan).** Multiple calls with Richard, Azmain, Martin, and BenVH debugging deployment. Azmain is new to Git, doesn't have it installed. Martin helps with the technical setup. They struggle with the build — missing files, import resolution errors. Richard hits Cursor premium limits. They run out of tokens. Conversation with Divya about AI licences: Cursor Pro gate blocking agent workflows, $10K corporate budget is insufficient across 1200 users, Anthropic/Claude Code access can be via AWS Bedrock. Richard told to contact Dennis Clement for Claude Code access.

- **Data model work begins.** Richard creates an updated data model with acceptance criteria, projects, action plans, blockers, milestones. Azmain begins mapping the December golden source to the new schema. Decision: use SQL Server on AWS RDS for speed; can migrate to Postgres/DynamoDB later.

**Key tensions surfacing:**
- Speed vs stability — Ben wants the app deployed immediately; database schema changes keep breaking things
- Real data vs synthetic data — Ben worried CSMs will reject demo if they see fake data
- Access/tooling constraints — Cursor token limits, no Claude Code access, Azure security blocks

---

### Week 2: 12–16 January 2026

**Key files:** `12-01-2026_-_Program_Review_-_Rich.txt`, `12-01-2026_-_Review_Agenda_for_Sales_Recon.txt`, `13-01-2026_-_Tracker_Discussion.txt`, `14-01-2026_-_AI_Training_DIscussion.txt`, `14-01-2026_-_Catchup_x_Ben_Rich_6pm.txt`, `14-01-2026_-_Chat_with_Ben_B.txt`, `15-01-2026_-_Chat_with_Richard_1.txt` through `_6.txt`, `15-01-2026_-_Tracker_demo_to_advisory_team.txt`, `16-01-2026_-_Demo_and_Feedback_from_Josh_E.txt`

**What happened:**

- **Programme ROI framing (12 Jan).** Richard and Azmain discuss how to message the programme's value. Ben's framing: value-at-risk model — 30+ implementations at risk without governance tooling. Azmain's framing: 30-40% CSM capacity unlock. Gainsight integration discussed — Natalia Plant's team blocked API access pending security review, likely not before March. Decision: build standalone, plan convergence later. Richard raises Sales Recon as the longer-term platform.

- **Sales Recon executive meeting prep (12 Jan).** First meeting with Jamie (Sales Recon lead), Conrad, Idris (banking equivalent), Chiara. Agenda for the 26 Jan executive session with Ari Lahavi, Colin Holmes, Mike Steele established. Jamie confirms "Intelligence Anywhere" (Salesforce data surfaced into Copilot) is on the Q1 roadmap. Scepticism from Bernard about whether it will actually deliver by end of Q1.

- **Data strategy debate (13 Jan).** Ben insists on using real data for demos — synthetic data will cause CSMs to fixate on errors rather than the system. Decision: use golden source data, acknowledge gaps, and have CSMs fill in the rest. Azmain proposes building a front-end data input form rather than sharing raw Excel.

- **AI Training Discussion with Colin, Pietro, Stephanie (14 Jan).** Colin Holmes (very senior) explains the insurance-wide AI steerco established mid-2025 at Diya/Mike's request. Purpose: inventory AI activities, prioritise for 2026, establish evaluation framework, improve cross-functional collaboration. Pietro (learning specialist) advises against starting with training — start with identifying AI capabilities needed per project, then assess team proficiency, then design learning. Stephanie emphasises measuring success with clear KPIs. Azmain proposes solution-focused training buckets (dashboarding, presentations, etc.) rather than tool-focused training. Train-the-trainer approach discussed for scale.

- **App deployed to AWS (14 Jan evening).** BenVH gets the CICD pipeline working. Advisory app factory URL established. Richard, Ben, and Azmain plan the demo for the advisory team. Ben wants to phase features: first nail use cases, blockers, data issues, action plans, team members — then move to charters and blueprints.

- **Continuous debugging (15 Jan).** Multiple calls throughout the day — fixing build failures (6 of 186 API tests failing), database schema mismatches, deployment pipeline issues. BenVH resolves ALB routing issues. Azmain learning Git branching, CI/CD concepts in real-time. Richard pushing for developer laptop approval for Azmain.

- **Demo to advisory team — Stacy, Liz, Christine, Steve Gentilli (15 Jan).** First external demo of the tracker. Key feedback: Liz asks about sold vs unsold customers (Ben: "sold only, no sales tracking yet — that would cause a mass freak out"). Stacy concerned about data quality — wants guidance on what good blockers look like. Steve Gentilli asks for dropdown categorisation on blockers to enable grouping and reporting. Ben proposes v2 feature: run blockers through Anthropic API to validate quality.

- **Josh Ellingson feedback session (16 Jan).** Critical stakeholder engagement. Josh's key concern: data interpretation accuracy — "I don't want Andy Frappe seeing one piece of data that's interpreted incorrectly and we can't get them off of it." Josh is bullish on the tool's potential but cautious about release timing. He and Ben have "slight disagreements" on when to let CSMs loose. Josh proposes a CSM-wide demo session before opening for feedback. Azmain proposes replacing the AI chatbot with a feedback button that captures screenshots.

**Key evolution:**
- The app went from local-only to deployed on AWS with CI/CD
- First real stakeholder feedback collected
- Data quality emerges as the defining challenge — not features
- Ben's phasing strategy crystallises: data infrastructure first, features second

---

### Week 3: 19–23 January 2026

**Key files:** `19-01-2026_-_Account_Planner_w_George_D.txt`, `19-01-2026_-_Customer_Success_Sales_Recon_Roadmap_Alignment___Pre-Meeting_Preparation.txt`, `19-01-2026_-_Deployment_Database_Synchronization_Debugging_Session.txt`, `19-01-2026_-_Deployment_Troubleshooting_Database_Connectivity_Review.txt`, `20-01-2026_-_Programme_Alignment_and_Stakeholder_Readiness_Meeting.txt`, `21-01-2026_-_Data_chat_with_richard.txt`, `21-01-2026_-_Data_input_call_with_PM_s.txt`, `21-01-2026_-_Portfolio_Review_-_new_process_w_Nat_BenB.txt`, `21-01-2026_-_Review_Slides_for_Sales_Recon_Executive_Meeting.txt`, `22-01-2026_-_Chat_with_Rich_-_Diya_s_priorities.txt`, `22-01-2026_-_Richard__George_-_SalesRecon_Decision_Prep.txt`, `23-01-2026_-_chat_with_ben.txt`, `23-01-2026_-_chat_with_richard.txt`, `23-01-2026_-_portfolio_review_contd.txt`, `23-01-2026_-_Portfolio_review_call_discussion_w_Nat_Ben.txt`, `23-01-2026_-_Next_steps_on_dev_work_w_RIch.txt`, `23-01-2026_-_Pre-Monday_Demo_Discussion.txt`, `23-01-2026_-_Adoption_charter_w_Steve_Gentilli_.txt`

**What happened:**

- **George Dyke onboarded to Cursor (19 Jan).** Richard walks George through building an account planner app in Cursor. Ben comments on the cultural resistance to rapid iteration: "I've spent an hour and a half on the phone with Charlotte talking about, just do it, press the button... and she was like, Oh, what do I do? Am I allowed?"

- **Sales Recon executive meeting prep (19 Jan).** Full prep call with Conrad, Idris, Jamie. Slide deck reviewed. Key message alignment: this isn't a new initiative — it started with June workshops. Jamie confirms his team is ramping down from sales kickoff work and can start thinking about CS requirements. The presentation structure: Jamie does Sales Recon overview → CS team presents pain points and requirements → banking requirements overlap → priority decisions → 90-day action plan.

- **More deployment debugging (19 Jan).** Database synchronisation issues — Azmain's front-end changes deployed but database schema changes didn't propagate. The Alembic migration process isn't syncing to production. Richard walks Azmain through AWS CloudWatch logs and debugging. Fundamental issue: not all stack components deploy automatically.

- **Diya prep and stakeholder readiness (20 Jan).** Richard explains Diya's communication style to Azmain: "She's not going to have time to sit with you and go over the detail... She starts looking at her phone. She's scrolling." The strategy: elevator pitch, not detailed walkthroughs. Richard frames the programme's origin story for Diya around Salesforce data access (note: the actual origin was Azmain's dashboard built to replace Stacy's 30-slide deck — Richard's retelling reframes it through Diya's lens). Planning to meet Diya Thursday to get her priority input.

- **Data input hub created (21 Jan).** Azmain builds a dedicated data input section overnight using Claude. Call with PMs (Vlad, Diana) to explain the approach: go through accounts with CSMs, fill in easy data live, ask them to handle time-consuming entries. Vlad asks about timeline — Azmain says priority accounts need defining by Natalia/Ben first.

- **Portfolio Review structure defined (21 Jan).** Critical design meeting with Natalia, Ben, Azmain. Ben proposes meeting structure: timeline → action owners → knowledge gaps → accelerate. Natalia insists priority accounts always discussed regardless of status. She pushes back on a separate Portfolio Review tab — wants to use existing dashboard/filters to demonstrate tool usability during the meeting. She specifically does not want editing during the meeting ("It takes too much time and makes it unclear who's responsible for updates"). CSM instruction agreed: "Set up a meeting with the people that have been involved, 20-minute meeting, fill out the data together."

- **Sales Recon slides reviewed with Bernard (21 Jan).** Bernard (Life team) provides customer success perspective on Sales Recon — wants 360-degree account view, not just product-specific. Richard confirms "Intelligence Anywhere" API is on Q1 roadmap. Bernard sceptical about Q1 delivery. Discussion of Midas (Life usage platform) and whether it's in scope for data pipeline.

- **Diya's priorities sought (22 Jan).** Richard sets up a call but Diya can't join. Richard pre-fills priority slides: (1) CS managers pulling data from Salesforce, (2) Adoption tracker, (3) Account planning workflow. Key question for Diya: Can we get agreement that the CS workflow application migrates to Sales Recon by end of FY26? If Jamie says no, then Ben needs a dedicated maintenance team.

- **UI cleanup and prep for Monday launch (23 Jan).** Multiple calls fixing dashboard display issues — red backgrounds confused with RAG statuses, stale update indicators, duplicate colour coding. Ben identifies specific visual bugs. Azmain and Richard work on team member assignment without adding database fields (to avoid breaking deployment). Richard warns: "We're gonna add a field, the database migration thing's gonna break, we're gonna spend ages with Ben debugging."

- **Portfolio review meeting structure finalised (23 Jan).** Natalia reviews the deck with Ben and Azmain. Ben's opening speech scripted. Data entry instruction: "CSMs, set up a meeting with your squad. We've already put the golden source data in — we're not asking for new data entry." Name solicitation for the tool launched (eventually becomes "CLARA").

- **Adoption charter discussion with Steve Gentilli (23 Jan).** Steve describes current adoption charter process and pain points. This workstream is being folded into the tracker rather than built separately.

**Key evolution:**
- Portfolio Review process designed and ready for launch
- Data input hub built — shift from "fill in Excel" to "fill in app"
- Diya engagement planned but not yet completed
- Sales Recon executive meeting fully prepped
- Tech debt accumulating rapidly from speed of development

---

### Week 4: 26–30 January 2026

**Key files:** `26-01-2026_-_Chat_with_Rich___BenVH__2_.txt`, `26-01-2026_-_IRP_Adoption_call_-_Intro__2_.txt`, `26-01-2026_-__IMP__SalesRecon__1_.txt`, `27-01-2026_-_IRP_Tracker_next_steps__2_.txt`, `27-01-2026_-_Partners_workflow_workshop__1_.txt`

**What happened:**

- **Monday deployment before Portfolio Review launch (26 Jan).** BenVH and Azmain work through database changes — employee import, account team mapping. Richard insists on keeping changes separate to avoid breaking prod. The team discusses need for multiple environments (dev/staging/prod) now that real users are entering data.

- **PORTFOLIO REVIEW LAUNCHES — First IRP Adoption Call (26 Jan).** Landmark session. Natalia presents the running agenda structure. Ben gives the overview speech: building blocks (training, charters, blueprints, solution fit, teams) are now mature enough to be woven together into a structured collaboration process. Diya speaks — positions this as critical to the insurance scorecard and Andy Frappe's visibility requirements. She says: "There is both an expectation, but if I were you, I would really think about leaning in and being excited." Natalia opens CSM name nominations for the tool. Azmain demos the app with Ben narrating. This is the first time the broader CSM team sees the tool.

- **SALES RECON EXECUTIVE SESSION (26 Jan).** Meeting with Ari Lahavi, Jamie, Colin Holmes, Mike Steele, Diya, Idris, Bernard, Conrad. Insurance and banking teams present CS requirements to Sales Recon. Key outcomes: alignment on CS as the next priority after sales, Intelligence Anywhere confirmed on roadmap. Richard presents CLARA as the interim solution. George's RMB account planner also shown. The session establishes that CS workflow incorporation into Sales Recon is the target end-state, but standalone CLARA is needed in the meantime.

- **Next steps and resourcing (27 Jan).** Richard flags that Azmain has been 100% on CLARA with no time for programme management. Martin is back from holiday — decision needed: double down on tracker features or start platform work (generic app builder, release pipeline). Ben wants a curated data set within two weeks. Richard pushes for project hygiene — PID still not finalised, stakeholder mapping incomplete.

- **Partners workflow workshop (27 Jan).** Brief session about partner tracking requirements for the tracker — Alexandra and Liz need to see which use cases are using which implementation partners.

**Key evolution:**
- Tool goes live with real users for the first time
- Executive visibility achieved through Sales Recon session
- Resource constraints becoming acute — Azmain stretched too thin
- Need for dev/staging/prod environments now urgent

---

### Week 5: 2–5 February 2026

**Key files:** `02-02-2026_-_Adoption_Tracker_RBAC_Permissions_Debug.txt`, `02-02-2026_-_IRP_Priority_Accounts_Migration___Adoption_Review.txt`, `02-02-2026_-_RBAC___Authentication_Debugging.txt`, `03-02-2026_-_CSM_Dashboard_Permissions___Testing_Review.txt`, `03-02-2026_-_Workshop_discussion_with_George__1_.txt`, `2026-02-04_-_AI_discussion_with_Asset_Management.txt`, `2026-02-04_-_SalesRecon_Process_Coordination.txt`, `2026-02-04_-_Tracker_next_steps.txt`, `2026-02-05_-_Portfolio_review_with_Natalia__1_.txt`, `2026-02-05_-_Programm_call_x_Martin__1_.txt`, `2026-02-05_-_Tracker_discussion_with_Josh.txt`, `2026-02-05_Chat_with_Rich.txt`

**What happened:**

- **RBAC and permissions debugging (2 Feb).** Multiple sessions debugging role-based access control. BenVH resolves authentication issues. Users testing — Philip used as test subject. The team discovers that CSM-entered data was lost over the weekend due to a deployment refresh. This causes significant trust damage: Diya notes in the Portfolio Review that CSMs entered data Friday through Monday morning and it disappeared. George Dyke asks for a hands-up to gauge the scale of data loss.

- **FIRST LIVE PORTFOLIO REVIEW (2 Feb).** Natalia runs the inaugural review using the tool. She walks through nine priority accounts. Rhonda gives the first live account update (Aeon — 4+ years on platform, North America team now migrating, one red use case is a legacy exposure add-on that's no longer relevant). The data loss issue dominates — multiple CSMs report entries disappeared after refresh. Azmain confirms the issue and promises it won't recur.

- **CSM dashboard and permissions testing (3 Feb).** Philip Garner asks about client-facing transparency dashboard — can they share a live view with customers showing defect/feature tracking progress? Richard explains the product alignment challenge and Alicia's (PM) openness to requirements traceability. Testing continues with RBAC — Azmain removes himself from admin to simulate CSM experience.

- **Workshop planning with George (3 Feb).** George plans two-day CSM workshop. Clara is a key component — he wants hands-on data entry sessions where CSMs fix their own data in real time, with Azmain in the room to capture feedback and potentially fix things live. George distinguishes Clara's scope (IRP adoption/migration) from Gainsight's scope (overall customer health) — they overlap but are not the same.

- **Cross-OU AI discussion (4 Feb).** Richard and Azmain present to asset management colleagues (Amanda Fleming's team from KYC). KYC team has already automated their customer management on top of a database — they're ahead. Session about sharing coding standards and prompts across OUs.

- **Sales Recon process coordination (4 Feb).** Eight CSMs nominated across OUs for Sales Recon UAT pilot: Julia Fuller (casualty), someone from Life, Kevin Pern (Hossa), Azmain from the advisory side, plus solution architects. George coordinates.

- **Natalia's portfolio review requirements (5 Feb).** Detailed session with Natalia redefining what "priority" means — not the old high-priority list, but the 31 accounts on the 2026 migration timeline (scorecard target: 30 migrations). The 17 "accelerated" accounts are a subset needing special attention. Natalia wants to rotate focus: one week priorities, next week accelerated. She identifies specific filter/search gaps and asks for status vs stage distinction in the UI.

- **Martin onboarded to Build in Five (5 Feb).** Azmain and Martin discuss the Cursor for Pipeline project (later called "Build in Five"). The concept: build a framework that allows non-technical users to scope, design, and deploy apps on IRP's Risk Data Lake using Cursor in a controlled environment. Both admit they don't fully understand the end goal and need more input from Richard.

- **Josh/Catherine data alignment (5 Feb).** Richard's plan: Catherine takes the most complex accounts (reinsurer, primary, broker, global entity), does a side-by-side comparison of Salesforce vs Clara data, signs off in a spreadsheet, then data gets loaded. Goal: tackle 80-90% of data mapping issues in one pass. Azmain's frustration with Josh/Catherine's pushback on data they themselves provided: "I don't know how many times you can tell the same thing to people, especially the person that gave you the data."

**Key evolution:**
- Data loss incident damages credibility with CSMs — critical trust issue
- Priority definition shifts from arbitrary "high priority" to scorecard-aligned 31 accounts
- Cross-OU interest growing — KYC, Asset Management, Banking all engaging
- Build in Five workstream begins to take shape with Martin

---

### Week 6: 9–12 February 2026

**Key files:** `2026-02-09_-_Monday_Tracker_Standup.txt`, `2026-02-09_-_Next_Steps.txt`, `2026-02-09_-_session_with_Josh_Kathryn.txt`, `2026-02-11_13-30-56.txt`, `2026-02-11_13-59-58.txt`, `2026-02-11_15-31-58.txt`, `2026-02-11_16-16-12.txt`, `2026-02-11_16-33-16.txt`, `2026-02-12_-_CSM_Workshop_Session_1.txt`, `2026-02-12_-_CSM_Workshop_Session_2.txt`

**What happened:**

- **Claude Code access secured (9 Feb).** Richard confirms they'll be onboarded to the Claude Code pilot via AWS. Not the desktop interface — they'll connect Claude Code to the AWS environment. Both Richard and Azmain running out of personal subscriptions.

- **Data strategy reset (9 Feb).** Richard's plan: Catherine must take complicated accounts and sense-check against Clara data this week. If it reveals schema changes needed, they handle Wednesday. Goal: build to dev Monday, staging Thursday, prod Thursday. "If we don't tackle it holistically, all that's going to happen is every week there's a new schema change, a new data fix, and that's all we'll be doing."

- **Josh and Catherine session (9 Feb).** Action plans pushed to prod. Catherine finding data that vanished after computer upgrade. The orphan data and action plan visibility issues identified — front-end filter blocking action plans from displaying. Josh starting to engage but remains cautious about CSM data entry.

- **Diana discusses ILS team (11 Feb).** Diana explains she's helping the ILS (cat bond) team adopt basic Microsoft tools — they didn't even use Teams. Building them lists and Power BI reporting. Shows how far behind some teams are on basic tooling.

- **Individual CSM session with Naveen (11 Feb).** Azmain does one-on-one onboarding with a CSM from Arkansas. Practical issues surface: Salesforce name mismatches (three names vs two fields), CSM confusion about status vs RAG status fields.

- **Sales Recon pilot kickoff (11 Feb).** Cara (from Jamie's team) launches the two-week Sales Recon zero pilot with 8 CSMs. Testing period: 11-24 Feb. Three features to evaluate: account intelligence, meeting preparation agent, share knowledge agent. Feedback tracker built. Post-pilot interviews scheduled. Bernard asks about timeline — when will first CS version ship?

- **Meeting with Divya on AI programme governance (11 Feb).** Major alignment session. Idris explains the full context to Divya: RMS acquisition created a gap where insurance CS doesn't have Gainsight working, so Richard's team proactively built their own tool. Divya's key questions: (1) What are the efficiency metrics/KPIs? (2) Is Sales Recon the biggest bang for the buck, or are there other AI solutions to consider? (3) She wants the next meeting to be "more philosophical" about priorities. Richard agrees to provide directional KPIs.

- **Josh Ellingson and data requirements (11 Feb).** Josh and Azmain discuss what CSMs actually need to update weekly. Azmain pushes for identifying the most pertinent data points for regular updates rather than trying to maintain everything. Richard joins — the portfolio review is the big report; need to understand if Josh has additional metric requirements.

- **CSM Workshop Day 1 (12 Feb).** George's team workshop in London. Broader discussion about collaboration with sales, product teams, specialists. Communication gaps identified — CSMs didn't know about sales team restructuring (property workflow specialists becoming "relationship managers", casualty relationship managers, cyber possibly moving to casualty side).

- **CSM Workshop Day 2 — Clara hands-on session (12 Feb).** Azmain joins remotely. Key commitment: "Any updates you make from yesterday onwards will be preserved. We're no longer going to do any big update to wipe things." He flips the conversation bottom-up: "What's helpful for you guys?" Rather than top-down reporting requirements. Miles used as a guinea pig to walk through the CSM workflow. Parent/subsidiary account issues identified — updates to subsidiary accounts don't roll up to parent, making it look like the CSM hasn't updated.

**Key evolution:**
- Claude Code access finally secured
- Sales Recon pilot active — CS evaluation underway
- Divya formally engaged on programme governance
- CSM workshop reveals communication gaps and practical usability issues
- Trust rebuilding after data loss — explicit commitment that data will be preserved

---

### Week 7: 19–20 February 2026

**Key files:** `2026-02-19_-_App_development_with_Rhett.txt`, `2026-02-19_-_MCP_server_with_Cihan___Lonny.txt`, `2026-02-20_-_Chat_w_Liz__tracker_feedback_.txt`, `2026-02-20_-_Natalia_1-1.txt`, `2026-02-20_-_tracker_stand_up.txt`

**What happened:**

- **Rhett onboarded to app development (19 Feb).** Rhett (from consulting/tech team) being set up with GitHub, learning to push code. Richard explains the dual-purpose infrastructure: internal productivity apps AND customer-facing demo apps on IRP's Risk Data Lake. Standard tech stack and automated deployment pipeline is the goal so Ben doesn't become a bottleneck.

- **MCP server discussion with Cihan and Lonny (19 Feb).** Product team building MCP (Model Context Protocol) server for IRP Navigator. Nikhil (new tech consulting lead, replacing Alex) introduced. Azmain introduced as overseeing the Gen AI programme. Bala (also new) joining from banking/edfx. Early-stage collaboration on MCP between product and CS teams.

- **Azmain's workload conversation with Natalia (20 Feb).** Critical 1:1. Azmain flags that CLARA has consumed all bandwidth — the other five workstreams have had no meaningful progress. Richard warned this question is coming. Azmain walks Natalia through all six projects: (1) Training & enablement — biggest/quickest win, (2) CLARA — ongoing, (3) CS Agent (Kevin Pern) — needs engagement, (4) Adoption Charter — folding into CLARA, (5) IRP Navigator L1 — not fully understood, (6) Cursor for Pipeline. Natalia's advice and response not fully captured but the flag is raised.

- **Ben demos to Andy Frappe (20 Feb).** Ben drops a "surprise bomb" — he's meeting Andy Frappe (President of Moody's Analytics, one level below the board) on Monday to demo CLARA. Richard and Azmain scramble to fix orphan data and duplicate records. Azmain discovers the blockers page was making 60+ individual API calls; optimises to a single batch call.

- **Liz Couchman feedback session (20 Feb).** Starts with extended political discussion (Prince Andrew, US politics). Liz is solution architecture team — provides tracker feedback on specific accounts and usability.

**Key evolution:**
- Azmain formally raises bandwidth constraint with Natalia
- MCP server work begins — new capability area
- Andy Frappe exposure imminent — highest visibility moment yet
- New team members onboarding (Nikhil, Bala, Rhett)

---

### Week 8: 23–27 February 2026

**Key files:** `2026-02-23_-_Meeting_with_Diya.txt`, `2026-02-23_-_next_2_weeks_plan.txt`, `2026-02-23_-_tracker_standup.txt`, `2026-02-25_-_Clara_Standup.txt`, `2026-02-26_-_AI_Infrastructure.txt`, `2026-02-26_-_Blockers_with_P_Kimes.txt`, `2026-02-26_-_Chat_with_Asset_Management.txt`, `2026-02-26_-_Chat_with_Stacy.txt`, `2026-02-26_-_HD_Models.txt`, `2026-02-26_-_Moodys_v_env_s_with_BenVH.txt`, `2026-02-27_-_Build_in_Five_with_Martin.txt`

**What happened:**

- **MEETING WITH DIYA (23 Feb).** The long-awaited governance session. Richard presents three pillars: (1) Governance of IRP portfolio (CLARA + George's account planner), (2) Customer intelligence/Sales Recon alignment, (3) Platform enablement. Natalia contributes — suggests CLARA isn't IRP-specific, could be reused for other programmes (EGL, Hosted), but advises building for a specific programme first. Ben mentions taking the architecture to Christos's (Life) leadership team. Diya appears engaged. Discussion of getting Courtney or Carlin from specialist teams involved.

- **Resource plan for next 8 weeks (23 Feb).** Priorities: (1) Finish CLARA features — solution architecture/blueprint attachment flow, (2) Address CSM feedback (Chanel's issues from last week), (3) Platform infrastructure. Resource ask: Nikhol 50% time, Martin back from holiday, Chris 50%. Azmain pushes back on treating all feedback as equal: "We need to draw a line between this is needed and people just giving feedback because it's in-house and they can just change stuff." Ben's strategy: shopping around internally, getting Life MD to independently tell Diya to invest.

- **Cursor budget crisis (23 Feb).** Azmain used $750 in three days. Corporate budget increased from $10K to $20K but Opus 4.6 is 3x more expensive. Banking OU had a hackathon consuming tokens. Azmain downgraded to Sonnet 4.5 to manage costs.

- **AI Infrastructure planning (26 Feb).** Technical session with BenVH, Nicole, and others. Two objectives: (1) Cat Accelerate tech debt — need separate non-prod account, CDK vs CloudFormation debate, no deployment traceability, (2) AWS Bedrock/Claude model enablement for CLARA integration and Claude Code access for the team. Nicole identifies issues: manual Step Function deployment, no backup, no traceability. Discussion of whether to stay on CDK or move to simpler CloudFormation templates.

- **Peter Kimes — User Voice integration requirements (26 Feb).** Detailed requirements session. Peter, Stacy, Kevin Pern discuss bringing User Voice data into CLARA. Distinction: not all User Voice entries are blockers (some are nice-to-haves), but blocker-tagged items should be traceable. Azmain proposes creating a separate User Voice object rather than appending to blockers. API integration preferred over Excel dumps. Stacy cautions about "running really fast and taking steps back" — wants to think through the data model carefully.

- **Stacy — migration dashboard and reporting (26 Feb).** Andy Frappe saw banking's migration dashboard and wants all migrations reported centrally in Power BI. Banking has a full-time resource building their dashboard and wrote a formal BRD. Stacy writing insurance requirements into the banking BRD template. Asks Azmain for Excel exports from CLARA (not APIs — "too much is changing"). Azmain shows her the Reports section he built modelled on Salesforce's structure. Data cleanup still ongoing — CSMs nervous about deleting records, Azmain reassures with 24-hour backups.

- **HD Models discussion with Courtney (26 Feb).** Courtney's team analysed 2000-3000 HD-related support cases to identify adoption barriers. Two buckets: (1) enablement gaps — customers don't understand DLM-to-HD transition nuances, (2) product feature gaps. Richard identifies the disconnect: CLARA tracks migration (switching off Risk Link), while Salesforce cases tell a different, more granular story about HD adoption. Discussion of how to surface Courtney's aggregate analysis in CLARA — not necessarily per-account but thematic patterns for product prioritisation.

- **BenVH virtual environments (26 Feb).** BenVH shows Azmain his personal CICD orchestration project (patented). Discusses how it could apply to AI agent management. Practical issue: some team members (like George's team) don't know what Git is — the deployment tooling must be "idiot proof."

- **Build in Five with Martin (27 Feb).** Martin back from holiday. Build in Five targeting the March 21 exceedance event demo. Scope has expanded from the original concept. Martin and Azmain discuss the approach.

**Key evolution:**
- Diya governance session completed — three pillars established
- Resource plan formalised for next 8 weeks
- Multiple new integration requirements emerging: User Voice, HD model data, migration dashboard
- Infrastructure decisions pending: Bedrock, Claude Code, CDK vs CloudFormation
- Budget/token cost becoming a real constraint
- Build in Five demo target: March 21

---

## 3. Workstream Evolution Summary

### Workstream 1: Training & Enablement
- **Jan 6**: Identified as project one. Previous training in Dec 2025 with ~40 attendees from 80 registered.
- **Jan 14**: Deep planning session with Colin, Pietro, Stephanie. Shifted from tool-focused to solution-focused training. Competency assessment survey proposed.
- **Feb 20**: Azmain flags to Natalia that this has had no meaningful progress due to CLARA consuming all bandwidth.
- **Status by end of Feb**: Stalled. Conceptual framework exists but no execution.

### Workstream 2: CLARA (IRP Adoption Tracker)
- **Jan 6**: Ben demos Christmas build to Azmain/Richard. Local-only, SQLite.
- **Jan 7-9**: Azure blocked → pivot to AWS. CI/CD pipeline built. Data model redesigned.
- **Jan 13-15**: Multiple debugging sessions. First deployed to AWS. Advisory team demo.
- **Jan 16**: Josh Ellingson feedback — data interpretation accuracy is critical.
- **Jan 21**: Portfolio Review structure designed with Natalia. Data input hub built.
- **Jan 26**: FIRST LIVE PORTFOLIO REVIEW. Tool goes to full CSM team.
- **Feb 2**: Data loss incident damages trust. First real portfolio review with Natalia facilitating.
- **Feb 5**: Priority definition shifts to 31 scorecard migration accounts. Natalia's filter/search requirements captured.
- **Feb 9-12**: Claude Code access secured. CSM workshops — hands-on data entry. Parent/subsidiary issues found.
- **Feb 20**: Andy Frappe demo. Highest visibility achieved.
- **Feb 23**: Diya governance meeting. Resource plan for 8 weeks.
- **Feb 26**: User Voice integration, HD model data, and Power BI migration dashboard requirements all land simultaneously.
- **Status by end of Feb**: Live and stabilising. Data quality is primary focus. Feature backlog growing (User Voice, HD models, solution blueprints, partners, reports). Scorecard dashboard and migration burndown in development.

### Workstream 3: Customer Success Agent
- **Jan 6**: Kevin Pern identified as lead. Copilot Studio + Salesforce.
- **Feb 20**: Azmain tells Natalia it needs engagement — Kevin working alone, nothing operationalised.
- **Status by end of Feb**: Minimal progress. Kevin has a prototype but no programme oversight.

### Workstream 4: Adoption Charter Workflow
- **Jan 23**: Steve Gentilli session. Decision to fold into CLARA rather than build separately.
- **Feb 5**: Azmain confirms v1 of adoption charter section already built in CLARA; needs modification not greenfield work.
- **Status by end of Feb**: Partially folded into CLARA. Blueprint and charter flow still needs finalisation with Steve/Liz.

### Workstream 5: IRP Navigator L1 Automation
- **Jan 6**: Identified — use Navigator's upcoming API support to auto-answer L1 tickets.
- **Feb 19**: MCP server discussion with Cihan and Lonny begins.
- **Feb 20**: Azmain tells Natalia he doesn't fully understand it.
- **Status by end of Feb**: Early stage. MCP server work underway with product team. No CS-side build started.

### Workstream 6: Cursor for Pipeline Sales (→ Build in Five)
- **Jan 6**: Richard explains the concept — use Cursor in customer conversations to build apps on IRP live, demonstrating platform power as a sales tool.
- **Feb 5**: Martin and Azmain discuss the framework concept but both unclear on end goal.
- **Feb 27**: Martin begins work. Demo target: March 21 exceedance event.
- **Status by end of Feb**: Martin actively developing. Scope expanded from original concept. Demo in 3 weeks.

---

## 4. Key Stakeholder Map & Dynamics

### Decision Makers
- **Diya Sawhny** — Executive sponsor. Communication style: impatient with detail, wants elevator pitch, scrolls phone during long explanations. Feedback on sessions: "Should feel like continuation, not reset." Engaged properly by late Feb.
- **Ben Brooks** — De facto product owner/visionary. Built the original app. Pushes hard for speed. Key phrases: "Just do it, press the button." Wants to "kill CSMs with kindness." Running 5am training sessions. Races HighRox.
- **Natalia** — CS lead, Azmain's manager. Runs portfolio reviews. Practical, process-focused. Pushed back on separate portfolio review tab. Wants existing dashboard to demonstrate tool value. Key concern: CSM workload perception.
- **Richard Dosoo** — Programme/operational owner. Technical bridge between Ben's vision and Azmain's execution. Manages up to Diya, across to Sales Recon, down to dev team. Carries the deployment knowledge.

### Influential Stakeholders
- **Josh Ellingson** — CSM leadership. Gatekeeper for CSM adoption. Conservative — doesn't want bad data reaching Andy Frappe. "Slight disagreements" with Ben on release timing. Once bought in, provides strong feedback.
- **George Dyke** — CSM leadership (different team). Organised workshops. Building account planner app. Comfortable with ambiguity, pragmatic about getting things done.
- **Stacy Dixtra** — Data backbone. Manages the 300-slide reporting decks. Defines reporting requirements. Cautious but supportive — warns about "running fast and stepping back."

### Technical Team
- **BenVH (Ben Van Houten)** — Platform/infrastructure engineer. Runs AWS deployment, CI/CD pipeline, security. Showed personal patented CICD orchestration tool. Pushing for proper environments.
- **Martin Davies** — Developer, 12-week assignment. Building Build in Five. Football fan (Stockholms County). Collaborative.
- **Chris** — Developer handling bug fixes on CLARA.
- **Nikhil** — New tech consulting lead (replaced Alex). Recently joined from banking/edfx.

### External/Adjacent
- **Jamie** — Sales Recon lead. Supportive but constrained. His team is small and was consumed by Salesforce partnership.
- **Divya** — AI programme governance. Managing Cursor budgets, licences, cross-OU coordination. Key meeting on Feb 11 set expectations.
- **Ari Lahavi** — Head of Applied AI. Met in Jan 26 executive session. Team building Sales Recon.

---

## 5. Critical Decisions & Turning Points

1. **AWS over Azure (7 Jan)**: Unblocked deployment. Without this, the app would still be local-only weeks later.

2. **Real data over synthetic (13 Jan)**: Ben's insistence shaped the entire data quality journey. Painful but correct.

3. **Standalone-first architecture (12 Jan)**: Building independently of Gainsight/Salesforce enabled rapid iteration. Planned convergence later.

4. **Portfolio Review as the forcing function (21 Jan)**: Making CLARA the backbone of a weekly executive-visible process created urgency and adoption pressure simultaneously.

5. **Priority = scorecard migrations (5 Feb)**: Natalia's reframe from arbitrary "high priority" to the 31 scorecard-tracked accounts aligned the tool with what executives actually measure.

6. **Data loss incident (2 Feb)**: Damaged trust but forced the team to commit: "From yesterday onwards, everything persists."

7. **Diya governance session (23 Feb)**: Formalised three pillars and resource plan. Moved from ad-hoc to structured programme governance.

---

## 6. Unresolved Threads & Open Questions

1. **Gainsight integration timeline**: Charlotte's team owns this. March was mentioned as earliest engagement. No API access granted. What's the current status?

2. **Sales Recon pilot outcomes**: The two-week pilot (11-24 Feb) results should be in. What did CSMs think? Does it change the CLARA roadmap?

3. **AWS Bedrock / Claude Code rollout**: Access was secured in principle by Feb 9. Has the team actually onboarded? Are models integrated into CLARA?

4. **Scorecard target accuracy**: The 30-31 migration target for 2026 — is data now good enough to track against it? Are switch-off dates populated?

5. **Build in Five demo (March 21)**: Is Martin on track? Has the scope stabilised or is it still expanding?

6. **Kevin Pern's CS Agent**: Still operating independently. Has anyone engaged him formally?

7. **User Voice integration**: Peter Kimes' requirements were detailed. Has the data model been designed? Is API access available?

8. **Andy Frappe follow-up**: The demo happened. What was the reaction? Any new asks or escalations?

9. **Budget/token management**: $750 in 3 days is unsustainable. What's the resolution? Has the Moody's budget increased beyond $20K?

10. **Single points of failure**: BenVH for infrastructure, Azmain for CLARA features. What's the mitigation plan?
