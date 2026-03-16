# Integration Meeting with Gainsight Team
**Date:** 2026-03-12
**Attendees:** Kathryn Palkovics (facilitator), Tina Palumbo, Rajesh (solution architect), Nadeem, Azmain Hossain, Richard Dosoo, Ben Brookes, BenVH, Kevin Pern
**Duration context:** Medium (~25 minutes)
**Primary project:** CLARA (IRP Adoption Tracker)
**Secondary projects:** Program Management

## Speaker Identification Notes
- Speaker 1 = Kathryn Palkovics (organised and facilitated the meeting)
- Speaker 2 = Tina Palumbo (Business Systems team)
- Speaker 3 = BenVH (technical API questions from Clara side)
- Speaker 5 = Nadeem (project manager, Gainsight team)
- Speaker 6 = Rajesh (solution architect, Gainsight team)

## Key Points
- First formal meeting between the Clara team and the Gainsight Business Systems team to discuss integration
- Tina Palumbo presented a bi-directional integration proposal: CSMs create IRP use cases in Gainsight, sync to Clara; blockers and adoption data flow back
- Gainsight team's philosophy: CSMs should have one home (Gainsight) for all day-to-day work; Clara serves cross-functional teams (product, implementation) who need adoption visibility
- Azmain initially stated Clara only needs read-only access from Gainsight, but discussion moved toward bi-directional sync to avoid CSMs double-entering data
- Kevin Pern raised concern about overlapping data: executive summaries and customer updates tracked in both systems
- Azmain described the automated transcript-to-update pipeline as a potential POC test case (weekly call transcribed, notes automatically pushed to Clara — could push to Gainsight too)
- Rajesh explained Gainsight's integration options: batch export via S3 bucket (proven method) or real-time API (with limitations to assess)
- BenVH asked for API documentation and authentication details to determine Clara-side integration requirements
- Ben Brookes pushed for a formal charter defining success criteria and stakeholder responsibilities
- Gainsight team focused on sunsetting RMS Salesforce by June; POC would be fitted into that timeline
- Tina confirmed they want to start with a POC to validate system connectivity

## Decisions Made
- Azmain to create a v1 integration charter document → share with Tina and Natalia Plant
- Gainsight team to share API documentation (Rajesh and Shashank to provide)
- Kathryn Palkovics to coordinate follow-up technical sessions between the two teams
- Both sides agreed the integration should start as a POC before full implementation
- Automated meeting note push (Clara → Gainsight) identified as a potential first test case

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Create v1 Gainsight integration charter | Azmain | Next week | Open |
| Share Gainsight API documentation | Rajesh/Shashank | ASAP | Open |
| Coordinate follow-up technical sessions with Gainsight team | Kathryn Palkovics | TBD | Open |
| Provide rough POC timeline after internal regroup | Tina/Nadeem | Next week | Open |
| Assess full scope of data objects needing sync (beyond use cases) | Both teams | Follow-up session | Open |

## Stakeholder Signals
- Tina Palumbo: cooperative and solution-oriented, clearly mandated to protect Gainsight adoption while accommodating Clara's cross-functional needs
- Rajesh: technically pragmatic, offered batch and real-time options without overselling either
- Azmain: diplomatically positive ("love the idea") while protecting Clara's autonomy
- Ben Brookes: strategic framing — insisted on a written charter to pin down commitments and prevent scope creep
- BenVH: focused on technical detail — immediately asked about authentication and API specs

## Open Questions Raised
- What is the full scope of data objects that need to sync beyond use cases and blockers?
- Can Gainsight support real-time API integration, or is batch-only the practical option?
- What is the authentication method for Clara to access Gainsight APIs?
- When will the POC be scheduled given the Gainsight team's March 30 onboarding deadline?

## Raw Quotes of Note
- "We want to be mindful of trying to balance the cross functional needs while making it very streamlined for the CSMs to have one space that they work in" — Tina Palumbo, on the integration philosophy
