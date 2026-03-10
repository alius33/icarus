# Demo and Feedback from Josh E -- Data Quality, Gainsight, and CSM Champion Model
**Date:** 2026-01-16
**Attendees:** Josh Ellingson, Azmain Hossain, Ben Brooks
**Duration context:** medium (~2500 words)
**Workstreams touched:** WS2 (CLARA)

## Key Points
- Josh's overriding concern is data quality and interpretation: "I don't want people to come away with the incorrect interpretation, because with Andy Frappe that sticks and we can't get them off of it"
- Josh is careful to frame his concern as not demeaning Azmain's work: "I think it's really, really good. I just think the interpretation" needs validation by CSMs before it reaches leadership
- Ben Brooks arrives mid-call; Josh shares that Andy Frappe's team is already misinterpreting data (requesting GMB numbers for migration when it should be zero)
- Azmain frames the primary ask: CSMs need to go in and correct/enter data -- the biggest gap is empty fields, not incorrect data
- Josh is bullish on the tool's ability to rapidly add new data capture fields: "one of the things I really love about this tool is... we get a lot of requests for additional information that we haven't thought to capture"
- Azmain explains two data ingestion paths: (1) CSMs identify gaps and new fields; (2) existing data in spreadsheets can be imported programmatically via Cursor
- Josh asks about the Salesforce naming convention problem: Hartford vs. "The Hartford" vs. Hartford Insurance -- different sources use different names. Azmain confirms Salesforce Account ID is stored to link entities
- Only 40% of accounts have Salesforce IDs (were done manually, only 40% through when data was imported)
- Azmain proposes replacing the AI chat widget with a feedback button that captures screenshots -- front and centre for CSM feedback
- Josh strongly advocates for a CSM champion model rather than sending to all CSMs at once: "you might get more meaningful, targeted feedback if we bring in a couple CSM champions"
- Josh warns about champion fatigue: already have Gainsight champions, digital engagement champions, and soon Salesforce migration champions -- too many parallel champion programmes
- Ben Brooks proposes compromise: champions as feedback collators, not exclusive users -- show everyone but have designated people gather and triage feedback (Watson in London, Julia in Zurich, Dave Kenny in US)
- Critical timing: Gainsight go-live is end of March; digital engagement service model change is imminent -- CSMs being asked to do a lot simultaneously
- Josh raises the philosophical question: where does CLARA end and Gainsight begin? If a client is migrated and ongoing adoption tracking continues, which system is the record?
- Ben Brooks: "we probably want it in here and then push to Gainsight on the back end"
- Azmain confirms Gainsight API is blocked due to a security breach -- approval process must complete before API access is restored
- Josh warns about the consequences of making assumptions about Gainsight integration: CSMs are being measured by metrics tied to Gainsight data entry; if this tool diverts their time from Gainsight, there are real performance implications
- Ben Brooks reframes the messaging: "it's not data quality, it's data visibility" -- this is about multiple teams collaborating on the same data, not about fixing bad data
- Josh agrees: "data visibility, that's the right positioning. I said data quality and I knew it was like, why did I say that?"
- Ben pushes for squad-based approach from day one: implementation leads and cross-functional team members, not just CSMs
- Azmain and Josh agree on scheduling: demo to portfolio/project people early next week, broader CSM demo Wednesday/Thursday; Josh warns about lead time for CSM calendars
- Josh's final framing: "any pushback I have is about data quality, not about function. I think the function is great"

## Decisions Made
- **CSM champion model for feedback collection**: 2-3 champions per region collate feedback rather than all CSMs feeding back individually -> Josh (proposed), Ben (refined)
  - **Type:** explicit
  - **Confidence:** HIGH
- **Data visibility, not data quality, as positioning**: Messaging to CSMs and leadership should emphasise collaboration and visibility, not fixing bad data -> Ben Brooks (proposed), Josh (agreed)
  - **Type:** explicit
  - **Confidence:** HIGH
- **Feedback button replaces AI chat widget**: Screenshot-capture feedback mechanism front and centre on the UI -> Azmain
  - **Type:** explicit
  - **Confidence:** HIGH
