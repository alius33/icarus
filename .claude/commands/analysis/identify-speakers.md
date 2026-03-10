---
description: Identify unnamed speakers in meeting transcripts using multi-stage analysis
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent
argument-hint: [filepath|all|--apply|--dry-run]
---

# Identify Unknown Speakers in Transcripts

Multi-stage speaker identification pipeline that identifies unnamed speakers
(Speaker 1, Speaker 2, Unknown Speaker) in meeting transcripts using:
- Meeting title parsing
- Self-introduction detection
- Greeting exchange analysis
- Process of elimination
- Conversation structure analysis
- Stylometric fingerprinting
- Bayesian confidence aggregation
- Claude-assisted inference for remaining unknowns

## Arguments
$ARGUMENTS — Options:
- `all` or empty: Analyze all transcripts
- `filepath`: Analyze a single transcript (e.g., `Transcripts/2026-02-23_-_Meeting_with_Diya.txt`)
- `--apply`: Apply high-confidence identifications to files
- `--dry-run`: Preview changes without modifying files
- `--threshold 0.85`: Minimum confidence for applying (default: 0.0)

## Step 0: Load Context

Read these files for stakeholder knowledge:
1. `context/stakeholders.md` — who everyone is, roles, speech patterns
2. `context/glossary.md` — names and acronyms
3. `backend/scripts/speaker_id/config.py` — canonical aliases and patterns

## Step 1: Run Automated Pipeline (Stages 0-5)

```bash
cd backend && python -m scripts.speaker_id.runner --analyze --output /tmp/speaker_id_mapping.json --report /tmp/speaker_id_review.md $ARGUMENTS
```

Read the review report to understand results:
```bash
cat /tmp/speaker_id_review.md
```

## Step 2: Claude-Assisted Identification (Stage 6)

For transcripts with unresolved speakers after the automated pipeline:

1. Read the mapping JSON to find unresolved transcripts
2. For each unresolved transcript:
   a. Read the full transcript file
   b. Read the automated analysis (who is identified, what evidence exists)
   c. Use stakeholder knowledge to identify remaining unknowns:
      - Who typically attends this type of meeting?
      - What topics is the unknown speaker discussing?
      - How does their speech style match known stakeholders?
      - Who do other speakers address or reference?
      - What role/domain expertise is demonstrated?
   d. Assign identifications with confidence scores and evidence

3. Update the mapping JSON with Claude-assisted identifications

## Step 3: Review and Apply

Review the complete mapping. For each identification:
- Show: transcript filename, speaker label, identified name, confidence, method, evidence
- Flag any identification below 0.7 confidence for user review

If user confirms (or --apply flag used):
```bash
cd backend && python -m scripts.speaker_id.runner --apply --mapping-file /tmp/speaker_id_mapping.json --threshold 0.7
```

## Step 4: Re-import to Database

After modifications, trigger backend re-import:
```bash
cd backend && python -m scripts.import_data --data-root .. --db-url "$DATABASE_URL"
```
Or call `POST /api/import/trigger` if the backend is running.

## Output Summary
- Number of speakers identified per transcript
- Number still unresolved
- List of low-confidence identifications flagged for review
- Total replacements made (if --apply used)
