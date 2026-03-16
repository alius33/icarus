# Tracker Stand Up
**Date:** 2026-02-20
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (Speaker 1)
**Duration context:** Short (~16 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Ben Brookes has dropped a surprise: he is meeting Andy Frappe (President of Moody's Analytics, one level below the board) on Monday 23 Feb to demo CLARA. None of the dev team knew this was coming. Richard is visibly alarmed.
- Critical data issues discovered in production:
  1. **Orphan records** causing API failures
  2. **Duplicate customer accounts** created during the golden source data import -- happened only in production, not in dev/staging. The import was careful not to overwrite existing data (which it achieved) but inadvertently created duplicate account records.
- Azmain discovers the blockers page was making 60+ individual API calls (one per action plan ID) rather than a batch query. He optimised this to a single joined query -- a significant performance fix that reveals the AI-as-junior-developer pattern.
- Richard proposes a soft-delete approach for duplicate records: add an inactive/dead status flag rather than hard-deleting. This is safer, allows reconciliation later, and avoids the risk of cascading deletes breaking referential integrity.
- BenVH will take a snapshot of production and restore it to staging so the team can test the fix safely before deploying to production on Monday before the Andy Frappe demo.
- Richard raises the broader need for a regression test suite and performance testing using agents to simulate CSM usage at different throughput levels. They have run five performance efficiency analyses already and still missed the 60-call problem.
- Azmain suggests the performance analysis needs a dedicated skill or prompt that tells the LLM what to look for, rather than generic "find efficiencies" instructions.
- Richard mentions Idris (banking equivalent) wants to demo to his senior leadership -- the team has been talking up their work and feels obligated to deliver. This creates external pressure beyond the Andy Frappe demo.
- Richard suggests BenVH could visit the UK; BenVH is open to the idea but just returned from Poland.
- The fix is planned for Monday morning in staging, then deployed to production before the 3pm UK time programme review.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Use soft-delete approach for duplicate records (status flag, not hard delete) | Technical architecture | High | Richard (proposed), Azmain (implementing) |
| BenVH to snapshot production and restore to staging for safe testing | Operations | High | BenVH |
| Fix to be tested Monday morning, deployed to prod before Andy Frappe demo | Deployment timing | High | Azmain / Richard |
| Regression test suite to be set up as a Monday priority | Quality assurance | Medium | Richard / Azmain (aspirational given Monday pressure) |
| Blocker page API optimisation (60 calls -> 1) to be deployed | Performance | High | Azmain |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Snapshot production database and restore to staging | BenVH | Tonight (20 Feb) | Open | High -- BenVH committed |
| Implement soft-delete status for duplicate accounts | Azmain / Richard | Monday 23 Feb morning | Open | High -- approach is clear |
| Deploy blocker page API optimisation (60 calls -> 1) to prod | Azmain | Monday 23 Feb | Open | High -- fix already written |
| Set up regression test suite and performance testing | Richard / Azmain | Next week | Open | Low -- likely to be deprioritised by Monday pressure |
| Find time for Ben's Monday Andy Frappe demo | Richard | Monday 23 Feb | Open | High -- must happen |
| Clean up orphan data causing API failures | Azmain | Monday 23 Feb | Open | Medium -- scope unclear |
| Standardise data import process to prevent duplicate creation | Azmain / BenVH | TBD | Open | Low -- important but not urgent |

## Theme Segments
| Time Range | Theme | Key Participants |
|------------|-------|-----------------|
| 0:00-2:26 | Andy Frappe bomb: surprise demo on Monday, data quality panic | Richard (alarmed), BenVH (learning) |
| 2:26-5:38 | Performance fix discovery (60 API calls), blocker page optimisation | Azmain (technical), BenVH |
| 5:38-6:50 | Broader discussion: regression tests, CICD pipeline, AI testing inadequacy | Richard, Azmain, BenVH |
| 6:50-10:26 | Duplicate account problem: golden source import created duplicates in prod only | Azmain, BenVH |
| 10:26-13:11 | Soft-delete solution, staging snapshot plan, Monday deployment timeline | Richard (directing), BenVH (offering) |
| 13:11-15:18 | Idris app delivery, UK visit suggestion, wrap-up | Richard, BenVH |

## Power Dynamics
- **Richard controls the conversation** -- he frames the Andy Frappe demo as a crisis, proposes the soft-delete solution, and directs the response plan. Despite not being the developer, he is making architectural decisions in real-time.
- **Azmain is the problem-solver under pressure** -- he found the 60-call performance issue and fixed it, and he is transparent about the duplicate account problem. He operates at the tactical level while Richard operates at the strategic level.
- **BenVH is the infrastructure enabler** -- he cannot fix the data issues himself but provides the critical capability (database snapshots, staging environment) that makes safe testing possible. His offer to snapshot production immediately is the right response.
- **Ben Brookes (absent but driving the crisis)** -- his decision to demo to Andy Frappe without telling the dev team is the source of all Monday pressure. This is characteristic of his "just do it" approach but creates real risk for the team.

## Stakeholder Signals
- **Richard Dosoo:** Visibly alarmed by the Andy Frappe demo timing. His first instinct is to assess risk ("what's the safest and least risky way?"), not to rush a fix. This is the "don't break things" posture he adopted in recent weeks. Also carrying guilt about Idris -- the team has made promises they have not delivered on.
- **Azmain Hossain:** Problem-solving efficiently under pressure. His insight about needing AI skills/prompts for performance analysis rather than generic instructions shows growing sophistication in how he uses AI tools. Pragmatic about the duplicate account issue -- "we achieved our purpose, everything is totally as it was."
- **BenVH:** Collaborative and solution-oriented. His offer to snapshot production immediately demonstrates competence and willingness to work late. He is the calm technical anchor in what is otherwise a panicked conversation.
- **Ben Brookes (absent):** His unannounced Andy Frappe demo is a high-risk, high-reward move. If it goes well, CLARA gets executive visibility at the highest level. If orphan data causes an API failure during the demo, it could damage programme credibility at the worst possible level.
- **Andy Frappe (absent):** President of Moody's Analytics, one level below the board. This is the highest-stakes audience CLARA has ever had. His reaction to the demo is an open question that will shape the programme's trajectory.

## Commitments Made
| Commitment | Who | To Whom | Specificity |
|------------|-----|---------|-------------|
| Will snapshot production and restore to staging tonight | BenVH | Richard / Azmain | Tonight |
| Will implement soft-delete fix Monday morning | Azmain / Richard | Team | Monday morning |
| Will be available in ~2 hours if issues arise | Richard | BenVH | Specific timeframe |
| Will set up a conversation about Idris's app next week | Richard | BenVH | Next week |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of purpose | 5 | Crystal clear: prepare for Andy Frappe demo, fix data issues |
| Decision quality | 4 | Soft-delete approach is sound; staging snapshot is the right safety measure |
| Participation balance | 4 | Three people, all contributing their expertise appropriately |
| Action item specificity | 4 | Clear owners, specific deadlines (tonight, Monday morning) |
| Time efficiency | 5 | 16 minutes, covered everything needed, no wasted time |
| **Overall** | **4.4** | Highly efficient crisis response meeting. The team works well under pressure. |

## Risk Signals
| Risk | Severity | Type |
|------|----------|------|
| Andy Frappe demo with unresolved data quality issues -- highest-stakes audience ever | CRITICAL | Stakeholder |
| Orphan records causing API failures that could occur during live demo | CRITICAL | Technical |
| Duplicate accounts visible in production -- confusing for anyone viewing the data | HIGH | Data quality |
| Import created duplicates only in prod, not staging -- untested production path | HIGH | Deployment process |
| No regression test suite exists -- five performance analyses missed the 60-call issue | HIGH | Quality assurance |
| AI-generated code exhibits junior developer patterns (60 individual queries instead of joins) | MEDIUM | Code quality |
| Idris has made promises to banking leadership that the team has not delivered on | MEDIUM | Stakeholder |
| No standardised data import process -- each import is ad hoc and risky | MEDIUM | Process |
| Team working late on a Thursday to fix Friday/weekend issues -- unsustainable pace | MEDIUM | Team health |

## Open Questions Raised
- What time is Ben's meeting with Andy Frappe on Monday? (Hard deadline needed)
- Why did the import create duplicate records only in production and not in staging?
- When will the standardised data import process be built to prevent recurrence?
- How do you build a performance test suite that catches the kind of issues AI code generates?
- What does Azmain mean by needing a "skill" for performance analysis -- is there a specific framework?

## Raw Quotes of Note
- "Ben dropped the fucking surprise bomb on us that he's meeting with Andy Frappe on Monday to demo Clara." -- Richard Dosoo, on the surprise escalation
- "That's such an AI thing... it's straight up a junior developer." -- BenVH, on the 60-individual-API-calls pattern
- "We need to have a performance test suite that we've run, right? That actually we know... without that baseline of tests, how do you know what we've done works?" -- Richard Dosoo, on the absence of systematic testing
- "We achieved our purpose. Everything is totally as it was, no data was touched." -- Azmain, silver-lining the duplicate import problem

## Narrative Notes
This is a crisis management meeting disguised as a standup. Ben Brookes's decision to demo CLARA to Andy Frappe -- the President of Moody's Analytics, one level below the board -- without informing the development team is the single most consequential event of the week. It transforms a routine data quality discussion into an urgent production fix with the highest possible stakes.

The team's response reveals their crisis mode dynamics. Richard immediately shifts to risk assessment, not panic. He proposes the soft-delete approach (safe, reversible, no cascading risks) and ensures a staging environment is available for testing. Azmain has already found and fixed the most visible performance issue (60 API calls reduced to 1 join query). BenVH offers the critical infrastructure support (production snapshot) without hesitation. This is a team that has been through enough fires to know how to respond.

The 60-API-call discovery is emblematic of a larger problem. Azmain notes they have run five performance efficiency analyses on the codebase and still missed this. BenVH's observation that it is "such an AI thing" is both funny and important -- AI-generated code produces working but naive solutions that require human oversight to catch. Azmain's insight about needing dedicated skills or prompts for performance analysis (rather than generic "find efficiencies" instructions) is a meta-learning moment: the team is developing an understanding of how to use AI tools effectively, including knowing their failure modes.

The duplicate account problem reveals a process gap that is common in early-stage tools: production data has different characteristics than staging data (more records, more edge cases, different import histories). The team did not think to check for duplicate creation because the staging import did not produce it. This is a testing philosophy problem, not a coding problem.

The Idris thread is a secondary but important concern. The team has been promoting CLARA to banking leadership, creating obligations that are now in tension with the CLARA stabilisation work. Richard's guilt about this is palpable -- he knows they need to deliver, but every new commitment competes with the same finite bandwidth.

What is absent from this conversation is any discussion of what happens if the demo goes badly. The team is focused on making the data clean enough for Monday, but there is no contingency plan for API failures during a live demo to the President of Moody's Analytics. This is a gap that reflects the programme's general optimism bias -- they plan for success but do not prepare for failure.
