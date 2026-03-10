# WS3: Customer Success Agent

## Overview

Workstream 3 covers the development of a Customer Success Agent — an AI-powered assistant designed to help CSMs with their day-to-day work by pulling data from Salesforce and providing conversational access to account intelligence. The prototype was built by Kevin Pern using Microsoft Copilot Studio with a Salesforce integration. The concept is distinct from CLARA (which is an IRP adoption tracker) — this is meant to be a general-purpose CS agent that helps CSMs query customer data, prepare for meetings, and surface relevant information without navigating multiple systems.

The workstream has been essentially orphaned since the programme began. Kevin has been working alone with no programme oversight, no review of what he has built, and no integration into the broader programme roadmap.

## Status

**MINIMAL PROGRESS** as of early March 2026.

Kevin Pern built a prototype using Copilot Studio connected to Salesforce, but the workstream has received no programme attention. Azmain told Natalia on 20 February that it "needs engagement" — Kevin is working alone with nothing operationalised. No one has formally assessed what the prototype does, whether it is viable, or how it fits with the broader programme direction (CLARA, Sales Recon, Gainsight).

In the March 3 standup, Richard mentioned that Nicole and Chris should eventually work on "the Salesforce agent piece" after completing their CLARA onboarding — this is the first concrete signal that WS3 may get programme resources, though it is positioned as a future priority, not an immediate one.

## Team

| Role | Person | Notes |
|------|--------|-------|
| Prototype Builder | Kevin Pern | Built Copilot Studio + Salesforce prototype. Working alone. No programme oversight. Located in Hossa. Also involved in User Voice integration discussions (26 Feb). |
| Nominal Programme Lead | Azmain | Has not engaged Kevin. Identified this gap to Natalia on 20 Feb. |
| Future Resources (Planned) | Nicole, Chris | Richard stated (3 Mar) they should work on "the Salesforce agent piece" after CLARA onboarding (estimated ~1 week). |
| Programme Owner | Richard Dosoo | Framed WS3 on 6 Jan. Has not followed up with Kevin. On 3 Mar, explicitly named it as a future task for Nicole/Chris. |

## Timeline

| Date | Event | Significance |
|------|-------|-------------|
| 6 Jan 2026 | Richard identifies WS3 in programme framing | Described as "Customer Success Agent (Kevin Pern's Copilot Studio work)" — Project 3 of 6 workstreams. Richard positions it alongside the other five for Azmain to oversee. |
| 26 Jan 2026 | Sales Recon executive session | Meeting with Ari Lahavi, Jamie, and senior leadership. "Intelligence Anywhere" (Salesforce data surfaced into Copilot) confirmed on Sales Recon Q1 roadmap. Raises the question of whether Kevin's agent overlaps with or complements Sales Recon's planned capabilities. |
| 4 Feb 2026 | Sales Recon pilot — CSM nominations | Kevin Pern nominated as one of 8 CSMs for the Sales Recon UAT pilot. This gives him direct exposure to the enterprise platform that may overlap with his agent's functionality. |
| 11 Feb 2026 | Sales Recon two-week pilot begins | 8 CSMs testing account intelligence, meeting prep agent, and share knowledge agent. These capabilities overlap directly with what a CS Agent would do. Kevin is one of the pilot participants. |
| 20 Feb 2026 | Azmain flags WS3 to Natalia | In 1:1, Azmain walks through all six workstreams. On WS3: "CS Agent (Kevin Pern) — needs engagement." Explicitly calls out that Kevin is working alone with nothing operationalised. |
| 26 Feb 2026 | Peter Kimes / User Voice discussion | Kevin Pern participates in the User Voice integration requirements session alongside Peter Kimes and Stacy. Shows Kevin is active in adjacent conversations but still isolated on his agent work. |
| 3 Mar 2026 | GenAI Standup — future resource allocation | Richard states that after Nicole and Chris onboard to CLARA (~1 week), they should move to "the data pipeline, the Salesforce agent piece." First concrete signal that WS3 will get programme resources. |

## Technical Details

### What Kevin Built
- **Platform:** Microsoft Copilot Studio — Microsoft's low-code agent builder
- **Integration:** Connected to Salesforce — the primary CRM used by CSMs
- **Functionality:** Details are sparse because no one from the programme has formally reviewed the prototype. Based on the programme framing (6 Jan), the concept is an agent that can:
  - Query Salesforce data conversationally
  - Help CSMs access account information without navigating Salesforce directly
  - Potentially surface insights across accounts

### Overlap with Sales Recon
The Sales Recon platform led by Jamie includes "Intelligence Anywhere" — described as Salesforce data surfaced into Copilot. This is functionally very similar to what Kevin's agent appears to do. The Sales Recon pilot (11-24 Feb) tested three features:
1. Account intelligence
2. Meeting preparation agent
3. Share knowledge agent

All three overlap with a CS Agent's intended capabilities. If Sales Recon delivers on its roadmap, Kevin's standalone prototype may become redundant — or it may fill gaps that Sales Recon does not address for insurance-specific use cases.

