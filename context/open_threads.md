# Open Threads & Unresolved Questions

Last updated: 2026-03-12 (all transcripts through 12 March processed)

Each thread has a status: **OPEN** (unresolved), **WATCHING** (partially addressed, needs follow-up), or **CLOSED** (resolved — move to bottom with resolution date).

---

## OPEN

### 1. Gainsight Integration Timeline — MEETING HELD, CHARTER PHASE
- **First raised:** 12 Jan
- **Updated:** 12 Mar — Meeting held between Clara team and Gainsight Business Systems team (Tina Palumbo, Rajesh, Nadeem). Bi-directional integration proposed by Gainsight team. Ben Brooks demanded formal charter before any development. Team privately agreed strategy: demanding requirements to slow integration. Natalia Orzechowska confirmed no POC before end of March; earliest May. Gainsight team focused on March 30 onboarding deadline for RMS/Cape/Predicate.
- **Context:** Catherine organised the meeting without consulting Clara team — described as a "blindside" by the entire team. Prep materials sent to Catherine were not shared.
- **Question:** Will the charter approach successfully control integration pace? Will Catherine's gatekeeping role persist or be addressed?
- **Why it matters:** Gainsight integration is outside the 12-week Diya plan but the expectation is now set. Scope creep risk if not managed.

### 2. Sales Recon Pilot Results
- **First raised:** 11 Feb
- **Context:** Two-week pilot (11-24 Feb) with 8 CSMs evaluating account intelligence, meeting prep agent, and share knowledge agent.
- **Question:** What did CSMs think? Does it change the CLARA roadmap or the Sales Recon convergence timeline?
- **Why it matters:** Determines whether Sales Recon is a viable end-state platform for CS, or if CLARA needs longer-term investment.

### 3. AWS Bedrock / Claude Code Rollout
- **First raised:** 9 Jan (licences), secured in principle 9 Feb
- **Updated:** 3 Mar — Bedrock API key now working. Security audit caught personal Claude account usage for Moody's work; Ben Brooks providing cover. Azmain admitted "no proprietary information" defence is "wildly a lie."
- **Context:** Access approved via AWS. Bedrock API key functional as of March.
- **Question:** Is all development now on Bedrock/corporate accounts? Has the personal account usage been resolved?
- **Why it matters:** Personal account usage is a compliance risk. Bedrock integration should resolve this but transition needs confirming.

### 4. Andy Frappe Follow-up
- **First raised:** 20 Feb (demo)
- **Context:** Ben demoed CLARA to Andy Frappe, President of Moody's Analytics.
- **Question:** What was the reaction? Any new asks, escalations, or mandates?
- **Why it matters:** Highest-visibility moment for the programme. Reaction shapes resourcing and priority.

### 5. Kevin Pern's CS Agent (WS3)
- **First raised:** 6 Jan
- **Context:** Kevin built a Copilot Studio + Salesforce prototype. Working alone. No programme oversight.
- **Question:** Has anyone formally engaged him? What does the prototype actually do?
- **Why it matters:** This workstream is essentially orphaned. Could be valuable or could be wasted effort.

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
- **Updated:** 6 Mar — **CRITICAL**: Richard is interviewing for jobs in New York (partly because he dislikes working with Rhett). BenVH admitted his recent absence wasn't illness but being worn down by Nikhil taking credit for App Factory work. Both key people showing signs of disengagement/departure.
- **Context:** BenVH is the only person who can deploy. Azmain is the only person building CLARA features. Richard carries irreplaceable institutional knowledge.
- **Question:** What's the retention/mitigation plan? Is anyone documenting Richard's knowledge? Can BenVH/Nikhil conflict be resolved?
- **Why it matters:** If Richard leaves, the programme loses its strategic brain. If BenVH leaves, nothing deploys. Both are now flight risks.

### 10. Build in Five Scope — MAJOR PROGRESS
- **First raised:** 5 Feb (Martin and Azmain both unclear), demo target shifted
- **Updated:** 10 Mar — Martin's dashboard builder dramatically exceeded expectations. Full drag-drop UI, white-labelling, live Risk Modeller API connection, AI assistant mode, theming/dark mode. Richard compared it to Databricks Genie. Ben Brooks saw it and was positive. Critical next step: wire up Navigator MCP server for live API definitions. Stakeholder cascade defined. Exceedance panel format being planned.
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

