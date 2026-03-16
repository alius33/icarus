"""Remove workstreams system, add project codes

Revision ID: 019
Revises: 018
"""

from alembic import op
import sqlalchemy as sa

revision = "019"
down_revision = "018"


def upgrade():
    # 1. Add code column to projects
    op.add_column("projects", sa.Column("code", sa.String(), nullable=True))

    # 2. Populate project codes as PR{id}
    op.execute("UPDATE projects SET code = 'PR' || CAST(id AS VARCHAR)")

    # 3. Make code NOT NULL + unique
    op.alter_column("projects", "code", nullable=False)
    op.create_unique_constraint("uq_projects_code", "projects", ["code"])
    op.create_index("idx_projects_code", "projects", ["code"])

    # 4. Add project_id FK to decisions (migrate from workstream_id)
    op.add_column(
        "decisions",
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="SET NULL"), nullable=True),
    )
    # Migrate: decision.workstream_id -> find project with that workstream_id -> set decision.project_id
    op.execute("""
        UPDATE decisions d
        SET project_id = p.id
        FROM projects p
        WHERE d.workstream_id IS NOT NULL
          AND p.workstream_id = d.workstream_id
    """)

    # 5. Drop workstream_id from decisions
    op.drop_column("decisions", "workstream_id")

    # 6. Drop workstream_id from projects (drop index + constraint first)
    op.drop_index("idx_projects_workstream", table_name="projects")
    op.drop_constraint("projects_workstream_id_key", type_="unique", table_name="projects")
    op.drop_column("projects", "workstream_id")

    # 7. Rename workstream text columns on other tables
    op.alter_column("programme_wins", "workstream", new_column_name="project", existing_type=sa.String())
    op.alter_column("scope_items", "workstream", new_column_name="project", existing_type=sa.String())
    op.alter_column("adoption_metrics", "workstream", new_column_name="project", existing_type=sa.String())
    op.alter_column("dependencies", "affected_workstreams", new_column_name="affected_projects", existing_type=sa.Text())

    # 8. Rename JSON key in resource_allocations.allocations (workstream -> project)
    op.execute("""
        UPDATE resource_allocations
        SET allocations = (
            SELECT jsonb_agg(
                CASE WHEN elem ? 'workstream'
                    THEN (elem - 'workstream') || jsonb_build_object('project', elem->>'workstream')
                    ELSE elem
                END
            )
            FROM jsonb_array_elements(allocations::jsonb) AS elem
        )
        WHERE allocations IS NOT NULL
          AND allocations::text != '[]'
          AND allocations::text != 'null'
    """)

    # 9. Drop workstream tables (milestones first due to FK)
    op.drop_table("workstream_milestones")
    op.drop_table("workstreams")


def downgrade():
    raise NotImplementedError("One-way migration — workstream removal cannot be reversed")
