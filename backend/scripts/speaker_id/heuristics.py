"""Stage 2: Deterministic heuristic strategies for speaker identification."""

from __future__ import annotations

import re
from collections import Counter

from .config import (
    STAKEHOLDER_ALIASES, TITLE_NAME_PATTERNS, AMBIGUOUS_NAMES,
    MEETING_TYPE_PATTERNS, MEETING_TYPE_ATTENDEES, ALWAYS_PRESENT,
    INTRO_PATTERNS, GREETING_PATTERNS, DIRECT_ADDRESS_PATTERNS,
    SPEECH_PATTERNS, TECHNICAL_TERMS, resolve_name,
)
from .models import (
    Identification, IdentificationMethod, TranscriptAnalysis,
    SpeakerSegment,
)
from .segment_parser import (
    parse_title_from_filename, get_known_speakers, get_unknown_labels,
    get_segments_by_label, get_combined_text, get_total_words,
)


def _detect_meeting_type(title: str) -> str:
    """Classify meeting type from title."""
    for pattern, mtype in MEETING_TYPE_PATTERNS:
        if re.search(pattern, title):
            return mtype
    return "unknown"


def _extract_title_candidates(title: str) -> list[str]:
    """Extract stakeholder names from meeting title."""
    candidates = []
    seen = set()

    for pattern, canonical in TITLE_NAME_PATTERNS:
        if re.search(pattern, title):
            if canonical not in seen:
                candidates.append(canonical)
                seen.add(canonical)

    # Handle ambiguous "Ben" — if title has "Ben" but no qualifier
    if "Ben" in title and "Ben Brooks" not in seen and "Ben Van Houten" not in seen:
        # Check for infrastructure context
        if re.search(r'(?i)aws|deploy|cicd|infrastructure|env|phantom', title):
            if "Ben Van Houten" not in seen:
                candidates.append("Ben Van Houten")
                seen.add("Ben Van Houten")
        else:
            if "Ben Brooks" not in seen:
                candidates.append("Ben Brooks")
                seen.add("Ben Brooks")

    return candidates


def _name_matches_known(name: str) -> str | None:
    """Check if a name matches any known stakeholder. Returns canonical name or None."""
    canonical = resolve_name(name)
    if canonical:
        return canonical

    # Fuzzy match: try first name only
    first_name = name.split()[0] if name.split() else name
    canonical = resolve_name(first_name)
    return canonical


# ──────────────────────────────────────────────
# Strategy 1: Title Parsing
# ──────────────────────────────────────────────

def run_title_strategy(analysis: TranscriptAnalysis,
                       segments: list[SpeakerSegment]) -> None:
    """Extract names from title, record as candidates (not yet assigned)."""
    title = analysis.title
    candidates = _extract_title_candidates(title)
    analysis.title_candidates = candidates

    # For 1:1 meetings with a single title candidate and a single unknown label
    unknown_labels = analysis.unknown_labels
    known = set(analysis.known_speakers)

    # Filter candidates to only those NOT already in known speakers
    unmatched_candidates = []
    for c in candidates:
        # Check if candidate is already a known speaker (by canonical or alias)
        already_known = False
        for k in known:
            if resolve_name(k) == c or k == c:
                already_known = True
                break
        if not already_known:
            unmatched_candidates.append(c)

    # Simple case: 1 unmatched candidate, 1 unknown label (excluding "Unknown Speaker")
    numbered_unknowns = [l for l in unknown_labels if l != "Unknown Speaker"]
    if len(unmatched_candidates) == 1 and len(numbered_unknowns) == 1:
        label = numbered_unknowns[0]
        candidate = unmatched_candidates[0]
        analysis.add_identification(Identification(
            speaker_label=label,
            identified_as=candidate,
            method=IdentificationMethod.TITLE_PARSE,
            confidence=0.92,
            evidence=f"Title '{title}' contains '{candidate}', "
                     f"only 1 numbered unknown label",
            line_number=next(
                (s.line_number for s in segments if s.label == label), 0
            ),
            timestamp=next(
                (s.timestamp for s in segments if s.label == label), ""
            ),
        ))

    # Two unmatched candidates, two unknown labels
    elif len(unmatched_candidates) == 2 and len(numbered_unknowns) == 2:
        # Can't distinguish yet — record candidates for elimination stage
        pass

    # If there's also "Unknown Speaker" and exactly one unmatched candidate remains
    # after numbered unknowns are handled, assign it
    if "Unknown Speaker" in unknown_labels and len(unmatched_candidates) == 1:
        already_identified = analysis.get_identified_labels()
        if not any(l for l in numbered_unknowns if l not in already_identified):
            # All numbered unknowns handled, Unknown Speaker gets the candidate
            candidate = unmatched_candidates[0]
            first_us = next(
                (s for s in segments if s.label == "Unknown Speaker"), None
            )
            if first_us:
                analysis.add_identification(Identification(
                    speaker_label="Unknown Speaker",
                    identified_as=candidate,
                    method=IdentificationMethod.TITLE_PARSE,
                    confidence=0.75,
                    evidence=f"Title candidate '{candidate}' with Unknown Speaker",
                    line_number=first_us.line_number,
                    timestamp=first_us.timestamp,
                ))


