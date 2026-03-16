# Tracker Standup — Programme Alignment
**Date:** 2026-02-23
**Attendees:** Richard Dosoo, Azmain Hossain, BenVH (Speaker 1)
**Duration context:** Long (~39 minutes)
**Workstreams touched:** WS2 CLARA, WS6 Build in Five, WS1 Training

## Key Points
- Follows the Diya governance session and next-2-weeks planning. Richard, Azmain, and BenVH align on programme execution.
- Azmain burned $750 in three Cursor days. Team discusses the AI agent spend crisis -- parallels drawn to a viral video about AI agents costing more than employees.
- Richard articulates the internal evangelism strategy: Ben Brookes is shopping CLARA around to create demand (Life team, Andy Frappe, Maps team). Azmain needs to prepare slides for Christoph's leadership team demo.
- Ben Brookes is positioned as going to Life team to show CLARA architecture; the aim is to have Life's MD endorse the programme to Diya at the Wednesday governance follow-up.
- Key insight about programme politics: if the team does not control the narrative, someone like Ray or Steve will do it for them and they lose control.
- Discussion of App Factory governance: what gating criteria should determine what gets deployed. Richard and Azmain agree they need product management discipline -- not every request deserves deployment.
- Richard reveals he wasted his weekend rewriting Steve's code, only to discover Steve was simultaneously updating it with Rhett. Deep frustration with coordination failures.
- Kathryn Palkovics Lady identified as an active CLARA detractor -- flagging problems in the IRP adoption chat but never contributing solutions. Stacy ends up doing manual cleanup work that Kathryn Palkovics should be doing.
- BenVH reveals four to five apps in the deployment queue: Idris, Rhett, Stacy, Eddie. Pipeline automation is the critical enabler.
- Richard presents a six-layer platform architecture slide covering: design layer (voice input, guided workflow), data/tools layer (consulting IP, MCP servers, skills library), deployment layer (App Factory).
- Azmain describes deliberate friction in the consulting AI platform intake -- designed to filter out low-value requests by making people work through structured questions.
- Maps team dynamic shift confirmed: previously told the team to "go fuck yourselves" (paraphrased), now offering help after seeing the programme's demonstrated value.

## Decisions Made
| Decision | Type | Confidence | Owner |
|----------|------|------------|-------|
| Idris's app prioritised over others because he has advocated for the team | Political / strategic | High | Richard / BenVH |
| Rhett's work delayed to next week | Prioritisation | High | Richard |
| App Factory needs gating criteria for what gets deployed | Governance | High | Azmain / Richard |
| BenVH ROI security work is his priority this week | Prioritisation | High | BenVH |
| Slides for Christoph's Life team demo to be prepared by Azmain | Tactical | High | Azmain |

## Action Items
| Action | Owner | Deadline | Confidence | Status |
|--------|-------|----------|------------|--------|
| Prepare slides for Christoph's leadership team demo | Azmain | Tomorrow | High | Open |
| Complete ROI/security audit work | BenVH | End of week | High | Open |
| Deploy Idris's app | BenVH | This week | High | Open |
| Message Rhett about delay | Richard | Today | High | Open |
| Share spreadsheet with sprint priorities | Richard | Today | High | Open |
| Formalise monthly cross-team check-in with Asset Management | Richard | Next week | Medium | Open |

## Theme Segments
1. **AI spend crisis and tooling** (0:00-5:00) -- Token budget discussion, evangelism strategy
2. **Internal politics and narrative control** (5:00-13:00) -- Steve/Rhett coordination failure, App Factory queue, gating criteria
3. **Platform architecture review** (13:00-27:00) -- Six-layer consulting AI platform, deliberate friction design
4. **Evangelism and stakeholder management** (27:00-39:00) -- Maps team reversal, Christoph demo prep, Diya management

## Power Dynamics
- **Richard is the political strategist.** He frames the evangelism, manages the narrative, handles the "bullshit politics" directly.
- **Azmain is the product thinker.** His deliberate friction design and gating criteria thinking shows he is maturing from builder to product manager.
- **BenVH is stretched thin** -- security audit, Idris's app, four more apps waiting. He is the only person who can deploy.

## Stakeholder Signals
- **Richard Dosoo:** Exhausted but strategic. Managing multiple fronts. Deeply frustrated by Steve's wasted-weekend episode. Recognises evangelism is necessary but "icky."
- **Azmain Hossain:** Growing into the product management role. Designs deliberate friction to filter low-value requests. Recognises the need to "scream from the rooftops" about their work.
- **BenVH:** Quietly effective but under-resourced. Has four to five apps queued and a security audit. Single point of failure for infrastructure.
- **Kathryn Palkovics Lady (absent):** Identified as active CLARA detractor. Creates negative sentiment without volunteering solutions.
- **Steve (absent):** Over-engineers, does not coordinate, wastes senior people's time. Richard explicitly frustrated.

## Commitments Made
| Who | Commitment | To Whom | Confidence |
|-----|-----------|---------|------------|
| Azmain | Prepare Christoph demo slides | Richard | High |
| BenVH | Prioritise Idris's app this week | Richard | High |
| Richard | Delay Rhett's work, message him | Rhett | High |
| Richard | Share priority spreadsheet | Team | High |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of purpose | 3 | Alignment meeting but scope wandered |
| Decision quality | 4 | Good political decisions on prioritisation |
| Engagement | 4 | Strong three-way discussion |
| Follow-through setup | 3 | Spreadsheet shared, but informal tracking |
| Time efficiency | 2 | 39 minutes with significant personal tangent at end |

## Risk Signals
- **Narrative control risk.** If the team does not control the programme narrative, others (Steve, Ray) will reframe it for their own purposes.
- **BenVH as single point of failure for deployment.** Four to five apps queued, one person to deploy them all. Any illness or absence = everything stops.
- **Token budget sustainability.** $750 in three days on Cursor alone. Corporate budget doubled to $20K but Opus 4.6 is 3x more expensive. No sustainable model.
- **Coordination failures at scale.** Steve/Rhett episode is a preview of what happens without App Factory governance.

## Open Questions Raised
- What are the gating criteria for the App Factory?
- How to handle the Maps team's new willingness to engage without losing infrastructure control?
- How to demonstrate ROI for post-12-week funding?

## Raw Quotes of Note
- "If we don't do it someone, you're going to get someone like Ray or Steve coming and doing it for you, and then you've lost control of the narrative" -- Richard, on evangelism urgency
- "I wasted my weekend rewriting fucking dickhead's code" -- Richard, on Steve's coordination failure
- "She is maliciously trying to just undermine everything" -- Azmain, on Kathryn Palkovics Lady's behaviour in the IRP adoption chat

## Narrative Notes
This standup reveals the political layer of the programme that Diya's governance session did not see. The team is simultaneously building software, managing stakeholder relationships, controlling narratives, and fighting fires. Richard's weekend wasted on Steve's code is emblematic of the coordination chaos that happens without proper governance. The identification of Kathryn Palkovics Lady as an active detractor and the Maps team's about-face show how rapidly the political landscape is shifting. Azmain's growing product thinking -- deliberate friction in intake, gating criteria for the factory -- suggests he is developing the strategic muscle the programme needs, even as his tooling runs dry.
