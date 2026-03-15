"""Add programme deliverables, milestones, weekly plans, actions, and progress snapshots

Revision ID: 018
Revises: 017
"""

from alembic import op
import sqlalchemy as sa

revision = "018"
down_revision = "017"


def upgrade():
    # Programme deliverables
    op.create_table(
        "programme_deliverables",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("pillar", sa.Integer(), nullable=False),
        sa.Column("pillar_name", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("rag_status", sa.String(), nullable=False, server_default="GREEN"),
        sa.Column("progress_percent", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_programme_deliverables_pillar", "programme_deliverables", ["pillar"])

    # Deliverable milestones
    op.create_table(
        "deliverable_milestones",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "deliverable_id",
            sa.Integer(),
            sa.ForeignKey("programme_deliverables.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="NOT_STARTED"),
        sa.Column("target_week", sa.Integer(), nullable=True),
        sa.Column("completed_week", sa.Integer(), nullable=True),
        sa.Column("evidence", sa.Text(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_deliverable_milestones_deliverable", "deliverable_milestones", ["deliverable_id"])

    # Weekly plans
    op.create_table(
        "weekly_plans",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("week_number", sa.Integer(), nullable=False, unique=True),
        sa.Column("week_start_date", sa.Date(), nullable=False),
        sa.Column("week_end_date", sa.Date(), nullable=False),
        sa.Column("deliverable_progress_summary", sa.Text(), nullable=True),
        sa.Column("programme_actions_summary", sa.Text(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="DRAFT"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_weekly_plans_week_number", "weekly_plans", ["week_number"])

    # Weekly plan actions
    op.create_table(
        "weekly_plan_actions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "weekly_plan_id",
            sa.Integer(),
            sa.ForeignKey("weekly_plans.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("priority", sa.String(), nullable=False, server_default="MEDIUM"),
        sa.Column("owner", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="PENDING"),
        sa.Column(
            "deliverable_id",
            sa.Integer(),
            sa.ForeignKey("programme_deliverables.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_ai_generated", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("carried_from_week", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_weekly_plan_actions_plan", "weekly_plan_actions", ["weekly_plan_id"])
    op.create_index("idx_weekly_plan_actions_deliverable", "weekly_plan_actions", ["deliverable_id"])

    # Deliverable progress snapshots
    op.create_table(
        "deliverable_progress_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "deliverable_id",
            sa.Integer(),
            sa.ForeignKey("programme_deliverables.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "weekly_plan_id",
            sa.Integer(),
            sa.ForeignKey("weekly_plans.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("week_number", sa.Integer(), nullable=False),
        sa.Column("rag_status", sa.String(), nullable=False, server_default="GREEN"),
        sa.Column("progress_percent", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("milestones_completed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("milestones_total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("narrative", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_progress_snapshots_deliverable", "deliverable_progress_snapshots", ["deliverable_id"])
    op.create_index("idx_progress_snapshots_plan", "deliverable_progress_snapshots", ["weekly_plan_id"])

    # --- Seed deliverables and milestones ---
    deliverables_table = sa.table(
        "programme_deliverables",
        sa.column("id", sa.Integer),
        sa.column("pillar", sa.Integer),
        sa.column("pillar_name", sa.String),
        sa.column("title", sa.String),
        sa.column("description", sa.Text),
        sa.column("position", sa.Integer),
        sa.column("project_id", sa.Integer),
        sa.column("rag_status", sa.String),
        sa.column("progress_percent", sa.Integer),
        sa.column("notes", sa.Text),
    )

    milestones_table = sa.table(
        "deliverable_milestones",
        sa.column("id", sa.Integer),
        sa.column("deliverable_id", sa.Integer),
        sa.column("title", sa.String),
        sa.column("description", sa.Text),
        sa.column("status", sa.String),
        sa.column("target_week", sa.Integer),
        sa.column("completed_week", sa.Integer),
        sa.column("evidence", sa.Text),
        sa.column("position", sa.Integer),
    )

    # Pillar 1: IRP Portfolio Governance -> CLARA (project_id=1)
    deliverables = [
        dict(id=1, pillar=1, pillar_name="IRP Portfolio Governance", title="Real-time visibility into IRP adoption, milestones, and blockers", description="CLARA dashboard providing live view of IRP adoption status across clients", position=0, project_id=1, rag_status="GREEN", progress_percent=33, notes="CLARA is live and being used by CSMs. Dashboard shows adoption data."),
        dict(id=2, pillar=1, pillar_name="IRP Portfolio Governance", title="Automated adoption charters generation", description="Auto-generate adoption charter documents from IRP data", position=1, project_id=1, rag_status="AMBER", progress_percent=0, notes="Charter template design not yet started."),
        dict(id=3, pillar=1, pillar_name="IRP Portfolio Governance", title="60-90% reduction in manual reporting effort", description="Reduce manual reporting through CLARA automation", position=2, project_id=1, rag_status="GREEN", progress_percent=33, notes="Initial automation reducing some manual work. Further reduction expected as CLARA matures."),
        dict(id=4, pillar=1, pillar_name="IRP Portfolio Governance", title="Clear tracking of onboarding progress, blockers and outcomes", description="End-to-end onboarding tracking in CLARA", position=3, project_id=1, rag_status="GREEN", progress_percent=33, notes="Blocker tracking operational. Onboarding flow being refined."),
        dict(id=5, pillar=1, pillar_name="IRP Portfolio Governance", title="Future Phases: Casualty & Cyber products", description="Extend CLARA to cover Casualty and Cyber product lines", position=4, project_id=1, rag_status="GREEN", progress_percent=0, notes="Not yet started — scheduled for later phases."),
        # Pillar 2: Platform-Embedded Customer Intelligence -> CS Agent (7), Navigator (5)
        dict(id=6, pillar=2, pillar_name="Platform-Embedded Customer Intelligence", title="AI-assisted case preparation and executive meeting support", description="AI tools to prepare CSMs for client meetings with relevant data and talking points", position=0, project_id=7, rag_status="AMBER", progress_percent=0, notes="Concept defined but not yet built."),
        dict(id=7, pillar=2, pillar_name="Platform-Embedded Customer Intelligence", title="Intelligence layer connecting Salesforce and IRP usage data", description="Bridge between Salesforce CRM data and IRP platform usage metrics", position=1, project_id=7, rag_status="AMBER", progress_percent=0, notes="Data mapping in early stages. Salesforce integration requires coordination."),
        dict(id=8, pillar=2, pillar_name="Platform-Embedded Customer Intelligence", title="Navigator API testing embedded into CS workflows", description="IRP Navigator API testing integrated into daily CS operations", position=2, project_id=5, rag_status="GREEN", progress_percent=33, notes="Navigator API analysis underway. L1 automation concepts developing."),
        dict(id=9, pillar=2, pillar_name="Platform-Embedded Customer Intelligence", title="Foundation for automated L1 triage via Salesforce skill", description="Automated first-level support triage using Salesforce skill integration", position=3, project_id=5, rag_status="AMBER", progress_percent=0, notes="Dependent on Navigator API and Salesforce integration."),
        # Pillar 3: Internal Productivity & Revenue Acceleration -> Build in Five (3), App Factory (10)
        dict(id=10, pillar=3, pillar_name="Internal Productivity & Revenue Acceleration", title="Rapid client POC development for Property & Casualty", description="Build in Five framework for rapid POC delivery", position=0, project_id=3, rag_status="GREEN", progress_percent=33, notes="Martin actively developing. Build in Five framework operational."),
        dict(id=11, pillar=3, pillar_name="Internal Productivity & Revenue Acceleration", title="Live API demonstrations in pre-sales", description="Real-time API demos for pre-sales meetings", position=1, project_id=3, rag_status="AMBER", progress_percent=0, notes="Demo environment setup in progress."),
        dict(id=12, pillar=3, pillar_name="Internal Productivity & Revenue Acceleration", title="Improved delivery velocity and pipeline conversion", description="Faster delivery cycles and better pipeline conversion rates", position=2, project_id=10, rag_status="GREEN", progress_percent=33, notes="App Factory platform operational. Deployment automation working."),
        dict(id=13, pillar=3, pillar_name="Internal Productivity & Revenue Acceleration", title="Shared best practices across Insurance, Banking, and AM", description="Cross-OU knowledge sharing on AI development practices", position=3, project_id=None, rag_status="GREEN", progress_percent=33, notes="Cross-OU meetings happening. Banking Credit team AI training discovered. Idrees Deen building bridges."),
    ]
    op.bulk_insert(deliverables_table, deliverables)

    # Seed milestones — 2-4 per deliverable, some already completed for weeks 1-3
    # All dicts must have identical keys for bulk_insert
    def m(id, did, title, status, tw, pos, cw=None, ev=None, desc=None):
        return dict(id=id, deliverable_id=did, title=title, description=desc, status=status, target_week=tw, completed_week=cw, evidence=ev, position=pos)

    milestones = [
        # D1: Real-time visibility
        m(1, 1, "CLARA dashboard live with IRP data", "COMPLETED", 2, 0, cw=1, ev="CLARA launched and operational since programme start"),
        m(2, 1, "Blocker tracking operational", "IN_PROGRESS", 4, 1, ev="Blocker data entry working but deployment refresh issues reported"),
        m(3, 1, "Portfolio-level reporting available", "NOT_STARTED", 8, 2),
        # D2: Automated charters
        m(4, 2, "Charter template designed", "NOT_STARTED", 5, 0),
        m(5, 2, "Auto-generation from IRP data working", "NOT_STARTED", 8, 1),
        m(6, 2, "CSM adoption of generated charters", "NOT_STARTED", 11, 2),
        # D3: 60-90% reporting reduction
        m(7, 3, "Baseline manual effort measured", "COMPLETED", 2, 0, cw=2, ev="Manual reporting effort documented during initial assessment"),
        m(8, 3, "First automated reports replacing manual", "IN_PROGRESS", 6, 1, ev="CLARA generating some automated views, replacing ad-hoc spreadsheets"),
        m(9, 3, "Target reduction validated with metrics", "NOT_STARTED", 10, 2),
        # D4: Onboarding tracking
        m(10, 4, "Onboarding stages defined in CLARA", "COMPLETED", 3, 0, cw=2, ev="IRP onboarding stages mapped in CLARA"),
        m(11, 4, "Outcome tracking per client", "IN_PROGRESS", 6, 1),
        m(12, 4, "Blocker-to-resolution workflow operational", "NOT_STARTED", 9, 2),
        # D5: Casualty & Cyber
        m(13, 5, "Product scope assessment for Casualty", "NOT_STARTED", 8, 0),
        m(14, 5, "Cyber product data mapping", "NOT_STARTED", 10, 1),
        # D6: AI-assisted case prep
        m(15, 6, "Meeting brief template designed", "NOT_STARTED", 5, 0),
        m(16, 6, "Auto-brief generation from CRM data", "NOT_STARTED", 8, 1),
        m(17, 6, "CSM usage in live meetings", "NOT_STARTED", 11, 2),
        # D7: Salesforce-IRP intelligence
        m(18, 7, "Data mapping documented", "NOT_STARTED", 4, 0),
        m(19, 7, "Read-only integration working", "NOT_STARTED", 7, 1),
        m(20, 7, "Bi-directional sync operational", "NOT_STARTED", 11, 2),
        # D8: Navigator API testing
        m(21, 8, "Navigator API endpoints catalogued", "COMPLETED", 3, 0, cw=3, ev="API analysis completed, endpoints documented"),
        m(22, 8, "Test suite embedded in CS workflow", "NOT_STARTED", 7, 1),
        m(23, 8, "L1 automation POC running", "NOT_STARTED", 10, 2),
        # D9: Automated L1 triage
        m(24, 9, "Triage decision tree designed", "NOT_STARTED", 6, 0),
        m(25, 9, "Salesforce skill prototype", "NOT_STARTED", 9, 1),
        m(26, 9, "L1 triage pilot with real cases", "NOT_STARTED", 12, 2),
        # D10: Rapid POC development
        m(27, 10, "Build in Five framework documented", "COMPLETED", 2, 0, cw=2, ev="Martin onboarded, framework established"),
        m(28, 10, "First POC delivered to client", "IN_PROGRESS", 6, 1, ev="Martin actively building first POC"),
        m(29, 10, "Second POC with different product line", "NOT_STARTED", 10, 2),
        # D11: Live API demos
        m(30, 11, "Demo environment set up", "IN_PROGRESS", 4, 0, ev="Environment setup underway"),
        m(31, 11, "First live demo in pre-sales meeting", "NOT_STARTED", 7, 1),
        m(32, 11, "Reusable demo library created", "NOT_STARTED", 10, 2),
        # D12: Delivery velocity
        m(33, 12, "App Factory platform operational", "COMPLETED", 2, 0, cw=1, ev="BenVH has App Factory running, deployments automated"),
        m(34, 12, "First external team onboarded", "IN_PROGRESS", 5, 1, ev="Lucia's team identified as first App Factory external customer"),
        m(35, 12, "Pipeline conversion metrics tracked", "NOT_STARTED", 9, 2),
        # D13: Shared best practices
        m(36, 13, "Cross-OU meeting cadence established", "COMPLETED", 3, 0, cw=3, ev="Regular meetings with Banking (Idrees Deen), AM outreach started"),
        m(37, 13, "Shared AI development standards documented", "NOT_STARTED", 7, 1),
        m(38, 13, "Joint initiative launched with another OU", "NOT_STARTED", 10, 2),
    ]
    op.bulk_insert(milestones_table, milestones)


def downgrade():
    op.drop_index("idx_progress_snapshots_plan", table_name="deliverable_progress_snapshots")
    op.drop_index("idx_progress_snapshots_deliverable", table_name="deliverable_progress_snapshots")
    op.drop_table("deliverable_progress_snapshots")
    op.drop_index("idx_weekly_plan_actions_deliverable", table_name="weekly_plan_actions")
    op.drop_index("idx_weekly_plan_actions_plan", table_name="weekly_plan_actions")
    op.drop_table("weekly_plan_actions")
    op.drop_index("idx_weekly_plans_week_number", table_name="weekly_plans")
    op.drop_table("weekly_plans")
    op.drop_index("idx_deliverable_milestones_deliverable", table_name="deliverable_milestones")
    op.drop_table("deliverable_milestones")
    op.drop_index("idx_programme_deliverables_pillar", table_name="programme_deliverables")
    op.drop_table("programme_deliverables")
