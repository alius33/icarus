# Generate Weekly Report

Generate or update a weekly summary report for a specific week.

## Arguments
$ARGUMENTS = week date (e.g. "2026-03-03") or "latest"

## Steps

1. Determine the target week:
   - If "$ARGUMENTS" is "latest", find the most recent Monday
   - Otherwise, parse the date and find its Monday
2. Read the previous week's summary from `analysis/weekly/`
3. Find all summaries in `analysis/summaries/` that fall within the target week
4. Read all relevant summaries
5. Load context:
   - All files in `context/projects/`
   - `context/stakeholders.md`
   - `context/open_threads.md`

## Generation

Follow the weekly summary template from CLAUDE.md exactly. Key requirements:
- **Continuity**: Reference last week's state. What moved forward? What stalled?
- **Narrative flow**: Write like an executive briefing, not a bullet dump
- **Risk tracking**: Carry forward risks with escalation/de-escalation notes
- **Stakeholder trajectories**: Track sentiment over time
- **Carried forward**: Explicitly list 3-5 live items from previous weeks

## Output
Write to `analysis/weekly/week-of-YYYY-MM-DD.md` (Monday date).
Report: transcripts covered, key findings, any context files updated.
