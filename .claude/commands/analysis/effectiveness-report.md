---
description: Analyse meeting patterns and generate recommendations for improving meeting productivity
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent
argument-hint: [period|meeting-title|all]
---

# Meeting Effectiveness Report

Analyse meeting patterns across the programme and generate actionable recommendations for improving meeting productivity, decision velocity, and follow-through rates.

## Arguments
$ARGUMENTS -- Options:
- empty or `all`: full analysis across all scored meetings
- `last N weeks`: analyse meetings from the last N weeks only
- `[meeting-title]`: deep-dive into a specific meeting or meeting series

---

## Step 1: Load Data

Read these files in parallel:

1. `analysis/trackers/meeting_scores.md` -- existing meeting effectiveness scores
2. `analysis/trackers/action_items.md` -- action items for follow-through analysis
3. `analysis/trackers/commitments.md` -- commitments for tracking fulfilment
4. `context/decisions.md` -- decision log for decision velocity analysis
5. ALL files in `analysis/summaries/` -- for meetings that lack scores and for qualitative analysis

---

## Step 2: Score Unscored Meetings

Check each summary in `analysis/summaries/` against `analysis/trackers/meeting_scores.md`. For any meeting that lacks a score entry, compute one.

### Scoring Method

For each unscored meeting, read the summary and compute:

1. **Meeting type classification** -- Categorise based on content:
   - `decision_making`: agenda was focused on reaching decisions. Multiple options weighed, conclusions drawn.
   - `status_update`: participants reported progress. Mostly informational, light on decisions.
   - `brainstorming`: exploratory discussion, idea generation. Few concrete outcomes expected.
   - `escalation`: raised problems or blockers to higher authority for resolution.
   - `planning`: created or refined plans, timelines, resource allocations.
   - `review`: reviewed completed work, retrospective analysis.
   - `onboarding`: introduced new people or concepts to the group.
   - If the meeting had mixed purposes, classify by the dominant mode (>50% of discussion time).

2. **Decision Velocity** (0.0 - 1.0):
   - Count topics discussed (from Theme Segments or Key Points)
   - Count decisions made + decisions explicitly deferred (from Decisions Made section)
   - Score = (decisions_made + decisions_deferred) / max(topics_discussed, 1)
   - Cap at 1.0
   - Note: for brainstorming or status_update meetings, this metric is less relevant but still computed

3. **Action Clarity** (0.0 - 1.0):
   - Count total action items (from Action Items table)
   - Count action items that have BOTH a named owner AND a deadline (not "unspecified")
   - Score = clear_actions / max(total_actions, 1)
   - If no actions were generated: score = 0.5 (neutral -- not all meetings need actions)

4. **Engagement Balance** (0.0 - 1.0):
   - Estimate speaking time distribution from Power Dynamics table or general transcript analysis
   - Compute Gini coefficient of speaking time across participants
   - Score = 1.0 - gini_coefficient
   - 1.0 = perfectly balanced participation, 0.0 = one person monopolised
   - If only 2 participants: use simple ratio (more balanced = higher score)
   - If Power Dynamics table is missing: estimate from the number of people quoted or contributing to Key Points

5. **Topic Completion** (0.0 - 1.0):
   - Count topics discussed
   - Count topics that reached a conclusion: a decision was made, an action was assigned, or the topic was explicitly deferred to a specific follow-up
   - Score = completed_topics / max(total_topics, 1)
   - Partial credit: if a topic had actions assigned but no decision, count as 0.5 completed

6. **Follow Through** (0.0 - 1.0):
   - Check `analysis/trackers/action_items.md` for items created before this meeting
   - Count how many previous open items were mentioned, addressed, or updated in this meeting
   - Score = addressed_previous_items / max(total_previous_open_items, 1)
   - If this is the first meeting (no prior items): score = 0.5 (neutral)
   - Note: this requires knowing what items were open at the time of the meeting

7. **Overall Score** (0-100):
   ```
   overall = round((
     decision_velocity * 0.25 +
     action_clarity * 0.20 +
     engagement_balance * 0.20 +
     topic_completion * 0.20 +
     follow_through * 0.15
   ) * 100)
   ```

