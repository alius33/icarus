# Sales team apps in App Factory
**Date:** 2026-03-11
**Attendees:** Richard Dosoo, Juliet (Valencia), Azmain Hossain
**Duration context:** Short (~18 minutes)
**Primary project:** App Factory
**Secondary projects:** Cross OU Collaboration

## Key Points
- Juliet is struggling with Azure/Power Automate/Copilot Studio infrastructure — the exact same wall the insurance team hit months ago. Her bot connects to Databricks but cannot write to SharePoint because Copilot is in a sandbox environment while Power Automate connects to the Moody's default environment
- John Cushing is getting Juliet a Power Automate Premium licence to try to bridge the gap
- Richard offered two solutions: (1) App Factory can host her application on AWS, (2) they can show her how to set up her own AWS infrastructure. Juliet chose option 2 — she has confidential data (commission targets) and wants her own environment
- Richard will set up an AWS infrastructure walkthrough next week — BenVH is packaging up App Factory deployment as a reusable process for other teams
- Juliet needs to raise two tickets: one for Azure (Entra/authentication) and one for AWS (application hosting)
- Major convergence on Slidey (PowerPoint generation): Juliet independently built a Moody's branded PowerPoint generator using Python. Richard's team has built a similar conversational agent. Azmain noted this will likely be the most widely adopted tool across the company
- Richard plans a cross-team Slidey meeting for next week (Tuesday) to combine efforts. His manager (also working on Slidey) wants it to be a collaborative idea/brief tool, not just a generator
- Juliet will share her GitHub repo. Richard will build a local Docker version and compare approaches
- Mick Louder (corporate TSG) identified as the go-to for infrastructure questions — has the organisational tentacles to point people in the right direction
- After Juliet left, Richard and Azmain had a brief sidebar (audio cut off at end)

## Decisions Made
- Juliet to set up her own AWS infrastructure rather than use shared App Factory hosting → Juliet/Richard
- BenVH to package App Factory deployment process for other teams → BenVH
- Cross-team Slidey collaboration meeting to be scheduled next week (Tuesday) → Richard
- Juliet to use Cursor + AWS approach rather than continuing with Power Automate/Copilot Studio → Richard's recommendation

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Raise AWS account Snow ticket | Juliet | This week | Open |
| Raise Azure tenant ticket for Entra/auth | Juliet | This week | Open |
| Set up AWS infrastructure walkthrough for Juliet | Richard / BenVH | Next week | Open |
| Share PowerPoint generator GitHub repo | Juliet → Richard | This week | Open |
| Schedule cross-team Slidey meeting | Richard | Next Tuesday | Open |
| Connect Juliet with Mick Louder for corporate infra access | Richard | This week | Open |
| Send Juliet the ticket templates for AWS/Azure setup | Richard | Today | Open |

## Stakeholder Signals
- **Juliet Valencia** — Pragmatic and self-reliant. Hitting the same infrastructure walls as everyone else. Data governance instincts are good (chose own infrastructure over shared hosting due to confidential data). Already a Cursor user. Her PowerPoint generator shows independent innovation happening across the org
- **Azmain** — Immediately spotted the strategic value of Slidey as the tool that reaches the most people. Perceptive about product-market fit within the organisation
- **Richard** — Continues to position App Factory as a service for the wider organisation, not just the insurance CS team. His manager's interest in Slidey adds executive visibility

## Open Questions Raised
- How many other teams across Moody's have independently built PowerPoint generators?
- Should Slidey become a centrally supported App Factory application?
- What is the corporate DCI team's position on enabling Claude for PowerPoint/Excel?

## Raw Quotes of Note
- "Of all the complicated, fancy stuff we do, this will be the one that reaches the most people and gives the most value." — Azmain, on Slidey
