# WS4: Friday (Project Management App)

## Overview

Friday is an internal project/task management application being built by the team, conceptually similar to Monday.com. It occupies the WS4 slot in the programme, replacing the original Adoption Charter Workflow. The tool is intended for tracking programme tasks, managing project work across the Gen AI Programme's multiple workstreams, and providing internal project management capabilities for the team.

Azmain has been building Friday alongside his other work. As of early March 2026, he references it as "my project management app" and has been iterating on it using Claude Code in a cloud environment. On 4 March, he noted that he had instructed it to install additional skills and perform a full analysis and build, but the latest changes had not yet been pulled down and built locally -- explaining why visible progress appeared minimal despite significant backend work.

## History

### Original WS4: Adoption Charter Workflow

The Adoption Charter Workflow was the original fourth workstream, identified on 6 January 2026 when Richard laid out the six projects. The concept was to create a structured process for building customer-level adoption plans (adoption charters) that CSMs would use to guide IRP adoption at each account.

**Steve Gentilli** owned the adoption charter process. His session on 23 January revealed the current state: adoption charters are Excel-based documents containing diagrams, images, and structured data about each customer's adoption plan. They range from simple spreadsheets to complex multi-page documents with visual diagrams that are difficult for an LLM to parse.

### The 23 January Decision

On 23 January, Steve Gentilli and Azmain agreed to **fold the adoption charter functionality into CLARA** rather than building a separate system. The rationale: CLARA was already capturing much of the data that feeds into adoption charters (use cases, blockers, action plans, team members), so building a separate tool would create duplication.

### Adoption Charter Features in CLARA

- **v1 built:** By 5 February, Azmain confirmed that a v1 of the adoption charter section had already been built within CLARA. It needs modification, not greenfield work.
- **Blueprint and charter flow:** Still needs finalisation with Steve Gentilli and Liz Couchman.
- **Solution fit matrix:** Richard described Steve's "solution fit matrix" as a "glorified lookup" -- a separate piece that may or may not live inside CLARA. Richard was working on this as of early March (based on the 3 March standup, where he mentioned doing what Rhett had built and pushing it into dev).
- **Bi-directional challenge:** On 3 March, Azmain raised the complexity of adoption charters: many already exist as Excel files with diagrams and images. The ideal flow is CSMs enter data in CLARA, which generates an adoption charter document that can be exported and sent to customers. But customers then annotate or modify the document, and getting those changes back into CLARA requires reverse-engineering the document -- something difficult given the visual/diagrammatic content. Richard acknowledged this but argued the data flow should be one-directional to start: CLARA generates the charter, not the other way around.
- **Current priority:** On 3 March, Azmain explicitly deprioritised adoption charters, placing them third in the sequence after (1) processing consolidated feedback and (2) the blocker intelligence feature. He told the team: "I don't want to put that in the immediate plan."

### Transition to Friday

With adoption charter functionality folding into CLARA, the WS4 slot became available for Friday. The exact date of Friday's inception is not recorded in the transcripts, but by early March 2026, Azmain references it as an active side project built using Claude Code.

## Current Status (as of 9 March 2026)

