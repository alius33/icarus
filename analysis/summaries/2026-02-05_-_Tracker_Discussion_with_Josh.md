# Tracker Discussion with Josh
**Date:** 2026-02-05
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH, Martin Davies
**Duration context:** Long (~33 minutes)
**Workstreams touched:** WS2 CLARA, WS6 Build in Five

## Key Points
- Richard spoke to Josh and Kathryn Palkovics the previous night and is relaying their feedback to the team
- Key data issue: action plans not populated. Azmain clarified that next steps data IS in the database but the frontend does not surface it -- a UI fix, not a data gap
- Design disagreement on action plans: Josh/Kathryn Palkovics want every blocker to automatically generate an action plan with one action item ("path to green"). Azmain argues this creates bloatware -- every blocker would have a single-line action plan inherited from the "next steps" field, not a structured plan with assigned items
- Ben Brookes aligned with Azmain: Josh is not thinking structurally, just wants it to look and act like Salesforce. "Make it Salesforce" is the unspoken demand.
- Separate data issue: product adoption table has duplicate rows -- same use case appearing multiple times with different PAT (Product Adoption Tracking) numbers. Salesforce stores all historical rows but only displays the latest. The import needs to aggregate and keep only the latest row per product per customer.
- BenVH now has direct database access on AWS RDS -- can run queries and stored procedures to clean duplicate data
- Azmain's plan: address Josh/Kathryn Palkovics' feedback items, then focus on Natalia's portfolio review redesign -- both must be done before Monday
- Martin was properly briefed on Build in Five during this call -- heard the two-dimension explanation (internal productivity + external client demos) and the naming confusion was resolved
- Richard assigned Martin to work with Azmain on scoping Build in Five, creating a skeleton project plan before Martin's holiday
- Cross-OU session debrief: BenVH noted Amanda's tool lacks authentication -- serious concern for any tool storing Moody's data. First time BenVH raised this concern in a group setting.
- Azmain observed a pattern: non-developers building AI tools do not think about UX, security, or scalability -- Amanda's tool is a case study. This is exactly what Build in Five needs to address with guardrails.
- BenVH proposed a project management conversation step before app creation, producing HTML mockups before any real code -- ensures requirements are captured before the app factory generates a full application
- Explicit prototyping step agreed: static HTML pages for reference and feedback, iterating until user is happy and agent has validated requirements, before generating full React/database application
- Azmain's guardrails concept: a massive README with Moody's guidelines, security rules, architecture specs embedded in the app factory so the AI agent stays within a governed walled garden
- Mobile responsiveness issues demonstrated live: sidebar not collapsible, cards not stacking on small screens, horizontal scrolling required
- BenVH offered to work on mobile responsiveness as a background task
- Natalia and Stacy sent a new list of priority customers, accelerated customers, and 2026 migration clients -- Azmain needs to assign them. Dev and production databases are separate, so assignments in dev will not carry over.

## Decisions Made
- **Next steps data to be surfaced in the blocker view UI -- fix the frontend** | Type: Technical | Confidence: High | Owner: Azmain
- **Duplicate product adoption rows to be cleaned -- keep only latest per product per customer** | Type: Data quality | Confidence: High | Owner: BenVH/Azmain
- **Action plans stay as designed (structured plans, not auto-generated from blockers) -- push back on Josh** | Type: Design | Confidence: Medium | Owner: Azmain to communicate
- **Build in Five scope to be drafted Mon-Tue by Martin/Azmain** | Type: Planning | Confidence: Medium | Owner: Martin/Azmain
- **Explicit prototyping step (static HTML) before full app generation in app factory** | Type: Architecture | Confidence: High | Owner: Team
- **Mobile responsiveness to be addressed as background work** | Type: UX | Confidence: Medium | Owner: BenVH

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Surface next steps data in blocker frontend view | Azmain | Before Monday | Open | High |
| Clean duplicate product adoption rows in database | BenVH/Azmain | Before Monday | Open | High |
| Communicate action plan design rationale to Josh | Azmain | Today | Open | Medium |
| Apply Natalia's priority/tab changes to portfolio review | Azmain | Before Monday | Open | High |
| Draft Build in Five skeleton project plan | Martin/Azmain | Mon-Tue next week | Open | Medium |
| Make app responsive/mobile-friendly (sidebar, card stacking) | BenVH | Background task | Open | Medium |
| Assign new priority/accelerated customer lists in production | Azmain | Before Monday | Open | High |

## Theme Segments
1. **Josh/Kathryn Palkovics Feedback Relay (0:00-5:00)** -- Action plans missing, design disagreement on blocker-to-action-plan automation
2. **Data Quality: Duplicate Product Adoption Rows (5:00-11:00)** -- Salesforce historical rows creating duplicates, BenVH database access for cleanup
3. **Build in Five Scoping (11:00-17:00)** -- Martin properly briefed, two-dimension framework, naming confusion resolved, scoping assignment
4. **Cross-OU Session Debrief and App Factory Vision (17:00-28:00)** -- Amanda's tool, authentication concerns, non-developer pattern, prototyping step proposal
5. **Mobile Responsiveness and Wrap-up (28:00-33:00)** -- Live demonstration of UI issues, BenVH takes on background responsiveness work

