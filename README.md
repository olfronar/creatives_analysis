# Creative Deconstruction Workspace

Reusable workspace for evidence-first competitor video deconstruction and Submagic adaptation brainstorming.

The project turns competitor short-form video creatives into structured evidence, then uses that evidence to support two later outputs:

- `deconstruct` - precise creative deconstruction of competitor ads.
- `adapt` - Submagic-native adaptation ideas for creators and agencies.

V1 is intentionally infrastructure-first. It creates the research notes, prompt contracts, rubrics, schemas, extraction tooling, and HTML report renderer needed for later analysis, but it does not generate deconstruct or adapt reports for the existing `creatives/ad1.mp4` through `creatives/ad5.mp4` files unless a deconstruction task is explicitly run.

## Principles

- Use `uv` strictly for Python dependency management and execution.
- Do not use `pip`, Conda, Poetry, or `python -m venv`.
- Treat creative scores as inferred creative-signal judgments unless platform metrics are provided.
- Every future deconstruction claim must cite timestamped evidence.
- Human-readable HTML reports are presentation artifacts over validated JSON and evidence packets.
- Deconstruction reports must explain why the creative was likely made before explaining how it works.
- Deconstruction reports must include a core-understanding layer, not only timeline summaries and scores.
- Adapt competitor tactics into Submagic-native strategy. Do not copy scripts, visuals, brand identity, claims, music, or creator likeness.

## What Is Included

- Source competitor videos in `creatives/`.
- Research notes on creative deconstruction, Submagic positioning, and the proposed pipeline.
- Prompt modules for evidence extraction, deconstruction, adaptation, validation, and synthesis.
- Rubrics for short-form creative quality, platform fit, and Submagic adaptation.
- JSON schemas and sample fixtures for evidence packets, reports, variants, and validation results.
- Python CLI tooling for environment checks, metadata inventory, evidence extraction scaffolding, and schema validation.
- A deterministic HTML deconstruction report renderer that pairs timeline insights with evidence shots, contact sheets, proof ladders, and Submagic-transfer notes when evidence is available.
- A stricter artifact graph: evidence IDs, cold-watch perception, mechanism deconstruction, Submagic proof scenes, swappability checks, and schema-backed validation.

## Setup

```bash
uv sync
```

`uv` creates and manages the local environment. Do not activate or manage the environment with other Python package tools.

## Commands

```bash
uv run creatives-doctor
uv run creatives-inventory
uv run creatives-inventory --json
uv run creatives-extract --video creatives/ad1.mp4
uv run creatives-validate
uv run creatives-render-report --deconstruct outputs/ad1/reports/deconstruct.json --evidence outputs/ad1/evidence/evidence_packet.json --output outputs/ad1/reports/deconstruct.html
```

Command purpose:

- `creatives-doctor` verifies system tools and Python dependencies.
- `creatives-inventory` reads MP4 metadata without generating reports.
- `creatives-extract` writes evidence artifacts under `outputs/<video-id>/evidence/`.
- `creatives-validate` validates sample fixtures against JSON schemas.
- `creatives-render-report` writes a concise HTML report from an existing deconstruct JSON file and evidence packet.

`creatives-extract` does not write deconstruction or adaptation reports.
`creatives-render-report` does not create analysis; it only formats validated report data for review.

The HTML report is intentionally distilled. It shows the strategic read first and hides raw evidence, full score matrices, and platform details in expandable sections. If a report feels long, fix the JSON prompt or renderer hierarchy rather than adding more visible blocks.

Deconstruct JSON must include `creative_intent`: creative label, creative type, likely hypothesis, target audience, awareness stage, funnel stage, likely KPI, offer strategy, marketer job-to-be-done, evidence IDs, confidence, and unknowns.

Deconstruct JSON must include `distilled_core`: core thesis, mechanism formula, belief-shift summary, why it works, where it breaks, Submagic transfer, what to steal, what to avoid, and what to test next.

Deconstruct JSON must include `core_understanding`: human truth, belief shift, tension stack, proof ladder, viewer-state timeline, skeptic read, Submagic transfer principle, and counterfactuals.

## Workspace Map

- `creatives/` - source competitor MP4 files.
- `research/` - source-cited research notes.
- `prompts/` - reusable prompt modules.
- `rubrics/` - scoring and judgment rubrics.
- `schemas/` - JSON contracts for evidence, reports, variants, and validation.
- `templates/html/` - structural HTML report template guide.
- `src/creatives_analysis/` - `uv`-run Python tooling.
- `tests/fixtures/` - schema sample fixtures.
- `outputs/` - future generated evidence and reports.

## Research Anchors

The current workspace is grounded in official platform guidance and product research:

- [Google Ads: ABCDs of effective video ads](https://support.google.com/google-ads/answer/14783551)
- [TikTok Creative Codes](https://ads.tiktok.com/business/en-GB/creative-codes)
- [TikTok Creative Insights](https://ads.us.tiktok.com/help/article/creative-insights?lang=en)
- [Submagic](https://www.submagic.co/)
- [Submagic API](https://docs.submagic.co/introduction)
- [HF Papers: VideoAds](https://hf.co/papers/2504.09282)
- [HF Papers: E-VAds](https://hf.co/papers/2602.08355)
- [HF Papers: MMPersuade](https://hf.co/papers/2510.22768)
- [HF Papers: AdTEC](https://hf.co/papers/2408.05906)
- [HF Papers: Creative Preference Optimization](https://hf.co/papers/2505.14442)
- [HF Papers: AD-Bench](https://hf.co/papers/2602.14257)
- [HF Papers: Long-Term Ad Memorability](https://hf.co/papers/2309.00378)

## Verification

```bash
uv run pytest
uv run creatives-doctor
uv run creatives-inventory
uv run creatives-validate
uv run creatives-render-report --deconstruct tests/fixtures/deconstruct_report.sample.json --evidence tests/fixtures/evidence_packet.sample.json --output /tmp/deconstruct_report.html
```

The expected default state is that `outputs/` contains no generated reports until an explicit extraction, deconstruction, or render command is run.
