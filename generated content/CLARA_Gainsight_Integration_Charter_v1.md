# CLARA-Gainsight Integration Charter

**Version:** 1.0 (Draft)
**Date:** 13 March 2026
**Author:** Azmain Hossain, Customer Success Gen AI Programme
**Status:** For Review

---

## 1. Purpose

This charter defines the scope, responsibilities, timeline, and success criteria for integrating CLARA (the IRP Adoption Tracker) with Gainsight. It exists to ensure both teams have a shared understanding of what will be built, by whom, and by when — so that no party is surprised by requirements, resource demands, or delivery expectations during execution.

---

## 2. Background

**Gainsight** is being rolled out as the system of record for Customer Success Managers (CSMs) across Moody's Analytics Insurance Division. It provides a unified view of customer health, engagement, time tracking, and BAU activities. CSMs are being onboarded to Gainsight with a production go-live target of 30 March 2026.

**CLARA** is an internally built web application that tracks IRP (Intelligent Risk Platform) adoption and migration across the insurance portfolio. It serves cross-functional teams — not just CSMs, but also product, implementation, and advisory teams — who need visibility into IRP use cases, blockers, adoption milestones, and migration progress. CLARA is used in weekly Portfolio Reviews and is the primary reporting surface for senior leadership migration metrics.

**The problem:** CSMs currently need to work in both systems. Gainsight holds customer health, engagement, and BAU activities. CLARA holds IRP-specific use case tracking, blocker management, and migration reporting. Without integration, CSMs must duplicate data entry, and cross-functional teams lose visibility into CSM-side activities.

**The goal:** Enable CSMs to work primarily in Gainsight while ensuring IRP adoption data flows seamlessly to CLARA, and that cross-functional inputs captured in CLARA are visible back in Gainsight.

---

## 3. Parties & Stakeholders

### CLARA Team
| Name | Role |
|------|------|
| Azmain Hossain | Programme Manager & Lead Developer, CLARA |
| Ben Brookes | Product Owner, CLARA |
| Richard Dosoo | Programme & Operational Owner |
| BenVH (Van Houten) | Infrastructure Engineer (AWS, CI/CD, App Factory) |

### Gainsight / Business Systems Team
| Name | Role |
|------|------|
| Tina Palumbo | Business Systems, Gainsight Programme Lead |
| Rajesh | Solution Architect, Gainsight |
| Shashank | Technical Lead, Gainsight Application |
| Nadeem | Project Manager, Gainsight Programme |

---

## 4. Guiding Principles

1. **Gainsight is the system of record for CSM BAU activities.** CSMs should not be required to enter the same data in two systems.
2. **CLARA is the system of record for cross-functional IRP adoption tracking.** Product, implementation, and advisory teams work in CLARA and should not need Gainsight access.
3. **Integration must be bi-directional.** Gainsight-originated data (use cases, blockers from CSMs) must flow to CLARA. CLARA-originated data (blockers from product/implementation teams, automated meeting notes) must flow back to Gainsight.
4. **Neither system replaces the other.** Gainsight covers the full customer lifecycle. CLARA covers IRP adoption specifically. The overlap is the IRP use case and blocker dataset.
5. **Start small, prove connectivity, then expand.** A POC must demonstrate end-to-end data flow before any production integration is built.
6. **No disruption to active migrations.** The CLARA team's primary obligation is supporting the 2026 insurance scorecard target of 30+ IRP migrations. Integration work must not divert resources from this.

---

## 5. Scope

### 5.1 In Scope — Phases 1-3 (This Quarter)

The following Salesforce/Gainsight objects will be synchronised with CLARA in a phased approach:

#### Phase 1 — Foundation (Accounts & Customer Updates)
| Source Object | CLARA Target | Direction | Notes |
|---------------|-------------|-----------|-------|
| Account (Parent + Sub) | `parent_accounts` / `customers` | Gainsight -> CLARA | Establishes the account hierarchy. Must include parent-subsidiary relationships. CLARA currently holds 155+ active accounts. |
| Customer Weekly Updates | `customer_updates` | Bi-directional | Per-account executive summaries and meeting notes. CLARA auto-generates these from transcribed weekly calls. CSMs also enter updates in Gainsight. Both sources must be visible in both systems. |

