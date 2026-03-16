---
description: Run the full 11-agent deep analysis pipeline on new or specified transcripts
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent
argument-hint: [date|--all|empty for new only]
---

# Deep Analyse Transcripts (Multi-Agent Engine)

Run the full 11-agent analysis swarm on new or specified transcripts. Produces enhanced summaries with structured extraction tables, per-project mini-summaries, and populates all tracker files.

## Arguments
$ARGUMENTS — Options:
- empty: process all new (unsummarised) transcripts
- `YYYY-MM-DD`: process transcripts from a specific date only
- `--all`: re-analyse ALL transcripts (full backfill, overwrites existing summaries)

---

## Step 0: Detect New Transcripts

Compare `Transcripts/*.txt` filenames against `analysis/summaries/*.md`. A transcript is "new" if no matching summary exists.

Normalisation rules:
- `DD-MM-YYYY_-_Title.txt` becomes `YYYY-MM-DD_-_Title`
- `YYYY-MM-DD_-_Title.txt` stays as-is
- `YYYY-MM-DD_HH-MM-SS.txt` extracts the date portion `YYYY-MM-DD_HH-MM-SS`
- Spaces in filenames are treated as equivalent to underscores for matching
- Strip `.txt` extension, then check if `analysis/summaries/{normalised_stem}.md` exists

If `--all` flag: ignore existing summaries, process every transcript in `Transcripts/`.
If a specific date (e.g. `2026-03-06`): only process transcripts whose normalised date matches.
If no arguments: process only new (unmatched) transcripts.

If there are no transcripts to process, report "No new transcripts found." and stop.

Report: "Found N transcript(s) to process: [list filenames]"

---

## Step 1: Load Context

Read ALL of these files into memory before any analysis begins. Read them in parallel:

**Core context:**
1. `context/glossary.md` -- names, acronyms, systems, jargon
2. `context/stakeholders.md` -- who matters, roles, dynamics
3. All files in `context/projects/` -- per-project context and status

**Continuity:**
4. The most recent file in `analysis/weekly/` (sort by filename descending, take first) -- last weekly summary for narrative continuity

**Tracker state (all current tracker files):**
5. `analysis/trackers/action_items.md`
6. `analysis/trackers/sentiment_tracker.md` (create if missing with header: `# Sentiment Tracker\n\n| Date | Person | Sentiment | Shift | Topic | Meeting | Quote | Confidence |\n|------|--------|-----------|-------|-------|---------|-------|------------|`)
7. `analysis/trackers/commitments.md` (create if missing with header: `# Commitments Tracker\n\n| Date | Person | Commitment | Implied_Deadline | Condition | Status | Meeting | Confidence |\n|------|--------|------------|-----------------|-----------|--------|---------|------------|`)
8. `analysis/trackers/topic_evolution.md`
9. `analysis/trackers/influence_graph.md`
10. `analysis/trackers/contradictions.md`
11. `analysis/trackers/meeting_scores.md`
12. `analysis/trackers/risk_register.md`

**Projects:**
13. Read all project data. Try `GET /api/projects` if backend is running, otherwise scan `analysis/projects/` directories. When running without a local backend (e.g., Railway-deployed workflow), project data is loaded from filesystem only — this is fine. For each project, need: name, slug, description, keywords, key stakeholders. Store as a lookup table for project segmentation.
14. Current programme wins: `GET /api/wins` (if backend running) — needed to avoid creating duplicate wins
15. Current outreach contacts: `GET /api/outreach` (if backend running) — needed to update existing contacts vs create new ones

If any tracker files are missing, create them with empty table headers as shown above.

---

## Step 2: Speaker Identification (Pre-processing)

For each transcript to process, scan the content for unidentified speaker patterns:
- `Speaker 1:`, `Speaker 2:`, etc.
- `Unknown Speaker:`, `Unknown:`, `Unidentified:`

If unidentified speakers are found:

```bash
cd backend && python -m scripts.speaker_id.runner --analyze --file "{transcript_path}" --output /tmp/speaker_id_mapping.json --report /tmp/speaker_id_review.md
```

