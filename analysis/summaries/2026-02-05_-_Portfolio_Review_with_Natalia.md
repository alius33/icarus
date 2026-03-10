# Portfolio Review with Natalia
**Date:** 2026-02-05
**Attendees:** Natalia (Plant), Azmain Hossain, Sneha (mentioned)
**Duration context:** Long (~42 minutes, detailed requirements session)
**Workstreams touched:** WS2 CLARA

## Key Points
- Critical requirements redefinition session: Natalia redefining what "priority" means in CLARA -- no longer arbitrary, now means the 31 accounts on the 2026 migration timeline aligned to the scorecard target of 30 migrations
- The 17 "accelerated" accounts are a subset of the 31 needing special attention -- not a separate concept
- Ben had created an "accelerate" tab with a different concept (acceleration opportunities / analytics). Natalia says "we're not there yet" for that kind of analytics -- she wants accelerated clients, not acceleration opportunities
- Natalia wants rotating meeting focus: one week priority accounts, next week accelerated accounts -- because data does not change week on week
- Detailed tab restructuring requested: Priority tab (31 migration customers), Accelerated tab (17 accelerated customers), Non-priority reds/ambers tab (with filter buttons, not separate tabs -- "less tabs is better"), Timeline tab retained for quarterly target date views
- Key distinction identified: **status** = RAG (red/amber/green); **stage** = adoption stage (not started, in flight, complete). Multiple fields all labelled "status" in the current UI -- some are Ben's additions, not from Salesforce
- Three distinct views defined:
  1. **Portfolio Review** -- operational, for running the Monday meeting. Shows priority tabs, filters, meeting-focused data
  2. **Management Dashboard** -- for Diya/leadership. Replicates the manual PowerPoint reports: cumulative migration status by product, in-flight RAG breakdown, overall portfolio health
  3. **CSM Manager View** -- for people management. Shows data completeness by CSM, action owners, gaps. Separate menu item, not part of portfolio review
- CSM dashboard (landing page) should be personalised -- when Jeff signs in, he sees his accounts. When Natalia/Stacy/Ben/Diya sign in, they see the management dashboard
- Client health status must be manual (CSM input), not algorithmically derived from use case RAG statuses -- this is a deliberate design decision
- Natalia referenced existing PowerPoint reporting as the minimum standard for what the management dashboard must show -- cumulative charts by product (Risk Link, Risk Browser), stage breakdowns
- Historical data challenge: CLARA does not have historical records. May need to import from Sneha's Excel data used for previous monthly reports
- Scorecard view should exist alongside overall portfolio view -- both needed, same analytics style
- Diya engagement discussed: presentations must be two slides, 15 minutes maximum. No feedback mechanism -- just thumbs up/thumbs down. Multiple people confused by Diya's communication style.
- Natalia's criticism of Ben's approach: "he is just trying to have too much on one screen in one meeting" -- diplomatically delivered but pointed

## Decisions Made
- **Priority = 2026 migration customers (31 accounts) aligned to scorecard** | Type: Definition/Strategic | Confidence: High | Owner: Natalia
- **Three separate views: Portfolio Review (operational), Management Dashboard (executive), CSM Manager View (people management)** | Type: Architecture | Confidence: High | Owner: Natalia/Azmain
- **Status vs Stage naming must be corrected across the entire UI** | Type: UX/Naming | Confidence: High | Owner: Azmain
- **Client health RAG is CSM-entered, not algorithmically derived** | Type: Design principle | Confidence: High | Owner: Natalia
- **Non-priority reds and ambers in one tab with filter buttons, not separate tabs** | Type: UX | Confidence: High | Owner: Azmain
- **Management dashboard must replicate PowerPoint reporting as minimum standard** | Type: Requirements | Confidence: High | Owner: Natalia/Azmain

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Redesign portfolio review tabs per Natalia's specifications (priority, accelerated, non-priority reds/ambers, timeline) | Azmain | Before Monday meeting | Open | High |
| Create management dashboard replicating PowerPoint metrics (cumulative migration by product, in-flight RAG, portfolio health) | Azmain | Next 2 weeks | Open | Medium |
| Fix status vs stage naming across all screens | Azmain | This sprint | Open | High |
| Get Sneha's Excel data for historical migration charts | Azmain | This week | Open | Medium |
| Separate CSM Manager view from Portfolio Review as distinct menu item | Azmain | Later sprint | Open | Medium |
| Implement role-based landing page (CSMs see their accounts, seniors see management dashboard) | Azmain | Later sprint | Open | Medium |

## Theme Segments
1. **Priority Redefinition (0:00-5:00)** -- Natalia redefining "priority" from arbitrary to scorecard-aligned 31 migration accounts
2. **Tab Restructuring (5:00-12:00)** -- Detailed walkthrough of desired tab layout, filter buttons, removal of unused tabs
3. **Status vs Stage Confusion (5:00-10:00)** -- Discovery that multiple fields all named "status" cause confusion
4. **Three-View Architecture (12:00-22:00)** -- Portfolio Review vs Management Dashboard vs CSM Manager View -- the critical separation
5. **Management Dashboard Requirements (20:00-30:00)** -- PowerPoint as minimum standard, Sneha's data as source, cumulative charts
6. **Diya Communication Challenge (30:00-35:00)** -- How to present to Diya, difficulty reading her responses
7. **Ben's Sandbox and Cleanup (34:00-42:00)** -- Ben needs a separate tab for experiments, not breaking existing tabs