### 16. Richard Departure Risk
- **First raised:** 6 Mar (Azmain revealed to BenVH)
- **Context:** Richard is interviewing for positions in New York. Partly motivated by disliking working with Rhett. Richard carries irreplaceable institutional knowledge — programme strategy, stakeholder relationships, Diya management approach.
- **Question:** Does anyone else know? Is there a knowledge transfer plan? Can the underlying issues (Rhett) be addressed?
- **Why it matters:** Richard is the programme's strategic brain. His departure would leave a leadership vacuum at the worst possible time (Gainsight integration, Diya engagement, cross-OU expansion all in flight).

### 17. BenVH / Nikhil Conflict — CRISIS LEVEL
- **First raised:** 6 Mar
- **Updated:** 12 Mar — BenVH still stopped responding to Nikhil. Making progress on MCP server using Bedrock AI agents. Channelling anger productively. Richard planning confrontation and Ben Brooks escalation this week.
- **Context:** BenVH feels Nikhil is taking credit for his App Factory work, renaming it, and presenting his architecture as his own. BenVH's recent absence was not illness but being worn down. This is a serious morale/retention risk.
- **Question:** Has Richard confronted Nikhil yet? Has Ben Brooks been briefed?
- **Why it matters:** BenVH is the only person who can deploy. Losing him would be catastrophic for infrastructure.

### 18. Security Audit / Personal Claude Usage
- **First raised:** 6 Mar
- **Context:** Security audit caught personal Claude account usage for Moody's work. Ben Brooks providing cover. Azmain admitted the "no proprietary information" defence is false. Team spending 200 GBP/month personal money for Claude that they cannot expense.
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

### 24. Catherine COE Political Threat to AI Programme
- **First raised:** 12 Mar (Diana 1-1 and Post Gainsight debrief)
- **Context:** Catherine's Centre of Excellence mandate (digital engagement, enablement, Gainsight/SFDC retirement) overlaps directly with the AI programme. She organised the Gainsight integration meeting without consulting the Clara team. Ben Brooks, Richard, Azmain, and BenVH unanimously view her as a threat. Diana revealed Catherine's objectives were approved by Natalia Orzechowska and signed off by Diya. Diana suspects Josh Ellingson may be Catherine's senior backer.
- **Question:** Can the "AI enablement ≠ digital enablement" framing hold politically? Will Natalia Orzechowska adjust Catherine's scope? Will Richard's direct approach with Diya work?
- **Why it matters:** If Catherine's COE absorbs the AI programme, Azmain stated he will leave. The entire programme's delivery capability depends on keeping the current team intact and autonomous.

### 25. CLARA Governance and Release Cadence
- **First raised:** 12 Mar (Clara feedback cadence meeting)
- **Context:** Natalia Plant established fortnightly release cycle with Tuesday governance reviews. Chris handling feedback systematically. Two grads arriving April 7 for dedicated maintenance. Ben Brooks restricted to sandbox.
- **Question:** Will Ben Brooks respect the sandbox restriction? Can governance hold when ISLT is using Clara live from Monday?
- **Why it matters:** CLARA's transition from build mode to maintenance mode is critical for programme credibility. Uncontrolled changes risk data corruption ahead of senior leadership usage.

### 26. Adoption Runbook Collaboration (Rhett + PMs)
- **First raised:** 12 Mar (Diana 1-1)
- **Context:** Rhett built a digital adoption runbook (Cursor prototype). Diana's PM team (Vlad, Christian, Prashant) built an Excel-based PM task list. They agreed to collaborate. Rhett uncertain about long-term maintenance. Over 50% of adoption governance owners already use Clara.
- **Question:** Will the runbook be absorbed into Clara or stay standalone? Does it overlap with George's account planning work?
- **Why it matters:** Risk of fragmented tools if not consolidated. But also evidence of organic adoption of structured approaches across the programme.

---

## WATCHING

### Parent/Subsidiary Account Rollup
- **First raised:** 12 Feb (CSM workshop)
- **Context:** Updates to subsidiary accounts don't roll up to parent, making it look like CSMs haven't updated.
- **Status:** Issue identified and acknowledged. Unknown if fix is in progress.

### Scorecard Data Accuracy
- **First raised:** 5 Feb
- **Context:** The 30-31 migration target for 2026. Are switch-off dates populated? Is the data good enough to track against the scorecard?
- **Status:** Catherine doing sense-check on complex accounts. Unclear if complete.

---

## CLOSED

(None yet — this log starts from the debrief baseline)
