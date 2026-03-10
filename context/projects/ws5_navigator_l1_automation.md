# WS5: IRP Navigator L1 Automation

## Overview

Workstream 5 aims to use the IRP Navigator's upcoming API support to automatically answer Level 1 (L1) support tickets — the routine, low-complexity queries that currently consume CSM and support team time. The concept is that a system built on top of Navigator's API could receive an L1 ticket, query Navigator for the relevant answer, and either auto-resolve or draft a response for human review.

The workstream sits at the intersection of the product team (who are building the Navigator API and MCP server infrastructure) and the customer success team (who handle the support tickets). The product team is building the foundational capability; the CS team needs to build the workflow and automation layer on top of it.

This is the least understood workstream in the programme. Azmain told Natalia on 20 February that he "doesn't fully understand it." No CS-side build has started. The product team is progressing independently with their MCP server work.

## Status

**EARLY STAGE** as of early March 2026.

The product team (Cihan, Lonny) is building MCP (Model Context Protocol) server infrastructure for IRP Navigator. This provides the technical foundation that WS5 would build upon. However, no CS-side work has started — there is no automation layer, no ticket routing logic, no integration with the support ticket system. The workstream exists as a concept with product-side progress but no CS-side execution.

The March 3 standup did not mention WS5 specifically. Richard grouped future work for Nicole/Chris as "the data pipeline, the Salesforce agent piece" — Navigator L1 automation was not listed among the immediate next priorities.

## Team

| Role | Person | Notes |
|------|--------|-------|
| Product — MCP Server | Cihan | Product team member building the MCP server for IRP Navigator. Met with Azmain on 19 Feb. |
| Product — MCP Server | Lonny | Product team member working with Cihan on MCP server. Described as being on the product side. |
| New Tech Consulting Lead | Nikhil | Replaced Alex. Introduced in the 19 Feb MCP meeting. Recently joined from banking/edfx. May bridge product and CS. |
| New Team Member | Bala | Also joined from banking/edfx. Introduced alongside Nikhil. Role in WS5 unclear. |
| Programme Lead (Nominal) | Azmain | Admitted to Natalia (20 Feb) that he "doesn't fully understand" this workstream. Has had no bandwidth to engage. |
| Programme Owner | Richard Dosoo | Framed WS5 on 6 Jan. Introduced Azmain to the product team (19 Feb). Has not defined the CS-side scope. |
| CS-Side Build | Unassigned | No one from the CS team has been allocated to build the automation layer. |

## Timeline

| Date | Event | Significance |
|------|-------|-------------|
| 6 Jan 2026 | Richard identifies WS5 in programme framing | Described as "IRP Navigator L1 Automation" — use Navigator's upcoming API support to auto-answer L1 tickets. Listed as Project 5 of 6 workstreams. |
| 19 Feb 2026 | MCP server discussion with Cihan and Lonny | **Key meeting.** Product team introduces MCP server work for Navigator. Nikhil (new tech consulting lead, replacing Alex) introduced. Bala also introduced. Azmain introduced as overseeing the Gen AI programme. Early-stage collaboration between product and CS teams begins. |
| 20 Feb 2026 | Azmain flags WS5 to Natalia | In 1:1, Azmain walks through all six workstreams. On WS5: "IRP Navigator L1 — not fully understood." Admits he does not have a clear picture of what the CS team needs to build versus what the product team delivers. |
| 3 Mar 2026 | GenAI Standup | WS5 not discussed. Nicole/Chris allocated to CLARA and then "data pipeline, Salesforce agent piece" — Navigator automation not in the immediate queue. |

## Technical Details

### MCP (Model Context Protocol) Server
The product team is building an MCP server for IRP Navigator. MCP is a protocol that enables AI models to interact with external tools and data sources in a standardised way. In this context:

- **What the product team is building:** An MCP server that exposes IRP Navigator's capabilities (data, models, results) through a standardised API. This would allow AI agents to query Navigator programmatically.
- **What this enables for WS5:** Once the MCP server is operational, a CS-side automation system could receive an L1 support ticket, parse the question, query Navigator via the MCP server, and generate a response.

### IRP Navigator
Navigator is the IRP platform's interface for accessing risk model results and data. Currently, using Navigator requires a human user interacting through the product UI. API support (via the MCP server) would allow programmatic access — opening the door to automated workflows.

### L1 Ticket Automation Concept
The envisioned workflow (not yet built):
1. L1 support ticket received (source system unclear — could be ServiceNow, Salesforce Cases, email)
2. Ticket parsed to identify the question type and relevant parameters
3. Query sent to Navigator via MCP server API
4. Response generated (either auto-resolve or draft for human review)
5. Response sent back to the ticket system