Read the review report. If identifications have confidence > 0.7:

```bash
cd backend && python -m scripts.speaker_id.runner --apply --mapping-file /tmp/speaker_id_mapping.json --threshold 0.7
```

Re-read the transcript after speaker identification is applied.

If all speakers are already identified (named individuals like "Richard:", "Diya:", etc.), skip this step.

If the speaker identification scripts are not available, skip this step and note it in the final report.

---

## Step 3: Standard Summarisation

For each transcript, read the full `.txt` file and generate a comprehensive summary.

**Parallelisation strategy:** If more than 3 transcripts, split into two batches. Use Agent tool to spawn two parallel summarisation agents (Agent A and Agent B), each processing half the batch. If 3 or fewer, process sequentially.

### Enhanced Summary Template

Create `analysis/summaries/YYYY-MM-DD_-_Title.md` for each transcript:

```markdown
# [Meeting Title]
**Date:** YYYY-MM-DD
**Attendees:** [names mentioned or identified in transcript]
**Duration context:** [short/medium/long — short: <2000 words, medium: 2000-5000, long: >5000]
**Primary project:** [name of the primary project this transcript relates to]
**Secondary projects:** [list of other projects touched, if any]

## Key Points
- [Bullet points -- what was discussed, decided, revealed]
- [Be specific: "CSMs entering blocker data that disappears on refresh" not "data quality issues"]

## Projects Discussed
| Project | Relevance | Key Points |
|---------|-----------|------------|
| [project name or _unassigned] | HIGH/MEDIUM/LOW | [1-2 sentence summary of what was said about this project] |

## Decisions Made
- [Decision]: [rationale if given] -> [owner if identified]
  - **Type:** explicit / implicit / deferred / non-decision
  - **Confidence:** HIGH / MEDIUM / LOW

## Action Items
| Action | Owner | Deadline | Status | Project | Confidence |
|--------|-------|----------|--------|---------|------------|
| [specific action] | [name] | [date or "unspecified"] | Open | [project slug or _general] | HIGH/MEDIUM/LOW |

## Theme Segments
| Topic | Category | Project | Key Quote | Confidence |
|-------|----------|---------|-----------|------------|
| [topic name] | technical/strategic/interpersonal/operational/governance | [project slug or _general] | "[short quote]" | HIGH/MEDIUM/LOW |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| [name] | driver/supporter/observer/blocker/broker | [proposal_adopted, deferred_to, challenged, redirected, etc.] | [rough % of speaking time] |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| [name] | champion/supportive/neutral/cautious/frustrated/resistant/disengaged | UP/DOWN/STABLE/NEW | [topic] | "[short quote]" |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| [name] | [what they committed to] | [parsed deadline or "unspecified"] | [any conditions stated] | HIGH/MEDIUM/LOW |

## Information Flow
| Topic | Previously Discussed | Previous Group | Current Awareness | Gap Severity |
|-------|---------------------|----------------|-------------------|--------------|
| [topic] | [date or "first mention"] | [who was there before] | aware/partial/unaware | HIGH/MEDIUM/LOW/NONE |

## Meeting Effectiveness
- **Type:** decision_making / status_update / brainstorming / escalation / planning / review / onboarding
- **Overall Score:** [0-100]
- **Decision Velocity:** [0.0-1.0] -- decisions made relative to topics discussed
- **Action Clarity:** [0.0-1.0] -- % of actions with clear owner + deadline
- **Engagement Balance:** [0.0-1.0] -- how evenly distributed was participation
- **Topic Completion:** [0.0-1.0] -- % of topics reaching conclusion
- **Follow Through:** [0.0-1.0] -- % of previous actions addressed (check action_items.md)
- **Recommendation:** [pattern-based suggestion if applicable]

## Contradictions Detected
| Person | Previous Position | Date | Current Position | Severity | Confidence |
|--------|-------------------|------|------------------|----------|------------|
(Leave empty if none detected. Compare against previous summaries and tracker files loaded in Step 1.)

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-XXX or NEW | new/update | [short title] | CRITICAL/HIGH/MEDIUM/LOW | escalating/stable/de-escalating | explicit/implicit/absence_inferred | HIGH/MEDIUM/LOW |

## Programme Wins Detected
| Category | Title | Description | Before State | After State | Project | Confidence |
|----------|-------|-------------|--------------|-------------|---------|------------|
| time_saved/adoption/quality/reach/process_improvement | [short title] | [what was achieved] | [how it was before] | [how it is now] | [project slug] | HIGH/MEDIUM/LOW |

(Extract: milestone completions, "we shipped X", "X is now live", time/effort savings mentioned with numbers, adoption figures, process changes. Only include concrete achievements, not aspirations. Leave empty if none.)

## Outreach Signals
| Contact | Role | Division | Signal Type | Detail | Interest Level |
|---------|------|----------|-------------|--------|----------------|
| [name] | [role] | [division] | new_contact/status_change/meeting/next_step | [what happened] | 1-5 |

(Extract: new people from other divisions mentioned for the first time, existing contacts with engagement changes, meetings scheduled/held with cross-divisional stakeholders, next steps agreed for outreach. Leave empty if none.)

## Open Questions Raised
- [Questions that came up but were not resolved in the meeting]

## Raw Quotes of Note
- "[Exact quote]" -- [Speaker], on [topic]

## Narrative Notes
[1-2 paragraphs of cross-cutting observations. Connect the dots that structured tables cannot capture. Story arc updates for issues that progressed or regressed. Stakeholder arc shifts. Programme momentum signals. Tensions worth watching.]
```

