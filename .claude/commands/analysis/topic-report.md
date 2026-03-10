---
description: Generate a deep analysis of how discussion topics have evolved across all meetings
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent
argument-hint: [period|all|topic-name]
---

# Topic Evolution Report

Generate a deep analysis of how discussion topics have evolved across all meetings. Identifies rising, stable, declining, and going-cold themes with supporting evidence.

## Arguments
$ARGUMENTS -- Options:
- empty or `all`: analyse all topics across all available summaries
- `last N weeks`: analyse topics from the last N weeks only
- `[topic-name]`: deep-dive into a specific topic's evolution

---

## Step 1: Load Data

Read these files in parallel:

1. `analysis/trackers/topic_evolution.md` -- existing topic tracking data
2. `context/glossary.md` -- for recognising topic-related terminology
3. `context/workstreams.md` -- for mapping topics to workstreams
4. ALL files in `analysis/summaries/` -- list with `ls analysis/summaries/`, then read each file

**Context window strategy:** If there are more than 30 summaries, process in chronological batches of 15. Carry forward a compressed topic state between batches (topic name, last mention date, mention count, last known intensity).

---

## Step 2: Extract Topic Data

For each summary file, extract topic data from the "Theme Segments" table (if present) and from the "Key Points" section. For each topic found:

- **Topic name**: normalise to a canonical form (e.g., "CLARA adoption", "token costs", "data quality", "resource strain")
- **Category**: technical / strategic / interpersonal / operational / governance
- **Date**: from the summary's date field
- **Intensity**: rate 1-5 based on how much discussion time/depth the topic received
  - 1 = passing mention (one sentence)
  - 2 = brief discussion (one paragraph)
  - 3 = moderate discussion (multiple points, some back-and-forth)
  - 4 = significant topic (extended discussion, multiple stakeholders weighed in)
  - 5 = dominant topic (central theme of the meeting)
- **Project association**: which project(s) this topic relates to
- **Key stakeholders**: who discussed this topic
- **Key quote**: most representative quote (if available)
- **Confidence**: HIGH / MEDIUM / LOW

Build a timeline for each topic: an ordered list of (date, intensity, meeting_title, key_point) tuples.

---

## Step 3: Compute Topic Trends

For each topic with 2+ data points, compute:

1. **First raised**: date of earliest mention
2. **Last mentioned**: date of most recent mention
3. **Total meetings**: count of meetings where this topic appeared
4. **Average intensity**: mean of all intensity scores
5. **Recent intensity**: average intensity over the last 2 weeks
6. **Trend classification**:
   - **RISING**: recent intensity > historical average by 0.5+ points, OR frequency increasing (more mentions per week recently than historically)
   - **STABLE**: recent intensity within 0.5 points of historical average, AND frequency roughly constant
   - **DECLINING**: recent intensity < historical average by 0.5+ points, OR frequency decreasing
   - **GOING COLD**: no mention in the last 2 weeks despite being discussed 3+ times previously
   - **NEW**: first appeared in the last 2 weeks
   - **ONE-OFF**: mentioned only once, not repeated
7. **Trajectory chart**: ASCII sparkline showing intensity over time (e.g., `_.-'^-._.` )
8. **Concern level**: Should this topic be getting more attention than it is? Based on severity of related risks and decisions pending.

---

## Step 4: Cross-Reference Analysis

For each significant topic (3+ mentions or HIGH intensity):

1. **Related decisions**: check `context/decisions.md` for decisions touching this topic
2. **Related risks**: check `analysis/trackers/risk_register.md` for risks on this topic
3. **Related actions**: check `analysis/trackers/action_items.md` for open actions
4. **Stakeholder positions**: check `analysis/trackers/sentiment_tracker.md` for sentiments on this topic
5. **Contradictions**: check `analysis/trackers/contradictions.md` for position changes on this topic

Flag topics where:
- There is a risk but declining discussion (potential blind spot)
- There are open actions but no recent follow-up (stalled execution)
- There is active discussion but no decisions (decision latency)
- Stakeholder sentiment is shifting on this topic

---

## Step 5: Identify Gaps and Blind Spots

Look for topics that SHOULD be discussed but are not:

