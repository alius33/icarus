# Meeting with Dan Flemington
**Date:** 2026-03-04
**Attendees:** Azmain Hossain, Richard Dosoo, Dan Flemington (Speaker 1)
**Duration context:** Medium (~30 minutes)
**Workstreams touched:** Sales enablement (new), WS2 CLARA (Salesforce integration)

## Key Points
- Dan Flemington is a sales leader who has independently been building Python tools in Cursor for his own workflow automation. He is a new stakeholder and potential ally.
- Dan demonstrated two tools he built: (1) An email formatter that takes a Salesforce forecast accountability report CSV, transforms it, and generates a formatted management email. (2) A variance report that compares two date-stamped Salesforce exports and highlights changes (stage changes, probability changes, value changes) with hyperlinks back to Salesforce.
- The variance report concept was immediately adopted by Azmain for CLARA -- CSMs have been asking for a "what changed since I last logged in" view. Dan's approach (compare two snapshots, show deltas) maps directly to this need.
- Dan introduced Julia Valencia from sales analytics as a critical enabler. She has direct access to the SFDC CDR database (the underlying Salesforce data layer, not just reports). She can explain the data model and help gain programmatic access.
- Richard identified significant convergence: CLARA already needs Salesforce integration (for Bernard, Courtney, Kevin Pern). Dan's needs are "another thing we add to the list." The underlying infrastructure work (Salesforce programmatic access) serves multiple teams.
- Dan's tools are candidates for App Factory hosting once they mature. Richard walked him through the infrastructure (dev -> staging -> production pipeline), authentication (Moody's SSO), and offered cursor rules files and migration prompts.
- Richard sent Dan a training document and cursor rules file for aligning his apps with the team's tech stack (Postgres, AWS, their API patterns).
- Dan needs GitHub access (ticket already raised) to version control and share his code.
- Dan is going to Vienna for SKO next week; follow-up after his return.
- Richard explicitly framed the value proposition: "The cost of getting this stuff wrong is practically zero" with modern tools, so iteration is cheap.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Dan's variance report concept adopted for CLARA | Feature | High | Azmain |
| Julia Valencia identified as Salesforce data access contact | Resource | High | Dan |
| Dan's tools to be considered for App Factory hosting | Architecture | Medium | Richard |
| Dan to connect Julia Valencia with Richard and Azmain | Process | High | Dan |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Send email connecting Julia Valencia with Richard and Azmain | Dan | This week | Open | High |
| Follow up with Julia on SFDC CDR access and data model | Richard/Azmain | While Dan is in Vienna | Open | High |
| Send cursor rules file and training doc to Dan | Richard | Today | Open | High |
| Get GitHub access approved for Dan | Dan/IT | In progress | Open | Medium |
| Add Dan's Salesforce data needs to the access request list | Richard | This week | Open | High |

## Theme Segments
1. **Dan's existing tools demo** (0:00-10:00) -- Email formatter and variance report
2. **Salesforce data access opportunity** (10:00-16:00) -- Julia Valencia, CDR database, programmatic access
3. **App Factory and hosting** (16:00-22:00) -- How Dan's tools could be hosted; infrastructure walkthrough
4. **Enablement and next steps** (22:00-30:00) -- Cursor rules, training docs, GitHub access, Vienna timeline

## Power Dynamics
- **Dan enters as a peer, not a subordinate.** He is a sales leader who has already built useful tools independently. Richard and Azmain treat him as a collaborator.
- **Richard is the connector and enabler.** He frames the conversation strategically (linking Dan's needs to existing CLARA plans) and provides technical resources.
- **Azmain is opportunistic in the best sense.** He immediately sees how Dan's variance report maps to a CLARA user request and "steals" the concept enthusiastically.
- **Dan brings something the team lacks**: a direct contact (Julia Valencia) with Salesforce database access. This is a gating resource for multiple programme needs.

## Stakeholder Signals
- **Dan Flemington** -- Self-starter, already building in Cursor, pragmatic about what he needs. Not territorial -- openly shares his tools and connections. Potential strong ally for sales/CS convergence.
- **Julia Valencia** (mentioned) -- Critical new contact. Has direct access to SFDC CDR database. Could unlock Salesforce programmatic access that has been blocked for months.
- **Richard** -- Sees the bigger picture: Dan's needs plus Bernard's plus Courtney's plus Kevin Pern's all require the same underlying Salesforce integration. Efficient thinker.
- **Azmain** -- Energised by the variance report concept. Immediately maps it to existing CLARA user requests.

## Commitments Made
| Who | Commitment | To Whom | Context |
|-----|-----------|---------|---------|
| Dan | Connect Julia Valencia with the team | Richard/Azmain | Salesforce access |
| Richard | Send training materials and cursor rules | Dan | Enablement |
| Richard | Follow up with Julia while Dan is in Vienna | Dan | Data access |
| Richard | Add Dan's tools to App Factory pipeline list | Dan | Hosting |

## Meeting Effectiveness
| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 8 | Clear next steps and mutual value identified |
| Decision quality | 8 | Excellent opportunity recognition (variance report, Julia) |
| Participation balance | 8 | All three contribute meaningfully |
| Action item specificity | 7 | Good specificity with travel-bounded timeline |
| Strategic alignment | 9 | Directly addresses Salesforce integration need across multiple workstreams |

## Risk Signals
- **LOW: Dan's tools are pre-governance.** He is building on his laptop without version control or security review. App Factory hosting would mitigate this but is not yet available.
- **LOW: Julia Valencia is a single point of access.** If she is unwilling or unable to help, Salesforce programmatic access remains blocked.

## Open Questions Raised
- What is the SFDC CDR data model and what access restrictions exist?
- Can they get automated daily data feeds rather than manual CSV exports?
- Should Dan's tools eventually move to the same tech stack as CLARA?

## Raw Quotes of Note
- "I'm definitely going to steal your variance report." -- Azmain, immediately adopting Dan's concept for CLARA
- "It's like, you're changing your gearbox, you might as well change the clutch at the same time." -- Richard, on combining Salesforce access needs across teams

## Narrative Notes
This is the most productive new stakeholder meeting of the week. Dan Flemington arrives as an unexpected gift: a sales leader who is already building tools in Cursor, has substantive working prototypes, and brings the single most valuable resource the programme has been missing -- a contact with direct Salesforce database access (Julia Valencia). The variance report concept is a genuine cross-pollination moment: Dan built it for sales pipeline tracking, Azmain immediately maps it to CLARA's "what changed" user request. Richard's strategic framing is excellent -- he positions all the Salesforce integration needs (Bernard, Courtney, Kevin Pern, Dan) as one pipeline, making the infrastructure investment more justifiable. The biggest takeaway: Dan is exactly the kind of self-starter the programme needs as an ally, and Julia Valencia could be the key that unlocks the Salesforce data access that has been a blocker for months.