**Analysis guidelines for summarisation:**
- Be specific. Track sentiment, not just facts.
- Note contradictions against historical positions (use loaded tracker data).
- Distinguish what was decided from what was discussed.
- Quote sparingly but well -- one good quote is better than five mediocre ones.
- If a transcript is ambiguous about a point, say so rather than guessing.
- Never fabricate information. Never merge transcripts.

---

## Step 4: Project Segmentation

For each transcript analysed, determine which existing projects (loaded in Step 1) are discussed.

Matching criteria (check in order):
1. Is the project name explicitly mentioned in the transcript?
2. Are the project's keywords mentioned?
3. Are project-specific stakeholders present AND discussing project-relevant topics?
4. Are related projects discussed in a way that connects to this project?

For each match, assign relevance:
- **HIGH**: project was a primary discussion topic (multiple exchanges, decisions made)
- **MEDIUM**: project received significant discussion (dedicated segment, actions raised)
- **LOW**: project was briefly mentioned or tangentially referenced

Output a mapping for each transcript:
```json
{
  "transcript_file": "YYYY-MM-DD_-_Title.txt",
  "projects": {
    "project-slug-1": { "relevance": "HIGH", "sections": ["topic1", "topic2"], "quotes": ["..."] },
    "project-slug-2": { "relevance": "LOW", "sections": ["topic3"], "quotes": [] }
  },
  "unassigned_topics": ["topic that matched no project"]
}
```

Tag unmatched content as `_unassigned`. If a topic could belong to a project but the match is uncertain, include it with a note: `[UNCERTAIN_MATCH]`.

---

## Step 5: Deep Analysis Swarm

Spawn 4 analysis agents IN PARALLEL using Agent tool. Each agent receives:
- The full transcript text
- The project segmentation map from Step 4
- All context files from Step 1
- All current tracker file contents from Step 1

### Agent A: Theme-Sentiment-Influence Analyst

**Mission:** Extract topics, sentiment signals, influence dynamics, and information flow patterns.

**Outputs:**

1. **Topics** -- For each topic discussed:
   - Topic name, category (technical/strategic/interpersonal/operational/governance)
   - Intensity (1-5 scale), project slug
   - Whether this is first appearance or recurrence (check topic_evolution.md)
   - Key quote
   - Confidence level
   - Append new entries to `analysis/trackers/topic_evolution.md`

