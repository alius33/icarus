"""Data models for the speaker identification pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any


class IdentificationMethod(Enum):
    TITLE_PARSE = "title_parse"
    SELF_INTRODUCTION = "self_introduction"
    GREETING_EXCHANGE = "greeting_exchange"
    DIRECT_ADDRESS = "direct_address"
    ELIMINATION = "elimination"
    CROSS_REFERENCE = "cross_reference"
    NAMED_MENTION = "named_mention"
    AZMAIN_RECORDER = "azmain_recorder"
    CONVERSATION_ROLE = "conversation_role"
    STYLOMETRIC_MATCH = "stylometric_match"
    BAYESIAN_AGGREGATE = "bayesian_aggregate"
    CLAUDE_ASSISTED = "claude_assisted"
    MANUAL = "manual"


@dataclass
class SpeakerSegment:
    """A single speaking turn in a transcript."""
    label: str              # "Azmain Hossain" or "Speaker 1"
    timestamp: str          # "0:52"
    timestamp_seconds: int  # 52
    text: str               # Everything until next speaker line
    line_number: int        # Line in file where label appears
    word_count: int         # Words in this segment
    is_unidentified: bool   # True for "Speaker N" / "Unknown Speaker"
    segment_index: int      # Position in conversation (0, 1, 2, ...)


@dataclass
class Identification:
    """A single speaker identification result."""
    speaker_label: str           # "Speaker 1" or "Unknown Speaker"
    identified_as: str           # "Richard Dosoo"
    method: IdentificationMethod
    confidence: float            # 0.0 - 1.0
    evidence: str                # Human-readable explanation
    line_number: int             # First line where this label appears
    timestamp: str               # Original timestamp
    supporting_signals: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "speaker_label": self.speaker_label,
            "identified_as": self.identified_as,
            "method": self.method.value,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "line_number": self.line_number,
            "timestamp": self.timestamp,
            "supporting_signals": self.supporting_signals,
        }


@dataclass
class ConversationRole:
    """Conversation structure features for a speaker."""
    degree_centrality: float = 0.0
    betweenness_centrality: float = 0.0
    in_degree: float = 0.0
    out_degree: float = 0.0
    is_likely_facilitator: bool = False
    is_likely_presenter: bool = False
    is_likely_questioner: bool = False
    is_likely_passive: bool = False
    speaks_first: bool = False
    speaks_last: bool = False
    segment_count: int = 0
    total_words: int = 0
    avg_segment_length: float = 0.0
    question_ratio: float = 0.0
    primary_interlocutor: str | None = None
    response_to_pattern: dict[str, int] = field(default_factory=dict)
    responded_to_by: dict[str, int] = field(default_factory=dict)


@dataclass
class TranscriptAnalysis:
    """Full analysis result for a single transcript."""
    filename: str
    filepath: str
    title: str
    meeting_type: str = "unknown"
    known_speakers: list[str] = field(default_factory=list)
    unknown_labels: list[str] = field(default_factory=list)
    total_segments: int = 0
    total_unknown_segments: int = 0
    identifications: list[Identification] = field(default_factory=list)
    exclusions: dict[str, list[str]] = field(default_factory=dict)
    unresolved: list[str] = field(default_factory=list)
    conversation_roles: dict[str, ConversationRole] = field(default_factory=dict)
    title_candidates: list[str] = field(default_factory=list)

    def get_identified_labels(self) -> set[str]:
        """Return set of labels that have been identified."""
        return {i.speaker_label for i in self.identifications}

    def get_best_identification(self, label: str) -> Identification | None:
        """Get the highest-confidence identification for a label."""
        matches = [i for i in self.identifications if i.speaker_label == label]
        if not matches:
            return None
        return max(matches, key=lambda x: x.confidence)

    def add_identification(self, ident: Identification) -> None:
        """Add an identification, checking for consistency."""
        self.identifications.append(ident)

    def to_dict(self) -> dict:
        return {
            "filename": self.filename,
            "title": self.title,
            "meeting_type": self.meeting_type,
            "known_speakers": self.known_speakers,
            "unknown_labels": self.unknown_labels,
            "total_segments": self.total_segments,
            "total_unknown_segments": self.total_unknown_segments,
            "identifications": [i.to_dict() for i in self.identifications],
            "unresolved": self.unresolved,
            "title_candidates": self.title_candidates,
        }


@dataclass
class SpeakerProfile:
    """Persistent profile built from all named segments across transcripts."""
    canonical_name: str
    aliases: list[str] = field(default_factory=list)

    # Volume
    total_segments: int = 0
    total_words: int = 0
    transcripts_appeared_in: int = 0
    transcript_list: list[str] = field(default_factory=list)
    avg_segment_length: float = 0.0
    segment_length_std: float = 0.0

    # Vocabulary
    vocabulary_size: int = 0
    type_token_ratio: float = 0.0
    top_words: dict[str, float] = field(default_factory=dict)

    # Filler word signature (per 1000 words)
    filler_frequencies: dict[str, float] = field(default_factory=dict)

    # Discourse markers (per 1000 words)
    discourse_markers: dict[str, float] = field(default_factory=dict)

    # Signature phrases
    signature_phrases: list[str] = field(default_factory=list)
    phrase_frequencies: dict[str, float] = field(default_factory=dict)

    # Syntactic
    avg_sentence_length: float = 0.0
    question_ratio: float = 0.0
    exclamation_ratio: float = 0.0

    # Style
    formality_score: float = 0.5
    technical_density: float = 0.0
    hedge_ratio: float = 0.0
    assertiveness_ratio: float = 0.0

    # Greeting patterns
    greeting_patterns: list[str] = field(default_factory=list)

    # Meeting role
    opens_meetings: float = 0.0
    closes_meetings: float = 0.0
    facilitator_score: float = 0.0

    # Gender
    gender: str | None = None  # "M", "F", or None

    # Co-occurrence
    co_speakers: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> SpeakerProfile:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class SpeakerMapping:
    """Final output: complete mapping for a transcript."""
    filename: str
    mappings: dict[str, dict] = field(default_factory=dict)
    flagged_for_review: list[str] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "filename": self.filename,
            "mappings": self.mappings,
            "flagged_for_review": self.flagged_for_review,
            "unresolved": self.unresolved,
        }


@dataclass
class PipelineResult:
    """Complete result of the speaker identification pipeline."""
    generated_at: str = ""
    pipeline_version: str = "1.0"
    confidence_threshold: float = 0.7
    profiles_used: int = 0
    transcript_results: dict[str, dict] = field(default_factory=dict)
    summary: dict[str, int] = field(default_factory=dict)

    def to_json(self, path: Path) -> None:
        data = {
            "generated_at": self.generated_at,
            "pipeline_version": self.pipeline_version,
            "confidence_threshold": self.confidence_threshold,
            "profiles_used": self.profiles_used,
            "transcripts": self.transcript_results,
            "summary": self.summary,
        }
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def from_json(cls, path: Path) -> PipelineResult:
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            generated_at=data.get("generated_at", ""),
            pipeline_version=data.get("pipeline_version", "1.0"),
            confidence_threshold=data.get("confidence_threshold", 0.7),
            profiles_used=data.get("profiles_used", 0),
            transcript_results=data.get("transcripts", {}),
            summary=data.get("summary", {}),
        )
