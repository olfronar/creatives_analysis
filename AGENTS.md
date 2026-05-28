# AGENTS.md

Guidance for agents working in this repository.

## Project Purpose

This workspace supports competitor short-form video creative analysis and Submagic adaptation brainstorming.

Primary outputs for future runs:

- `deconstruct`: timestamped, evidence-backed creative deconstruction.
- `adapt`: Submagic-native creative briefs and script variants for creators and agencies.

## Hard Rules

- Use `uv` strictly for all Python dependency management and command execution.
- Do not use `pip`, Conda, Poetry, or `python -m venv`.
- Do not claim a creative is high-performing unless real performance metrics are provided.
- Every deconstruction claim must cite timestamped evidence.
- Prefer evidence IDs over prose timestamps in structured artifacts.
- Adapt strategy and mechanisms only. Do not copy competitor scripts, visuals, captions, music, creator likeness, brand identity, or proprietary claims.
- Preserve the V1 build-only boundary unless explicitly asked to run analysis: do not generate `deconstruct` or `adapt` reports for `ad1-ad5` by accident.

## Common Commands

```bash
uv sync
uv run pytest
uv run creatives-doctor
uv run creatives-inventory
uv run creatives-extract --video creatives/ad1.mp4
uv run creatives-validate
```

## Repository Map

- `creatives/` contains source competitor videos.
- `research/` contains source-cited research notes.
- `prompts/` contains reusable prompt modules.
- `rubrics/` contains scoring rubrics.
- `schemas/` contains JSON output contracts.
- `src/creatives_analysis/` contains CLI and extraction tooling.
- `tests/` contains pytest coverage and schema fixtures.
- `outputs/` is for generated evidence and reports; generated contents are ignored except `.gitkeep`.

## Development Standards

- Prefer small, focused changes.
- Keep schemas and fixtures in sync.
- Add or update tests for CLI behavior, schema behavior, and report-contract changes.
- Keep README command examples accurate.
- Before saying work is complete, run the relevant `uv run ...` verification commands and inspect their output.

## Evidence And Output Discipline

Future deconstruction reports should separate:

- observation: what is visible or audible
- interpretation: why it matters
- evidence: timestamp, transcript line, OCR text, keyframe, scene note, or audio note
- confidence: low, medium, or high

Future adaptation reports should map each idea to Submagic features such as AI Captions, Magic Clips, Auto Edit, B-roll, Magic Zoom, Brand Kit, templates, publishing, or API workflows.

Reject shallow outputs that skip:

- cold-watch viewer perception
- mechanism extraction
- evidence lineage
- visible Submagic proof scene
- swappability check
- copycat/IP risk rationale
