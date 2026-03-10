# CSM Dashboard Permissions and Testing Review
**Date:** 2026-02-03
**Attendees:** Richard Dosoo, BenVH (Ben Van Houten), Azmain Hossain, Philip Garner, Sneha (testing)
**Duration context:** Long (~38 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- Philip asked about client-facing transparency dashboards -- can they share a live view with customers showing defect/feature tracking progress linked to JIRA?
- Richard explained the product alignment challenge: Alicia (PM) supports requirements traceability from workflow to use case to product feature, linked to JIRA tickets -- but this is future work
- RBAC verification continued: BenVH removed himself from admin to simulate CSM experience, then restored permissions and merged dev to production
- **RBAC confirmed working in production:** CSMs can save edits on assigned accounts, correctly blocked on unassigned accounts
- Sneha tested successfully -- saves working on her assigned accounts, permissions blocking correctly on others
- Error UX flagged: generic 403 instead of a helpful popup when CSMs attempt unauthorised edits -- on the backlog
- Dashboard timestamp issue discovered: "last updated" only reflects account-level edits, not blocker or action plan updates
- CSMs requested better navigation between accounts -- refreshing sends them back to the dashboard every time
- **Richard was not invited to CSM workshops organised by Liz** -- expressed frustration but chose to disengage ("I don't give a shit") and told Azmain to focus on the build
- Richard was candid about the Josh/Ben tensions and the dynamics of people without work creating noise

## Decisions Made
- **RBAC confirmed working -- CSMs edit only their assigned accounts** | Type: Technical verification | Confidence: High | Owner: Team
- **Need user-friendly popups for permission errors** | Type: UX | Confidence: High | Owner: Azmain
- **Richard deliberately staying out of workshops he wasn't invited to** | Type: Political/Strategic | Confidence: High | Owner: Richard
- **CSM workshops to be action-oriented, not introductory** | Type: Process | Confidence: Medium | Owner: George (implied)

## Action Items
| Action | Owner | Deadline | Status | Confidence |
|--------|-------|----------|--------|------------|
| Add friendly popup for permission errors instead of generic 403 | Azmain | Next sprint | Open | High |
| Fix dashboard timestamps to include blocker/action plan updates | Azmain | Before Monday review | Open | High |
| Deploy production fixes for RBAC | BenVH | 2026-02-03 | Complete | High |
| Get another CSM to test beyond Philip | Azmain | Today | Open | Medium |
| Keep Natalia and Diana informed about competing demands on Azmain's time | Azmain | Ongoing | Open | Medium |

## Theme Segments
1. **Philip's Client-Facing Dashboard Request (0:00-3:30)** -- Forward-thinking CSM feedback on transparency
2. **RBAC Testing and Verification (3:30-25:00)** -- Testing with multiple users, confirming production fix
3. **Sneha Testing (18:00-29:00)** -- Independent CSM validation of RBAC
4. **Workshop Discussion / Team Dynamics (30:00-38:00)** -- Richard's frustration about being excluded, team morale talk

## Power Dynamics
- **Richard** oscillates between strategic leader and frustrated operative. His raw candour about Liz, Josh, and the workshop exclusion reveals both his authenticity and his exhaustion.
- **BenVH** continues to be the quiet technical anchor -- merging, deploying, verifying
- **Azmain** is caught in the middle -- Richard tells him to focus on the build while CSM workshops pull his attention
- **Philip and Sneha** represent the CSM adoption frontline -- their testing is what validates the tool for the broader group

## Stakeholder Signals
- **Philip Garner:** Forward-thinking -- his client-facing dashboard request shows he is thinking beyond the internal tool. Growing into an internal champion.
- **Sneha:** Providing hands-on testing beyond the core team. A positive sign of broader CSM engagement.
- **Richard:** Openly frustrated about being excluded from CSM workshops by Liz. His language is raw and unfiltered. He channels frustration into delivery focus but the resentment is real.
- **BenVH:** Steady and reliable. His role as the deployer and fixer is undramatic but essential.
- **Josh (offscreen):** Described as being at loggerheads with Ben. The political tension is becoming an operational drag.

## Commitments Made
| Who | Commitment | To Whom | Strength |
|-----|-----------|---------|----------|
| BenVH | Production RBAC fix deployed | Team | Done |
| Azmain | Will add permission error popups | Team | Moderate |
| Azmain | Will get another CSM to test | Team | Moderate |
| Richard | Will stay out of workshops -- focus on delivery | Self | Firm |

## Meeting Effectiveness
- **Clarity of purpose:** 8/10 -- Testing and verification with clear outcomes
- **Decision quality:** 8/10 -- RBAC confirmed, UX improvements identified
- **Follow-through potential:** 8/10 -- Production fixes deployed
- **Stakeholder alignment:** 5/10 -- Richard's exclusion from workshops signals deeper alignment issues
- **Time efficiency:** 7/10 -- Some tangents about team dynamics but overall productive

## Risk Signals
- **Richard's disengagement from CSM workshops** -- His choice not to engage is understandable but creates a gap between the build team and the CSM adoption effort. Severity: MEDIUM
- **Josh/Ben tension persisting** -- Described as "at loggerheads" with Josh being "resistant to change." Severity: MEDIUM
- **Liz gatekeeping workshops** -- Not inviting the builder of the tool to the training sessions about the tool is counterproductive. Severity: MEDIUM
- **Azmain's bandwidth** -- Being pulled between build work, data fixes, portfolio review redesign, workshops, and cross-OU coordination. Severity: HIGH

## Open Questions Raised
- When will the Jira API integration for product feature traceability be ready?
- How to handle CSM workshops that Azmain was not initially included in
- Timeline for adoption charter functionality -- Steve Gentilli and Liz Couchman need to agree first

## Raw Quotes of Note
- "This is the first time I've seen on the meeting... Okay, let's go through the accounts in this order. This is the priority" -- Richard, reflecting on the Portfolio Review's significance
- "Bro, I don't care. I really can give fuck. Let whoever wants to do whatever they want to do" -- Richard, on being excluded from CSM workshops
- "I'm being asked to spend my time across these different initiatives... Can you tell me which one we should be focusing on?" -- Azmain, revealing bandwidth stress

## Narrative Notes
This session serves two purposes. The first half is productive technical verification -- RBAC is confirmed working in production, which is a genuine milestone. Sneha's independent testing validates the fix beyond the core team. The second half reveals the political undercurrents: Richard's exclusion from CSM workshops is a symptom of the fragmented programme management. His raw language about Josh, Liz, and the broader dynamics is both illuminating and concerning -- it shows a leader who is stretched thin and losing patience with the politics. His advice to Azmain to "focus on what you need to focus on" is pragmatic but also a form of retreat from the stakeholder management that the programme desperately needs. The BenVH deployment of RBAC to production is the quiet win of the day.
