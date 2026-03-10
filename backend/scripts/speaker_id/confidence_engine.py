"""Stage 5: Bayesian confidence aggregation — combine multiple signals."""

from __future__ import annotations

import math
from collections import defaultdict

from .config import CONFIDENCE_THRESHOLD, SIGNAL_CORRELATIONS
from .models import (
    Identification, IdentificationMethod, TranscriptAnalysis,
    SpeakerMapping,
)


def _get_correlation(method_a: str, method_b: str) -> float:
    """Get correlation between two identification methods."""
    key1 = (method_a, method_b)
    key2 = (method_b, method_a)
    return SIGNAL_CORRELATIONS.get(key1, SIGNAL_CORRELATIONS.get(key2, 0.0))


def _discount_correlated_confidence(confidences: list[tuple[str, float]]) -> float:
    """Combine confidences with correlation discounting.

    Uses Bayesian updating but discounts correlated signals to avoid
    double-counting evidence.
    """
    if not confidences:
        return 0.0

    if len(confidences) == 1:
        return confidences[0][1]

    # Sort by confidence (highest first — primary signal)
    sorted_confs = sorted(confidences, key=lambda x: -x[1])

    # Start with highest confidence signal
    posterior = sorted_confs[0][1]

    # Update with each additional signal
    for i in range(1, len(sorted_confs)):
        method_i = sorted_confs[i][0]
        conf_i = sorted_confs[i][1]

        # Find max correlation with any previous signal
        max_corr = 0.0
        for j in range(i):
            method_j = sorted_confs[j][0]
            corr = _get_correlation(method_i, method_j)
            max_corr = max(max_corr, corr)

        # Discount the new signal by correlation
        effective_conf = conf_i * (1.0 - max_corr)

        # Bayesian update
        if effective_conf > 0:
            # P(identity | evidence) via Bayes
            likelihood = effective_conf
            posterior = (likelihood * posterior) / (
                likelihood * posterior + (1 - likelihood) * (1 - posterior)
            )

    return min(posterior, 0.99)


def aggregate_identifications(analysis: TranscriptAnalysis) -> TranscriptAnalysis:
    """Aggregate multiple identifications per label into best candidates.

    For each unknown label, if multiple methods identified it as the same person,
    combine their confidence using Bayesian aggregation.
    If different methods disagree, pick the one with highest aggregated confidence.
    """
    # Group identifications by label
    label_idents: dict[str, list[Identification]] = defaultdict(list)
    for ident in analysis.identifications:
        label_idents[ident.speaker_label].append(ident)

    # Process each label
    final_idents: list[Identification] = []

    for label, idents in label_idents.items():
        if label == "Unknown Speaker":
            # For Unknown Speaker, group by timestamp (each instance independent)
            ts_groups: dict[str, list[Identification]] = defaultdict(list)
            for ident in idents:
                ts_groups[ident.timestamp].append(ident)

            for ts, ts_idents in ts_groups.items():
                best = _pick_best_for_group(ts_idents)
                if best:
                    final_idents.append(best)
        else:
            # For "Speaker N", all identifications refer to the same person
            best = _pick_best_for_group(idents)
            if best:
                final_idents.append(best)

    analysis.identifications = final_idents
    return analysis


def _pick_best_for_group(idents: list[Identification]) -> Identification | None:
    """Pick the best identification from a group of signals for the same label."""
    if not idents:
        return None

    if len(idents) == 1:
        return idents[0]

    # Group by identified_as (candidate name)
    candidate_signals: dict[str, list[tuple[str, float]]] = defaultdict(list)
    candidate_idents: dict[str, list[Identification]] = defaultdict(list)

    for ident in idents:
        candidate_signals[ident.identified_as].append(
            (ident.method.value, ident.confidence)
        )
        candidate_idents[ident.identified_as].append(ident)

    # Compute aggregated confidence per candidate
    candidate_scores: dict[str, float] = {}
    for candidate, signals in candidate_signals.items():
        candidate_scores[candidate] = _discount_correlated_confidence(signals)

    # Pick the best candidate
    best_candidate = max(candidate_scores, key=candidate_scores.get)
    best_score = candidate_scores[best_candidate]

    # Find the primary identification (highest individual confidence)
    best_ident = max(
        candidate_idents[best_candidate],
        key=lambda i: i.confidence
    )

    # Create aggregated identification
    methods_used = [i.method.value for i in candidate_idents[best_candidate]]
    all_evidence = "; ".join(i.evidence for i in candidate_idents[best_candidate])

    return Identification(
        speaker_label=best_ident.speaker_label,
        identified_as=best_candidate,
        method=IdentificationMethod.BAYESIAN_AGGREGATE
               if len(candidate_idents[best_candidate]) > 1
               else best_ident.method,
        confidence=best_score,
        evidence=all_evidence if len(candidate_idents[best_candidate]) > 1
                 else best_ident.evidence,
        line_number=best_ident.line_number,
        timestamp=best_ident.timestamp,
        supporting_signals=methods_used,
    )


def build_final_mapping(analysis: TranscriptAnalysis) -> SpeakerMapping:
    """Convert analysis into a final SpeakerMapping ready for application."""
    mapping = SpeakerMapping(filename=analysis.filename)

    for ident in analysis.identifications:
        label = ident.speaker_label
        entry = {
            "identified_as": ident.identified_as,
            "confidence": round(ident.confidence, 3),
            "method": ident.method.value,
            "evidence": ident.evidence,
            "supporting_signals": ident.supporting_signals,
        }

        if label == "Unknown Speaker":
            # Instance-specific: key by timestamp
            if label not in mapping.mappings:
                mapping.mappings[label] = {"instances": {}}
            mapping.mappings[label]["instances"][ident.timestamp] = entry
        else:
            mapping.mappings[label] = entry

        # Flag for review if below threshold
        if ident.confidence < CONFIDENCE_THRESHOLD:
            flag_key = f"{label}@{ident.timestamp}" if label == "Unknown Speaker" else label
            mapping.flagged_for_review.append(flag_key)

    mapping.unresolved = analysis.unresolved
    return mapping
