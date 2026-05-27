# Creative Deconstruction Workspace

Reusable workspace for evidence-first competitor video deconstruction and Submagic adaptation brainstorming.

The project turns competitor short-form video creatives into structured evidence, then uses that evidence to support two later outputs:

- `deconstruct` - precise creative deconstruction of competitor ads.
- `adapt` - Submagic-native adaptation ideas for creators and agencies.

V1 is intentionally build-only. It creates the research notes, prompt contracts, rubrics, schemas, and extraction tooling needed for later analysis, but it does not generate deconstruct or adapt reports for the existing `creatives/ad1.mp4` through `creatives/ad5.mp4` files.

## Principles

- Use `uv` strictly for Python dependency management and execution.
- Do not use `pip`, Conda, Poetry, or `python -m venv`.
- Treat creative scores as inferred creative-signal judgments unless platform metrics are provided.
- Every future deconstruction claim must cite timestamped evidence.
- Adapt competitor tactics into Submagic-native strategy. Do not copy scripts, visuals, brand identity, claims, music, or creator likeness.

## What Is Included

- Source competitor videos in `creatives/`.
- Research notes on creative deconstruction, Submagic positioning, and the proposed pipeline.
- Prompt modules for evidence extraction, deconstruction, adaptation, validation, and synthesis.
- Rubrics for short-form creative quality, platform fit, and Submagic adaptation.
- JSON schemas and sample fixtures for evidence packets, reports, variants, and validation results.
- Python CLI tooling for environment checks, metadata inventory, evidence extraction scaffolding, and schema validation.

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
```

Command purpose:

- `creatives-doctor` verifies system tools and Python dependencies.
- `creatives-inventory` reads MP4 metadata without generating reports.
- `creatives-extract` writes evidence artifacts under `outputs/<video-id>/evidence/`.
- `creatives-validate` validates sample fixtures against JSON schemas.

`creatives-extract` does not write deconstruction or adaptation reports.

## Workspace Map

- `creatives/` - source competitor MP4 files.
- `research/` - source-cited research notes.
- `prompts/` - reusable prompt modules.
- `rubrics/` - scoring and judgment rubrics.
- `schemas/` - JSON contracts for evidence, reports, variants, and validation.
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
- [HF Papers: Long-Term Ad Memorability](https://hf.co/papers/2309.00378)

## Verification

```bash
uv run pytest
uv run creatives-doctor
uv run creatives-inventory
uv run creatives-validate
```

The expected build-only state is that `outputs/` contains no generated reports.
