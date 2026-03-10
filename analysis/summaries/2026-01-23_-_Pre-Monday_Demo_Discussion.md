# Pre-Monday Demo Discussion — Full Group Run-Through
**Date:** 2026-01-23
**Attendees:** Richard Dosoo, Azmain Hossain, Idris (Banking CS), Bernard (Life team), Alexandra (Life team), George Dyke, Martin Davies
**Duration context:** Long (~60 minutes)
**Workstreams touched:** WS2 CLARA, WS3 CS Agent, WS5 Sales Recon Convergence, WS6 Build in Five

## Key Points
- Pre-Monday meeting run-through with cross-functional team including banking (Idris), life (Bernard, Alexandra), and insurance (Richard, George, Azmain)
- Idris calling from an airport en route to London — changed travel plans due to major storm, taking red eye from JFK, will be in London office Monday morning by 9am
- Richard outlined three demos for Monday: (1) CLARA adoption tracker, (2) Bernard's Copilot Light sentiment dashboard for Sompo, (3) Customer Insights RMB (ran out of time, not shown)
- Azmain delivered a comprehensive live walkthrough of CLARA to Idris, explaining the IRP migration context, the data fragmentation problem, and the centralised data capture vision
- Idris asked the critical scale question: what percentage of the insurance business does IRP represent? Bernard answered approximately three-quarters of the business unit revenue. Richard estimated 300 customers total, with targets of 40 migrations per year
- Idris drew parallels to banking's Credit Lens 360 Hub platform and suggested CLARA could be "the central source of data that feeds out into other systems"
- Idris probed the workflow: how do different stakeholders (CSMs, advisory, implementation) interact with the tool? Azmain explained the SSO-based personalised views (my customers, my team, all accounts)
- Idris raised the strategic question about non-IRP workflows within insurance — George confirmed they are in early exploration stages, particularly on the asset management side with products like Orbis, GRID, and Price Catalyst
- Richard framed the Monday ask: CLARA should ideally be absorbed into Sales Recon, but they have not received approval yet — Monday's meeting with Colin and Diya should greenlight this, or alternatively, signal that CLARA will remain standalone with defined interfaces
- Bernard demonstrated his Copilot Light sentiment dashboard: extracted Salesforce meeting data, case feeds, NPS scores, and Mixpanel usage data into a SharePoint folder, pointed a Copilot Light agent at it, and generated an HTML health assessment dashboard
- Idris was very impressed by Bernard's demo but raised hallucination concerns — their banking team found Copilot Light would change numbers when challenged
- Alexandra raised concern about hallucination risk if presenting to executives
- Bernard acknowledged hallucination risk increases with prompt complexity — recommended focused, specific agents rather than one complex prompt
- Richard flagged the data pipeline bottleneck: Natalia Plant directed the team to target Gainsight rather than Salesforce APIs, but Gainsight implementation would not be complete until end of March — creating a holding pattern
- The Intelligence Anywhere feature from Sales Recon's Q1 roadmap could solve the data pipeline problem by surfacing Salesforce, Gainsight, and Mixpanel data through APIs

**Post-meeting (Richard and Azmain only):**
- Azmain's Cursor was confirmed fully blocked — "absolute worst time"
- Richard decided to purchase Claude Max Pro for Azmain ($200/month) using a personal email (email@azmain.co.uk) as a workaround — the formal Snow ticket process was too slow
- Extended technical session setting up Claude Code: connecting to GitHub, understanding the difference between chat (thinking/planning) and code (execution) modes
- Martin Davies confirmed he still had Cursor credits (335 of 500, resetting February 1)
- Authentication issues: Azmain's work browser had his personal Claude account cached, causing the new account authorization to fail repeatedly
- Richard offered to have Martin run prompts if needed as a backup
- Richard noted the ability to run multiple Claude Code instances in parallel (planning, executing, QA) — sharing knowledge about advanced usage

## Decisions Made
- **Position CLARA as central data source for insurance CS** (type: strategic, confidence: high) — Idris and George both endorsed the concept of CLARA as the single source feeding into other systems
- **Monday's ask: Sales Recon absorption of CLARA or defined standalone interfaces** (type: governance, confidence: high) — Richard framed this as a binary outcome with clear implications for resourcing
- **Purchase Claude Max Pro for Azmain as emergency workaround** (type: resource, confidence: high) — Richard decided unilaterally to unblock development before Monday
- **Bernard's sentiment dashboard to be included in Monday demo** (type: presentation, confidence: high) — demonstrates what can be built with existing data and tools
- **Third demo (Customer Insights RMB) deferred to in-person Monday morning** (type: scheduling, confidence: high) — ran out of time in the call

