"""
One-time backfill script: Run AFTER deploying migration 022.
Adds summaries, ProjectSummary entries, and source_update_id to the 4 existing updates.

Usage:
    python -m scripts.backfill_update_summaries
"""

import requests

BASE = "https://icarus-production-5044.up.railway.app/api"

# Analytical summaries for each update
SUMMARIES = {
    1: (
        "- **Samuel Gibson** (Risk Modeller demo team, UK) added to Build in Five Teams chat by Ben Brookes\n"
        "- Gibson keen on MCP server possibilities for customer demos — wants to show capabilities to clients\n"
        "- Richard flagged need to connect Gibson and Mike with Martin's Build in Five work\n"
        "- Richard asked Azmain to organize stakeholder share-out sessions (MPS, Sales, Product) — similar format to App Factory showcase\n"
        "- Timing: once Martin's work is ready for demonstration"
    ),
    2: (
        "- **Gainsight Charter V1** created by Azmain (13 Mar) and shared for review\n"
        "- Ben Brookes flagged critical business requirements: integration must not slow migration, split CSM workflows, or block adoption squads\n"
        "- Natalia Orzechowska suggested consulting CSMs on business requirements\n"
        "- Idrees Deen (Banking CS) offered help with Gainsight integration\n"
        "- **Richard Dosoo pushed back hard**: team was excluded from scoping exercise impacting their roadmap\n"
        "- Richard demanded Phase 0: structured CLARA feature review with Gainsight team present before proceeding\n"
        "- Specific gap: adoption charter workflow missing from Gainsight documentation despite expected high charter volume\n"
        "- Political dimension: COE authority assertion by Kathryn Palkovics intersects with Gainsight governance"
    ),
    3: (
        "- Azmain requested 2 graduates for AI programme: **Alvin** (London) and **Sam** (New York)\n"
        "- Both interviewed and selected specifically for AI programme work\n"
        "- **Nikhil Koli** separately requesting replacement for Elliot (former team member brought into AI programme)\n"
        "- Risk: Nikhil may attempt to redirect one of the AI programme grads to backfill his own shortage\n"
        "- Azmain escalated concern to Richard for resolution\n"
        "- Resource tension reflects broader Nikhil boundary issues (50% CLARA / 50% App Factory split)"
    ),
    4: (
        "- **Emma Jaggs** (graduate manager) confirmed only 2 grads total in Q2: Alvin and Sam — not 3\n"
        "- Richard Dosoo clarified to Emma: Azmain's 2 analysts for CLARA development are separate from Nikhil's Elliot replacement\n"
        "- Richard confirmed CLARA support is a separate workstream from IRP adoption (under Nikhil)\n"
        "- Emma and Richard to meet Monday to align\n"
        "- **Azmain's private concern to Richard**: grads were interviewed and told they're coming for AI work, now Nikhil may 'pinch' one\n"
        "- Richard reassured: Nikhil's replacement request is completely separate, Emma incorrectly mixed the two together\n"
        "- Highlights ongoing confusion around resource boundaries between Nikhil's team and AI programme"
    ),
}

# ProjectSummary entries to create (project_id, update_id, date, relevance, content)
PROJECT_SUMMARIES = [
    # Update 1 → Build in Five (6)
    (6, 1, "2026-03-16", "MEDIUM",
     "- Samuel Gibson (Risk Modeller) added to Build in Five chat — keen on MCP server for customer demos\n"
     "- Richard wants to connect Gibson/Mike with Martin's work\n"
     "- Stakeholder share-out sessions to be organized once Martin's work is ready"),
    # Update 2 → CLARA (2)
    (2, 2, "2026-03-16", "HIGH",
     "- Gainsight Charter V1 created and shared for review\n"
     "- Ben Brookes flagged business requirements: no migration slowdown, no CSM workflow split\n"
     "- Richard demanded Phase 0 CLARA feature review with Gainsight team before proceeding\n"
     "- Adoption charter workflow missing from Gainsight documentation — critical gap"),
    # Update 3 → Program Management (8)
    (8, 3, "2026-03-16", "MEDIUM",
     "- 2 graduates requested for AI programme (Alvin + Sam), selected through interviews\n"
     "- Nikhil separately requesting Elliot replacement — risk of resource conflict\n"
     "- Escalated to Richard for resolution"),
    # Update 4 → Program Management (8)
    (8, 4, "2026-03-16", "HIGH",
     "- Emma Jaggs confirmed only 2 grads in Q2 (Alvin + Sam)\n"
     "- Richard clarified: CLARA dev support is separate from Nikhil's IRP adoption / Elliot replacement\n"
     "- Monday meeting with Emma to fully resolve allocation confusion"),
    # Update 4 → App Factory (10)
    (10, 4, "2026-03-16", "LOW",
     "- Nikhil's request for Elliot replacement touches App Factory (Nikhil is 50% App Factory)\n"
     "- Resource allocation confusion may indirectly affect App Factory staffing"),
]

# Weekly plan actions to update with source_update_id
ACTION_UPDATES = {
    67: 1,  # "Organize Build in Five stakeholder share-out sessions" → update 1
    65: 2,  # "Review and finalize Gainsight Charter V1" → update 2
    66: 2,  # "Plan Phase 0 CLARA feature review for Gainsight integration" → update 2
    68: 2,  # "Establish COE boundary: RACI for Gainsight workstream" → update 2
    64: 4,  # "Resolve grad allocation confusion" → update 4
}


def main():
    print("=== Phase 1: PATCH summaries onto update records ===")
    for uid, summary in SUMMARIES.items():
        r = requests.patch(f"{BASE}/project-updates/{uid}", json={"summary": summary})
        print(f"  Update {uid}: {r.status_code}")
        if r.status_code != 200:
            print(f"    ERROR: {r.text[:200]}")

    print("\n=== Phase 2: Create ProjectSummary entries ===")
    for project_id, update_id, date, relevance, content in PROJECT_SUMMARIES:
        r = requests.post(f"{BASE}/project-summaries", json={
            "project_id": project_id,
            "project_update_id": update_id,
            "date": date,
            "relevance": relevance,
            "content": content,
        })
        print(f"  Project {project_id} ← Update {update_id}: {r.status_code}")
        if r.status_code not in (200, 201):
            print(f"    ERROR: {r.text[:200]}")

    print("\n=== Phase 3: Set source_update_id on weekly plan actions ===")
    for action_id, update_id in ACTION_UPDATES.items():
        r = requests.patch(f"{BASE}/weekly-plans/actions/{action_id}", json={
            "source_update_id": update_id,
        })
        print(f"  Action {action_id} → Update {update_id}: {r.status_code}")
        if r.status_code != 200:
            print(f"    ERROR: {r.text[:200]}")

    print("\nDone! Verify at:")
    print("  - https://icarus-production-5044.up.railway.app/projects/2 (CLARA Current Status)")
    print("  - https://icarus-production-5044.up.railway.app/projects/6 (Build in Five Current Status)")
    print("  - https://icarus-production-5044.up.railway.app/projects/8 (Program Management Current Status)")
    print("  - https://icarus-production-5044.up.railway.app/weekly-plan (action context panels)")


if __name__ == "__main__":
    main()
