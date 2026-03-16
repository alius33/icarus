# CSM Session with Naveen — Individual Onboarding
**Date:** 2026-02-11
**Attendees:** Azmain Hossain, Naveen
**Duration context:** Short (~12 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Naveen is a CSM based in Little Rock, Arkansas. He is the only CSM who proactively reached out to have a one-on-one CLARA onboarding session — Azmain notes this with genuine appreciation.
- Naveen's Salesforce name has three components but Salesforce only has two fields, causing a mismatch when data was pulled into CLARA. Naveen needs to reassign himself to his correct employee profile for each of his customers.
- When Naveen attempts to reassign himself, the system throws a "failed to assign CSM" error. Azmain discovers the employee profile is not linked to the customer. Naveen will send his customer list and Azmain will assign them manually.
- Azmain has pre-populated the last two weeks of portfolio review call updates into individual customer records from the meeting transcripts. The "executive summary" holds the first week's overview; subsequent updates are added as timestamped entries.
- Naveen tries editing a use case (portfolio management for Chubb) — changes health status to red and marks it "at risk." He identifies that the status field and RAG status field are confusingly redundant. Azmain acknowledges this is a recurring question but says senior stakeholders requested both fields.
- Naveen asks about "scope and criticality" fields (risk link critical, risk browser critical, in scope, in scope date). Azmain is transparent that Ben Brookes requested these but he does not fully understand the rationale. Suggests Naveen raise the question in the Monday meeting.
- Naveen commits to spending a couple of hours going through all his accounts to update data, then reporting back any issues or questions.
- Azmain commits to freezing changes after today — no more updates until after the Monday call, to give CSMs stability for data entry.

## Decisions Made
| Decision | Type | Made By | Confidence |
|----------|------|---------|------------|
| No more CLARA changes until after the Monday portfolio review call | Stability | Azmain | High |
| Naveen's accounts to be manually assigned by Azmain due to system error | Workaround | Azmain | High |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Send customer list to Azmain for manual assignment | Naveen | 2026-02-11 | Open | High |
| Go through all accounts and update data | Naveen | This week | Open | High — Naveen is proactive |
| Raise "in scope" and scope/criticality questions at Monday meeting | Naveen | 2026-02-16 | Open | Medium |

## Theme Segments
| Time Range | Theme | Key Speakers |
|------------|-------|--------------|
| 0:00-2:00 | Introductions, Naveen's proactive outreach noted | Azmain, Naveen |
| 2:00-5:00 | Salesforce name mismatch and CSM assignment error | Azmain, Naveen |
| 5:00-9:00 | Use case editing walkthrough, status vs RAG confusion | Naveen, Azmain |
| 9:00-12:00 | Scope/criticality questions, commitment to data entry, closing | Naveen, Azmain |

## Power Dynamics
- **Azmain as guide, Naveen as willing student.** The dynamic is collaborative and warm. Naveen does not question whether the tool should exist — he is already using it and wants to understand it better.
- **Azmain is transparent about his own knowledge gaps.** He admits he does not understand the "in scope" field or why Ben requested certain features. This honesty builds trust with Naveen.

## Stakeholder Signals
- **Naveen:** The most proactive CSM so far — the only one to request a 1:1 session. He spent time on a Sunday two weeks prior trying to get data ready. This is notable engagement from the field. He is the kind of early adopter who can become a champion.
- **Azmain:** Visibly grateful for any CSM who shows initiative. The contrast between Naveen's willingness and the broader resistance from others is a recurring theme that shapes Azmain's emotional state.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| Naveen | Spend couple of hours updating all accounts | Azmain | Firm |
| Naveen | Send customer list for manual assignment | Azmain | Firm |
| Azmain | Freeze changes until after Monday call | CSMs broadly | Firm |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 4 | Naveen knows what to do |
| Decision quality | 3 | Workaround for assignment bug, not a fix |
| Engagement balance | 5 | Both participated fully in a short session |
| Time efficiency | 5 | 12 minutes, highly productive |
| Follow-through potential | 5 | Naveen is self-motivated |

## Risk Signals
- **Status vs RAG redundancy is a design debt item.** It surfaces with every new CSM who touches the tool. If not resolved, it will erode confidence in data quality.
- **CSM assignment bug** (failed to assign error) could affect other CSMs with non-standard Salesforce names. The manual workaround does not scale.
- **Naveen's earlier data entry was wiped.** He spent a Sunday entering data that was subsequently lost in a deployment refresh. The fact that he is still willing to engage after that experience speaks to his character, but the risk of repeat data loss would likely end his engagement.

## Open Questions Raised
- Why are there both a "status" and a "RAG status" field? What is the difference?
- What does "in scope" mean for a use case, and what is "in scope date"?
- Why does the CSM assignment fail for some employee profiles?

## Raw Quotes of Note
- "You're actually the only person that reached out and actually showed interest in having a session." -- Azmain, to Naveen

## Narrative Notes
This is a small but significant interaction. Naveen represents what the programme needs most: a CSM who is willing to engage despite imperfect tooling. His proactive outreach, his willingness to spend hours on data entry, and his constructive questioning (why two status fields? what does "in scope" mean?) are exactly the feedback loop that will improve CLARA. Azmain's emotional response — genuine gratitude — reveals how starved the programme is for this kind of voluntary engagement. The session also surfaces the recurring design debt: fields that exist because someone senior requested them but nobody defined them. The "in scope" field is a ghost requirement from Ben Brookes that haunts the UI without purpose.