Append each scored meeting to `analysis/trackers/meeting_scores.md`:
```
| [date] | [title] | [type] | [overall] | [decision_velocity] | [action_clarity] | [engagement_balance] | [topic_completion] | [follow_through] | [participant_count] | [duration_category] |
```

---

## Step 3: Aggregate Analysis

With all meetings scored, compute aggregate metrics:

### By Meeting Type
| Type | Count | Avg Score | Avg Decision Velocity | Avg Action Clarity | Avg Engagement | Avg Completion | Avg Follow Through |
|------|-------|-----------|----------------------|-------------------|----------------|----------------|-------------------|

### By Time Period (weekly)
| Week | Meetings | Avg Score | Trend vs Previous | Best Meeting | Worst Meeting |
|------|----------|-----------|-------------------|-------------|---------------|

### By Participant Count
| Size | Count | Avg Score | Notes |
|------|-------|-----------|-------|
| Small (2-3) | ... | ... | ... |
| Medium (4-6) | ... | ... | ... |
| Large (7+) | ... | ... | ... |

### Score Distribution
- Minimum score: [X]
- Maximum score: [X]
- Median score: [X]
- Standard deviation: [X]
- Meetings scoring below 40: [count] (these need attention)
- Meetings scoring above 70: [count] (good examples to replicate)

---

## Step 4: Pattern Detection

Analyse the scores for actionable patterns:

### Decision Latency

Read `context/decisions.md` and cross-reference with summaries. For each topic that appears in multiple meetings:
1. When was it first discussed?
2. When was a decision made (if ever)?
3. How many meetings elapsed between first discussion and decision?
4. Latency = meetings_to_decision

Flag topics with latency >= 3 meetings as **decision latency alerts**.

### Recurring Topics Without Resolution

From summaries, identify topics that appear in 3+ meetings without reaching a decision or generating clear actions. These are meeting time sinks.

### Follow-Through Trends

From the action items tracker:
1. What percentage of actions get completed vs. left open?
2. Average time from action creation to completion (or staleness)
3. Is follow-through improving or declining over time?
4. Which owners have the best/worst completion rates? (Be diplomatic in reporting this.)

### Engagement Patterns

From Power Dynamics tables across meetings:
1. Who consistently dominates? (might need meeting facilitation)
2. Who is consistently an observer? (might be disengaged or not needed in the meeting)
3. Are there meetings where key decision-makers are absent?

### Meeting Type Effectiveness

Which meeting types score highest? Are there meeting types that consistently underperform? Should any meeting types be restructured?

---

## Step 5: Generate Recommendations

Based on patterns detected, generate specific, actionable recommendations:

### Structural Recommendations
- Meetings that should be split, combined, or eliminated
- Optimal meeting size suggestions based on data
- Meeting type adjustments (e.g., "Convert weekly status updates to async written updates")

### Process Recommendations
- Specific process changes that would improve low-scoring dimensions
- Template for each recommendation:
  - **Problem:** [what the data shows]
  - **Recommendation:** [specific change]
  - **Expected impact:** [which scores would improve]
  - **Priority:** HIGH / MEDIUM / LOW

### Follow-Through Recommendations
- Action tracking improvements
- Commitment accountability suggestions
- Meeting start rituals (review of previous actions)

---

## Step 6: Update Tracker

Ensure `analysis/trackers/meeting_scores.md` contains entries for all meetings. Remove any duplicate entries (same meeting scored twice).

---

## Step 7: Generate Report

Write the report to `analysis/insights/YYYY-MM-DD_-_meeting-effectiveness.md`:

