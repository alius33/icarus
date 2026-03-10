# Generate Standup Notes

Generate a daily standup summary based on recent activity.

## Steps

1. Check git log for recent commits:
   ```bash
   git log --oneline --since="yesterday" --all
   ```
2. Check git diff for uncommitted work:
   ```bash
   git diff --stat
   git diff --staged --stat
   ```
3. Read the most recent weekly report from `analysis/weekly/`
4. Check for any new transcripts in `Transcripts/` not yet processed

## Output Format

### Yesterday
- [What was completed — from git log and recent summaries]

### Today
- [Suggested focus areas based on:]
  - Uncommitted work in progress
  - Unprocessed transcripts
  - Open threads from the latest weekly report
  - Any pending action items

### Blockers
- [Any issues detected:]
  - Build failures
  - Failing tests
  - Unresolved merge conflicts
  - Missing environment variables

Keep it brief — 5-10 bullet points total.
