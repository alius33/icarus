# Program Review with Rich
**Date:** 2026-01-12
**Attendees:** Richard Dosoo, Azmain Hossain
**Duration context:** medium (~3500 words)
**Workstreams touched:** WS1 (Programme Governance), WS2 (CLARA/Adoption Tracker), WS4 (Sales Recon Convergence), WS6 (AI Enablement)

## Key Points
- Richard and Azmain reviewing pre-read slides for the January 26 executive meeting with Mike Steele, Colin Holmes, and Ari la Harvey (Sales Recon)
- Discussion of ROI framing: Ben Brooks frames CLARA as a "value at risk" model -- managing a pipeline of 40 customers worth significant GMB; without tooling, implementations risk failure
- Azmain estimates 30-40% CSM capacity unlock from the Gen AI initiative alone, with more once Gainsight integration happens
- Critical blocker identified: Natalia Plant has communicated that Gainsight/Salesforce API access is blocked due to cybersecurity concerns; no programmatic access until internal review completes (possibly March)
- Strategy agreed: build data model internally in CLARA, accumulate data, then push to Gainsight when API access opens
- Idris (banking CS counterpart) is 4-5 months ahead -- has documented requirements and is prototyping in Cursor, but lacks infrastructure/CICD pipeline
- Plan to consolidate insurance and banking requirements before presenting to Sales Recon team
- Discussion of various AI models: Richard using Opus in Claude Code ("Max Max" plan at 4x cost), Azmain using Gemini for presentations; both noting model quality differences
- Idris coming to London the week of January 26 -- workshops planned for convergence discussions

## Decisions Made
- **ROI messaging for Jan 26 meeting**: Frame as value-at-risk model for managed pipeline + CSM capacity unlock -> Richard/Azmain/Ben to align
  - **Type:** implicit
  - **Confidence:** MEDIUM
- **Gainsight integration deferred to post-March**: Build internally, push data when API access opens -> Richard
  - **Type:** explicit
  - **Confidence:** HIGH
- **Consolidated requirements with banking**: Insurance and banking to reconcile requirements before presenting to Sales Recon -> Richard/Idris
  - **Type:** explicit
  - **Confidence:** HIGH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Forward Gainsight API thread to Azmain | Richard | 2026-01-12 | Open | HIGH |
| Draw up cross-workstream stakeholder map (RACI) | Richard/Azmain | 2026-01-19 | Open | MEDIUM |
| Prepare consolidated slides for Jan 26 exec meeting | Richard/Azmain | 2026-01-24 | Open | HIGH |
| Record stakeholder mapping call for AI transcription | Azmain | 2026-01-19 | Open | MEDIUM |
| Schedule workshops with Idris during London visit (Jan 26 week) | Richard | 2026-01-20 | Open | HIGH |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| ROI framing for executive meeting | strategic | "the ROI is actually, you know, you managing a pipeline of 40 customers, which is x GMB" -- Richard | HIGH |
| Gainsight API blocker | technical | "they can't give any API access. It needs to go through internal review" -- Azmain referencing Natalia | HIGH |
| Banking convergence with Idris | strategic | "he's about four or five months ahead of us" -- Richard on Idris | HIGH |
| AI model quality comparison | operational | "there is a real difference" -- Richard comparing Opus to ChatGPT | MEDIUM |
| Adoption charter commercial value | strategic | "it is going to affect the commercial negotiations" -- Azmain | MEDIUM |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Richard Dosoo | Strategic lead, framing executive narrative | Setting agenda, defining ROI language, managing stakeholder sequence | 60% |
| Azmain Hossain | Programme manager, technical bridge | Challenging assumptions, proposing practical solutions | 40% |
| Ben Brooks (referenced) | Product visionary (absent but influential) | ROI framing cited by Richard as "value at risk" model | N/A |
| Natalia Plant (referenced) | Gatekeeper for API access | Blocked Gainsight/Salesforce programmatic access | N/A |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Richard | Energised, strategic | Stable | Executive meeting prep | Confident in framing, eager to align stakeholders pre-meeting |
| Azmain | Pragmatic, sceptical | Stable | Gainsight blocker | "I'm telling you right now" -- Gainsight will be late |
| Natalia Plant (ref) | Blocking | Stable | API access | Communicated no access until security review completes |
| Bernard (ref) | Frustrated with Gainsight | Stable | Tool adoption | 3 years pushing Gainsight adoption, only ~50% |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Richard | Will create stakeholder RACI across all workstreams | Before Jan 26 meeting | None | MEDIUM |
| Azmain | Will prepare slides and storyboard | End of week (Jan 17) | Richard provides content | HIGH |
| Richard | Will schedule Idris workshops for London visit | Before Jan 26 | Idris confirms travel | HIGH |

## Meeting Effectiveness
- **Type:** Strategic planning / pre-read review
- **Overall Score:** 72
- **Decision Velocity:** 0.6
- **Action Clarity:** 0.5
- **Engagement Balance:** 0.7
- **Topic Completion:** 0.6
- **Follow Through:** 0.5

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-012 | New | Gainsight API access blocked indefinitely | HIGH | Stable | Technical/Policy | HIGH |
| R-013 | New | No group-wide ROI metric exists for AI initiatives | MEDIUM | Stable | Governance | HIGH |
| R-014 | New | Personal AI licence costs unsustainable without enterprise agreement | MEDIUM | Escalating | Financial | HIGH |

## Open Questions Raised
- When exactly will Gainsight API access be available? (March is hopeful but uncertain)
- How to demonstrate value without Salesforce/Gainsight integration in the interim?
- What is the group-wide ROI measurement framework for AI initiatives?
- Can Natalia and Ben push for earlier API access?

## Raw Quotes of Note
- "the ROI is actually, you know, you managing a pipeline of 40 customers, which is x GMB... without this tooling, they're not going to get managed correctly" -- Richard, on Ben's value-at-risk framing
- "I'm telling you right now" -- Azmain, predicting Gainsight will be late
- "So it's a pile of dog shit, and we're waiting for it" -- Richard, on Gainsight adoption state
- "we can't... it's not sustainable for us to all do that" -- Richard, on everyone buying personal AI licences

## Narrative Notes
This meeting reveals the strategic tension at the heart of the programme: the team needs Salesforce/Gainsight integration to demonstrate full value, but security policy blocks API access. Richard and Azmain are building around this constraint by accumulating data internally, but this creates a dependency risk -- if Gainsight access doesn't materialise by March, the demo narrative weakens significantly. The banking convergence with Idris represents a smart political move: presenting a unified cross-OU requirement to Sales Recon carries more weight than insurance alone. Richard's energy level is high as he orchestrates multiple stakeholder threads for the January 26 meeting, though the sheer number of coordination tasks risks something falling through the cracks. The personal AI licence discussion foreshadows a recurring theme -- the team is spending personal money on Claude/Cursor subscriptions because enterprise procurement hasn't kept pace with their needs.
