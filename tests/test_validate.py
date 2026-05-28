import json
from pathlib import Path

from creatives_analysis.validation import validate_fixture_files


def test_validate_fixture_files_accepts_valid_samples() -> None:
    results = validate_fixture_files(
        schemas_dir=Path("schemas"),
        fixtures_dir=Path("tests/fixtures"),
    )

    assert results
    assert all(result.valid for result in results), [
        (result.fixture.name, result.errors) for result in results
    ]


def test_sample_evidence_packet_has_no_report_content() -> None:
    sample = json.loads(Path("tests/fixtures/evidence_packet.sample.json").read_text())

    assert "deconstruct" not in sample
    assert "adaptations" not in sample


def test_deconstruct_sample_enforces_perception_and_mechanism_layers() -> None:
    sample = json.loads(Path("tests/fixtures/deconstruct_report.sample.json").read_text())

    assert "cold_watch" in sample
    assert "evidence_timeline" in sample
    assert "core_mechanism" in sample
    assert "platform_fit" in sample


def test_adaptation_sample_enforces_taste_and_lineage_fields() -> None:
    sample = json.loads(Path("tests/fixtures/adaptation_variant.sample.json").read_text())

    assert "competitor_mechanism" in sample
    assert "evidence_lineage" in sample
    assert "proof_scene" in sample
    assert "test_hypothesis" in sample
    assert "swappability_check" in sample