## Action Items
| Action | Owner | Deadline | Confidence |
|--------|-------|----------|------------|
| Polish CLARA demo for Monday (data input hub + portfolio review) | Azmain Hossain | 2026-01-27 AM | High |
| Set up time Monday morning to show Customer Insights RMB to Idris | Richard Dosoo | 2026-01-27 AM | High |
| Bernard to validate sentiment dashboard slides with Alexandra | Bernard | 2026-01-24 | Medium |
| Resolve Claude Code GitHub authentication for Azmain | Azmain Hossain | 2026-01-23 | High |
| Martin to be available as backup Cursor user | Martin Davies | 2026-01-24 onwards | Medium |
| Richard to raise Azure access ticket for Azmain | Richard Dosoo | 2026-01-24 | Medium |

## Theme Segments
| Timestamp Range | Theme | Speakers | Tone |
|----------------|-------|----------|------|
| 0:00-2:00 | Idris travel logistics, weather, team introductions | Richard, Idris, Azmain | Casual, warm |
| 2:00-7:00 | Monday meeting agenda overview, three demo structure | Richard | Structured, comprehensive |
| 7:00-12:00 | CLARA live walkthrough for Idris: IRP context, data problem, centralised vision | Azmain | Demo, enthusiastic |
| 12:00-17:00 | Idris asks about workflow, scale, and non-IRP scope; George on asset management | Idris, George, Azmain | Strategic, probing |
| 17:00-23:00 | CLARA as central data source discussion, Sales Recon convergence ask | Idris, Richard, Azmain | Strategic, consequential |
| 23:00-33:00 | Bernard's Copilot Light sentiment dashboard demo | Bernard | Demo, impressive |
| 33:00-37:00 | Hallucination concerns and data pipeline bottleneck | Idris, Alexandra, Bernard, Richard | Candid, concerned |
| 37:00-44:00 | Wrap with group; transition to Richard-Azmain private session | Richard, Azmain | Transition |
| 44:00-55:00 | Claude Code setup, Claude Max Pro purchase, GitHub authentication | Richard, Azmain, Martin | Technical, troubleshooting |
| 55:00-60:00 | Authentication debugging, Martin's Cursor credits, close | Richard, Azmain, Martin | Frustrated, persevering |

## Power Dynamics
- **Idris** asked the most strategically important questions: scale of IRP to the insurance business, non-IRP workflow coverage, and whether this was meant to be a data hub or an integrated enterprise tool. His banking CS perspective provided valuable cross-pollination.
- **Richard Dosoo** orchestrated the entire session, managing the agenda across a large group and pivoting smoothly when time constraints required deferring the third demo. His post-meeting action to purchase a licence for Azmain showed decisive resource allocation.
- **Azmain Hossain** delivered the CLARA demo effectively to a new audience (Idris had never seen it), translating technical implementation into business value. His characterisation of CLARA's origin as "I was lazy — they wanted a 60-page slide deck" landed well.
- **Bernard** demonstrated genuine technical capability with the Copilot Light sentiment dashboard — a working tool built with no engineering support that Idris called "very impressive."
- **George Dyke** provided the business context that IRP represents approximately three-quarters of the insurance business unit revenue, making the tracking system strategically critical.

## Stakeholder Signals
- **Idris** — Immediately saw CLARA's potential as an enterprise data hub, drawing parallels to banking's Credit Lens 360 Hub. His hallucination concern about Copilot Light was informed by direct experience — banking had moved to Copilot Studio with hard-coded rules after finding inconsistencies. His enthusiasm for the work ("very impressive, happy to see other groups doing this stuff") was genuine and positioned him as a cross-divisional ally.
- **Bernard** — His Copilot Light demo was the most tangible proof of AI capability in the programme. His recommendation for focused, specific agents rather than complex prompts showed practical LLM experience. Alexandra's concern about hallucination when presenting to executives was a valid governance flag.
- **George Dyke** — His confirmation that non-IRP insurance workflows are still in "exploring rather than anything established" stages was honest and set appropriate expectations. His brief contribution to the revenue context was the most impactful statement in the call for positioning.
- **Martin Davies** — His Cursor credits (335/500, resetting Feb 1) made him a potential backup developer. His offer to let Azmain log in as him showed team solidarity, though Richard correctly identified the authentication barrier.
- **Richard Dosoo** — His decision to purchase a $200/month licence without formal approval showed both leadership and the desperation of the tooling situation. His knowledge of Claude Code's advanced features (parallel instances, chat vs code modes) positioned him as the team's AI tools expert.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Idris | In London office Monday morning by 9am | Richard | High |
| Richard | Show Customer Insights RMB Monday morning | Idris | High |
| Richard | Purchase Claude Max Pro for Azmain | Azmain | High |
| Bernard | Validate slides with Alexandra | Richard | Medium |
| Martin | Available as backup Cursor user | Azmain/Richard | Medium |

