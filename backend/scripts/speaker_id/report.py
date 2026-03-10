"""Generate mapping JSON and human-readable review reports."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .config import CONFIDENCE_THRESHOLD
from .models import PipelineResult, SpeakerMapping, TranscriptAnalysis


def build_pipeline_result(analyses: dict[str, TranscriptAnalysis],
                          mappings: dict[str, SpeakerMapping],
                          profiles_count: int) -> PipelineResult:
    """Build complete pipeline result from all analyses."""
    result = PipelineResult()
    result.generated_at = datetime.now(timezone.utc).isoformat()
    result.profiles_used = profiles_count

    total_unknown = 0
    total_identified_high = 0
    total_identified_medium = 0
    total_flagged = 0
    total_unresolved = 0
    transcripts_with_unknowns = 0

    for filename, analysis in analyses.items():
        mapping = mappings.get(filename)
        if not mapping:
            continue

        if analysis.unknown_labels:
            transcripts_with_unknowns += 1

        # Count from identifications
        for ident in analysis.identifications:
            if ident.confidence >= 0.85:
                total_identified_high += 1
            elif ident.confidence >= CONFIDENCE_THRESHOLD:
                total_identified_medium += 1
            else:
                total_flagged += 1

        total_unknown += analysis.total_unknown_segments
        total_unresolved += len(analysis.unresolved)

        # Build transcript entry
        result.transcript_results[filename] = {
            "meeting_type": analysis.meeting_type,
            "known_speakers": analysis.known_speakers,
            "title_candidates": analysis.title_candidates,
            "mappings": mapping.mappings,
            "flagged_for_review": mapping.flagged_for_review,
            "unresolved": mapping.unresolved,
        }

    result.summary = {
        "total_transcripts": len(analyses),
        "transcripts_with_unknowns": transcripts_with_unknowns,
        "total_unknown_instances": total_unknown,
        "identified_high_confidence": total_identified_high,
        "identified_medium_confidence": total_identified_medium,
        "flagged_for_review": total_flagged,
        "unresolved": total_unresolved,
    }

    return result


def generate_review_report(analyses: dict[str, TranscriptAnalysis],
                           mappings: dict[str, SpeakerMapping]) -> str:
    """Generate human-readable Markdown review report."""
    lines = []
    lines.append("# Speaker Identification Review Report")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    # Summary
    total_files = len(analyses)
    files_with_unknowns = sum(
        1 for a in analyses.values() if a.unknown_labels
    )
    total_idents = sum(
        len(a.identifications) for a in analyses.values()
    )
    total_unresolved = sum(
        len(a.unresolved) for a in analyses.values()
    )
    total_flagged = sum(
        len(m.flagged_for_review) for m in mappings.values()
    )

    lines.append("## Summary")
    lines.append(f"- **Total transcripts analyzed:** {total_files}")
    lines.append(f"- **Transcripts with unknowns:** {files_with_unknowns}")
    lines.append(f"- **Total identifications made:** {total_idents}")
    lines.append(f"- **Flagged for review:** {total_flagged}")
    lines.append(f"- **Still unresolved:** {total_unresolved}")
    lines.append("")

    # High-confidence identifications
    lines.append("## High Confidence Identifications (>= 0.85)")
    lines.append("")
    high_conf = []
    for filename, analysis in sorted(analyses.items()):
        for ident in analysis.identifications:
            if ident.confidence >= 0.85:
                high_conf.append((filename, ident))

    if high_conf:
        lines.append("| Transcript | Label | Identified As | Confidence | Method |")
        lines.append("|-----------|-------|---------------|------------|--------|")
        for filename, ident in high_conf:
            lines.append(
                f"| {_short_name(filename)} | {ident.speaker_label} | "
                f"**{ident.identified_as}** | {ident.confidence:.2f} | "
                f"{ident.method.value} |"
            )
    else:
        lines.append("*None*")
    lines.append("")

    # Flagged for review
    lines.append("## Flagged for Review (confidence < 0.70)")
    lines.append("")
    for filename, analysis in sorted(analyses.items()):
        flagged_idents = [
            i for i in analysis.identifications if i.confidence < CONFIDENCE_THRESHOLD
        ]
        if not flagged_idents:
            continue

        lines.append(f"### {_short_name(filename)}")
        lines.append(f"Meeting type: {analysis.meeting_type} | "
                     f"Known: {', '.join(analysis.known_speakers)}")
        lines.append("")

        for ident in flagged_idents:
            emoji = "⚠️" if ident.confidence >= 0.50 else "❓"
            lines.append(
                f"**{ident.speaker_label}** → {ident.identified_as} "
                f"(confidence: {ident.confidence:.2f}) {emoji}"
            )
            lines.append(f"  - Evidence: {ident.evidence}")
            if ident.supporting_signals:
                lines.append(f"  - Signals: {', '.join(ident.supporting_signals)}")
            lines.append("")

    # Unresolved
    lines.append("## Unresolved Speakers")
    lines.append("")
    for filename, analysis in sorted(analyses.items()):
        if not analysis.unresolved:
            continue
        lines.append(f"### {_short_name(filename)}")
        lines.append(f"Meeting type: {analysis.meeting_type} | "
                     f"Known: {', '.join(analysis.known_speakers)}")
        lines.append(f"Unresolved labels: {', '.join(analysis.unresolved)}")
        if analysis.title_candidates:
            lines.append(f"Title candidates: {', '.join(analysis.title_candidates)}")
        lines.append("")

    # Statistics by method
    lines.append("## Identification Methods Used")
    lines.append("")
    method_counts: dict[str, int] = {}
    for analysis in analyses.values():
        for ident in analysis.identifications:
            method = ident.method.value
            method_counts[method] = method_counts.get(method, 0) + 1

    lines.append("| Method | Count |")
    lines.append("|--------|-------|")
    for method, count in sorted(method_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {method} | {count} |")
    lines.append("")

    return "\n".join(lines)


def _short_name(filename: str) -> str:
    """Shorten filename for display."""
    name = filename.replace('.txt', '')
    if len(name) > 60:
        return name[:57] + "..."
    return name
