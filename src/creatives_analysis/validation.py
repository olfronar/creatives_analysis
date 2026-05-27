from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from .models import ValidationResult


def validate_fixture_files(
    *,
    schemas_dir: Path = Path("schemas"),
    fixtures_dir: Path = Path("tests/fixtures"),
) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    for fixture in sorted(fixtures_dir.glob("*.sample.json")):
        schema = schemas_dir / fixture.name.replace(".sample.json", ".schema.json")
        results.append(validate_json_file(fixture=fixture, schema=schema))
    return results


def validate_json_file(*, fixture: Path, schema: Path) -> ValidationResult:
    if not schema.exists():
        return ValidationResult(
            fixture=fixture,
            schema_path=schema,
            valid=False,
            errors=[f"Schema not found: {schema}"],
        )

    data = json.loads(fixture.read_text())
    schema_data = json.loads(schema.read_text())
    validator = Draft202012Validator(schema_data)
    errors = [
        f"{'.'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(data), key=str)
    ]
    return ValidationResult(
        fixture=fixture,
        schema_path=schema,
        valid=not errors,
        errors=errors,
    )
