# Customer Success Gen AI Programme — Full Overview

**Programme:** CS Gen AI Programme, Moody's Analytics (Insurance Division)
**Duration:** January 2026 — present (11 weeks as of 18 March 2026)
**Scope:** 11 concurrent projects across three strategic pillars
**Team:** Core team of ~6, extended network of 40+ stakeholders across four operating units
**Sponsor:** Diya Sawhny (SVP, Executive Sponsor)

---

## Programme Genesis

The programme launched in the first week of January 2026 when Ben Brookes — the de facto product owner — revealed a prototype he'd built solo over Christmas: CLARA, an IRP adoption tracker. The prototype exposed that 12 client migrations had been completed without anyone in leadership knowing. This single artefact validated the core thesis: Customer Success had a data visibility problem, and AI-assisted tooling could solve it faster than traditional procurement cycles.

Within four weeks, the programme went from prototype to production. An AWS infrastructure pivot (from Azure, which was blocked by corporate approvals), a CI/CD pipeline, authentication, role-based access, and a live data model were all stood up by a team that was simultaneously learning Git, Docker, and cloud deployment. CLARA went live with the full CSM team on 27 January, the same day Diya Sawhny publicly positioned it as critical to the division's scorecard.

---

## Strategic Structure

Following executive endorsement on 23 February (described internally as "the most consequential twenty minutes in the programme's history"), the programme was organised into three pillars:

| Pillar | Focus | Projects |
|--------|-------|----------|
| **1. IRP Portfolio Governance** | Client adoption tracking, data-driven decision making, migration oversight | CLARA, Training & Enablement |
| **2. Customer Intelligence & Embedded Platform** | AI agents surfacing insights within existing workflows | Customer Success Agent, Navigator L1 Automation, Cross-OU Collaboration |
| **3. Internal Productivity & Innovation** | Tools that accelerate the team's own work | Build in Five, Friday, Slidey, App Factory, TSR Enhancements |

**Programme Management** (PR9) operates as the cross-cutting governance layer.

---

## The Arc: January to March 2026

### Phase 1 — Explosion (Weeks 1-4, Jan 6 - Jan 27)

From concept to live product in four weeks. The team adopted a "build first, ask permission later" posture that proved effective but created technical debt and compliance exposure.

**Key milestones:**
- CLARA prototype revealed (7 Jan), exposing 12 hidden completed migrations
- AWS infrastructure pivot completed in days (Azure approvals would have taken months)
- CI/CD pipeline operational by Week 2
- Advisory team (Liz Couchman, Stacy Dixtra, Steve Gentilli) gave first strong endorsement
- Josh Ellingson reframed CLARA's narrative from "data quality" to "data visibility" — an adoption-friendly positioning that shaped the entire rollout
- CLARA launched live with full CSM team (27 Jan)
- Sales Recon executive session + CLARA portfolio review kickoff on same day
- Integration-first architecture decided: CLARA and Sales Recon coexist with API bridges

**Decisions made:** 27 (decisions #1-27 in the log)

### Phase 2 — Stress Testing (Weeks 5-6, Feb 2 - Feb 12)

First real contact with users exposed fragility. A deployment refresh caused CSM data entries to vanish — the first trust crisis. But the response was swift: the issue was contained, Natalia Orzechowska's composure during the Portfolio Review kept CSM confidence intact, and the team introduced spec-first schema governance.

**Key milestones:**
- First live Portfolio Review delivered (3 Feb) — CSMs had entered data over the weekend, proving willingness
- Data loss incident managed without losing user trust
- RBAC fix for Azure AD username/email mismatch
- Diya's first substantive engagement (11 Feb) — asked the right questions about KPIs and strategic alternatives
- Josh Ellingson defined CLARA's scope as IRP migrations only, resolving months of ambiguity about CLARA vs Gainsight
- Claude Code access secured via AWS Bedrock, ending the personal-subscription compliance crisis
- CSM workshops revealed the reciprocity question: "What do I get back for entering this data?"

**Complications:** Richard formally reprimanded for Cursor usage on proprietary data. Team members spending ~$400/month from personal funds on AI tooling. Compliance and tooling sustainability became urgent governance issues.

### Phase 3 — Governance Reckoning (Weeks 7-8, Feb 19 - Feb 27)

The programme hit an honest reckoning. Azmain formally escalated to Natalia Orzechowska that five of eleven workstreams had made zero progress — CLARA was consuming all bandwidth. The same week, Ben Brookes revealed he'd scheduled a demo for Andy Frappe (President, Moody's Analytics) without informing the development team.