### Copilot Studio Context
Copilot Studio is part of the Microsoft ecosystem. Moody's already uses Microsoft tools (Teams, Azure AD). Using Copilot Studio for the CS Agent means:
- Lower integration friction with existing Moody's infrastructure
- Potential licence cost implications (Copilot Studio licences are separate from standard M365)
- Alignment with the "Intelligence Anywhere" direction that Sales Recon is pursuing

## Blockers

1. **No programme oversight** — Kevin has been working alone since the programme started. No one has reviewed his prototype, assessed its viability, or connected it to the broader programme roadmap.

2. **No engagement from programme team** — Azmain has not had bandwidth to engage Kevin. Richard has not followed up. The workstream has been de facto deprioritised in favour of CLARA.

3. **Unclear overlap with Sales Recon** — "Intelligence Anywhere" and the Sales Recon pilot cover similar ground. Until the pilot results are assessed and the Sales Recon roadmap is clear, it is hard to define what WS3 should uniquely deliver.

4. **Salesforce data access constraints** — CLARA has struggled with Salesforce data access (API access blocked for Gainsight, no direct read access). Kevin's agent presumably depends on Salesforce API access — the status of that access for his prototype is unknown.

5. **Resource availability** — Nicole and Chris are the planned future resources, but they are currently onboarding to CLARA and helping BenVH with app factory infrastructure. Their availability for WS3 is at least 1-2 weeks out as of early March.

## Open Questions

1. **What does Kevin's prototype actually do?** — No one from the programme team has formally reviewed it. Before making any decisions about WS3, someone needs to sit with Kevin, see the prototype, and assess its capabilities, maturity, and viability.

2. **How does this relate to Sales Recon's "Intelligence Anywhere"?** — The two-week Sales Recon pilot (11-24 Feb) tested capabilities that overlap with a CS Agent. What were the pilot results? Does Sales Recon cover the CS Agent use case, or are there insurance-specific gaps?

3. **Should WS3 pivot or continue?** — Depending on the Sales Recon pilot results and Kevin's prototype assessment, WS3 could:
   - Continue as a standalone Copilot Studio agent filling gaps Sales Recon does not cover
   - Merge into the Sales Recon workstream as insurance-specific requirements
   - Be deprioritised entirely if Sales Recon delivers equivalent functionality
   - Pivot to a different agent concept (e.g., an agent that queries CLARA data rather than Salesforce)

4. **Who should engage Kevin?** — Richard, Azmain, or the new team members (Nicole/Chris)? Kevin has been isolated for two months — the engagement needs to be respectful of his work while honest about programme direction.

5. **What Salesforce API access does Kevin have?** — CLARA's experience suggests Salesforce API access is not straightforward at Moody's. Does Kevin have working API access, or is his prototype using a workaround?

6. **Is Copilot Studio the right platform?** — With the team standardising on AWS (for CLARA) and exploring Claude/Bedrock (for AI capabilities), does a Microsoft Copilot Studio agent fit the target architecture? Or would it be better to rebuild using the same stack as CLARA?

7. **What is the data pipeline relationship?** — Richard (3 Mar) grouped "the data pipeline, the Salesforce agent piece" together as work for Nicole/Chris. Is the data pipeline separate from the CS Agent, or are they related components?

## Transcript References

| Date | Transcript | Relevance |
|------|-----------|-----------|
| 6 Jan | `06-01-2026_-_AI_PM_Discussion_w_Richard.txt` | **Key transcript.** Richard identifies WS3 as "Customer Success Agent (Kevin Pern's Copilot Studio work)." |
| 12 Jan | `12-01-2026_-_Review_Agenda_for_Sales_Recon.txt` | Sales Recon meeting prep — "Intelligence Anywhere" on Q1 roadmap. Establishes the overlap question. |
| 26 Jan | `26-01-2026_-__IMP__SalesRecon__1_.txt` | Executive session with Ari/Jamie. "Intelligence Anywhere" confirmed. CS workflow convergence with Sales Recon agreed as end-state. |
| 4 Feb | `2026-02-04_-_SalesRecon_Process_Coordination.txt` | Kevin Pern nominated for Sales Recon UAT pilot. |
| 11 Feb | `2026-02-11_15-31-58.txt` | Sales Recon pilot kickoff. Three features being tested that overlap with CS Agent concept. |
| 20 Feb | `2026-02-20_-_Natalia_1-1.txt` | **Key transcript.** Azmain flags to Natalia that WS3 "needs engagement" — Kevin working alone, nothing operationalised. |
| 26 Feb | `2026-02-26_-_Blockers_with_P_Kimes.txt` | Kevin Pern participates in User Voice integration discussion. Shows he is active but still isolated on WS3. |
| 3 Mar | `2026-03-03 - GenAI Program Standup & Next steps.txt` | **Key transcript.** Richard plans Nicole/Chris to work on "the Salesforce agent piece" after CLARA onboarding. First resource commitment to WS3. |
