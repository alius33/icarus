# Cowork Usage Guide

## Quick Start: Process New Transcripts

The most common task. Drop new `.txt` files into `Transcripts/`, then run:

```
claude cowork cowork/analyse-transcripts.md
```

This runs the full pipeline: detect new transcripts → summarise each one → update weekly summaries → update context files → trigger backend import.

See `analyse-transcripts.md` for the full task definition with agent roles.

You can also use `/analyse` as a slash command in Claude Code for the same pipeline (single-agent mode).

## How This Project Works with Cowork

Cowork allows multiple Claude instances to work on this project in parallel. This is useful for:

- **Batch transcript processing** — multiple transcripts analysed simultaneously
- **Cross-referencing** — one agent reads transcripts while another updates trackers
- **Deep analysis** — one agent traces a theme across all transcripts while another handles new additions

## Recommended Cowork Patterns

### Pattern 1: Process New Transcripts (most common)

Use the `analyse-transcripts.md` task definition. It handles:

1. **Agent 1 (Detector):** Finds unprocessed transcripts, loads context
2. **Agents 2-3 (Summarisers):** Split transcripts between them, write summaries in parallel
3. **Agent 4 (Weekly + Context):** Updates weekly summaries and context files
4. **Agent 5 (Import):** Triggers backend import and reports results

### Pattern 2: Deep Thematic Analysis

When you want to trace a theme (e.g., "how has data quality sentiment evolved?"):

1. **Agent A:** Read all transcripts chronologically, extract relevant passages
2. **Agent B:** Read context files and debrief, identify the current state
3. **Synthesis:** Combine findings into `analysis/trackers/[theme].md`

### Pattern 3: Stakeholder Deep Dive

When you want to understand one person's arc:

1. **Agent A:** Find all transcripts where [person] is mentioned or present
2. **Agent B:** Build a timeline of their positions, concerns, and decisions
3. **Output:** Update `context/stakeholders.md` with richer profile

### Pattern 4: Advisory & Operational

Conversational tasks where Claude acts as a programme analyst colleague. These respond in text, not files.

| Task | Use when... |
|------|-------------|
| `meeting-prep.md` | You're about to go into a meeting and want context, talking points, and risk flags |
| `programme-advice.md` | You need strategic advice: what to escalate, where to focus, whether to push for something |
| `review-and-challenge.md` | You want a critical review of a plan, tracker, decision, or situation — gaps, inconsistencies, political risks |
| `stakeholder-briefing.md` | You're about to meet someone and want their full arc: sentiment, commitments, influence, approach tips |
| `weekly-pulse.md` | It's Monday morning — what do you need to know and do this week? |
| `catch-up.md` | You've been away and need a structured debrief of what changed since a specific date |
| `status-draft.md` | You need to draft an email, Slack message, or speaking notes tailored to a specific audience |
| `trend-analysis.md` | You want to compare time periods or trace how risk/sentiment/topics have evolved |

### Pattern 5: Report Generation

Generate exportable reports (PowerPoint, Excel, Word, PDF) from programme data.

| Task | What it produces |
|------|-----------------|
| `generate-report.md` | Unified report generator supporting 4 types: executive debrief (PPTX), stakeholder dossier (XLSX), risk dashboard (XLSX), or custom (any format) |

Reports use the `/pptx`, `/xlsx`, `/docx`, and `/pdf` skills. Output is saved to the project root.

## File Locking Awareness

Cowork agents should avoid editing the same file simultaneously. To prevent conflicts:

- Each agent writes to **different output files** (e.g., separate summary files)
- Only **one agent** updates a shared context file at a time
- Use the summary files as intermediaries — write summaries first, then consolidate into context files in a separate step

## Context Files for Cowork Agents

Every cowork agent should read these at session start:
1. `CLAUDE.md` — project rules and workflow
2. `context/glossary.md` — names, acronyms, systems
3. `context/stakeholders.md` — who's who

Then read additional context based on the task:
- Transcript processing → also read all files in `context/projects/`
- Decision tracking → also read `context/decisions.md`
- Gap analysis → also read `context/open_threads.md`
