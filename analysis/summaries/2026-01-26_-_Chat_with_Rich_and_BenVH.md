# Chat with Rich & BenVH — Pre-deployment Morning Sync
**Date:** 2026-01-26
**Attendees:** Richard Dosoo, BenVH (Ben Van Houten), Azmain Hossain, Martin Davies
**Duration context:** Medium (~40 minutes)
**Workstreams touched:** WS2 CLARA, WS6 Build in Five

## Key Points
- Morning coordination session before the afternoon Portfolio Review launch and Sales Recon executive session
- Azmain had been working on database changes locally (employee import, account team mapping) but couldn't deploy to prod without BenVH due to Alembic/database sync risks
- Richard insisted on keeping database changes separate to avoid breaking prod — team decided to wait for BenVH before deploying
- BenVH identified a schema mismatch: plan references `customer.name` but database uses `customer_name` — needs alignment before import
- Discussion about employee data import: currently 600 employees loaded, debating whether to expand to full org (~14,000) or limit to Colin/Mike/Helen's reports
- BenVH raised need for Anthropic/Claude API key — Richard explained they were told to go through the enablement team, not the MAp team (which only supports customer-facing products)
- BenVH building a form-based app generator with CICD workflows baked in — wants Claude API to enable prompt-driven app creation
- Richard flagged the need to decouple the monorepo: separate repos for separate apps (adoption tracker vs RMB app) to minimise blast radius from Cursor changes
- Martin tasked with creating a separate repo for the RMB (Risk Maturity Benchmarking) app and pushing his code there
- Afternoon plan: Azmain demos CLARA (~2 min), Richard demos RMB workflow (~1-2 min), Bernard demos his Copilot Studio agent

## Decisions Made
- Separate repos per app instead of monorepo: reduces risk of Cursor accidentally modifying adjacent apps → BenVH/Richard
- Employee import order: do employees first, then account team mapping (so employees exist for matching) → Azmain
- Dev/staging/prod environments now urgent priority after the tool goes live with real users → BenVH

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Deploy employee and account team changes to prod | Azmain/BenVH | 2026-01-26 (before 2pm) | Open |
| Create separate repo for RMB app | Martin Davies | 2026-01-26 | Open |
| Obtain Claude/Anthropic API key via enablement team | Richard | ASAP | Open |
| Introduce BenVH to Victor (MAp team) re: infrastructure hosting decision | Richard | Next week | Open |
| Workshop session on platform architecture (5 people including Ben Brooks) | Richard | 2026-01-27 | Open |

## Stakeholder Signals
- Richard is strategic about infrastructure decisions — wants to avoid premature commitment to AWS vs Azure vs MAp environments
- BenVH is proactively building platform tooling (app factory, TerraForm, CICD) — wants to ensure consistency across all future apps
- Azmain's laptop is painfully slow when running Cursor — hardware is a tangible constraint on productivity

## Open Questions Raised
- Should they stay on their current AWS account, migrate to MAp, or move to Azure? Decision deferred until Victor consultation
- How to handle the Salesforce-to-Gainsight transition for data integration — Gainsight team not ready until March

## Raw Quotes of Note
- "I'm slowly teaching you all the git commands" — BenVH to Azmain, on the learning-on-the-job reality
