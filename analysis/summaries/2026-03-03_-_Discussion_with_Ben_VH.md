# Discussion with Ben VH
**Date:** 2026-03-03
**Attendees:** Azmain Hossain, BenVH (Speaker 1)
**Duration context:** Long (~32 minutes)
**Workstreams touched:** WS2 CLARA, WS4 Adoption Charter, App Factory, Phantom Agent

## Key Points
- BenVH pitched Phantom Agent to Azmain as a solution for uncontrolled AI agent orchestration across Moody's. It is an MCP server that can orchestrate LLM workers anywhere (AWS, Azure, GCP, on-prem, Kubernetes, local).
- The core problem BenVH articulated: at least four other apps want to spin up AI agents, but there is no governance over where agents run, who pays, or what data they access. Everything currently routes through one RMS AWS bedrock key with zero cost allocation.
- Azmain revealed he used 30 concurrent agents in Cursor to build Friday (the PM app), burning his entire monthly $1,000 Cursor budget in one day. He ran this on a cloud environment (anthropic infrastructure), not locally.
- Azmain offered strategic advice: let Moody's feel the cost pain first, then present Phantom Agent as the solution. This positions BenVH's technology as the answer to a felt need rather than an unsolicited pitch.
- BenVH expressed anxiety about Nikhil potentially building a competing solution before BenVH can introduce Phantom Agent. BenVH explicitly said he does not want anyone focusing on LLM worker orchestration before he can show Phantom Agent.
- Adoption charters revealed as far more complex than expected -- Azmain showed a real charter with embedded images, diagrams, and multi-page documents. Would need OCR and multi-modal LLM to parse.
- Priority sequence for CLARA onboarding established: feedback/bugs first, blocker intelligence (Bedrock API) second, adoption charters third.
- Nikhil confirmed to have Bedrock API key working on his local environment using IAM roles (not hard-coded keys) -- this is a significant technical milestone.
- Azmain mentioned deploying his new PM app (Friday) via App Factory.
- They agreed to sync with Richard before approaching Ben Brookes about Phantom Agent.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Deliberately delay Phantom Agent introduction until cost pain is felt | Strategic | Medium | Azmain advising BenVH |
| Keep onboarding call focused on bugs/features, not LLM orchestration | Tactical | High | Azmain |
| CLARA work priority: bugs -> blocker intelligence -> adoption charters | Prioritisation | High | Azmain |
| Sync with Richard before approaching Ben Brookes about Phantom Agent | Process | High | Azmain, BenVH |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Prepare Phantom Agent for introduction once cost pressure emerges | BenVH | Ongoing | Open | High |
| Sync with Richard about Phantom Agent positioning | Azmain, BenVH | This week | Open | High |
| Create test environment for Phantom Agent within App Factory | BenVH | TBD | Open | Medium |
| Onboard Nikhil and Chris to CLARA (bugs first) | Azmain | This week | Open | High |

## Theme Segments
1. **Phantom Agent pitch and capabilities** (0:00-6:00) -- BenVH explains the technology and its strategic value
2. **CLARA onboarding and adoption charter complexity** (6:00-14:00) -- What Nikhil and Chris will work on; adoption charter reality check
3. **Strategic positioning of Phantom Agent** (14:00-25:00) -- "Let them feel the pain" strategy; Nikhil concerns
4. **Career concerns and personal dynamics** (25:00-32:00) -- Azmain and BenVH bonding over career frustrations

## Power Dynamics
- **Azmain is the strategic advisor**, despite BenVH being the technical creator. BenVH defers to Azmain on political positioning of Phantom Agent.
- **BenVH is vulnerable and seeking protection.** His anxiety about being scooped is driven by real career trauma. He is asking for Azmain as an ally.
- **Azmain is building a coalition** -- he controls information flow between BenVH, Richard, and the programme. He is the connective tissue.
- **BenVH has leverage he is not exploiting** -- he owns the only deployment pipeline and has a patented product, but is too focused on threats to leverage his position.

## Stakeholder Signals
- **BenVH** -- Anxious, protective, technically strong but politically insecure. Career trauma (Microsoft) is actively shaping behaviour. Passionate about Phantom Agent but fearful of being outmanoeuvred by Nikhil.
- **Azmain** -- Playing strategic advisor/kingmaker. Genuinely wants BenVH to succeed but also sees value in controlling timing. His "let them feel the pain" advice is sophisticated political strategy. Also reveals personal career frustration and ambition.
- **Nikhil** (discussed, not present) -- BenVH views him as immediate threat. Brand new, eager to prove himself, has Bedrock working (legitimate technical contribution).

## Commitments Made
| Who | Commitment | To Whom | Context |
|-----|-----------|---------|---------|
| Azmain | Keep LLM orchestration off the onboarding call | BenVH | Protect Phantom Agent introduction |
| Azmain | Name-drop BenVH and Phantom Agent in group chats | BenVH | Credit protection |
| Both | Sync with Richard before approaching Ben Brookes | Each other | Strategic alignment |

## Meeting Effectiveness
| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 7 | Strategy agreed but deliberately vague on timing |
| Decision quality | 7 | Smart political play; risk of waiting too long |
| Participation balance | 6 | BenVH pitches, Azmain advises -- unequal but appropriate |
| Action item specificity | 5 | Mostly directional, not time-bound |
| Strategic alignment | 8 | Aligns with cost governance need and programme maturity |

## Risk Signals
- **CRITICAL: BenVH retention risk.** Anxiety about credit-taking mirrors Microsoft experience. If Nikhil gets visibility for his work, he could disengage.
- **HIGH: Phantom Agent introduction could be too late.** The "feel the pain" strategy assumes Nikhil will not build a competing solution first.
- **HIGH: Security exposure.** Azmain running 30 agents on Anthropic's cloud environment with Moody's code/data. No enterprise controls.
- **MEDIUM: Azmain making strategic programme decisions without formal authority.** He is advising BenVH on when to introduce a major capability.

## Open Questions Raised
- How should BenVH protect his IP (Phantom Agent patent) while introducing it to Moody's?
- Can Phantom Agent be positioned as a paid service rather than given away?
- How will the four other pipeline apps handle AI agent orchestration without Phantom Agent?

## Raw Quotes of Note
- "One thing about business people, you can't give them the solution too early. They don't value it. They got to feel the pain first, and then they value the solution." -- Azmain, on Phantom Agent timing
- "I've had people steal my ideas. I've had people build something and it's half assed, but because of their visibility in the company, their shit gets pushed versus mine." -- BenVH, revealing career trauma

## Narrative Notes
This is one of the most strategically significant conversations of the week. It reveals two critical dynamics: (1) BenVH is not just technically frustrated but existentially anxious about repeating a traumatic career pattern, and (2) Azmain is emerging as a sophisticated political operator who controls information flow across the programme. The "let them feel the pain" strategy is a calculated gambit -- protecting BenVH's position but also allowing unnecessary costs to accumulate. The adoption charter complexity reveal is also significant: what Ben Brookes frames as a simple feature requires multi-modal AI capabilities nobody has scoped. The personal career frustrations shared by both men -- BenVH's Microsoft trauma, Azmain's deferred promotion -- reveal a programme held together by people who are personally invested but professionally under-rewarded.