## Meeting Effectiveness
- **Clarity of outcomes:** 7/10 — Monday demo plan clarified, but third demo deferred and tooling crisis consumed the back half
- **Decision quality:** 7/10 — Good strategic framing of the Monday ask; Claude Max Pro purchase was pragmatic
- **Engagement balance:** 8/10 — Seven participants across three time zones all contributed; Idris was particularly engaged despite being at an airport
- **Time efficiency:** 6/10 — Ran over time, could not show third demo, post-meeting tech setup consumed significant time

## Risk Signals
| Risk | Severity | Signal |
|------|----------|--------|
| Hallucination risk in Bernard's sentiment dashboard | HIGH | Idris flagged from direct banking experience that Copilot Light changes numbers when challenged. If this happens during the Monday demo to executives, credibility of all AI work would be damaged. |
| Data pipeline blocked until Gainsight (end of March) | HIGH | Natalia directed team to target Gainsight, not Salesforce APIs. But Gainsight implementation is months away, creating a data access vacuum. Intelligence Anywhere from Sales Recon could solve this but is Q1 at best. |
| Monday meeting overloaded with content | MEDIUM | Three demos plus executive context plus requirements discussion. Third demo already deferred. Risk of running over and losing executive attention. |
| Claude Code authentication not resolved | HIGH | Despite purchasing Max Pro licence, GitHub connector repeatedly failed due to cached personal account sessions. If not resolved by Monday, Azmain still cannot use AI development tools effectively. |
| Informal licence procurement creating audit trail gap | MEDIUM | Personal email used for Claude account, personal credit card for payment, no formal procurement record. If audited, this would be difficult to justify. |

## Open Questions Raised
- How will non-IRP workflows (Orbis, GRID, Price Catalyst) eventually be tracked — through CLARA expansion or a separate system?
- Can Intelligence Anywhere deliver the data pipeline that would replace manual Salesforce extracts?
- How should the hallucination risk in Copilot Light-generated dashboards be mitigated for executive presentations?
- What is the banking team's experience with Credit Lens 360 Hub that could inform CLARA's development?
- When will formal AI tool licences be provisioned through the Snow ticket process?

## Raw Quotes of Note
- "This is the major focus of the business unit... it's about three quarter of the business unit revenue" — Bernard/Alexandra, on IRP's significance to insurance
- "Very impressive. Happy to see other groups doing this stuff" — Idris, on CLARA and Bernard's dashboard
- "I know the robots will eventually take over and kill us all, but for a while, could they just be good?" — Azmain Hossain, on Claude Code authentication issues
- "If you're going to stand up in front of Mike and Colin and say it's there, that puts the target on your back to make sure it gets delivered" — Richard Dosoo (from earlier call, repeated in context)

## Narrative Notes
This was the final substantive preparation session before the Monday executive meeting, and it achieved its primary goal: Idris — the most important new stakeholder to see CLARA — understood the system, saw its potential, and endorsed the strategic direction. His comparison to banking's Credit Lens 360 Hub was the kind of cross-divisional validation that would strengthen the Monday pitch. Bernard's Copilot Light demo added a second proof point: the insurance team could build useful AI tools independently, but they needed the data pipeline from Sales Recon's Intelligence Anywhere to make them scalable. The revenue context (IRP representing approximately three-quarters of insurance business unit revenue) reframed CLARA from a project management tool to a business-critical platform tracking the majority of the division's income stream.

The post-meeting technical session, however, revealed the programme's fragile operational reality. The fact that the primary developer needed the programme manager to purchase a $200 personal licence, create an account with a personal email address, and then spend 20 minutes debugging authentication issues — all on the Thursday before a high-visibility Monday demo — was a governance failure that had been accumulating throughout the week. The formal procurement process (Snow ticket) was too slow, the informal process (personal credit cards and shared accounts) was too risky, and the result was significant developer time wasted on tooling logistics rather than preparing the actual demo. Martin Davies's Cursor credits represented a lifeline, but one with an expiration date (February 1 reset). The programme was entering its most important meeting with its development infrastructure held together by personal subscriptions and workarounds.
