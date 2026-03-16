---
globs: analysis/**, context/**
---

# Update Handling Rules

When the user says "analyse updates" or "analyse my updates":
- Look at the **Updates page** in the app (database-only content via `/api/project-updates`) — NOT transcript files
- Never confuse "updates" with "transcripts" — they are different content types

## Full Processing Pipeline (Every Time)

### Phase 1: Fetch & Parse

1. **Fetch updates** from the production API: `GET /api/project-updates?is_processed=false`
   - Production base URL: `https://icarus-production-5044.up.railway.app/api`
2. **Strip "(Moody's)"** from all names — Teams appends this to every person's name and it must be removed during analysis
3. **Extract timestamps** from Teams chat messages — note the date and time of each message, use them to establish when things happened
4. **Correct name spellings** — Teams chat shows the official spelling of each person's name. Compare against `context/stakeholders.md` and fix any discrepancies

### Phase 2: Analyse Content

5. **Analyse content** — extract ALL intelligence from the updates:
   - Decisions made or implied
   - Action items / tasks assigned
   - Open threads created, updated, or resolved
   - Sentiment shifts and political dynamics
   - Stakeholder updates (roles, relationships, attitudes)
   - Project status changes

### Phase 2b: Generate Update Summaries

5b. **Write an analytical summary** for each update (same quality as transcript summaries):
    - Structured markdown, 5-10 bullet points covering: key decisions, actions, stakeholder dynamics, implications
    - Store via `PATCH /api/project-updates/{id}` with `{summary: "<markdown>"}`
    - This summary is displayed in "Current Status" on project pages and as context in weekly plan actions
    - Do NOT use the raw update text — write an analytical summary like you would for a transcript

### Phase 3: Update Context Files (Markdown)

6. **Update context files** — these are the source of truth for the import pipeline:
   - `context/stakeholders.md` — new people, role changes, sentiment shifts
   - `context/open_threads.md` — new threads, status updates, resolutions
   - `context/decisions.md` — new decisions with numbers continuing from last entry
   - `analysis/trackers/action_items.md` — new action items (read tail with offset, never whole file)
   - `context/projects/*.md` — relevant project context files
   - Any other tracker files as needed

### Phase 4: Update Database Entities (API Calls)

7. **Create/update decisions** in the database:
   - `POST /api/decisions` with `{decision, date, rationale, key_people, execution_status, project_id}`
   - Link to project: `POST /api/projects/{project_id}/links` with `{links: [{entity_type: "decision", entity_id: <id>}]}`

8. **Create/update open threads** in the database:
   - `POST /api/open-threads` with `{title, context, question, why_it_matters, status, first_raised, severity, trend}`
   - Or `PATCH /api/open-threads/{id}` to update existing threads

9. **Create tasks** in the database:
   - `POST /api/tasks` with `{title, description, status, priority, assignee, project_id, due_date}`
   - Use tasks for actionable items that need tracking (prefer tasks over legacy action_items)

10. **Link updates to relevant projects** (MANDATORY — verify links exist):
    - `POST /api/projects/{project_id}/links` with `{links: [{entity_type: "project_update", entity_id: <update_id>}]}`
    - EVERY update must be linked to at least one project — this is how they appear on project pages
    - Determine relevant projects from the content of each update
    - After creating links, verify with `GET /api/projects/{project_id}/hub` that the update appears

10b. **Create ProjectSummary entries** for each linked project (MANDATORY):
    - `POST /api/project-summaries` with `{project_id, project_update_id: <update_id>, date: "<YYYY-MM-DD>", relevance: "HIGH"|"MEDIUM"|"LOW", content: "<project-specific summary>"}`
    - The `content` should be the portion of the analytical summary relevant to this specific project
    - This is what powers "Current Status" on project pages — without it, updates are invisible there

11. **Update stakeholders** if needed:
    - `POST /api/stakeholders` for new people, or `PATCH /api/stakeholders/{id}` for updates

### Phase 5: Weekly Plan

12. **Update the weekly plan** with new actions derived from the updates:
    - Check current plan: `GET /api/weekly-plans/current`
    - Add new actions: `POST /api/weekly-plans/{plan_id}/actions` with `{category, title, description, priority, owner, status, deliverable_id, source_update_id: <update_id>, context: "<rich analytical context from the summary>"}`
    - The `context` field MUST contain rich analytical content from the update summary — NOT just "From project update: <title>"
    - The `source_update_id` field MUST be set so the UI can link back to the source update
    - Categories: `deliverable_strategic`, `deliverable_tactical`, `programme_strategic`, `programme_tactical`
    - If no current plan exists, create one: `POST /api/weekly-plans`

### Phase 6: Finalise

13. **Mark updates as processed** via `PATCH /api/project-updates/{id}/processed`
14. **Commit context file changes** (don't push unless asked)

## Name Correction Workflow (Every Time)

- Compare all names in the update against the stakeholder file
- If a name spelling differs from what's in the stakeholder file, the Teams spelling is authoritative
- Update the stakeholder file AND context files with the correct spelling
- Note the correction for the user

## Project ID Reference

| ID | Project |
|----|---------|
| 1  | Training & Enablement |
| 2  | CLARA (IRP Adoption Tracker) |
| 3  | Customer Success Agent |
| 4  | Friday (CS AI Agent) |
| 5  | Navigator L1 Automation |
| 6  | Build in Five |
| 7  | Cross OU Collaboration |
| 8  | Program Management |
| 9  | TSR Enhancements |
| 10 | App Factory |

## Key Reminders

- Updates are stored in the database only — they do NOT create files in `Transcripts/`
- The `content_type` field indicates whether it's a `note` (user's own context) or `teams_chat` (pasted from Teams)
- Teams chats have timestamps embedded in the messages — use these for chronological ordering
- "Sales Recon" is NOT a project — never create a project for it
- All API calls go to the **production** Railway URL, not localhost (updates are on production)
- The project overview tab shows "Recent Updates" only if ProjectLink entries exist for that project
- "Current Status" on project pages requires ProjectSummary entries — without them, updates are invisible there
- Weekly plan actions MUST include `source_update_id` + rich `context` from the summary

## Processing Checklist (Verify Every Time)

- [ ] Analytical summary generated and stored on each update record (`PATCH /api/project-updates/{id}`)
- [ ] ProjectLink entries created for ALL relevant projects
- [ ] ProjectSummary entries created for each linked project (powers "Current Status")
- [ ] Weekly plan actions include `source_update_id` + rich analytical context
- [ ] Context files updated (stakeholders, decisions, threads, trackers, projects)
