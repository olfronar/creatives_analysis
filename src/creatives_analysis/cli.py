from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .doctor import collect_doctor_status, doctor_has_failures
from .extraction import build_evidence_packet
from .inventory import collect_inventory, inventory_as_json, inventory_as_table
from .validation import validate_fixture_files


def doctor_app() -> None:
    status = collect_doctor_status()
    print(json.dumps(status, indent=2, sort_keys=True))
    if doctor_has_failures(status):
        raise SystemExit(1)


def inventory_app() -> None:
    parser = argparse.ArgumentParser(
        prog="creatives-inventory",
        description="Inspect MP4 metadata without generating deconstruction reports.",
    )
    parser.add_argument("--creatives-dir", default="creatives")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    args = parser.parse_args()

    videos = sorted(Path(args.creatives_dir).glob("*.mp4"))
    rows = collect_inventory(videos)
    print(inventory_as_json(rows) if args.json else inventory_as_table(rows))


def extract_app() -> None:
    parser = argparse.ArgumentParser(
        prog="creatives-extract",
        description="Create evidence artifacts only; no deconstruct/adapt report is generated.",
    )
    parser.add_argument("--video", required=True)
    parser.add_argument("--output-root", default="outputs")
    parser.add_argument("--sample-frames", type=int, default=8)
    args = parser.parse_args()

    packet = build_evidence_packet(
        video=Path(args.video),
        output_root=Path(args.output_root),
        sample_frames=args.sample_frames,
    )
    print(packet)


def validate_app() -> None:
    parser = argparse.ArgumentParser(
        prog="creatives-validate",
        description="Validate sample fixtures against JSON schemas.",
    )
    parser.add_argument("--schemas-dir", default="schemas")
    parser.add_argument("--fixtures-dir", default="tests/fixtures")
    args = parser.parse_args()

    results = validate_fixture_files(
        schemas_dir=Path(args.schemas_dir),
        fixtures_dir=Path(args.fixtures_dir),
    )
    for result in results:
        status = "PASS" if result.valid else "FAIL"
        print(f"{status} {result.fixture} -> {result.schema_path}")
        for error in result.errors:
            print(f"  - {error}")

    if not results:
        print("No fixture files found.", file=sys.stderr)
        raise SystemExit(1)
    if not all(result.valid for result in results):
        raise SystemExit(1)
