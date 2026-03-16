# Project Conventions

## File Organisation
- Generated content (PDFs, PPTX, DOCX) → `generated content/` folder
- Analysis output → `analysis/summaries/`, `analysis/weekly/`, `analysis/trackers/`
- Context updates → `context/` files
- Never save working files to the project root

## Planning Meta-Rule
Every plan must go through **two analysis passes** after the initial draft:
- **Pass 1**: Identify gaps, missing dependencies, outdated references, structural weaknesses
- **Pass 2**: Challenge assumptions, verify referenced files exist, optimize for minimal change

## Commit Rules
- Never commit `.env` files or secrets
- After analysis: stage `Transcripts/`, `analysis/`, AND `context/` — all needed for Railway import
