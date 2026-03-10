# Chat with Chris
**Date:** 2026-03-06
**Attendees:** Azmain Hossain, Chris M
**Duration context:** Short (~10 minutes)
**Workstreams touched:** WS2 CLARA

## Key Points
- **Chris's bug triage progress**: Chris has been going through the consolidated feedback list using Cursor to do a first-pass analysis of what is fixed vs. what remains. Most early feedback items (first two weeks of February) appear to be already fixed but never marked as such. More recent items are still open or undetermined.
- **Azmain's approach to bug prioritisation**: Start with the most recent feedback first (more likely to be genuine open issues), then work backwards by date. Older items are probably fixed but undocumented.
- **Data access blocker**: Many bug verifications require data access that Chris does not yet have. He needs the data to confirm whether issues are code-related or data-related.
- **Bugs are "nice to have" not "must have"**: Azmain clarified that all critical bugs are already fixed (portfolio review works for Natalia, management dashboard works for Diya/Ben Brooks). Remaining bugs are user-level problems, and the users only log in on Sunday evenings to update before Monday calls anyway.
- **Learning opportunity framing**: Azmain positioned bug fixing as an onboarding exercise for Chris -- getting familiar with the codebase and workflow -- rather than urgent production fixes.
- **Two grads arriving April 7**: One in New York, one in London. Bug fixes will be their initial assignment too. Chris's bug fix work will create a template process for them.
- **Nikhil frustration (briefly)**: Azmain mentioned that Nikhil speaking up in the advisory all-hands surprised him and that he needs a single source of truth on technical matters -- he will always defer to BenVH as the creator of App Factory.
- **Stacy and Catherine's field debates**: Azmain referenced the "essays" in the IRP adoption chat about individual fields and explicitly said he does not want that level of debate replicated on the technical side.
- **Security audit revelation**: Azmain candidly told Chris that the security team caught them using personal Claude accounts for Moody's work, that it is "mildly illegal," and that Ben Brooks is providing cover. He said the claim of no proprietary information being involved is "wildly a lie, but whatever." Now that Bedrock API is working, this should be resolved going forward.
- **Next week's plan**: After Chris finishes bugs this week, he will move to features and additions next week. Bugs first, features second -- fix the broken stuff before adding more.

## Decisions Made
- Bug fixes are a learning exercise, not urgent production work -> Azmain
- Work through feedback list from most recent to oldest -> Azmain
- Features and additions deferred to next week -> Azmain
- Two grads (arriving April 7) will inherit ongoing bug fix work -> Azmain

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Continue working through bug/defect list (most recent first) | Chris | This week | Open |
| Get data access for Chris to verify data-dependent bugs | Azmain/BenVH | ASAP | Open |
| Transition to feature work next week | Chris | Next week | Open |

## Stakeholder Signals
- **Chris** is methodical and humble. He acknowledges this is a learning opportunity and is not trying to rush or overextend. Good cultural fit for the team.
- **Azmain** is managing expectations well -- making clear that bug fixes are not urgent while still valuing Chris's contribution. He is also being remarkably candid about the security risks the team has taken.
- The "mildly illegal" personal account usage and the "wildly a lie" claim about no proprietary information are notable admissions that signal the programme has been operating in a grey area that is now being cleaned up with Bedrock API access.

## Open Questions Raised
- When will Chris get data access to verify data-dependent bugs?
- What will Chris's feature work look like next week?
- Who exactly are the two April grads?

## Raw Quotes of Note
- "The security audit caught it... we were just like, there's no proprietary information, which is wildly a lie, but whatever. Ben is providing cover for us." -- Azmain, on the personal account usage
