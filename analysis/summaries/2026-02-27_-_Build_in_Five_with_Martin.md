# Build in Five with Martin
**Date:** 2026-02-27
**Attendees:** Richard Dosoo, Azmain Hossain, Martin Davies
**Duration context:** Short (~28 minutes)
**Workstreams touched:** WS6 Build in Five

## Key Points
- Martin's first detailed scoping session for Build in Five since returning from holiday. Richard confirms 75% time allocation approved for 12 weeks, with Stacy sign-off pending as a formality.
- The March 21 exceedance event is confirmed as the target: Ben has a slot on the innovation panel and wants to demo Build in Five. The submission needs to go through an approval process, so the work needs to be ready well before the event date.
- Dubai ambition reiterated: if Build in Five is ready, the team wants to demo to Dimitri and Olga in Dubai for cross-OU expansion. Richard's manager (Ed) is supportive -- "if you guys can make it happen, we'll go."
- Ben expanded the original three demo scenarios significantly while Martin was away. The scenarios are still three in number but much broader in scope: (1) a data integration service for customers claiming "your platform can't handle our data formats" -- building CSV import, schema validation, and sandbox write; (2) custom analytics views using React front-end querying Exposure IQ data with aggregation; (3) a webhook/notification integration mock for guidewire/Golden Bear use case -- proving that a "six month" integration estimate can be done in five minutes.
- The Golden Bear scenario is based on a real lost deal: Golden Bear wanted to move to Guidewire's Policy Centre, which needs webhook notifications from the modelling platform. The team estimated six months; the customer would not pay. Build in Five could demonstrate this as a five-minute problem.
- Martin raises a key clarification question: is Build in Five producing pre-built prompts that sales teams follow step by step, or a live foundation that sales teams customise in real-time during customer meetings? The answer is the latter -- a pre-configured foundation with API connections already wired, where the salesperson adds components (location analytics, specific data views) during the conversation based on customer needs.
- The GSD (Get Stuff Done) framework needs adaptation: it is developer-focused, but Build in Five users are non-technical. Azmain redesigned the intake process to start with "what problem are you trying to solve?" rather than "tell me what to build" -- deliberately pushing users to think about outcomes before specifications. The four-step guided process (problem definition, solution thinking, recommended build, detailed spec) can take hours to days depending on user speed.
- Azmain intentionally designed friction into the process: if someone has a trivial problem, the structured question flow will discourage them from wasting build resources. Only worthwhile problems survive the intake process.
- Richard demos a web front-end he built for non-technical users to go through the guided requirement questions, which then generates a brief on the right side. The brief is detailed enough to fire directly at Cursor/Claude to build the app within the team's architecture constraints.
- Four delivery mechanisms identified: (1) the web front-end guided workflow, (2) a set of prompts for Cursor/Claude Code, (3) a requirements shopping market where pre-built BRDs can be combined into new specs, (4) (forgotten fourth mechanism, to be documented later).
- Martin needs onboarding: Richard will send all programme documents, service now tickets for Claude Code access (requires admin rights, which Martin has), and AWS CLI setup instructions. A deeper scoping session is planned for next week.

## Decisions Made
- Build in Five target remains March 21 exceedance event -> Martin / Richard / Ben
- Martin to first onboard and understand expanded scope before committing to timelines -> Martin
- GSD framework to be adapted for non-technical user personas -> Azmain / Martin
- Three demo scenarios to be validated with Rahul and other stakeholders for relevance -> Martin
- Programme documents to be moved to SharePoint (not local machines) and split from CLARA project folders -> Azmain / Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Send all programme documents and updated scope to Martin | Richard | Today (27 Feb) | Open |
| Send ServiceNow tickets for Claude Code onboarding (AWS CLI + Claude Code install) | Richard | Today | Open |
| Set up deeper scoping session for Build in Five next week | Richard / Martin | Next week | Open |
| Create SharePoint folder structure for Build in Five (separate from CLARA) | Azmain | This week | Open |
| Validate demo scenarios with Rahul and other stakeholders | Martin | Next week | Open |
| Martin to review expanded scope document and confirm understanding | Martin | Early next week | Open |

## Stakeholder Signals
- Martin is methodical: he asks the right clarifying questions about end goals before jumping in, and is comfortable pushing back when scope is unclear. He wants to understand the full picture before committing to timelines.
- Richard is struggling with logistics: laptop rebooting during the meeting, Docker containers failing to start, unable to find mock-up files. The pace of activity is outstripping his ability to stay organised.
- Azmain's design philosophy is deliberate: he wants the intake process to filter out low-value requests by requiring structured thinking. This is a governance mechanism disguised as a user experience choice.
- The team's excitement about Dubai/exceedance is genuine motivational fuel, but the March 21 deadline is aggressive given Martin is still onboarding.

## Open Questions Raised
- Is the March 21 exceedance deadline realistic given Martin's onboarding time?
- Which of the four delivery mechanisms should be prioritised for the exceedance demo?
- Should the demo scenarios use IRP Responder APIs instead of Underwriting IQ, as Martin suggests for two of the three scenarios?
- What does the deployment side look like for demo apps -- local host only, or does Ben's automation need to be ready?

## Raw Quotes of Note
- "If you guys can make it happen, we'll go." -- Ed (Richard's manager's manager), on the Dubai opportunity tied to Build in Five
