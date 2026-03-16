"""One-time script to backfill source_transcript_id and context for Week 4 plan actions."""

import requests

BASE = "http://localhost:8000/api/weekly-plans/actions"

actions = [
    {
        "id": 71,
        "source_transcript_id": 110,
        "context": (
            "**Navigator MCP server** is the integration layer that connects Martin's drag-drop "
            "dashboard builder to live API data. Currently the dashboard uses a JavaScript agent "
            "stub \u2014 replacing it with the Navigator MCP server means dashboards can pull real "
            "portfolio data dynamically.\n\n"
            "This is critical because **AIG has signed a strategic deal with Anthropic and Palantir** "
            "and is using MCP servers to drive their entire underwriting agenda (revealed by Richard "
            "in the 11 Mar standup). Martin's Build in Five needs to demonstrate the same MCP-driven "
            "workflow transformation.\n\n"
            "**Nicole** (Navigator team) controls repo access. Without it, Martin cannot wire up the "
            "server. BenVH expects the App Factory MCP server complete by end of week, making Martin "
            "the first integration POC."
        ),
    },
    {
        "id": 72,
        "source_transcript_id": 121,
        "context": (
            "**Adoption charter** (Deliverable D2) is a structured template for onboarding customers "
            "onto IRP products. Currently at 0% progress with a target of week 5.\n\n"
            "The Banking Credit team's **\"Agent Day\" framework** (presented by Wasim and Nils on "
            "13 Mar) provides a model: they use a **four-tier adoption approach** \u2014 (1) Copilot "
            "Light, (2) Copilot Studio, (3) Cursor coding agents with MCPs, (4) Custom-built agents. "
            "Their key insight: **pre-work is everything** \u2014 surveys weeks before to identify use "
            "cases, all technical setup completed before the event.\n\n"
            "Challenge: Rhett's uncoordinated Excel approach to adoption tracking needs resolution. "
            "Multi-page documents with embedded images require OCR and multi-modal LLM processing, "
            "which the current pipeline doesn't support."
        ),
    },
    {
        "id": 73,
        "source_transcript_id": 109,
        "context": (
            "**Salesforce-IRP data mapping** (Milestone M18) defines which Salesforce objects and "
            "fields map to CLARA's data model. The architecture decided on 11 Mar is **one-way only** "
            "(read from Salesforce, no write-back) using the **App Factory MCP server as middleware**.\n\n"
            "Four user groups drive the requirements:\n"
            "1. **Bernard** \u2014 customer sentiment analysis from real-time tickets\n"
            "2. **Courtney Spillers** \u2014 HD adoption blockers from support cases (2,000-3,000 cases)\n"
            "3. **Kevin Pern** \u2014 ticket info + possibly User Voice data\n"
            "4. **Azmain/CLARA** \u2014 blocker intelligence synced from Salesforce\n\n"
            "**Phase 1** focuses on Cases and Case Feed objects only. Kathryn Palkovics confirmed Gainsight "
            "goes live March 30 \u2014 CLARA and Gainsight are complementary (IRP-specific vs. overall "
            "CSM BAU)."
        ),
    },
    {
        "id": 74,
        "source_transcript_id": 118,
        "context": (
            "**Kathryn Palkovics' Centre of Excellence (COE)** has three pillars: digital engagement, "
            "enablement, and Gainsight/SFDC retirement. The **first pillar (digital engagement) "
            "directly overlaps** with the AI programme's scope.\n\n"
            "Key incidents (from 12 Mar Diana 1-1 and Post-Gainsight debrief):\n"
            "- Kathryn Palkovics organised the Gainsight team meeting **without consulting the CLARA team**, "
            "blindsiding them\n"
            "- She finds trivial CLARA issues every two days, claims CSMs complained (they haven't)\n"
            "- She gatekeeps Gainsight/Salesforce access\n"
            "- Her objectives were **approved by Natalia Orzechowska and signed off by Diya**\n\n"
            "**Strategy**: Frame \"digital enablement\" (Kathryn Palkovics' domain) as distinct from \"AI "
            "enablement\" (Azmain's domain). Diana to discuss with Natalia O. Richard to raise with "
            "Diya during London visit. Risk R#045."
        ),
    },
    {
        "id": 75,
        "source_transcript_id": 110,
        "context": (
            "**Nicole** is on the Navigator team and controls access to the Navigator repository. "
            "Martin cannot proceed with MCP server wiring without this access \u2014 it's the single "
            "biggest blocker for the Build in Five demo.\n\n"
            "Richard committed to chasing Nicole in the 11 Mar standup. The Navigator MCP server "
            "would replace the current JavaScript agent stub with live API definitions, enabling "
            "Martin's dashboard builder to query real portfolio data. This is the critical path item "
            "for demonstrating workflow transformation at the exceedance demo."
        ),
    },
    {
        "id": 76,
        "source_transcript_id": 89,
        "context": (
            "**Exceedance** is the upcoming demo event where Build in Five will be showcased. Ben "
            "Brooks saw Martin's dashboard builder for the first time on 10 Mar and was positive but "
            "strategically focused.\n\n"
            "Ben's key framing question: **\"Is this a Moody's product experience for customers to "
            "use inside the platform, or a self-service demonstration tool?\"** \u2014 this fundamental "
            "product positioning must be resolved before the demo.\n\n"
            "Ben wants to show a **common, irritating market workflow being solved in 5 minutes** "
            "\u2014 not just a cool dashboard, but a time transformation story. The demo format discussed: "
            "innovation track intro, customer challenges panel, then pivot to live/semi-live Build in "
            "Five demo. **Risk data lake** capabilities and portfolio context are potential additions."
        ),
    },
    {
        "id": 77,
        "source_transcript_id": 121,
        "context": (
            "**Agent Days** are full-day in-person AI adoption events run by the Banking Credit team "
            "(Wasim and Nils). Their framework is directly relevant to the Training & Enablement "
            "deliverables (D4/D5).\n\n"
            "**Four-tier agent model:**\n"
            "1. **Copilot Light** \u2014 basic chat interface\n"
            "2. **Copilot Studio** \u2014 low-code workflow builder\n"
            "3. **Cursor coding agents with MCPs** \u2014 developer tools (target for most participants)\n"
            "4. **Custom-built agents** \u2014 full autonomy\n\n"
            "**Critical success factors:**\n"
            "- **Pre-work** (surveys weeks before to identify use cases and experience levels)\n"
            "- **\"Transit teachers\"** \u2014 4+ trained multipliers pre-briefed on each participant's project\n"
            "- All technical setup completed before the day\n"
            "- Every participant builds their own agent (not group work) \u2014 everyone succeeded, "
            "including non-coders\n"
            "- Shared GitHub repo of curated rules/skills with governance"
        ),
    },
    {
        "id": 78,
        "source_transcript_id": 119,
        "context": (
            "**Azmain announced on 13 Mar** that all ~4,000-5,000 people under Andy Frappe have been "
            "imported as CLARA viewers with SSO access. Anyone can log in to see everything; only "
            "certain people have edit access.\n\n"
            "This was revealed at the CLARA demo to Cihan's entire Product & Technology team (~40-50 "
            "attendees). Cihan (MD Product & Technology) personally endorsed CLARA as a daily tool.\n\n"
            "The risk (R#049, LOW): this massive viewer expansion happened **without a support plan**. "
            "No onboarding documentation, no FAQ, no feedback channel established yet. Azmain committed "
            "to setting up a feedback submission process, but the scale of potential questions from "
            "5,000 new viewers could overwhelm the team \u2014 especially with only two grads arriving "
            "April 7."
        ),
    },
    {
        "id": 79,
        "source_transcript_id": 108,
        "context": (
            "**BenVH/Nikhil conflict** has been escalating since Week 2 (Risk R#039, CRITICAL). In "
            "the 11 Mar App Factory standup, daily boundary violations were documented:\n\n"
            "- Nikhil attempting to deploy without permission\n"
            "- Introducing App Factory tasks to CAT team without authorisation\n"
            "- Going directly to Richard about centralised logging after BenVH explicitly said it was "
            "out of scope\n"
            "- Scheduling deployment meetings 30 minutes after being told no\n\n"
            "BenVH explicitly stated he'd **\"prefer to work overtime rather than have Nikhil interact "
            "with any App Factory app.\"** Richard is planning a direct confrontation with Nikhil about "
            "boundary violations and intends to escalate to Ben Brookes.\n\n"
            "**Neutralisation strategy:** redirect Nikhil to Salesforce integration or AIG project, "
            "away from App Factory."
        ),
    },
    {
        "id": 80,
        "source_transcript_id": 113,
        "context": (
            "**Cross-OU showcase** planned for Wednesday, deliberately timed because **ISLTR (Insurance "
            "Senior Leadership Team) is in London** \u2014 maximum visibility for cross-divisional AI "
            "traction.\n\n"
            "Agenda items (discussed with Idrees on 11 Mar):\n"
            "- CS team AI initiative updates across Operating Units\n"
            "- Idrees's **segment-agnostic retention dashboard** (looped in DIA and George Dyke)\n"
            "- **ROB AI app** for senior leadership visibility\n"
            "- App Factory infrastructure demo\n\n"
            "Idrees's strategic framing: showing cross-OU consistency helps DIA pressure Charlotte to "
            "move things forward. **AON intelligence:** Rob Fulber meeting Dan Dick (Global Head of "
            "Cat Risk at AON) next week in London \u2014 potential showcase opportunity."
        ),
    },
    {
        "id": 81,
        "source_transcript_id": 87,
        "context": (
            "**AWS Bedrock costs** reached $1,163 with zero attribution \u2014 nobody knows which apps "
            "or teams are consuming the tokens. Richard raised this on 10 Mar.\n\n"
            "Multiple apps (CLARA, App Factory, Build in Five, Slidey) all use Claude via AWS Bedrock, "
            "but there are no cost attribution tags configured. Without tagging, the programme cannot "
            "demonstrate ROI per project or justify continued spend to Diya.\n\n"
            "Azmain's personal token consumption was highlighted when he \"ran through his monthly "
            "allowance in two days\" building the 30-agent swarm for CLARA's reporting system."
        ),
    },
    {
        "id": 82,
        "source_transcript_id": 89,
        "context": (
            "**Slidey** is Ben Brookes's presentation app \u2014 he built it as a personal tool and it "
            "gained traction internally. The Life Insurance team reacted strongly to it. Ben mentioned "
            "he \"nearly didn't make it a Moody's app.\"\n\n"
            "Slidey is now positioned as part of the App Factory platform alongside Martin's dashboard "
            "builder and CLARA. This meeting aims to coordinate across teams building similar tools to "
            "avoid duplication and ensure consistent App Factory architecture (MCP server middleware "
            "pattern).\n\n"
            "BenVH completed Azure app registration for Slidey authentication on 11 Mar."
        ),
    },
    {
        "id": 83,
        "source_transcript_id": 116,
        "context": (
            "**CLARA is transitioning from Build Mode to Maintenance Mode.** Natalia Plant called a "
            "meeting on 12 Mar to establish governance \u2014 she felt \"lost\" by the volume of recent "
            "changes.\n\n"
            "New process established:\n"
            "- **Fortnightly release cycle** with Tuesday review meetings for prioritisation\n"
            "- Release schedule: skip next week, **release 27 March**, then grads take over\n"
            "- **Two grads arriving April 7** (one London, one New York) \u2014 100% dedicated to CLARA "
            "maintenance\n"
            "- Chris maintaining feedback Excel: plan \u2192 build \u2192 test \u2192 push\n\n"
            "Key items for 27 March release:\n"
            "- **Analytics tab removal** from management dashboard (confusing for Diya)\n"
            "- Management dashboard and Portfolio Review moved higher in sidebar\n"
            "- Validation check: CSMs cannot mark use case \"complete\" if software status fields open\n"
            "- Navigation UX fix: back button scroll position loss"
        ),
    },
    {
        "id": 84,
        "source_transcript_id": 108,
        "context": (
            "**Juliet Valencia** needs AWS infrastructure provisioned for her work. This was flagged "
            "in the 11 Mar App Factory standup as a tactical item.\n\n"
            "The App Factory is expanding beyond the core team (BenVH, Martin, Nikhil) to include new "
            "contributors. AWS Bedrock access, IAM roles, and development environment setup are "
            "prerequisites. BenVH is pivoting the entire App Factory to an **MCP server architecture** "
            "\u2014 any new infrastructure should be configured to work within this middleware pattern "
            "rather than the old standalone app model.\n\n"
            "Related: AWS costs are unattributed ($1,163 total) \u2014 new infrastructure should include "
            "cost attribution tags from the start."
        ),
    },
]

for a in actions:
    aid = a.pop("id")
    resp = requests.patch(f"{BASE}/{aid}", json=a)
    if resp.status_code == 200:
        data = resp.json()
        title = data.get("source_transcript_title") or "?"
        ctx_len = len(data.get("context") or "")
        print(f"OK  id={aid} src=\"{title}\" ctx={ctx_len}ch")
    else:
        print(f"ERR id={aid} status={resp.status_code} {resp.text[:100]}")
