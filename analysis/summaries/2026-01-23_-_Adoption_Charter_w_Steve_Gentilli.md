# Adoption Charter with Steve Gentilli
**Date:** 2026-01-23
**Attendees:** Azmain Hossain, Steve Gentilli
**Duration context:** Long (~50+ minutes)
**Workstreams touched:** WS4 Friday (Adoption Charter)

## Key Points
- Steve describes the current adoption charter tracking: a standalone Excel tool with columns for region, sales manager, client director, client name, active status, sales stage, solution architect, implementation basis, partner info, and adoption charter status
- Significant overlap discovered: roughly 15 out of 20 columns Steve is tracking already exist in CLARA's database. Only ~5 need to be added (sales stage from Salesforce, MPN specialist, implementation basis/partner fields, adoption charter status)
- Steve is enthusiastic about folding the adoption charter tracking into CLARA rather than maintaining a parallel Excel — it eliminates data duplication
- Azmain demonstrates the adoption charter section that Ben has already partially built in CLARA: success criteria tracking, milestones, blueprints, roles and responsibilities, with use cases linked to charters
- Two modes for adoption charters: (1) build in Word, then upload and auto-extract fields; (2) build directly in the app with full audit trail, then export as PDF
- Steve offers to help with data modelling given his experience building databases and systems
- Azmain explains that employee mapping under Colin Holmes is in the app — allows assigning solution architects, implementation leads, etc. to accounts
- Discussion of partner tracking: need a section for partner information (introduced, selected, reason for non-selection) — Alexandra is also working on this
- Steve suggests manual status fields for adoption charter stages rather than algorithmic rules, since the number of criteria varies by customer
- Live demo had a hiccup: use cases page failed to load, customers briefly disappeared — revealing ongoing instability
- Steve agrees to send his Excel tracker data (first 10 rows) for cross-referencing with CLARA fields

## Decisions Made
- Adoption charter tracking will be folded into CLARA rather than maintained as a separate Excel → Steve, Azmain
- Additional columns (sales stage, MPN, implementation basis, partner fields, charter status) to be added to CLARA → Azmain
- Adoption charter status field should be manual/user-controlled, not algorithmic → Steve, Azmain
- Further design discussions needed with Alexandra (partners) and the broader team post-Monday meeting → Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Send first 10 rows of adoption tracker Excel with all columns | Steve Gentilli | This week | Open |
| Cross-reference Steve's columns with CLARA database fields | Azmain | After receiving data | Open |
| Set up follow-up meeting with Steve, Alexandra, and Ben to align on adoption charter design | Azmain | Post-Monday meeting | Open |
| Add implementation lead field to customer records (before Monday) | Azmain | Before Monday | Open |

## Stakeholder Signals
- Steve is genuinely enthusiastic about CLARA's potential and willing to invest time — a strong ally for WS4
- Steve has relevant database/systems experience and wants to contribute to data modelling
- This conversation marks the beginning of formally folding WS4 (Adoption Charter) into WS2 (CLARA)

## Open Questions Raised
- How will the partner tracking section work across adoption charters? (Needs Alexandra's input)
- What is the right granularity for adoption charter stages and milestones?
- How to handle the pipeline/pre-sale stage tracking within CLARA?

## Raw Quotes of Note
- "I've been amazed at how lacking data we are as an organisation in certain areas." — Steve Gentilli, on the state of data management at Moody's
