# Programme Alignment and Stakeholder Readiness Meeting
**Date:** 2026-01-20
**Attendees:** Richard Dosoo, Azmain Hossain
**Duration context:** Long (~25 minutes of programme content, plus extended personal conversation about faith, ADHD, and family)
**Workstreams touched:** WS2 CLARA, WS1 Training, All workstreams (programme-level governance)

## Key Points
- Richard provided critical context on Diya Sawhny's management style: she is not detail-oriented, needs elevator-pitch communication, and will visibly disengage (scroll phone) during long presentations
- Richard traced the programme's origin story: it started when Diya asked how to get better data out of Salesforce, then expanded through Copilot experiments, training sessions, and cross-pollination with Sales Recon and Idris's banking team
- Azmain demonstrated CLARA's new responsive UI design that adapts to different screen sizes (mobile and desktop), a direct response to Ben Brooks' request for phone accessibility
- Critical infrastructure discussion: once CSMs start using CLARA for data entry, no more uncontrolled deployments — need dev/prod environment separation before handing keys to users
- Richard proposed the deployment workflow: builds auto-deploy to Dev on check-in, but releases to prod must be human-gated (by BenVH) at scheduled intervals with data fix scripts
- The two spent significant time (~15 minutes) discussing personal faith (Islam), ADHD medication, family life, and setting work-life boundaries — particularly blocking Friday prayer time on calendars
- Richard revealed he is a Muslim revert (converted roughly 12 months ago) and that his faith journey is new and energizing
- Azmain shared that he lived as Catholic from ages 12-30 before returning to Islam, largely through his wife's influence

## Decisions Made
- **Freeze deployments to production once CSMs start data entry** (type: process, confidence: high) — rationale: any schema changes without data fix scripts could corrupt production data
- **Get on Diya's calendar for Thursday** (type: tactical, confidence: high) — present programme overview in elevator-pitch format
- **Set up meeting with Bernard/Alexandra** (type: coordination, confidence: high) — for cross-team alignment on presentation

## Action Items
| Action | Owner | Deadline | Confidence |
|--------|-------|----------|------------|
| Send stakeholder map and scope iteration to Azmain for review | Richard Dosoo | 2026-01-21 | High |
| Book Diya for Thursday afternoon to present programme overview | Richard Dosoo | 2026-01-21 | High |
| Set up meeting with Bernard/Alexandra | Richard Dosoo | 2026-01-21 | High |
| Fix action plans and blockers UI, then freeze feature development | Azmain Hossain | 2026-01-21 | High |
| Connect tomorrow afternoon to review programme material | Both | 2026-01-21 | High |
| Forward Friday prayer calendar block to Azmain | Richard Dosoo | 2026-01-20 | Low |

## Theme Segments
| Timestamp Range | Theme | Speakers | Tone |
|----------------|-------|----------|------|
| 0:00-4:00 | Diya's communication style and programme origin story | Richard | Strategic, insightful |
| 4:00-17:00 | Personal conversation: ADHD, Islam, faith journeys, family, work-life boundaries | Both | Deeply personal, warm, vulnerable |
| 17:00-20:00 | Azmain's UI progress and responsive design demo | Azmain, Richard | Energized, collaborative |
| 20:00-25:00 | Deployment freeze strategy and next steps planning | Richard | Structured, forward-looking |

## Power Dynamics
- **Richard** acted as both mentor and peer in this conversation. On programme matters, he was the guide; on faith matters, they were equals sharing vulnerably. His candid characterization of Diya's management style was unusually direct and potentially valuable for Azmain's approach.
- **Azmain** was more vocal and personal in this call than in the debugging sessions. The faith conversation unlocked a level of openness that has not been visible in other meetings.

## Stakeholder Signals
- **Diya Sawhny** (discussed, not present) — Richard's characterization painted her as a high-level executive who delegates details and loses patience with granular presentations. This is critical intelligence for how the programme should communicate upward. She is waiting for a high-level overview of scope and resourcing but has not received it yet.
- **Richard Dosoo** — Revealed personal depth: a Muslim revert navigating faith, work, and programme leadership simultaneously. His understanding of Diya's style shows political awareness.
- **Azmain Hossain** — More personally open than in any other transcript. His ADHD self-diagnosis, faith journey, and family priorities reveal a person managing significant personal growth alongside intense professional demands.
- **Ben Brooks** (referenced) — His push for mobile accessibility was taken as a given requirement by Azmain.
- **BenVH** (referenced) — Confirmed as the gatekeeper for production deployments once the environment separation is complete.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Richard | Book Diya for Thursday | Azmain | High |
| Richard | Send stakeholder map iteration | Azmain | High |
| Richard | Set up Bernard/Alexandra meeting | Azmain | High |
| Azmain | Fix action plans/blockers then freeze features | Richard | High |
| Richard | Ask wife (Saba) about ADHD medication permissibility in Islam | Azmain | Low |

## Meeting Effectiveness
- **Clarity of outcomes:** 6/10 — Programme next steps were clear but occupied a minority of the call time
- **Decision quality:** 7/10 — The deployment freeze decision was important and well-reasoned
- **Engagement balance:** 8/10 — Genuinely two-way conversation, especially during the personal segment
- **Time efficiency:** 4/10 — Over half the call was personal conversation, though this clearly deepened the working relationship

## Risk Signals
| Risk | Severity | Signal |
|------|----------|--------|
| Diya receiving the programme overview too late | MEDIUM | Richard noted she is already getting antsy waiting for the scope/resourcing overview. Thursday timing is tight if Monday is the exec meeting. |
| Programme communication mismatch with Diya's style | MEDIUM | Richard's warning about Diya's attention span means the team must radically simplify their messaging or risk losing her engagement. |
| Azmain's bandwidth and wellbeing | MEDIUM | ADHD self-diagnosis, work-life boundary discussions, and the intensity of context-switching between debugging and programme management suggest sustainability concerns. |

## Open Questions Raised
- What specific scope and resourcing does Diya need to see on Thursday?
- How will the programme be framed to Diya — as six workstreams, or as a simpler narrative?
- When will BenVH complete the dev/prod environment separation?

## Raw Quotes of Note
- "She's not detail orientated... just give me the elevator. Just tell me. At a high level" — Richard Dosoo, on Diya Sawhny
- "Whenever I try and get details with her, she's looking at me like, I'm bored, bro... she's scrolling on her phone" — Richard Dosoo, on presenting to Diya
- "In 20 years, the only people that will remember that you work late are your children" — Azmain Hossain, on work-life priorities

## Narrative Notes
This transcript is exceptional in the Icarus corpus for the depth of personal connection it reveals between Richard and Azmain. Beneath the programme management and technical debugging lies a genuine friendship built on shared faith, vulnerability about mental health, and honest conversation about priorities. Richard's characterization of Diya is the most operationally useful stakeholder intelligence in any Week 3 transcript — understanding that she needs two-minute elevator pitches rather than detailed presentations will fundamentally shape how the programme communicates upward. The deployment freeze decision was the most consequential technical outcome: it marks the point where CLARA transitions from a prototype being rapidly iterated to a production system that requires proper change management. The contrast between the debugging chaos of the January 19 sessions and this more reflective, strategic conversation suggests the team is beginning to recognize the need to shift gears from building to governing.
