"""Add Slidey (AI Presentations) deliverable and milestones to Pillar 3.

Revision ID: 023
Revises: 022
"""

from alembic import op
import sqlalchemy as sa

revision = "023"
down_revision = "022"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    # Look up Slidey project ID
    result = conn.execute(
        sa.text("SELECT id FROM projects WHERE name = 'Slidey (AI Presentations)'")
    )
    row = result.fetchone()
    if not row:
        # Project may not exist yet if seed hasn't run — use NULL
        project_id = "NULL"
    else:
        project_id = str(row[0])

    # Insert Pillar 3 deliverable for Slidey
    conn.execute(
        sa.text(f"""
            INSERT INTO programme_deliverables
                (pillar, pillar_name, title, description, position, project_id,
                 rag_status, progress_percent, notes)
            VALUES
                (3,
                 'Internal Productivity & Revenue Acceleration',
                 'AI Presentation Platform (Slidey)',
                 'Collaborative AI-powered presentation tool deployed via App Factory infrastructure. Features markdown content layer, RBAC, and agentic extensions for account plans, charters, and executive decks.',
                 4,
                 {project_id},
                 'AMBER',
                 25,
                 'Auth + RBAC landed 16 Mar. Content layer in progress. Data scoping and env discipline are immediate blockers.')
        """)
    )

    # Get the deliverable ID we just inserted
    result = conn.execute(
        sa.text(
            "SELECT id FROM programme_deliverables "
            "WHERE title = 'AI Presentation Platform (Slidey)'"
        )
    )
    deliverable_id = result.fetchone()[0]

    # Insert milestones
    milestones = [
        (0, "Authentication + RBAC implemented", "COMPLETED", 4, 4,
         "Auth with logout landed 16 Mar. RBAC partially wired."),
        (1, "Markdown content layer operational", "IN_PROGRESS", 6, None,
         "CONTENT-LAYER.md spec created. Implementation started by Richard."),
        (2, "User data scoping + environment separation", "NOT_STARTED", 5, None,
         "User-ID filtering bug identified 16 Mar. No dev/staging/prod yet."),
        (3, "Collaborative editing workflow live", "NOT_STARTED", 8, None,
         "Storyboard workflow designed (brief > outline > edit > AI polish) but not built."),
    ]

    for pos, title, status, target_wk, completed_wk, evidence in milestones:
        completed_val = str(completed_wk) if completed_wk else "NULL"
        conn.execute(
            sa.text(f"""
                INSERT INTO deliverable_milestones
                    (deliverable_id, title, status, target_week, completed_week,
                     evidence, position)
                VALUES
                    ({deliverable_id},
                     '{title}',
                     '{status}',
                     {target_wk},
                     {completed_val},
                     '{evidence}',
                     {pos})
            """)
        )


def downgrade() -> None:
    conn = op.get_bind()

    # Delete milestones first (FK constraint)
    result = conn.execute(
        sa.text(
            "SELECT id FROM programme_deliverables "
            "WHERE title = 'AI Presentation Platform (Slidey)'"
        )
    )
    row = result.fetchone()
    if row:
        deliverable_id = row[0]
        conn.execute(
            sa.text(
                f"DELETE FROM deliverable_milestones "
                f"WHERE deliverable_id = {deliverable_id}"
            )
        )
        conn.execute(
            sa.text(
                f"DELETE FROM programme_deliverables WHERE id = {deliverable_id}"
            )
        )
