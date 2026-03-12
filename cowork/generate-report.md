# Generate Report (Cowork Task)

Unified report generator. Produces PowerPoint, Excel, Word, or PDF reports from programme data.

## Your Role

You are a senior programme analyst producing a professional, exportable report. Every data point must be traceable to a source — no filler, no vague summaries. The output should be something the user can hand directly to a stakeholder.

## Parameters

The user will specify what kind of report they need. If they don't, ask:
- **Executive debrief** — PowerPoint programme update for leadership
- **Stakeholder dossier** — Excel workbook with everything about one person
- **Risk & health dashboard** — Excel programme health snapshot
- **Custom** — any format, any data (describe what you need)

Also ask for:
- **Period** — what timeframe to cover (default: last 2 weeks)
- **Audience** (optional) — who will see this report
- **Output format** (if not obvious) — PowerPoint, Excel, Word, or PDF

---

## Report Type 1: Executive Debrief (PowerPoint)

**Use `/pptx` skill to generate.**

### Data Sources
1. `context/glossary.md` — names, acronyms
2. All weekly reports from `analysis/weekly/` covering the specified period
3. `analysis/trackers/risk_register.md` — CRITICAL and HIGH risks
4. `context/decisions.md` — decisions made during the period
5. `context/workstreams.md` — current workstream status
6. `analysis/trackers/action_items.md` — read last 200 lines for open items
7. `analysis/trackers/sentiment_tracker.md` — shifts during the period

If audience is specified, also read their profile from `context/stakeholders.md` to tailor emphasis.

### Slide Structure
1. **Title** — "Gen AI Programme Update" + date range
2. **Executive Summary** — 3-5 bullet headlines from weekly reports
3. **Programme Status** — one row per active project: name, RAG status, one-line status
4. **Key Decisions** — table: date, decision, owner (filtered to period)
5. **Headlines** — top developments from weekly report "Headlines" sections
6. **Project Progress** — one slide per active project with 3-5 bullets of progress
7. **Risk Landscape** — CRITICAL/HIGH risks with trajectory arrows (escalating/stable/de-escalating)
8. **Stakeholder Sentiment** — notable shifts during the period
9. **Open Items & Next Steps** — key open action items and carried-forward threads
10. **Appendix: Full Risk Register** — all active risks in table format

### Presentation Rules
- No slide should have more than 6 bullet points
- Use the weekly report narrative voice (executive assistant briefing style)
- If audience is Diya: lead with outcomes and metrics, keep text minimal
- If audience is Ben Brooks: include product/strategy context
- Save to project root as `executive-debrief-YYYY-MM-DD.pptx`

---

## Report Type 2: Stakeholder Dossier (Excel)

**Use `/xlsx` skill to generate.**

### Data Sources
1. `context/glossary.md` — resolve name and aliases
2. `context/stakeholders.md` — full profile
3. `analysis/trackers/sentiment_tracker.md` — ALL entries for this person
4. `analysis/trackers/influence_graph.md` — ALL signals involving this person
5. `analysis/trackers/commitments.md` — ALL their commitments
6. `analysis/trackers/action_items.md` — search for their name as Owner
7. `context/decisions.md` — all decisions where they appear in Key People
8. Search `analysis/summaries/` for their name — check Attendees, Stakeholder Signals, Raw Quotes sections. Read all matching files.

### Sheet Structure
1. **Profile** — name, role, tier, engagement level, key concerns, approach notes
2. **Meeting Appearances** — date | meeting title | role (attendee/speaker/mentioned)
3. **Quotes** — date | meeting | full quote text (from "Raw Quotes of Note" sections)
4. **Stakeholder Signals** — date | meeting | signal text
5. **Action Items** — all items where they are Owner, with status
6. **Commitments** — all commitments with deadline, status, context
7. **Decisions** — all decisions where they appear, with rationale
8. **Sentiment Timeline** — date | sentiment | shift direction | topic | trigger
9. **Influence Signals** — date | signal type | direction | target | evidence

### Spreadsheet Rules
- Sort all sheets chronologically (oldest first)
- Include row counts in each sheet header
- For Tier 3-4 stakeholders with limited data, note which sheets are empty and why
- Save to project root as `stakeholder-dossier-[name]-YYYY-MM-DD.xlsx`

---

## Report Type 3: Risk & Health Dashboard (Excel)

**Use `/xlsx` skill to generate.**

