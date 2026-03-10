"""Stage 1: Build speaker profile database from named segments across all transcripts."""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path
from statistics import mean, stdev

from .config import (
    STAKEHOLDER_ALIASES, SPEAKER_GENDER, FILLERS, TECHNICAL_TERMS,
    FACILITATOR_PHRASES, SPEECH_PATTERNS, resolve_name,
)
from .models import SpeakerProfile, SpeakerSegment
from .segment_parser import (
    parse_segments, get_known_speakers, get_segments_by_label,
    get_combined_text, get_total_words,
)


PROFILES_DIR = Path(__file__).parent / "profiles"
PROFILES_FILE = PROFILES_DIR / "speaker_profiles.json"


def _count_pattern_matches(text: str, patterns: list[str]) -> int:
    """Count total regex matches across patterns."""
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    return count


def _simple_sent_tokenize(text: str) -> list[str]:
    """Basic sentence tokenizer — split on .!? followed by space or end."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def _tokenize(text: str) -> list[str]:
    """Basic word tokenizer."""
    return re.findall(r'\b[a-zA-Z\']+\b', text.lower())


def _compute_formality(text: str) -> float:
    """Compute formality score: 0.0 (casual) to 1.0 (formal)."""
    words = _tokenize(text)
    if not words:
        return 0.5

    informal = len(re.findall(
        r'\b(gonna|wanna|gotta|kinda|sorta|bro|dude|mate|guys|yeah|yep|nah|nope)\b',
        text, re.IGNORECASE
    ))
    contractions = len(re.findall(r"n't\b", text))
    informal += contractions

    formal = len(re.findall(
        r'\b(furthermore|therefore|consequently|however|regarding|concerning|shall|ought)\b',
        text, re.IGNORECASE
    ))

    total = informal + formal
    if total == 0:
        return 0.5

    return formal / total


def _compute_tech_density(text: str) -> float:
    """Compute ratio of technical terms to total words."""
    words = _tokenize(text)
    if not words:
        return 0.0

    tech_count = 0
    text_lower = text.lower()
    for domain_terms in TECHNICAL_TERMS.values():
        for term in domain_terms:
            tech_count += len(re.findall(r'\b' + re.escape(term) + r'\b', text_lower))

    return tech_count / len(words)


def _compute_hedge_ratio(text: str) -> float:
    """Compute ratio of hedging language."""
    words = _tokenize(text)
    if not words:
        return 0.0

    hedge_count = 0
    for phrase in FILLERS["hedge"]:
        hedge_count += len(re.findall(re.escape(phrase), text, re.IGNORECASE))

    return hedge_count / (len(words) / 1000) if len(words) > 0 else 0.0


def _compute_assertiveness(text: str) -> float:
    """Compute ratio of assertive language."""
    words = _tokenize(text)
    if not words:
        return 0.0

    assert_count = 0
    for phrase in FILLERS["assertive"]:
        assert_count += len(re.findall(r'\b' + re.escape(phrase) + r'\b',
                                        text, re.IGNORECASE))

    return assert_count / (len(words) / 1000) if len(words) > 0 else 0.0


def _extract_greeting_patterns(segments: list[SpeakerSegment]) -> list[str]:
    """Extract how a speaker opens their turns."""
    patterns = []
    for seg in segments[:10]:  # Check first 10 segments
        text = seg.text.strip()
        if not text:
            continue
        first_words = " ".join(text.split()[:5]).lower()
        for greeting in ["hey guys", "hey everyone", "hi everyone", "morning",
                         "hello", "hey", "hi", "good morning", "afternoon"]:
            if first_words.startswith(greeting):
                patterns.append(greeting)
                break
    return list(set(patterns))


def build_profile(canonical_name: str,
                  all_segments: list[SpeakerSegment],
                  transcript_filenames: list[str]) -> SpeakerProfile:
    """Build a speaker profile from all their named segments."""
    profile = SpeakerProfile(canonical_name=canonical_name)
    profile.aliases = STAKEHOLDER_ALIASES.get(canonical_name, [])
    profile.gender = SPEAKER_GENDER.get(canonical_name)

    if not all_segments:
        return profile

    # Volume stats
    profile.total_segments = len(all_segments)
    profile.total_words = sum(s.word_count for s in all_segments)
    profile.transcript_list = list(set(transcript_filenames))
    profile.transcripts_appeared_in = len(profile.transcript_list)

    lengths = [s.word_count for s in all_segments]
    profile.avg_segment_length = mean(lengths) if lengths else 0.0
    profile.segment_length_std = stdev(lengths) if len(lengths) > 1 else 0.0

    # Combine all text
    all_text = " ".join(s.text for s in all_segments if s.text)
    if not all_text:
        return profile

    # Vocabulary
    words = _tokenize(all_text)
    word_counts = Counter(words)
    profile.vocabulary_size = len(word_counts)
    profile.type_token_ratio = len(word_counts) / max(len(words), 1)

    # Top words (normalized frequency per 1000 words)
    total = len(words)
    profile.top_words = {
        word: (count / total) * 1000
        for word, count in word_counts.most_common(100)
    }

    # Filler frequencies (per 1000 words)
    for category, filler_list in FILLERS.items():
        count = 0
        for filler in filler_list:
            count += len(re.findall(
                r'\b' + re.escape(filler) + r'\b', all_text, re.IGNORECASE
            ))
        profile.filler_frequencies[category] = (count / max(total, 1)) * 1000

    # Discourse markers specifically
    discourse_words = ["so", "well", "like", "basically", "actually",
                       "obviously", "honestly", "literally"]
    for marker in discourse_words:
        count = len(re.findall(r'\b' + marker + r'\b', all_text, re.IGNORECASE))
        profile.discourse_markers[marker] = (count / max(total, 1)) * 1000

    # Signature phrases from config
    config_patterns = SPEECH_PATTERNS.get(canonical_name, {})
    sig_words = config_patterns.get("signature_words", [])
    profile.signature_phrases = sig_words
    for pattern in sig_words:
        try:
            count = len(re.findall(pattern, all_text, re.IGNORECASE))
            profile.phrase_frequencies[pattern] = (count / max(total, 1)) * 1000
        except re.error:
            pass

    # Syntactic features
    sentences = _simple_sent_tokenize(all_text)
    if sentences:
        sent_lengths = [len(s.split()) for s in sentences]
        profile.avg_sentence_length = mean(sent_lengths)
        questions = sum(1 for s in sentences if s.strip().endswith("?"))
        exclamations = sum(1 for s in sentences if s.strip().endswith("!"))
        profile.question_ratio = questions / len(sentences)
        profile.exclamation_ratio = exclamations / len(sentences)

    # Style metrics
    profile.formality_score = _compute_formality(all_text)
    profile.technical_density = _compute_tech_density(all_text)
    profile.hedge_ratio = _compute_hedge_ratio(all_text)
    profile.assertiveness_ratio = _compute_assertiveness(all_text)

    # Greeting patterns
    profile.greeting_patterns = _extract_greeting_patterns(all_segments)

    # Facilitator score
    fac_count = 0
    for pattern in FACILITATOR_PHRASES:
        fac_count += len(re.findall(pattern, all_text))
    profile.facilitator_score = fac_count / max(profile.total_segments, 1)

    return profile


def build_all_profiles(transcripts_dir: Path) -> dict[str, SpeakerProfile]:
    """Build profiles for all named speakers across all transcripts.

    Scans every transcript, collects all segments from named speakers,
    and builds a profile per canonical speaker name.
    """
    # Collect segments per speaker across all files
    speaker_segments: dict[str, list[SpeakerSegment]] = {}
    speaker_transcripts: dict[str, list[str]] = {}

    transcript_files = sorted(transcripts_dir.glob("*.txt"))

    for filepath in transcript_files:
        segments = parse_segments(filepath)
        known = get_known_speakers(segments)

        for speaker_name in known:
            # Resolve to canonical name
            canonical = resolve_name(speaker_name) or speaker_name

            if canonical not in speaker_segments:
                speaker_segments[canonical] = []
                speaker_transcripts[canonical] = []

            segs = get_segments_by_label(segments, speaker_name)
            speaker_segments[canonical].extend(segs)
            speaker_transcripts[canonical].append(filepath.name)

    # Build co-occurrence data
    file_speakers: dict[str, list[str]] = {}
    for filepath in transcript_files:
        segments = parse_segments(filepath)
        known = get_known_speakers(segments)
        canonical_speakers = []
        for s in known:
            c = resolve_name(s) or s
            canonical_speakers.append(c)
        file_speakers[filepath.name] = list(set(canonical_speakers))

    # Build profiles
    profiles: dict[str, SpeakerProfile] = {}
    for canonical, segs in speaker_segments.items():
        profile = build_profile(canonical, segs, speaker_transcripts[canonical])

        # Co-occurrence
        for fname in profile.transcript_list:
            for co_speaker in file_speakers.get(fname, []):
                if co_speaker != canonical:
                    profile.co_speakers[co_speaker] = \
                        profile.co_speakers.get(co_speaker, 0) + 1

        # Meeting opener stats
        opener_count = 0
        closer_count = 0
        for fname in profile.transcript_list:
            file_segments = parse_segments(transcripts_dir / fname)
            if file_segments:
                first_canonical = resolve_name(file_segments[0].label) or file_segments[0].label
                last_canonical = resolve_name(file_segments[-1].label) or file_segments[-1].label
                if first_canonical == canonical:
                    opener_count += 1
                if last_canonical == canonical:
                    closer_count += 1

        if profile.transcripts_appeared_in > 0:
            profile.opens_meetings = opener_count / profile.transcripts_appeared_in
            profile.closes_meetings = closer_count / profile.transcripts_appeared_in

        profiles[canonical] = profile

    return profiles


def save_profiles(profiles: dict[str, SpeakerProfile]) -> Path:
    """Save profiles to JSON file."""
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    data = {name: p.to_dict() for name, p in profiles.items()}
    PROFILES_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    return PROFILES_FILE


def load_profiles() -> dict[str, SpeakerProfile]:
    """Load profiles from JSON file."""
    if not PROFILES_FILE.exists():
        return {}
    data = json.loads(PROFILES_FILE.read_text(encoding="utf-8"))
    return {name: SpeakerProfile.from_dict(pdata) for name, pdata in data.items()}
