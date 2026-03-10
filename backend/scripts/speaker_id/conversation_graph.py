"""Stage 3: Conversation structure analysis — turn-taking, roles, graph features."""

from __future__ import annotations

import re
from collections import Counter, defaultdict

from .config import FACILITATOR_PHRASES, resolve_name
from .models import ConversationRole, SpeakerSegment, TranscriptAnalysis


def build_conversation_roles(segments: list[SpeakerSegment]) -> dict[str, ConversationRole]:
    """Build conversation role profiles for all speakers in a transcript."""
    if not segments:
        return {}

    roles: dict[str, ConversationRole] = {}
    total_segments = len(segments)
    labels = list({s.label for s in segments})

    # Count segments per speaker
    label_counts = Counter(s.label for s in segments)

    # Build adjacency (who follows whom)
    adjacency: dict[str, Counter] = defaultdict(Counter)
    for i in range(1, len(segments)):
        prev_label = segments[i - 1].label
        curr_label = segments[i].label
        if prev_label != curr_label:  # Skip self-follow
            adjacency[prev_label][curr_label] += 1

    for label in labels:
        role = ConversationRole()
        segs = [s for s in segments if s.label == label]

        # Basic stats
        role.segment_count = len(segs)
        role.total_words = sum(s.word_count for s in segs)
        role.avg_segment_length = role.total_words / max(role.segment_count, 1)

        # Position
        role.speaks_first = segments[0].label == label
        role.speaks_last = segments[-1].label == label

        # Position distribution (early/mid/late thirds)
        if total_segments > 0:
            positions = [s.segment_index / total_segments for s in segs]
            early = sum(1 for p in positions if p < 0.33) / max(len(positions), 1)
            mid = sum(1 for p in positions if 0.33 <= p < 0.66) / max(len(positions), 1)
            late = sum(1 for p in positions if p >= 0.66) / max(len(positions), 1)
            role.segment_position_distribution = [early, mid, late]

        # Question ratio
        all_text = " ".join(s.text for s in segs if s.text)
        sentences = re.split(r'(?<=[.!?])\s+', all_text)
        sentences = [s for s in sentences if s.strip()]
        if sentences:
            questions = sum(1 for s in sentences if s.strip().endswith("?"))
            role.question_ratio = questions / len(sentences)

        # Degree centrality (unique interaction partners)
        out_partners = set(adjacency[label].keys())
        in_partners = set()
        for other_label, targets in adjacency.items():
            if label in targets:
                in_partners.add(other_label)

        all_partners = out_partners | in_partners
        role.degree_centrality = len(all_partners) / max(len(labels) - 1, 1)
        role.out_degree = sum(adjacency[label].values())
        role.in_degree = sum(
            targets[label] for targets in adjacency.values() if label in targets
        )

        # Betweenness centrality (simplified: bridge score)
        # Count how many unique pairs this speaker connects
        bridge_count = 0
        for source in adjacency[label]:
            for target_label, target_counts in adjacency.items():
                if target_label != label and source in target_counts:
                    bridge_count += 1
        role.betweenness_centrality = bridge_count / max(
            len(labels) * (len(labels) - 1), 1
        )

        # Interaction patterns
        role.response_to_pattern = dict(adjacency[label])
        role.responded_to_by = {}
        for other_label, targets in adjacency.items():
            if label in targets:
                role.responded_to_by[other_label] = targets[label]

        # Primary interlocutor
        if role.response_to_pattern:
            role.primary_interlocutor = max(
                role.response_to_pattern, key=role.response_to_pattern.get
            )

        # Role detection
        fac_count = 0
        for pattern in FACILITATOR_PHRASES:
            fac_count += len(re.findall(pattern, all_text))
        role.is_likely_facilitator = (
            fac_count >= 2 and role.betweenness_centrality > 0.1
        )

        role.is_likely_presenter = (
            role.avg_segment_length > 80 and role.question_ratio < 0.15
        )

        role.is_likely_questioner = (
            role.question_ratio > 0.4 and role.avg_segment_length < 40
        )

        role.is_likely_passive = (
            role.segment_count <= 3 and role.avg_segment_length < 20
        )

        roles[label] = role

    return roles


def analyze_conversation_structure(analysis: TranscriptAnalysis,
                                   segments: list[SpeakerSegment]) -> None:
    """Add conversation role data to the analysis."""
    analysis.conversation_roles = build_conversation_roles(segments)

    # Use role data to support identification
    # Facilitator in a programme meeting → likely Richard or Azmain
    # Passive listener in an executive meeting → likely Diya
    # Presenter with long segments → likely the meeting's subject matter expert

    for label, role in analysis.conversation_roles.items():
        if not any(s.is_unidentified for s in segments if s.label == label):
            continue
        if label in analysis.get_identified_labels():
            continue

        # Executive meetings: passive listener with few short segments → likely Diya
        if (analysis.meeting_type == "executive" and
                role.is_likely_passive and
                "Diya Sawhny" in (analysis.title_candidates or [])):
            from .models import Identification, IdentificationMethod
            first_seg = next((s for s in segments if s.label == label), None)
            if first_seg:
                analysis.add_identification(Identification(
                    speaker_label=label,
                    identified_as="Diya Sawhny",
                    method=IdentificationMethod.CONVERSATION_ROLE,
                    confidence=0.65,
                    evidence=f"Passive listener ({role.segment_count} segments, "
                             f"avg {role.avg_segment_length:.0f} words) "
                             f"in executive meeting titled with Diya",
                    line_number=first_seg.line_number,
                    timestamp=first_seg.timestamp,
                ))