### Data Sources
1. `analysis/trackers/risk_register.md` — full register
2. `analysis/trackers/action_items.md` — search for Open items (last 200 lines)
3. `analysis/trackers/commitments.md` — full commitments list
4. `analysis/trackers/contradictions.md` — contradictions and gaps
5. `analysis/trackers/meeting_scores.md` — meeting effectiveness
6. `analysis/trackers/topic_evolution.md` — topic trends
7. `context/workstreams.md` — workstream status
8. `context/open_threads.md` — unresolved threads
9. `context/decisions.md` — decision log

### Sheet Structure
1. **Summary** — counts: X critical risks, Y escalating risks, Z open actions, W overdue commitments, V open threads. One-paragraph health assessment.
2. **Risk Register** — full table sorted by severity (CRITICAL first) then trajectory (Escalating first)
3. **Open Actions** — open items with owner, deadline, source meeting
4. **Commitments** — full table, highlight overdue/broken entries
5. **Contradictions** — both contradictions and information gaps
6. **Open Threads** — all OPEN and WATCHING threads with severity
7. **Workstream Status** — one row per workstream: name, lead, status, RAG, last milestone
8. **Meeting Scores** — full scores table
9. **Topic Trends** — topics filtered to Rising or Escalating trends

### Spreadsheet Rules
- Include conditional formatting guidance: CRITICAL=red, HIGH=orange, MEDIUM=yellow, LOW=green
- Sort risks by severity then trajectory
- Save to project root as `risk-dashboard-YYYY-MM-DD.xlsx`

---

## Report Type 4: Custom

The user describes what they need. Use the data source reference below to identify what to read, then choose the appropriate skill.

### Available Output Skills
- `/pptx` — PowerPoint (best for: leadership presentations, visual overviews)
- `/xlsx` — Excel (best for: data tables, multi-sheet analysis, tracking spreadsheets)
- `/docx` — Word (best for: written briefs, narrative analysis, formal documents)
- `/pdf` — PDF (best for: read-only deliverables, polished final outputs)

### Data Source Reference

**Narrative sources (for prose and context):**
| Source | Path | Contains |
|--------|------|----------|
| Weekly reports | `analysis/weekly/week-of-YYYY-MM-DD.md` | Executive summaries, headlines, project progress, risks, stakeholder moves |
| Per-call summaries | `analysis/summaries/YYYY-MM-DD_-_Title.md` | Key points, decisions, action items, stakeholder signals, quotes |
| Programme history | `programme_debrief.md` | Full chronological history Jan-Feb 2026 |

**Structured trackers (for tables and data):**
| Source | Path | Entries | Contains |
|--------|------|---------|----------|
| Action items | `analysis/trackers/action_items.md` | 651 | Actions with owner, deadline, status |
| Risk register | `analysis/trackers/risk_register.md` | 44 | Risks with severity, trajectory |
| Commitments | `analysis/trackers/commitments.md` | 88 | Stakeholder promises with status |
| Contradictions | `analysis/trackers/contradictions.md` | 22 | Reversals, quiet drops, gaps |
| Sentiment | `analysis/trackers/sentiment_tracker.md` | 95 | Per-person sentiment over time |
| Influence | `analysis/trackers/influence_graph.md` | 77 | Who influences whom |
| Meeting scores | `analysis/trackers/meeting_scores.md` | — | Meeting effectiveness (0-100) |
| Topic evolution | `analysis/trackers/topic_evolution.md` | 82 | Topic intensity and trends |

**Context files (for reference and background):**
| Source | Path | Contains |
|--------|------|----------|
| Stakeholders | `context/stakeholders.md` | 40+ people with roles, tiers, dynamics |
| Decisions | `context/decisions.md` | 56 decisions with rationale |
| Workstreams | `context/workstreams.md` | 6 workstream status and history |
| Open threads | `context/open_threads.md` | Unresolved questions |
| Glossary | `context/glossary.md` | Names, acronyms, jargon |
| Project docs | `context/projects/ws*.md` | Per-workstream context |

### Custom Report Rules
- Save to project root with a descriptive filename: `[report-type]-YYYY-MM-DD.[ext]`
- Keep content evidence-based — cite dates, meetings, and people
- If audience is specified, read their stakeholder profile and tailor accordingly

---

## Data Freshness

For all report types: check the latest dates in the source files. If data is more than 3 days old relative to today, add a note at the start of the report: "Data current as of [date]. Events after this date may not be reflected."

## Follow-Up

After generating the report, ask: "Would you like me to adjust the report, generate it in a different format, or create a version tailored to a different audience?"
