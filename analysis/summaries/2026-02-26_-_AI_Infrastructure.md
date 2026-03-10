# AI Infrastructure
**Date:** 2026-02-26
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (Speaker 2), Rahul (Speaker 4), Nikhil (Speaker 3), Chris Moorhouse (Speaker 6)
**Duration context:** Medium (~30 minutes)
**Workstreams touched:** WS2 CLARA, WS3 CS Agent

## Key Points
- Meeting had two objectives: (1) assess Cat Accelerate tech debt and decide priorities for FY26, (2) plan enablement of AWS Bedrock Claude/Anthropic models for CLARA integration and Claude Code access for team members.
- Cat Accelerate tech debt: Nikhil identifies the top issue as needing a separate AWS account for non-prod environments. Everything currently sits in one account, meaning accidental production deployments are possible. This has been requested for four years (blocked by RMS SRE under the old organisation), but Moody's now allows as many AWS accounts as needed -- described as "fruit rotting on the floor."
- CDK deployment concerns: current deployment uses Python-based CDK which is hard-coded and monolithic. If one piece breaks, all deployments stop. Nikhil suggests evaluating a move to simpler CloudFormation templates for more contained, per-client deployments. Ben notes CDK is used across both prod and non-prod.
- Rahul proposes a two-step approach: (1) prioritise tech debt by value delivered and risk mitigation, (2) identify team capacity to determine how many items can be addressed. He and Nikhil will produce a first-pass prioritised list.
- BenVH raises a critical gap: there are no proper unit tests or integration tests for Cat Accelerate infrastructure. The only verification is ad-hoc Postman collections of uncertain currency. This has been a major pain point for any infrastructure changes. Chris confirms certain libraries have tests but the deployment projects themselves do not.
- Rahul suggests using AI to generate automated test suites -- creating a reusable repo that can provide confidence reports. This becomes a backlog item with AI-assisted approach.
- Feature parity exercise needed: to migrate clients off Cat Accelerate onto product APIs, the team needs a client-by-client matrix of what Cat Accelerate does that the products do not. Chris has been doing this at the data view and orchestration layer level but without formal direction. Rahul wants to overlay this with capacity to produce a clear migration plan.
- Richard then pivots to the broader CS AI acceleration programme, walking Nikhil and Chris through the three-pillar structure: (1) IRP portfolio governance / CLARA, (2) platform embedded intelligence (Salesforce data pipeline, Sales Recon testing, IRP Navigator, L1 ticket automation via agents), (3) internal productivity and revenue acceleration.
- The L1 ticket automation concept explained in detail: agents managing a Salesforce ticket queue, answering questions via Navigator, routing back to customers if confidence threshold is met, or escalating to humans if not. This is the most significant piece of work in the programme.
- Nikhil raises the automated fixer agent concept for Cat Accelerate -- having agents debug issues using CloudWatch logs and GitHub repos. BenVH confirms the architecture would support this but emphasises agents should only submit PRs requiring human review, never auto-approve.
- Cursor budget crisis surfaces again: Azmain explains the $500 included-in-plan limit vs. the on-demand second $500 that got shut down. Someone from asset management suggested downgrading to Sonnet 4.5, which Azmain initially resisted.

## Decisions Made
- Separate non-prod AWS account to be top priority for Cat Accelerate tech debt -> Nikhil / Richard
- Tech debt list to be prioritised by value delivered and risk mitigation -> Rahul / Nikhil
- Automated test suite creation to be approached using AI-generated scripts -> Rahul / Nikhil
- Feature parity matrix for Cat Accelerate migration to be built client-by-client -> Chris / Rahul
- Nikhil and Chris to support CS AI programme on platform embedded intelligence and Navigator testing -> Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Produce first-pass prioritised tech debt list with risk/value assessment | Rahul / Nikhil | Next week | Open |
| Present tech debt prioritisation to Richard (30 min session) | Rahul / Nikhil | Next week | Open |
| Work with Stacy on capacity view overlay for tech debt | Rahul | Next week | Open |
| Refine feature parity matrix for Cat Accelerate migration | Chris / Rahul | Ongoing | Open |
| Set up AI-generated automated test suite approach | Rahul / Nikhil | Backlog | Open |
| Send CLARA link and GitHub repo access to Chris | Richard / Nikhil | Today | Open |

## Stakeholder Signals
- Rahul is structured and action-oriented, immediately proposing a clear prioritisation framework and capacity overlay approach.
- BenVH is frustrated by the lack of testing infrastructure -- he cannot verify systems work as expected and regularly has to go to other team members just to figure out how to test things.
- Nikhil is technically engaged and already thinking about practical solutions (separate AWS account, CloudFormation migration).
- Chris has been doing feature parity work independently but without direction -- an opportunity to formalise and accelerate.

## Open Questions Raised
- Should the team move from CDK to CloudFormation for deployments, or is the CDK investment worth preserving?
- How much capacity does the team have for tech debt vs. new programme work?
- Will the automated fixer agent concept extend to Cat Accelerate or remain scoped to CLARA/app factory?
- How will the AI governance process affect the timeline for deploying Bedrock models?

## Raw Quotes of Note
- "I'm not aware of proper unit testing or integration testing... the only way that we verify it works honestly is we have some Postman collections that are kind of floating around." -- BenVH, on the Cat Accelerate testing gap
