# HTML Deconstruction Report Renderer Contract

## Role

Use this prompt when deciding what should appear in the human-readable HTML report. Do not ask a model to hand-code the final HTML report. The renderer in `src/creatives_analysis/html_report.py` owns HTML, CSS, escaping, and image placement.

## Inputs

- Validated deconstruct JSON matching `schemas/deconstruct_report.schema.json`.
- Evidence packet matching `schemas/evidence_packet.schema.json`.
- Submagic report brand kit from `research/submagic_report_brand_kit.md`.
- HTML report guidelines from `research/html_report_template_guidelines.md`.

## Output

The deterministic renderer should produce one `.html` file per deconstruction task.

Required first-order report sections:

1. Minimal hero with contextual creative label and core thesis only.
2. Why this creative exists: one hypothesis card plus compact facts for audience, funnel stage, likely KPI, awareness, confidence.
3. Creative mechanism: shot-backed narrative steps with beat annotations below each shot and semantic color coding for hook, pain, proof, CTA, and risk.
4. Core Read: core thesis, belief shift, and Submagic transfer.
5. What to steal / what not to copy / what to test next.
6. Top diagnostics: strongest signals, weakest signals, and proof gap.

Required second-order collapsed sections:

- Key shots: selected visual beats paired with concise interpretation.
- Contact sheet when a contact-sheet artifact exists.
- Full evidence timeline with shot, what happens, why it works, mechanism, and evidence sources.
- Full proof ladder.
- Creative intent evidence: offer strategy, marketer job-to-be-done, unknowns, and evidence IDs.
- Core-understanding notes: human truth, skeptic read, counterfactuals, tension stack, viewer-state timeline.
- Full score matrix.
- Platform fit.
- Drop-off and risk notes.

## Report Compression Policy

The HTML report is a review dashboard, not a complete dump of every field.

First-order visible sections:

1. Why this creative exists
2. Core thesis
3. Creative mechanism
4. What to steal / what not to copy / what to test
5. Top diagnostics

Second-order collapsed sections:

- Key shots
- Full evidence timeline
- Full proof ladder
- Full score matrix
- Platform fit
- Drop-off and risk notes
- Raw evidence IDs

Visible prose should read like a strategy memo. Hide raw evidence IDs and long supporting reasoning inside `<details>`.

## Rules For Report Content

- The HTML report may rearrange and format source data, but it may not add new analysis.
- The report must show the likely creative hypothesis before the core read.
- Short metadata should render as compact facts, not as large equal-height cards.
- `evidence_timeline[*].narrative_function` should drive the color coding when supplied. If missing, the renderer may use a deterministic keyword fallback.
- Every rendered score must keep its evidence IDs available in collapsed details.
- Every rendered timeline card should try to show the first keyframe or scene artifact attached to its evidence IDs.
- Mechanism step labels, narrative function, and mechanism summaries should render below the shot, not as overlays.
- Do not truncate first-order Creative mechanism annotations; use wider cards instead of hiding meaning-bearing text.
- If no visual artifact exists, render an explicit empty state: `No shot available for this beat`.
- Use a Submagic-style light report surface: warm off-white background, white cards, black headline text, orange accent, muted gray support copy.
- Shot `alt` text should include the timestamp and adjacent observation.
- Never render raw JSON as a substitute for editorial hierarchy.
- Never remove confidence labels or risk notes; they may be placed in collapsed second-order sections.
- Never convert creative-signal scores into performance claims.
- Keep raw evidence IDs in collapsible details. The first-order reading flow should show source counts or short source labels, not long ID strings.

## Report Quality Checklist

- Can a reviewer understand the hook problem in less than 20 seconds?
- Can a reviewer understand why the advertiser likely made the creative before reading the shot-by-shot analysis?
- Does each important interpretation sit next to the shot that supports it?
- Are missing evidence and weak confidence visible?
- Could the report be discussed by a strategist, creative director, and editor without opening the JSON first?
- Does it feel like a Submagic-adjacent creator tool rather than a generic analytics dump?
- Does the page reveal the underlying human truth and proof ladder, not just the beat sequence?
