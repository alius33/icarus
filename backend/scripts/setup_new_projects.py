"""
Create 3 new projects and link historical transcripts + create ProjectSummary entries.

New projects:
- Cross OU Collaboration (cross-OU enablement work)
- Program Management (programme governance, standups, infrastructure, budget)
- TSR Enhancements (Idris's TSR automation work)

Run: docker exec icarus-backend-1 python -m scripts.setup_new_projects
"""

import asyncio
import sys
from datetime import date

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models.project import Project
from app.models.project_link import ProjectLink
from app.models.project_summary import ProjectSummary
from app.models.transcript import Transcript


async def main():
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        # ── 1. Create the 3 new projects ──
        new_projects = [
            {
                "name": "Cross OU Collaboration",
                "description": "Managing cross-operational unit collaboration — banking, life insurance, and asset management AI enablement discussions",
                "status": "active",
                "color": "#10B981",  # green
                "is_custom": True,
            },
            {
                "name": "Program Management",
                "description": "Programme-as-a-whole governance, standups, infrastructure, budget, and strategic alignment",
                "status": "active",
                "color": "#6366F1",  # indigo
                "is_custom": True,
            },
            {
                "name": "TSR Enhancements",
                "description": "Idris's TSR automation and AI enhancement work",
                "status": "active",
                "color": "#F59E0B",  # amber
                "is_custom": True,
            },
        ]

        project_ids = {}
        for proj_data in new_projects:
            # Check if already exists
            result = await db.execute(
                select(Project).where(Project.name == proj_data["name"])
            )
            existing = result.scalar_one_or_none()
            if existing:
                print(f"  Project '{proj_data['name']}' already exists (id={existing.id})")
                project_ids[proj_data["name"]] = existing.id
            else:
                project = Project(**proj_data)
                db.add(project)
                await db.flush()
                project_ids[proj_data["name"]] = project.id
                print(f"  Created project '{proj_data['name']}' (id={project.id})")

        await db.commit()

        # ── 2. Define transcript → project mappings ──
        # Format: transcript_id: (primary_project_name, relevance)

        # Get existing project IDs
        result = await db.execute(select(Project))
        all_projects = {p.name: p.id for p in result.scalars().all()}
        print(f"\nAll projects: {all_projects}")

        cross_ou_id = all_projects["Cross OU Collaboration"]
        program_mgmt_id = all_projects["Program Management"]
        tsr_id = all_projects["TSR Enhancements"]
        build_in_five_id = all_projects.get("Build in Five (Cursor for Pipeline Sales)")
        clara_id = all_projects.get("CLARA (IRP Adoption Tracker)")

        # Primary project assignments (transcript_id → project_id)
        primary_assignments = {
            # March 10 transcripts
            100: cross_ou_id,       # AI enablement with Life Insurance
            101: cross_ou_id,       # AI enablement with Banking
            102: program_mgmt_id,   # Chat with Rich about AWS Bedrock
            103: tsr_id,            # Intro to AI project for Idris
            104: build_in_five_id,  # Build in Five Standup
            105: build_in_five_id,  # Showing BenB Martin's Build in 5

            # Historical: Cross OU Collaboration
            35: cross_ou_id,    # 2026-02-04 AI discussion with Asset Management
            63: cross_ou_id,    # 2026-02-26 Chat with Asset Management
            96: cross_ou_id,    # 2026-03-03 Life Side SLT

            # Historical: Program Management
            17: program_mgmt_id,    # 2026-01-12 Program Review Rich
            34: program_mgmt_id,    # 2026-01-20 Programme Alignment and Stakeholder Readiness
            43: program_mgmt_id,    # 2026-02-09 Next Steps
            48: program_mgmt_id,    # 2026-02-11 Divya AI Programme Governance (16:16:12)
            55: program_mgmt_id,    # 2026-02-20 Natalia 1-1
            57: program_mgmt_id,    # 2026-02-23 Meeting with Diya
            58: program_mgmt_id,    # 2026-02-23 next 2 weeks plan
            61: program_mgmt_id,    # 2026-02-26 AI Infrastructure (first entry)
            86: program_mgmt_id,    # 2026-02-26 AI Infrastructure (duplicate)
            95: program_mgmt_id,    # 2026-03-03 GenAI Program Standup and Next Steps
        }

        # ── 3. Set primary_project_id on transcripts ──
        print("\nSetting primary_project_id on transcripts...")
        for tid, pid in primary_assignments.items():
            if pid is None:
                print(f"  Skipping transcript {tid} — project not found")
                continue
            await db.execute(
                update(Transcript)
                .where(Transcript.id == tid)
                .values(primary_project_id=pid)
            )
            print(f"  Transcript {tid} → project {pid}")
        await db.commit()

        # ── 4. Create ProjectLinks ──
        print("\nCreating project links...")
        for tid, pid in primary_assignments.items():
            if pid is None:
                continue
            # Check if link already exists
            result = await db.execute(
                select(ProjectLink).where(
                    ProjectLink.project_id == pid,
                    ProjectLink.entity_type == "transcript",
                    ProjectLink.entity_id == tid,
                )
            )
            if result.scalar_one_or_none():
                print(f"  Link already exists: project {pid} ← transcript {tid}")
                continue
            link = ProjectLink(project_id=pid, entity_type="transcript", entity_id=tid)
            db.add(link)
            print(f"  Linked: project {pid} ← transcript {tid}")
        await db.commit()

        # ── 5. Create ProjectSummary entries ──
        print("\nCreating ProjectSummary entries...")

        # Fetch all relevant transcripts to get dates
        tid_list = list(primary_assignments.keys())
        result = await db.execute(
            select(Transcript).where(Transcript.id.in_(tid_list))
        )
        transcripts = {t.id: t for t in result.scalars().all()}

        # Summary content for each transcript → project
        summary_content = {
            # Cross OU Collaboration
            (100, cross_ou_id): "**Life Insurance AI Enablement** — First engagement with Jack Cheyne and Christian Curran from the Life Insurance OU. Explored potential AI use cases for their team, focusing on document processing and underwriting workflows. Strong initial interest in leveraging CLARA's architecture for their domain.",
            (101, cross_ou_id): "**Banking AI Enablement** — Discussion with Gina Greer and Olivier from Banking OU about AI opportunities. Mapped out potential collaboration areas and shared learnings from the Customer Success programme. Identified TSR automation as a cross-OU opportunity.",
            (35, cross_ou_id): "**Asset Management Discussion** — Initial exploratory conversation about AI adoption in Asset Management. Discussed potential use cases and how the Customer Success programme's tools might be adapted for their needs.",
            (63, cross_ou_id): "**Asset Management Follow-up** — Continued dialogue with Asset Management team. Discussed specific workflow pain points and potential AI solutions. Alignment growing on collaborative approach.",
            (96, cross_ou_id): "**Life Side SLT** — Senior Leadership Team presentation on the Life Insurance side. Showcased the Customer Success AI programme's progress and discussed cross-OU expansion plans.",

            # Program Management
            (102, program_mgmt_id): "**AWS Bedrock Discussion** — Chat with Rich about AWS Claude Bedrock usage, infrastructure costs, and scaling considerations for the programme. Reviewed current token usage patterns and discussed optimization strategies.",
            (17, program_mgmt_id): "**Programme Review** — Comprehensive review session with Rich covering all workstreams, resource allocation, and strategic priorities. Set direction for the coming weeks.",
            (34, program_mgmt_id): "**Programme Alignment & Stakeholder Readiness** — Cross-functional alignment meeting. Discussed stakeholder readiness for key upcoming milestones and identified gaps in communication.",
            (43, program_mgmt_id): "**Next Steps Planning** — Mapped out immediate priorities and resource allocation across all workstreams. Addressed blockers and dependencies.",
            (48, program_mgmt_id): "**Diya AI Programme Governance** — Diya's first governance session covering programme structure, reporting cadence, and oversight mechanisms. Key step in formalizing programme management.",
            (55, program_mgmt_id): "**Natalia 1-1** — One-on-one with Natalia covering programme health, team dynamics, and upcoming priorities. Discussed data quality improvements and stakeholder engagement.",
            (57, program_mgmt_id): "**Meeting with Diya** — Follow-up governance discussion. Addressed budget tracking, resource planning, and alignment with broader organizational AI strategy.",
            (58, program_mgmt_id): "**Next 2 Weeks Plan** — Sprint planning for the programme. Mapped out deliverables, dependencies, and key milestones for the coming fortnight.",
            (61, program_mgmt_id): "**AI Infrastructure** — Discussion about the programme's AI infrastructure needs, including compute resources, model access, and development environment setup.",
            (86, program_mgmt_id): "**AI Infrastructure (continued)** — Extended infrastructure planning session. Covered deployment architecture, cost management, and scaling strategy.",
            (95, program_mgmt_id): "**GenAI Program Standup & Next Steps** — Weekly programme standup covering progress across all workstreams. Identified key blockers and action items for the week ahead.",

            # TSR Enhancements
            (103, tsr_id): "**Intro to AI for Idris** — Initial discussion with Idris about AI-driven TSR enhancements. Mapped out the current TSR workflow pain points and identified automation opportunities. This is the first call establishing this workstream.",

            # Build in Five (March 10)
            (104, build_in_five_id): "**Build in Five Standup** — Regular standup covering progress on Martin's Build in Five project. Discussed timeline to March 21 demo and remaining work items.",
            (105, build_in_five_id): "**Showing BenB Martin's Build** — Demo session showing Ben B the progress on Martin's Build in Five project. Gathered feedback and discussed next steps.",
        }

        for (tid, pid), content in summary_content.items():
            if pid is None:
                continue
            t = transcripts.get(tid)
            if not t:
                print(f"  Transcript {tid} not found, skipping")
                continue

            # Check if summary already exists
            result = await db.execute(
                select(ProjectSummary).where(
                    ProjectSummary.project_id == pid,
                    ProjectSummary.transcript_id == tid,
                )
            )
            if result.scalar_one_or_none():
                print(f"  ProjectSummary already exists: project {pid} / transcript {tid}")
                continue

            relevance = "HIGH" if tid in primary_assignments and primary_assignments[tid] == pid else "MEDIUM"
            summary = ProjectSummary(
                project_id=pid,
                transcript_id=tid,
                date=t.meeting_date,
                relevance=relevance,
                content=content,
                source_file=t.filename,
            )
            db.add(summary)
            print(f"  Created ProjectSummary: project {pid} / transcript {tid} ({t.meeting_date})")

        await db.commit()
        print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())
