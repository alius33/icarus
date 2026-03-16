# Monday Tracker Standup
**Date:** 2026-02-09
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brookes, BenVH (Speaker 1), Martin Davies
**Duration context:** Medium (~30 minutes)
**Workstreams touched:** WS2 CLARA, WS6 Build in Five

## Key Points
- Richard confirms Claude Code access secured via AWS pilot. They will connect Claude Code to the AWS environment rather than using the desktop interface. Both Richard and Azmain running out of personal Claude subscriptions (Azmain's expires ~13 Feb).
- Action plans have been pushed to prod successfully after BenVH resolved the EC2 instance issue. A front-end filter was blocking action plans from displaying — one of the PRs addresses this.
- Azmain has two PRs with merge conflicts: PR #38 (removes demo mode functionality + fixes) supersedes PR #33. BenVH resolves one conflict; Claude resolves the other by creating a new PR.
- BenVH announces a new staging environment, giving three environments total (dev, staging, prod). Staging is a clone of the production database, enabling proper QA before promoting to prod.
- Ben Brookes pushes for CSM usability features as the top priority — specifically transcript upload to auto-populate customer updates. Argues this will drive adoption faster than adding partner management or solution architecture tracking.
- Richard wants to prioritise the partner management piece (for Alexandra and Liz McLagan). Ben disagrees on sequencing — partners can tolerate a spreadsheet for two more weeks, but losing CSM engagement momentum is costly given the 40-migration target this year.
- Natalia has been briefed on the portfolio review screen layout: start with 2026 scorecard migration priority clients (31), then non-priority reds/ambers, then accelerated adoption. She also wants a management dashboard that could replace the PowerPoint deck Diya currently receives.
- Ben Brookes envisions embedding LLM capabilities (via AWS Bedrock) into CLARA: (1) transcript triage to pre-populate fields with human-in-the-loop before save, (2) executive chat window to ask questions about implementations.
- Richard reports the asset management team (Amanda Fleming) has independently built a similar but more advanced app with LLM integration and NPS categorization. Natalia advised against replicating what Amanda has done to avoid antagonizing the Gainsight team.
- Martin Davies leaves Wednesday for two weeks. Richard wants to walk through Martin's Build in Five plan before he goes.
- Richard raises whether they should prepare demos for the Exceedance event, noting Martin's work could overlay nicely.

## Decisions Made
| Decision | Type | Made By | Confidence |
|----------|------|---------|------------|
| CSM usability (transcript upload, ease of data entry) prioritised over partner management features | Priority | Ben Brookes, agreed by team | High |
| PR #33 cancelled, PR #38 is the canonical fix | Technical | Azmain/BenVH | High |
| Three-environment workflow adopted (dev -> staging -> prod) | Infrastructure | BenVH | High |
| Defer partner management to after CSM adoption features | Sequencing | Ben Brookes | Medium — Richard initially disagreed |

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Get Claude Code API keys and environment access set up | Richard | 2026-02-09 | Open | High |
| Get PRs merged and ready for Josh/Kathryn Palkovics review this afternoon | Azmain | 2026-02-09 | Open | High |
| Walk through Martin's Build in Five plan before Wednesday departure | Richard/Martin | 2026-02-11 | Open | Medium |
| Schedule conversation about Exceedance demos | Ben Brookes/Richard | TBD | Open | Low |
| Compare Amanda's PRD against CLARA features | Richard | TBD | Open | Low |

## Theme Segments
| Time Range | Theme | Key Speakers |
|------------|-------|--------------|
| 0:00-2:30 | Claude Code access update and PR status | Richard, Azmain |
| 2:30-8:30 | PR merge conflicts, three-environment setup, data fixes for Monday | Azmain, BenVH, Richard |
| 8:30-17:00 | Feature prioritisation debate — CSM usability vs partner management | Ben Brookes, Richard, Azmain |
| 17:00-22:30 | Claude Code API keys, LLM integration vision, Martin's Build in Five | Richard, Azmain, Ben |
| 22:30-30:00 | BenVH PR resolution, staging environment details, closing actions | BenVH, Azmain |

## Power Dynamics
- **Ben Brookes exerts soft authority on sequencing.** He overrides Richard's preference for partner management features with a framing that is hard to argue against: migrations matter more than spreadsheets. Richard yields without resistance.
- **BenVH is the quiet infrastructure authority.** He announces three-environment setup without seeking permission — it is already done. Nobody questions it because nobody else can do what he does.
- **Martin Davies is peripheral.** He barely speaks. His two-week absence is discussed as a scheduling constraint, not as a loss of capability. His work on Build in Five has not yet earned him standing in the core team dynamic.

## Stakeholder Signals
- **Ben Brookes:** Laser-focused on CSM usability as the adoption lever. Impatient with feature requests that do not directly drive migration tracking engagement. His instinct is always speed and simplicity. Shows excitement about LLM integration — sees it as the way to make CLARA irreplaceable.
- **Richard Dosoo:** Trying to balance multiple stakeholder demands (partners, Natalia's dashboard, Ben's usability vision) while keeping the team focused. Continues to manage the Cursor compliance issue pragmatically — still using personal subscription until it expires.
- **Martin Davies:** About to go on two weeks' leave, creating a gap in Build in Five progress.
- **Natalia (mentioned):** Shaping the portfolio review to be structured and scorecard-aligned, resisting unnecessary complexity. Wants a management dashboard to replace Diya's PowerPoint.
- **Azmain:** Working productively. Confident about the state of the build. Has two PRs ready and is already thinking about next features. The Claude-assisted PR resolution workflow is becoming normalised.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| Richard | Get Claude Code API keys set up today | Team | Firm |
| Azmain | Get PRs merged for Josh/Kathryn Palkovics review | Richard | Firm |
| Ben Brookes | Will schedule half hour to discuss Exceedance demos | Richard/Martin | Soft |
| Richard | Walk through Martin's plan before Wednesday | Martin | Firm |

## Meeting Effectiveness
| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Clarity of outcomes | 4 | Clear priorities set, actions assigned |
| Decision quality | 4 | Ben's sequencing logic was sound and accepted |
| Engagement balance | 3 | Martin barely spoke. BenVH joined late. |
| Time efficiency | 4 | 30 minutes, covered ground efficiently |
| Follow-through potential | 4 | Actions are concrete and near-term |

## Risk Signals
- **Cursor compliance:** Richard and Azmain still running personal subscriptions that are about to expire. Claude Code access via AWS is the replacement but is not yet set up. A gap in tooling could slow development.
- **Martin's two-week leave:** Build in Five loses momentum at a critical scoping stage. The March 21 Exceedance demo target is now under pressure.
- **Scope creep from LLM vision:** Ben's vision for transcript triage and executive Q&A via Claude is exciting but adds significant complexity. Without a formal prioritisation mechanism, these ideas compete with data quality fixes.

## Open Questions Raised
- Should they prepare IRP demos for the Exceedance event this year?
- Can the Amanda Fleming PRD be used to accelerate CLARA features without stepping on Gainsight's toes?
- When will Claude Code API keys be available for embedding LLM in the app?

## Raw Quotes of Note
- "If we hammer usability for the CSMs, implementations, SAT teams and then execs as well for visibility, so that we're really crunching down on everybody to use this thing because the visibility is forcing it, then I would go to partners after that." -- Ben Brookes, on prioritisation

## Narrative Notes
This standup is energised and productive — a marked contrast to the fire-fighting mode of previous weeks. The RBAC crisis is resolved, the data loss incident is behind them, and the team is looking forward. Ben Brookes's prioritisation of CSM usability over partner management is the defining moment: it signals that the team is now optimising for adoption velocity rather than feature breadth. The Claude Code access is a genuine milestone — it transitions the team from personal subscriptions to institutional tooling, though the actual onboarding has not happened yet. The gap between vision (LLM-powered executive Q&A) and reality (action plans not displaying correctly) is wide, but the team is not deluded about it — they are just dreaming while they fix bugs.
