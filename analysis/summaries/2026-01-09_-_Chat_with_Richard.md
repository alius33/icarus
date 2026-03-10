# Chat with Richard
**Date:** 2026-01-09
**Attendees:** Richard Dosoo, Azmain Hossain (Ben Brooks mentioned but not directly on call)
**Duration context:** Long (~42 minutes, transcript ~345 lines)
**Workstreams touched:** WS2 (CLARA/IRP Adoption Tracker), WS1 (Training & Enablement -- discussed), WS6 (Build in Five -- mentioned)

**Note:** This transcript is nearly identical to "AWS Deployment of Adoption Tracker" from the same date (one speaker label differs). Same meeting recorded under two names.

## Key Points
- Richard shares overnight debugging work: identified RAG status breakage caused by null/zero values in customer use case status fields
- Used Claude (personal 18 pounds/month account) to analyse data model and create Python fix scripts after Cursor ran out of tokens
- AWS monthly cost confirmed at less than $100/month -- Richard sees this as trivial
- BenVH currently deploying to AWS -- target is end of his workday today
- Azmain's primary task: fill Excel spreadsheet with synthetic data for when AWS deployment completes
- Both team members using personal AI tools (Claude personal, Gemini personal) as workarounds for corporate Cursor limits
- Extensive Sales Recon meeting context: Richard walks Azmain through the Jan 26 meeting agenda, stakeholder map, and political dynamics
- Diya's warning: previous meeting with Sales Recon team produced nothing -- this one must be outcome-focused with commitments
- Richard reveals deep resource frustration: Liz blocks Martin for Canopus, Stacy blocks Martin for gap analysis, "no one wants to collaborate"
- If internal resources stay blocked, Richard will push for external contractors
- Azmain has been using AI to create programme charters and strategic documents from Richard's verbal brief -- ready for review
- Azmain articulates key insight: "AI is not going to take your job. Somebody who uses AI better than you is going to take your job"
- Richard introduces Nicole (new US-based senior engineer) as example of AI-augmented senior engineering -- used Cursor not to answer interview questions but to build a demo app
- Programme needs: stakeholder map, RACI, project plans for all five workstreams (currently only WS2 has one)
- OneDrive folder being set up for programme documentation
- Monday 11am catch-up planned for programme scope before 2pm Sales Recon prep
- Copilot presentation tips shared: use Word doc references to bypass 2000 character prompt limit

## Decisions Made
- Azmain fills Excel with synthetic data as priority: explicit -> Azmain
  - **Type:** explicit
  - **Confidence:** HIGH
- BenVH deploys to AWS today: explicit -> BenVH
  - **Type:** explicit
  - **Confidence:** HIGH
- Monday 11am for programme scope discussion: explicit -> Richard/Azmain
  - **Type:** explicit
  - **Confidence:** HIGH
- External contractors if internal resources blocked: implicit -> Richard
  - **Type:** implicit
  - **Confidence:** MEDIUM
- OneDrive folder for programme docs: explicit -> Azmain
  - **Type:** explicit
  - **Confidence:** HIGH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Fill Excel with synthetic/dummy data | Azmain | Today | Open | HIGH |
