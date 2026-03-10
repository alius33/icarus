# Tracker Discussion
**Date:** 2026-01-13
**Attendees:** Richard Dosoo, Azmain Hossain, Ben Brooks, BenVH (Van Houten)
**Duration context:** Long (~58 minutes, multi-part)
**Workstreams touched:** WS2 (CLARA)

## Key Points
- Core debate: what data to use for the first demo. Ben Brooks is worried that synthetic data will cause CSMs to fixate on errors ("that's wrong, that's not right") and disengage. Azmain had created both a golden source version (real but incomplete) and a synthetic data version (complete but fake).
- Decision: use real golden source data, acknowledge the gaps, and have CSMs fill in the rest. Create a separate test account with fake company names (e.g., "Acme Insurance") for demo purposes that can be deleted later. Ben suggests a toggle between real and demo data.
- Ben proposes phasing: first nail use cases, blockers, data issues, action plans, team members. Then move to charters, blueprints, milestones. Partners and partner bench come later.
- Mid-call, Ben Brooks gets a message from Josh Ellingson asking if the app will be ready by 7pm for a leadership call. This creates urgency.
- BenVH joins to help configure Azure SSO -- they walk through configuring redirect URIs in Azure Active Directory for the IRP Adoption Tracker (switching from "web" to "single page application"). Richard is made an application owner so he can troubleshoot independently.
- The Azure/Entra ID configuration is painstaking -- multiple attempts needed, with confusion over tenant IDs, client IDs, subscription IDs.
- Both Azmain and Richard can successfully log in to the deployed app via Microsoft SSO, but no data is showing (API not returning data -- networking/backend issue).
- BenVH gets added to the GitHub repo. His GitHub access had been raised via ticket but the Moody's provisioning process was slow.
- Discussion of CICD pipeline: BenVH needs to push his Docker/nginx changes to GitHub to avoid conflicting versions when setting up the deployment pipeline.

## Decisions Made
- Use real golden source data for demos, not synthetic data. Create separate fake test accounts for demo purposes -> Ben Brooks
- Phase features: first nail use cases, blockers, data issues, action plans, team members; then charters/blueprints/milestones -> Ben Brooks
- Build a toggle between real and demo data in the app -> Azmain
- Azmain to build a front-end data input mechanism rather than sharing raw Excel with CSMs for data entry -> discussed but Ben prefers using the deployed app directly

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Create test accounts with fake company names for demo mode | Azmain | This week | Open |
| Get CICD pipeline working from GitHub to AWS | BenVH/Richard | Tomorrow (14 Jan) | Open |
| Fix API backend issue preventing data from showing on deployed app | BenVH | ASAP | Open |
| Add BenVH to GitHub repo | Richard | Done in call | Open |
| Configure Azure SSO redirect URIs correctly | BenVH/Ben Brooks | Done in call (partially) | Open |

## Stakeholder Signals
- Ben Brooks is pushing hard for speed -- wants real data shown as soon as possible, does not want false pictures of any real accounts.
- Josh Ellingson's 7pm deadline request signals growing leadership interest but also pressure to deliver before the system is ready.
- BenVH is dealing with infrastructure friction (Azure policies, GitHub access, firewall blocks) but making progress.

## Open Questions Raised
- When will CICD pipeline be operational end-to-end?
- How to handle the dashboard when data is incomplete -- show the gaps honestly or hide them?
- When is the first real demo to CSMs with Natalia and team? (Target: next week Tuesday)

## Raw Quotes of Note
- "I don't want to create a false picture of any of the real accounts" -- Ben Brooks, on why demo data must be handled carefully
