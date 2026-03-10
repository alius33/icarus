# Chat with Richard 1
**Date:** 2026-01-15
**Attendees:** Richard Dosoo, Azmain Hossain
**Duration context:** Long (~60 minutes)
**Workstreams touched:** WS2 (CLARA)

## Key Points
- Extended working session covering multiple topics: a lengthy discussion about a nightmare client project (Amnon/Amin), then reviewing Azmain's local build progress, and finally doing a Git push to the feature branch.
- The Amnon discussion is a cautionary tale about what happens without governance: the client had no strategic alignment, contractors incentivised to overrun, IT blaming business for indecision, and the Moody's team got steamrolled because they did not push back. Prashant (most junior team member) was assigned the worst project. Diana was frustrated. Ben had to intervene to change the working relationship. Richard frames this as exactly the kind of failure the tracker is designed to prevent.
- Azmain shows Richard his local build progress. Key changes: table view for all customers (replacing tab-based layout), pagination added, pop-up modals for CRUD operations, improved blocker/action plan navigation, collapsible action items within action plans.
- Richard and Azmain have a detailed discussion about adding an "updates" functionality -- a way for CSMs to add timestamped free-text updates to blockers, action plans, action items, use cases. This would create an auditable trail. Ben wants version control with change tracking, which is more complex. They discuss whether to use hierarchical vs flat table structures for this.
- Richard advises: before making schema changes for version control, they should meet with Natalia, Catherine, and Kevin to align on the data model with Gainsight integration in mind -- otherwise they risk building something that cannot integrate.
- The CICD pipeline is now working: when code is checked into main, BenVH's automation kicks in and deploys to AWS.
- Azmain and Richard discuss AI model quality extensively. Both are impressed by Opus. Richard is using Claude Code connected to the GitHub repo. They discuss multi-model approaches (using different LLMs for different tasks) and a workflow orchestrator tool that routes questions to the best model.
- Richard is going to push for enterprise Claude access through Divya -- suggests getting a PO for 5 licences at 500 GBP/month rather than waiting for the enterprise negotiation.
- Developer laptop approvals are stuck -- Azmain's request has been "in progress fulfilment" for 7 days. Richard will escalate to Diya and Ben.

## Decisions Made
- Before making schema changes for version control/updates, align data model with Natalia/Catherine/Kevin for Gainsight integration -> Richard to set up meeting
- Push for enterprise Claude licences through Divya rather than waiting for negotiation -> Richard
- Use table view instead of tab layout for all customers page -> Azmain (done)

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Set up data model alignment meeting with Natalia, Catherine, Kevin | Richard | Next week | Open |
| Escalate developer laptop approvals to Diya and Ben | Richard | Today | Open |
| Push for enterprise Claude access via Divya (5 licences, PO) | Richard | Next week | Open |
| Add pagination to use cases table | Azmain | Next iteration | Open |
| Push local changes to feature branch | Azmain | Done in call | Open |

## Stakeholder Signals
- Richard is deeply aware of what happens when projects lack governance (Amnon cautionary tale) and uses it to motivate the tracker's importance.
- Both Richard and Azmain are burning personal money on Claude licences -- this is an organisational failure that Richard plans to escalate.
- Developer laptop provisioning is a blocker -- Azmain cannot work effectively without it.

## Open Questions Raised
- How should version control / audit trail for updates be structured? Hierarchical vs flat table?
- When will developer laptops be approved?
- Can Divya greenlight enterprise Claude access quickly?

## Raw Quotes of Note
- "I don't know how the hell writing 10,000 lines of code in like six hours and not actually writing anything" -- Azmain, on the productivity gains from Opus in Cursor
