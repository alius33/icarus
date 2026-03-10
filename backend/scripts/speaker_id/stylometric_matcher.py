"""Stage 4: Stylometric matching — compare unknown speakers against profiles."""

from __future__ import annotations

import math
import re
from collections import Counter

from .config import FILLERS, TECHNICAL_TERMS, resolve_name
from .models import (
    Identification, IdentificationMethod, SpeakerProfile,
    SpeakerSegment, TranscriptAnalysis,
)


def _tokenize(text: str) -> list[str]:
    return re.findall(r'\b[a-zA-Z\']+\b', text.lower())


def _compute_filler_frequencies(text: str, total_words: int) -> dict[str, float]:
    """Compute filler word frequencies per 1000 words."""
    freqs = {}
    for category, filler_list in FILLERS.items():
        count = 0
        for filler in filler_list:
            count += len(re.findall(
                r'\b' + re.escape(filler) + r'\b', text, re.IGNORECASE
            ))
        freqs[category] = (count / max(total_words, 1)) * 1000
    return freqs


def _compute_discourse_frequencies(text: str, total_words: int) -> dict[str, float]:
    """Compute individual discourse marker frequencies per 1000 words."""
    markers = ["so", "well", "like", "basically", "actually",
               "obviously", "honestly", "literally"]
    freqs = {}
    for marker in markers:
        count = len(re.findall(r'\b' + marker + r'\b', text, re.IGNORECASE))
        freqs[marker] = (count / max(total_words, 1)) * 1000
    return freqs


def _compute_formality(text: str) -> float:
    informal = len(re.findall(
        r'\b(gonna|wanna|gotta|kinda|sorta|bro|dude|mate|guys|yeah|yep|nah|nope)\b',
        text, re.IGNORECASE
    ))
    informal += len(re.findall(r"n't\b", text))
    formal = len(re.findall(
        r'\b(furthermore|therefore|consequently|however|regarding|concerning|shall|ought)\b',
        text, re.IGNORECASE
    ))
    total = informal + formal
    return formal / total if total > 0 else 0.5


def _compute_tech_density(text: str, total_words: int) -> float:
    tech_count = 0
    text_lower = text.lower()
    for domain_terms in TECHNICAL_TERMS.values():
        for term in domain_terms:
            tech_count += len(re.findall(r'\b' + re.escape(term) + r'\b', text_lower))
    return tech_count / max(total_words, 1)


def extract_features(text: str) -> dict[str, float]:
    """Extract stylometric feature vector from text."""
    words = _tokenize(text)
    total = len(words)

    if total < 10:
        return {}

    word_counts = Counter(words)

    # Lexical
    features: dict[str, float] = {
        "avg_word_length": sum(len(w) for w in words) / total,
        "type_token_ratio": len(word_counts) / total,
        "vocab_size_norm": min(len(word_counts) / 100, 1.0),
    }

    # Filler frequencies
    filler_freqs = _compute_filler_frequencies(text, total)
    for cat, freq in filler_freqs.items():
        features[f"filler_{cat}"] = freq

    # Discourse markers
    discourse_freqs = _compute_discourse_frequencies(text, total)
    for marker, freq in discourse_freqs.items():
        features[f"discourse_{marker}"] = freq

    # Syntactic
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s for s in sentences if s.strip()]
    if sentences:
        sent_lengths = [len(s.split()) for s in sentences]
        features["avg_sentence_length"] = sum(sent_lengths) / len(sent_lengths)
        questions = sum(1 for s in sentences if s.strip().endswith("?"))
        features["question_ratio"] = questions / len(sentences)

    # Style
    features["formality_score"] = _compute_formality(text)
    features["technical_density"] = _compute_tech_density(text, total)

    # Hedge/assertiveness
    hedge_count = 0
    for phrase in FILLERS["hedge"]:
        hedge_count += len(re.findall(re.escape(phrase), text, re.IGNORECASE))
    features["hedge_ratio"] = (hedge_count / max(total / 1000, 0.1))

    assert_count = 0
    for phrase in FILLERS["assertive"]:
        assert_count += len(re.findall(
            r'\b' + re.escape(phrase) + r'\b', text, re.IGNORECASE
        ))
    features["assertiveness"] = (assert_count / max(total / 1000, 0.1))

    return features


def _profile_to_features(profile: SpeakerProfile) -> dict[str, float]:
    """Convert a speaker profile to a comparable feature vector."""
    features: dict[str, float] = {}

    if profile.total_words < 50:
        return features

    features["avg_word_length"] = 4.5  # Approximate — not stored directly
    features["type_token_ratio"] = profile.type_token_ratio
    features["vocab_size_norm"] = min(profile.vocabulary_size / 100, 1.0)

    for cat, freq in profile.filler_frequencies.items():
        features[f"filler_{cat}"] = freq

    for marker, freq in profile.discourse_markers.items():
        features[f"discourse_{marker}"] = freq

    features["avg_sentence_length"] = profile.avg_sentence_length
    features["question_ratio"] = profile.question_ratio
    features["formality_score"] = profile.formality_score
    features["technical_density"] = profile.technical_density
    features["hedge_ratio"] = profile.hedge_ratio
    features["assertiveness"] = profile.assertiveness_ratio

    return features


