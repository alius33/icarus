"""One-time script to backfill source_transcript_id and context for weeks 1-3 incomplete actions,
and carry unresolved actions into week 4."""

import requests

BASE = "http://localhost:8000/api"

# ── PART 1: PATCH all 15 incomplete actions with context ──

patches = [
    # ═══ WEEK 1 ═══
    {
        "id": 35,
        "source_transcript_id": 60,
        "context": (
            "**CLARA feature freeze** was mandated after Diya endorsed the three-pillar programme "
            "structure on 23 Feb. Scope is locked to **insurance IRP only** — no Life roadmap, no "
            "multi-tenant expansion.\n\n"
            "The feedback backlog is significant: CSMs are treating CLARA like an enterprise product "
            "and submitting feature requests at scale. **Azmain** advocated for strict triage discipline "
            "— bugs get fixed, feature requests get logged but deferred. The **flat-pack model** "
            "(stripping out IRP-specific elements for cross-OU reuse) was proposed but is post-freeze "
            "work.\n\n"
            "**Peter Kimes** submitted structured blocker feedback (User Voice URLs, JIRA IDs, Case URLs) "
            "but the team decided NOT to import User Voice data wholesale — links only, keeping User Voice "
            "as system of record. Reports feature has a breaking bug when adding a second object."
        ),
    },
    {
        "id": 37,
        "source_transcript_id": 58,
        "context": (
            "**Token budget crisis** hit on 23 Feb when Azmain burned **$750 in three Cursor days** "
            "(75% of monthly allowance). Claude Max subscription expired the same day, cutting off "
            "mid-build. The team scrambled to **Windsurf via Moody's SSO** as a free alternative.\n\n"
            "Root cause: no enterprise AI tooling budget. Azmain and Richard are paying **£200/month "
            "combined from personal funds** for Claude Code subscriptions. Azmain described this as "
            "\"insanely stupid\" — the company should provide $200/month Claude subscriptions instead "
            "of $1,000/month Cursor licences.\n\n"
            "**BenVH's Phantom Agent** was identified as the structural fix: dynamically provision "
            "isolated environments with cost controls per user/OU. Value proposition: one $5K dev "
            "laptop's cost can run Phantom Agent for 1,000 people for a month. Meanwhile, getting "
            "the **AWS Bedrock API key** working was the immediate tactical priority."
        ),
    },
    {
        "id": 39,
        "source_transcript_id": 61,
        "context": (
            "**Sales Recon UAT failed** — missing parent-child hierarchy, wrong date queries, and "
            "outdated SSO SAML configuration. The team decided to **build an interim Salesforce/"
            "Mixpanel data pipeline** rather than wait for Sales Recon fixes.\n\n"
            "This was discussed in the AI Infrastructure meeting on 26 Feb alongside broader tech "
            "debt concerns. **Rahul** proposed a structured prioritisation framework (value + risk "
            "mitigation + capacity). The immediate need: programmatic access to Salesforce data for "
            "CLARA's blocker intelligence.\n\n"
            "**Stacy Dixstra** confirmed that monthly Excel exports from CLARA are sufficient for the "
            "migration dashboard in the interim — no APIs or automated feeds required yet. The "
            "scorecard target of 34 migrations is built on **fabricated dates** (CSMs made up "
            "switch-off dates in December), adding urgency to getting real data flowing."
        ),
    },
    {
        "id": 40,
        "source_transcript_id": 59,
        "context": (
            "**App Factory** has **4-5 apps queued** for BenVH's deployment (Idris, Rhett, Stacy, "
            "Eddie) with **zero governance** — every request gets built, no product management "
            "discipline to filter.\n\n"
            "Richard wasted an entire weekend rewriting Steve Gentilli's code, only to discover Steve "
            "was simultaneously updating the same app with Rhett — a coordination failure that "
            "highlights the lack of intake process.\n\n"
            "**Azmain** designed deliberate friction into the GSD (Build in Five) intake as a "
            "governance mechanism disguised as UX: if the problem is trivial, structured questions "
            "discourage wasted build resources. But this only covers new builds — existing App Factory "
            "requests bypass it entirely.\n\n"
            "BenVH is the **sole deployment bottleneck** — he manually deploys every app. Without "
            "gating criteria, his queue grows indefinitely. The Phantom Agent automation is the "
            "structural fix but isn't ready yet."
        ),
    },

    # ═══ WEEK 2 ═══
    {
        "id": 50,
        "source_transcript_id": 78,
        "context": (
            "**BenVH's absence was NOT illness** — he was worn down by Nikhil taking credit for "
            "App Factory work. This explicitly parallels his **traumatic Microsoft experience**: a "
            "manager took his ideas, put their name on them, and destroyed his career.\n\n"
            "Specific grievances: Nikhil sending BenVH's architecture diagrams as his own, renaming "
            "App Factory to **\"Moplit\"**, speaking in advisory all-hands about App Factory without "
            "crediting BenVH, and trying to overwrite Cat Accelerate processes.\n\n"
            "BenVH is emotionally fragile and considering apartment relocation (financial stress). "
            "**All three key technical people** were simultaneously considering exit: Richard briefly "
            "explored other positions (resolved mid-March), Azmain was looking at internal Moody's "
            "jobs, and BenVH was at breaking point.\n\n"
            "**Response plan**: Azmain committed to name-dropping App Factory and Phantom Agent in "
            "group chats to establish credit. Both planning separate conversations with Richard about "
            "addressing Nikhil. Strategy: redirect Nikhil to client-facing IRP work."
        ),
    },
    {
        "id": 51,
        "source_transcript_id": 79,
        "context": (
            "**Security audit caught the team using personal Claude accounts** for Moody's work. "
            "Azmain admitted to Chris: \"The security team caught it... we were just like, there's "
            "no proprietary information, which is wildly a lie, but whatever. Ben is providing "
            "cover for us.\"\n\n"
            "The exposure is significant: Azmain ran **30 concurrent agents** in Cursor on "
            "Anthropic's cloud infrastructure with full internet access — no enterprise controls, "
            "data processing outside Moody's infrastructure. Personal spend: Azmain burned his "
            "entire **$1,000 monthly Cursor budget in ONE DAY** building Friday.\n\n"
            "**Ben Brooks is providing political cover** but the risk persists if re-examined "
            "formally. The **AWS Bedrock API** (working since Nikhil's contribution on 3 Mar) "
            "should resolve the issue going forward by keeping data within Moody's infrastructure, "
            "but the historical exposure remains unaddressed."
        ),
    },
    {
        "id": 52,
        "source_transcript_id": 80,
        "context": (
            "**Catherine** volunteered to design an **App Factory decision tree/intake process** "
            "during the Pre-Gainsight team meeting on 6 Mar. When the governance need was "
            "described, she responded: **\"you're speaking my love language.\"**\n\n"
            "Her proposed role: serve as a gating checkpoint — should an idea be built as a custom "
            "app, or does it already exist in Gainsight? This prevents silo creation. Examples: "
            "**George** building an account planning app and **Idris** (Banking) building something "
            "similar, both independently with no coordination.\n\n"
            "Catherine sits between business and enterprise tooling, making her ideal for intake "
            "triage. She identified herself as a willing governance ally, NOT a blocker. However, "
            "Richard flagged that Gainsight integration is **NOT in the original 12-week plan** — "
            "replanning required if integration is expected."
        ),
    },
    {
        "id": 53,
        "source_transcript_id": 71,
        "context": (
            "**Rhett created an Excel-based adoption charter** without consulting CSMs, directly "
            "contradicting the agreed Word-to-app approach. The adoption charters turned out to be "
            "far more complex than expected — actual documents have **embedded images, diagrams, and "
            "multi-page formatting** requiring OCR and multi-modal LLM processing.\n\n"
            "Richard spent a **full day reverse-engineering** Rhett's incomplete spec (5 Mar Clara "
            "standup). His explicit advice: **do NOT escalate to Ben Brooks** — Rhett has Ben's "
            "political protection.\n\n"
            "Azmain set the priority sequence: bugs first → Bedrock blocker intelligence second → "
            "adoption charters third. The one-directional data flow decision (CLARA → document, not "
            "bi-directional) was made to limit scope. Meanwhile, Rhett was observed talking about "
            "App Factory in advisory meetings **without understanding it**, compounding BenVH's "
            "credit-taking frustration."
        ),
    },
    {
        "id": 54,
        "source_transcript_id": 74,
        "context": (
            "**Friday** is Azmain's programme management tool, named after the 1940 film "
            "\"His Girl Friday.\" Features include Kanban boards, list views, timeline views, "
            "milestones, budgeting, decision tracking, stakeholder heatmaps, and time tracking.\n\n"
            "**Diana explicitly endorsed Friday** in her 4 Mar 1-1: \"today is the last Wednesday "
            "review meeting\" — Friday replaces the slide-based Wednesday advisory project review. "
            "IRP projects sync bidirectionally with CLARA; non-IRP advisory projects (internal, ILS, "
            "cat bonds) live only in Friday.\n\n"
            "**BenVH agreed to deploy** the Friday repo to dev environment without authentication "
            "for a four-week pilot (confirmed 6 Mar). Azmain needs the link to share with project "
            "managers. **Prashant** was allocated by Diana to help with Friday development. Azmain "
            "explicitly did NOT want Vlad (\"launches into tangents about Natalia being awful\")."
        ),
    },

    # ═══ WEEK 3 ═══
    {
        "id": 65,
        "source_transcript_id": 108,
        "context": (
            "The **BenVH/Nikhil conflict** escalated to CRITICAL in week 3. In the 11 Mar App "
            "Factory standup, daily boundary violations were documented:\n\n"
            "- Nikhil attempting to deploy without permission\n"
            "- Introducing App Factory tasks to CAT team without authorisation\n"
            "- Going directly to Richard about centralised logging after BenVH explicitly said "
            "it was out of scope\n"
            "- Scheduling deployment meetings 30 minutes after being told no\n\n"
            "BenVH explicitly stated he'd **\"prefer to work overtime rather than have Nikhil "
            "interact with any App Factory app.\"** Richard is planning a direct confrontation "
            "with Nikhil about boundary violations and intends to escalate to Ben Brooks.\n\n"
            "**Neutralisation strategy:** redirect Nikhil to Salesforce integration or AIG "
            "project, away from App Factory."
        ),
    },
    {
        "id": 66,
        "source_transcript_id": 118,
        "context": (
            "**Catherine's Centre of Excellence (COE)** has three pillars: digital engagement, "
            "enablement, and Gainsight/SFDC retirement. The **first pillar (digital engagement) "
            "directly overlaps** with the AI programme's scope.\n\n"
            "Key incidents (from 12 Mar Diana 1-1 and Post-Gainsight debrief):\n"
            "- Catherine organised the Gainsight team meeting **without consulting the CLARA team**, "
            "blindsiding them\n"
            "- She finds trivial CLARA issues every two days, claims CSMs complained (they haven't)\n"
            "- She gatekeeps Gainsight/Salesforce access\n"
            "- Her objectives were **approved by Natalia Orzechowska and signed off by Diya**\n\n"
            "**Strategy**: Frame \"digital enablement\" (Catherine's domain) as distinct from \"AI "
            "enablement\" (Azmain's domain). Diana to discuss with Natalia O. Richard to raise with "
            "Diya during London visit. Risk R#045."
        ),
    },
    {
        "id": 67,
        "source_transcript_id": 87,
        "context": (
            "**AWS Bedrock costs** reached **$1,163 with zero attribution** — nobody knows which apps "
            "or teams are consuming the tokens. Richard raised this on 10 Mar.\n\n"
            "Multiple apps (CLARA, App Factory, Build in Five, Slidey) all use Claude via AWS Bedrock, "
            "but there are **no cost attribution tags** configured. Without tagging, the programme "
            "cannot demonstrate ROI per project or justify continued spend to Diya.\n\n"
            "Azmain's personal token consumption was highlighted when he \"ran through his monthly "
            "allowance in two days\" building the 30-agent swarm for CLARA's reporting system. "
            "Cost attribution is a prerequisite for scaling Bedrock usage across the programme."
        ),
    },
    {
        "id": 68,
        "source_transcript_id": 113,
        "context": (
            "**Cross-OU showcase** planned for Wednesday, deliberately timed because **ISLTR "
            "(Insurance Senior Leadership Team) is in London** — maximum visibility for "
            "cross-divisional AI traction.\n\n"
            "Agenda items (discussed with Idrees on 11 Mar):\n"
            "- CS team AI initiative updates across Operating Units\n"
            "- Idrees's **segment-agnostic retention dashboard** (looped in DIA and George Dyke)\n"
            "- **ROB AI app** for senior leadership visibility\n"
            "- App Factory infrastructure demo\n\n"
            "Idrees's strategic framing: showing cross-OU consistency helps DIA pressure Charlotte "
            "to move things forward. **AON intelligence:** Rob Fulber meeting Dan Dick (Global Head "
            "of Cat Risk at AON) next week in London — potential showcase opportunity."
        ),
    },
    {
        "id": 69,
        "source_transcript_id": 111,
        "context": (
            "**Slidey convergence** was discovered on 11 Mar: **Juliet Valencia** (Sales) "
            "independently built a Moody's-branded PowerPoint generator — the same tool Richard's "
            "team is building as **Slidey** (Ben Brooks's presentation app).\n\n"
            "Juliet's bot connects to Databricks but can't write to SharePoint in the Azure sandbox. "
            "She opted for her **own AWS infrastructure** rather than shared App Factory (data "
            "governance: commission targets are confidential).\n\n"
            "**Azmain's insight:** \"Of all the complicated, fancy stuff we do, this will be the one "
            "that reaches the most people.\" Richard to schedule a cross-team Slidey meeting on "
            "Tuesday. Juliet to share her GitHub repo. App-to-app communication (CLARA → Slidey: "
            "write MD file, auto-generate PowerPoint) is a key integration use case."
        ),
    },
    {
        "id": 70,
        "source_transcript_id": 112,
        "context": (
            "**App Factory governance** discussed at the 11 Mar App Factory Discussion meeting. The "
            "core architecture decision: **MCP server is the central middleware** — all apps (CLARA, "
            "Slidey, Build in Five) connect to a central App Factory MCP server instead of building "
            "per-app LLM pipelines.\n\n"
            "**Wednesday 12 Mar** was set as the public launch meeting with senior stakeholders "
            "(Ben Brooks, George, CS contacts). Catherine's intake design from week 2 feeds into "
            "this governance board.\n\n"
            "Key decisions: no more per-app LLM pipelines, SharePoint knowledge cataloguing "
            "initiative (profile 10 years of consulting documents, vector DB, MCP on top for RAG). "
            "**BenVH** to complete App Factory MCP server for Martin integration by 15 Mar. "
            "Cross-OU adoption model being developed — insurance team sharing infrastructure "
            "with Banking and Life Insurance."
        ),
    },
]