1. **Expected topics from workstream status**: Read `context/workstreams.md`. Are there active workstreams or initiatives that have not been discussed recently?
2. **Open threads**: Read `context/open_threads.md`. Are there unresolved threads that have gone quiet?
3. **Previous week's concerns**: Read the most recent weekly summary. Were any "Emerging Risks" or "Carried Forward" items not addressed in subsequent meetings?
4. **Seasonal or deadline-driven topics**: Are there upcoming deadlines or milestones that should be generating discussion but are not?

---

## Step 6: Update Topic Evolution Tracker

Append new entries to `analysis/trackers/topic_evolution.md` for any topics not already tracked. Update existing entries if new data changes their trend classification.

Format for new entries:
```
| [date] | [topic] | [category] | [intensity] | [first_raised] | [meetings_count] | [trend] | "[key_quote]" | [confidence] |
```

---

## Step 7: Generate Report

Write the report to `analysis/insights/YYYY-MM-DD_-_topic-evolution.md`:

```markdown
# Topic Evolution Report -- [Date]
**Period analysed:** [start date] to [end date]
**Summaries analysed:** [count]
**Unique topics tracked:** [count]

## Key Findings
[3-5 bullet points summarising the most important topic trends and their implications for the programme]

## Rising Topics (increasing intensity or frequency)

### [Topic Name]
- **First raised:** [date]
- **Meetings:** [count]
- **Trend:** RISING
- **Recent intensity:** [score] (historical avg: [score])
- **Trajectory:** [ASCII sparkline]
- **Key stakeholders:** [names]
- **Project:** [project name or _general]
- **Summary:** [2-3 sentences explaining why this topic is rising, what is driving it, and what it means]
- **Related decisions:** [any pending or recent decisions]
- **Related risks:** [any associated risks]

[Repeat for each rising topic, sorted by recent intensity descending]

## Declining Topics (decreasing mention or intensity)

### [Topic Name]
- **First raised:** [date]
- **Last mentioned:** [date]
- **Meetings:** [count]
- **Trend:** DECLINING
- **Recent intensity:** [score] (historical avg: [score])
- **Trajectory:** [ASCII sparkline]
- **Summary:** [2-3 sentences explaining why this topic is declining and whether that is appropriate or concerning]
- **Concern level:** [Should this still be discussed? Is it resolved or being ignored?]

[Repeat for each declining topic]

## Going Cold (not mentioned in 2+ weeks despite prior activity)

### [Topic Name]
- **First raised:** [date]
- **Last mentioned:** [date] ([N] days ago)
- **Previous intensity:** [score]
- **Open items:** [any unresolved actions, decisions, or risks related to this topic]
- **Assessment:** [Is this resolved, forgotten, or being avoided?]

[Repeat for each going-cold topic]

## Stable Topics (consistent presence)

| Topic | Meetings | Avg Intensity | Category | Key Stakeholders |
|-------|----------|---------------|----------|------------------|
| ... | ... | ... | ... | ... |

## New Topics (first appeared in last 2 weeks)

### [Topic Name]
- **First raised:** [date]
- **Intensity:** [score]
- **Category:** [category]
- **Key stakeholders:** [names]
- **Summary:** [what this topic is about and why it emerged]
- **Watch level:** [Should we expect this to grow? Is it a one-off or the start of a trend?]

## Blind Spots and Gaps

### Topics That Should Be Discussed But Are Not
| Topic | Last Mentioned | Why It Matters | Related Open Items |
|-------|---------------|----------------|-------------------|
| ... | ... | ... | ... |

### Stalled Execution Topics
[Topics with open actions but no recent discussion or follow-up]

### Decision Latency Topics
[Topics discussed 3+ times without reaching a decision]

## Topic Relationship Map

[Identify clusters of related topics and how they interact. For example, "CLARA adoption" connects to "data quality", "CSM engagement", and "token costs". Draw the relationships:]

- [Topic A] <-> [Topic B]: [relationship description]
- [Topic B] -> [Topic C]: [one-directional dependency]

## Recommendations

1. [Recommendation based on topic analysis, e.g., "Schedule a dedicated session on [going-cold topic] -- it has 3 open actions and an escalating risk"]
2. [Second recommendation]
3. [Third recommendation]
```

---

## Step 8: Trigger Import (if tracker was updated)

If `analysis/trackers/topic_evolution.md` was modified:

```bash
cd backend && python -m scripts.import_data --data-root .. --db-url "$DATABASE_URL"
```

Report completion with summary statistics.
