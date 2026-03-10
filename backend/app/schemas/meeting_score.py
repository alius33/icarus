from pydantic import BaseModel


class MeetingScoreBase(BaseModel):
    id: int
    transcript_id: int
    date: str | None = None
    meeting_title: str | None = None
    meeting_type: str | None = None
    overall_score: int
    decision_velocity: float | None = None
    action_clarity: float | None = None
    engagement_balance: float | None = None
    topic_completion: float | None = None
    follow_through: float | None = None
    participant_count: int | None = None
    duration_category: str | None = None
    recommendations: str | None = None
    is_manual: bool = False


class MeetingScoreCreate(BaseModel):
    transcript_id: int
    date: str | None = None
    meeting_title: str | None = None
    meeting_type: str | None = None
    overall_score: int
    decision_velocity: float | None = None
    action_clarity: float | None = None
    engagement_balance: float | None = None
    topic_completion: float | None = None
    follow_through: float | None = None
    participant_count: int | None = None
    duration_category: str | None = None
    recommendations: str | None = None


class MeetingScoreUpdate(BaseModel):
    transcript_id: int | None = None
    date: str | None = None
    meeting_title: str | None = None
    meeting_type: str | None = None
    overall_score: int | None = None
    decision_velocity: float | None = None
    action_clarity: float | None = None
    engagement_balance: float | None = None
    topic_completion: float | None = None
    follow_through: float | None = None
    participant_count: int | None = None
    duration_category: str | None = None
    recommendations: str | None = None


class MeetingScoreTrend(BaseModel):
    date: str
    score: int
    meeting_type: str | None = None