#### Phase 2 — Core IRP Data
| Source Object | CLARA Target | Direction | Notes |
|---------------|-------------|-----------|-------|
| Contact / User | `employees` (CSM assignments) | Gainsight -> CLARA | Maps CSMs and key contacts to accounts. |
| Case / Custom Object (Blocker) | `blockers` | Bi-directional | CSM-created blockers originate in Gainsight. Product/implementation-created blockers originate in CLARA. Both systems must reflect the full set. |
| Success Criteria (CSC) | `success_criteria` | Bi-directional | IRP use case success criteria tracked by CSMs in Gainsight, supplemented by product teams in CLARA. |

#### Phase 3 — Extended Data
| Source Object | CLARA Target | Direction | Notes |
|---------------|-------------|-----------|-------|
| Product Adoption (PAT) | `product_adoption_tracking` | Gainsight -> CLARA | Adoption milestone data for IRP products. |
| Task / Activity | `action_plans` / `items` | Bi-directional | Cross-functional action items. CSM tasks from Gainsight, product/implementation tasks from CLARA. |
| Full Case Feed | `case_feed` (new table) | Gainsight -> CLARA | Historical case context for blocker analysis and reporting. New data object in CLARA. |

### 5.2 On Roadmap — Phase 4+ (Future State)

The following are acknowledged as valuable but explicitly **out of scope** for the current charter. They require separate scoping once Phases 1-3 are delivered and stable.

| Capability | Description | Dependency |
|------------|-------------|------------|
| Microsoft 365 Context (Graph API) | Email + meeting signals per account to enrich CS Agent synthesis | Graph API access, security review |
| Usage Telemetry (MIDAS / Mixpanel) | Product usage signals for adoption scoring and proactive engagement | MIDAS integration, data pipeline |
| NPS Verbatim & Detractor CTAs | Survey data for sentiment overlay (closes AMBER scorecard item) | Qualtrics integration |
| Gainsight Health Scores (read-only) | CSM qualitative health as context signal — Gainsight remains SoR | Gainsight reporting API |
| Write-back to Salesforce / Gainsight | Gated, future-state capability — requires governance approval | Governance framework, security review |

---

## 6. Integration Architecture

### 6.1 Proposed Pattern

Based on the Gainsight team's presentation and technical discussion on 12 March 2026:

```
Salesforce (CRM)
    |
    v
Gainsight (CSM System of Record)
    |
    |--- Batch (S3 Bucket) ---> CLARA  [Master data: accounts, contacts]
    |
    |--- API (Real-time) <----> CLARA  [Transactional: blockers, use cases, tasks]
    |
    v
Databricks (Reporting & Analytics)
```

### 6.2 Integration Methods

| Data Type | Method | Frequency | Rationale |
|-----------|--------|-----------|-----------|
| Account (Parent + Sub) | Batch (S3 export) | Daily | Low change frequency. Batch is proven and low-risk. |
| Customer Weekly Updates | API (real-time) | On create/update | Auto-generated meeting summaries from CLARA and CSM-entered updates from Gainsight. Timeliness matters for cross-functional visibility. |
| Contact / User | Batch (S3 export) | Daily | Low change frequency. |
| Blocker (Case / Custom) | API (real-time) | On create/update | CSMs and product teams need to see blockers immediately. Delay causes duplicate work. |
| Success Criteria | API (real-time) | On create/update | Active during customer engagements. Timeliness matters. |
| Product Adoption (PAT) | Batch (S3 export) | Daily | Milestone data, not time-critical. |
| Task / Activity | API (real-time) | On create/update | Cross-functional task coordination requires immediacy. |
| Case Feed | Batch (S3 export) | Daily | Historical context. No real-time requirement. |

### 6.3 Authentication & Connectivity

The Gainsight team will provide:
1. API documentation (endpoints, schemas, rate limits, error handling)
2. Authentication method and credentials (API key, OAuth, SSO — to be confirmed)
3. S3 bucket configuration for batch data exchange (IAM roles, encryption, access policies)
4. Sandbox / test environment access for POC development

