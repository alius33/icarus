# AI Discussion with Asset Management
**Date:** 2026-02-04
**Attendees:** Richard Dosoo, Azmain Hossain, Amanda Fleming (KYC/Asset Management), George Dyke, Sean, Martin Davies (phone), BenVH (phone), Bernard, Rhett, others from insurance and KYC teams
**Duration context:** Long (~43 minutes)
**Workstreams touched:** WS2 CLARA, WS3 CS Agent

## Key Points
- Cross-OU session: Richard and Azmain presented CLARA to Amanda Fleming's KYC team, who have already automated their customer management -- they are far ahead of insurance
- Amanda demonstrated her own tool -- vastly feature-rich, built in Cursor with GPT-4: client health dashboards, AI-generated tasks from meeting notes, engagement tracker, renewals management, contract parsing, prospecting pipeline with trial tracking, AI recommendations based on all account data
- Amanda's tool does things CLARA does not: auto-parses contracts for key dates/fees, tracks engagement frequency vs expectations, generates client-ready renewal proposals, creates weekly project reports
- Critical governance gap: Amanda's tool has NO authentication -- BenVH flagged this as a serious risk for Moody's data
- Azmain noted Amanda's tool is built for a power user (herself and one colleague) -- would not scale to 40 CSMs without major UX rework
- Richard connected both teams to Sales Recon: the Intelligence Anywhere feature will build the Salesforce data pipeline -- CS teams should be downstream consumers, not building their own integrations
- Decision: no merging of CLARA and Amanda's tool -- compartmentalisation with shared data pipelines preferred given rapid iteration needs
- Richard proposed app comparison via Claude-generated functional specs to identify feature deltas
- Sean's team (KYC) has already built a self-service app deployment platform called "Usher" -- ahead on infrastructure
- George's observation about Gainsight: Amanda's tool makes him question what Gainsight offers -- a politically dangerous sentiment

## Decisions Made
- **No merging of apps -- compartmentalisation with shared data pipelines** | Type: Architecture/Strategic | Confidence: High | Owner: Team
- **Amanda/Sean added to Sales Recon UAT and cadence** | Type: Coalition-building | Confidence: High | Owner: Richard
- **Cross-OU Teams channel to be created** | Type: Process | Confidence: High | Owner: Richard
- **App comparison via Claude-generated functional specs** | Type: Analysis | Confidence: Medium | Owner: Richard/Azmain

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Add Amanda/Sean to Sales Recon UAT pilot | Richard | This week | Open | High |
| Create cross-OU Teams channel for collaboration | Richard | This week | Open | High |
| Get Amanda to run product definition prompt on her app | Richard | This week | Open | Medium |
| Compare functional specs of CLARA vs Amanda's tool | Azmain/Richard | Next 2 weeks | Open | Medium |
| Set up follow-up meeting with Sales Recon including KYC | Richard | Next week | Open | High |

## Theme Segments
1. **Introduction and CLARA Demo (0:00-10:00)** -- Richard and Azmain present CLARA, data sources, authentication approach
2. **Amanda's Tool Demo (10:00-27:00)** -- Extensive walkthrough of KYC management platform
3. **Sales Recon Alignment (27:00-35:00)** -- Connecting both teams to the Intelligence Anywhere pipeline
4. **App Convergence Discussion (35:00-43:00)** -- Merge vs compartmentalise, next steps

## Power Dynamics
- **Richard** is the convener and coalition-builder -- he brought the OUs together and is shaping the narrative about shared infrastructure
- **Amanda** is technically impressive but politically naive -- she built a powerful tool without considering governance, authentication, or Gainsight implications
- **BenVH** plays the governance conscience -- his authentication concern is the one reality check in the room
- **George** asks the dangerous question about Gainsight's value -- his instinct is correct but the statement is politically risky
- **Sean** is quietly ahead on infrastructure with the Usher platform

## Stakeholder Signals
- **Amanda Fleming:** A natural ally for cross-OU collaboration but a governance risk (no authentication, no security review). Her tool's existence is both opportunity and threat. If Gainsight discovers it, the political fallout could be significant.
- **George Dyke:** His spontaneous questioning of Gainsight's value based on what Amanda has built reveals his pragmatic thinking -- but this sentiment must be managed carefully.
- **BenVH:** The only person in the room thinking about security. His flag about authentication is critical and could prevent a future governance crisis.
- **Sean (KYC):** Has built app deployment infrastructure (Usher) that could complement BenVH's app factory. A potential technical alliance.
- **Bernard:** Quietly observing, will need integration into the broader effort.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| Richard | Add Amanda/Sean to Sales Recon UAT | Amanda/Sean | Firm |
| Richard | Create cross-OU Teams channel | All | Firm |
| Richard | Set up Sales Recon follow-up meeting | All | Firm |
| Amanda | Run product definition prompt on her app | Richard | Moderate |

## Meeting Effectiveness
- **Clarity of purpose:** 8/10 -- Good cross-OU knowledge sharing
- **Decision quality:** 8/10 -- Compartmentalisation decision is pragmatic and correct
- **Follow-through potential:** 7/10 -- Multiple action items across OUs, coordination complexity high
- **Stakeholder alignment:** 7/10 -- Good within the room, but Gainsight and Sales Recon not present
- **Time efficiency:** 8/10 -- Dense meeting with lots of content in 43 minutes

## Risk Signals
- **Gainsight political threat is now live.** George's comment questioning Gainsight's purpose, combined with Amanda's tool existing without governance, creates a dual threat. If Gainsight discovers Amanda's tool, it is a far bigger problem than CLARA. Severity: HIGH
- **Authentication gap in Amanda's tool** -- Moody's data stored in an unauthenticated application. If this is discovered by security or compliance, it could result in a shutdown order. Severity: HIGH
- **Cross-OU coordination complexity** -- Multiple OUs building similar tools independently. Without governance, this becomes shadow IT. Severity: MEDIUM
- **Sales Recon dependency** -- Both teams are deferring integration work to wait for Sales Recon pipeline. If Sales Recon is delayed, both teams are stuck. Severity: MEDIUM

## Open Questions Raised
- Should the OUs coordinate on a single app or maintain separate apps with shared data?
- How to handle Amanda's tool from a governance perspective?
- When will Sales Recon Intelligence Anywhere be available for CS consumption?
- How to position CLARA and Amanda's tool relative to Gainsight without triggering institutional resistance?

## Raw Quotes of Note
- "When I see this, I wonder what the purpose of Gainsight is, actually, because this is much richer" -- George, the dangerous observation about Amanda's tool vs enterprise platforms
- "Compartmentalisation makes more sense... if we structurally fix the problems of having an endpoint, having the data pipeline" -- Azmain, articulating the architecture principle

## Narrative Notes
This session is one of the most significant of the week. Amanda's tool demonstration is a revelation -- she has built, essentially alone, a customer management platform that surpasses what the enterprise Gainsight implementation offers. The gap between what one motivated CSM with Cursor can build in weeks versus what an enterprise implementation delivers in months is stark, and everyone in the room notices it. George's unguarded comment about Gainsight's value is the elephant in the room: if these tools are better, faster, and cheaper, what is the enterprise platform for? The answer -- governance, scale, single source of truth -- is correct but unsexy. Richard's instinct to compartmentalise rather than merge is sound: it preserves agility while acknowledging the need for shared infrastructure. But the unspoken risk is that Amanda's tool, with no authentication and no security review, is a ticking governance bomb. If Moody's security discovers it, the fallout will affect not just Amanda but the entire cross-OU AI initiative.