2. **Sentiment signals** -- For each speaker:
   - Current sentiment (champion/supportive/neutral/cautious/frustrated/resistant/disengaged)
   - Shift direction vs last known state (check sentiment_tracker.md)
   - Topic triggering the sentiment
   - Supporting quote
   - Confidence level
   - Append to `analysis/trackers/sentiment_tracker.md`

3. **Influence signals** -- For each notable influence act:
   - Person, influence type (propose/decide/defer/block/broker/redirect)
   - Direction and target person
   - Topic, evidence quote, strength (1-5)
   - Confidence level
   - Append to `analysis/trackers/influence_graph.md` Influence Signals table

4. **Coalition observations** -- Detected groupings:
   - Coalition name, members, issue, alignment type
   - Whether this is new or an update to existing coalition
   - Append to `analysis/trackers/influence_graph.md` Coalitions table

5. **Information flow gaps** -- Topics that appear to be siloed:
   - What was discussed, who knows, who should know but might not
   - Include in the summary's Information Flow table

6. **Outreach signals** -- Cross-divisional engagement updates:
   - New contacts: people from other divisions mentioned for the first time (not already in loaded outreach data from Step 1)
   - Status changes: existing contacts whose engagement level has visibly shifted (e.g., attended a demo = interested→engaged)
   - Meeting evidence: any cross-divisional meetings held or scheduled
   - Next steps: agreed follow-ups with cross-divisional contacts
   - For each signal: contact_name, contact_role, division, signal_type (new_contact/status_change/meeting/next_step), detail, suggested interest_level (1-5)
   - Populate the "Outreach Signals" table in the summary

### Agent B: Decision-Commitment-Action Analyst

**Mission:** Extract decisions at 4 levels, commitments with deadline parsing, and action items.

**Outputs:**

1. **Decisions** -- Classify each at one of 4 levels:
   - **Explicit**: clearly stated as a decision ("We've decided to...", "Let's go with...")
   - **Implicit**: emerged from discussion without formal declaration but treated as settled
   - **Deferred**: explicitly postponed ("Let's revisit this next week")
   - **Non-decision**: discussed but no resolution reached, left open
   - Include: decision text, type, owner, rationale, dissent, project slug, confidence
   - Append new decisions to `context/decisions.md` with date prefix

2. **Commitments** -- Personal pledges to do something:
   - Person, what they committed to, implied deadline (parse from language: "by Friday", "next week", "end of sprint")
   - Any conditions stated ("if we get the budget", "once X is resolved")
   - Project slug, confidence level
   - Append to `analysis/trackers/commitments.md`

3. **Action items** -- Both committed and implicit:
   - Committed: explicitly assigned ("John, can you do X?")
   - Implicit: implied by discussion ("Someone should look into...")
   - Include: action, owner, deadline, status (Open), project slug, confidence
   - Append new items to `analysis/trackers/action_items.md`
   - Check existing actions in action_items.md -- if a previously open action was addressed in this meeting, update its status

4. **Programme Wins** -- Concrete achievements or milestones:
   - Look for: shipped features, adoption numbers, time savings, process improvements, quality improvements, new reach/partnerships
   - Categories: time_saved (quantified time/effort reduction), adoption (usage numbers, migration targets), quality (improved outputs/processes), reach (new audiences, endorsements, cross-OU expansion), process_improvement (workflow changes, governance improvements)
   - Each win needs: category, title, description, before_state, after_state, project slug, confidence
   - Only log concrete achievements backed by evidence in the transcript — not plans or aspirations
   - Cross-reference loaded wins (from Step 1) to avoid duplicates — skip if a win with the same title already exists
   - Populate the "Programme Wins Detected" table in the summary

### Agent C: Risk-Contradiction-Gap Analyst

**Mission:** Detect risks, contradictions against historical positions, and information gaps.

**Outputs:**

