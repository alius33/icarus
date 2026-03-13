# Decision Log

Last updated: 2026-03-10 (all transcripts through 10 March processed)

Decisions are listed chronologically. Each entry includes context and rationale where available.

---

| # | Date | Decision | Rationale | Key People |
|---|------|----------|-----------|------------|
| 1 | 7 Jan | Deploy on AWS instead of Azure | Azure networking/security restrictions blocked progress. Couldn't resolve in architecture review. AWS enabled immediate deployment. | Richard, BenVH, Adrian Thomas |
| 2 | 9 Jan | Use SQL Server on AWS RDS | Speed of setup. Can migrate to Postgres/DynamoDB later. | Richard, Azmain |
| 3 | 12 Jan | Build standalone, plan Gainsight convergence later | Gainsight API access blocked until March at earliest. Waiting would stall everything. | Richard, Azmain |
| 4 | 13 Jan | Use real data for demos, not synthetic | Ben argued CSMs would fixate on errors in fake data rather than evaluating the system. Painful but forced early data quality confrontation. | Ben Brooks |
| 5 | 14 Jan | Solution-focused training buckets over tool-focused | Training on "dashboarding" and "presentations" rather than "Cursor" or "Copilot." More transferable. | Azmain, Colin, Pietro, Stephanie |
| 6 | 19 Jan | Roll forward, not roll back on deployment issues | When CLARA's deployed version broke (schema out of sync), Richard insisted on pushing fixes forward rather than reverting. | Richard, Azmain |
| 7 | 19 Jan | Schema changes must ship with data fix scripts | Once users start entering production data, any schema change must include scripts to prime new tables/fields. Prevents empty-field deployments. | Richard, Azmain |
| 8 | 19 Jan | Remove "priorities" and "out of scope" slides from exec deck | Too early for priority decisions until Sales Recon pilot feedback gathered. Jamie will only present what is in scope. | Richard, Jamie |
| 9 | 20 Jan | Reframe programme origin story for Diya | Richard tells Diya the programme started from "how do I get data out of Salesforce?" — deliberately different from actual origin (Azmain's dashboard replacing Stacy's 30-slide deck). Tailored for executive audience. | Richard |
| 10 | 20 Jan | Freeze production once users start entering data | No more ad-hoc builds to production. BenVH to set up dev/test/prod environments. Prod deploys only once a week. | Richard, Azmain, BenVH |
| 11 | 21 Jan | Portfolio Review uses existing dashboard, not a separate tab | Natalia's insistence: demonstrate the tool's usability by using it live, don't build a special view. No editing during meetings. | Natalia |
| 12 | 21 Jan | CSMs fill data in the app, not Excel | Data input hub built. Shift from "fill in Excel and we'll import" to "fill in the app directly." | Azmain, Ben |
| 13 | 21 Jan | No data export from CLARA (intentional) | Forces users to stay in the platform rather than defaulting back to spreadsheets. Deliberate behaviour-change design. | Azmain |
| 14 | 21 Jan | Deploy to production at weekly frequency only | Once users are in the system, limit production deploys to prevent disruption. | Richard, Azmain, BenVH |
| 15 | 22 Jan | George's account planner integration deferred | Overlap with Sales Recon account planning discovered. Decision on folding into CLARA vs standalone deferred to next week. | Richard, George, Azmain |
| 16 | 23 Jan | Fold adoption charter workflow into CLARA | Rather than building a separate system (WS4), absorb charter functionality into the tracker. Steve's Excel has ~75% field overlap with CLARA. | Steve Gentilli, Azmain |
| 17 | 23 Jan | Adoption charter status field manual, not algorithmic | Number of criteria varies by customer, so status should be user-controlled rather than computed. | Steve, Azmain |
| 18 | 23 Jan | Strip dashboard colour confusion (red/green to blue/grey) | Red backgrounds confused with RAG status. Remove background colours, remove blue RAG pill, add data completeness labels. Migration critical/non-critical changed to blue/grey. | Ben, Azmain |
| 19 | 23 Jan | No schema changes until BenVH approves | After use case creation broke (500 errors from Alembic migration), all planned changes written as specifications only. Execution deferred to Monday morning with BenVH oversight. | Azmain, Richard |
| 20 | 23 Jan | Richard personally pays for Azmain's Claude Code Max subscription | Workaround for corporate Cursor block. Google SSO prevents credential sharing. | Richard |
| 21 | 23 Jan | Questions during Monday demo, not held to end | Natalia wanted 15 min intro + 30 min demo + 15 min Q&A. Azmain and Ben pushed for questions during demo for better engagement. | Azmain, Natalia, Ben |
| 22 | 23 Jan | CSMs take accountability for data updates but involve full account team | CSMs set up 20-minute meetings with solution architects, implementation leads, and PMs to fill out data together. CSMs own accountability, not sole execution. | Ben Brooks, Natalia |
| 23 | 23 Jan | Portfolio Review page: keep high priority, timeline, accelerate; remove action owners and knowledge gaps | Streamlined sections. Action owners and knowledge gaps covered naturally when discussing red accounts. | Ben, Natalia, Azmain |
| 24 | 26 Jan | CLARA is interim; target end-state is Sales Recon | Agreed at executive session with Ari, Jamie, Diya. CS workflow should migrate to Sales Recon by end of FY26, but standalone CLARA needed in the meantime. | Executive group |
| 25 | 5 Feb | Priority = 31 scorecard migration accounts | Natalia reframed from arbitrary "high priority" list to the accounts on the 2026 migration timeline (scorecard target: 30 migrations). 17 "accelerated" accounts are a subset. | Natalia |
| 26 | 9 Feb | Holistic data fix, not incremental patches | Richard: "If we don't tackle it holistically, all that's going to happen is every week there's a new schema change, a new data fix." Catherine to sense-check complex accounts. | Richard |
| 27 | 12 Feb | Data preserved from "yesterday onwards" | After data loss incident, explicit commitment to CSMs that entered data will persist. No more wipe-and-reload deployments. | Azmain, Ben |
| 28 | 23 Feb | Three programme pillars formalised | (1) Governance of IRP portfolio (CLARA + account planner), (2) Customer intelligence / Sales Recon alignment, (3) Platform enablement. Established at Diya governance session. | Richard, Diya, Natalia, Ben |
| 29 | 23 Feb | 8-week resource plan | Nikhil 50%, Martin (back from holiday), Chris 50%. Priorities: finish CLARA features, address CSM feedback, platform infrastructure. | Richard, Azmain |
| 30 | 26 Feb | User Voice as separate data object, not appended to blockers | Not all User Voice entries are blockers. Azmain proposed a separate object with traceability to blocker-tagged items. | Azmain, Peter Kimes, Stacy |
| 31 | 3 Mar | Nikhil and Chris formally onboarded to CLARA | Nikhil 50% App Factory / 50% CLARA. Chris on bug fixes. Priorities: scorecard tab, migration burndown, Bedrock integration. | Richard, Azmain |
| 32 | 3 Mar | CLARA template/flat-pack approach for cross-OU reuse | Life SLT shown CLARA; template approach proposed so other teams can deploy their own instance rather than sharing one. | Ben, Azmain |
| 33 | 3 Mar | Adoption charter data flow one-directional to start | Bi-directional data flow too complex (customer-annotated Excel with diagrams hard for LLMs to parse). Start with one-directional. | Richard, Azmain |
| 34 | 4 Mar | Two-week release cycle for CLARA | Move from ad-hoc deploys to structured two-week release cycles. | Azmain, Diana |
| 35 | 4 Mar | Azmain reports to Diana | New reporting line. Diana (not Stacy as Natalia originally considered) becomes Azmain's manager. Supportive of Friday development. | Natalia, Diana |
| 36 | 4 Mar | Build in Five demo shifted from March 21 to May | Exceedance event is in May, content due April. Richard: "timelines may not work." Martin to summarise demo approach for Ben. | Richard, Martin |
| 37 | 6 Mar | Gainsight architecture alignment meeting planned | Meeting with Gainsight team (Tina Palumbo, Nadim, Rajesh) scheduled for next Thursday. Catherine offered governance help. Also pushing for Salesforce programmatic access. | Azmain, Catherine |
| 38 | 10 Mar | Idris given dedicated time for AI programme work | Ben Brooks approved. Idris to focus on TSR automation and become the AI champion back to the risk advisory team. | Ben Brooks, Richard |
| 39 | 10 Mar | TSR automation treated as a proper scoped project | Not just a side experiment — Azmain to help define plan and scope. Team to support. | Richard, Azmain, Idris |
| 40 | 10 Mar | Navigator MCP server integration is Build in Five's top priority | Must be plugged into Martin's dashboard builder before exceedance to complete the live demo loop. | Richard, Martin |
| 41 | 10 Mar | Build in Five stakeholder cascade defined | Sequence: MCP integration → tech consulting team → demo team (Bibo/Gibson) → sales (Flemington) → exceedance content factory | Richard, Azmain |
| 42 | 9 Mar | Date input min set to 2022 across all CLARA date fields | Someone entered a 1999 date breaking the migration burndown chart. Ben Brooks asked for limits. Max also defined explicitly. | Azmain, Chris |
| 43 | 9 Mar | Users should use calendar picker for dates, not type manually | Prevents format and range issues. Free-form typing allowed but edge cases handled via user feedback. | Azmain |
| 44 | 9 Mar | Dan Flemington's app to be deployed to App Factory | Rather than running locally, Dan's sales tool will be hosted on the shared AWS infrastructure with user access controls. | Richard |
| 45 | 11 Mar | App Factory core pivoting to MCP server architecture | BenVH: rather than a UI platform, App Factory becomes a middleware MCP server that any app can consume. This eliminates need for a standalone UI and makes the platform more portable and composable. | BenVH |
| 46 | 11 Mar | Nikhil UI work put on back burner — MCP server is the priority | BenVH: the MCP server makes Nikhil standalone UI unnecessary. MCP server approach also satisfies Asia-Pac teams who want speed. | BenVH |
| 47 | 11 Mar | Nikhil to be redirected away from App Factory to Salesforce integration or AIG | Richard and BenVH agreed Nikhil should be moved to a different project entirely. Persistent boundary violations and credit-taking are unsustainable. | Richard, BenVH |
| 48 | 11 Mar | Build in Five: Nikhil and Martin workstreams merged under single plan | Richard briefed team that BenVH wants to fold Nikhil work into Martin. Azmain to create combined project plan including Elliot profiling agent. | Richard, Azmain |
| 49 | 11 Mar | Salesforce integration one-way only (read from Salesforce, no write back) | Azmain: pushing data back is a huge can of worms given unknown SF data structure. Catherine agreed. Focus on pulling cases and case feed. | Richard, Catherine, Azmain |
| 50 | 11 Mar | Salesforce key data objects: Cases and Case Feed only (phase 1) | Success criteria and accounts not needed from Salesforce — those go to Gainsight. Four consumers: Bernard (sentiment), Courtney (HD), Kevin (tickets), CLARA (blockers). | Richard, Catherine |
| 51 | 11 Mar | Juliet to get own AWS infrastructure for confidential data | Juliet has commission targets — too sensitive for shared hosting. Richard and BenVH to provide walkthrough next week. | Richard, Juliet |
| 52 | 11 Mar | All reusable processes must go into App Factory MCP server | If a process could be used by more than one app, it belongs in App Factory — not in the individual app. Increases cross-app and cross-OU reusability. | BenVH |
| 53 | 11 Mar | SharePoint knowledge cataloguing as next major data initiative | Profile 10 years of consulting documents via PowerShell scripts, tag with Purview/MDM, build vector database with MCP server on top for RAG queries. Slidey would pull real consulting IP. | Richard |
| 54 | 11 Mar | Wednesday meeting next week to publicly launch App Factory | Richard wants Ben Brooks to present the MCP server to senior stakeholders. Timing deliberate — ISLTR in London. | Richard |
| 55 | 11 Mar | Inter-app communication (CLARA → Slidey) prioritised | Azmain identified the use case: build an MD file in CLARA, send via App Factory to Slidey for PowerPoint generation. BenVH asked Azmain to write it up. | Azmain, BenVH |
| 56 | 11 Mar | Cross-OU showcase meeting scheduled for Wednesday next week | Insurance, banking (Idrees), asset management (Amanda), and potentially ISLTR. Agenda: CS AI initiatives, retention dashboard, ROB AI, App Factory. | Richard, Idrees |
| 57 | 12 Mar | Gainsight-Clara integration starts with POC, charter-first approach | Ben Brooks insisted on formal charter before any development. Team strategy: demanding business requirements that slow integration without refusing. | Ben Brooks, Azmain |
| 58 | 12 Mar | Clara remains the UI and reporting layer; Gainsight used as data store; App Factory handles integration | Team consensus: even if Gainsight is source of truth for CSM data, Clara stays as the cross-functional UI | Ben Brooks, BenVH, Azmain, Richard |
| 59 | 12 Mar | Fortnightly CLARA release cycle with Tuesday governance review | Natalia Plant established structured cadence: Tuesday review to prioritise, release every other Friday. No more ad-hoc builds. | Natalia Plant |
| 60 | 12 Mar | Skip next CLARA release; next release 27 March | Current pipeline stable enough; no urgent changes needed before grads arrive | Azmain, Natalia Plant |
| 61 | 12 Mar | Ben Brooks restricted to sandbox for CLARA changes | Can build and break in sandbox freely; must not push to user-facing production outside release cycle | Natalia Plant, Azmain |
| 62 | 12 Mar | Analytics tab removed from management dashboard | Confusing for Diya if she clicks around; only scorecard and overview tabs remain | Azmain, Stacy |
| 63 | 12 Mar | Management dashboard moved higher in sidebar navigation | Make it easier for senior leadership to find; done before Monday ISLT | Azmain, Natalia Plant |
| 64 | 12 Mar | Use case completion check: software status must be in production first | Blocking check, not automation — forces CSMs to manually update software status before closing use case | Azmain, Catherine, Natalia Plant |
| 65 | 12 Mar | Two grads joining April 7 for CLARA maintenance (London + New York) | 100% utilisation on CLARA. Interviews underway. Enables maintenance mode transition. | Azmain |
| 66 | 12 Mar | Weekly 1-hour 1-1 established between Azmain and Diana | Regular debrief cadence to stay aligned on programme, politics, Friday development | Azmain, Diana |
| 67 | 12 Mar | Catherine situation to be raised with Natalia Orzechowska and Diya separately | Diana to discuss with Natalia; Richard to raise with Diya in London. Tactical approach: define AI enablement as separate from digital enablement. | Diana, Richard, Azmain |
| 68 | 12 Mar | App Factory MCP server using AWS Bedrock AI agents for orchestration | BenVH pivoting from custom LLM orchestration to leveraging Bedrock agents for faster iteration | BenVH |