- **Squad-based approach from day one**: Implementation leads and cross-functional team, not just CSMs -> Ben Brooks
  - **Type:** explicit
  - **Confidence:** HIGH
- **Two-phase demo rollout**: Portfolio/project people early next week, then broader CSM demo mid-week -> Azmain/Josh
  - **Type:** explicit
  - **Confidence:** HIGH
- **CLARA data pushes to Gainsight, not the reverse**: CLARA is the working system; Gainsight gets data pushed on the back end -> Ben Brooks
  - **Type:** explicit
  - **Confidence:** MEDIUM

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Replace AI chat widget with screenshot-based feedback button | Azmain | 2026-01-20 | Open | HIGH |
| Identify 2-3 CSM champions per region for feedback collection | Josh | 2026-01-22 | Open | MEDIUM |
| Schedule demo for portfolio/project people (early next week) | Azmain/Natalia | 2026-01-20 | Open | HIGH |
| Schedule broader CSM demo (mid-week) | Azmain/Josh | 2026-01-22 | Open | HIGH |
| Get CSMs to validate data interpretation before showing to leadership | Josh | 2026-01-24 | Open | HIGH |
| Fill remaining 60% of Salesforce Account IDs | Azmain/CSMs | 2026-02-01 | Open | MEDIUM |
| Coordinate with Josh on messaging for CSM rollout | Azmain/Ben Brooks | 2026-01-20 | Open | HIGH |

## Theme Segments
| Topic | Category | Key Quote | Confidence |
|-------|----------|-----------|------------|
| Data quality vs data visibility framing | strategic | "it's not data quality, it's data visibility" -- Ben Brooks | HIGH |
| CSM champion model debate | operational | "you might get more meaningful, targeted feedback if we bring in a couple CSM champions" -- Josh | HIGH |
| Gainsight integration and boundaries | strategic | "at what point... which use cases come into this tool, and which ones are evergreen?" -- Josh | HIGH |
| Andy Frappe data misinterpretation risk | political | "I don't want Andy Frappe seeing one piece of data that's interpreted incorrectly and we can't get them off of it" -- Josh | HIGH |
| Champion fatigue across programmes | operational | "we have Gainsight champions... digital engagement champions... Salesforce migration champions" -- Josh | HIGH |

## Power Dynamics
| Person | Role This Meeting | Influence Acts | Engagement % |
|--------|-------------------|----------------|--------------|
| Josh Ellingson | Gatekeeper, quality guard | Setting conditions for CSM rollout, proposing champion model, flagging Andy Frappe risk | 45% |
| Ben Brooks | Product owner, reframer | Arriving mid-call, reframing data quality to data visibility, proposing squad approach | 30% |
| Azmain Hossain | Builder, listening and absorbing | Proposing feedback button, explaining data ingestion paths, scheduling demos | 25% |

## Stakeholder Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| Josh Ellingson | Supportive but cautious, protective of CSMs | Warming | Tool function vs data risk | "the function is great... any pushback I have is about data quality" |
| Ben Brooks | Confident, politically savvy | Stable | Positioning | Reframed the entire conversation with "data visibility" |
| Azmain | Receptive, eager to incorporate feedback | Positive | Feedback loop | Immediately adopting champion model and feedback button |
| Andy Frappe (referenced) | Source of interpretation risk | Stable | Data misuse | Already requesting wrong metrics (GMB for migrations) |
| Kevin Burns (referenced) | Building related tools | Stable | Quality tooling | Has built a tool for evaluating success criteria quality |
| Catherine (referenced) | Digital engagement champion | Stable | Service model change | Working on digital engagement that will change how CSMs operate |

## Commitments Made
| Person | Commitment | Implied Deadline | Condition | Confidence |
|--------|------------|------------------|-----------|------------|
| Josh | Will identify CSM champions for feedback | Before CSM demo | None | MEDIUM |
| Josh | Will ensure CSMs validate data before it reaches leadership | Before any exec presentation | Data populated | HIGH |
| Azmain | Will build feedback button with screenshot capture | Before CSM demo | None | HIGH |
| Azmain | Will schedule two-phase demo (portfolio people, then CSMs) | Next week | Josh/Natalia available | HIGH |
| Ben Brooks | Will work on squad-based rollout messaging | Before CSM demo | None | MEDIUM |