**Key milestones:**
- Feature freeze declared until Diya governance meeting (25 Feb)
- Diya's governance session endorsed the three-pillar structure and approved a twelve-week resource plan: Martin Davies 75%, Chris M 50%, Nikhil 50%, BenVH 50%, rotating graduate from 7 April
- MCP server strategic conversation — first forward-looking architecture discussion in weeks
- Budget crisis formally acknowledged: $750 consumed in three days of Cursor usage alone
- Programme shifted from "can we build it?" to "can we sustain it?"

### Phase 4 — Expansion Under Strain (Weeks 9-11, Mar 3 - Mar 16)

The programme's reputation outran its resources. Banking and Life Insurance divisions both arrived asking for what the Insurance team had built. Idrees Deen began building a cross-OU coalition. Martin Davies' Build in Five output exceeded expectations. Slidey generated more executive excitement than CLARA.

But beneath the expansion, three retention crises converged:
- **BenVH** admitted burnout after Nikhil Koli presented App Factory work as his own, derailing a Microsoft partnership BenVH had been cultivating. Morale dropped to crisis level.
- **Richard Dosoo** briefly explored other positions within Moody's, citing exhaustion and feeling undervalued.
- **Azmain** was spotted browsing Moody's internal careers site.

All three stabilised by mid-March — Richard recommitted after strategic conversations about the programme's direction, BenVH's situation was addressed by redirecting Nikhil to AIG, and Azmain's reporting line shifted to Diana Kazakova-Ivanova (effective 1 April), providing fresh management support.

**Key milestones:**
- Slidey (AI presentations) went from concept to auth-enabled collaborative platform in one week
- Friday's skeleton built by 30 concurrent AI agents in a single day
- CLARA shown to Life SLT; Gainsight integration formalised with charter-first approach
- Cross-OU demand validated (banking, life insurance, KYC all requesting capability)
- Diana identified critical governance gap: IRP consulting projects ($800K budget) had no tracking mechanism
- HD model data deadline set (35 Americas clients by 31 March)
- Kathryn Palkovics (COE) identified as political threat — team shifted from reactive to strategic framing for Ben Brookes

**Current state (Week 11):** Governance crystallising. The wild-west building period is being replaced by structured tracking demands. The programme's most striking characteristic is the gap between what it's building and what it's tracking.

---

## Project-by-Project Status (as of 16 March 2026)

### PR1: CLARA (IRP Adoption Tracker) — AMBER, Stable

The programme's flagship. A React/FastAPI/SQL Server application tracking IRP client adoption, migration status, blockers, and action plans across ~68 accounts.

**What it does:** Dashboard views for CSMs, managers, and executives. Portfolio review support. Use case tracking. Blocker/action plan management. Data input hub. Scorecard alignment for 31 priority accounts.

**Current state:** Live and stabilising. Feature-complete for core use. Expanding scope to HD model data entry (26 of 68 clients populated, 35 Americas clients need data by 31 March). Gainsight integration in charter phase (POC earliest May). Fortnightly release cadence established by Natalia Plant.

**Team:** Azmain (PM + lead dev), Ben Brookes (product owner), Richard Dosoo (technical bridge), BenVH (infrastructure/CI/CD), Chris M (bug fixes), Natalia Plant (release governance), two rotating graduates arriving 7 April.

**Key risks:** Azmain and BenVH as single points of failure. Scope creep from HD model data and consulting PM tracking. Data quality undermining trust. Gainsight political dynamics (Kathryn Palkovics asserting authority). Sales Recon convergence timeline unclear.

**Relationship to Sales Recon:** CLARA is the interim solution. Sales Recon is the long-term end-state. Integration-first approach: coexist with API bridges, not merge.

---

### PR2: Friday (CS AI Agent / PM Tool) — AMBER, Blocked

Originally "Adoption Charter Workflow," pivoted to a project management tool combining capabilities of Asana, Trello, Monday.com, and JIRA.