print("=== PART 1: Patching context on weeks 1-3 incomplete actions ===\n")
for p in patches:
    aid = p.pop("id")
    resp = requests.patch(f"{BASE}/weekly-plans/actions/{aid}", json=p)
    if resp.status_code == 200:
        data = resp.json()
        title = data.get("source_transcript_title") or "?"
        ctx_len = len(data.get("context") or "")
        print(f"OK  id={aid} src=\"{title}\" ctx={ctx_len}ch")
    else:
        print(f"ERR id={aid} status={resp.status_code} {resp.text[:120]}")

# ── PART 2: Carry unresolved actions into week 4 ──

# Identify which incomplete week 1-3 actions are NOT already in week 4:
# - id=40 (App Factory gating, wk1) → id=52 (wk2) → id=70 (wk3): NOT in week 4
# - id=51 (security audit, wk2): NOT in week 4
# - id=54 (Friday deployment, wk2): NOT in week 4
# All others are either resolved or already carried into week 4.

new_actions = [
    {
        "category": "programme_strategic",
        "title": "Establish App Factory governance framework with intake criteria",
        "description": (
            "Define gating criteria for App Factory intake and formalise Catherine's "
            "decision tree design. Merge the intake process, MCP architecture governance, "
            "and cross-OU adoption model into a single framework. Unblocks BenVH's queue."
        ),
        "priority": "HIGH",
        "owner": "Richard / Catherine",
        "status": "PENDING",
        "position": 14,
        "is_ai_generated": True,
        "carried_from_week": 1,
        "source_transcript_id": 112,
        "context": (
            "This action has been carried forward through **three consecutive weeks** without "
            "resolution — first raised in Week 1 as \"Establish App Factory gating criteria\" "
            "(id=40), then Week 2 as \"Establish App Factory governance with Catherine intake "
            "design\" (id=52), and Week 3 as \"App Factory governance board with Catherine "
            "intake design\" (id=70).\n\n"
            "**Catherine** volunteered to design the decision tree on 6 Mar (\"you're speaking my "
            "love language\"). The 11 Mar App Factory Discussion established MCP server as central "
            "middleware. A Wednesday 12 Mar public launch meeting was planned with senior "
            "stakeholders.\n\n"
            "BenVH has **4-5 apps queued** with zero governance. Duplicate apps being built "
            "independently (George's account planning, Idris's similar tool). Without formal "
            "intake criteria, every request gets built and BenVH's queue grows indefinitely."
        ),
    },
    {
        "category": "programme_tactical",
        "title": "Close security audit exposure on personal LLM account usage",
        "description": (
            "Migrate all team members off personal Claude/Cursor accounts to AWS Bedrock. "
            "Document the transition for security team. Ensure no proprietary data is processed "
            "outside Moody's infrastructure going forward."
        ),
        "priority": "HIGH",
        "owner": "Azmain / BenVH",
        "status": "PENDING",
        "position": 15,
        "is_ai_generated": True,
        "carried_from_week": 2,
        "source_transcript_id": 79,
        "context": (
            "**Security audit caught the team using personal Claude accounts** for Moody's work "
            "in early March. Azmain admitted: \"The security team caught it... we were just like, "
            "there's no proprietary information, which is wildly a lie.\" **Ben Brooks is providing "
            "political cover** but the risk persists.\n\n"
            "The exposure: Azmain ran **30 concurrent agents** on Anthropic's cloud with full "
            "internet access — no enterprise controls, data outside Moody's infrastructure. "
            "Personal spend: £200/month combined (Azmain + Richard) from personal funds.\n\n"
            "**AWS Bedrock API** is now working (Nikhil's contribution, 3 Mar) which should "
            "resolve the issue going forward. But the team needs to formally transition all "
            "usage and close out the historical exposure. Related to AWS cost attribution "
            "(action id=81) but distinct: this is about **security compliance**, not cost tracking."
        ),
    },
    {
        "category": "deliverable_tactical",
        "title": "Deploy Friday PM to dev environment for pilot",
        "description": (
            "BenVH agreed to deploy Friday repo to dev without auth for 4-week pilot. "
            "Get the link, share with project managers, begin Diana's team pilot."
        ),
        "priority": "MEDIUM",
        "owner": "BenVH / Azmain",
        "status": "PENDING",
        "position": 16,
        "is_ai_generated": True,
        "carried_from_week": 2,
        "source_transcript_id": 74,
        "context": (
            "**Friday** is Azmain's programme management tool (named after the 1940 film "
            "\"His Girl Friday\"). Features: Kanban boards, list/timeline views, milestones, "
            "budgeting, decision tracking, stakeholder heatmaps, time tracking.\n\n"
            "**Diana endorsed Friday** on 4 Mar: \"today is the last Wednesday review meeting\" — "
            "Friday replaces the slide-based Wednesday advisory project review. IRP projects sync "
            "bidirectionally with CLARA; non-IRP advisory projects live only in Friday.\n\n"
            "**BenVH agreed to deploy** to dev environment without auth for a four-week pilot "
            "(confirmed 6 Mar). Azmain needs the link to share with project managers. **Prashant** "
            "allocated by Diana to help with development. This has been IN_PROGRESS since Week 2 "
            "— blocked on BenVH's bandwidth (he's also managing App Factory MCP server, Slidey "
            "deployment, and the Nikhil conflict)."
        ),
    },
]

print("\n=== PART 2: Carrying unresolved actions into week 4 (plan_id=6) ===\n")
for action in new_actions:
    resp = requests.post(f"{BASE}/weekly-plans/6/actions", json=action)
    if resp.status_code == 201:
        data = resp.json()
        print(f"OK  new_id={data['id']} carried_from_wk={data.get('carried_from_week')} | {data['title'][:70]}")
    else:
        print(f"ERR status={resp.status_code} {resp.text[:120]}")

print("\n=== DONE ===")
