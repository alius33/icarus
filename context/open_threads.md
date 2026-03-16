# Open Threads & Unresolved Questions

Last updated: 2026-03-16 (transcripts through 16 March processed)

Each thread has a status: **OPEN** (unresolved), **WATCHING** (partially addressed, needs follow-up), or **CLOSED** (resolved — move to bottom with resolution date).

---

## OPEN

### 1. Gainsight Integration Timeline — CHARTER V1 CREATED, UNDER REVIEW
- **First raised:** 12 Jan
- **Updated:** 16 Mar (from project update) — Azmain created CLARA-Gainsight Integration Charter V1 and shared with the team (14 Mar). Ben Brookes added business SLAs: cannot slow migration, cannot split CSMs between two systems, cannot block adoption squads. Natalia Orzechowska asked about consulting CSMs on business requirements. Idrees Deen offered cross-OU help. Richard demanded Phase 0 structured review of CLARA features with Gainsight team present, plus immediate RACI. Kathryn Palkovics (Catherine) asserted COE authority — asked to be added to project team, offered Gainsight demo.
- **Previous:** 12 Mar — Meeting held with Gainsight Business Systems team (Tina Palumbo, Rajesh, Nadeem). Bi-directional integration proposed. Natalia Orzechowska confirmed no POC before end of March; earliest May.
- **Context:** Kathryn organised the original meeting without consulting Clara team — described as a "blindside." Now asserting COE authority on the charter itself.
- **Question:** Will the charter process give the team enough control? Will Kathryn's COE role be contained or will she end up owning the integration?
- **Why it matters:** Gainsight integration is outside the 12-week Diya plan. The charter is now the battleground for who controls the process.

### 2. Sales Recon Pilot Results
- **First raised:** 11 Feb
- **Context:** Two-week pilot (11-24 Feb) with 8 CSMs evaluating account intelligence, meeting prep agent, and share knowledge agent.
- **Question:** What did CSMs think? Does it change the CLARA roadmap or the Sales Recon convergence timeline?
- **Why it matters:** Determines whether Sales Recon is a viable end-state platform for CS, or if CLARA needs longer-term investment.

### 3. AWS Bedrock / Claude Code Rollout
- **First raised:** 9 Jan (licences), secured in principle 9 Feb
- **Updated:** 3 Mar — Bedrock API key now working. Security audit caught personal Claude account usage for Moody's work; Ben Brookes providing cover. Azmain admitted "no proprietary information" defence is "wildly a lie."
- **Context:** Access approved via AWS. Bedrock API key functional as of March.
- **Question:** Is all development now on Bedrock/corporate accounts? Has the personal account usage been resolved?
- **Why it matters:** Personal account usage is a compliance risk. Bedrock integration should resolve this but transition needs confirming.

### 4. Andy Frappe Follow-up
- **First raised:** 20 Feb (demo)
- **Context:** Ben demoed CLARA to Andy Frappe, President of Moody's Analytics.
- **Question:** What was the reaction? Any new asks, escalations, or mandates?
- **Why it matters:** Highest-visibility moment for the programme. Reaction shapes resourcing and priority.

### 5. Customer Success Agent — BLOCKED ON SALESFORCE API ACCESS
- **First raised:** 6 Jan
- **Updated:** 16 Mar — Genuinely blocked. Needs Salesforce API access to pull customer data. Gainsight team getting Salesforce access — Richard hoping to piggyback on their access pattern. Christopher and Nick were supposed to continue work this week but got derailed by the Gainsight meeting. Richard needs to follow up with Bernard tomorrow (17 Mar) about the API key. Wednesday CLARA POC scope call (Azmain, Ben, BenVH) is the next milestone.
- **Previous:** Kevin built a Copilot Studio + Salesforce prototype. Working alone. No programme oversight.
- **Context:** The Salesforce API access dependency is now the concrete blocker, not just programme neglect.
- **Question:** Will the Wednesday call unblock Salesforce access? Can Richard get the API key from Bernard this week?
- **Why it matters:** CS Agent was front and centre in the Diya presentation but has made zero progress. The Salesforce dependency connects to the broader Gainsight integration pipeline.

### 6. User Voice Integration Design
- **First raised:** 26 Feb
- **Context:** Peter Kimes gave detailed requirements. Azmain proposed separate data object. API integration preferred over Excel dumps.
- **Question:** Has the data model been designed? Is User Voice API access available?
- **Why it matters:** Another integration requirement landing on CLARA's growing backlog.

