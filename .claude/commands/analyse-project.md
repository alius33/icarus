# Analyse Project

Retroactively analyse existing transcripts to find content relevant to a specific project.

## Arguments
$ARGUMENTS = project name

## Steps

1. Look up the project "$ARGUMENTS" via `GET /api/projects` (search by name). If not found, create it via POST.
2. Load context files for background:
   - `context/glossary.md`
   - `context/stakeholders.md`
   - All files in `context/projects/`
3. Fetch the project's keywords from the API. If no keywords, use the project name + description as search terms.
4. Read ALL summaries from `analysis/summaries/*.md` (not raw transcripts).
5. Two-pass relevance detection:
   a. **Keyword scan**: Check each summary for project keywords
   b. **Semantic pass**: For summaries with no keyword hits, check if the content semantically relates to the project
6. For each relevant summary, extract:
   - Decisions related to the project
   - Action items assigned to project stakeholders
   - Open threads touching the project
   - Stakeholder sentiment signals
   - Commitments made
7. Write a comprehensive project brief to `analysis/projects/{slug}.md`
8. Link relevant entities to the project via `POST /api/projects/{id}/links`
9. Update the project's `last_analysed_date` via `PATCH /api/projects/{id}`
10. Trigger backend import: `POST /api/import/trigger` or run `cd backend && python -m scripts.import_data --data-root ..`
11. Report findings: number of transcripts scanned, relevant ones found, entities linked
