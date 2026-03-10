"""Pydantic schemas for speaker identification review endpoints."""

from __future__ import annotations

from pydantic import BaseModel


class ReviewSummary(BaseModel):
    total_transcripts: int
    total_identifications: int
    applied_count: int
    flagged_count: int
    unresolved_count: int
    methods: dict[str, int]


class SpeakerReviewItem(BaseModel):
    id: str  # "{filename}::{label}::{timestamp}"
    transcript_filename: str
    meeting_type: str
    known_speakers: list[str]
    speaker_label: str
    timestamp: str
    identified_as: str
    confidence: float
    method: str
    evidence: str
    status: str  # "applied" | "flagged" | "unresolved"


class SpeakerReviewResponse(BaseModel):
    summary: ReviewSummary
    items: list[SpeakerReviewItem]
    stakeholder_names: list[str]


class ConfirmAction(BaseModel):
    id: str
    action: str  # "accept" | "reject" | "manual"
    manual_name: str | None = None


class ConfirmRequest(BaseModel):
    actions: list[ConfirmAction]


class ConfirmResponse(BaseModel):
    applied: int
    rejected: int
    errors: list[str]


class TranscriptContext(BaseModel):
    filename: str
    lines: list[str]
    highlight_line: int