# ──────────────────────────────────────────────
# Strategy 2: Self-Introduction Detection
# ──────────────────────────────────────────────

def run_self_intro_strategy(analysis: TranscriptAnalysis,
                            segments: list[SpeakerSegment]) -> None:
    """Detect self-introductions in unidentified speaker text."""
    for seg in segments:
        if not seg.is_unidentified or not seg.text:
            continue
        if seg.label in analysis.get_identified_labels():
            continue

        for pattern in INTRO_PATTERNS:
            matches = re.findall(pattern, seg.text)
            for name_match in matches:
                canonical = _name_matches_known(name_match)
                if canonical:
                    # Verify this person isn't already a known speaker
                    if canonical not in analysis.known_speakers and \
                       not any(resolve_name(k) == canonical
                               for k in analysis.known_speakers):
                        analysis.add_identification(Identification(
                            speaker_label=seg.label,
                            identified_as=canonical,
                            method=IdentificationMethod.SELF_INTRODUCTION,
                            confidence=0.97,
                            evidence=f"Self-intro detected: '{name_match}' "
                                     f"→ {canonical} at line {seg.line_number}",
                            line_number=seg.line_number,
                            timestamp=seg.timestamp,
                        ))
                        break
            else:
                continue
            break


# ──────────────────────────────────────────────
# Strategy 3: Greeting Exchange Detection
# ──────────────────────────────────────────────

def run_greeting_strategy(analysis: TranscriptAnalysis,
                          segments: list[SpeakerSegment]) -> None:
    """Detect named greetings and link to the next unknown speaker."""
    for i, seg in enumerate(segments):
        if not seg.text:
            continue

        for pattern in GREETING_PATTERNS:
            matches = re.findall(pattern, seg.text)
            for name_match in matches:
                canonical = _name_matches_known(name_match)
                if not canonical:
                    continue

                # Skip if this person is already a known speaker
                if canonical in analysis.known_speakers or \
                   any(resolve_name(k) == canonical for k in analysis.known_speakers):
                    continue

                # Look at next 1-3 segments for an unidentified response
                for j in range(i + 1, min(i + 4, len(segments))):
                    next_seg = segments[j]
                    if next_seg.is_unidentified and \
                       next_seg.label not in analysis.get_identified_labels():
                        # Check if response is a greeting-like reply
                        resp = next_seg.text.strip().lower()[:50]
                        is_greeting_response = any(
                            resp.startswith(g) for g in
                            ["hey", "hi", "hello", "morning", "yeah", "yes",
                             "thanks", "thank you", "good"]
                        ) or next_seg.word_count < 15

                        confidence = 0.85 if is_greeting_response else 0.70

                        analysis.add_identification(Identification(
                            speaker_label=next_seg.label,
                            identified_as=canonical,
                            method=IdentificationMethod.GREETING_EXCHANGE,
                            confidence=confidence,
                            evidence=f"Greeted as '{name_match}' by "
                                     f"{seg.label} at line {seg.line_number}",
                            line_number=next_seg.line_number,
                            timestamp=next_seg.timestamp,
                        ))
                        break
                    elif not next_seg.is_unidentified:
                        break  # Named speaker interrupted


