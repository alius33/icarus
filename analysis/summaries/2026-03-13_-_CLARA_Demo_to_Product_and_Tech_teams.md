# CLARA Demo to Product & Tech Teams
**Date:** 2026-03-13
**Attendees:** Cihan (MD, Product & Technology), Ben Brookes, Natalia Plant, Azmain Hossain, Ollie (product team), Julie (product team), and wider product/engineering teams (~40-50 attendees)
**Duration context:** Medium-long (~42 minutes)
**Primary project:** CLARA (IRP Adoption Tracker)
**Secondary projects:** App Factory, Program Management

## Key Points
- Cihan (MD Product & Technology) convened his entire product and engineering team — the largest audience CLARA has been shown to. He framed the session around his customer obsession culture goal, pod structure, and how CLARA enables data-driven customer engagement.
- Cihan personally endorses CLARA as a daily tool: described it as "an amazing source to actually get all of the information you need." He uses it to understand blockers, customer status, and dissatisfaction issues.
- Ben Brookes gave strategic context: 32 customer migration scorecard target for 2026, CLARA as the system of record for the adoption and migration process. Emphasised the structured data approach — use cases → RAG status → blockers → themes → actions — as the real power of the system.
- **Major milestone cited:** more than half of the yearly 32-migration target completed before end of Q1. Azmain explicitly attributed this to CLARA's organisational alignment effect.
- HD model adoption data point: 21 customers using HD models in production (out of 111 with HD models). Acknowledged this number is rough and the focus of Monday's programme review.
- Natalia Plant explained the weekly programme review discipline that started in January — CSMs know data they enter drives the weekly agenda and is visible to senior leadership.
- Azmain demonstrated the AI agent swarm approach (30 agents with a project manager orchestrator, team leads, and worker agents) used to build CLARA's reporting system. Showed the visual architecture of the swarm.
- Future vision shared: per-customer AI agents that understand individual account context and suggest blocker solutions, plus automated feedback-to-PR pipeline where AI reads the codebase, creates a fix, and a human just reviews.
- Ben Brookes noted the LLM analysis hit the edge of what it could do with existing blocker data — the data quality of blocker descriptions limits thematic analysis quality. Team actively rewriting blockers with better structure.
- Gainsight relationship explained to the audience: CLARA is IRP-specific, Gainsight is overall CSM BAU. They are complementary, not competing. Bi-directional sync planned.
- Azmain announced all ~4,000-5,000 people under Andy Frappe have been imported as viewers — anyone can log in with SSO to see everything. Only certain people have edit access.
- Julie asked about deeper blocker theme analysis — led to discussion of per-customer agents as next step
- Ollie asked what product/engineering teams can do to contribute — Ben asked for adoption-relevant customer intel, familiarity with adoption squads, and reducing duplicate data entry

## Decisions Made
- All users under Andy Frappe (~4,000-5,000) imported as CLARA viewers with SSO → Azmain
- Call chat to remain as a living channel for questions and feedback → Azmain
- User Voice integration to be explored as a future data source for CLARA → Ben Brookes
- Per-customer AI agents for blocker analysis to be developed as next AI feature → Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Share CLARA demo slides and presentation deck in call chat | Azmain | Immediate | Open |
| Set up feedback submission channel/process for product & tech teams | Azmain | This week | Open |
| Explore User Voice data integration into CLARA | Azmain/Ben | TBD | Open |
| HD model adoption data deep-dive at Monday's programme review | Natalia/Ben | Monday 17 Mar | Open |
| Rewrite blocker descriptions with better structure for thematic analysis | CSMs/Natalia | Ongoing | Open |

## Stakeholder Signals
- **Cihan** — Full champion. Personally uses CLARA daily, brought his entire team to see it, and explicitly encouraged everyone to explore and give feedback. His framing around pod structure and customer obsession positions CLARA as a strategic enabler, not just a reporting tool. This is the strongest product/tech endorsement the programme has received.
- **Ben Brookes** — Strategic and measured in presenting to a technical audience. Focused on the structured data approach rather than AI features. Honest about data quality limitations of LLM analysis. Positioned CLARA as a collaborative tool, not just a CS tool.
- **Natalia Plant** — Brief but impactful interjection about programme governance discipline. Credited the early adoption of CLARA (before it was polished) as key to its current success.
- **Ollie** — Asked the ideal question about how product teams can contribute. Shows genuine interest in cross-functional collaboration.
- **Julie** — Asked penetrating question about blocker theme granularity. Shows product thinking about the data quality problem.
- **Azmain** — Confident presenting to a large technical audience. The agent swarm demonstration was bold — showing the AI development methodology to the product team. His revelation about the token cost ("one of the reasons I ran through my monthly allowance in two days") was characteristically candid.

## Open Questions Raised
- Can CLARA's blocker data granularity extend to specific model types and validation status?
- How will User Voice integration avoid conflating different business requirements?
- What is the right feedback channel for product/engineering teams to contribute to CLARA?
- Could CLARA's approach extend beyond IRP to other product adoption use cases (Treaty IQ, Exposure IQ, Data Vault, Cape)?

## Raw Quotes of Note
- "I honestly believe because of Clara, we've done more than half of our yearly target in less than Q1." — Azmain, attributing migration success to CLARA
