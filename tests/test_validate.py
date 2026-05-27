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
