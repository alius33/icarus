# HD Guidance to CSM's — 16 March 2026

**Primary project:** CLARA (IRP Adoption Tracker)
**Secondary projects:** Program Management

**Participants:** Stacy Dixtra (Speaker 1), Ben Brookes, Kevin Purn, plus multiple CSMs (Speakers 2-5)
**Duration:** ~16 minutes
**Type:** CSM team call — Americas and brokers group

---

## Summary

A call to action for CSMs to enter HD (High-Definition) model adoption data into CLARA at use-case-level granularity. The team ran a five-dimension baseline poll (same exercise done with European teams that morning) and set a hard deadline of end of March to populate all HD client data before the 1 April IRP report to leadership.

---

## Key Points

### HD Model Baseline Poll

- Ben Brookes led a polling exercise across five dimensions to baseline CSM perceptions of HD model maturity:
  1. **Scientific excellence** — from unvalidated methodology to market reference standard
  2. **Decision utility** — from aggregate portfolio reporting to dynamic pricing and trigger-based actions
  3. **Risk currency** — common language around the HD ecosystem
  4. **Operability** — from standalone tools with manual exports to fully embedded operational infrastructure
  5. **Business impact** — from cost centre to transforming business models with new products

- European teams had done the same exercise that morning. Results to be aggregated as a baseline that the team will work to improve over time.

### CLARA HD Data Gap — Call to Action

- **26 clients** currently have HD data in CLARA (migrated from Salesforce).
- **~68 clients** total need HD data entered.
- **35 Americas/brokers clients** assigned to this group need data entry by **end of March**.
- Spreadsheet with client-level HD licence data to be shared after the meeting so CSMs know what each client has.
- Stacy will also provide additional bullet points from a follow-up standup call with IOP team managers.

### Bulk Upload Debate

- A CSM (Speaker 2) asked about bulk uploading the spreadsheet data into CLARA. Stacy pushed back: continuous bulk uploads are causing data quality issues, and statuses would still need manual verification regardless.
- The CSM persisted — at least upload the base data, then update statuses manually. Saves time given other end-of-month tasks.
- Stacy: "We can chat about it in our call in an hour." Deferred but not dismissed.
- **This directly feeds the CLARA bulk update feature** flagged in the notes. Ben Brookes had already proposed a matrix UI for this (use cases on rows, HD models on columns, status grid). Requirements call with Chernell is being set up.

### Status Category Changes

- Salesforce had "testing" as a status. CLARA now has three statuses: **in progress, validation, full production**. CSMs need to be aware of the mapping change.

### Granularity: Per HD Model Per Use Case

- Data needed at the intersection of each HD model and each use case for each client. High granularity.
- Kevin Purn asked for clarification — confirmed it's per HD model, not overall HD adoption.
- Ben Brookes' rationale: need to tell a data story about where customers succeeded and where they haven't. Each HD model has specific challenges (earthquake has weighted PLDs, event response is consistently difficult). Without granular data, decisions default to opinions and loudest-voice-wins.
- Stacy confirmed: example shown was ACRISTO with 2 models (Canada wildfire, US wildfire) across 3 use cases.

### API Feature Win

- Kevin Purn highlighted a major feature release: **full RDM data export via API**. One of the biggest blockers across all clients — slowness of exporting to RDM was a universal complaint. Partners were being pushed to parquet as a workaround.

---

## Speaker Identification

| Label | Identity | Confidence | Basis |
|-------|----------|------------|-------|
| Speaker 1 | Stacy Dixtra | High | Runs the call, manages the agenda, references "our call in an hour" with Speaker 2, discusses management dashboard — consistent with known role |
| Ben Brooks | Ben Brookes | Confirmed | Named in transcript. Product vision, science-first framing, data story emphasis |
| Kevin Purn | Kevin Purn | Confirmed | Named in transcript. Technical observation about API, probing questions |
| Speaker 2 | Unknown CSM | Low | Americas CSM pushing for bulk upload. Has end-of-month deadlines. |
| Speaker 3 | Unknown | Low | Brief interjection about management dashboard |
| Speaker 4 | Unknown CSM | Low | Asks about use case level vs model level data entry |
| Speaker 5 | Unknown | Low | Brief interjection about use cases |

---

## Sentiment

- **Ben Brookes**: Passionate about data-driven decision-making. Frustrated that without granular HD data, the team is stuck in opinion-land. Wants the baselining exercise to create accountability.
- **Stacy**: Cautious about bulk uploads (quality concerns) but responsive to the team's workload pressures. Will discuss further.
- **CSMs**: Mild resistance to the workload — one CSM pushing back on manual entry, wanting upload capability. This is the same friction pattern CLARA has seen before: data entry feels like more work for CSMs.

---

## Implications

1. **CLARA bulk update feature is urgent** — CSMs are already asking for it. The 35-client, end-of-March deadline creates immediate pressure. Ben Brookes' matrix UI proposal (from the project update context) is the right answer.
2. **April 1 is a hard deadline** — first IRP report with HD data goes to leadership. Incomplete data means incomplete story.
3. **The granularity requirement is significant** — each model × each use case × each client. This is a lot of data entry. Without bulk tools, compliance will be patchy.
4. **Status mapping could cause confusion** — Salesforce→CLARA status changes (testing → in progress/validation/full production) need clear communication.
5. **API/RDM export win** should be surfaced — Kevin Purn's highlight about full RDM data via API is a genuine adoption unblocker that the team can use in their HD success narrative.
