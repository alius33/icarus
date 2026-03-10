# Chat with Ben
**Date:** 2026-01-23
**Attendees:** Ben Brooks, Azmain Hossain
**Duration context:** Short (~10 minutes)
**Workstreams touched:** WS2 CLARA (UI fixes)

## Key Points
- Ben reviews the CLARA dashboard and identifies multiple UI confusion issues:
  - Red background colours on account cards are being confused with RAG status — they actually indicate stale/old update dates
  - A blue RAG status pill is superfluous alongside the coloured top bar
  - Data completeness percentage (e.g. "45") shown without a label — needs to say "data completeness 45%"
  - Duplicate colour coding: red background + amber top + red side bar on the same card
- Ben proposes cleanup: keep the coloured top bar for RAG status, remove background colours entirely, keep hover-over tooltips for data completeness (which are actually useful)
- Discussion of the list view vs card view — Ben prefers keeping the widget cards as they are interactive and clickable
- Azmain is blocked on Cursor: "your team has hit its user limit" error. They discuss workarounds (Richard using personal Claude Code account, getting corporate licence approval)
- Ben asks about edit restrictions (can only edit your own accounts) — not yet implemented due to lack of SSO-to-user mapping
- Developer laptops approved for delivery on Tuesday
- Ben mentions Diya may be unhappy about the developer laptop request, anticipating she will question focus

## Decisions Made
- Strip background colours from account cards on dashboard → Azmain
- Remove the blue RAG status pill (keep the coloured top bar) → Azmain
- Add "data completeness" label to the percentage pill → Azmain
- Keep card widgets rather than switching to list view → Ben, Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Fix dashboard colour/RAG confusion | Azmain | Before Monday | Open |
| Add data completeness label to percentage pill | Azmain | Before Monday | Open |
| Resolve Cursor token/licence block | Richard / Azmain | Urgent | Open |

## Stakeholder Signals
- Ben is doing hands-on UX testing himself — first real usability review of the dashboard
- Azmain acknowledges no formal UX testing has been done: "nobody's done like UX testing on this"
- Ben frames the first week of CSM use as effectively being the UX test

## Open Questions Raised
- Why does the red side bar appear on some accounts but not others?
- When will Cursor licence issues be resolved?

## Raw Quotes of Note
- "DIA is going to hit the roof. Today, I've submitted a request for a developer laptop" — Ben Brooks, anticipating pushback from Diya on his focus