```markdown
# Meeting Effectiveness Report -- [Date]
**Period analysed:** [start date] to [end date]
**Meetings scored:** [count]
**Average score:** [X]/100

## Key Findings
[3-5 bullet points summarising the most important patterns and their implications]

## Score Overview

### Overall Distribution
- **Best meeting:** [title] ([score]) -- [why it scored well in 1 sentence]
- **Worst meeting:** [title] ([score]) -- [why it scored poorly in 1 sentence]
- **Median score:** [X]
- **Meetings needing attention (< 40):** [count]
- **Strong meetings (> 70):** [count]

### Score Trend Over Time
[ASCII chart showing weekly average scores over time]
```
Week 1 (MM-DD): ========== [avg]
Week 2 (MM-DD): ============ [avg]
Week 3 (MM-DD): ======= [avg]
...
```

### By Meeting Type
| Type | Count | Avg Score | Best Dimension | Worst Dimension | Notes |
|------|-------|-----------|---------------|-----------------|-------|
| decision_making | N | X | [dim] | [dim] | ... |
| status_update | N | X | [dim] | [dim] | ... |
| ... | ... | ... | ... | ... | ... |

### By Meeting Size
| Size | Count | Avg Score | Insight |
|------|-------|-----------|---------|
| Small (2-3) | N | X | [pattern observation] |
| Medium (4-6) | N | X | [pattern observation] |
| Large (7+) | N | X | [pattern observation] |

## Dimension Deep Dive

### Decision Velocity
- **Programme average:** [X]
- **Trend:** [improving/stable/declining]
- **Best performing:** [meeting type or specific meeting]
- **Concern areas:** [where decision velocity is consistently low]
- **Decision latency alerts:**
  | Topic | First Discussed | Meetings Elapsed | Status |
  |-------|----------------|-----------------|--------|
  | ... | ... | ... | [still open / finally decided on DATE] |

### Action Clarity
- **Programme average:** [X]
- **Trend:** [improving/stable/declining]
- **Most common gap:** [missing owners / missing deadlines / both]
- **Meetings with no clear actions:** [count] -- [is this appropriate for their type?]

### Engagement Balance
- **Programme average:** [X]
- **Dominant voices:** [people who consistently have high engagement %]
- **Consistently quiet:** [people who are mostly observers]
- **Most balanced meeting:** [title] ([score])
- **Least balanced meeting:** [title] ([score])

### Topic Completion
- **Programme average:** [X]
- **Recurring incomplete topics:**
  | Topic | Meetings Discussed | Times Completed | Completion Rate |
  |-------|-------------------|-----------------|-----------------|
  | ... | ... | ... | ... |

### Follow Through
- **Programme average:** [X]
- **Trend:** [improving/stable/declining]
- **Action completion rate:** [X]% of all actions ever created are now completed
- **Average action lifespan:** [X] days from creation to completion
- **Stalled actions (2+ weeks open):** [count]
- **Owners with best follow-through:** [names, diplomatically]

## Meeting Time Analysis

### Estimated Time Investment
- Total meetings in period: [N]
- Estimated total person-hours: [rough estimate based on participant count * duration]
- Meetings with score < 50: [N] -- estimated [X] person-hours of low-value meetings

### Meetings That Could Be Async
[List meetings that were primarily status_update type with high engagement imbalance (one person presenting). These might be better as written updates.]

### Meetings That Need More Time
[List meetings with low topic_completion but high decision_velocity -- they are making decisions but running out of time for all topics.]

## Recurring Topics Without Resolution

| Topic | First Discussed | Times Discussed | Any Decision? | Any Actions? | Assessment |
|-------|----------------|-----------------|---------------|-------------|------------|
| ... | ... | ... | No | N open | [time sink / needs escalation / needs dedicated session] |

## Recommendations

### High Priority
1. **[Recommendation]**
   - Problem: [data-backed observation]
   - Action: [specific change to implement]
   - Expected impact: [which scores improve, by how much]

2. **[Recommendation]**
   - Problem: [observation]
   - Action: [change]
   - Expected impact: [improvement]

### Medium Priority
3. **[Recommendation]** -- [brief rationale]
4. **[Recommendation]** -- [brief rationale]

### Quick Wins
5. **[Small change, easy to implement]** -- [brief rationale]
6. **[Small change]** -- [brief rationale]

## What Good Looks Like

Based on the highest-scoring meetings in this programme, effective meetings share these traits:
- [Trait 1 observed in high-scoring meetings]
- [Trait 2]
- [Trait 3]
- [Trait 4]

Consider using these as a checklist for meeting organisers.
```

---

## Step 8: Trigger Import (if tracker was updated)

If `analysis/trackers/meeting_scores.md` was modified:

```bash
cd backend && python -m scripts.import_data --data-root .. --db-url "$DATABASE_URL"
```

Report completion with summary statistics.
