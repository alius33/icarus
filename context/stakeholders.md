# Stakeholder Map

Last updated: 2026-03-16 (project updates through 16 March processed — gainsight integration charter, grad rotation, Build in Five expansion, Sam Gibson onboarding)

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

### Ben Brookes — De Facto Product Owner
- **Engagement level:** Maximum. Built the original app over Christmas 2025.
- **Style:** Pushes hard for speed. "Just do it, press the button." Runs 5am training sessions. Races HighRox.
- **Key tension:** Disagrees with Josh on release timing — wants to move faster than stakeholders are comfortable with.
- **Strategy:** "Kill CSMs with kindness." Shopping CLARA around internally (e.g., Life MD) to create independent demand.
- **Week 3 signals:** Built local Portfolio Review prototype overnight in Cursor (21 Jan). First hands-on UX review of dashboard (23 Jan) — identified colour/RAG confusion. Accepted Natalia's pushback on separate Portfolio Review tab gracefully. Framing CSM instruction collaboratively: "Set up a meeting with your account team, fill out the data together." Also blocked on Cursor tokens by 23 Jan.
- **14 Mar:** On Gainsight charter — demands business SLAs: integration cannot slow migration, cannot split CSMs between two systems, cannot block adoption squads from key info. Also added Samuel Gibson to Build in Five chat.
- **Concern:** Becoming emotionally invested in adoption — may push past stakeholder readiness.
- **Note:** Name previously misspelled as "Ben Brookes" in early analysis — correct spelling confirmed from Teams as "Ben Brookes."

### Natalia Orzechowska — Senior Director, CS Lead, Azmain's Manager (until 31 March)
- **Engagement level:** High. Runs weekly Portfolio Reviews using CLARA. Azmain's direct manager until 31 March 2026 (Diana Kazakova-Ivanova takes over 1 April).
- **Style:** Practical, process-focused. Pushes back on unnecessary features. Asks the right questions (e.g., "Should we consult CSMs on the business reqs?" re: Gainsight charter).
- **Key contributions:** Reframed "priority" from arbitrary to scorecard-aligned 31 accounts. Insisted on using dashboard filters in meetings rather than building separate tabs.
- **Week 3 signals:** Heavily engaged in Portfolio Review design (21 Jan) and Monday demo prep (23 Jan). Set key process rules: no editing during meetings, no formal RACI in first meeting deck (too heavy). Reviewing every slide and every UI element for the Monday demo. Highly detail-oriented. First genuine endorsement of the data input hub: "This looks really, really good."
- **14 Mar:** Engaged on Gainsight integration charter — asking about consulting CSMs. Agreed to Gainsight demo suggestion.
- **Concern:** CSM workload perception. Doesn't want CLARA to feel like more work.
- **Important context:** Owns Gainsight relationship. Sees CLARA as potentially reusable beyond IRP.

### Natalia Plant — Gainsight Governance & CLARA Release Cadence Lead
- **Engagement level:** High. Established fortnightly CLARA release governance (12 Mar).
- **Role:** Leads Gainsight team. Manages CLARA release cadence (Tuesday governance reviews, fortnightly releases).
- **Key contribution:** Two grads arriving April 7 for dedicated CLARA maintenance under her oversight. Ben Brookes restricted to sandbox.
- **IMPORTANT:** Different person from Natalia Orzechowska. Not Azmain's manager.

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
- **March signals:** Was briefly considering other roles in early March but has since committed to the programme. Energy high from mid-March onwards -- driving cross-OU expansion, Build in Five cascade, and Idris onboarding.
- **Risk:** Carries significant institutional knowledge — programme strategy, stakeholder relationships, Diya management. Knowledge documentation should continue as good practice.

## Tier 3 — Technical & Delivery

