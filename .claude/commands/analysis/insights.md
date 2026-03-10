# Deep Transcript Insights

Perform deep analysis on transcripts to extract patterns, trends, and strategic intelligence.

## Arguments
$ARGUMENTS = focus area (e.g. "CLARA adoption", "stakeholder dynamics", "risks", or "all")

## Steps

1. Load all context files (glossary, stakeholders, workstreams)
2. Read ALL summaries from `analysis/summaries/`
3. Read ALL weekly reports from `analysis/weekly/`

## Analysis Dimensions

### Stakeholder Dynamics
- Map who talks to whom most frequently
- Track sentiment trajectories per person over time
- Identify power dynamics and influence patterns
- Flag relationship tensions or alignments
- Note who's absent from key conversations

### Decision Patterns
- How quickly do decisions get made vs. discussed?
- Which decisions get revisited or reversed?
- Who drives decisions vs. who blocks them?
- Are decisions being followed through?

### Risk Evolution
- Which risks have been raised most frequently?
- Which risks escalated vs. de-escalated?
- Are there blind spots — risks that should be discussed but aren't?
- What's the gap between stated priorities and actual attention?

### Programme Momentum
- Is the programme accelerating, steady, or decelerating?
- Which workstreams are moving vs. stalled?
- Resource allocation vs. stated priorities
- Scope creep trajectory

### Sentiment Analysis
- Overall programme mood trajectory
- Confidence levels per stakeholder
- Frustration indicators
- Enthusiasm signals

## Output

Write a strategic intelligence brief covering the requested focus area(s).
Include:
- Key findings with supporting evidence (quotes, dates, patterns)
- Trend visualizations (ASCII charts where helpful)
- Recommendations ranked by impact
- Watchlist items for coming weeks

Save to `analysis/insights/YYYY-MM-DD_-_focus-area.md`
