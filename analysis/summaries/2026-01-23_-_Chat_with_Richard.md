# Chat with Richard — Employee Mapping and Tool Access
**Date:** 2026-01-23
**Attendees:** Richard Dosoo, Azmain Hossain
**Duration context:** Short (~12 minutes)
**Workstreams touched:** WS2 CLARA (data, team assignments, infrastructure)

## Key Points
- Richard had rushed through the employee data mapping, admitting he did not review it carefully because he was heading to Jummah prayer — the initial mapping attempted to add organisation levels but was messy
- Azmain needed to expand the employee database to include solution architects and implementation leads (beyond just CSMs) per Ben's request for account teams
- Agreed that the people lookup field would be open to all employees rather than role-filtered — Azmain would trust users not to assign inappropriate people to roles
- Richard proposed adding a role column to the people table, but Azmain pushed back citing the risk of schema changes before Monday and the database breaking with BenVH unavailable
- Azmain compromised: he would make three exact copies of the CSM assignment model (for implementation lead, solution architect, etc.) that pull from the entire employee database with search functionality
- Richard confirmed BenVH would be working in the same timezone for the next couple of weeks from Amsterdam, which would improve collaboration
- Both agreed any risky schema changes should wait until after Monday — get BenVH's approval first
- Richard attempted to share his Claude Code credentials with Azmain since Cursor was blocked — Google SSO authentication made this impossible without creating a new account
- Richard planned to raise an Azure access ticket for Azmain to get backend logs

## Decisions Made
- **Open people selection (no role filtering) for Monday** (type: tactical, confidence: high) — trust users to assign correctly rather than risk schema changes
- **Defer role column addition to people table** (type: risk management, confidence: high) — avoid schema changes before Monday demo
- **Richard to purchase Claude Max Pro for Azmain** (type: resource, confidence: high) — workaround for Cursor block using personal email account
- **Schema changes only after BenVH review and approval** (type: governance, confidence: high) — learned from previous database breaks

## Action Items
| Action | Owner | Deadline | Confidence |
|--------|-------|----------|------------|
| Map all employees under Colin into system | Azmain Hossain | 2026-01-24 | High |
| Get CSM assignments from Josh, Miles, and George | Azmain Hossain | 2026-01-24 | High |
| Raise Azure access ticket for Azmain | Richard Dosoo | 2026-01-23 | Medium |
| Purchase Claude Max Pro licence for Azmain | Richard Dosoo | 2026-01-23 | High |
| Start Teams thread with Jamie, Alexandra, Bernard for data pipeline requirements | Richard Dosoo | 2026-01-23 | Medium |
| Reconnect at 2pm to sort remaining items | Both | 2026-01-23 | High |

## Theme Segments
| Timestamp Range | Theme | Speakers | Tone |
|----------------|-------|----------|------|
| 0:00-1:30 | Employee data mapping review, rushed quality | Richard, Azmain | Apologetic, pragmatic |
| 1:30-4:00 | Solution architect and implementation lead fields — schema risk | Richard, Azmain | Technical, cautious |
| 4:00-6:00 | BenVH timezone overlap, post-Monday plan | Richard, Azmain | Planning, relieved |
| 6:00-9:00 | Claude Code credential sharing attempt, Cursor blocked | Richard, Azmain | Frustrated, problem-solving |
| 9:00-11:30 | Claude authentication issues, personal account workarounds | Richard, Azmain | Exasperated, resourceful |
| 11:30-12:00 | Wrap up, Teams thread follow-up | Richard, Azmain | Brief, action-oriented |

## Power Dynamics
- **Richard Dosoo** took a caretaker role, trying to solve Azmain's tooling crisis by purchasing a licence and sharing credentials despite compliance concerns. His willingness to use his own resources showed commitment but also highlighted the absence of proper procurement channels.
- **Azmain Hossain** showed growing maturity in risk management — he explicitly refused to add new schema fields before Monday despite pressure to deliver more features, having learned from previous database failures.

## Stakeholder Signals
- **Richard Dosoo** — His admission of rushing the data mapping and his urgency to leave for prayer revealed the personal strain of the programme. His instinct to solve problems by spending personal money or sharing accounts flagged a pattern of informal workarounds substituting for proper process.
- **Azmain Hossain** — His anxiety about the database was well-founded given the history of schema changes breaking the system. His decision to make three copies of the CSM assignment model rather than add a proper role field was a defensible short-term hack, but it would accumulate technical debt.
- **BenVH** (referenced) — "We need to stop even having him as an option" — Azmain's frank statement about the dependency on BenVH for database operations highlighted the unsustainability of the current setup.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Azmain | Map all employees under Colin | Ben Brooks | High |
| Azmain | Get CSM assignments before Monday | Ben Brooks | High |
| Richard | Purchase Claude Max Pro for Azmain | Azmain | High |
| Richard | Raise Azure access ticket | Azmain | Medium |
| Both | Reconnect at 2pm | Each other | High |

## Meeting Effectiveness
- **Clarity of outcomes:** 7/10 — Clear plan for employee mapping but licence/tooling situation remained chaotic
- **Decision quality:** 8/10 — Smart decision to defer schema changes; open people selection was a reasonable compromise
- **Engagement balance:** 7/10 — Both contributed, though Richard was distracted by time pressure
- **Time efficiency:** 6/10 — Significant time spent on Claude authentication issues that were not resolved

## Risk Signals
| Risk | Severity | Signal |
|------|----------|--------|
| Development tooling completely blocked before Monday demo | CRITICAL | Azmain cannot use Cursor or Claude Code. Richard buying personal licence as workaround. Compliance risk of shared credentials. |
| Informal licence procurement creating compliance exposure | HIGH | Richard purchasing Claude Max Pro on personal card, creating accounts with personal email addresses. Ben noted "I don't think I would... he's not supposed to" about this practice. |
| Employee data quality from rushed mapping | MEDIUM | Richard admitted he did not review the data mapping — potential errors in org structure that could surface during Monday demo. |
| Schema changes as a persistent instability risk | MEDIUM | Every field addition risks breaking the database. Three-copy pattern for role assignment creates technical debt. |

## Open Questions Raised
- Can the Claude Code credential sharing workaround actually be made to work?
- When will the formal Snow ticket process deliver proper tool licences?
- How will the three-copy assignment model (CSM, implementation lead, solution architect) be consolidated later?
- Does Azmain have sufficient Azure access to diagnose backend issues independently?

## Raw Quotes of Note
- "We need to stop even having him as an option" — Azmain Hossain, on the unsustainable dependency on BenVH for database operations
- "I didn't really review it. I was just like, just let me get this done quickly" — Richard Dosoo, on the rushed employee data mapping

## Narrative Notes
This call was a microcosm of the programme's operational reality: a developer blocked from his tools, a programme manager buying personal licences to unblock work, and both people making pragmatic compromises to ship before Monday. The Cursor/Claude Code licence crisis had now consumed significant time across multiple calls — Ben's call earlier, this call with Richard, and the eventual resolution would eat into the Pre-Monday Demo Discussion. Azmain's growing caution about schema changes was a healthy evolution from the earlier attitude of moving fast and breaking things — he had learned from the deployment synchronization failures earlier in the week. Richard's attempt to share Claude Code credentials, while well-intentioned, crossed into territory that both acknowledged was problematic from a compliance perspective. The programme was operating on the kind of informal resource allocation that works in a startup but creates liability in an enterprise context.
