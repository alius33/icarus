# Chat with Stacy
**Date:** 2026-02-26
**Attendees:** Azmain Hossain, Stacy Dixstra (Speaker 1)
**Duration context:** Short (~25 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Stacy needs Excel exports from CLARA to feed into a central migration dashboard that Andy Frappe has mandated. Banking team built a Power BI migration dashboard; Andy saw it and now wants all migrations (including Insurance) reported centrally. Banking has a full-time resource dedicated to their dashboard for three months.
- Insurance migrations are fundamentally different from Banking: Banking tracks pipeline-driven migrations, while Insurance tracks switch-off dates for Risk Link and Risk Browser. Stacy also needs to incorporate Glass-to-EGL and Access-to-Access Hosting migrations, which are more pipeline-like. She tells Banking they will need to redesign their dashboard to accommodate Insurance data.
- Stacy is not asking for APIs or fancy integrations -- just a monthly Excel export from CLARA's reports feature is sufficient, since Banking already uses multiple data sources including Excel.
- Azmain walks Stacy through the reports functionality he built specifically with her needs in mind, modelled on Salesforce's report builder structure: choose a data source, select columns from related objects, save, and export.
- They discover a technical issue: adding a second object (customer legacy products) to a report does not work properly. Azmain troubleshoots live and finds the planned switch-off and actual switch-off date fields sit under the customer legacy products object, which needs a fix.
- A date override bug identified: Catherine found that when someone manually updates a date in CLARA, it does not override the date imported from the golden source spreadsheet. Azmain has the fix ready but has not deployed it yet. He warns Stacy not to rely on exports until this is resolved.
- Data cleanup ongoing: Stacy is meeting individually with CSMs to clean up account records. CSMs are nervous about deleting records, but Stacy is walking them through it. Azmain reassures that daily backups with 7-day retention mean nothing catastrophic can happen.
- Scorecard target revelation: Insurance must switch off 34 legacy products in 2026, but the target number is already shifting because CSMs made up dates in December that are proving unrealistic. Six clients have already been pushed out of 2026. However, four clients discovered to have been switched off long ago but never recorded -- these can be claimed as 2026 wins.
- Strategic reporting discussion: Stacy and Azmain discuss timing of when to report the discovered switch-offs. If they report 10 early, leadership might increase the target. They agree to pace the reporting to match a linear trajectory -- report wins at a rate that shows "exactly on schedule" rather than ahead.
- Azmain proposes adding a "reported off date" field so these legacy switch-offs can be captured in 2026 without changing the actual historical dates in the system, ensuring the data remains accurate while the reporting meets leadership expectations.

## Decisions Made
- Monthly Excel export from CLARA reports sufficient for migration dashboard -> Stacy / Azmain
- "Reported off date" field to be added to capture legacy switch-offs credited to 2026 -> Azmain
- Do not export data until date override bug is fixed -> Azmain / Stacy
- Pace reporting of discovered switch-offs to match linear trajectory against 34 target -> Stacy

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Fix date override bug (manual updates not overriding golden source dates) | Azmain | This week | Open |
| Add "reported off date" field to CLARA | Azmain | This week | Open |
| Fix report builder to support multiple object sections | Azmain | This week | Open |
| Notify Stacy when date fix is deployed so she can do a clean export | Azmain | After fix | Open |
| Write requirements document for Banking team's Power BI dashboard integration | Stacy | This week | Open |
| Continue individual CSM meetings to clean up account data | Stacy | Ongoing | Open |

## Stakeholder Signals
- Stacy is pragmatic and low-maintenance: she is not demanding real-time integrations or complex features, just a working Excel export once a month. She is doing the hard work of individually meeting CSMs to clean up data.
- Stacy is politically savvy about the scorecard: she understands the game of when to report wins and how to manage upward expectations. Her instinct to pace reporting shows experience with target-ratcheting behaviour from leadership.
- Azmain is responsive to Stacy's needs, having built the reports feature specifically for her use case, but the tooling is not fully tested -- the live troubleshooting reveals rough edges.
- The scorecard target of 34 is already questionable: based on dates CSMs fabricated in December, with six already pushed out and four retroactive wins discovered. The data integrity problems are systemic, not CLARA-specific.

## Open Questions Raised
- Will Andy Frappe's central dashboard requirement lead to additional data demands beyond the basic switch-off metrics?
- How many more retroactive switch-offs will be discovered as CSMs continue data cleanup?
- What is the actual realistic target for 2026 given the date fabrication problem?

## Raw Quotes of Note
- "Must be nice, because whatever. So anyway, I'm writing a requirements document, because they even wrote a BRD... who's got the luxury of writing a BRD anymore?" -- Stacy Dixstra, on the Banking team's dedicated dashboard resource
