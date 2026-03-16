# Slidey (AI Presentations)

## Overview

Slidey is an AI-powered collaborative presentation platform that generates branded HTML slide decks from prompts. It emerged from the programme with the strongest internal traction of any product demo — Richard described it as generating more excitement than CLARA. The product is being repositioned from a personal slide generator into a collaborative executive-authoring workflow with RBAC, a markdown content layer, and agentic extensions for account plans, charters, and climate reports.

Deployed via App Factory infrastructure. Consumes App Factory MCP server for inter-app communication (e.g., CLARA builds an MD file, sends to Slidey via App Factory for PowerPoint generation).

## Status (as of 16 March 2026)

**ACTIVE — Auth landed, RBAC partially wired, moving to data scoping and performance**

Key milestones:
- **10 Mar:** Team decides Slidey deserves serious effort. Richard: strongest traction of all demos.
- **11 Mar:** Biggest day — demo pressure, deployment failures, auth issues, architecture debate (markdown content model), RBAC spec created, collaborative storyboard workflow designed.
- **12-13 Mar:** Consolidation — codebase audit, alembic head cleanup, RBAC working on local.
- **14 Mar:** Content/narrative layer spec (CONTENT-LAYER.md) shared. Auth still incomplete in dev.
- **15 Mar:** UI showing collaboration features but auth not wired. Diya sent an HTML presentation and couldn't comment on it — key product feedback.
- **16 Mar:** Auth + logout landed. RBAC partially connected. New problem: users can see all presentations (user-ID not filtering). Performance refactoring started using cost telemetry data.

## Team

| Role | Person | Notes |
|------|--------|-------|
| Architecture / Lead | Richard Dosoo | Bulk of design thinking — RBAC, content layer, markdown-per-slide model, async processing. Live triage under demo pressure. |
| Product Vision | Ben Brookes | Use cases, UX pain points, collaboration needs. Identified /data slash command for analysis+charting. Framed Slidey as a platform for agentic situations (account plans, charters, climate reports). |
| Auth / Infrastructure | BenVH (Ben Van Houten) | Implemented auth + logout. RBAC wiring. MCP server work. Late-night debugging. |
| Early Tester | Amit Gondha | Invited for testing 11 Mar. API key coordination ongoing. |

## Architecture

### Current Pipeline
`prompt → LLM → HTML → preview`

### Target Pipeline (markdown-first)
Richard proposed a markdown-per-slide content model:
1. Owner provides brief
2. Storyboard Architect creates outline with skeleton `content_md`
3. Team reviews outline
4. Section owners fill content collaboratively in a Content tab
5. Owner runs continuity review on markdown
6. Final "Polish with AI" render generates branded HTML
7. Only visual iteration happens in HTML after this point

**Key design elements:**
- `content_md` column alongside `html` in the database
- Split view: markdown editor (left) + HTML preview (right)
- Steps 1-4 have zero LLM content-editing cost — significant cost optimisation
- Obsidian-like editing but purpose-built for live collaboration (Obsidian itself is a poor fit)

### RBAC
- SLIDEY-RBAC-SPEC.md created 11 Mar
- Biggest risk: project invitation flow (owner-only invite/remove implied, but UX/API for inviting, accepting, removing, and handling in-flight work not yet specified)
- Auth + logout landed 16 Mar
- Data scoping bug: user-ID not filtering presentations (all users see all content)

### Async Processing
- Added 10 Mar for heavier workloads
- Necessary for multi-slide generation and data analysis extensions

## Key Decisions

| Date | Decision | Key People |
|------|----------|------------|
| 10 Mar | Slidey prioritized — strongest traction of all demos | Richard, Ben Brookes |
| 11 Mar | Markdown-per-slide content model adopted | Richard, Ben Brookes |
| 11 Mar | Auth + RBAC required before wider sharing | Richard, BenVH, Ben Brookes |
| 11 Mar | Collaborative storyboard workflow designed | Richard |
| 14 Mar | Content/narrative layer spec created (CONTENT-LAYER.md) | Richard |
| 16 Mar | Auth + logout + RBAC landed | BenVH |

## Risks

| Risk | Impact | Likelihood | Notes |
|------|--------|------------|-------|
| Data scoping incomplete — all users see all content | High | High | User-ID not taken into account in queries. Blocks wider rollout. |
| HTML output unfit for executive review | Medium | Confirmed | Diya couldn't comment on HTML. Need PDF/comment-friendly format. |
| No dev/staging/prod separation | Medium | High | Ben Brookes requesting environments + release notes structure. |
| Convergence gap — multiple teams building slide generators | Medium | Medium | Juliet built one independently. Cross-team meeting planned. |
| RBAC invitation flow not specified | Medium | Medium | Owner-only invite/remove implied but UX not designed. |

## Dependencies

| Dependency | Owner | Status | Impact |
|------------|-------|--------|--------|
| App Factory MCP server | BenVH | Active | Slidey deployed through App Factory infrastructure |
| Azure AD auth | BenVH | Landed 16 Mar | Required for RBAC and data scoping |
| Bedrock/Anthropic API access | Richard | Active | LLM generation for slide content |
| Content layer implementation | Richard | In progress | Enables collaborative editing before AI render |

## Open Questions

1. **When will data scoping be fixed?** User-ID filtering is the immediate blocker for wider rollout.
2. **Will dev/staging/prod environments be set up?** Ben Brookes is asking for this. Signals transition to production use.
3. **What output format solves the reviewability problem?** Diya couldn't comment on HTML. PDF? Native presentation format?
4. **How will the Juliet convergence work?** She built a Moody's branded PowerPoint generator independently. Cross-team meeting was planned for Tuesday.
5. **What is the /data slash command scope?** Ben Brookes proposed data file processing with chart generation — extends Slidey beyond presentations into analysis.
6. **Who are Colin and Keith?** Mentioned as demo targets on 11 Mar but no further context.

## Technical Artifacts

- **SLIDEY-RBAC-SPEC.md** — Role-based access control specification (11 Mar)
- **CONTENT-LAYER.md** — Content/narrative layer design spec (14 Mar)
- **CODEBASE-AUDIT.md** — Codebase audit identifying alembic head merge needs (13 Mar)
- **cost_entries.json** — Cost telemetry data extracted for performance analysis (16 Mar)

## Transcript References

| Date | Source | Relevance |
|------|--------|-----------|
| 10-16 Mar | Teams channel day-by-day summary | Full project history from inception to auth landing |