# ──────────────────────────────────────────────
# Strategy 4: Direct Address Detection
# ──────────────────────────────────────────────

def run_direct_address_strategy(analysis: TranscriptAnalysis,
                                segments: list[SpeakerSegment]) -> None:
    """Detect when a known speaker addresses someone by name."""
    for i, seg in enumerate(segments):
        if seg.is_unidentified or not seg.text:
            continue

        for pattern in DIRECT_ADDRESS_PATTERNS:
            matches = re.findall(pattern, seg.text, re.MULTILINE)
            for name_match in matches:
                canonical = _name_matches_known(name_match)
                if not canonical:
                    continue
                if canonical in analysis.known_speakers:
                    continue

                # Next segment is likely the addressed person
                if i + 1 < len(segments):
                    next_seg = segments[i + 1]
                    if next_seg.is_unidentified and \
                       next_seg.label not in analysis.get_identified_labels():
                        analysis.add_identification(Identification(
                            speaker_label=next_seg.label,
                            identified_as=canonical,
                            method=IdentificationMethod.DIRECT_ADDRESS,
                            confidence=0.75,
                            evidence=f"Addressed as '{name_match}' by "
                                     f"{seg.label} at line {seg.line_number}",
                            line_number=next_seg.line_number,
                            timestamp=next_seg.timestamp,
                        ))


# ──────────────────────────────────────────────
# Strategy 5: Process of Elimination
# ──────────────────────────────────────────────

def run_elimination_strategy(analysis: TranscriptAnalysis,
                             segments: list[SpeakerSegment]) -> None:
    """Use process of elimination to identify remaining unknowns."""
    identified = analysis.get_identified_labels()
    remaining = [l for l in analysis.unknown_labels if l not in identified]

    if not remaining:
        return

    # Unmatched title candidates
    identified_names = {i.identified_as for i in analysis.identifications}
    known_canonical = {resolve_name(k) or k for k in analysis.known_speakers}
    unmatched = [c for c in analysis.title_candidates
                 if c not in identified_names and c not in known_canonical]

    # Azmain-as-recorder: if Azmain isn't a known speaker, add him as candidate
    azmain_canonical = resolve_name(ALWAYS_PRESENT)
    azmain_in_known = azmain_canonical in known_canonical
    if not azmain_in_known and azmain_canonical not in identified_names:
        unmatched.append(azmain_canonical)

    # Meeting type attendees as additional candidates
    meeting_type = analysis.meeting_type
    if meeting_type in MEETING_TYPE_ATTENDEES:
        for attendee in MEETING_TYPE_ATTENDEES[meeting_type]:
            if attendee not in known_canonical and \
               attendee not in identified_names and \
               attendee not in unmatched:
                unmatched.append(attendee)

    # Filter to numbered unknowns (consistent label = one person)
    numbered_remaining = [l for l in remaining if l != "Unknown Speaker"]

    # 1 remaining numbered unknown, 1 unmatched candidate → assign
    if len(numbered_remaining) == 1 and len(unmatched) >= 1:
        label = numbered_remaining[0]
        candidate = unmatched[0]  # Best candidate (title > azmain > meeting type)

        # Higher confidence if from title, lower if from meeting type
        is_title_candidate = candidate in analysis.title_candidates
        confidence = 0.88 if is_title_candidate else 0.72

        # Boost for 1:1 meetings
        if analysis.meeting_type == "1_on_1":
            confidence = min(confidence + 0.05, 0.95)

        analysis.add_identification(Identification(
            speaker_label=label,
            identified_as=candidate,
            method=IdentificationMethod.ELIMINATION,
            confidence=confidence,
            evidence=f"Only unresolved label '{label}', "
                     f"candidate '{candidate}' "
                     f"({'from title' if is_title_candidate else 'from meeting type'})",
            line_number=next(
                (s.line_number for s in segments if s.label == label), 0
            ),
            timestamp=next(
                (s.timestamp for s in segments if s.label == label), ""
            ),
        ))

    # --- Handle "Unknown Speaker" instances via elimination ---
    has_unknown_speaker = "Unknown Speaker" in remaining
    if has_unknown_speaker and "Unknown Speaker" not in analysis.get_identified_labels():
        # Filter unmatched to exclude anyone already identified
        identified_names = {i.identified_as for i in analysis.identifications}
        us_unmatched = [c for c in unmatched if c not in identified_names]

        if len(us_unmatched) == 1:
            candidate = us_unmatched[0]
            is_title_candidate = candidate in analysis.title_candidates
            confidence = 0.78 if is_title_candidate else 0.68

            first_us = next(
                (s for s in segments if s.label == "Unknown Speaker"), None
            )
            if first_us:
                analysis.add_identification(Identification(
                    speaker_label="Unknown Speaker",
                    identified_as=candidate,
                    method=IdentificationMethod.ELIMINATION,
                    confidence=confidence,
                    evidence=f"Only unmatched candidate '{candidate}' for "
                             f"Unknown Speaker "
                             f"({'from title' if is_title_candidate else 'from meeting type attendees'})",
                    line_number=first_us.line_number,
                    timestamp=first_us.timestamp,
                ))

    # Azmain-as-recorder special case — applies to ALL meeting types
    if not azmain_in_known and azmain_canonical not in {
        i.identified_as for i in analysis.identifications
    }:
        still_remaining = [l for l in remaining if l not in analysis.get_identified_labels()]
        if len(still_remaining) == 1:
            label = still_remaining[0]
            best = analysis.get_best_identification(label)
            if not best:
                # Higher confidence for 1:1, moderate for group meetings
                confidence = 0.80 if analysis.meeting_type == "1_on_1" else 0.68
                analysis.add_identification(Identification(
                    speaker_label=label,
                    identified_as=ALWAYS_PRESENT,
                    method=IdentificationMethod.AZMAIN_RECORDER,
                    confidence=confidence,
                    evidence="Azmain records virtually every meeting "
                             "and is not in named speakers"
                             + (f" (meeting type: {analysis.meeting_type})"
                                if analysis.meeting_type != "1_on_1" else ""),
                    line_number=next(
                        (s.line_number for s in segments if s.label == label), 0
                    ),
                    timestamp=next(
                        (s.timestamp for s in segments if s.label == label), ""
                    ),
                ))


