"""
Backfill ProjectSummary entries for all projects that have linked transcripts
but no corresponding ProjectSummary records.

Reads the full summary markdown from the summaries table, extracts the title
and first 2-3 key points, and creates concise project-relevant entries.

Run: docker exec icarus-backend-1 python -m scripts.backfill_project_summaries
"""

import asyncio
import re
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models.project import Project
from app.models.project_link import ProjectLink
from app.models.project_summary import ProjectSummary
from app.models.summary import Summary
from app.models.transcript import Transcript


def extract_title(markdown: str) -> str:
    """Extract the title from the first # heading."""
    for line in markdown.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_key_points(markdown: str, max_points: int = 3) -> list[str]:
    """Extract bullet points from the ## Key Points section."""
    lines = markdown.split("\n")
    in_section = False
    points = []

    for line in lines:
        stripped = line.strip()

        # Detect section start
        if stripped.startswith("## Key Points") or stripped.startswith("## Executive Summary"):
            in_section = True
            continue

        # Detect next section (stop)
        if in_section and stripped.startswith("## "):
            break

        # Capture bullet points
        if in_section and stripped.startswith("- "):
            point = stripped[2:].strip()
            # Clean up markdown bold
            point = re.sub(r"\*\*([^*]+)\*\*", r"\1", point)
            # Truncate very long points
            if len(point) > 200:
                point = point[:197] + "..."
            points.append(point)
            if len(points) >= max_points:
                break

    return points


def build_content(title: str, key_points: list[str]) -> str:
    """Build the concise ProjectSummary content from title + key points."""
    if not title and not key_points:
        return "Meeting summary — no key points extracted."

    # Format: **Title** — first point. Second point.
    parts = []
    if title:
        parts.append(f"**{title}**")

    if key_points:
        # Join first 2-3 points with periods
        summary_text = ". ".join(key_points)
        # Ensure it ends with a period
        if not summary_text.endswith("."):
            summary_text += "."
        if title:
            parts.append(f" — {summary_text}")
        else:
            parts.append(summary_text)

    return "".join(parts)


async def main():
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        # Get all projects
        result = await db.execute(select(Project).order_by(Project.id))
        projects = result.scalars().all()

        total_created = 0

        for project in projects:
            # Get linked transcript IDs for this project
            result = await db.execute(
                select(ProjectLink.entity_id).where(
                    ProjectLink.project_id == project.id,
                    ProjectLink.entity_type == "transcript",
                )
            )
            linked_tids = [r[0] for r in result.all()]

            if not linked_tids:
                continue

            # Get transcript IDs that already have ProjectSummary entries
            result = await db.execute(
                select(ProjectSummary.transcript_id).where(
                    ProjectSummary.project_id == project.id,
                )
            )
            existing_tids = {r[0] for r in result.all()}

            missing_tids = [tid for tid in linked_tids if tid not in existing_tids]

            if not missing_tids:
                print(f"  Project {project.id} ({project.name}): all {len(linked_tids)} transcripts covered")
                continue

            print(f"\n=== Project {project.id}: {project.name} — {len(missing_tids)} missing ===")

            # Fetch transcripts and their summaries in bulk
            result = await db.execute(
                select(Transcript).where(Transcript.id.in_(missing_tids))
            )
            transcripts = {t.id: t for t in result.scalars().all()}

            # Get summary content for these transcripts
            result = await db.execute(
                select(Summary).where(Summary.transcript_id.in_(missing_tids))
            )
            summaries_by_tid = {s.transcript_id: s for s in result.scalars().all()}

            created_count = 0

            for tid in missing_tids:
                t = transcripts.get(tid)
                if not t:
                    print(f"  Transcript {tid} not found, skipping")
                    continue

                summary = summaries_by_tid.get(tid)

                if summary and summary.content:
                    title = extract_title(summary.content)
                    key_points = extract_key_points(summary.content)
                    content = build_content(title, key_points)
                else:
                    # No summary content available — use transcript title
                    content = f"**{t.title or 'Meeting'}** — Transcript linked to this project."

                # Determine relevance based on primary_project_id
                if t.primary_project_id == project.id:
                    relevance = "HIGH"
                else:
                    relevance = "MEDIUM"

                ps = ProjectSummary(
                    project_id=project.id,
                    transcript_id=tid,
                    date=t.meeting_date,
                    relevance=relevance,
                    content=content,
                    source_file=t.filename,
                )
                db.add(ps)
                created_count += 1
                print(f"  Created: TID={tid} date={t.meeting_date} [{relevance}] ({len(content)} chars)")

            await db.commit()
            total_created += created_count
            print(f"  → {created_count} entries created for {project.name}")

        print(f"\n=== Done! Created {total_created} ProjectSummary entries total ===")


if __name__ == "__main__":
    asyncio.run(main())
