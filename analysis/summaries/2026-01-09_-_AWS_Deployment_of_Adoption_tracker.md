# AWS Deployment of Adoption Tracker
**Date:** 2026-01-09
**Attendees:** Richard Dosoo, Azmain Hossain
**Duration context:** Long (~42 minutes)
**Workstreams touched:** WS2 (CLARA / IRP Adoption Tracker), WS1 (Training & Enablement — discussed), WS6 (Build in Five — mentioned in broader programme context)

## Key Points
- Richard hit Cursor premium limits the previous evening — agent workflows blocked by a Pro entitlement gate, not a budget issue. Tried switching models (GPT, longer versions) but each ran out after one or two uses.
- Before Cursor died, Richard identified that the RAG status dashboard wasn't working because customer_use_cases had null status values and zero RAG values. He ran an analysis across the full schema to find similar nullable fields causing dashboard failures, and generated Python scripts to fix them.
- Richard created an Excel spreadsheet with the data model populated and shares it with Azmain along with Markdown files documenting the fix plan. The portable Excel is the mechanism for moving data between AWS/Azure.
- Richard is using a **personal Claude account** (GBP 18/month) because corporate access isn't available yet. Azmain considers using personal Gemini Pro. Both acknowledge this is unsanctioned.
- Azmain's blockers page is broken locally. Richard can't redeploy because he's out of Cursor tokens.
- Significant discussion about the broader programme, Sales Recon meeting on 26 Jan, and stakeholder mapping. Richard reveals that **Diya warned him**: previous meetings with Sales Recon produced nothing because there were no committed outcomes. She insists this meeting must be outcome-focused with commitments.
- Richard is frustrated by **resource politics** — when asking for Martin, Ben, or others to support the programme, he expects pushback from Liz, Stacy, and others who are "defensive about their resources." He's considering requesting external developers instead of fighting internal resource battles.
- Richard and Azmain discuss AI as a productivity multiplier at length. Richard mentions a new hire (Nikhil) who demonstrated excellent AI-augmented engineering in his interview, versus existing team members who feel threatened by AI.
- Azmain has been creating programme charters, strategic documents, and governance structures using AI tools — all ready for Richard's review.
- Practical next step: BenVH is deploying to AWS today. Azmain's task is to fill the Excel with synthetic/dummy data so it's ready when the deployment completes.

## Decisions Made
- Azmain to fill Excel spreadsheet with dummy data as per the data model while BenVH deploys → Azmain (today)
- Monday morning (12 Jan) catch-up scheduled for broader programme planning before the Jamie/Sales Recon agenda review at 2pm → Richard/Azmain
- Richard to create OneDrive folder for programme documents → Richard
- Azmain added to Sales Recon meeting invite and Jamie's thread → Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Fill Excel spreadsheet with synthetic data per data model | Azmain | Today (9 Jan) | Open |
| BenVH to deploy app to AWS | BenVH | Today (9 Jan) | Open |
| Once deployed, upload synthetic data to Postgres database | BenVH/Azmain | Today/Tomorrow | Open |
| Set up Monday 11am catch-up on programme planning | Richard | 12 Jan | Open |
| Send programme charter and governance docs to Richard | Azmain | Weekend/Monday | Open |
| Create OneDrive folder for programme documents | Azmain | Today | Open |
| Prepare straw man presentation for Jan 26 Sales Recon meeting | Richard/Azmain | Next week | Open |

## Stakeholder Signals
- **Richard** is increasingly frustrated with internal collaboration culture. Describes colleagues as "defensive about resources" and "not interested in helping even when it helps them." He's ready to go external for dev resources rather than fight internal politics.
- **Azmain** is confident and productive — has already generated programme charters and strategic documents autonomously using AI. His self-assessment is honest: "My job is so useless, like an AI could do it. But the thing that I keep telling everyone is AI is not going to take your job. Somebody who uses AI better than you is going to take your job."
- **Diya** (referenced) is sceptical about the Sales Recon meeting based on past experience. She explicitly told Richard it must be outcome-focused or it will be another wasted session.

## Open Questions Raised
- Will BenVH's AWS deployment complete today? Richard estimates "a couple hours" but it's uncertain.
- How will Cursor budget/licence issues be resolved? Divya's finance call moved to Monday.
- Who exactly are the "CS leads" for the Jan 26 presentation? Needs stakeholder map — Catherine, Kevin, Alexandra (Life), Idris (banking) mentioned.
- Will internal resources (Martin, Ben's team) be allocated, or will the programme need external contractors?

## Raw Quotes of Note
- "AI is not going to take your job. Somebody who uses AI better than you is going to take your job." — Azmain Hossain, on why he embraces AI tooling