### 7. Budget / Token Management & Developer Tooling Access — ESCALATING
- **First raised:** 9 Jan (licences), acute by 23 Jan, still acute 23 Feb
- **Updated:** 10 Mar — AWS Bedrock costs hit $1,163 in the first two weeks of March — on pace for $10K by month end. Cost tags not set correctly, making per-project/per-user attribution impossible. Richard exploring Max subscriptions ($200/user) as more cost-efficient alternative. Multiple users on a single shared Bedrock key with zero tracking.
- **Context:** Azmain burned $750 in Cursor tokens in 3 days. Corporate budget went from $10K to $20K. Opus 4.6 is 3x more expensive. Now Bedrock costs are the new frontier of the same problem.
- **Question:** Can AWS tags be fixed urgently? Is Max subscription viable for corporate use without creating the same personal-account compliance issue? Who is accountable for the $10K trajectory?
- **Why it matters:** Budget visibility is now worse than before Bedrock — at least personal accounts had per-user limits. The shared key model means costs scale without anyone knowing who is spending what.

### 8. Infrastructure: CDK vs CloudFormation
- **First raised:** 26 Feb
- **Context:** Cat Accelerate has tech debt — manual Step Function deployment, no backup, no traceability. Debate on whether to stay with CDK or move to simpler CloudFormation.
- **Question:** Has a decision been made?
- **Why it matters:** Affects who can deploy and how reliable deployments are.

### 9. Single Points of Failure Mitigation — ESCALATED
- **First raised:** Implicit throughout, explicit by late Feb
- **Updated:** 6 Mar — **CRITICAL**: Richard flight risk resolved (committed to programme). BenVH admitted his recent absence wasn't illness but being worn down by Nikhil taking credit for App Factory work. BenVH Nikhil conflict being actively addressed.
- **Context:** BenVH is the only person who can deploy. Azmain is the only person building CLARA features. Richard carries irreplaceable institutional knowledge.
- **Question:** Can BenVH/Nikhil conflict be resolved? Is knowledge documentation progressing?
- **Why it matters:** If BenVH leaves, nothing deploys. Knowledge concentration remains a structural risk even with Richard stable.