### Azmain — Programme Manager & CLARA Developer
- **Engagement level:** 100% consumed by CLARA + now building Friday on the side
- **Key tension:** Formally raised with Natalia (20 Feb) that the other five workstreams have had zero progress. Recognised this as early as 21 Jan.
- **Growth arc:** Learning Git, CI/CD, AWS in real-time on the job. Richard positioning this as a career growth vehicle.
- **March signals:** Now reports to Diana Kazakova-Ivanova (not Stacy). Building Friday PM app as side project — burned $500 Cursor in one day on it. Using Claude Code in cloud environment. Aware of BenVH's Nikhil Koli frustrations.
- **Risk:** Single point of failure for CLARA features. Bandwidth now split across CLARA + Friday + programme management. Richard is his primary mentor and strategic guide.

### BenVH (Van Houten) — Infrastructure
- **Role:** AWS deployment, CI/CD, security. The only person who can deploy.
- **Risk:** Single point of failure for infrastructure. If he's unavailable, nothing deploys.
- **Asset:** Has a personal patented CICD orchestration project (Phantom Agent). Thinking about how to make deployment "idiot proof."
- **March signals (CONCERNING):** Admitted his recent absence was not illness but being worn down by Nikhil Koli taking credit for his App Factory work, renaming it, and presenting his architecture as his own. Morale/retention risk. Also flagged on 3 Mar that four other apps are in the App Factory pipeline — he's under-resourced.
- **11 Mar (CRITICAL):** Conflict with Nikhil Koli at peak. BenVH cancelled Nikhil Koli's meetings, stopped responding to his messages, described daily boundary violations as "getting my blood boiling" and "taking too much of my mental acuity." Pivoted entire App Factory to MCP server architecture — both technically correct and strategically designed to make Nikhil Koli's UI work irrelevant. Channelling anger productively but retention risk acute. Asia-Pac teams (Singapore, Japan, Australia) interested in App Factory — adds pressure and validation simultaneously.

### Martin Davies — Developer (12-week assignment)
- **Focus:** Build in Five workstream
- **Status:** Back from holiday late Feb. Demo target: March 21.

## Tier 4 — Adjacent / Emerging