# ──────────────────────────────────────────────
# Strategy 6: Cross-Reference Exclusion
# ──────────────────────────────────────────────

def run_cross_reference_strategy(analysis: TranscriptAnalysis,
                                 segments: list[SpeakerSegment]) -> None:
    """When unknown speaker mentions a name, they are NOT that person."""
    for seg in segments:
        if not seg.is_unidentified or not seg.text:
            continue

        text = seg.text
        # Patterns: "as Richard said", "I agree with Courtney",
        # "like Josh mentioned", "what Diya was saying"
        ref_patterns = [
            r"(?i)\bas\s+([A-Z][a-z]+)\s+(?:said|mentioned|noted|suggested)",
            r"(?i)\bagree\s+with\s+(?:what\s+)?([A-Z][a-z]+)",
            r"(?i)\blike\s+([A-Z][a-z]+)\s+(?:said|mentioned|was saying)",
            r"(?i)\bwhat\s+([A-Z][a-z]+)\s+(?:said|was saying|mentioned)",
            r"(?i)\b([A-Z][a-z]+)\s+(?:was saying|was mentioning|pointed out)",
            r"(?i)\bI told\s+([A-Z][a-z]+)",
            r"(?i)\b([A-Z][a-z]+)\s+and I\b",
        ]

        for pattern in ref_patterns:
            matches = re.findall(pattern, text)
            for name_match in matches:
                canonical = _name_matches_known(name_match)
                if canonical:
                    # This speaker is NOT this person
                    if seg.label not in analysis.exclusions:
                        analysis.exclusions[seg.label] = []
                    if canonical not in analysis.exclusions[seg.label]:
                        analysis.exclusions[seg.label].append(canonical)