## Power Dynamics
- **Richard** is the relay between Josh/Kathryn Palkovics and the build team. He translates their complaints into actionable items without taking sides, though he leans toward Azmain's design rationale
- **Azmain** is frustrated but disciplined -- he understands Josh's complaint but refuses to build bloatware. His phrase "make it Salesforce" captures the tension between mimicking the familiar and building something better
- **BenVH** emerges as both the infrastructure operator (database access, cleanup queries) and the architecture thinker (project management conversation, HTML prototyping step). His dual role is increasingly important.
- **Martin** is absorbing context rapidly. The naming confusion resolution marks his transition from confused observer to engaged participant.
- **Josh/Kathryn Palkovics (offscreen)** -- their influence is felt through Richard's relay. They push for Salesforce-like behaviour and data perfection, creating friction with the build team's approach.

## Stakeholder Signals
- **Josh Ellingson (offscreen):** Continues to push for Salesforce-like behaviour. His request that every blocker auto-generates an action plan reveals a mindset rooted in the familiar rather than thinking about what a purpose-built tool should do differently. Azmain's frustration is growing but he is choosing diplomacy over confrontation.
- **Kathryn Palkovics (offscreen):** The data quality enforcer. Her knowledge of Salesforce internals (PAT number deduplication, historical row behaviour) is valuable for data cleaning.
- **Martin Davies:** Now properly oriented. His immediate willingness to start scoping Build in Five shows engagement once the confusion is resolved.
- **BenVH:** His observation about Amanda's tool -- that non-developers do not think about authentication -- is the insight that shapes the Build in Five guardrails discussion. He is thinking about systems, not just features.
- **Amanda (offscreen):** Her tool continues to generate discussion. Used here as a case study for why non-developer-built apps need governance guardrails.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| Azmain | Surface next steps data before Monday | Richard/Team | Firm |
| BenVH | Clean duplicate product adoption rows | Team | Firm |
| Azmain | Communicate design rationale to Josh | Richard | Moderate |
| Martin | Work with Azmain on Build in Five scope | Richard | Moderate (holiday compressed) |
| BenVH | Mobile responsiveness improvements | Team | Moderate (background task) |

## Meeting Effectiveness
- **Clarity of purpose:** 8/10 -- Multiple clear objectives covered: data issues, design decisions, Build in Five scoping, app factory architecture
- **Decision quality:** 8/10 -- Prototyping step is a strong architectural decision. Action plan design rationale is sound.
- **Follow-through potential:** 7/10 -- Depends on Azmain delivering before Monday and Martin scoping before holiday
- **Stakeholder alignment:** 6/10 -- Team aligned internally, but Josh/Kathryn Palkovics pushback creates external friction
- **Time efficiency:** 7/10 -- 33 minutes covering multiple topics efficiently, though some cross-OU debrief could have been separate

## Risk Signals
- **Josh/Kathryn Palkovics design friction may escalate** -- The action plan disagreement is a symptom of a deeper tension: Josh wants Salesforce recreated, Azmain wants something better. If this is not resolved, it becomes a recurring source of friction at every feature discussion. Severity: MEDIUM
- **Salesforce data quality at source** -- Duplicate PAT rows, all statuses showing "not started," historical data inconsistencies. The data CLARA imports is only as good as Salesforce's data governance. Severity: MEDIUM
- **Monday deadline pressure** -- Azmain must surface next steps data, clean duplicates, apply Natalia's tab redesign, assign new priority customers, and address Josh/Kathryn Palkovics feedback -- all before Monday's Portfolio Review. Severity: HIGH
- **Dev/production database separation** -- Assignments made in dev do not carry to production. This creates a manual step that could be missed or inconsistent. Severity: LOW
- **Non-developer app governance gap** -- Amanda's tool is the visible example, but the pattern (people building without thinking about auth, UX, scale) will repeat across the organisation. Build in Five guardrails are the proposed solution but are still conceptual. Severity: MEDIUM

## Open Questions Raised
- Will Josh accept the action plan design as-is, or will this become a larger conflict?
- How to handle data quality issues that originated in Salesforce's own messy records?
- What is the right level of prototyping before Build in Five generates real apps?
- How to synchronise dev and production databases for customer assignments?
- Should the app factory README/guardrails be prescriptive (enforced rules) or advisory (guidelines)?

## Raw Quotes of Note
- "They're not thinking structurally. They're just like, why doesn't it look like Salesforce and why doesn't it act like Salesforce? Just make it Salesforce" -- Azmain, on Josh/Kathryn Palkovics' feedback mindset
- "People that have never built software, they don't think about a lot of things... the app she's built is very much for an expert user" -- Azmain, on Amanda's tool and the non-developer pattern
- "What if, before it even gets to the creation part of the app factory, you have a project management conversation, and then it will spin up a simple HTML" -- BenVH, proposing the prototyping step

## Narrative Notes
This session covers more ground than its 33 minutes would suggest. The Josh/Kathryn Palkovics feedback relay is the opening act, revealing the persistent tension between "make it like Salesforce" and "build something better." Azmain's refusal to auto-generate action plans from blockers is a design principle worth defending -- he is right that it would create meaningless bloatware -- but the political cost of pushing back on Josh and Kathryn Palkovics needs to be managed. The product adoption duplicate rows are a symptom of a deeper problem: Salesforce's own data governance is messy, and CLARA inherits that mess. BenVH's database access is the practical solution, but the root cause (Salesforce storing historical rows while only displaying the latest) will keep creating issues. The Build in Five discussion is where the session gets architecturally interesting: BenVH's proposal for a project management conversation before app creation, followed by static HTML prototyping, is a genuinely good idea that addresses the Amanda problem (non-developers building without governance) with a structural solution rather than just policy. The prototyping step is the kind of design thinking that separates a tool factory from a chaos factory.
