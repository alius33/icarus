# AI Tool Development Meeting
**Date:** 2026-03-03
**Attendees:** Azmain Hossain, Martin Davies
**Duration context:** Medium (~28 minutes)
**Workstreams touched:** WS6 Build in Five

## Key Points
- Azmain and Martin discussed the architecture and vision for the customer-facing pre-sales component of Build in Five. This is distinct from the internal "app factory" side that BenVH and Nikhil will work on.
- Martin showed Azmain a dashboard he previously built at Apollo that visualises EDM/RDM data by country, peril, and layer (location, AL, curves, RDS). This becomes the reference point for what the Build in Five pre-sales tool should look like.
- The agreed MVP concept: a modular UI where a pre-sales person can drag-and-drop IRP API modules (e.g., windstorm, hurricane, location API) onto a foundation layer. Each module would have two tabs -- raw data (exportable as CSV) and an auto-generated intelligent dashboard.
- Phase 1 scope: three modules with a foundation layer and a drag-and-drop UI. Phase 2 would add combined dashboards across modules.
- Azmain explicitly said not to include AI/LLM functionality in the app itself to avoid spiralling costs -- it should be a straightforward app that runs on localhost.
- Martin's existing Apollo dashboard already demonstrates the end-to-end workflow: drop a database file into a watch folder, the system identifies countries/perils, pulls appropriate models, and generates results.
- Azmain advised Martin to start from a brand new folder without cursor rules or excessive context, to keep the build lean and avoid burning through the context window.
- Budget discussion: Azmain's cursor budget reset on March 1. He and Richard are paying 200 pounds/month from personal cards for Claude subscriptions because they cannot expense them. Martin does not have a Claude licence.
- Azmain's Anthropic API key via AWS is not working -- keeps returning "not authorised," likely an IAM role issue.
- Azmain's development approach: use Opus for planning/thinking, Sonnet for building. Do a big initial build in one go, then fine-tune afterwards.

## Decisions Made
- Build in Five pre-sales tool will start from scratch, not iterate on existing codebase -> Azmain
- MVP scope frozen at three modules + foundation layer + basic UI -> Azmain, Martin
- No AI/LLM integration in the app itself (to control costs) -> Azmain
- Martin to focus exclusively on the customer-facing pre-sales component; internal app factory work goes to BenVH and Nikhil -> Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Identify three initial API modules for MVP | Martin | TBD | Open |
| Build foundation layer and modular drag-and-drop UI | Martin | TBD | Open |
| Create an assets folder with Moody's colours and logo | Azmain | TBD | Open |
| Show progress to Richard and Ben Brooks for feedback | Martin/Azmain | TBD | Open |

## Stakeholder Signals
- **Azmain** is energised about the pre-sales concept and sees it as a "massive win" if they can demonstrate it
- **Martin** is eager and has relevant prior work (Apollo dashboards) that maps closely to the vision
- Both are navigating budget constraints -- personal expenditure on AI tools is a recurring pain point

## Open Questions Raised
- How do the IRP model licences work in practice -- is it per-model or per-API?
- What exactly should the three initial modules be?
- Will the Anthropic API key issue get resolved for Martin to use?

## Raw Quotes of Note
- "I don't want to put in AI stuff, because the moment you start putting that in, the costs just spiral." -- Azmain, on keeping the MVP simple
