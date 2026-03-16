from app.models.task import Task

# Backward compatibility alias
ActionItem = Task
from app.models.adoption_metric import AdoptionMetric
from app.models.commitment import Commitment
from app.models.contradiction import Contradiction
from app.models.cross_project_link import CrossProjectLink
from app.models.decision import Decision
from app.models.deleted_import import DeletedImport
from app.models.dependency import Dependency
from app.models.division_profile import DivisionProfile
from app.models.document import Document
from app.models.glossary import GlossaryEntry
from app.models.influence_signal import InfluenceSignal
from app.models.meeting_score import MeetingScore
from app.models.open_thread import OpenThread
from app.models.outreach import Outreach
from app.models.outreach_link import OutreachLink
from app.models.programme_win import ProgrammeWin
from app.models.project import Project
from app.models.project_link import ProjectLink
from app.models.project_summary import ProjectSummary
from app.models.resource_allocation import ResourceAllocation
from app.models.risk_entry import RiskEntry
from app.models.scope_item import ScopeItem
from app.models.sentiment_signal import SentimentSignal
from app.models.stakeholder import Stakeholder
from app.models.summary import Summary
from app.models.topic_signal import TopicSignal
from app.models.transcript import Transcript
from app.models.transcript_attachment import TranscriptAttachment
from app.models.transcript_mention import TranscriptMention
from app.models.transcript_note import TranscriptNote
from app.models.weekly_report import WeeklyReport
from app.models.programme_deliverable import ProgrammeDeliverable
from app.models.project_update import ProjectUpdate
from app.models.deliverable_milestone import DeliverableMilestone
from app.models.weekly_plan import WeeklyPlan
from app.models.weekly_plan_action import WeeklyPlanAction
from app.models.deliverable_progress_snapshot import DeliverableProgressSnapshot

__all__ = [
    "Transcript", "Summary", "WeeklyReport",
    "Stakeholder", "Decision", "OpenThread",
    "Task", "ActionItem", "GlossaryEntry", "TranscriptMention",
    "Document", "Project", "ProjectLink", "DeletedImport",
    "Dependency", "ResourceAllocation", "ScopeItem",
    "ProgrammeWin", "AdoptionMetric", "Outreach", "OutreachLink", "DivisionProfile",
    "SentimentSignal", "Commitment", "CrossProjectLink",
    "TopicSignal", "InfluenceSignal", "Contradiction",
    "MeetingScore", "RiskEntry", "ProjectSummary",
    "TranscriptNote", "TranscriptAttachment",
    "ProgrammeDeliverable", "DeliverableMilestone",
    "WeeklyPlan", "WeeklyPlanAction", "DeliverableProgressSnapshot",
    "ProjectUpdate",
]
