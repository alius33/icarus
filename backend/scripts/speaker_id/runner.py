"""CLI entry point — orchestrates the full speaker identification pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add parent to path for module imports when run as script
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from scripts.speaker_id.models import (
    TranscriptAnalysis, SpeakerMapping, PipelineResult,
)
from scripts.speaker_id.segment_parser import (
    parse_segments, get_known_speakers, get_unknown_labels,
    parse_title_from_filename,
)
from scripts.speaker_id.profiler import (
    build_all_profiles, save_profiles, load_profiles,
)
from scripts.speaker_id.heuristics import run_all_heuristics
from scripts.speaker_id.conversation_graph import analyze_conversation_structure
from scripts.speaker_id.stylometric_matcher import run_stylometric_matching
from scripts.speaker_id.confidence_engine import (
    aggregate_identifications, build_final_mapping,
)
from scripts.speaker_id.applier import apply_all_mappings
from scripts.speaker_id.report import (
    build_pipeline_result, generate_review_report,
)


def find_transcripts_dir() -> Path:
    """Find the Transcripts directory relative to this script."""
    # From backend/scripts/speaker_id/ → go up to project root
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent.parent  # backend/scripts/speaker_id → project root
    transcripts = project_root / "Transcripts"
    if transcripts.exists():
        return transcripts

    # Try current working directory
    cwd_transcripts = Path.cwd() / "Transcripts"
    if cwd_transcripts.exists():
        return cwd_transcripts

    # Try parent of cwd
    parent_transcripts = Path.cwd().parent / "Transcripts"
    if parent_transcripts.exists():
        return parent_transcripts

    raise FileNotFoundError("Could not find Transcripts directory")


def analyze_single_file(filepath: Path, profiles: dict | None = None) -> tuple:
    """Analyze a single transcript file through the full pipeline.

    Returns (TranscriptAnalysis, SpeakerMapping)
    """
    segments = parse_segments(filepath)
    if not segments:
        return None, None

    title = parse_title_from_filename(filepath.name)
    known = get_known_speakers(segments)
    unknown = get_unknown_labels(segments)

    analysis = TranscriptAnalysis(
        filename=filepath.name,
        filepath=str(filepath),
        title=title,
        known_speakers=known,
        unknown_labels=unknown,
        total_segments=len(segments),
        total_unknown_segments=sum(1 for s in segments if s.is_unidentified),
    )

    if not unknown:
        # No unknowns — nothing to do
        mapping = build_final_mapping(analysis)
        return analysis, mapping

    # Stage 2: Heuristics
    run_all_heuristics(analysis, segments)

    # Stage 3: Conversation graph analysis
    analyze_conversation_structure(analysis, segments)

    # Stage 4: Stylometric matching (if profiles available)
    if profiles:
        run_stylometric_matching(analysis, segments, profiles)

    # Stage 5: Confidence aggregation
    aggregate_identifications(analysis)

    # Update unresolved
    identified = analysis.get_identified_labels()
    analysis.unresolved = [l for l in unknown if l not in identified]

    # Build mapping
    mapping = build_final_mapping(analysis)
    return analysis, mapping


def run_pipeline(transcripts_dir: Path,
                 single_file: Path | None = None,
                 build_profiles_flag: bool = True,
                 output_json: Path | None = None,
                 output_report: Path | None = None,
                 apply_flag: bool = False,
                 threshold: float = 0.0,
                 dry_run: bool = False,
                 mapping_file: Path | None = None) -> PipelineResult:
    """Run the full speaker identification pipeline."""

    print(f"{'='*60}")
    print("  SPEAKER IDENTIFICATION PIPELINE")
    print(f"{'='*60}")
    print(f"Transcripts dir: {transcripts_dir}")
    print()

    # Stage 1: Build speaker profiles
    profiles = {}
    if build_profiles_flag:
        print("Stage 1: Building speaker profiles...")
        profiles = build_all_profiles(transcripts_dir)
        profile_path = save_profiles(profiles)
        print(f"  Built {len(profiles)} profiles")
        print(f"  Saved to {profile_path}")
        print()
    else:
        profiles = load_profiles()
        print(f"Stage 1: Loaded {len(profiles)} cached profiles")
        print()

    # Determine files to process
    if single_file:
        files = [single_file]
    else:
        files = sorted(transcripts_dir.glob("*.txt"))

    print(f"Stage 2-5: Analyzing {len(files)} transcripts...")

    # If applying from a mapping file, load it
    if apply_flag and mapping_file:
        return _apply_from_file(transcripts_dir, mapping_file, threshold, dry_run)

    # Run analysis pipeline
    analyses: dict[str, TranscriptAnalysis] = {}
    mappings: dict[str, SpeakerMapping] = {}

    files_with_unknowns = 0
    total_identifications = 0
    total_unresolved = 0

    for filepath in files:
        analysis, mapping = analyze_single_file(filepath, profiles)
        if analysis is None:
            continue

        analyses[filepath.name] = analysis
        mappings[filepath.name] = mapping

        if analysis.unknown_labels:
            files_with_unknowns += 1

        n_idents = len(analysis.identifications)
        n_unresolved = len(analysis.unresolved)
        total_identifications += n_idents
        total_unresolved += n_unresolved

        # Progress indicator for files with unknowns
        if analysis.unknown_labels:
            status = "OK" if not analysis.unresolved else f"~{n_unresolved} left"
            print(f"  [{status}] {filepath.name}: "
                  f"{n_idents} identified, "
                  f"{n_unresolved} unresolved")

    print()
    print(f"Results:")
    print(f"  Total files analyzed: {len(analyses)}")
    print(f"  Files with unknowns: {files_with_unknowns}")
    print(f"  Total identifications: {total_identifications}")
    print(f"  Total unresolved: {total_unresolved}")
    print()

    # Build pipeline result
    result = build_pipeline_result(analyses, mappings, len(profiles))

    # Output JSON
    if output_json:
        result.to_json(output_json)
        print(f"Mapping JSON saved to: {output_json}")

    # Output review report
    if output_report:
        report_text = generate_review_report(analyses, mappings)
        output_report.write_text(report_text, encoding="utf-8")
        print(f"Review report saved to: {output_report}")

    # Apply mappings
    if apply_flag:
        print()
        print(f"Applying mappings (threshold: {threshold}, dry_run: {dry_run})...")
        results = apply_all_mappings(
            transcripts_dir, mappings, threshold, backup=True, dry_run=dry_run
        )
        total_replacements = sum(r["replacements"] for r in results)
        print(f"  {'Would make' if dry_run else 'Made'} {total_replacements} "
              f"replacements across {len(results)} files")

        if dry_run:
            for r in results:
                if r["replacements"] > 0:
                    print(f"  {Path(r['file']).name}: {r['replacements']} replacements")
                    for d in r.get("details", [])[:5]:
                        print(f"    Line {d['line']}: {d['old']} → {d['new']} "
                              f"({d['confidence']:.2f})")

    return result


def _apply_from_file(transcripts_dir: Path,
                     mapping_file: Path,
                     threshold: float,
                     dry_run: bool) -> PipelineResult:
    """Apply mappings from a previously generated JSON file."""
    data = json.loads(mapping_file.read_text(encoding="utf-8"))
    transcripts_data = data.get("transcripts", {})

    all_mappings: dict[str, SpeakerMapping] = {}
    for filename, tdata in transcripts_data.items():
        mapping = SpeakerMapping(
            filename=filename,
            mappings=tdata.get("mappings", {}),
            flagged_for_review=tdata.get("flagged_for_review", []),
            unresolved=tdata.get("unresolved", []),
        )
        all_mappings[filename] = mapping

    results = apply_all_mappings(
        transcripts_dir, all_mappings, threshold, backup=True, dry_run=dry_run
    )
    total = sum(r["replacements"] for r in results)
    print(f"{'Would apply' if dry_run else 'Applied'} {total} replacements")

    return PipelineResult(
        generated_at=datetime.now(timezone.utc).isoformat(),
        summary={"total_replacements": total},
    )


def main():
    parser = argparse.ArgumentParser(
        description="Speaker Identification Pipeline for Icarus transcripts"
    )
    parser.add_argument(
        "--file", type=str, help="Analyze a single transcript file"
    )
    parser.add_argument(
        "--analyze", action="store_true",
        help="Run full analysis pipeline (stages 0-5)"
    )
    parser.add_argument(
        "--build-profiles", action="store_true",
        help="Build/rebuild speaker profiles only"
    )
    parser.add_argument(
        "--output", "-o", type=str,
        help="Output mapping JSON path"
    )
    parser.add_argument(
        "--report", type=str,
        help="Output human-readable review report path"
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Apply mappings to transcript files"
    )
    parser.add_argument(
        "--mapping-file", type=str,
        help="Path to mapping JSON to apply (with --apply)"
    )
    parser.add_argument(
        "--threshold", type=float, default=0.0,
        help="Minimum confidence to apply (default: 0.0)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview changes without modifying files"
    )
    parser.add_argument(
        "--transcripts-dir", type=str,
        help="Path to Transcripts directory (auto-detected if not provided)"
    )

    args = parser.parse_args()

    # Find transcripts directory
    if args.transcripts_dir:
        transcripts_dir = Path(args.transcripts_dir)
    else:
        transcripts_dir = find_transcripts_dir()

    if not transcripts_dir.exists():
        print(f"Error: Transcripts directory not found: {transcripts_dir}")
        sys.exit(1)

    # Build profiles only
    if args.build_profiles:
        print("Building speaker profiles...")
        profiles = build_all_profiles(transcripts_dir)
        save_profiles(profiles)
        print(f"Built {len(profiles)} profiles")
        for name, p in sorted(profiles.items(), key=lambda x: -x[1].total_segments):
            print(f"  {name}: {p.total_segments} segments, "
                  f"{p.total_words} words, "
                  f"{p.transcripts_appeared_in} transcripts")
        return

    # Single file or batch
    single_file = Path(args.file) if args.file else None
    if single_file and not single_file.is_absolute():
        single_file = transcripts_dir / single_file

    output_json = Path(args.output) if args.output else None
    output_report = Path(args.report) if args.report else None
    mapping_file = Path(args.mapping_file) if args.mapping_file else None

    # Default behavior: analyze + output
    if not args.analyze and not args.apply and not args.build_profiles:
        args.analyze = True

    run_pipeline(
        transcripts_dir=transcripts_dir,
        single_file=single_file,
        build_profiles_flag=True,
        output_json=output_json,
        output_report=output_report,
        apply_flag=args.apply,
        threshold=args.threshold,
        dry_run=args.dry_run,
        mapping_file=mapping_file,
    )


if __name__ == "__main__":
    main()