The CLARA team will provide:
1. CLARA API specification (REST endpoints for all objects listed in Section 5)
2. Authentication details for CLARA's API
3. Data mapping document (Gainsight field -> CLARA field, with transformation rules)
4. Test environment access

### 6.4 Middleware

Integration orchestration will be managed through the **App Factory** platform (CLARA's AWS infrastructure layer). App Factory will handle:
- API call orchestration and retry logic
- Data transformation between Gainsight and CLARA schemas
- Error logging and alerting
- Rate limiting and backpressure management

This approach ensures the integration layer is vendor-agnostic and can be adapted if the underlying systems change.

---

## 7. Responsibilities

### 7.1 Gainsight / Business Systems Team Owns:
- Gainsight API documentation and access provisioning
- S3 bucket setup and configuration for batch exports
- Gainsight sandbox environment for POC
- Data export scheduling and reliability (batch jobs)
- Gainsight-side webhook or event configuration for real-time sync
- Gainsight data model documentation (field definitions, relationships, constraints)
- CSM change management (ensuring CSMs know how to enter IRP data in Gainsight)
- Gainsight-side testing and validation of inbound data from CLARA
- Project management coordination (Nadeem)

### 7.2 CLARA Team Owns:
- CLARA API endpoints for receiving and sending data
- Data transformation and mapping logic (Gainsight schema -> CLARA schema)
- CLARA-side storage, indexing, and display of Gainsight-sourced data
- Integration orchestration via App Factory middleware
- CLARA-side testing and validation of inbound data from Gainsight
- Reporting and dashboards that consume integrated data
- Technical architecture and infrastructure for the CLARA side of the integration

### 7.3 Joint Responsibilities:
- Data mapping agreement (which fields map where, transformation rules)
- Integration testing (end-to-end validation across both systems)
- Error handling and escalation procedures
- POC evaluation and go/no-go decision
- Ongoing monitoring and incident response post-launch

---

## 8. Success Criteria

### 8.1 POC Success Criteria

The POC is considered successful when **all** of the following are demonstrated:

1. **Connectivity proven:** CLARA can authenticate with and read from the Gainsight API (or consume S3 exports).
2. **Account sync working:** At least 10 parent accounts with subsidiaries successfully synced from Gainsight to CLARA, with correct parent-subsidiary hierarchy.
3. **Blocker round-trip:** A blocker created by a CSM in Gainsight appears in CLARA within 5 minutes. A blocker created by a product team member in CLARA appears in Gainsight within 5 minutes.
4. **Data integrity validated:** Synced records match across both systems — no data loss, no field truncation, no encoding issues.
5. **No regression in CLARA:** CLARA's existing functionality (Portfolio Reviews, management dashboards, migration reporting) is unaffected by the integration.
6. **Performance acceptable:** API response times remain under 2 seconds. Batch jobs complete within agreed windows. No degradation to either system's user experience.

### 8.2 Production Success Criteria

1. All Phase 1-3 data objects synchronised per the schedule defined in Section 6.2.
2. CSMs can enter IRP use cases and blockers in Gainsight and see them reflected in CLARA without manual intervention.
3. Cross-functional teams can enter blockers and action items in CLARA and have them visible in Gainsight without manual intervention.
4. Zero instances of CSMs needing to double-enter data across both systems for objects covered by the integration.
5. CLARA's management reporting accurately reflects data from both sources.
6. Integration uptime of 99.5% during business hours (08:00-18:00 GMT).

---

## 9. Timeline

### 9.1 Constraints

- **Gainsight onboarding deadline:** 30 March 2026 (RMS, Cape, Predicate teams). The Gainsight team will have no capacity for integration work before this is complete.
- **Post-launch stabilisation:** Approximately 4 weeks after go-live (April 2026) for Gainsight to stabilise with new user groups.
- **CLARA graduate onboarding:** Two rotating graduates arriving 7 April 2026. These resources will be available for integration support from May onwards.
- **CLARA team priority:** The 2026 insurance scorecard target (30+ migrations) is the CLARA team's primary obligation. Integration work is secondary.

### 9.2 Proposed Milestones

| Phase | Milestone | Target Date | Owner |
|-------|-----------|-------------|-------|
| 0 | Charter signed off by both teams | TBD | Azmain / Tina |
| 0 | Gainsight API documentation shared with CLARA team | TBD | Rajesh / Shashank |
| 0 | CLARA API specification shared with Gainsight team | TBD | Azmain / BenVH |
| 0 | Data mapping document agreed | TBD | Joint |
| 1 | POC environment setup (sandbox access both sides) | TBD | Joint |
| 1 | POC: Batch account sync + customer updates (Phase 1 data) | TBD | Joint |
| 1 | POC: Real-time blocker sync (Phase 2 core) | TBD | Joint |
| 1 | POC evaluation and go/no-go decision | TBD | Joint + Governance |
| 2 | Phase 2 production build (contacts, blockers, success criteria) | TBD | Joint |
| 3 | Phase 3 production build (adoption, tasks, case feed) | TBD | Joint |
| — | Phase 4+ scoping begins | TBD | Joint |

### 9.3 Governance Checkpoints

Integration work will be reviewed as part of the CLARA governance process (fortnightly Tuesday reviews, facilitated by Natalia Plant). Key governance gates:

1. **Charter approval** — both teams and governance leads sign off
2. **POC go/no-go** — based on POC success criteria (Section 8.1)
3. **Phase 2 go/no-go** — based on POC results and resource availability
4. **Phase 3 go/no-go** — based on Phase 2 stability and remaining scope

---

## 10. Risks & Mitigations

| # | Risk | Severity | Mitigation |
|---|------|----------|------------|
| 1 | Gainsight API limitations prevent real-time sync for blockers/tasks | HIGH | POC specifically tests real-time API capability. Fallback: near-real-time batch (every 15 minutes) via S3. |
| 2 | Integration work diverts CLARA team from migration support | HIGH | Integration work is explicitly secondary to migration targets. Governed via fortnightly reviews. Graduate resources (from May) to be allocated to integration. |
| 3 | Data model mismatch between Gainsight and CLARA | MEDIUM | Data mapping document agreed before any build work. Transformation logic centralised in App Factory middleware. |
| 4 | Gainsight team capacity constrained by RMS onboarding | MEDIUM | Timeline explicitly accounts for March-April Gainsight stabilisation. No POC work until May at earliest. |
| 5 | Bi-directional sync creates data conflicts | MEDIUM | Clear ownership rules per data type (Section 5). Conflict resolution: source system wins. Audit trail for all sync operations. |
| 6 | Scope creep into Phase 4+ items during POC | MEDIUM | Phase 4+ items explicitly deferred in charter. Any additions require governance approval and charter amendment. |
| 7 | CSM adoption of new Gainsight IRP workflows is low | MEDIUM | Gainsight team owns CSM change management and training. CLARA team provides cross-functional workflow documentation. |
| 8 | Authentication/security review delays access provisioning | LOW | Raise security review requests early (Phase 0). Both teams to engage security contacts in parallel. |

---

## 11. Change Control

Any changes to the scope, timeline, or responsibilities defined in this charter must be:

1. Raised in writing (email or shared document comment)
2. Reviewed at the next fortnightly governance session
3. Agreed by both the CLARA team lead (Azmain) and the Gainsight programme lead (Tina)
4. Approved by governance (Natalia Orzechowska)
5. Documented as a charter amendment with version number and date

No work outside the defined scope will be undertaken without an approved charter amendment.

---

## 12. Assumptions

1. Gainsight will have stable API and S3 export capabilities available for the POC by May 2026.
2. The Gainsight team will provide dedicated technical resource (Rajesh/Shashank) for integration sessions.
3. CLARA's existing AWS infrastructure (App Factory) can support the integration middleware without additional provisioning.
4. Both teams will have sandbox/test environments available that mirror production data structures.
5. CSMs will have been trained on entering IRP data in Gainsight before the integration goes live.
6. Salesforce data (accounts, contacts, cases) will continue to flow into Gainsight and does not need to be independently sourced by CLARA.

---

*This charter is a living document. Version history will be maintained below.*

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 13 Mar 2026 | Azmain Hossain | Initial draft |