### 10. Build in Five Scope — MAJOR PROGRESS
- **First raised:** 5 Feb (Martin and Azmain both unclear), demo target shifted
- **Updated:** 10 Mar — Martin's dashboard builder dramatically exceeded expectations. Full drag-drop UI, white-labelling, live Risk Modeller API connection, AI assistant mode, theming/dark mode. Richard compared it to Databricks Genie. Ben Brookes saw it and was positive. Critical next step: wire up Navigator MCP server for live API definitions. Stakeholder cascade defined. Exceedance panel format being planned.
- **Context:** The "cheating" approach (reverse-engineering Apollo) worked brilliantly. Martin has built something that could be a product feature, not just a demo.
- **Question:** Can MCP server integration happen in the next two weeks? Will product team want to absorb this? How does Ben frame this at exceedance — product capability or customer self-service?
- **Why it matters:** Build in Five has gone from "unclear scope" to "potentially the programme's most impactful deliverable for adoption blockers." The product positioning question (Moody's experience vs customer self-service) is strategically important.

### 11. Alembic Migration / Deployment Sync
- **First raised:** 19 Jan
- **Context:** CLARA's deployed version broke because Alembic migrations did not propagate schema changes to production RDS. "Multiple migration heads" error encountered. BenVH was building an automated deployment script but it was not complete. By 23 Jan, BenVH's Alembic migration for portfolio review broke use case creation (500 error, duplicate key violation).
- **Question:** Is the deployment pipeline reliable? Can anyone other than BenVH fix migration issues?
- **Why it matters:** Every schema change risks breaking production. No tested rollback procedure exists. The team admitted they have never tested a rollback and attempting one could leave the system completely unusable.

### 12. Dev/Test/Prod Environment Split
- **First raised:** 19 Jan (implicit), 20 Jan (explicit)
- **Context:** Richard proposes dev environment for frequent deploys, prod deploys only once a week. BenVH to set up when he returns. As of 23 Jan, still everything deploys to one environment.
- **Question:** Has BenVH set up the environment split?
- **Why it matters:** Without separation, every deployment risks breaking the live system that CSMs are using.

### 13. Diya's Priorities for the Programme
- **First raised:** 22 Jan
- **Context:** Diya was invited to a priority-setting call but did not join (said she was slammed). Richard pre-filled priority slides. Diya told Richard she wants the Monday meeting to be "a continuation, not a reset" and wants outcome-based milestones with timelines.
- **Question:** Has Diya formally endorsed the programme priorities? Does she agree CS workflow migrates to Sales Recon by end of FY26?
- **Why it matters:** Without executive priority endorsement, the programme lacks direction on the critical CLARA-vs-Sales Recon fork.

### 14. George's Account Planner Integration
- **First raised:** 19 Jan (built in Cursor), 22 Jan (overlap with Sales Recon discovered)
- **Context:** George built an account planner in Cursor. Overlap with Sales Recon's account planning features discovered. George distinguishes his work (writing the plan) from Sales Recon (informing the plan). Decision on folding into CLARA vs standalone deferred.
- **Question:** Will this fold into CLARA, remain standalone, or be superseded by Sales Recon?
- **Why it matters:** Multiple tools for overlapping needs creates confusion and maintenance burden. CSMs need account plans for non-IRP customers too, which CLARA does not cover.

### 15. LLM Hallucination Risk in Executive Demos
- **First raised:** 23 Jan
- **Context:** Idris's banking team found that Copilot changes SRB figures when challenged. They hard-coded rules in Copilot Studio to handle dollar amounts. Bernard acknowledges risk but says it is manageable with focused prompts. Alexandra wants to know how to protect against it in the Monday presentation.
- **Question:** What is the mitigation strategy for hallucination in customer-facing or executive-facing demos?
- **Why it matters:** One incorrect figure in front of Andy Frappe or Colin Holmes could damage programme credibility.

### 16. Richard Departure Risk -- RESOLVED
- **First raised:** 6 Mar (Azmain revealed to BenVH)
- **Context:** Was briefly considering other roles in early March. Resolved mid-March -- Richard committed to programme. Carries important institutional knowledge — programme strategy, stakeholder relationships, Diya management approach.
- **Question:** RESOLVED. Knowledge documentation should continue as good practice.
- **Why it matters:** Resolved. Richard committed to programme. Knowledge documentation continues.

### 17. BenVH / Nikhil Conflict — POTENTIALLY RESOLVED
- **First raised:** 6 Mar
- **Updated:** 16 Mar — Richard claims to have sorted it: Nikhil's resources being redirected to AIG. Azmain sceptical it'll stick ("he's gonna ask you for another report mid-month"). Needs confirmation that the redirect is permanent and BenVH is satisfied.
- **Previous:** 12 Mar — BenVH still stopped responding to Nikhil. Making progress on MCP server using Bedrock AI agents. Richard planning confrontation and Ben Brookes escalation.
- **Context:** BenVH felt Nikhil was taking credit for his App Factory work, renaming it, and presenting his architecture as his own. BenVH's recent absence was not illness but being worn down.
- **Question:** Is the AIG redirect permanent? Has BenVH been told? Does BenVH accept this resolution?
- **Why it matters:** BenVH is the only person who can deploy. The redirect is the right move but Nikhil's pattern of boundary-crossing may reassert.

### 18. Security Audit / Personal Claude Usage
- **First raised:** 6 Mar
- **Context:** Security audit caught personal Claude account usage for Moody's work. Ben Brookes providing cover. Azmain admitted the "no proprietary information" defence is false. Team spending 200 GBP/month personal money for Claude that they cannot expense.
- **Question:** Has Bedrock fully replaced personal accounts? Is there ongoing compliance risk?
- **Why it matters:** Data governance violation. If escalated, could damage programme credibility or result in disciplinary action.

### 19. Friday PM App Development
- **First raised:** 4 Mar
- **Context:** Azmain building Friday (internal Monday.com-like PM tool) as a side project using Claude Code. Named after "His Girl Friday." Diana supportive, plans to present to Ben/Charlotte. Azmain burned $500 Cursor in one day building it. Prashant to be allocated to help.
- **Question:** Where does Friday fit in programme priorities? Is it sanctioned or a skunkworks project? Who funds it?
- **Why it matters:** Could be valuable but risks diverting Azmain's already-stretched bandwidth from CLARA and other workstreams.

### 20. Rhett Operating Independently
- **First raised:** 5 Mar
- **Context:** Rhett did adoption charter work (Excel-based) without consulting CSMs, Liz Couchman, or following the agreed Word-to-app approach. Richard wasted a day integrating his work.
- **Question:** Is Rhett being managed? Does he understand the agreed approach?
- **Why it matters:** Uncoordinated work creates rework and frustration. Richard's time is already scarce.

### 21. Cross-OU AI Enablement (Banking & Life)
- **First raised:** 10 Mar
- **Context:** Diya asked insurance team to meet with banking (Gina Greer, Olivier) and Life (Jack Cheyne, Christian Curran) to share the AI enablement approach. Both meetings happened same day. Banking is at the exact same stage insurance was in November 2025 — siloed efforts, no dedicated resources, no deployment solution. Life team shown IRP native modelling engine and App Factory.
- **Question:** Will this produce tangible collaboration or remain a one-off information share? Who coordinates the cross-OU follow-up?
- **Why it matters:** Cross-OU expansion validates the programme's approach but risks further stretching an already overloaded team. If banking wants App Factory support, that's more work for BenVH.

### 22. Idris / TSR Automation Project
- **First raised:** 10 Mar
- **Context:** Idris formally onboarded to the AI programme with Ben's approval for dedicated time. Immediate project: automating Transaction Summary Reports for cat bonds. Azmain to support with project planning. Richard managing the politics with Arno.
- **Question:** How will Arno react? Is 500/month Cursor credits enough? Can the TSR process be meaningfully automated?
- **Why it matters:** First formal expansion of the programme beyond the core insurance CS team. Validates the enablement model. If successful, creates a template for onboarding other teams.

### 23. AWS Bedrock Cost Control
- **First raised:** 10 Mar
- **Context:** $1,163 in first two weeks of March on a single shared Bedrock key. No per-project or per-user cost attribution. Tags not configured. On pace for $10K/month.
- **Question:** Can cost tags be fixed this week? Who approves the Bedrock budget? Is there a per-project allocation model?
- **Why it matters:** The Bedrock migration was supposed to solve the personal-account compliance problem, but it introduced a new problem: invisible cost scaling with zero accountability.

### 24. Kathryn Palkovics (Catherine) COE Political Threat to AI Programme — ESCALATING
- **First raised:** 12 Mar (Diana 1-1 and Post Gainsight debrief)
- **Updated:** 16 Mar (from transcript) — Azmain and Richard strategizing how to frame the issue for Ben Brookes. Richard's approach: tell the story factually — pattern of overreach, misalignment, risk to the Diya-approved programme. Key rhetorical point: when they sat with Diya, Kathryn's name never came up; the stakeholders that matter are Dennis Clement (MD DCR), Keith Berry, Christoph. Richard's honest preference: not involved at all. Azmain: need delineation of responsibilities, can't push her out. Richard to discuss with Ben Brookes in person this week.
- **Previous:** 16 Mar (from project update) — Kathryn asserting COE authority on Gainsight integration charter, requesting to join the project team.
- **Context:** Kathryn's COE mandate (digital engagement, enablement, Gainsight/SFDC retirement) overlaps directly with the AI programme. Diana revealed her objectives were approved by Natalia Orzechowska and signed off by Diya. Diana suspects Josh Ellingson may be Kathryn's senior backer.
- **Question:** Will Ben Brookes take action? Can the team frame this as a programme risk rather than a personal conflict?
- **Why it matters:** If Kathryn's COE absorbs the AI programme, Azmain stated he will leave. The charter process is becoming the mechanism through which this could happen.
- **Note:** "Catherine" in earlier audio transcripts = "Kathryn Palkovics" per Teams chat (confirmed 14 Mar).

### 25. CLARA Governance and Release Cadence
- **First raised:** 12 Mar (Clara feedback cadence meeting)
- **Context:** Natalia Plant established fortnightly release cycle with Tuesday governance reviews. Chris handling feedback systematically. Two grads arriving April 7 for dedicated maintenance. Ben Brookes restricted to sandbox.
- **Question:** Will Ben Brookes respect the sandbox restriction? Can governance hold when ISLT is using Clara live from Monday?
- **Why it matters:** CLARA's transition from build mode to maintenance mode is critical for programme credibility. Uncontrolled changes risk data corruption ahead of senior leadership usage.

### 26. Adoption Runbook Collaboration (Rhett + PMs)
- **First raised:** 12 Mar (Diana 1-1)
- **Context:** Rhett built a digital adoption runbook (Cursor prototype). Diana's PM team (Vlad, Christian, Prashant) built an Excel-based PM task list. They agreed to collaborate. Rhett uncertain about long-term maintenance. Over 50% of adoption governance owners already use Clara.
- **Question:** Will the runbook be absorbed into Clara or stay standalone? Does it overlap with George's account planning work?
- **Why it matters:** Risk of fragmented tools if not consolidated. But also evidence of organic adoption of structured approaches across the programme.

### 27. CLARA Visibility Expansion to Product & Tech Teams
- **First raised:** 13 Mar (CLARA Demo to Product & Tech teams)
- **Context:** Cihan (MD Product & Technology) brought his entire team to see CLARA. Azmain imported ~4,000-5,000 users under Andy Frappe as viewers with SSO. Cihan personally endorses CLARA as a daily tool. Product teams (Ollie, Julie) asked how to contribute. Call chat remains as living feedback channel.
- **Question:** Will product/tech engagement translate into better data quality and cross-functional collaboration? How will the team handle support requests from a much larger user base?
- **Why it matters:** Biggest audience expansion since launch. If product managers start contributing adoption-relevant intel to CLARA, it becomes significantly more valuable. But support burden could overwhelm the small team.

### 28. Customer & Model Success Team Dashboard Needs
- **First raised:** 13 Mar (Review AI Powered Dashboards)
- **Context:** Lucia's team facing wave of dashboard requests. Cape team needs Tableau replacement by September 2026. Team uses R/Streamlit but has no hosting solution. App Factory is the proposed solution. Lucia and Joel offered to test Salesforce integration.
- **Question:** How many dashboards are needed? Can App Factory scale to support another team's apps alongside CLARA?
- **Why it matters:** First concrete external demand for App Factory beyond the core team. If successful, validates the platform model. If delayed, team may build their own solution.

### 29. Cross-OU AI Training Methodology
- **First raised:** 13 Mar (How Credit team in Banking does AI training)
- **Context:** Banking Credit team has a mature agent day framework: 4-tier model, pre-work, transit teachers, individual projects, bi-weekly follow-ups. Insurance team acknowledged their November training was too generic. Richard committed to homework on skills repo and governance before formalising collaboration.
- **Question:** Will the insurance team adopt Banking's agent day model? Who will coordinate the cross-OU skills sharing? Can the quarterly cadence be maintained?
- **Why it matters:** WS1 (Training & Enablement) has been stalled since January. Banking has a proven framework that could be adopted. If skills sharing works cross-OU, it multiplies the value of every agent built.

### 30. Graduate Rotation Resource Conflict (Azmain vs Nikhil)
- **First raised:** 16 Mar (from project updates)
- **Context:** Azmain requested and interviewed 2 graduates (Alvin, London; Sam, New York) specifically for AI/CLARA work. Nikhil Koli separately asked Emma Jaggs (grad manager) for a replacement for Elliot (former team member who joined the AI programme). Emma merged the two requests and told them only 2 grads available. Richard clarified to Emma that the requests are separate: Azmain's 2 for CLARA + Nikhil's 1 Elliot replacement = 3 total needed.
- **Question:** Will Emma actually allocate 3 grads (2 for Azmain + 1 for Nikhil)? Or is budget/availability truly capped at 2? Which project did Elliot join?
- **Why it matters:** If Nikhil takes one of Azmain's grads, CLARA maintenance mode is undermined. This is another front in the Nikhil friction pattern — after credit-taking (BenVH conflict) and boundary violations, now resource encroachment.

### 31. Build in Five Stakeholder Cascade
- **First raised:** 16 Mar (from project update)
- **Context:** Richard wants to organize a Build in Five share-out similar to the App Factory approach. Key stakeholder groups: MPS, Sales, Product. Samuel Gibson added to group chat — keen on MCP server for customer demos, says "Mike B sees the DataLake as the future." Richard asked Azmain to connect Samuel and Mike Bibo with Martin's work and schedule a brief call once Martin is ready.
- **Question:** When is Martin ready for the share-out? How does this relate to the exceedance event demo?
- **Why it matters:** Build in Five is transitioning from internal development to external stakeholder engagement. This is the programme starting to commercialise the work.

### 32. Slidey Data Scoping — Users Can See All Presentations
- **First raised:** 16 Mar (Teams channel)
- **Context:** Auth + logout landed 16 Mar (BenVH). But BenVH immediately noticed he could see all presentations — user-ID is not being taken into account in queries. Richard said he would investigate when he gets back. This is a next-order problem after auth hookup: access scoping / per-user filtering.
- **Question:** When will user-ID filtering be implemented? Is this a query-level fix or does RBAC need deeper wiring?
- **Why it matters:** Blocks wider rollout of Slidey. Without data scoping, every user sees every presentation — a security and UX problem that prevents sharing the tool beyond the core team.

### 33. Slidey Environment Discipline — No Dev/Staging/Prod
- **First raised:** 16 Mar (Teams channel)
- **Context:** Ben Brookes wants to use Slidey on "live stuff" and fix/nudge it simultaneously. Requested dev/staging/prod environments back, asked for a lesson on updating via GitHub without asking for help, and suggested setting up release notes. These signals indicate the product is crossing from lab/demo mode into real-use mode, but engineering hygiene is missing.
- **Question:** Will environments be set up before wider rollout? Who manages the release process? Is this BenVH's responsibility alongside everything else?
- **Why it matters:** Without environment separation, every change risks breaking the live product. This is the same pattern that caused problems with CLARA early on (see thread #12).

### 34. IRP Consulting Project Tracking Gap — NO VISIBILITY
- **First raised:** 16 Mar (Weekly PM forum)
- **Context:** Diana Kazakova-Ivanova identified that IRP implementation and cat accelerate consulting projects have **no forum, no tracking, and no status updates**. Advisory projects (cat bond etc.) have functioning calls, but consulting/implementation work under Rhett and Kate is invisible. Diana pushing to resolve by: (a) resuming Wednesday calls with implementation leads, (b) enabling CLARA's project management section as temporary tracking tool. Wednesday meeting with Rhett and Kate is the next milestone.
- **Question:** Will Rhett and Kate agree to a governance framework? Can CLARA's PM section be made functional quickly enough?
- **Why it matters:** Without visibility, revenue-generating consulting work (e.g., AZSA's $800K budget) silently consumes the same resources needed for IRP adoption. Diana called this "the most important" gap.

### 35. HD Model Data Entry Deadline — 1 April
- **First raised:** 16 Mar (HD Guidance to CSMs)
- **Context:** Only 26 of ~68 clients have HD data in CLARA (migrated from Salesforce). ~35 Americas/brokers clients need data entered by end of March for the April 1 IRP report to leadership. Data needed at use-case-level granularity per HD model. CSMs pushing back on manual entry — want bulk upload capability. Stacy cautious about data quality from bulk uploads. Requirements call with Chernell planned for the bulk update feature.
- **Question:** Can the bulk update feature be built before the deadline? Will CSMs comply with manual entry if not?
- **Why it matters:** First IRP report with HD data goes to leadership April 1. Incomplete data undermines the data-driven narrative Ben Brookes is building.

### 36. Knowledge Graph for IQ — Diya Request
- **First raised:** 16 Mar (Chat with Richard)
- **Context:** Diya personally asked Richard and Ben to look into adding a knowledge graph on top of IQ. Richard worked on it over the weekend. Needs to be added to the 12-week deliverable plan — falls under same pillar.
- **Question:** Where does this fit in the pillar structure? How much effort is involved? Is there a demo target date?
- **Why it matters:** Diya-originated request. Must be tracked and delivered or risk executive disappointment.

---

## WATCHING

### Parent/Subsidiary Account Rollup
- **First raised:** 12 Feb (CSM workshop)
- **Context:** Updates to subsidiary accounts don't roll up to parent, making it look like CSMs haven't updated.
- **Status:** Issue identified and acknowledged. Unknown if fix is in progress.

### Scorecard Data Accuracy
- **First raised:** 5 Feb
- **Context:** The 30-31 migration target for 2026. Are switch-off dates populated? Is the data good enough to track against the scorecard?
- **Status:** Kathryn Palkovics doing sense-check on complex accounts. Unclear if complete.

---

## CLOSED

(None yet — this log starts from the debrief baseline)
