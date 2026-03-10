# Decision Log

Last updated: 2026-03-09 (all transcripts through 6 March processed)

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