# ──────────────────────────────────────────────
# Strategy 7: Speech Pattern Matching
# ──────────────────────────────────────────────

def run_speech_pattern_strategy(analysis: TranscriptAnalysis,
                                segments: list[SpeakerSegment]) -> None:
    """Match unknown speaker text against known speech patterns."""
    for label in analysis.unknown_labels:
        if label in analysis.get_identified_labels():
            continue

        combined_text = " ".join(
            s.text for s in segments if s.label == label and s.text
        )
        if len(combined_text.split()) < 30:
            continue  # Not enough text

        # Score against each known speaker's patterns
        scores: dict[str, float] = {}
        for speaker_name, patterns_dict in SPEECH_PATTERNS.items():
            score = 0.0
            total_patterns = 0

            for category in ["signature_words", "role_phrases",
                             "cultural_markers", "personal_markers"]:
                pattern_list = patterns_dict.get(category, [])
                if not pattern_list:
                    continue
                total_patterns += len(pattern_list)
                for pattern in pattern_list:
                    try:
                        matches = re.findall(pattern, combined_text, re.IGNORECASE)
                        if matches:
                            score += 1.0
                    except re.error:
                        pass

            if total_patterns > 0:
                scores[speaker_name] = score / total_patterns

        # Check exclusions
        excluded = set(analysis.exclusions.get(label, []))

        # Best match
        if scores:
            best_name = max(
                (name for name in scores if name not in excluded),
                key=lambda n: scores[n],
                default=None,
            )
            if best_name and scores[best_name] > 0.15:
                confidence = min(0.55 + scores[best_name] * 0.3, 0.75)
                first_seg = next(
                    (s for s in segments if s.label == label), None
                )
                if first_seg:
                    analysis.add_identification(Identification(
                        speaker_label=label,
                        identified_as=best_name,
                        method=IdentificationMethod.STYLOMETRIC_MATCH,
                        confidence=confidence,
                        evidence=f"Speech patterns match {best_name} "
                                 f"(score: {scores[best_name]:.2f})",
                        line_number=first_seg.line_number,
                        timestamp=first_seg.timestamp,
                    ))


# ──────────────────────────────────────────────
# Consistency Enforcement
# ──────────────────────────────────────────────

def enforce_consistency(analysis: TranscriptAnalysis) -> None:
    """Ensure each 'Speaker N' label maps to at most one person.

    For 'Unknown Speaker', each instance is independent (no consistency needed).
    """
    label_to_best: dict[str, Identification] = {}

    for ident in analysis.identifications:
        label = ident.speaker_label
        if label == "Unknown Speaker":
            continue  # Instance-specific, no consistency needed

        existing = label_to_best.get(label)
        if existing is None or ident.confidence > existing.confidence:
            label_to_best[label] = ident

    # Rebuild identifications: keep best per label + all Unknown Speaker
    new_idents = []
    for ident in analysis.identifications:
        if ident.speaker_label == "Unknown Speaker":
            new_idents.append(ident)
        elif ident == label_to_best.get(ident.speaker_label):
            new_idents.append(ident)

    analysis.identifications = new_idents


# ──────────────────────────────────────────────
# Main Heuristic Pipeline
# ──────────────────────────────────────────────

def run_all_heuristics(analysis: TranscriptAnalysis,
                       segments: list[SpeakerSegment]) -> None:
    """Run all 7 heuristic strategies in order."""
    # Detect meeting type
    analysis.meeting_type = _detect_meeting_type(analysis.title)

    # Run strategies in order of reliability
    run_title_strategy(analysis, segments)
    run_self_intro_strategy(analysis, segments)
    run_greeting_strategy(analysis, segments)
    run_direct_address_strategy(analysis, segments)
    run_elimination_strategy(analysis, segments)
    run_cross_reference_strategy(analysis, segments)
    run_speech_pattern_strategy(analysis, segments)

    # Enforce consistency
    enforce_consistency(analysis)

    # Update unresolved list
    identified = analysis.get_identified_labels()
    analysis.unresolved = [l for l in analysis.unknown_labels if l not in identified]
