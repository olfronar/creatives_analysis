import json
from pathlib import Path

from jsonschema import Draft202012Validator

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
    assert "creative_intent" in sample
    assert "distilled_core" in sample
    assert "core_understanding" in sample
    assert "platform_fit" in sample


def test_deconstruct_schema_rejects_shallow_reports_without_core_understanding() -> None:
    schema = json.loads(Path("schemas/deconstruct_report.schema.json").read_text())
    sample = json.loads(Path("tests/fixtures/deconstruct_report.sample.json").read_text())
    sample.pop("core_understanding", None)

    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(sample))

    assert any("core_understanding" in error.message for error in errors)


def test_deconstruct_schema_requires_distilled_core() -> None:
    schema = json.loads(Path("schemas/deconstruct_report.schema.json").read_text())
    sample = json.loads(Path("tests/fixtures/deconstruct_report.sample.json").read_text())
    sample.pop("distilled_core", None)

    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(sample))

    assert any("distilled_core" in error.message for error in errors)


def test_deconstruct_schema_rejects_empty_distilled_core_fields() -> None:
    schema = json.loads(Path("schemas/deconstruct_report.schema.json").read_text())
    sample = json.loads(Path("tests/fixtures/deconstruct_report.sample.json").read_text())
    sample["distilled_core"] = {
        "core_thesis": "",
        "mechanism_formula": "",
        "belief_shift_summary": "",
        "why_it_works": "",
        "where_it_breaks": "",
        "submagic_transfer": "",
        "steal": [],
        "avoid": [],
        "test_next": [],
    }

    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(sample))

    assert errors


def test_deconstruct_schema_requires_creative_intent() -> None:
    schema = json.loads(Path("schemas/deconstruct_report.schema.json").read_text())
    sample = json.loads(Path("tests/fixtures/deconstruct_report.sample.json").read_text())
    sample.pop("creative_intent", None)

    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(sample))

    assert any("creative_intent" in error.message for error in errors)


def test_deconstruct_schema_rejects_empty_creative_intent_fields() -> None:
    schema = json.loads(Path("schemas/deconstruct_report.schema.json").read_text())
    sample = json.loads(Path("tests/fixtures/deconstruct_report.sample.json").read_text())
    sample["creative_intent"] = {
        "creative_label": "",
        "creative_type": "",
        "likely_hypothesis": "",
        "target_audience": "",
        "awareness_stage": "",
        "funnel_stage": "",
        "likely_kpi": "",
        "offer_strategy": "",
        "marketer_job_to_be_done": "",
        "evidence_ids": [],
        "confidence": "high",
        "unknowns": [],
    }

    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(sample))

    assert errors


def test_adaptation_sample_enforces_taste_and_lineage_fields() -> None:
    sample = json.loads(Path("tests/fixtures/adaptation_variant.sample.json").read_text())

    assert "competitor_mechanism" in sample
    assert "evidence_lineage" in sample
    assert "proof_scene" in sample
    assert "test_hypothesis" in sample
    assert "swappability_check" in sample
