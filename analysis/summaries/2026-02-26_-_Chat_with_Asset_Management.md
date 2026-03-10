# Chat with Asset Management -- Amanda's Platform Demo and Cross-Team Collaboration
**Date:** 2026-02-26
**Attendees:** Azmain Hossain, BenVH (Ben Van Houten), Amanda (Speaker 2), Ben Reynolds (Speaker 3), Richard Dosoo
**Duration context:** Long (~41 minutes)
**Workstreams touched:** WS2 CLARA, WS6 Build in Five, Infrastructure/Governance

## Key Points
- Cross-team knowledge sharing session with Asset Management. Amanda demos her comprehensive customer success platform -- built solo -- with AI-generated PDF reports, renewal tracking, prospecting pipeline, cross-sell/upsell heat maps, task management with AI processing, and engagement tracking.
- Amanda's app generates detailed AI-powered PDF reports using the OpenAI API. Per-client renewal analysis includes non-repetitive commentary (she spent significant time ensuring the AI does not repeat the same observations across clients), risk metrics (custom-built, replacing NPS which she considers outdated), actionable next steps, and proposal tracking. Each client gets its own page with meeting notes analysis and trend data.
- Amanda built custom risk metrics to replace NPS, which she considers shallow and outdated. These get updated quarterly, and she is building trend tracking so the team can see if client health changed for specific reasons.
- The app includes features CLARA is still building toward: AI task generation from meeting notes (the AI reads notes and creates tasks with assignees automatically), engagement tracking with per-client meeting frequency expectations based on contract value, project management timeline with PDF output, and per-trial weekly reporting.
- Azmain is simultaneously inspired and frustrated. He sees Amanda's outputs as aspirational benchmarks for IRP CSMs but recognises the fundamental difference: Amanda is both builder and user. She enters her own data diligently because she designed the system for herself. IRP CSMs are resistant to data entry and afraid to click buttons.
- Azmain's leverage strategy: take Amanda's PDF reports to seniors (Ben Brooks, Natalia) and frame it as "look what Asset Management CSMs produce -- don't you want reports like this?" He deliberately plans not to reveal that Amanda is the sole user, instead framing it as a team output to create competitive motivation.
- Azmain demonstrates CLARA to Amanda: the reports functionality (modelled after Salesforce report builder), the executive summary vs. updates confusion (CSMs keep updating the executive summary instead of using the updates section), and the tab-based layout designed to address scrolling complaints.
- BenVH raises the AI governance process requirement: any app making calls to OpenAI/Claude API needs to go through an intake form, potential cyber security review (Frank Cifuentes), and risk governance review (Melinda Tigerino). He warns the process is opaque -- he sent a form and heard nothing for two weeks until he directly messaged Melinda.
- BenVH confirms the AI governance process still applies even for self-hosted Bedrock models. The review covers who consumes outputs, whether users know outputs are AI-generated, and quality validation.
- Richard's manager and their manager are encouraging formalisation of the cross-team collaboration. Richard will set up monthly check-in cadence.
- Token budget discussion: Azmain ran out of Cursor mid-January, got a $200 Claude Max subscription, then got access to Windsurf (Moody's approved). BenVH notes they increased the token budget from $10K to $20K but Opus 4.6 is three times more expensive and more people are using Cursor (banking had a hackathon). BenVH has Claude Code access and calls it "unbelievably expensive."
- BenVH reveals Moody's has a strategic partnership with Anthropic -- they were involved in Anthropic's financial expert stuff. S&P and LSEG have already published MCP tools on Anthropic's marketplace. Moody's should be doing the same.
- BenVH mentions cursor rules have been created as guardrails for the team. He suggests looking at agent skills as a more portable alternative that works across Cursor, Windsurf, and Claude Code.
- Ben Reynolds asks detailed technical questions about how AI task generation works -- showing genuine curiosity about the architecture, not just the outputs.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Amanda to provide PRD of account planning features for CLARA integration after holiday | Product | High | Amanda / Richard |
| Monthly cross-team check-in formalised between Insurance and Asset Management | Process | High | Richard |
| AI governance intake form to be submitted for CLARA's LLM integration | Compliance | High | Azmain / Richard |
| Cursor rules to be shared; agent skills to be evaluated as portable alternative | Technical | Medium | BenVH / Richard |
| Use Amanda's PDF outputs as leverage to motivate IRP CSMs | Political | High | Azmain |

## Action Items
| Action | Owner | Deadline | Confidence | Status |
|--------|-------|----------|------------|--------|
| Send AI governance intake form link and contact details to Asset Management team | BenVH | Today | High | Open |
| Submit AI governance intake form for CLARA LLM integration | Azmain / Richard | ASAP | High | Open |
| Set up monthly cross-team check-in with Asset Management | Richard | Next week | High | Open |
| Provide account planning PRD after holiday | Amanda | After holiday | Medium | Open |
| Share cursor rules file with Asset Management team | Richard | Next check-in | Medium | Open |
| Obtain PDF report samples from Amanda for CSM motivation | Azmain | This week | High | Open |
| Get Claude Code access via Richard (higher permissions needed) | Azmain | This week | Medium | Open |

## Theme Segments
1. **Token budget and tooling comparison** (0:00-7:00) -- Cursor costs, Claude Max, Windsurf, Bedrock API keys, Moody's-Anthropic partnership reveal, MCP marketplace
2. **Amanda's platform demo** (8:00-20:00) -- Renewal tracking, AI PDF reports, cross-sell heat maps, prospecting pipeline, risk metrics, engagement tracking, task generation from meeting notes
3. **CLARA comparison and CSM adoption challenges** (20:00-28:00) -- Executive summary misuse, scrolling complaints, Salesforce imitation, data entry hand-holding
4. **AI governance process** (28:00-37:00) -- Intake form, Melinda Tigerino, Frank Cifuentes, Bedrock self-hosting still requires governance, opaque process
5. **Cross-team formalisation and next steps** (37:00-41:00) -- Management encouragement, monthly cadence, cursor rules vs skills, Amanda's PRD commitment

## Power Dynamics
- **Amanda is the aspirational benchmark.** Her solo-built platform demonstrates what is possible when the builder is also the user. She is both proof of concept and an implicit rebuke to IRP CSM resistance.
- **Azmain is strategically opportunistic.** He immediately sees how to weaponise Amanda's outputs for political leverage with IRP seniors and CSMs. His plan to misattribute the outputs to "their CSMs" (rather than Amanda alone) is deliberately deceptive but tactically effective.
- **BenVH is the governance sage.** He has been through the AI governance process and provides practical advice: start early, chase directly, do not wait for the form to be processed.
- **Ben Reynolds is the engaged newcomer.** His technical questions about AI task generation suggest he is thinking about how to apply similar patterns in his own work.
- **Richard arrives late but immediately steers** toward strategic next steps: PRD for account planning, formalised collaboration, and cross-team governance alignment.

## Stakeholder Signals
- **Amanda:** Impressively self-sufficient builder. Generated a comprehensive platform solo using OpenAI API. Her custom risk metrics (replacing NPS), non-repetitive AI commentary, and engagement tracking based on contract value show sophisticated product thinking. She is her own best user, which is both her strength and the reason her model does not translate directly to IRP.
- **Azmain Hossain:** Strategic opportunist. Plans to use Amanda's outputs as leverage to motivate CSMs. Frustrated by the gap between what Amanda achieves solo and what 50 IRP CSMs cannot manage collectively. His description of hand-holding CSMs through basic data entry reveals deep frustration with adoption dynamics.
- **BenVH (Ben Van Houten):** Reveals the Moody's-Anthropic strategic partnership -- a significant intelligence point. Practical about AI governance. Has Claude Code access and confirms it is expensive. Advocates for agent skills over cursor rules for portability.
- **Ben Reynolds:** Technically curious. Asks detailed questions about AI task generation architecture. His interest signals potential as an early adopter of similar patterns in Asset Management.
- **Richard Dosoo:** Arrives late but focuses on strategic outcomes: PRD commitment, formalised collaboration, management backing for cross-team work.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| BenVH | Send AI governance intake form and contacts | Azmain / Ben Reynolds | High |
| Amanda | Provide account planning PRD after holiday | Richard | Medium |
| Richard | Set up monthly cross-team check-in | Both teams | High |
| Richard | Share cursor rules with Asset Management | BenVH / Ben Reynolds | Medium |
| Azmain | Use Amanda's outputs to motivate CSMs | Self (strategic) | High |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of purpose | 3 | Started as knowledge sharing, evolved into multiple threads |
| Decision quality | 4 | Good decisions on governance process, cross-team cadence, and PRD commitment |
| Engagement | 5 | All participants contributing actively; Amanda's demo highly engaging |
| Follow-through setup | 3 | Actions identified but some timelines loose (especially Amanda's PRD post-holiday) |
| Time efficiency | 3 | 41 minutes with some tangential discussion; Richard's late arrival caused re-cap |

## Risk Signals
- **AI governance process is a bottleneck.** BenVH's warning that the intake form went unanswered for two weeks is consistent with what he reported in other meetings. CLARA's LLM integration cannot proceed without this clearance, and the process is opaque.
- **Amanda's outputs may create unrealistic expectations.** If Azmain shows Amanda's PDF reports to IRP seniors as "what is possible," the expectation gap between a solo builder-user and 50 reluctant CSMs could backfire. The quality depends on Amanda's personal data discipline, which is not replicable across IRP.
- **Moody's-Anthropic partnership is underexploited.** BenVH reveals this exists but the insurance programme team was unaware. S&P and LSEG are already on the Anthropic marketplace. If Moody's does not act, competitors get first-mover advantage.
- **Token budget pressure is escalating.** Banking's hackathon consumed significant budget. Opus 4.6 is three times more expensive. Claude Code is "unbelievably expensive." The $10K to $20K increase may not be sufficient with increasing adoption.
- **CSM adoption gap is widening.** Amanda demonstrates what engaged users can achieve. IRP CSMs still need hand-holding for basic data entry. The gap is not technical -- it is cultural and behavioural.

## Open Questions Raised
- How long will the AI governance process take for CLARA's LLM integration?
- Will the Moody's-Anthropic strategic partnership accelerate access to Claude tools company-wide?
- Can agent skills replace cursor rules as a more portable guardrail framework?
- How should the team handle the discrepancy between Asset Management's data discipline and IRP CSMs' resistance to data entry?
- What does the Moody's MCP marketplace strategy look like, given S&P and LSEG are already publishing tools?

## Raw Quotes of Note
- "It's freaking 2001 and somebody's teaching them data entry and literally be like, click here" -- Azmain, on the state of CSM adoption in IRP
- "I'm not gonna tell them it's just you doing it. I'll be like, look at their CSMs. They're so diligent" -- Azmain, on his plan to use Amanda's outputs as leverage
- "We have a strategic partnership with Anthropic, right? We've given them a bunch of stuff, and they're supposed to be giving us a bunch of stuff" -- BenVH, revealing the Moody's-Anthropic relationship
- "I don't really agree with NPS metrics. I think they're a bit outdated and a bit shallow" -- Amanda, on why she built custom risk metrics

## Narrative Notes
This meeting is a study in contrasts. Amanda has built, solo, what the IRP programme is struggling to achieve with a team of fifty. Her platform generates AI-powered PDF reports, tracks renewals with custom risk metrics, creates tasks from meeting notes, and monitors engagement against contract-value-based expectations. She is her own best user -- entering data diligently because she designed the system for her own needs. Meanwhile, Azmain describes hand-holding IRP CSMs through basic data entry like it is 2001. The gap is not technical; it is cultural and structural. Amanda's solution works because she is both builder and user. CLARA's challenge is that builders and users are different populations with different motivations. Azmain's plan to weaponise Amanda's outputs is tactically clever but risks creating expectations that cannot be met without fundamental behavioural change from CSMs. The BenVH intelligence drop about the Moody's-Anthropic partnership is significant -- it means enterprise access to Claude tools should be coming, which could moot Azmain's plan to build a Claude wrapper. The AI governance process remains the gatekeeper for any LLM integration, and BenVH's practical advice (start early, chase directly) is the most actionable takeaway for the programme.
