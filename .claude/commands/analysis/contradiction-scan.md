---
description: Scan across all meeting summaries to detect contradictions, reversals, and information gaps
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent
argument-hint: [period|person-name|all]
---

# Contradiction & Gap Scanner

Scan across all meeting summaries to detect contradictions, position reversals, dropped topics, and information gaps. Produces a structured report of inconsistencies that may require attention.

## Arguments
$ARGUMENTS -- Options:
- empty or `all`: full scan across all available summaries
- `last N weeks`: scan the last N weeks only
- `[person-name]`: deep-dive into a specific person's position consistency

---

## Step 1: Load Data

Read these files in parallel:

1. `analysis/trackers/contradictions.md` -- existing contradiction and gap entries
2. `context/decisions.md` -- decision log for tracking reversals
3. `context/open_threads.md` -- unresolved threads for tracking dropped topics
4. `context/stakeholders.md` -- stakeholder context for understanding positions
5. `analysis/trackers/action_items.md` -- actions to check for follow-through gaps
6. `analysis/trackers/commitments.md` -- commitments to check for broken promises
7. `analysis/trackers/sentiment_tracker.md` -- sentiment history for detecting attitude shifts

---

## Step 2: Build Position History

Read ALL summaries from `analysis/summaries/` in chronological order.

**Context window strategy for large sets:**
Since this analysis needs ALL summaries to detect cross-meeting contradictions, process in chronological batches:

1. **Build compressed per-person statement history** -- For each person, maintain a rolling record of their stated positions. Structure:
   ```
   {
     "person_name": {
       "topic_1": [
         { "date": "YYYY-MM-DD", "position": "summary of stated position", "quote": "exact quote if available", "meeting": "meeting title" },
         ...last 5 positions per topic...
       ]
     }
   }
   ```

2. **Process in batches of 10 summaries** (chronologically). After each batch:
   - Check for contradictions within the batch AND against the accumulated history
   - Compress the history: keep only the last 5 positions per topic per person
   - Carry forward to the next batch

3. If a contradiction is detected that needs deeper verification (e.g., the earlier statement is from a batch already processed), note it for targeted re-reading in Step 4.

---

## Step 3: Detect Contradictions

For each person in the position history, compare their statements across meetings. A contradiction exists when:

### Types of Contradictions

1. **Reversal** -- Complete flip on a position:
   - Person said X at time T1, then said not-X at time T2
   - Example: "We should keep Sales Recon standalone" -> "We should integrate Sales Recon into the platform"
   - Severity: HIGH if the decision had consequences, MEDIUM if still under discussion

2. **Softening** -- Hedging or walking back a firm position:
   - Person stated X firmly at T1, then at T2 used qualifiers ("maybe", "it depends", "I'm less sure")
   - Example: "We will launch by March 21" -> "We're aiming for March 21 but it depends on..."
   - Severity: MEDIUM (may indicate growing uncertainty or political pressure)

3. **Escalation** -- Strengthening a previously tentative position:
   - Person suggested X tentatively at T1, then stated it firmly at T2
   - Example: "We might want to consider..." -> "We absolutely need to..."
   - Severity: LOW (usually positive -- indicates growing conviction)

4. **Inconsistency** -- Saying different things to different groups:
   - Person told Group A one thing and Group B another thing on the same topic
   - Example: telling technical team "timeline is flexible" while telling leadership "we're on track for March 21"
   - Severity: HIGH (potential trust/communication issue)

5. **Silent reversal** -- A decision was made but later ignored or quietly overridden:
   - Decision D was logged at T1, but by T2 the opposite approach is being followed without acknowledgment
   - Example: "Decided to use Azure" -> later discussions assume AWS with no reversal discussion
   - Severity: HIGH (decision integrity issue)

### Detection Rules

