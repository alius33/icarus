# Next Steps on Dev Work with Richard
**Date:** 2026-01-23
**Attendees:** Richard Dosoo, Azmain Hossain
**Duration context:** Short (~8 minutes)
**Workstreams touched:** WS2 CLARA (infrastructure, risk management)

## Key Points
- Focused call on risk management for the Monday demo — what to change vs what to leave alone
- Richard proposes a cautious approach: do all high-risk schema changes last, so if they need to roll back, they have a stable state to return to
- Azmain agrees to write up all planned schema changes but not execute them — wait for BenVH's approval over the weekend or Monday morning
- They discuss the rollback problem: they have never tested a rollback, so attempting one could leave the system completely unusable
- Azmain fixed the use case creation issues — everything is now working again. Agrees not to push any further changes that might break things
- Strategy: write everything up, get BenVH's thumbs up, execute Monday morning before the 2:30pm call (with 1 hour buffer before the 3:30pm CSM demo)
- Richard offers to explain the situation to BenVH so he understands the caution

## Decisions Made
- No more schema changes until BenVH approves them → Azmain
- Write up all planned changes as specifications, not code → Azmain
- Defer execution to Monday morning with BenVH oversight → All
- Do not attempt untested rollbacks → All

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Write up planned schema changes for BenVH review | Azmain | This weekend | Open |
| Get BenVH approval for changes | BenVH | Monday morning | Open |
| Execute approved changes Monday morning before 2:30pm | Azmain | Monday AM | Open |
| Explain deployment caution to BenVH | Richard | This weekend/Monday | Open |

## Stakeholder Signals
- Both Richard and Azmain have shifted from "move fast" to "don't break things" — the fragility has made them cautious
- There is genuine anxiety about the Monday demo being derailed by technical failures

## Open Questions Raised
- Will BenVH be available over the weekend or Monday morning to review and approve changes?
- What is the actual rollback procedure if something goes wrong?

## Raw Quotes of Note
- "I would have preferred us to have tested the rollback procedure first, because we could leave the system in a completely unusable state" — Richard, on the risks of untested rollbacks
