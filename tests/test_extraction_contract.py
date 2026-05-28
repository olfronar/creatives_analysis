import json
from pathlib import Path

from creatives_analysis.extraction import build_evidence_packet
from creatives_analysis.validation import validate_json_file

from tests.helpers import make_test_video


def test_generated_evidence_packet_matches_schema(tmp_path: Path) -> None:
    video = make_test_video(tmp_path)

    packet_path = build_evidence_packet(
        video=video,
        output_root=tmp_path,
        sample_frames=0,
    )

    result = validate_json_file(
        fixture=packet_path,
        schema=Path("schemas/evidence_packet.schema.json"),
    )

    assert result.valid, result.errors


def test_generated_evidence_packet_uses_evidence_ids(tmp_path: Path) -> None:
    video = make_test_video(tmp_path)

    packet_path = build_evidence_packet(
        video=video,
        output_root=tmp_path,
        sample_frames=0,
    )

    packet = json.loads(packet_path.read_text())

    assert packet["analysis_run"]["run_id"]
    assert packet["timeline_evidence"]
    assert all(event["evidence_id"] for event in packet["timeline_evidence"])
