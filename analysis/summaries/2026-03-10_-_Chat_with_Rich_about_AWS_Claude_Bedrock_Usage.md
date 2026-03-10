# Chat with Rich about AWS Claude Bedrock Usage
**Date:** 2026-03-10
**Attendees:** Richard Dosoo, Azmain Hossain
**Duration context:** Short (~800 words)
**Workstreams touched:** WS2 CLARA, App Factory, Infrastructure

## Key Points
- AWS Bedrock costs have hit **$1,163 in the first two weeks of March** — on track to reach $10K by month end at current pace
- Cost breakdown: primarily Claude Opus 4.5/4.6 usage (most expensive), plus Sonnet usage from Ben's Slidey presentation app and Richard's local builds
- The cost tracking infrastructure is broken — **tags are not set correctly** on the AWS accounts, making it impossible to break down costs by project or API key
- Discussion about getting individual Max subscriptions ($200/person) as a more cost-efficient alternative to Bedrock for personal usage — Azmain's personal Max subscription provides unlimited usage for his non-work builds
- Current Bedrock key is shared across everyone: Azmain, Richard, Ben, Martin, Nikhil — no per-user or per-project cost attribution
- Richard acknowledged this needs to become "the second highest cost across the whole month" issue resolved urgently
- Call cut short — Richard had to jump to an Idris onboarding call

## Decisions Made
- Need to urgently implement proper AWS cost tagging for Bedrock usage → Richard / BenVH
- Explore Max subscription model as alternative for individual developers → Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Fix AWS Bedrock cost tags for per-project/per-user attribution | BenVH / Richard | Urgent | Open |
| Evaluate Max subscription vs Bedrock for cost efficiency | Richard | This week | Open |
| Set up cost allocation monitoring before month end | Richard | End of March | Open |

## Stakeholder Signals
- **Azmain** — Pragmatic about cost management. Already using personal Max subscription for non-work builds. Recognises the $10K trajectory is unsustainable.
- **Richard** — Concerned about optics and sustainability. This is becoming a budget visibility problem, not just a spending problem.

## Open Questions Raised
- Can AWS Cost Explorer be configured to show Bedrock spend by API key or tagged project?
- Is the Max subscription model viable for corporate use, or does it create the same personal-account compliance issue?

## Raw Quotes of Note
- "We're going to hit a point where the costs are going to start to become an issue" — Richard, on the $10K trajectory