# Feature weights — higher = more discriminative
FEATURE_WEIGHTS: dict[str, float] = {
    "filler_hesitation": 2.0,
    "filler_affirmative": 1.5,
    "filler_discourse": 2.0,
    "filler_hedge": 2.0,
    "filler_assertive": 2.0,
    "filler_tag_questions": 2.5,
    "filler_connective": 1.5,
    "discourse_so": 1.5,
    "discourse_well": 1.5,
    "discourse_like": 2.0,
    "discourse_basically": 2.5,
    "discourse_actually": 1.5,
    "discourse_obviously": 2.5,
    "discourse_honestly": 2.0,
    "discourse_literally": 2.0,
    "formality_score": 1.5,
    "technical_density": 1.5,
    "question_ratio": 1.0,
    "avg_sentence_length": 0.8,
    "type_token_ratio": 0.5,
    "hedge_ratio": 1.5,
    "assertiveness": 1.5,
}


def compute_stylometric_distance(unknown_features: dict[str, float],
                                 profile_features: dict[str, float]) -> float:
    """Compute weighted distance between unknown speaker and profile.

    Lower distance = more similar. Uses modified Burrows' Delta with
    feature-specific weights.
    """
    if not unknown_features or not profile_features:
        return float('inf')

    # Common features only
    common = set(unknown_features.keys()) & set(profile_features.keys())
    if len(common) < 3:
        return float('inf')

    total_distance = 0.0
    total_weight = 0.0

    for feat in common:
        weight = 1.0
        for pattern, w in FEATURE_WEIGHTS.items():
            if feat == pattern or (pattern.endswith('*') and
                                    feat.startswith(pattern[:-1])):
                weight = w
                break

        diff = abs(unknown_features[feat] - profile_features[feat])
        # Normalize by max of the two values to avoid scale issues
        scale = max(abs(unknown_features[feat]), abs(profile_features[feat]), 0.01)
        normalized_diff = diff / scale

        total_distance += weight * normalized_diff
        total_weight += weight

    return total_distance / max(total_weight, 1.0)


def run_stylometric_matching(analysis: TranscriptAnalysis,
                             segments: list[SpeakerSegment],
                             profiles: dict[str, SpeakerProfile]) -> None:
    """Match unresolved unknown speakers against speaker profiles."""
    if not profiles:
        return

    # Pre-compute profile features
    profile_features: dict[str, dict[str, float]] = {}
    for name, profile in profiles.items():
        feats = _profile_to_features(profile)
        if feats:
            profile_features[name] = feats

    if not profile_features:
        return

    for label in analysis.unknown_labels:
        if label in analysis.get_identified_labels():
            continue

        # Combine all text from this speaker
        combined = " ".join(s.text for s in segments if s.label == label and s.text)
        word_count = len(combined.split())

        # Minimum text thresholds
        if word_count < 50:
            continue  # Not enough text for stylometric analysis

        # Confidence cap based on text amount
        if word_count < 100:
            max_confidence = 0.55
        elif word_count < 200:
            max_confidence = 0.65
        elif word_count < 500:
            max_confidence = 0.75
        else:
            max_confidence = 0.85

        unknown_features = extract_features(combined)
        if not unknown_features:
            continue

        # Compute distances to all profiles
        distances: dict[str, float] = {}
        for name, pfeats in profile_features.items():
            # Skip if already a known speaker in this transcript
            canonical_known = {resolve_name(k) or k for k in analysis.known_speakers}
            if name in canonical_known:
                continue

            # Skip excluded names
            excluded = set(analysis.exclusions.get(label, []))
            if name in excluded:
                continue

            dist = compute_stylometric_distance(unknown_features, pfeats)
            if dist < float('inf'):
                distances[name] = dist

        if not distances:
            continue

        # Best match (lowest distance)
        best_name = min(distances, key=distances.get)
        best_dist = distances[best_name]

        # Convert distance to confidence
        # Distance of 0 = perfect match → confidence = max_confidence
        # Distance of 1+ = poor match → low confidence
        raw_confidence = max(0, 1.0 - best_dist)
        confidence = min(raw_confidence * max_confidence, max_confidence)

        # Only report if meaningful
        if confidence >= 0.40:
            # Check if this is the clear winner (gap to second place)
            sorted_dists = sorted(distances.values())
            if len(sorted_dists) > 1:
                gap = sorted_dists[1] - sorted_dists[0]
                if gap > 0.1:
                    confidence = min(confidence + 0.05, max_confidence)

            first_seg = next((s for s in segments if s.label == label), None)
            if first_seg:
                analysis.add_identification(Identification(
                    speaker_label=label,
                    identified_as=best_name,
                    method=IdentificationMethod.STYLOMETRIC_MATCH,
                    confidence=confidence,
                    evidence=f"Stylometric match to {best_name} "
                             f"(distance: {best_dist:.3f}, "
                             f"word count: {word_count})",
                    line_number=first_seg.line_number,
                    timestamp=first_seg.timestamp,
                ))