**Current state:** Skeleton built (by Azmain using Claude Code's cloud environment, with 30 concurrent AI agents in a single day). Not customised. Blocked by Slidey priority consuming all bandwidth. Strategic decision: CLARA's existing PM section will serve as temporary stepping stone; Friday is the long-term play.

**Key dynamic:** Diana pragmatically chose to enable CLARA's PM features for immediate consulting project visibility rather than wait for Friday. Azmain agreed: "People need to feel the pain before you drink the juice."

---

### PR3: Build in Five — GREEN, Active

A framework demonstrating that AI-assisted tooling can produce working solutions in five minutes rather than twelve months. Two tracks: (1) customer-facing pre-sales tool, (2) internal app factory pipeline.

**Current state:** Martin Davies (exceptional 12-week contractor) building MVP with three IRP API modules. Demo target shifted from 21 March to May (exceedance event). Apollo dashboard being reverse-engineered as proof of concept.

**Key achievement:** Martin's output has exceeded expectations to the point where "product teams are getting nervous." The Build in Five concept is the programme's strongest pitch for AI-accelerated delivery.

**Tech stack:** Cursor (Opus for planning, Sonnet for building), IRP APIs, Docker for local MVP. No LLM integration in the product itself — the AI is in the build process, not the output.

---

### PR4: Training & Enablement — RED, Stalled

Elevated to a full workstream at December 2025 steerco after senior leadership feedback. Conceptual framework designed (solution-focused training buckets, train-the-trainer model) but zero execution since January.

**Root cause:** No dedicated owner. Azmain is nominal lead but has zero bandwidth. Framework exists on paper (dashboarding, presentations, data analysis, automation) but no delivery.

**Cultural challenge:** Wide gap between early adopters (Ben, Azmain, George Dyke) and mainstream users. Resistance to rapid iteration observed in CSM workshops.

---

### PR5: Navigator L1 Automation — AMBER, Early Stage

Concept: use IRP Navigator's upcoming API support (via MCP server) to automatically answer Level 1 support tickets.

**Current state:** Product team (Cihan, Lonny) building MCP server independently. No CS-side work started. Azmain admitted he "doesn't fully understand" this workstream. Clear path identified through Build in Five integration, but no CS-side owner assigned.

**Key blocker:** No clear division between what the product team delivers and what the CS team needs to build.

---

### PR7: Customer Success Agent — RED, Blocked

A Salesforce-integrated AI agent for CSM workflows. Kevin Pern built a prototype using Microsoft Copilot Studio, working alone with no programme oversight.

**Current state:** Genuinely blocked on Salesforce API access. Richard hopes to piggyback on Gainsight team's Salesforce access pattern. Wednesday CLARA POC scope call is the next milestone for unblocking.

**Overlap risk:** Sales Recon's "Intelligence Anywhere" covers similar ground (Salesforce data surfaced into Copilot). Delineation needed.

---

### PR8: Cross-OU Collaboration — GREEN, Active

The programme's cross-divisional expansion. Banking, Life Insurance, and KYC divisions have all expressed interest in the capabilities the Insurance team has built.

**Key relationships:**
- **Idrees Deen** (Banking CS) — building a cross-OU coalition, formally engaged as strategic ally
- **Life Insurance SLT** — CLARA demonstrated; interest validated
- **Banking KYC** — early conversations about applicability

Quarterly cadence established for cross-OU engagement.

---

### PR9: Programme Management — AMBER, Improving

The governance layer. Entered March with significant gaps: no documentation, no formal cost tracking, no resource allocation framework.

**Improvements in progress:**
- Three-pillar structure endorsed by Diya (23 Feb)
- Twelve-week resource plan approved
- Feature freeze mechanism proven effective
- Fortnightly release cadence for CLARA
- Diana driving consulting project governance
- Weekly plan review cadence established (Azmain, Richard, Ben)

**Remaining gaps:** No per-project budget tracking (AWS Bedrock at $1,163 in two weeks, trending toward $10K/month). Documentation close to zero. Security/compliance exposure from tooling choices.

---

### PR10: App Factory — AMBER, Pivoting

Infrastructure for deploying AI-built applications at scale. BenVH's domain — includes the patented Phantom Agent CI/CD orchestration system.

**Current state:** Pivoting to MCP server architecture using Bedrock AI agents. App governance approval board being established. Complicated by the BenVH/Nikhil credit attribution conflict (now resolved).

---

### PR11: TSR Enhancements — AMBER, Active

Cat bond automation work led by Idris Abram. Separate from the core programme but connected through shared infrastructure and the Build in Five framework.

---

### PR12: Slidey (AI Presentations) — GREEN, Active

The programme's breakout success. An AI-powered collaborative presentation platform generating branded HTML slide decks from prompts.

**Current state:** Auth landed, RBAC partially wired. Moving to data scoping and performance. Richard described it as generating more executive excitement than CLARA. Consumed the entire team's bandwidth for a full week (acknowledged as opportunity cost by Azmain).

**Architecture journey:** Started as prompt-to-HTML generator. Repositioned to collaborative executive workflow with RBAC, markdown content layer, and agentic extensions after Diya's feedback that HTML was unfit for executive review.

**Team:** Richard Dosoo (architecture lead), Ben Brookes (product vision), BenVH (auth/infrastructure), Amit Gondha (early tester).

---

## Stakeholder Landscape

### Decision Makers & Sponsors

| Person | Role | Engagement | Dynamic |
|--------|------|------------|---------|
| **Diya Sawhny** | Executive Sponsor | Low initially, substantive from Feb | Impatient with detail; scorecard/KPI focused; endorsed three-pillar structure in the most consequential 20 minutes of the programme |
| **Andy Frappe** | President, Moody's Analytics | Episodic, high-stakes | Saw CLARA demo 20 Feb; wants centralised Power BI migration dashboard; highest-stakes audience in the programme |
| **Ben Brookes** | De Facto Product Owner | Maximum | Pushes speed relentlessly; 5am training sessions; emotionally invested; "kill CSMs with kindness" strategy; shopping CLARA to Life leadership |
| **Natalia Orzechowska** | Senior Director, CS Lead | High | Practical, process-focused; runs Portfolio Reviews; Azmain's manager until 31 Mar |
| **Diana Kazakova-Ivanova** | Incoming CS Lead | Rapidly increasing | Emerging as programme's governance voice; identified consulting tracking gap; takes over Azmain's line management 1 Apr |

### Influential Gatekeepers

| Person | Role | Dynamic |
|--------|------|---------|
| **Josh Ellingson** | CSM Leadership | Cautious gatekeeper turned governance contributor; defined CLARA scope as IRP-only; tension with Ben on release timing |
| **George Dyke** | CSM Leadership | Comfortable with ambiguity; bridges management and practitioner perspectives; building account planner; natural training lead |
| **Stacy Dixtra** | Data & Reporting | Cautious, thorough; manages 300-slide decks; warns about running fast; prefers Excel exports; quality enforcer |
| **Natalia Plant** | Gainsight & CLARA Releases | Established fortnightly release cadence; governance gating; different person from Natalia Orzechowska |

### Core Build Team

| Person | Role | Dynamic |
|--------|------|---------|
| **Azmain** | Programme Manager & CLARA Developer | 100% consumed; learning AWS/Git/CI/CD on the job; single point of failure; stretched across all projects; increasingly assertive on PM authority |
| **Richard Dosoo** | Programme/Operational Owner | Technical bridge and strategic direction-setter; Slidey architecture lead; briefly considered leaving in early March; carries most institutional knowledge |
| **BenVH** | Infrastructure | AWS/CI/CD/security; single point of failure for deployment; patented Phantom Agent; burnout crisis in March from credit misattribution; four other apps in pipeline |
| **Martin Davies** | Build in Five Developer | 12-week contractor; exceptional output; back from holiday late Feb; demo target shifted to May |

### Political Dynamics

**Kathryn Palkovics (COE):** The programme's most significant political challenge. Asserting authority over AI programme scope through a Centre of Excellence that could absorb or constrain the CS team's autonomy. The team shifted from reactive fury (12 March) to deliberate strategic framing (16 March) — building a case for Ben Brookes that the programme has Diya's direct approval and Kathryn's COE is orthogonal to it.

**Nikhil Koli:** Boundary-crossing pattern caused the programme's most acute personnel crisis. Presented App Factory work as his own, derailing BenVH's Microsoft partnership. Redirected to AIG (16 March) as a resolution, though the team expects the pattern to reassert.

**Cross-OU coalition building:** Idrees Deen (Banking CS) emerging as strategic ally. The programme's success is creating demand from Life Insurance and Banking divisions, validating the model but stretching resources further.

---

## Governance Evolution

The programme's governance matured significantly over 11 weeks:

| Week | Governance State |
|------|-----------------|
| 1-4 | None — "build first, ask permission later" |
| 5-6 | Reactive — responding to data loss, compliance incidents |
| 7 | Crisis — feature freeze, honest reckoning about stalled workstreams |
| 8 | Structural — Diya endorsement, three-pillar framework, resource allocation |
| 9-10 | Expanding — release cadence, charter-first approach, approval boards forming |
| 11 | Crystallising — consulting governance, HD data accountability, strategic political framing |

**84 decisions** logged across 11 weeks. **54 risks** tracked. **36 open threads** monitored. **714+ action items** generated and tracked.

---

## Key Metrics & Indicators

| Dimension | Current | Trend |
|-----------|---------|-------|
| Projects active | 11 | Stable |
| Projects with meaningful delivery | 4 (CLARA, Build in Five, Slidey, Cross-OU) | Improving |
| Projects stalled or blocked | 3 (Training, CS Agent, Navigator L1) | Persistent |
| Stakeholders engaged | 40+ across 4 OUs | Growing |
| Decisions logged | 84 | 7-8 per week |
| Risks tracked | 54 | Growing |
| Open threads | 36 | Growing |
| Team retention crises managed | 3 (all resolved) | Improving |
| Cross-OU demand | Banking, Life, KYC | Accelerating |
| AWS Bedrock spend | ~$1,163/2 weeks | Needs controls |
| CLARA clients with HD data | 26/68 | 35 needed by 31 Mar |

---

## Programme Risks (Top 10)

| # | Risk | Severity | Status |
|---|------|----------|--------|
| 1 | Single points of failure (Azmain, BenVH) | CRITICAL | Mitigating — graduates arriving Apr 7 |
| 2 | Kathryn Palkovics COE absorbing programme autonomy | HIGH | Active — strategic response being crafted |
| 3 | Budget/cost tracking absent | HIGH | Unresolved — trending $10K/month with no per-project visibility |
| 4 | Documentation near zero | HIGH | Unresolved |
| 5 | HD data entry deadline (31 Mar) | HIGH | Active — CSMs want bulk upload |
| 6 | IRP consulting project tracking gap ($800K invisible) | HIGH | Active — Diana driving CLARA PM extension |
| 7 | Slidey consuming all bandwidth | MEDIUM | Acknowledged — opportunity cost accepted |
| 8 | Sales Recon convergence timeline unclear | MEDIUM | Watching |
| 9 | Gainsight political dynamics | MEDIUM | Charter-first approach managing risk |
| 10 | Security/compliance exposure from tooling | MEDIUM | Improving — Bedrock access secured |

---

## What the Programme Has Delivered (11 Weeks)

1. **CLARA** — Live production application serving ~68 client accounts, used in fortnightly Portfolio Reviews, management dashboards, and executive reporting
2. **Three-pillar strategic framework** — Endorsed by executive sponsor, providing defensible programme structure
3. **Twelve-week resource plan** — First formal resource allocation in the programme's history
4. **Cross-OU demand validation** — Banking, Life, and KYC divisions requesting capabilities
5. **Build in Five framework** — Proving AI-accelerated delivery model with exceptional contractor output
6. **Slidey** — From concept to auth-enabled collaborative platform in one week, generating more executive excitement than any other deliverable
7. **Friday skeleton** — PM tool architecture built in a single day using 30 concurrent AI agents
8. **Gainsight integration charter** — Formal requirements-first approach to the most politically complex integration
9. **Governance structures** — Release cadence, feature freeze mechanism, spec-first schema governance, approval boards
10. **84 logged decisions, 54 tracked risks, 36 monitored threads** — Programme intelligence infrastructure

---

---

# Mapping to Director - Program Manager Responsibilities

The following maps the CS Gen AI Programme experience directly to the key responsibilities listed in the Director - Program Manager (Banking KYC) job description.

---

### "Leads global delivery and integration... across direct and partner-led implementations"

The programme delivers across 11 concurrent projects spanning four operating units. CLARA integrates with Salesforce, Gainsight, Sales Recon, and IRP APIs. The Gainsight integration alone involves a charter-first approach managing political dynamics between CS, product, and platform teams. Cross-OU delivery now spans Insurance, Banking, Life, and KYC — with demand validated from all four.

### "Develop and deliver the prioritization roadmap, balancing client and partner requirements with internal priorities and resource constraints"

The three-pillar framework (IRP governance, customer intelligence, internal productivity) was designed specifically to balance competing demands. The twelve-week resource plan allocates fractional capacity across projects: Martin 75%, Chris 50%, Nikhil 50%, BenVH 50%. Feature freeze was used as a governance mechanism when scope outran capacity. HD model data entry competes with consulting project tracking which competes with Slidey executive demos — all requiring explicit prioritisation.

### "Oversee end-to-end delivery... ensuring high-quality, enterprise-scale integrations"

CLARA went from prototype to production in four weeks: React frontend, FastAPI backend, SQL Server on AWS RDS, CI/CD pipeline, RBAC, audit trail. The team managed a mid-flight infrastructure pivot (Azure to AWS), a data loss incident without losing user trust, and a compliance crisis around AI tooling — all while maintaining fortnightly release cadence and serving ~68 client accounts.

### "Manage partner-led implementations... establishing clear accountability, success metrics, and escalation paths"

The Gainsight integration charter is the clearest parallel: a formal requirements document establishing phased delivery (Phase 0 structured review before development), accountability between CS and Gainsight teams, and explicit escalation paths through Natalia Plant's governance cadence. The Sales Recon coexistence model (integration-first, API bridges, not merger) is another example of managing a partner platform relationship with clear delineation.

### "Establish governance structures for program oversight, risk management, issue resolution, and executive reporting"

Governance evolved from nothing (Week 1) to a structured framework by Week 11: three-pillar strategic framework endorsed by executive sponsor, fortnightly release cadence with Tuesday governance reviews, feature freeze mechanism, charter-first integration approach, risk register (54 risks), decision log (84 decisions), open thread tracker (36 threads), weekly programme summaries, and executive reporting for Portfolio Reviews and presidential demos.

### "Drive portfolio-level decision making across multiple concurrent implementations to optimize resource utilization and business impact"

Eleven concurrent projects competing for a core team of six. The governance reckoning in Week 7 — where Azmain formally escalated that five workstreams had zero progress — led directly to the resource allocation framework. Portfolio-level decisions include: which projects get bandwidth (CLARA and Slidey, at the cost of Training & Enablement and Navigator L1), when to use interim solutions (CLARA PM features instead of waiting for Friday), and when to block scope expansion (feature freeze, Gainsight charter).

### "Build and maintain executive relationships with clients, serving as sponsor for high-priority or at-risk engagements"

The stakeholder map spans 40+ people across four tiers. Executive relationships managed include: Diya Sawhny (sponsor engagement from absent to active), Andy Frappe (presidential demo), Ben Brookes (daily product direction), Kathryn Palkovics (political threat requiring strategic framing), and Idrees Deen (cross-OU coalition building). The BenVH retention crisis and Richard's brief disengagement were both managed through direct relationship intervention.

### "Partner with Product Management to translate client and market feedback into product requirements and roadmap prioritization"

CSM workshop feedback ("what do I get back?") directly shaped CLARA's feature roadmap. Josh Ellingson's "data visibility" reframing changed the product narrative. The Build in Five framework was designed to demonstrate AI-accelerated delivery to clients, translating internal capability into market-facing value. Diana's identification of the consulting tracking gap ($800K budget with no visibility) is driving CLARA's PM extension.

### "Lead cross-functional delivery teams spanning Product Management, Product Engineering, Project Management, and Data Governance"

The programme spans: Product (Ben Brookes, Kevin Pern), Engineering (BenVH, Martin Davies, Chris M), Project Management (Azmain, Diana), Data Governance (Stacy Dixtra, Natalia Plant), CSM Operations (Josh Ellingson, George Dyke), and Executive Leadership (Diya, Andy Frappe). The Gainsight integration alone requires coordination across CS, product, platform, and governance teams.

### "Define and track key performance indicators related to delivery quality, customer satisfaction, portfolio health, and financial performance"

HD model data collection (five-dimension baselining: scientific excellence, decision utility, risk currency, operability, business impact) provides the KPI framework. CLARA tracks adoption status, blocker counts, action plan completion, and migration progress across ~68 accounts with 31 scorecard-aligned priority accounts. Programme health is tracked weekly across nine dimensions. Cost tracking is the acknowledged gap — AWS Bedrock trending $10K/month with no per-project visibility.

### "Build, mentor, and develop a high-performing delivery organization, fostering collaboration, accountability, and continuous improvement"

The programme took a team that was learning Git, Docker, and AWS on the job and delivered a production application in four weeks. Three retention crises were identified and resolved through direct intervention. Reporting lines were restructured (Azmain to Diana) to provide better management support. A train-the-trainer model was designed (though not yet executed) to scale capability beyond the core team. The graduate rotation programme (starting 7 April) is the first step toward building sustainable capacity.

---

*Document generated 18 March 2026 from programme intelligence tracked across 11 weeks, 50+ transcripts, 84 decisions, 54 risks, and 40+ stakeholder interactions.*