| Person | Domain | Status |
|--------|--------|--------|
| Kevin Pern | CS Agent (Copilot Studio) | Working alone, no programme oversight |
| Cihan | MD Product & Technology | **13 Mar: Brought entire product/tech team to see CLARA. Full personal endorsement — uses CLARA as a daily tool. Encouraged feedback and adoption. Drove ~4,000-5,000 SSO viewer import. Asked how product teams can contribute. Most senior product-side champion since Andy Frappe.** |
| Nikhil Koli | Tech consulting lead (new) | 50% App Factory / 50% CLARA. BenVH alleges daily boundary violations: scheduling deploys after being told no, introducing App Factory tasks to CAT team, going around BenVH to Richard. Richard planning direct confrontation and Ben Brookes escalation. To be redirected to Salesforce integration or AIG. Genuinely impressed by Martin's Build in Five demo (11 Mar) — unaware of plans to remove him. **16 Mar:** Also encroaching on graduate allocation — asked Emma Jaggs (grad manager) about replacing Elliot from his team, causing confusion with Azmain's separate 2-grad request for CLARA. Richard clarified the requests are separate. |
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
| Diana Kazakova-Ivanova | PM → Becoming Azmain's direct manager from 1 April 2026 (currently reports to Natalia Orzechowska) | Supportive of Friday development. Planning to present Friday vision to Ben/Charlotte. **12 Mar: First extended 1-1 with Azmain. Shared Kathryn Palkovics' COE objectives, confirmed the political threat, committed to discuss with Natalia Orzechowska. Shared IRP reporting slides and adoption runbook context. Invited Azmain to IRP weekly call. Growing into a key political ally and advisor. Weekly 1-hour 1-1 established.** |
| Martin Davies | Build in Five (WS6) | Exceptional output. Dashboard builder dramatically exceeded expectations (10 Mar). Richard compared to Databricks Genie. Live RM API integration working. Demo shifted to May. 12-week clock ticking but output justifies investment. |
| Kathryn Palkovics (referred to as "Catherine" in earlier audio transcripts) | Data alignment + Gainsight governance + COE lead | March: Offered to help with governance and App Factory decision tree. 11 Mar: Joined Salesforce integration design session. Enthusiastic about App Factory approach. Confirmed Gainsight hard launch March 30. **12 Mar (CRITICAL): Organised Gainsight integration meeting without consulting Clara team — team describes this as a "blindside." Ben Brookes, Richard, Azmain, BenVH all furious. Kathryn's COE (digital engagement, enablement, Gainsight/SFDC retirement) overlaps with AI programme. Diana Kazakova-Ivanova warned Azmain she may try to absorb the programme. Multiple interventions planned: Diana Kazakova-Ivanova to Natalia, Richard to Diya. Azmain: "If she's placed in charge, I leave." Status shifted from perceived ally to confirmed political threat.** **14 Mar: Asserted COE authority on Gainsight integration charter — requested to be added to the project team, claiming COE handles business reqs for CSMs when scoping. Pushed back on Richard's frustration, framing the prior meeting as "just exploring." Offered Gainsight demo so the team understands how it's used.** |
| Dan Flemington | Sales | March: New stakeholder with existing tools. Julia Valencia identified for Salesforce access. In Vienna at event (w/c 9 Mar). |
| Juliet Valencia | Sales analytics / Power BI dashboards | New 9 Mar. Manages Sales Hub dashboards. Clarified data ownership: Dan's data likely from SPM team (Tableau), not her. Uses Cursor for dashboards. Cooperative, good data governance instincts. Will connect team with SPM contacts. 11 Mar: Struggling with Azure/Power Automate/Copilot Studio integration (same wall insurance team hit). Has confidential data (commission targets) — chose own AWS infra over shared hosting. Also built Moody's branded PowerPoint generator independently — Slidey convergence opportunity. |
| Arno | Advisory team project lead | New 9 Mar. Leads weekly advisory project status call under Charlotte's org. Manages ILS, climate, banking advisory staffing. Diana Kazakova-Ivanova brought Azmain to observe. |
| Gina Greer | Banking customer engagement (central) | New 10 Mar. Mapping banking AI initiatives. Same stage as insurance Nov 2025. Potential cross-OU ally. |
| Olivier | Banking AI enablement lead | New 10 Mar. Thoughtful about tool selection. Working with Nick Louder/Kentucky teams. Deployment gap concern. |
| Jack Cheyne | Life insurance | New 10 Mar. Technically curious about NME. Aware of CAP from banking. Potential cross-OU expansion. |
| Christian Curran | Life insurance | New 10 Mar. Focused on SSO, security, RBAC practicalities. |
| Mike Bibo | Risk Modeller demo team lead | Identified 10 Mar as critical for Build in Five. Demos RM to customers. |
| Samuel Gibson | Risk Modeller demo team (UK) | Identified 10 Mar. Under Bibo. **16 Mar: Added to Build in Five group chat by Ben Brookes. Keen on MCP server possibilities for customer demos. Wants to show clients and get them thinking through solutions. Says "Mike B sees the DataLake as the future of our solutions." Actively engaged — not just a name on a list.** |
| Prashant | Developer (planned) | To be allocated to help Azmain with Friday development. |
| Natalie Bath | Sales / reports to Helen Ryder | New 11 Mar. Saw MENA's agent demo at Miami sales connect. Asked Idrees to run agent view on AON data for Rob Fulber's meeting. Cross-OU interest signal from sales side. |
| Tina Palumbo | Gainsight Business Systems team | New 12 Mar. Presented bi-directional Clara-Gainsight integration proposal. Cooperative and solutions-oriented. Wants POC to validate connectivity. No fixed timeline — March 30 onboarding deadline takes priority. |
| Rajesh | Gainsight solution architect | New 12 Mar. Explained batch (S3) and real-time API options for integration. Pragmatic. Will share API documentation. |
| Nadeem | Gainsight project manager | New 12 Mar. Coordinating follow-up sessions for Clara-Gainsight POC. |
| Rob Fulber | Senior leader | Meeting Dan Dick (Global Head Cat Risk, AON) next week in London. Cross-OU account intelligence opportunity. |
| Nils | Banking Credit team — AI training lead | New 13 Mar. Runs agent day framework: 4-tier model, pre-work methodology, transit teachers, bi-weekly follow-ups. Offered to share slide deck and materials. Quarterly cross-OU cadence agreed. |
| Wasim | Banking Credit team | New 13 Mar. Non-coder success story — built functioning agent via natural language. Validates accessibility of AI enablement approach. |
| Georgie | Banking Credit team | New 13 Mar. Presented agent examples including document summarisation and compliance screening. |
| Lucia | Customer & Model Success team lead | New 13 Mar. Facing wave of dashboard requests. Tableau sunsetting by Sep 2026 creates urgency. Immediately saw value in App Factory. Offered Salesforce integration testing help. Maintaining Confluence documentation. |
| Joel | Customer & Model Success team | New 13 Mar. R/Streamlit developer. Keen to explore App Factory for hosting team's apps. |
| Ollie | Product team | New 13 Mar. Asked how to contribute to CLARA during product/tech demo. |
| Julie | Product team | New 13 Mar. Asked about the difference between CLARA and Gainsight during product/tech demo. |
| Emma Jaggs | Graduate rotation manager | New 16 Mar. Manages graduate allocation. Incorrectly merged Azmain's 2-grad CLARA request with Nikhil Koli's separate Elliot replacement request — told them only 2 total. Richard clarified the requests are separate. |
| Alvin | Graduate (London) | Arriving Q2 2026 for CLARA maintenance. Interviewed and chosen by Azmain specifically for AI work. |
| Sam (grad) | Graduate (New York) | Arriving Q2 2026 for CLARA maintenance. Interviewed and chosen by Azmain specifically for AI work. Different person from Samuel Gibson. |
| Elliot | Former member of Nikhil Koli's team | Brought into the AI programme (specific project TBD). Nikhil requesting a replacement for him through the grad rotation. |
| DIA | Cross-OU coordination | Manages customer engagement across segments. Interested in Moody's-wide retention dashboards. Idrees looped her into retention dashboard thread (11 Mar). Key person for cross-OU pressure on Charlotte. |