1. **Risks** -- New risks and updates to existing:
   - Cross-reference `analysis/trackers/risk_register.md` by Risk_ID
   - For existing risks: update trajectory (escalating/stable/de-escalating), update last_reviewed date
   - For new risks: assign Risk_ID as `R-{next_number}`, set status=new
   - Include: title, description, category, severity, trajectory, source_type (explicit/implicit/absence_inferred), owner, mitigation, confidence
   - Source types: explicit (someone said "I'm worried about..."), implicit (the discussion implied a risk), absence_inferred (an expected topic was missing)
   - Update `analysis/trackers/risk_register.md`

2. **Contradictions** -- Compare current statements against historical positions:
   - Read all previous summaries and the contradictions tracker
   - For each person, check if their current stated position contradicts a prior one
   - Types: reversal (complete flip), softening (hedging), escalation (strengthening), inconsistency (saying different things to different groups)
   - Include: person, statement A with date, statement B with date, severity, resolution status, confidence
   - Only flag genuine contradictions, not natural evolution of positions
   - Append to `analysis/trackers/contradictions.md` Contradictions table

3. **Information gaps** -- Expected topics or follow-ups that were absent:
   - Check previous week's action items: were they addressed?
   - Check previous week's open questions: were they resolved?
   - Check for topics discussed last week that got zero mention this week
   - Include: gap description, expected source, last mentioned date, meetings absent, severity
   - Append to `analysis/trackers/contradictions.md` Information Gaps table

### Agent D: Meeting Effectiveness Scorer

**Mission:** Compute structured meeting effectiveness metrics.

**Outputs:**

1. **Meeting type classification** -- Categorise as:
   - decision_making, status_update, brainstorming, escalation, planning, review, onboarding
   - If mixed, pick the dominant type

2. **Five dimension scores** (each 0.0 to 1.0):
   - **Decision Velocity:** (decisions made + decisions deferred) / topics discussed. Higher = more decisive.
   - **Action Clarity:** % of action items that have both a clear owner AND a deadline. Higher = better.
   - **Engagement Balance:** 1 - Gini coefficient of speaking time distribution. 1.0 = perfectly balanced. 0.0 = one person monologue.
   - **Topic Completion:** % of topics that reached some conclusion (decision, action, or explicit deferral) vs topics left dangling.
   - **Follow Through:** Check action_items.md for items from previous meetings. % of previous items that were mentioned, addressed, or updated in this meeting.

3. **Overall score** (0-100): Weighted average:
   - Decision Velocity: 25%
   - Action Clarity: 20%
   - Engagement Balance: 20%
   - Topic Completion: 20%
   - Follow Through: 15%
   - Score = round(weighted_sum * 100)

4. **Pattern-based recommendations** -- Based on scores, suggest improvements:
   - Low decision velocity: "Consider using a decision framework or pre-circulating options"
   - Low action clarity: "End each topic by explicitly naming owner and deadline"
   - Low engagement: "Use round-robin or breakout format to increase participation"
   - Low topic completion: "Reduce agenda or time-box each topic"
   - Low follow through: "Start meetings with a review of previous action items"

5. Append entry to `analysis/trackers/meeting_scores.md`

---

## Step 6: Project Summary Writer

For each project identified in Step 4 (where relevance is MEDIUM or HIGH), generate a per-project summary.

Create the directory if needed:
```bash
mkdir -p "analysis/projects/{project_slug}/"
```

Create `analysis/projects/{project_slug}/YYYY-MM-DD_-_Title.md`:

```markdown
# [Project Name] -- Extract from [Meeting Title]
**Date:** YYYY-MM-DD
**Source transcript:** [transcript filename]
**Relevance:** HIGH/MEDIUM

## Discussion Summary
[2-5 paragraphs describing what was discussed about THIS project specifically. Include context, decisions being weighed, progress reported, blockers raised. Write as a narrative, not just bullet points.]

## Decisions (project-scoped)
- [Only decisions relevant to this project]
  - Type: [explicit/implicit/deferred/non-decision]

## Action Items (project-scoped)
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| [actions specific to this project] | ... | ... | Open |

## Risks & Concerns (project-scoped)
- [Risks specific to this project, with severity and trajectory]

## Stakeholder Signals (project-scoped)
- [Sentiment and positions about this project specifically]

## Key Quotes
- "[quote relevant to this project]" -- [Speaker]
```