| Deploy CLARA to AWS | BenVH | Today (end of day) | Open | HIGH |
| Set up OneDrive folder | Azmain | Today | Open | HIGH |
| Send programme charter v1 to Richard | Azmain | Today | Open | HIGH |
| Monday 11am programme scope catch-up | Richard/Azmain | Monday | Open | HIGH |
| Send straw man presentation slides | Richard | Today | Open | HIGH |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Data model debugging | technical | "rag status wasn't working because there's customer use cases that had null in the status" -- Richard | HIGH |
| Resource politics | interpersonal | "people aren't interested in helping you when it helps them" -- Richard | HIGH |
| Sales Recon preparation | strategic | "this can't be another meeting where we just chat" -- Richard (quoting Diya) | HIGH |
| AI augmentation philosophy | strategic | "AI is not going to take your job. Somebody who uses AI better than you is going to take your job" -- Azmain | HIGH |
| Programme governance | governance | "I've been creating the structured documents and governance" -- Azmain | MEDIUM |
| Personal AI tool workarounds | operational | "don't tell anybody... I'll just use personal Gemini" -- Azmain | LOW |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Richard Dosoo | Programme leader, political navigator, mentor | Provides context on resource politics, Sales Recon dynamics, technical fixes | 60% |
| Azmain Hossain | PM in training, AI-augmented contributor | Takes on data task, shares governance work, articulates AI philosophy | 40% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Richard | frustrated | DOWN | Resource politics and tooling | "I don't have the energy or the capacity to be arguing" |
| Azmain | supportive | UP | Programme contribution | "I've created project charters... everything's ready to go" |
| Diya (mentioned) | champion | STABLE | Demanding outcomes | Insists on commitment-driven Jan 26 meeting |
| Liz (mentioned) | resistant | STABLE | Resource blocking | Protects Martin for Canopus |
| Stacy (mentioned) | resistant | STABLE | Resource blocking | Protects Martin for gap analysis |
| Nicole (mentioned) | champion | NEW | AI-augmented engineering | Exemplar of senior engineer using AI effectively |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Azmain | Fill Excel with synthetic data | Today | None | HIGH |
| Azmain | OneDrive folder and programme charter | Today | None | HIGH |
| Richard | Monday 11am programme scope session | Monday | None | HIGH |
| Richard | Share presentation slides | Today | None | HIGH |
| BenVH | AWS deployment | Today | None | HIGH |

## Meeting Effectiveness
- **Type:** planning
- **Overall Score:** 70
- **Decision Velocity:** 0.6
- **Action Clarity:** 0.7
- **Engagement Balance:** 0.6
- **Topic Completion:** 0.6
- **Follow Through:** 0.7

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-028 | OPEN | Resource politics -- Liz and Stacy blocking collaboration | HIGH | ESCALATING | political | HIGH |
| R-029 | OPEN | Personal AI tools used as corporate workaround -- compliance risk | MEDIUM | STABLE | compliance | MEDIUM |
| R-030 | OPEN | Sales Recon Jan 26 meeting must produce commitments | HIGH | STABLE | strategic | HIGH |
| R-031 | OPEN | Programme governance still draft (Azmain creating v1) | MEDIUM | STABLE | governance | MEDIUM |
| R-032 | OPEN | Only WS2 actively worked -- five other workstreams still scoped only | MEDIUM | STABLE | scope | MEDIUM |

## Open Questions Raised
- Who are the CS leads for Sales Recon meeting (Josh, Kevin, Catherine, Alexandra, Idris)?
- Can external contractors be approved if internal resources blocked?
- Will Diya provide executive air cover for resource prioritisation?
- When will enterprise Claude access be provisioned?
- What are project plans for WS1, WS3, WS4, WS5, WS6?

## Raw Quotes of Note
- "people aren't interested in helping you when it helps them" -- Richard
- "AI is not going to take your job. Somebody who uses AI better than you is going to take your job" -- Azmain
- "I don't have the energy or the capacity to be arguing with Stacey and Liz about resources anymore" -- Richard
- "Guys, your problem is lack of imagination" -- Azmain, on colleagues resisting AI

## Narrative Notes
See "AWS Deployment of Adoption Tracker" for the same date -- this is the same meeting. The dual naming likely reflects different participants naming the recording differently. The content reveals both technical progress (data model fixes, AWS deployment underway) and political challenges (resource blocking by Liz and Stacy, collaboration dysfunction). Azmain's emergence as an AI-augmented PM -- creating programme documents from verbal briefs using AI tools -- is a concrete demonstration of the programme's thesis about AI-enabled productivity. The Sales Recon meeting looms as the next major milestone: Diya has demanded it be outcome-focused, and the team still needs stakeholder maps, RACI matrices, and project plans for five workstreams they have barely touched.