### Key Unknowns (Technical)
- What ticket system are L1 tickets currently managed in?
- What constitutes an "L1" ticket versus L2/L3? Is there a classification taxonomy?
- What percentage of L1 tickets could realistically be auto-answered?
- Does the MCP server provide sufficient capability to answer the types of questions that appear in L1 tickets?
- What accuracy threshold is required before auto-resolution is acceptable versus human-reviewed drafts?

## Blockers

1. **Azmain doesn't understand it** — The programme lead has explicitly stated he does not fully understand what this workstream requires. Without that understanding, no CS-side scope can be defined.

2. **No CS-side owner or build** — The product team is progressing their MCP server work independently. No one from the CS team has been assigned to build the automation layer that sits on top of the API.

3. **Unclear division of responsibility** — The fundamental question is: what does the product team deliver (the MCP server / Navigator API) versus what does the CS team need to build (the ticket routing, parsing, automation logic, integration with support systems)? This boundary has not been defined.

4. **Product team building independently** — Cihan and Lonny are building the MCP server as part of their product roadmap. Their timelines, priorities, and design decisions may not align with CS requirements. The 19 Feb meeting was the first formal connection between the two teams.

5. **Resource competition** — Even if the scope were clear, there are no CS-side development resources available. Azmain is consumed by CLARA. Nicole and Chris are being allocated to CLARA feedback and then the Salesforce agent piece. Martin is on Build in Five. BenVH is focused on app factory infrastructure.

6. **L1 ticket data not analysed** — No one has done the foundational analysis of what L1 tickets actually look like — volume, types, complexity distribution, current handling time. Without this, the business case and technical design cannot be grounded.

## Open Questions

1. **What does the CS team need to build versus what the product team delivers?** — This is the core question. The MCP server provides API access to Navigator. But someone needs to build: ticket ingestion, question parsing, query construction, response formatting, quality checks, human review workflow, and integration with the support ticket system. Who builds each piece?

2. **What is the MCP server timeline?** — When will the product team's MCP server be ready for CS to build on top of? Is it weeks, months, or quarters away?

3. **What does the L1 ticket landscape look like?** — Volume, types, complexity distribution, current handling time, current resolution rate. This analysis has not been done. Courtney's team analysed 2,000-3,000 HD-related support cases (26 Feb) — that data might be a starting point but is HD-specific, not Navigator-specific.

4. **Who should own the CS-side build?** — Given the technical nature (API integration, NLP for ticket parsing, automation logic), this needs someone with development skills. Nicole (who has Bedrock/AWS experience, as shown in the 3 Mar standup) could be a candidate once freed from CLARA work.

5. **How does this relate to the support team's existing processes?** — L1 tickets are presumably handled by a support team. Has that team been consulted? Are they open to automation? Do they have concerns about accuracy, accountability, or job displacement?

6. **Is the scope limited to Navigator, or broader?** — The original framing (6 Jan) specified "IRP Navigator L1 Automation." But L1 tickets may span topics beyond Navigator. Should the scope expand to cover other L1 question types, or stay focused on Navigator-answerable queries?

7. **What quality bar is required?** — Auto-answering support tickets carries risk. An incorrect automated response could damage customer trust. What accuracy threshold is needed? Should all responses be human-reviewed initially (draft mode) before moving to auto-resolve?

8. **How does this connect to Courtney's HD model analysis?** — Courtney (26 Feb) analysed thousands of support cases to identify adoption barriers. That analysis — while focused on HD models — demonstrates the kind of ticket taxonomy work needed for WS5. Is there an opportunity to leverage Courtney's methodology?

## Transcript References

| Date | Transcript | Relevance |
|------|-----------|-----------|
| 6 Jan | `06-01-2026_-_AI_PM_Discussion_w_Richard.txt` | **Key transcript.** Richard identifies WS5 as "IRP Navigator L1 Automation" — use Navigator API to auto-answer L1 tickets. |
| 19 Feb | `2026-02-19_-_MCP_server_with_Cihan___Lonny.txt` | **Key transcript.** Product team introduces MCP server work. Nikhil and Bala introduced. First formal connection between product MCP work and CS programme. |
| 20 Feb | `2026-02-20_-_Natalia_1-1.txt` | **Key transcript.** Azmain flags to Natalia that WS5 is "not fully understood." Admits he does not have clarity on what the CS team needs to build. |
| 26 Feb | `2026-02-26_-_HD_Models.txt` | Courtney's analysis of 2,000-3,000 HD support cases. Demonstrates ticket taxonomy methodology relevant to WS5 scoping. |
| 3 Mar | `2026-03-03 - GenAI Program Standup & Next steps.txt` | WS5 not discussed directly. Nicole/Chris allocated to CLARA then "data pipeline, Salesforce agent piece." Navigator automation not in immediate queue. |
