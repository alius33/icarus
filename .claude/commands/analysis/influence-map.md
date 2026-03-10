---
description: Generate a comprehensive stakeholder influence and relationship map
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent
argument-hint: [period|person-name|all]
---

# Stakeholder Influence Analysis

Generate a comprehensive stakeholder influence and relationship map based on meeting analysis. Tracks who drives decisions, who defers, who blocks, and how coalitions form and shift.

## Arguments
$ARGUMENTS -- Options:
- empty or `all`: full influence analysis across all available data
- `last N weeks`: analyse influence patterns from the last N weeks only
- `[person-name]`: deep-dive into a specific stakeholder's influence profile

---

## Step 1: Load Data

Read these files in parallel:

1. `analysis/trackers/influence_graph.md` -- existing influence signals and coalitions
2. `context/stakeholders.md` -- canonical stakeholder list with roles and known dynamics
3. `analysis/trackers/sentiment_tracker.md` -- sentiment trajectory for each person
4. `context/decisions.md` -- decision log (to identify who drove which decisions)
5. ALL recent summaries from `analysis/summaries/` (if `all`: read all; if time-bounded: filter by date in filename)

**Context window strategy:** If more than 25 summaries to process, batch into groups of 12. Carry forward a per-person influence state between batches.

---

## Step 2: Extract Influence Signals

For each summary, extract from the "Power Dynamics" table (if present), the "Decisions Made" section, and the "Stakeholder Signals" section:

For each person mentioned:

1. **Influence acts** -- Classify each observable act:
   - `proposal_adopted`: person proposed something that was accepted
   - `proposal_rejected`: person proposed something that was rejected or deferred
   - `deferred_to`: others explicitly deferred to this person's judgement
   - `challenged`: person challenged someone else's position
   - `blocked`: person blocked or vetoed a direction
   - `brokered`: person mediated between opposing positions
   - `redirected`: person redirected the conversation or reframed the problem
   - `delegated`: person assigned work to others
   - `escalated`: person escalated an issue to higher authority
   - `supported`: person actively backed someone else's proposal

2. **Meeting role** -- For each meeting, classify the person's role:
   - `driver`: set the agenda, drove outcomes
   - `supporter`: actively contributed, backed proposals
   - `observer`: present but mostly passive
   - `blocker`: opposed or slowed progress
   - `broker`: mediated, connected different viewpoints
   - `absent`: expected but not present

3. **Engagement level** -- Rough percentage of speaking time (estimate from transcript presence)

4. **Influence direction** -- Who was the target of the influence act (if identifiable)

---

## Step 3: Compute Influence Scores

For each stakeholder, compute:

### Raw Influence Score (0-100)

Weighted sum of influence acts:
- `proposal_adopted`: +10 points each
- `deferred_to`: +8 points each
- `delegated`: +6 points each
- `brokered`: +7 points each
- `redirected`: +5 points each
- `challenged`: +4 points each (shows engagement and standing)
- `escalated`: +3 points each
- `supported`: +2 points each
- `blocked`: +6 points each (shows veto power)
- `proposal_rejected`: -2 points each
- `observer` role: -1 per meeting (too passive reduces score)

Normalise to 0-100 scale based on the highest scorer.

### Influence Type Profile

Classify each person's PRIMARY influence style based on their most common acts:
- **Decisive**: mostly `proposal_adopted`, `delegated` -- they decide and direct
- **Consultative**: mostly `deferred_to`, `brokered` -- others seek their input
- **Challenging**: mostly `challenged`, `blocked` -- they push back and gatekeep
- **Supportive**: mostly `supported`, `brokered` -- they build consensus
- **Passive**: mostly `observer` role -- they attend but do not actively influence

### Influence Trajectory

Compare current period (last 2 weeks) vs. previous period:
- **RISING**: score increased by 10+ points, or more frequent `proposal_adopted` / `deferred_to`
- **STABLE**: score within 10 points of previous period
- **DECLINING**: score decreased by 10+ points, or shift toward `observer` role
- **EMERGING**: person newly active (first 2 weeks of meaningful participation)
- **FADING**: person becoming less active, fewer meetings attended

---

## Step 4: Map Relationships

For each pair of stakeholders who appeared in 2+ meetings together:

1. **Interaction frequency**: how many meetings did they both attend?
2. **Interaction type**: classify the dominant pattern:
   - `aligned`: they tend to support each other's positions
   - `opposing`: they tend to challenge or block each other
   - `hierarchical`: one consistently defers to or delegates to the other
   - `collaborative`: they work together on specific topics
   - `independent`: they co-attend but rarely interact directly
3. **Strength**: 1-5 based on frequency and intensity of interactions
4. **Key topic**: what do they most often interact about?
5. **Direction**: is the influence primarily one-directional or mutual?

---

## Step 5: Detect Coalitions

Identify groups of stakeholders who consistently align:

1. Look for 3+ people who frequently appear on the same side of discussions
2. Check for patterns: do they support each other's proposals? Do they share sentiment on key topics?
3. Classify each coalition:
   - **Name**: descriptive label (e.g., "Technical Leadership", "CSM Advocates", "Governance Push")
   - **Members**: list of members
   - **Core issue**: what unites them
   - **Opposing coalition**: if there is one, who are they opposed to?
   - **Stability**: STABLE (consistent membership), FORMING (new), FRACTURING (showing internal disagreement), DISSOLVED (no longer active)

