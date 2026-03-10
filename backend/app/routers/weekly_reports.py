from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.weekly_report import WeeklyReport
from app.schemas.weekly_report import WeeklyReportBase, WeeklyReportDetail

router = APIRouter(tags=["weekly_reports"])


def _report_base(r: WeeklyReport) -> WeeklyReportBase:
    return WeeklyReportBase(
        id=r.id,
        title=r.title,
        week_start=str(r.week_start) if r.week_start else "",
        week_end=str(r.week_end) if r.week_end else "",
        period_label=None,
    )


@router.get("/weekly-reports", response_model=list[WeeklyReportBase])
async def list_weekly_reports(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(WeeklyReport).order_by(desc(WeeklyReport.week_start))
    )
    reports = result.scalars().all()

    return [_report_base(r) for r in reports]


@router.get("/weekly-reports/{report_id}", response_model=WeeklyReportDetail)
async def get_weekly_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(WeeklyReport).where(WeeklyReport.id == report_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise NotFoundError("Weekly report", report_id)

    return WeeklyReportDetail(
        id=report.id,
        title=report.title,
        week_start=str(report.week_start) if report.week_start else "",
        week_end=str(report.week_end) if report.week_end else "",
        period_label=None,
        content=report.content,
        workstream_updates=[],
        highlights=[],
        risks=[],
    )
