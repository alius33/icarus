# Meeting with Dan Flemington
**Date:** 2026-03-04
**Attendees:** Azmain Hossain, Richard Dosoo, Dan Flemington (Speaker 1)
**Duration context:** Medium (~30 minutes)
**Workstreams touched:** WS2 CLARA (tangential -- Salesforce integration), Sales enablement

## Key Points
- **New stakeholder: Dan Flemington** -- a sales leader who has already been building his own tools in Cursor. This is a first contact for collaboration, not someone previously tracked in the programme.
- **Dan's existing tools**: He has already built two Python-based tools: (1) an automated email formatter that takes a Salesforce forecast accountability report CSV extract, transforms it into a narrative email format with monthly stratification and summaries; (2) a variance report tool that compares two Salesforce extracts and identifies what changed (month, probability, value) with hyperlinks back to SFDC. He is also building a dashboard that aggregates opportunities, quotes, growth, and top deals by month.
- **Dan's roadmap**: He wants to build historical opportunity tracking -- storing daily snapshots to tell the story of how opportunities evolved over 30+ days. Previously did this manually with pivot tables and heat maps.
- **Salesforce data access opportunity**: Dan introduced Julia Valencia from the sales analytics reporting team who has access to the underlying SFDC data (CDR database). She can explain the data model, which fields to use, and help ensure numbers align with official reporting. Richard and Azmain plan to follow up with her while Dan is at the Vienna SKO.
- **Convergence with CLARA needs**: Richard identified that CLARA also needs Salesforce integration for Bernard (customer sentiment from tickets) and Courtney (HD models analysis). The pipeline Dan needs from SFDC is "just another data set" they would extract alongside existing requirements.
- **Variance report concept adopted for CLARA**: Azmain immediately flagged that CLARA users are requesting exactly the same thing -- a variance view showing what changed since the last login (health status, executive status, field changes). He plans to implement Dan's variance approach.
- **App Factory hosting offer**: Richard offered to host Dan's tools on the App Factory infrastructure once they are validated, giving other sales team members access. Dan confirmed multiple people have already expressed interest in his tools.
- **Enablement approach**: Richard will send Dan cursor rules files, migration prompts, and training slides to help him re-architect his tools to use the team's standardised tech stack (Postgres, standard API patterns, SSO).
- **GitHub access**: Richard raised a ticket for Dan to get GitHub access, which will enable version control and sharing.

## Decisions Made
- Dan to connect Richard/Azmain with Julia Valencia for Salesforce data access -> Dan
- Dan's pipeline requirements to be added to the Salesforce data integration list alongside Bernard's and Courtney's -> Richard
- Richard to send Dan cursor rules and migration prompts for tech stack alignment -> Richard
- Dan's tools are candidates for App Factory hosting once validated -> Richard

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Send email connecting Richard/Azmain with Julia Valencia | Dan | Today/tomorrow | Open |
| Follow up with Julia Valencia while Dan is in Vienna | Richard/Azmain | Next week | Open |
| Send cursor rules, migration prompts, and training slides to Dan | Richard | Today | Open |
| Send CSV extract of forecast accountability report to Richard/Azmain | Dan | TBD | Open |
| Get GitHub access approved for Dan | Richard (ticket raised) | TBD | Open |
| Add Dan's pipeline requirements to Salesforce integration list | Richard | TBD | Open |

## Stakeholder Signals
- **Dan Flemington** is a self-starter who has built useful tools independently. He is sales-side, which means the programme is now attracting interest beyond CS. He is practical about not wanting to distribute flawed tools widely.
- **Richard** sees the strategic opportunity: the same Salesforce data extraction capability serves multiple projects. He is thinking in terms of economies of scale and shared infrastructure.
- **Azmain** is energised by the variance report concept -- it directly solves a user request in CLARA. This is a good example of cross-pollination across the programme.
- **Julia Valencia** is a new name -- she sits in sales analytics and has direct access to the underlying SFDC database. She could be a critical enabler for multiple workstreams.

## Open Questions Raised
- Can programmatic access to Salesforce be secured? (Previously blocked)
- What does the CDR data model look like?
- How many data fields per opportunity are available and which are stable/foundational?
- Will Dan's tools live on his machine or move to App Factory?

## Raw Quotes of Note
- "The cost of you building something and deciding you don't want to do it is less than it was before." -- Richard, to Dan, on the new development paradigm