Skip LOW relevance projects for per-project summaries (they are noted in the main summary's Projects Discussed table).

---

## Step 7: Self-Verification

For each transcript processed, spot-check the extracted analysis:

1. Pick 3 decisions or action items at random from Agent B's output
2. Pick 2 risk signals or contradictions from Agent C's output
3. For each picked item:
   - Search the transcript text for supporting evidence (a quote, a passage, a clear reference)
   - If the claim can be grounded in transcript text: PASS
   - If the claim cannot be grounded: mark with `[UNVERIFIED]` tag, set confidence=LOW, and add a note explaining what was expected vs what was found
4. Log all verification results for the final report

If more than 30% of spot-checked items fail verification, re-run the failing agent on that transcript with a note to be more conservative in extraction.

---

## Step 8: Coordinator Merge

Review all agent outputs holistically and reconcile:

1. **Deduplicate:** If Agent B and Agent C both identify the same item (e.g., a risk that is also an action), merge into one canonical entry. Keep the richer version.

2. **Cross-reference:** Link related items across agents:
   - A contradiction that creates a risk: add Risk_ID reference in the contradiction entry
   - A sentiment shift that explains a decision: note the connection in Narrative Notes
   - An influence act that resulted in a decision: cross-reference in both trackers

3. **Resolve conflicts:** If two agents give different assessments for the same data point:
   - Different sentiment for the same person: prefer the agent with the more specific supporting quote
   - Different confidence levels: prefer the lower confidence (be conservative)
   - Different project assignments: if ambiguous, tag with both project slugs

4. **Generate Narrative Notes:** Write the "Narrative Notes" section of each summary. This is the synthesis layer -- connect patterns across the structured tables. Address:
   - Story arc progress (what moved forward, what stalled)
   - Stakeholder trajectory changes
   - Programme momentum signals
   - Tensions worth watching that the tables alone do not convey

5. **Finalize summaries:** Incorporate all agent outputs into the summary files created in Step 3. Ensure all tables are populated from the correct agent outputs.

---

## Step 9: Update Context Files

Review the analysis outputs and update context files where changes occurred. Only modify files with actual updates. Add dates to all changes for traceability.

- **`context/decisions.md`** -- Append new decisions (from Agent B). Format: `- **[YYYY-MM-DD]** [Decision text] (Type: [type], Owner: [name])`
- **`context/open_threads.md`** -- Add new unresolved questions. Mark threads as CLOSED if the analysis found they were resolved (with date and resolution).
- **`context/stakeholders.md`** -- Update if:
  - A stakeholder's role changed
  - A notable attitude/sentiment shift was detected
  - New relationship dynamics emerged
  - A new stakeholder appeared for the first time
- **`context/projects/*.md`** -- Update relevant project context files if meaningful progress was reported

- **Programme Wins** (via API) -- For each win extracted by Agent B:
  - Check if a win with the same title exists in the loaded wins data (from Step 1). If so, skip.
  - `POST /api/wins` with: `{ "category": "...", "title": "...", "description": "...", "before_state": "...", "after_state": "...", "project": "...", "confidence": "estimated", "date_recorded": "YYYY-MM-DD", "notes": "Auto-extracted from: [transcript filename]" }`
  - If the backend is not running, list the wins in the final report and note they need manual entry.

- **Outreach contacts** (via API) -- For each outreach signal from Agent A:
  - If signal_type is `new_contact`: `POST /api/outreach` with contact details, `status="initial_contact"`, `first_contact_date` = transcript date
  - If signal_type is `status_change`, `meeting`, or `next_step` for an existing contact: `PATCH /api/outreach/{id}` with updated fields (`status`, `last_contact_date`, `meeting_count` increment, `next_step`, append to `notes`)
  - If the backend is not running, list the outreach updates in the final report.

---

## Step 10: Update Weekly Summaries

Determine which ISO weeks had transcripts processed. For each affected week:

1. Identify the Monday date for that ISO week
2. Read the PREVIOUS week's weekly summary (the file before this week's) for continuity
3. Read ALL summaries for this week (both existing and newly created)
4. Either create or update `analysis/weekly/week-of-YYYY-MM-DD.md` (Monday date)

