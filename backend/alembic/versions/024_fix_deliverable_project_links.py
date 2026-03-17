"""Fix deliverable project_id links to match correct project IDs.

The original migration 018 seeded deliverables with project_id=NULL.
Subsequent manual linking used incorrect IDs. This migration sets the
correct project_id for each deliverable by looking up projects by name.

Also links D13 (Cross-OU best practices) to the Cross OU Collaboration project.

Revision ID: 024
Revises: 023
"""

from alembic import op
import sqlalchemy as sa

revision = "024"
down_revision = "023"
branch_labels = None
depends_on = None

# Mapping: deliverable IDs → correct project name
DELIVERABLE_PROJECT_MAP = {
    # Pillar 1: IRP Portfolio Governance → CLARA
    1: "CLARA (IRP Adoption Tracker)",
    2: "CLARA (IRP Adoption Tracker)",
    3: "CLARA (IRP Adoption Tracker)",
    4: "CLARA (IRP Adoption Tracker)",
    5: "CLARA (IRP Adoption Tracker)",
    # Pillar 2: Platform-Embedded Customer Intelligence
    6: "Customer Success Agent",       # was wrongly linked to Cross OU (id=7)
    7: "Customer Success Agent",       # was wrongly linked to Cross OU (id=7)
    8: "Navigator L1 Automation",      # correct already
    9: "Navigator L1 Automation",      # correct already
    # Pillar 3: Internal Productivity & Revenue Acceleration
    10: "Build in Five",               # was wrongly linked to CS Agent (id=3)
    11: "Build in Five",               # was wrongly linked to CS Agent (id=3)
    12: "App Factory",                 # correct already
    13: "Cross OU Collaboration",      # was NULL
    # D14 (Slidey) was set correctly by migration 023
}


def upgrade() -> None:
    conn = op.get_bind()

    # Build project name → id lookup
    result = conn.execute(sa.text("SELECT id, name FROM projects"))
    project_lookup = {row[1]: row[0] for row in result.fetchall()}

    for deliverable_id, project_name in DELIVERABLE_PROJECT_MAP.items():
        project_id = project_lookup.get(project_name)
        if project_id is not None:
            conn.execute(
                sa.text(
                    "UPDATE programme_deliverables "
                    "SET project_id = :pid "
                    "WHERE id = :did"
                ),
                {"pid": project_id, "did": deliverable_id},
            )


def downgrade() -> None:
    # Reset all to NULL (original state from migration 018)
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "UPDATE programme_deliverables SET project_id = NULL "
            "WHERE id <= 13"
        )
    )
