# Stakeholder Map

Last updated: 2026-03-10 (all transcripts through 10 March processed)

## Tier 1 — Decision Makers & Sponsors

### Diya Sawhny — Executive Sponsor
- **Engagement level:** Low → Medium (engaged properly by late Feb after governance session)
- **Communication style:** Impatient with detail. Scrolls phone during long explanations. Wants elevator pitches, not walkthroughs. (Richard explained this to Azmain in detail on 20 Jan.)
- **Week 3 signal (22 Jan):** Invited to priority-setting call but did not join — said she was slammed and it was her only calendar break. Wants outcome-based milestones with timelines, and "continuation, not reset."
- **Key moment:** 23 Feb governance session — first substantive engagement. Appeared receptive.
- **What she cares about:** Insurance scorecard, Andy Frappe's visibility requirements, efficiency metrics/KPIs
- **Risk:** If she disengages, programme loses executive air cover. Week 3 confirms she is hard to reach — the team is working around her, not with her.
- **Approach:** "Should feel like continuation, not reset." Keep updates tight.

### Andy Frappe — President, Moody's Analytics
- **Engagement level:** Newly engaged (saw CLARA demo 20 Feb, Ben demoing again 23 Feb)
- **What he cares about:** Centralised migration reporting (saw banking's Power BI dashboard, wants equivalent)
- **Risk:** Highest-stakes audience. One misinterpreted data point could damage programme credibility.
- **Open question:** What was his reaction to the demo?

### Ben Brooks — De Facto Product Owner
- **Engagement level:** Maximum. Built the original app over Christmas 2025.
- **Style:** Pushes hard for speed. "Just do it, press the button." Runs 5am training sessions. Races HighRox.
- **Key tension:** Disagrees with Josh on release timing — wants to move faster than stakeholders are comfortable with.
- **Strategy:** "Kill CSMs with kindness." Shopping CLARA around internally (e.g., Life MD) to create independent demand.
- **Week 3 signals:** Built local Portfolio Review prototype overnight in Cursor (21 Jan). First hands-on UX review of dashboard (23 Jan) — identified colour/RAG confusion. Accepted Natalia's pushback on separate Portfolio Review tab gracefully. Framing CSM instruction collaboratively: "Set up a meeting with your account team, fill out the data together." Also blocked on Cursor tokens by 23 Jan.
- **Concern:** Becoming emotionally invested in adoption — may push past stakeholder readiness.

### Natalia (Plant) — CS Lead / Azmain's Manager
- **Engagement level:** High. Runs weekly Portfolio Reviews using CLARA.
- **Style:** Practical, process-focused. Pushes back on unnecessary features.
- **Key contributions:** Reframed "priority" from arbitrary to scorecard-aligned 31 accounts. Insisted on using dashboard filters in meetings rather than building separate tabs.
- **Week 3 signals:** Heavily engaged in Portfolio Review design (21 Jan) and Monday demo prep (23 Jan). Set key process rules: no editing during meetings, no formal RACI in first meeting deck (too heavy). Reviewing every slide and every UI element for the Monday demo. Highly detail-oriented. First genuine endorsement of the data input hub: "This looks really, really good."
- **Concern:** CSM workload perception. Doesn't want CLARA to feel like more work.
- **Important context:** Owns Gainsight relationship. Sees CLARA as potentially reusable beyond IRP.

## Tier 2 — Influential Gatekeepers

### Josh Ellingson — CSM Leadership
- **Engagement level:** Cautious but increasing
- **Key concern:** Data interpretation accuracy — "I don't want Andy Frappe seeing one piece of data that's interpreted incorrectly and we can't get them off of it."
- **Tension with Ben:** "Slight disagreements" on release timing. Josh wants more control before CSMs get access.
- **Trajectory:** Getting more engaged over time. Providing substantive feedback. Coming around.

### George Dyke — CSM Leadership (different team)
- **Engagement level:** High and proactive
- **Style:** Comfortable with ambiguity, pragmatic
- **Key contributions:** Organised two-day CSM workshop. Building separate account planner app in Cursor. Distinguishes CLARA scope (IRP migration) from Gainsight scope (overall health).
- **Week 3 signals:** Onboarded to Cursor by Richard in a multi-hour hands-on session (19 Jan). Building account planner app independently. Discovered overlap with Sales Recon's account planning features (22 Jan) but sees distinction: his work = writing the plan, Sales Recon = informing the plan. Pragmatic about Sales Recon dependency: values flexibility of owning their own tool. Flags that CSMs need account plans for non-IRP customers too. Confirmed IRP migrations are on the MA scorecard (three-quarters of business unit revenue related to IRP).
- **Asset:** Good at bridging management and practitioner perspectives.

### Stacy (Dixtra) — Data & Reporting
- **Engagement level:** Steady
- **Style:** Cautious, thorough. Manages 300-slide reporting decks. Warns about "running fast and stepping back."
- **Key role:** Defines reporting requirements. Writing insurance migration requirements into banking BRD template for Power BI.
- **Concern:** Prefers Excel exports over APIs because "too much is changing."

### Richard Dosoo — Programme / Operational Owner
- **Engagement level:** Maximum — but showing signs of exhaustion/disengagement by March.
- **Role:** Technical bridge between Ben's vision and Azmain's execution. Manages up to Diya, across to Sales Recon, down to dev team.
- **Style:** Strategic framing. Repackages messages for different audiences (note: tells Diya a different origin story than the actual one — confirmed 20 Jan).
- **Week 3 signals:** Patient and instructive with Azmain during debugging (19 Jan). Personally paid for Azmain's Claude Code Max subscription (23 Jan). Shifted from "move fast" to "don't break things."
- **March signals (CRITICAL):** Interviewing for jobs in New York. Partly motivated by disliking working with Rhett. Described as exhausted on 5 Mar standup. Wasted a day integrating Rhett's uncoordinated adoption charter work.
- **Risk:** FLIGHT RISK. Carries irreplaceable institutional knowledge — programme strategy, stakeholder relationships, Diya management. His departure would be the single biggest threat to the programme.

## Tier 3 — Technical & Delivery

### Azmain — Programme Manager & CLARA Developer
- **Engagement level:** 100% consumed by CLARA + now building Friday on the side
- **Key tension:** Formally raised with Natalia (20 Feb) that the other five workstreams have had zero progress. Recognised this as early as 21 Jan.
- **Growth arc:** Learning Git, CI/CD, AWS in real-time on the job. Richard positioning this as a career growth vehicle.
- **March signals:** Now reports to Diana (not Stacy). Building Friday PM app as side project — burned $500 Cursor in one day on it. Using Claude Code in cloud environment. Aware of Richard's departure plans and BenVH's Nikhil frustrations (he's the one who revealed both).
- **Risk:** Single point of failure for CLARA features. Bandwidth now split across CLARA + Friday + programme management. If Richard leaves, Azmain loses his primary mentor and strategic guide.

### BenVH (Van Houten) — Infrastructure
- **Role:** AWS deployment, CI/CD, security. The only person who can deploy.
- **Risk:** Single point of failure for infrastructure. If he's unavailable, nothing deploys.
- **Asset:** Has a personal patented CICD orchestration project (Phantom Agent). Thinking about how to make deployment "idiot proof."
- **March signals (CONCERNING):** Admitted his recent absence was not illness but being worn down by Nikhil taking credit for his App Factory work, renaming it, and presenting his architecture as his own. Morale/retention risk. Also flagged on 3 Mar that four other apps are in the App Factory pipeline — he's under-resourced.

### Martin Davies — Developer (12-week assignment)
- **Focus:** Build in Five workstream
- **Status:** Back from holiday late Feb. Demo target: March 21.

## Tier 4 — Adjacent / Emerging

| Person | Domain | Status |
|--------|--------|--------|
| Kevin Pern | CS Agent (Copilot Studio) | Working alone, no programme oversight |
| Cihan / Lonny | MCP server (Product) | Early-stage collaboration |
| Nikhil | Tech consulting lead (new) | 50% App Factory / 50% CLARA. BenVH alleges he is taking credit for App Factory work. Territorial. |
| Bala | Banking/edfx (new) | Just joined |
| Rhett | Consulting/tech | Learning to push code |
| Courtney | HD model analysis | Rich data on adoption barriers, exploring integration |
| Peter Kimes | User Voice integration | Detailed requirements captured 26 Feb |
| Jamie | Sales Recon | Supportive but constrained. Week 3: set clear boundaries ("Sales Recon cannot solve every problem"), transparent about costs (~$3/analysis), proposed Feb pilot |
| Divya | AI governance | Wants efficiency KPIs and philosophical discussion |
| Ari Lahavi | Head of Applied AI | Met at Jan 26 executive session |
| Idris | Banking CS → Now AI programme member | Formally onboarded 10 Mar with Ben's approval for dedicated time. Working on TSR automation for cat bonds. First expansion beyond core insurance CS team. Strong ally. |
| Conrad | Banking CS | Week 3: Present at Sales Recon prep (19 Jan). Less vocal than Idris. |
| Bernard | Life team | Week 3: Built Copilot health dashboard (Salesforce extracts + NPS + Mixpanel). Confident in demo. Acknowledges hallucination risk but says manageable with focused prompts. Sceptical about Q1 timelines. |
| Alexandra | Life team | Week 3: Wants broader framing ("successful cloud migration" not just IRP). Raised valid hallucination concern for Monday presentation. Working on partner tracking. |
| Steve Gentilli | Adoption charter (WS4) | Week 3: Enthusiastic about folding Excel tracker into CLARA. Has database/systems experience, wants to help with data modelling. Strong ally for WS4. |
| Vlad | PM | Week 3: Practical, willing to help populate data in CLARA. Has 3 accounts ready as quick wins. Wants clear scope and timelines. |
| Diana | PM → Azmain's new manager (4 Mar) | Now Azmain's reporting line. Supportive of Friday development. Planning to present Friday vision to Ben/Charlotte. |
| Martin Davies | Build in Five (WS6) | Exceptional output. Dashboard builder dramatically exceeded expectations (10 Mar). Richard compared to Databricks Genie. Live RM API integration working. Demo shifted to May. 12-week clock ticking but output justifies investment. |
| Catherine | Data alignment + Gainsight governance | March: Offered to help with governance and App Factory decision tree. Key new ally. |
| Dan Flemington | Sales | March: New stakeholder with existing tools. Julia Valencia identified for Salesforce access. |
| Gina Greer | Banking customer engagement (central) | New 10 Mar. Mapping banking AI initiatives. Same stage as insurance Nov 2025. Potential cross-OU ally. |
| Olivier | Banking AI enablement lead | New 10 Mar. Thoughtful about tool selection. Working with Nick Louder/Kentucky teams. Deployment gap concern. |
| Jack Cheyne | Life insurance | New 10 Mar. Technically curious about NME. Aware of CAP from banking. Potential cross-OU expansion. |
| Christian Curran | Life insurance | New 10 Mar. Focused on SSO, security, RBAC practicalities. |
| Mike Bibo | Risk Modeller demo team lead | Identified 10 Mar as critical for Build in Five. Demos RM to customers. |
| Sam Gibson | Risk Modeller demo team (UK) | Identified 10 Mar. Under Bibo. |
| Prashant | Developer (planned) | To be allocated to help Azmain with Friday development. |

## Dynamics to Watch

1. **Ben vs Josh** — Speed vs caution on CSM release. Ben pushing, Josh gating.
2. **Azmain's bandwidth** — Formally flagged. If not resolved, other workstreams stay stalled. Week 3 confirms: all five non-CLARA workstreams have had zero progress.
3. **Diya's attention** — Hard to get, easy to lose. Must be fed carefully. Week 3: did not join the one call designed for her input.
4. **CLARA vs Sales Recon** — Standalone now, but when does convergence happen? Jamie's team is tiny. Week 3: George discovered his account planner overlaps with Sales Recon. Critical fork identified: if Jamie says no to migration, Ben needs a permanent maintenance team.
5. **BenVH as bottleneck** — Only deployer. Infrastructure decisions (CDK vs CloudFormation) affect who else can deploy. Week 3: absent for HighRox race, causing real delays. His Alembic migration broke use case creation by 23 Jan.
6. **Deployment fragility** — Week 3 theme. Richard and Azmain shifted from "move fast" to "don't break things." No tested rollback procedure. Schema changes now require BenVH approval before execution.
7. **Corporate tooling crisis** — Cursor tokens exhausted for both Azmain and Ben by 23 Jan. Richard personally paying for Claude Code as workaround. Developer laptops only just approved.
8. **Richard flight risk (NEW - March)** — Interviewing in New York. If he leaves, the programme loses its strategic leader. Nobody else manages Diya or bridges the technical and business sides.
9. **BenVH/Nikhil conflict (NEW - March)** — BenVH worn down by Nikhil taking credit for his work. Morale risk for the only person who can deploy.
10. **Friday as scope creep risk (NEW - March)** — Azmain building a PM app on the side while already stretched thin on CLARA and five other workstreams.
11. **Security/compliance exposure (NEW - March)** — Personal Claude accounts used for Moody's work. Audit found it. Team spending personal money on tooling.
12. **Cross-OU expansion pressure (NEW - 10 March)** — Banking (Gina/Olivier) and Life (Jack/Christian) both want collaboration. Validates approach but risks further stretching an overloaded team.
13. **Bedrock cost trajectory (NEW - 10 March)** — $1,163 in two weeks, on pace for $10K/month. No cost attribution. Tags broken. New frontier of the same budget problem.