Compare against existing coalitions in `analysis/trackers/influence_graph.md` Coalitions table. Note new coalitions, changed coalitions, and dissolved coalitions.

---

## Step 6: Power Shift Analysis

Look for significant changes in the influence landscape:

1. **Role changes**: Did anyone move from observer to driver? From supporter to blocker?
2. **Authority shifts**: Did decision-making authority shift between people?
3. **New entrants**: Who entered the programme's conversations for the first time?
4. **Departures**: Who stopped attending meetings or became notably quieter?
5. **Gatekeepers**: Who controls access to key resources, decisions, or stakeholders?
6. **Bridges**: Who connects otherwise disconnected groups?
7. **Informal authority**: Who has influence beyond their formal role?

---

## Step 7: Update Trackers

Update `analysis/trackers/influence_graph.md`:

**Influence Signals table:** Append new entries for signals not already tracked:
```
| [date] | [person] | [influence_type] | [direction] | [target_person] | [topic] | [evidence] | [strength] | [confidence] |
```

**Coalitions table:** Append new coalitions or update existing ones:
```
| [date] | [coalition_name] | [members] | [issue] | [alignment] |
```

Update `context/stakeholders.md` if:
- A stakeholder's effective role has shifted beyond their formal title
- New relationship dynamics were identified that were not previously documented
- A stakeholder's engagement level changed significantly

---

## Step 8: Generate Report

Write the report to `analysis/insights/YYYY-MM-DD_-_influence-analysis.md`:

```markdown
# Stakeholder Influence Report -- [Date]
**Period analysed:** [start date] to [end date]
**Meetings analysed:** [count]
**Stakeholders tracked:** [count]

## Key Findings
[3-5 bullet points summarising the most important influence dynamics and shifts]

## Influence Rankings

| Rank | Person | Score | Primary Type | Trajectory | Meetings | Key Acts |
|------|--------|-------|-------------|------------|----------|----------|
| 1 | [name] | [score] | Decisive | RISING | [N] | [top 2-3 acts] |
| 2 | ... | ... | ... | ... | ... | ... |

## Influence Profiles

### [Person Name] (Rank #N)
- **Score:** [score]/100
- **Type:** [Decisive/Consultative/Challenging/Supportive/Passive]
- **Trajectory:** [RISING/STABLE/DECLINING/EMERGING/FADING]
- **Meetings attended:** [N] of [total]
- **Top influence acts:** [list top 3 acts with dates]
- **Key relationships:** [who they most frequently interact with, and how]
- **Coalitions:** [which coalitions they belong to]
- **Sentiment trajectory:** [from sentiment tracker -- champion/supportive/neutral/etc.]
- **Assessment:** [2-3 sentences on this person's current influence posture, what drives it, and what to watch]

[Repeat for top 8-10 stakeholders, ordered by score]

## Key Relationships

### Strong Alignments
| Person A | Person B | Type | Strength | Key Topic | Evidence |
|----------|----------|------|----------|-----------|----------|
| ... | ... | aligned | 4/5 | ... | "[short quote or reference]" |

### Notable Tensions
| Person A | Person B | Type | Strength | Key Topic | Evidence |
|----------|----------|------|----------|-----------|----------|
| ... | ... | opposing | 3/5 | ... | "[short quote or reference]" |

### Hierarchical Dynamics
| Superior | Subordinate | Dynamic | Notes |
|----------|------------|---------|-------|
| ... | ... | [formal hierarchy / informal deference] | ... |

## Active Coalitions

### [Coalition Name]
- **Members:** [list]
- **Core issue:** [what unites them]
- **Status:** STABLE / FORMING / FRACTURING / DISSOLVED
- **Opposing group:** [if any]
- **Recent activity:** [what happened this period]

[Repeat for each coalition]

## Power Shifts This Period

### [Shift Description]
- **Who:** [person or group]
- **What changed:** [description of the shift]
- **Evidence:** [specific meetings, decisions, or acts that demonstrate the shift]
- **Implications:** [what this means for the programme]

[Repeat for each notable shift]

## Gatekeepers and Bridges
- **Gatekeepers** (control access to key resources/decisions):
  - [Person]: controls [what]. Evidence: [brief].
- **Bridges** (connect otherwise disconnected groups):
  - [Person]: connects [Group A] and [Group B]. Evidence: [brief].

## Absent or Silent Stakeholders
[People who should be more engaged based on their role but are not. Why might they be disengaged? Is this a risk?]

| Person | Expected Role | Actual Engagement | Last Active Meeting | Concern Level |
|--------|--------------|-------------------|--------------------|-----------|
| ... | ... | ... | ... | HIGH/MEDIUM/LOW |

## Recommendations

1. **[Recommendation]** -- [rationale based on influence analysis]
2. **[Recommendation]** -- [rationale]
3. **[Recommendation]** -- [rationale]

[Recommendations should be actionable: who should talk to whom, which relationships need attention, which coalitions should be leveraged or managed]
```

---

## Step 9: Trigger Import (if trackers were updated)

If `analysis/trackers/influence_graph.md` or `context/stakeholders.md` was modified:

```bash
cd backend && python -m scripts.import_data --data-root .. --db-url "$DATABASE_URL"
```

Report completion with summary statistics.