## Meeting Effectiveness
- **Type:** Stakeholder feedback / strategic alignment
- **Overall Score:** 78
- **Decision Velocity:** 0.7
- **Action Clarity:** 0.7
- **Engagement Balance:** 0.7
- **Topic Completion:** 0.7
- **Follow Through:** 0.6

## Risk Signals
| Risk_ID | Status | Title | Severity | Trajectory | Source_Type | Confidence |
|---------|--------|-------|----------|------------|-------------|------------|
| R-041 | New | Andy Frappe team already misinterpreting data -- risk of incorrect conclusions becoming sticky | HIGH | Stable | Political | HIGH |
| R-042 | New | Champion fatigue: CSMs already juggling Gainsight, digital engagement, and Salesforce migration champions | MEDIUM | Escalating | Resource | HIGH |
| R-043 | New | Only 40% of accounts have Salesforce IDs -- data linkage is incomplete | MEDIUM | Stable | Data Quality | HIGH |
| R-044 | New | Gainsight vs CLARA boundary undefined -- which system is record for post-migration adoption? | MEDIUM | Stable | Strategic | HIGH |
| R-045 | New | CSM performance metrics tied to Gainsight data entry -- diverting time to CLARA has real consequences | HIGH | Stable | Political | HIGH |

## Open Questions Raised
- At what point do use cases stop being tracked in CLARA and move to Gainsight for ongoing adoption?
- How to ensure Salesforce naming consistency when only 40% of accounts have Salesforce IDs?
- Will there be a handover date from Salesforce data entry to CLARA data entry, or a gradual transition?
- How to balance CSM time across Gainsight, digital engagement, and CLARA champion programmes?
- When will the Gainsight API security review complete and access be restored?

## Raw Quotes of Note
- "I don't want Andy Frappe seeing one piece of data that's interpreted incorrectly and we can't get them off of it" -- Josh, on the political stakes of data presentation
- "it's not data quality, it's data visibility" -- Ben Brooks, reframing the entire messaging
- "any pushback I have is about data quality, not about function. I think the function is great" -- Josh, closing assessment
- "I got a request this morning from one of Andy Frappe's minions saying how much I need the GMB number right now from all the migrations" -- Ben Brooks, on existing data misinterpretation
- "we shouldn't expect you to understand how the data like, what the data represents. You're just being asked to pull all these things together" -- Josh, being careful not to criticise Azmain

## Narrative Notes
This is the session that determines whether CLARA will succeed with the CSM team. Josh Ellingson is the critical gatekeeper -- he manages the CSMs who will need to use CLARA daily, and his buy-in is essential. His feedback is nuanced and constructive: he loves the functionality ("the function is great") but is deeply worried about data interpretation reaching leadership before CSMs have validated it. The Andy Frappe reference is politically telling -- senior leaders who lock onto incorrect data points create lasting problems that are hard to undo. Ben Brooks's arrival mid-call is pivotal: his "data visibility, not data quality" reframing instantly changes the conversation's tone and gives Josh a messaging framework he can use with his CSMs. The champion model discussion reveals a real tension: Josh knows his CSMs are already stretched across multiple champion programmes (Gainsight, digital engagement, Salesforce migration), and adding another one risks fatigue and resentment. Ben's compromise -- champions as feedback collators, not exclusive users -- is elegant. The Gainsight boundary question (where does CLARA end and Gainsight begin?) is strategically unresolved and will need a clear answer before post-migration adoption tracking begins. Josh's warning about CSM performance metrics tied to Gainsight data entry is the most politically dangerous risk surfaced this week: if CLARA diverts CSM time from Gainsight without a corresponding change in how they're measured, it creates a direct conflict between using the new tool and meeting their KPIs.