## Power Dynamics
- **Natalia** is the clear requirements authority in this session -- she knows exactly what she needs and articulates the distinction between operational, executive, and management views with precision. She is the most structured thinker on the programme.
- **Azmain** is in listening and absorbing mode -- asking clarifying questions, proposing implementation approaches, learning Natalia's vocabulary and priorities
- **Ben Brooks (offscreen)** -- his approach is diplomatically criticised. He adds too many features to one screen in one meeting, creating confusion. His "accelerate" concept was different from what Natalia actually needs.
- **Sneha (offscreen)** -- the hidden data backbone. Her Excel sheets are the source of truth for historical reporting and the minimum standard that the dashboard must match.
- **Diya (offscreen)** -- described as having no patience, no attention span, and giving no feedback. Multiple people cannot interpret her communication.

## Stakeholder Signals
- **Natalia Plant:** The most structured requirements thinker on the team. She can articulate the difference between operational, executive, and management views with clarity that most PMs would struggle to match. Her criticism of Ben is diplomatic but firm -- he overloads screens. She is the gatekeeper for whether the Portfolio Review meeting works.
- **Diya (SVP):** Remains an enigma. "Sometimes I'm not sure... I have people coming, what do you think she wants?" Natalia's admission that even she cannot interpret Diya's feedback is significant -- if the person closest to Diya does not know what she wants, the programme is flying blind on executive sponsorship.
- **Ben Brooks (offscreen):** His feature additions (accelerate tab, extra status fields) are creating confusion rather than value. The gap between his concept and Natalia's actual needs reveals a requirements communication problem.
- **Sneha:** The person producing the manual PowerPoint reports that leadership relies on. Her data is the bridge between old reporting and new dashboard.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| Azmain | Redesign portfolio review tabs per specifications | Natalia | Firm |
| Azmain | Create management dashboard replicating PowerPoints | Natalia | Moderate (2-week timeline) |
| Azmain | Fix status/stage naming | Natalia | Firm |
| Azmain | Get Sneha's Excel data | Self | Moderate |

## Meeting Effectiveness
- **Clarity of purpose:** 9/10 -- Natalia knows exactly what she wants and communicates it precisely
- **Decision quality:** 9/10 -- Three-view architecture is the correct structural decision. Priority redefinition aligns to measurable scorecard targets.
- **Follow-through potential:** 7/10 -- Azmain has massive workload before Monday. Portfolio review tabs are feasible; management dashboard is a multi-week effort.
- **Stakeholder alignment:** 8/10 -- Natalia and Azmain are well aligned after this session. Ben's vision may conflict.
- **Time efficiency:** 8/10 -- 42 minutes for a comprehensive requirements session is efficient. Some tangents but generally productive.

## Risk Signals
- **Ben's vision vs Natalia's requirements** -- Ben added features (accelerate analytics, extra status fields) that Natalia does not want or is not ready for. This gap could create friction when Ben returns. Severity: MEDIUM
- **Historical data gap** -- Management dashboard needs cumulative migration charts, but CLARA has no historical data. Depends on Sneha's Excel sheets, which may not be complete or standardised. Severity: MEDIUM
- **Diya communication opacity** -- If leadership cannot interpret Diya's responses, the programme cannot confirm executive sponsorship. The 2-slide, 15-minute pitch next week is high-stakes with low feedback visibility. Severity: HIGH
- **Azmain's bandwidth** -- Portfolio review redesign before Monday, management dashboard in 2 weeks, status/stage naming fixes, Sneha data import -- all while handling Josh/Catherine feedback and partner section. Severity: HIGH
- **Status/stage naming confusion** -- Multiple fields all called "status" across the UI. Some from Salesforce, some Ben's additions. Users cannot tell what anything means. Severity: MEDIUM

## Open Questions Raised
- How to handle historical data in the dashboard -- CLARA does not have historical records, may need manual import from previous monthly PowerPoint reports
- What does "migration complete" mean precisely -- when Risk Link/Risk Browser is switched off?
- Should the management dashboard be a separate URL or a role-gated view within the same app?
- How to reconcile Ben's acceleration analytics concept with Natalia's simpler accelerated clients list?
- When will Gainsight be ready for IRP-specific data? If yes, does the management dashboard become redundant?

## Raw Quotes of Note
- "Sometimes, I'm not sure you know... I have people coming, what do you think she wants?" -- Natalia, on the difficulty of interpreting Diya's communications
- "Ben is just trying to have too much on one screen in one meeting" -- Natalia, diplomatically but firmly criticising the overloaded UI approach

## Narrative Notes
This is the most important requirements session of the week. Natalia redefines "priority" from a vague label to a measurable concept tied to the 2026 scorecard target of 30 migrations. This single decision -- priority means the 31 migration customers -- gives CLARA a concrete, defensible purpose that can be communicated to sceptics (including the Gainsight team). The three-view architecture (Portfolio Review for operations, Management Dashboard for executives, CSM Manager View for people management) is the structural insight that separates this from a generic dashboard project. It reflects Natalia's understanding that different audiences need different things, and that cramming everything into one screen (as Ben has been doing) creates confusion rather than utility. The Diya communication challenge is quietly alarming -- if the programme's executive sponsor is fundamentally unreadable, then the 2-slide pitch next week is not just a presentation but a coin flip. Natalia's role as the requirements authority is now firmly established: she speaks for what the business needs, even when that contradicts what the builder (Ben) has created.