For each pair of positions on the same topic by the same person:
- Compute semantic similarity. If the positions point in opposite directions (e.g., for/against, do/don't, now/later), flag as potential contradiction.
- Check temporal distance. Contradictions closer in time are more concerning (less likely to be legitimate evolution).
- Check if the change was acknowledged. If the person explicitly said "I've changed my mind because..." then it is NOT a contradiction -- it is a stated position evolution. Note it as such.
- Check if there was new information between the two positions that would justify the change.

Assign confidence to each detected contradiction:
- **HIGH**: clear opposing statements with quotes, no acknowledged change, short time gap
- **MEDIUM**: partially opposing statements, or long time gap where evolution is plausible
- **LOW**: ambiguous wording, uncertain attribution, or context may explain the difference

---

## Step 4: Detect Information Gaps

### Action Item Follow-Through Gaps

Read `analysis/trackers/action_items.md`. For each open action item:
1. When was it created?
2. Was it mentioned in any subsequent meeting summaries?
3. If not mentioned for 2+ weeks and still open: flag as **stalled action**
4. If it had a deadline that passed without update: flag as **missed deadline**

### Commitment Follow-Through Gaps

Read `analysis/trackers/commitments.md`. For each commitment:
1. Was the commitment fulfilled?
2. Was it discussed in a subsequent meeting?
3. If the implied deadline passed without follow-up: flag as **broken commitment**

### Topic Disappearance Gaps

From the position history built in Step 2:
1. Identify topics discussed in 2+ meetings that then disappeared entirely
2. Check if the topic was resolved (decision made, thread closed) or just dropped
3. If dropped without resolution: flag as **abandoned topic**
4. Cross-reference with `context/open_threads.md` -- is there a matching open thread?

### Expected Topics Not Discussed

For the most recent period (last 2 weeks):
1. Read the previous weekly summary's "Emerging Risks" and "Carried Forward" sections
2. Check if each item was addressed in subsequent meetings
3. If not addressed: flag as **unaddressed carry-forward**

### Stakeholder Absence Gaps

From meeting attendance across summaries:
1. Identify stakeholders who were regularly present but have stopped attending
2. Check if their absence was noted or explained
3. If unexplained and the person is relevant: flag as **stakeholder dropout**

---

## Step 5: Verify Findings

For each detected contradiction or gap:

1. If the supporting evidence is from a summary (not direct transcript quotes), try to verify against the original transcript if available
2. Check against existing entries in `analysis/trackers/contradictions.md` -- do not duplicate
3. For LOW confidence items, check if there is additional context that would explain the apparent contradiction
4. Remove false positives:
   - Legitimate evolution of positions (explicitly acknowledged)
   - Different contexts (person may hold different positions on subtopics within a broader topic)
   - Paraphrasing artifacts (summary may have simplified a nuanced position)

---

## Step 6: Update Trackers

Append new entries to `analysis/trackers/contradictions.md`:

**Contradictions table:**
```
| [today's date] | [type] | [person] | [statement A] | [date A] | [statement B] | [date B] | [severity] | [resolution: open/acknowledged/resolved] | [confidence] |
```

**Information Gaps table:**
```
| [today's date] | [gap description] | [expected source] | [last mentioned date] | [meetings absent count] | [severity] |
```

Update `context/open_threads.md`:
- Mark threads as CLOSED if evidence shows they were resolved but not formally closed
- Add new threads for significant abandoned topics that need attention

---

## Step 7: Generate Report

Write the report to `analysis/insights/YYYY-MM-DD_-_contradiction-scan.md`:

```markdown
# Contradiction & Gap Scan Report -- [Date]
**Period analysed:** [start date] to [end date]
**Summaries scanned:** [count]
**Stakeholders tracked:** [count]

## Summary Statistics
- **Contradictions detected:** [count] (N new, M previously known)
  - Reversals: N
  - Softening: N
  - Escalations: N
  - Inconsistencies: N
  - Silent reversals: N
- **Information gaps detected:** [count]
  - Stalled actions: N
  - Missed deadlines: N
  - Broken commitments: N
  - Abandoned topics: N
  - Unaddressed carry-forwards: N
  - Stakeholder dropouts: N
- **Confidence distribution:** HIGH: N, MEDIUM: N, LOW: N

## Critical Findings (HIGH severity)

### [Finding Title]
- **Type:** [reversal/inconsistency/silent_reversal/etc.]
- **Person:** [name]
- **Statement A:** "[quote or paraphrase]" -- [date], [meeting title]
- **Statement B:** "[quote or paraphrase]" -- [date], [meeting title]
- **Severity:** HIGH
- **Confidence:** [HIGH/MEDIUM/LOW]
- **Context:** [Why this matters. What are the implications? Who is affected?]
- **Recommended action:** [What should be done -- e.g., "Clarify position in next standup"]

[Repeat for each HIGH severity finding]

## Moderate Findings (MEDIUM severity)

### [Finding Title]
- **Type:** [type]
- **Details:** [brief description with dates and evidence]
- **Assessment:** [Is this concerning or expected? What should be watched?]

[Repeat for each MEDIUM finding]

## Position Evolution (not contradictions)

These are legitimate position changes that were explicitly acknowledged:

| Person | Topic | Old Position | New Position | Date of Change | Reason Given |
|--------|-------|-------------|-------------|----------------|-------------|
| ... | ... | ... | ... | ... | ... |

[Important to distinguish these from contradictions -- natural evolution is healthy.]

## Information Gaps

### Stalled Actions
| Action | Owner | Created | Last Mentioned | Days Stalled | Original Context |
|--------|-------|---------|----------------|-------------|-----------------|
| ... | ... | ... | ... | ... | ... |

### Missed Deadlines
| Commitment | Person | Deadline | Last Update | Status |
|------------|--------|----------|-------------|--------|
| ... | ... | ... | ... | ... |

### Abandoned Topics
| Topic | Last Discussed | Meetings Since | Was It Resolved? | Risk Level |
|-------|---------------|----------------|-----------------|------------|
| ... | ... | ... | No | HIGH/MEDIUM/LOW |

### Unaddressed Carry-Forwards
| Item | Raised In | Weeks Unaddressed | Current Status |
|------|----------|-------------------|---------------|
| ... | week-of-YYYY-MM-DD | N | [still open / partially addressed / ignored] |

### Stakeholder Dropouts
| Person | Last Meeting | Expected Involvement | Explanation Given | Concern Level |
|--------|-------------|---------------------|-------------------|---------------|
| ... | ... | ... | [none / partial / explained] | HIGH/MEDIUM/LOW |

## Pattern Analysis

### People with Most Position Changes
| Person | Total Changes | Contradictions | Evolutions | Net Direction |
|--------|--------------|----------------|------------|---------------|
| ... | ... | ... | ... | [becoming more cautious / more decisive / etc.] |

### Topics with Most Inconsistency
| Topic | Contradictions | Gaps | Open Threads | Assessment |
|-------|---------------|------|--------------|------------|
| ... | ... | ... | ... | [chaotic / evolving / neglected] |

### Decision Integrity Score
[What percentage of logged decisions are still being followed? How many were silently reversed?]
- Decisions logged: N
- Still active: N
- Explicitly revised: N
- Silently reversed: N
- Integrity score: [percentage]

## Recommendations

1. **[Urgent recommendation]** -- [rationale and specific action]
2. **[Important recommendation]** -- [rationale]
3. **[Monitoring recommendation]** -- [what to watch going forward]

[Focus recommendations on HIGH severity items and patterns, not individual LOW severity findings.]
```

---

## Step 8: Trigger Import (if trackers were updated)

If `analysis/trackers/contradictions.md` or `context/open_threads.md` was modified:

```bash
cd backend && python -m scripts.import_data --data-root .. --db-url "$DATABASE_URL"
```

Report completion with summary statistics.
