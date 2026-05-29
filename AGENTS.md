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
- Render HTML reports only from validated deconstruct JSON plus evidence packets. The HTML layer may format and arrange claims, but must not create new claims.
- HTML deconstruction reports must keep evidence IDs, confidence, risk notes, and shot cards or explicit missing-shot states available, but raw evidence IDs should be hidden from first-order prose.
- Deconstruction reports must include `creative_intent`: creative label, creative type, likely hypothesis, target audience, awareness stage, funnel stage, likely KPI, offer strategy, marketer job-to-be-done, evidence IDs, confidence, and unknowns.
- Deconstruction reports must include `distilled_core`: core thesis, mechanism formula, belief-shift summary, why it works, where it breaks, Submagic transfer, what to steal, what to avoid, and what to test next.
- Deconstruction reports must include `core_understanding`: human truth, belief shift, tension stack, proof ladder, viewer-state timeline, skeptic read, Submagic transfer principle, and counterfactuals.
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
uv run creatives-render-report --deconstruct tests/fixtures/deconstruct_report.sample.json --evidence tests/fixtures/evidence_packet.sample.json --output /tmp/deconstruct_report.html
```

## Repository Map

- `creatives/` contains source competitor videos.
- `research/` contains source-cited research notes.
- `prompts/` contains reusable prompt modules.
- `rubrics/` contains scoring rubrics.
- `schemas/` contains JSON output contracts.
- `templates/html/` contains the report structure guide.
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

HTML reports should be built after deconstruction validation and before adaptation brainstorming. Use them as the shared review surface for human plus Codex discussion. Do not paste raw JSON into the report body; show the shot, concise interpretation, source count, and uncertainty.
Default report styling should follow Submagic's current light/orange product surface, not the older dark lime/purple draft theme.

## HTML Report Rules

- Keep reports concise by default.
- Put "Why this creative exists" before Core Read.
- Do not expose raw evidence IDs in first-order prose.
- Show a compact shot-backed Creative mechanism near the top.
- Color-code Creative mechanism cards by narrative function: hook, pain, proof, CTA, risk.
- Show top diagnostics before the long key-shot section.
- Hide key shots under a details block; the Creative mechanism section is the first-order visual scan.
- Hide full timelines, platform notes, score matrices, and evidence IDs in details blocks.
- Preserve Submagic's light/orange, clean creator-productivity tone.

Future adaptation reports should map each idea to Submagic features such as AI Captions, Magic Clips, Auto Edit, B-roll, Magic Zoom, Brand Kit, templates, publishing, or API workflows.

Reject shallow outputs that skip:

- cold-watch viewer perception
- mechanism extraction
- evidence lineage
- visible Submagic proof scene
- swappability check
- copycat/IP risk rationale