If updating an existing weekly summary (because new transcripts were added to a week that already had some processed), regenerate the full summary incorporating ALL transcripts for that week.

### Enhanced Weekly Summary Template

```markdown
# Week of [date range, e.g. 3-7 March 2026]
**Transcripts processed:** [count]
**Previous week:** [one-line summary of where things stood]
**Programme Momentum:** ACCELERATING / STEADY / DECELERATING / STALLING

## Executive Summary
[2-3 paragraphs flowing from last week. Start with what moved forward, then what emerged as new, then what is concerning. Reference last week's state -- e.g. "The resource plan locked last week hit its first test when..." or "Richard's fatigue, noted last week, has escalated to..."]

## Headlines
- **[Bold key phrase]** -- [supporting detail]
- [3-5 most important developments, ranked by impact]

## Per-Project Progress
### [Project Name]
[What moved forward, what stalled, what is new for this project this week. Written in prose.]

### [Other active projects...]

## Key Decisions
[Decisions made this week. Include who, rationale, and any dissent. Reference decision type.]

## Meeting Effectiveness This Week
- Average score: [X]/100
- Best meeting: [title] ([score])
- Worst meeting: [title] ([score])
- Pattern observations: [recurring issues, improvements, trends]

## Emerging Risks / Concerns
[Each risk tagged with severity: CRITICAL / HIGH / MEDIUM / LOW. For risks carried from previous weeks, note trajectory: escalating / stable / de-escalating. Reference Risk_IDs where available.]

## Story Arc Updates
[Which ongoing issues progressed, escalated, or resolved this week. These are the multi-week narrative threads -- resource constraints, adoption friction, stakeholder relationships, scope debates.]

## Stakeholder Moves
[Notable shifts. Who leaned in, who pulled back, any new players, relationship dynamics that shifted. Reference sentiment tracker trajectory.]

## Information Flow Alerts
[Detected silos or awareness gaps from the Information Flow analysis. Who needs to know what they do not yet know.]

## Contradiction Highlights
[New contradictions or reversals detected this week. Reference specific statements if available.]

## Topic Momentum
- **Rising:** [topics with increasing frequency or intensity]
- **Stable:** [consistent themes]
- **Declining:** [topics losing attention]
- **Going cold:** [topics not mentioned in 2+ weeks that should be]

## Decision Latency Alerts
[Decisions that have been discussed for 3+ weeks without resolution. Pull from contradictions tracker and decision log.]

## Carried Forward from Last Week
- [Item 1] -- [progress or lack thereof]
- [Item 2] -- [progress or lack thereof]
- [3-5 live items from last week with updates]
```

---

## Step 11: Import & Report

### Trigger backend import

```bash
cd backend && python -m scripts.import_data --data-root .. --db-url "$DATABASE_URL"
```

If `$DATABASE_URL` is not set or the backend is unavailable, skip and tell the user: "Markdown files updated. Run the backend import to refresh the web app."

### Final Report

Output a comprehensive report:

```
## Deep Analysis Complete

**Transcripts processed:** N
**Summaries created/updated:** N
**Project summaries created:** N (across M projects)
**Tracker entries added:**
  - Topics: N
  - Sentiment signals: N
  - Influence signals: N
  - Commitments: N
  - Contradictions: N
  - Risks: N (new) + N (updated)
  - Meeting scores: N
**Weekly summaries created/updated:** N
**Programme wins logged:** N new (M skipped as duplicates)
**Outreach updates:** N new contacts, M existing contacts updated
**Context files modified:** [list which files were touched]
**Verification:** N items spot-checked, N passed, N flagged [UNVERIFIED]
**Backend import:** [success/skipped/failed]

### Notable Findings
1. [Most important insight from this batch]
2. [Second most important]
3. [Third most important]

### Attention Required
- [Any items flagged for user review: low-confidence identifications, unresolved contradictions, critical risks]
```