- **State:** Early / iterative development
- **Tooling:** Being built using Claude Code in a cloud environment (Azmain's preferred approach -- avoids permission prompts, runs dependencies freely)
- **Latest update (4 Mar):** Azmain ran a major build cycle with expanded skills ("I added like 415 skills all in one through like three Git repos"), performed a full analysis and build. The output visually appeared unchanged because the latest changes had not been pulled down and built locally. He acknowledged needing to do that step.
- **Visibility:** Low. Friday has not been presented to stakeholders. It is primarily Azmain's internal tool at this stage.

## Team

| Role | Person | Notes |
|------|--------|-------|
| Builder / Owner | Azmain | Building it alongside CLARA and programme management duties |
| Vision / Oversight | Richard Dosoo | Advised on skills integration and approach |

## Adoption Charter Legacy -- Detailed Status

| Aspect | Status | Notes |
|--------|--------|-------|
| v1 charter section in CLARA | Built | Needs modification per Steve/Liz feedback |
| Solution fit matrix | In progress | Richard working on Rhett's build, pushing to dev (3 Mar) |
| Steve Gentilli review | Not started | Steve has not yet re-engaged to review CLARA's charter section |
| Liz Couchman review | Not started | Blueprint and charter flow needs her input |
| Bi-directional data flow | Deferred | Acknowledged as complex; starting with one-way (CLARA to document) |
| Existing charter import | Deferred | Parsing visual/diagrammatic Excel charters is technically challenging |

## Key Decisions

| Date | Decision | Rationale | Key People |
|------|----------|-----------|------------|
| 23 Jan | Fold adoption charter into CLARA | Rather than building a separate system, absorb charter functionality into the tracker where the underlying data already lives | Steve Gentilli, Azmain |
| 3 Mar | Deprioritise adoption charters in near-term plan | Feedback processing and blocker intelligence are higher priority; adoption charters placed third in the queue | Azmain |
| 3 Mar | Data flow should be one-directional to start | CLARA generates charters as output; reverse-engineering customer-annotated documents is deferred | Richard, Azmain |

## Open Questions

1. **Who is building Friday beyond Azmain?** Currently a solo effort. No other team members assigned.
2. **What features are planned for Friday?** No feature list or requirements document exists. Azmain described it as a project management app but specifics are unclear.
3. **What is the timeline for Friday?** No target date or milestones established.
4. **How does Friday integrate with CLARA?** Unclear whether Friday will connect to CLARA's data or remain a separate standalone tool.
5. **When will Steve Gentilli and Liz Couchman review CLARA's charter section?** This has been pending since January with no scheduled date.
6. **Is the solution fit matrix part of CLARA or a separate app?** Richard mentioned it could be either (3 Mar standup). Decision not yet made.
7. **How will existing adoption charters (Excel files with diagrams) be handled?** Azmain raised this concern on 3 March. No solution identified -- LLM parsing of visual content is difficult.

## Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Friday has no formal requirements or plan | Could drift or become unused | High | Needs a brief scope document and stakeholder buy-in |
| Azmain is the sole builder and already stretched thin | Progress will be slow and intermittent | High | Needs either dedicated time allocation or another builder |
| Adoption charter features in CLARA are stalled | Steve/Liz feedback loop hasn't started; charter functionality remains incomplete | Medium | Schedule review sessions with Steve and Liz |
| No visibility with leadership | Friday could be seen as unauthorised side project | Medium | Present concept to Richard/Natalia for endorsement |

## Transcript References

| Date | Transcript | Relevance |
|------|-----------|-----------|
| 6 Jan | `06-01-2026_-_AI_PM_Discussion_w_Richard.txt` | Richard identifies Adoption Charter Workflow as project 4 in the programme |
| 7 Jan | `07-01-2026_-_IRP_Admin_Support_-_PM_Touchpoint.txt` | Adoption charter tracking going to bi-weekly |
| 15 Jan | `15-01-2026_-_Tracker_demo_to_advisory_team.txt` | Steve Gentilli asks for dropdown categorisation on blockers for reporting |
| 23 Jan | `23-01-2026_-_Adoption_charter_w_Steve_Gentilli_.txt` | Steve describes current charter process. Decision to fold into CLARA. |
| 5 Feb | `2026-02-05_-_Programm_call_x_Martin__1_.txt` | Azmain confirms v1 of adoption charter section built in CLARA; needs modification |
| 20 Feb | `2026-02-20_-_Natalia_1-1.txt` | Azmain tells Natalia WS4 is folding into CLARA |
| 3 Mar | `2026-03-03 - GenAI Program Standup & Next steps.txt` | Adoption charters discussed -- complexity of existing Excel files, bi-directional data flow challenge, deprioritised in near-term. Richard working on solution blueprint via Rhett's build. |
| 4 Mar | `2026-03-04 - Build in 5 Discussion.txt` | Azmain references "my project management app" (Friday) -- ran skills integration build, needs to pull and build locally |
