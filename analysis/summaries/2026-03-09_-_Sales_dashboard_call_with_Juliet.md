# Sales Dashboard Call with Juliet Valencia
**Date:** 2026-03-09
**Attendees:** Richard Dosoo, Azmain Hossain, Juliet Valencia (Speaker 1)
**Duration context:** Short (~17 min with Juliet, then ~8 min private sidebar between Richard and Azmain)
**Primary project:** Cross OU Collaboration
**Secondary projects:** CLARA, Sales Recon, Program Management

## Key Points
- Richard and Azmain met with Juliet Valencia (sales analytics / Power BI dashboards) to discuss Dan Flemington's Salesforce data workflow
- Dan has built a semi-automated process: Juliet provides a report → Dan puts it in a folder → his Cursor app ingests it → generates a report. They want to fully automate this with API access
- **The data Dan uses is likely from SPM team (Tableau), not Juliet's Sales Hub.** Juliet clarified she doesn't send Dan anything directly — the data appears to come from SPM. SPM data has rep/manager-level detail; Juliet's Sales Hub data does not
- Juliet will connect them with SPM team contacts once Dan confirms which data he's using (Dan is in Vienna until next week)
- There are security restrictions on who can access SPM/Tableau data — formal request to named individuals is required
- Richard pitched the App Factory as the hosting/deployment solution for Dan's app (AWS with user access controls already built)
- **Juliet also uses Cursor** to build Power BI dashboards. Richard offered to share the team's skills repo and prompt library
- Richard added Juliet to the "tooling for customer success" Teams channel

## Post-Juliet Sidebar (Richard & Azmain)
- **Strategic framing of cross-department work:** Richard explained that the Dan engagement, banking meeting, asset management, Life, and Singapore outreach collectively build the case for Diya to approve a dedicated team with proper resources
- **Banking meeting tomorrow** was set up by Diya herself via MENA (banking counterpart to Diya). Organisational mapping clarified: MENA → Irina → Idris (parallels Diya → [intermediate] → Ben)
- **Richard bullish on formal team approval:** "I think it's gonna happen, bro" — believes cross-OU demand makes the business case undeniable
- **Azmain bucketing all cross-OU work** under "Cross OU Collaboration" in Friday for project management
- **Richard's health:** Broken toe, diabetic ulcers from running, doctor told him to stop. On Ramadan fast. Staying home all week
- **Planning to organise:** Richard will spend time getting organised, plan a CLARA build for next week, reduce chaos. Azmain also catching up on notes and transcripts
- **Azmain delegating CLARA small fixes to Chris** — staying away from CLARA work to create brain space
- **Azmain joining advisory call** because Diana said "this is a shit show, please can you join"

## Decisions Made
- Dan's app will eventually be deployed to App Factory, not run locally → Richard, strategic direction
- Wait for Dan to confirm whether his data source is SPM/Tableau before pursuing access → practical

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Message Dan to confirm which data source he uses (Tableau/SPM vs Sales Hub) | Richard | Sent (awaiting reply, Dan in Vienna) | Open |
| Connect Richard/Azmain with SPM team contacts once data source confirmed | Juliet | Next week (when Dan returns) | Open |
| Share skills repo and prompt library with Juliet and the tooling channel | Richard | End of this week | Open |
| Organise programme workload and plan CLARA build for next week | Richard | This week | Open |

## Stakeholder Signals
- **Juliet Valencia** — Cooperative, knowledgeable about data governance. Clear about boundaries (won't share data she doesn't own). Already a Cursor user, interested in learning more. Good potential ally for the Salesforce data access push
- **Richard Dosoo** — Despite health issues and flight risk, still strategically driving cross-OU expansion. His framing of every new engagement as building the business case for a dedicated team shows long-term commitment — or legacy-building before departure
- **Azmain** — Self-aware about being overwhelmed. Actively creating space by delegating to Chris. Using Friday to organise project portfolio. Recognises the "octopus legs" growth pattern

## Open Questions Raised
- Is Dan's data from SPM/Tableau or from Juliet's Sales Hub? (Likely SPM but awaiting confirmation)
- Will SPM team grant programmatic API access, or will there be security/governance pushback?
- What is the timeline for onboarding Dan's app to App Factory?

## Raw Quotes of Note
- "Everybody thinks everything comes from me, but it doesn't" — Juliet, clarifying data ownership boundaries
