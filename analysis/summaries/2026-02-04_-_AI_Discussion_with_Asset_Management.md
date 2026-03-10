# AI Discussion with Asset Management
**Date:** 2026-02-04
**Attendees:** Richard Dosoo, Azmain Hossain, Amanda Fleming (KYC/Asset Management), George Dyke, Sean, Martin Davies (phone), BenVH (phone), Bernard, Rhett, others from insurance and KYC teams
**Duration context:** Long (~43 minutes)
**Workstreams touched:** WS2 CLARA, WS3 CS Agent

## Key Points
- Cross-OU session: Richard and Azmain presented CLARA to Amanda Fleming's KYC team, who have already automated their customer management on top of a database — they're ahead of insurance
- Amanda demonstrated her own tool — vastly feature-rich, built in Cursor for her KYC team: client health dashboards, engagement tracker, renewals management, contract parsing, AI-generated task lists from meeting notes, prospecting pipeline with trial tracking, AI recommendations based on all account data
- Amanda's tool uses GPT-4 (she's not sure which model) — has AI summaries, auto-generated tasks from meeting transcripts, NPS tracking considerations
- Richard identified strong parallels: both teams need Salesforce data, usage data from MixPanel, support ticket integration
- Key concern raised by BenVH: Amanda's tool has no authentication — storing Moody's data without proper security is a risk
- Azmain noted Amanda's tool is built for a power user (herself and one colleague) — it would not scale to 40 CSMs without significant UX redesign
- Richard connected this to Sales Recon: the Intelligence Anywhere feature will build the data pipeline from Salesforce that both teams can consume — CS should be downstream consumers
- Decision to not build separate Salesforce integrations — wait for Sales Recon pipeline and consume that instead
- Action to add Amanda/Sean to Sales Recon UAT and bi-weekly cadence
- Discussion of whether to merge the apps: concluded that compartmentalisation makes more sense given rapid iteration needs, but shared data pipelines are essential
- Richard proposed comparing apps: have Claude generate a functional specification of Amanda's app, compare to CLARA's features, identify deltas

## Decisions Made
- No merging of apps right now — compartmentalisation preferred, but shared data pipelines essential → Team
- Amanda's team to be added to Sales Recon UAT and cadence → Richard
- Richard to create a cross-OU Teams channel for sharing coding standards and prompts → Richard
- App comparison via Claude-generated functional specs to identify feature deltas → Richard/Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Add Amanda/Sean to Sales Recon UAT pilot | Richard | This week | Open |
| Create cross-OU Teams channel for collaboration | Richard | This week | Open |
| Get Amanda to run product definition prompt on her app | Richard | This week | Open |
| Compare functional specs of CLARA vs Amanda's tool | Azmain/Richard | Next 2 weeks | Open |
| Set up follow-up meeting with Sales Recon team including KYC | Richard | Next week | Open |

## Stakeholder Signals
- Amanda is far ahead technically — her tool is feature-rich but built without security/governance considerations. A pioneer but a governance risk.
- George (present) drawing parallels between all the CS tools being built — recognising the convergence opportunity
- BenVH flagged the authentication gap in Amanda's tool — technically astute and security-conscious
- Sean (KYC) has built self-service app deployment — "Usher" platform for non-database apps. Ahead on infrastructure.
- The life team (George) already uses Gainsight — adds complexity to any unified approach

## Open Questions Raised
- Should the OUs coordinate on a single app or maintain separate apps with shared data?
- How to handle Amanda's tool from a governance perspective — Gainsight team may be alarmed
- When will Sales Recon Intelligence Anywhere feature be available for CS consumption?

## Raw Quotes of Note
- "When I see this, I wonder what the purpose of Gainsight is, actually, because this is much richer" — George, on Amanda's tool vs. Gainsight
