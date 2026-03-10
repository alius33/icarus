# Chat with Asset Management
**Date:** 2026-02-26
**Attendees:** Azmain Hossain, Richard Dosoo (Speaker 4), BenVH (Speaker 1), Amanda (Speaker 2), Edward (Speaker 1/BenVH), Ben Reynolds (Speaker 3)
**Duration context:** Long (~41 minutes)
**Workstreams touched:** WS2 CLARA, WS6 Build in Five

## Key Points
- Cross-team knowledge sharing session with the Asset Management team. Amanda demos her asset management app -- a comprehensive customer success platform she built independently with AI-generated PDF reports, renewal tracking, prospecting pipeline, cross-sell heat maps, and task management.
- Amanda's app generates detailed AI-powered PDF reports using OpenAI API: per-client renewal analysis with non-repetitive commentary, risk metrics (custom-built, replacing NPS which she considers outdated), actionable next steps, and proposal tracking. Each client gets its own page with meeting notes analysis and trend data.
- The reports are a revelation for Azmain: he wants to use them as aspirational examples to motivate IRP CSMs to enter better data. His plan is to show seniors the Asset Management outputs and frame it as "look what their CSMs produce -- don't you want reports like this?"
- Amanda's app includes features CLARA is still building toward: task generation from meeting notes (AI reads notes and creates tasks with assignees), engagement tracking with per-client meeting frequency expectations, and a project management timeline with PDF output.
- Key difference between Asset Management and IRP: Amanda is both the builder and the user. She enters her own data diligently. IRP CSMs are resistant to data entry and afraid to click buttons in CLARA. Azmain describes hand-holding CSMs through basic data entry like it is 2001.
- Azmain demonstrates CLARA features to Amanda: the reports functionality (modelled after Salesforce report builder), the executive summary vs. updates confusion (CSMs keep updating the executive summary instead of using the updates section), and the tab-based layout designed to reduce scrolling complaints.
- BenVH raises the AI governance process requirement: any app making calls to OpenAI/Claude API needs to go through an intake form, potential cyber security review, and risk governance review. He shares that the process is opaque -- he sent a form and heard nothing for two weeks until he directly messaged Melinda Tigerino. Key contacts: Melinda Tigerino (risk governance) and Frank Cifuentes (cyber security).
- Richard confirms the team is deploying Anthropic models in their own AWS environment per Dennis Clement's instruction. BenVH believes the AI governance process still applies even for self-hosted models -- it covers who is consuming outputs, whether users know outputs are AI-generated, and quality validation.
- Richard's manager and their manager are encouraging formalisation of cross-team collaboration between Insurance and Asset Management. Richard will set up a monthly check-in cadence.
- BenVH mentions cursor rules have been created as guardrails for the team and suggests looking at agent skills as a more portable alternative that works across Cursor, Windsurf, and Claude Code.
- Amanda will provide a PRD of her account planning features for potential integration into CLARA after she returns from holiday.

## Decisions Made
- Amanda to provide PRD of account planning features for CLARA integration -> Amanda / Richard
- Monthly cross-team check-in to be formalised between Insurance and Asset Management -> Richard
- AI governance intake form to be submitted for CLARA's LLM integration -> Azmain / Richard
- Cursor rules to be shared with Asset Management team; agent skills to be evaluated as alternative -> BenVH / Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Send AI governance intake form link and contact details to Azmain/Richard | BenVH | Today | Open |
| Submit AI governance intake form for CLARA LLM integration | Azmain / Richard | ASAP | Open |
| Set up monthly cross-team check-in with Asset Management | Richard | Next week | Open |
| Provide account planning PRD after holiday | Amanda | After holiday | Open |
| Share cursor rules file with Asset Management team | Richard | Next check-in | Open |

## Stakeholder Signals
- Amanda is impressively self-sufficient: she built a comprehensive asset management platform solo, generates AI reports, and is her own best user. Her work serves as proof of what is possible with good data hygiene.
- Azmain is simultaneously inspired and frustrated: inspired by what Amanda's app can do, frustrated that IRP CSMs cannot match that level of data discipline. He plans to use Amanda's outputs as leverage to drive behavioural change.
- BenVH is the practical voice on governance: he has been through the AI governance process and warns it is opaque and slow. His advice is to start the process early and chase directly.
- Ben Reynolds is technically curious, asking detailed questions about AI task generation and wanting to understand the underlying architecture.

## Open Questions Raised
- How long will the AI governance process take for CLARA's LLM integration?
- Will the Moody's-Anthropic strategic partnership accelerate access to Claude tools company-wide?
- Can agent skills replace cursor rules as a more portable guardrail framework?
- How should the team handle the discrepancy between Asset Management's data discipline and IRP CSMs' resistance to data entry?

## Raw Quotes of Note
- "It's freaking 2001 and somebody's teaching them data entry and literally be like, click here." -- Azmain Hossain, on the state of CSM adoption in IRP
