# AWS Deployment of Adoption Tracker
**Date:** 2026-01-09
**Attendees:** Richard Dosoo, Azmain Hossain (Ben Brookes mentioned sending data/files, not directly on call)
**Duration context:** Long (~42 minutes, transcript ~345 lines)
**Workstreams touched:** WS2 (CLARA/IRP Adoption Tracker), WS1 (Training & Enablement -- discussed), WS6 (Build in Five -- mentioned in broader programme context)

**Note:** This transcript is nearly identical to "Chat with Richard" from the same date (only one speaker label difference). Same meeting recorded under two names.

## Key Points
- Richard shares his previous evening's work debugging the data model and fixing RAG status issues with Claude (personal account at 18 pounds/month)
- Identified root cause of broken RAG status display: customer use cases had null status/zero values, causing dashboard to break
- Richard ran analysis across entire schema to find similar null/missing data issues across customers, use cases, and other tables
- Created Python scripts to fix required fields and populate missing data -- ready to share with Azmain
- Azmain looking at the AWS network architecture diagrams Richard sent earlier -- AWS monthly cost confirmed at less than $100/month
- Richard confirms BenVH is currently working on deploying to AWS -- hoping to have something by end of BenVH's day
- Azmain's task: fill up the Excel spreadsheet with dummy/synthetic data so it is ready when BenVH finishes deployment
- Blockers page still broken on local builds -- neither Richard nor Azmain can fix it without Cursor tokens
- Both Richard and Azmain using personal AI tools (Claude personal, Gemini personal) as workarounds for exhausted Cursor tokens
- Richard and Azmain discuss the Sales Recon meeting on Jan 26 -- Richard shares the agenda, adds Azmain to the meeting invite and the thread with Jamie Stark (from Ari Lahavi's team)
- Richard gives context on Sales Recon meeting politics: Diya warned that last time they met with these people, nothing came of it. She demands outcome-focused, commitment-driven meeting -- not just chat
- Resource frustration emerges: Richard expects pushback when asking for people (Martin, Miriam) -- Liz and Stacy are defensive about their resources
- Richard openly discusses the collaboration dysfunction: "people aren't interested in helping you when it helps them"
- If internal resources are blocked, Richard will push for external contractors -- prefers that to arguing with Stacy and Liz
- Programme governance documents: Azmain has been creating project charters, strategic docs using AI -- will send to Richard for review
- Shared OneDrive folder being set up for programme documentation
- Monday 11am planned for programme scope discussion before 2pm Sales Recon prep meeting
- Discussion about AI replacing junior developer roles -- Richard introduces Nicole (new US-based senior engineer) as exemplar of AI-augmented engineering
- Divya's Cursor licence update came back during the call -- some progress on that front
- Richard shares tips on using Microsoft Copilot for presentations (referencing Word docs to bypass 2000 character prompt limit)

## Decisions Made
- Azmain to fill Excel with synthetic data as priority task: Richard/Azmain -> Azmain
  - **Type:** explicit
  - **Confidence:** HIGH
- BenVH deploying to AWS today -- target is end of his workday: Richard -> BenVH
  - **Type:** explicit
  - **Confidence:** HIGH
- Monday 11am programme scope discussion before 2pm Sales Recon prep: Richard -> Richard/Azmain
  - **Type:** explicit
  - **Confidence:** HIGH
- If internal resources are blocked, pursue external contractors: Richard -> Richard
  - **Type:** implicit
  - **Confidence:** MEDIUM
- Set up OneDrive folder for programme documentation: Azmain -> Azmain
  - **Type:** explicit
  - **Confidence:** HIGH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Fill Excel spreadsheet with synthetic/dummy data | Azmain | Today (before BenVH finishes AWS deployment) | Open | HIGH |
| Deploy CLARA to AWS | BenVH | Today (end of his day) | Open | HIGH |
| Set up OneDrive folder for programme docs | Azmain | Today | Open | HIGH |
| Send programme charter v1 to Richard for review | Azmain | Today | Open | HIGH |
| Add Azmain to Sales Recon meeting invite and Jamie Stark thread | Richard | Done during call | Done | HIGH |
| Monday 11am programme scope catch-up | Richard/Azmain | Monday | Open | HIGH |
| Send straw man presentation slides to Azmain for weekend work | Richard | Today | Open | HIGH |
| Pursue Cursor licence resolution with Divya/Megan | Richard | Ongoing | Open | MEDIUM |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Data model debugging and fixes | technical | "what we found out was the rag status wasn't working because there's customer use cases in there that had null in the status" -- Richard | HIGH |
| Resource politics and collaboration dysfunction | interpersonal | "people aren't interested in helping you when it helps them" -- Richard | HIGH |
| Sales Recon meeting preparation | strategic | "this can't be another meeting where we just chat... it needs to be outcome focused" -- Richard (quoting Diya) | HIGH |
| AI augmented development philosophy | strategic | "AI is not going to take your job. Somebody who uses AI better than you is going to take your job" -- Azmain | HIGH |
| Programme governance setup | governance | "I've been creating, like, the structured documents and governance" -- Azmain | MEDIUM |
| Workaround tooling | operational | "don't tell anybody... I'll just use, like, personal Gemini" -- Azmain | LOW |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Richard Dosoo | Programme leader, technical mentor, political navigator | Shares data model fixes, provides Sales Recon context, warns about resource politics, shares presentation tips | 60% |
| Azmain Hossain | Programme manager in training, data worker | Takes on synthetic data task, shares governance docs, honest about AI augmenting his PM work | 40% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Richard Dosoo | frustrated | DOWN | Resource politics | "I don't have the energy or the capacity to be arguing with Stacey and Liz about resources anymore" |
| Azmain Hossain | supportive | UP | Programme contribution | "I've created project charters... strategic documents... everything's ready to go" |
| Diya (mentioned) | champion | STABLE | Programme delivery | Demanding outcome-focused Jan 26 meeting |
| Liz (mentioned) | resistant | STABLE | Resource sharing | "no, he needs to be Canopus" (blocking Martin) |
| Stacy (mentioned) | resistant | STABLE | Resource sharing | "no, he needs to be gap analysis" (blocking Martin) |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Azmain | Fill Excel with synthetic data | Today | None | HIGH |
| Azmain | Set up OneDrive folder | Today | None | HIGH |
| Azmain | Send programme charter to Richard | Today | None | HIGH |
| Richard | Monday 11am programme scope discussion | Monday | None | HIGH |
| Richard | Send presentation slides | Today | None | HIGH |
| BenVH | AWS deployment | Today (end of day) | None | HIGH |

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
| R-028 | OPEN | Resource politics -- Liz and Stacy blocking collaboration on shared people | HIGH | ESCALATING | political | HIGH |
| R-029 | OPEN | Team using personal AI tools as workaround for corporate tooling gaps | MEDIUM | NEW | compliance | MEDIUM |
| R-030 | OPEN | Sales Recon Jan 26 meeting needs to produce commitments or programme loses strategic alignment | HIGH | NEW | strategic | HIGH |
| R-031 | OPEN | No formal programme governance documents yet (Azmain drafting v1) | MEDIUM | STABLE | governance | MEDIUM |
| R-032 | OPEN | Five workstreams scoped but only one (WS2) actively worked | MEDIUM | STABLE | scope | MEDIUM |

## Open Questions Raised
- Who exactly are the CS leads for the Sales Recon meeting (Josh -- lead or informed? Kevin?)
- Can external contractors be brought in if internal resources are blocked?
- Will Diya provide executive air cover for resource prioritisation?
- When will enterprise Claude/Anthropic access be provisioned?
- What are the five workstream project plans (only WS2 has one)?

## Raw Quotes of Note
- "people aren't interested in helping you when it helps them. That's the place, unfortunately, where we're at" -- Richard, on collaboration dysfunction
- "this can't be another meeting where we just chat. She was like, it needs to be outcome focused. We need commitment from these guys" -- Richard, quoting Diya on Sales Recon meeting
- "AI is not going to take your job. Somebody who uses AI better than you is going to take your job" -- Azmain, on AI and work
- "I don't have the energy or the capacity to be arguing with Stacey and Liz about resources anymore" -- Richard, on resource frustration
- "Guys, your problem is lack of imagination" -- Azmain, on colleagues not seeing AI potential

## Narrative Notes
This is a pivotal conversation that reveals the programme's political landscape alongside its technical progress. While the surface topic is AWS deployment logistics and data preparation, the real content is Richard's candid assessment of internal collaboration dysfunction. He names names -- Liz blocks Martin for Canopus work, Stacy blocks Martin for gap analysis -- and expresses genuine fatigue with the resource negotiation process. His willingness to consider external contractors signals that the collaboration problem is not new; it is a structural feature of the organisation.

Simultaneously, Azmain is emerging as a highly productive contributor, having used AI tools to generate programme charters and strategic documents from Richard's verbal brief. His self-awareness about AI augmenting his PM role is notable -- he openly acknowledges that AI can do most of his job, and his value proposition is being the person who uses it effectively. The Sales Recon meeting preparation reveals Diya as a demanding but supportive sponsor who has learned from past failures with the same stakeholders and will not tolerate another talk-shop. The programme is now racing on two fronts: getting CLARA deployed for next week's demos, and getting the broader programme governance ready for the Jan 26 executive meeting.
