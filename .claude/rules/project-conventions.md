# Project Conventions

## File Organisation
- Generated content (PDFs, PPTX, DOCX) → `generated content/` folder
- Analysis output → `analysis/summaries/`, `analysis/weekly/`, `analysis/trackers/`
- Context updates → `context/` files
- Never save working files to the project root

## Planning Meta-Rule (MANDATORY — enforce automatically)
Every plan MUST go through **two analysis passes** after the initial draft. Do NOT present the plan to the user or call ExitPlanMode until both passes are complete. Do NOT wait for the user to ask — run both passes yourself immediately after drafting the plan.

**After writing the initial plan draft, IMMEDIATELY do:**

**Pass 1 — Gap Analysis**: Re-read the plan and identify gaps, missing dependencies, outdated references, and structural weaknesses. Update the plan in-place with fixes.

**Pass 2 — Assumption Challenge**: Re-read the updated plan and challenge assumptions, verify any referenced files actually exist (use Glob/Read), and optimize for minimal change. Update the plan in-place with final fixes.

**Then** mark the plan as reviewed and present it to the user (ExitPlanMode). The plan shown to the user must be the post-Pass-2 version.

## Commit Rules
- Never commit `.env` files or secrets
- After analysis: stage `Transcripts/`, `analysis/`, AND `context/` — all needed for Railway import