## Dynamics to Watch

1. **Ben vs Josh** — Speed vs caution on CSM release. Ben pushing, Josh gating.
2. **Azmain's bandwidth** — Formally flagged. If not resolved, other workstreams stay stalled. Week 3 confirms: all five non-CLARA workstreams have had zero progress.
3. **Diya's attention** — Hard to get, easy to lose. Must be fed carefully. Week 3: did not join the one call designed for her input.
4. **CLARA vs Sales Recon** — Standalone now, but when does convergence happen? Jamie's team is tiny. Week 3: George discovered his account planner overlaps with Sales Recon. Critical fork identified: if Jamie says no to migration, Ben needs a permanent maintenance team.
5. **BenVH as bottleneck** — Only deployer. Infrastructure decisions (CDK vs CloudFormation) affect who else can deploy. Week 3: absent for HighRox race, causing real delays. His Alembic migration broke use case creation by 23 Jan.
6. **Deployment fragility** — Week 3 theme. Richard and Azmain shifted from "move fast" to "don't break things." No tested rollback procedure. Schema changes now require BenVH approval before execution.
7. **Corporate tooling crisis** — Cursor tokens exhausted for both Azmain and Ben by 23 Jan. Richard personally paying for Claude Code as workaround. Developer laptops only just approved.
8. **Richard knowledge concentration** — Richard carries significant institutional knowledge. Knowledge sharing with Diana Kazakova-Ivanova and the broader team should continue. Flight risk resolved as of mid-March.
9. **BenVH/Nikhil Koli conflict (ESCALATING - 11 March)** — Now at crisis point. BenVH cancelled Nikhil Koli's meetings, stopped responding. Richard planning direct confrontation and Ben Brookes escalation. Nikhil Koli to be redirected to Salesforce/AIG.
10. **Friday as scope creep risk (March)** — Azmain building a PM app on the side while already stretched thin on CLARA and five other workstreams.
11. **Security/compliance exposure (March)** — Personal Claude accounts used for Moody's work. Audit found it. Team spending personal money on tooling.
12. **Cross-OU expansion pressure (10 March)** — Banking (Gina/Olivier) and Life (Jack/Christian) both want collaboration. Validates approach but risks further stretching an overloaded team.
13. **Bedrock cost trajectory (10 March)** — $1,163 in two weeks, on pace for $10K/month. No cost attribution. Tags broken. New frontier of the same budget problem.
14. **App Factory MCP server pivot (NEW - 11 March)** — BenVH redefining App Factory as a middleware MCP server. Architecturally sound and addresses Asia-Pac demand, but adds more to BenVH's workload while he's already in crisis.
15. **Salesforce integration design crystallising (11 March)** — One-way read, Cases/CaseFeed only, four consumer groups (Bernard, Courtney, Kevin, CLARA). Kathryn Palkovics fully engaged. Tomorrow's Gainsight meeting is the next milestone.
16. **Slidey convergence (NEW - 11 March)** — Multiple teams (Richard, Juliet, Richard's manager) building PowerPoint generators independently. Cross-team meeting planned for next Tuesday. Could become App Factory's most widely adopted tool.
17. **Gainsight March 30 hard launch (11 March)** — Confirmed by Kathryn Palkovics. No IRP data expected at launch, but "does Clara sync?" questions will start immediately after.
18. **Kathryn Palkovics (Catherine) COE political threat (12 March, ESCALATING 14 March)** — Kathryn's Centre of Excellence mandate (digital engagement, enablement, Gainsight/SFDC retirement) overlaps directly with AI programme. Organised Gainsight meeting as blindside. Full team (Azmain, Richard, Ben Brookes, BenVH) furious. Diana Kazakova-Ivanova advising tactically. Multiple interventions planned: Diana Kazakova-Ivanova→Natalia, Richard→Diya. **14 Mar: Kathryn now asserting COE authority on the Gainsight charter itself — requesting to be added to project team, claiming COE handles business reqs for CSMs. Pushing back on Richard's frustration, framing the initial meeting as "just exploring." The charter process is becoming a battleground for who controls the integration.**
19. **CLARA entering maintenance mode (12 March)** — Natalia Plant established fortnightly release governance. Two grads arriving April 7 for dedicated maintenance. Ben Brookes restricted to sandbox. This is a programme maturation signal.
20. **Adoption runbook collaboration (12 March)** — Rhett built digital runbook, Diana Kazakova-Ivanova's PM team built Excel version. Agreed to merge efforts. Over 50% of adoption governance owners already AI-enabled through Clara. Potential overlap with George's account planning.
21. **Graduate rotation resource conflict (NEW - 16 March)** — Azmain requested and interviewed 2 grads (Alvin, London; Sam, New York) specifically for AI/CLARA work. Nikhil Koli separately requested replacement for Elliot. Emma Jaggs (grad manager) merged the requests, saying only 2 available. Richard clarified to Emma that the requests are separate. Adds to the Nikhil friction pattern — he's now encroaching on resources, not just credit/IP.
22. **Build in Five stakeholder cascade (NEW - 16 March)** — Richard wants to organize a share-out for Build in Five similar to App Factory's approach. Key stakeholders: MPS, Sales, Product. Samuel Gibson actively engaged — keen on MCP server for customer demos. This is the programme starting to commercialise Build in Five.
