# Catchup x Ben Rich 6pm
**Date:** 2026-01-14
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brooks, BenVH (Van Houten)
**Duration context:** Long (~33 minutes)
**Workstreams touched:** WS2 (CLARA), WS6 (Build in Five)

## Key Points
- Evening call to coordinate on the deployed app and plan for the advisory team demo the following day (15 Jan).
- The base version of the app is now deployed on AWS with dashboard, RAG statuses, use cases by customer, blockers, and data issues visible. Migration statuses are not yet showing.
- Ben Brooks has been fixing things locally with Opus -- improved dashboard with migration stats, attention-needed tabs. He demonstrates a mock-up account planning app he built for George Dyke in just two prompts with Opus ("the depth of what it produces is insane").
- Ben's phasing strategy is explicit: first get use cases, blockers, data issues, action plans, and team members working impressively. Then move to charters, blueprints, milestones. Bottom half of the menu can be switched off for now.
- Richard raises the 26 Jan meeting with Sales Recon -- wants to walk Jamie and Ari Lahavi through the tracker and show CS requirements that should eventually migrate to Sales Recon. This is about transparency, not waiting for Sales Recon to deliver.
- Ben is cautious about anything that slows them down waiting for a future Sales Recon solution.
- Azmain is walked through Git workflow for the first time: cloning the repo into Cursor, making changes locally, pushing to a feature branch, then doing a pull request to main. This is a learning moment -- Azmain is building development skills in real-time.
- All three discuss Opus's superiority over other models for development work. Richard is on the Max Max plan ($100/month personal spend). Azmain keeps getting rate-limited on Opus.
- Richard is out Friday for a family commitment. BenVH is heading to Amsterdam Friday evening for a HighRox race. Tomorrow (Wednesday) is the final push before both are unavailable.
- Immediate plan: Azmain pulls down the repo, builds locally, makes CRUD operation changes for the first seven entities, tests on localhost, then does a pull request.

## Decisions Made
- Phase the app: use cases, blockers, data issues, action plans, team members first; charters/blueprints/milestones second; hide bottom half of menu for now -> Ben Brooks
- Show the tracker to Sales Recon team at 26 Jan meeting as a transparency exercise, not as a request to wait for their solution -> Richard
- Azmain to start making CRUD operation changes on a feature branch tonight -> Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Pull down repo and start CRUD operations for first seven entities | Azmain | Tonight/tomorrow morning | Open |
| Fix CICD pipeline so merges to main auto-deploy | BenVH/Richard | Tonight | Open |
| Demo deployed app to advisory team (Stacy, Liz, Christine, Steve) | Richard/Azmain | Tomorrow (15 Jan) | Open |
| Set up meeting with Idris for 26 Jan meeting prep | Richard | Next week | Open |
| Chase developer laptop approvals for Azmain | Richard | Tomorrow | Open |

## Stakeholder Signals
- Ben Brooks is energised by the pace and by Opus capabilities -- showing off what two prompts can do. Emotionally invested.
- BenVH is practical and focused on getting the infrastructure right. He is a single point of failure for deployment.
- Azmain is learning Git/CICD in real-time on the job but picking it up quickly. Richard is actively mentoring him through it.
- Richard is burning personal money (Max Max Claude plan) to keep development moving, which is unsustainable.

## Open Questions Raised
- When will Martin's Build in Five app need its own deployment environment? Richard initially thought it would be part of the same app but Ben wants it separate.
- How to manage multiple apps in the same ECS cluster?

## Raw Quotes of Note
- "No pressure. Josh has just sent me a Teams message saying, will your app be finished by 7pm because I have a leadership call I'd like to show it" -- Ben Brooks, relaying Josh's request mid-call
