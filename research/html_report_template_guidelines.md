# HTML Deconstruction Report Guidelines

## Purpose

The HTML report exists so a human and Codex can review one creative together without reading raw JSON. It is a presentation layer over the structured `deconstruct` report and evidence packet. It must not introduce new analysis, new scores, or claims that are absent from the validated source files.

## Best Place In The Pipeline

Render HTML after these steps are complete:

1. Evidence extraction writes `outputs/<video-id>/evidence/evidence_packet.json`.
2. The deconstruction task writes a JSON report compatible with `schemas/deconstruct_report.schema.json`.
3. Validation confirms schema validity and evidence-ID resolution.
4. `creatives-render-report` renders the HTML from the validated JSON plus evidence packet.

Do not generate HTML inside the extraction step. Extraction should remain evidence-only. Do not ask the model to write final HTML. The model should write structured JSON; the deterministic renderer should handle layout, escaping, screenshots, and formatting.

## Template Principles

The report should be concise but detail-forming:

- Put the core thesis, mechanism formula, and adaptation implication above the fold.
- Put the likely campaign hypothesis, audience, funnel stage, and KPI before the core read so reviewers understand why the creative likely exists; render metadata as compact facts, not large equal-height cards.
- Put the deeper core read above the timeline: belief shift, proof gap, and Submagic transfer.
- Show a compact shot-backed creative mechanism near the top. It should reveal the visual arc and mechanism steps in one section.
- Color-code mechanism steps by narrative function: hook, pain, proof, CTA, and risk.
- Put selected key shots in the details hub before the full evidence timeline, so reviewers can expand the strongest visual proof without making the default page heavy.
- Keep the sampled contact sheet available when present, but treat it as second-order context if it makes the page feel heavy.
- Pair each selected timeline beat with a keyframe or scene image when available.
- Keep interpretation next to the image that supports it.
- Do not truncate first-order Creative mechanism annotations. They are compact but meaning-bearing, and should remain readable under the shot.
- Hide raw evidence IDs in collapsible details.
- Show top strengths and top weaknesses first; move the full ranked diagnostic score table into details.
- Keep uncertainty visible with confidence labels and risk notes.
- Do not dump JSON, transcripts, or full OCR output into the report body.

## First-Order / Second-Order Rule

The default HTML view should contain only the information needed for a human and Codex to discuss the creative productively:

- Core thesis
- Creative intent: likely hypothesis, audience, funnel stage, KPI, confidence
- Mechanism formula
- Transfer principle
- Top strengths
- Top weaknesses
- Shot-backed mechanism sequence

Everything else is second-order and should be hidden in accordions. This includes key-shot cards, full score matrices, raw evidence IDs, exhaustive viewer-state timelines, platform notes, and long risk lists.

## "Show, Do Not Tell" In This Workspace

For creative deconstruction, "show, do not tell" means:

- A hook critique should show the first shot or first caption.
- A visual memorability critique should show the frame being discussed.
- A pacing critique should show a sequence of beats or at least their timestamped cards.
- A CTA critique should show the CTA frame or state that no CTA shot was available.
- A product-integration critique should show the moment when the product appears or the absence of that moment.
- Mechanism step labels, narrative function, and mechanism summaries must sit below the shots in a separate caption band, never over the image itself.
- Mechanism cards should be wide enough for readable annotations; prefer fewer columns over cramped captions.

If no shot exists for a claim, the report should expose the gap instead of pretending the visual proof exists.

## Accessibility And Readability

Use informative images only where they help analysis. Each shot image should have an `alt` attribute that states the timestamp and the adjacent observation. If the image is redundant to nearby text, the alt text can be short. Follow W3C and GOV.UK guidance: images should not carry information that is unavailable in text, and color should not be the only way to understand meaning.

Layout constraints:

- Use a single-column flow on narrow screens.
- Keep body text at readable sizes.
- Use high contrast for text and chips.
- Keep headings descriptive and scannable.
- Avoid large card grids for short metadata. If the text is a label/value pair, use compact facts or a table-like grid.
- Avoid visual effects that obscure evidence.
- Make print output usable enough for a PDF export.

## Required Sections

1. Hero: contextual creative label and core thesis only.
2. Why this creative exists: hypothesis, audience, funnel, likely KPI, awareness, confidence.
3. Creative mechanism: selected shots plus mechanism annotations and narrative-function color coding.
4. Core Read: core thesis, belief shift, Submagic transfer.
5. What to steal / what not to copy / what to test next.
6. Top diagnostics: top strengths, top weaknesses, proof gap.
7. Details: key shots, creative intent evidence, contact sheet, full evidence timeline, proof ladder, core-understanding notes, score matrix, platform fit, drop-off, and risk notes.

## Brand Direction

Default reports should follow Submagic's current public-product feel: light background, white cards, black headline typography, orange accent, muted gray body copy, rounded upload-card-like surfaces, and creator-productivity language. Avoid the previous dark lime/purple report theme unless a specific future brand guide requires it.

## Sources

- [Nielsen Norman Group visual design principles](https://media.nngroup.com/media/articles/attachments/Principles_Visual_Design-A4.pdf)
- [Michelin Design System dashboard principles](https://designsystem.michelin.com/data-visualization/design-guidelines/principles-of-a-dashboard)
- [GOV.UK Design System image guidance](https://design-system.service.gov.uk/styles/images/)
- [W3C WAI alt decision tree](https://www.w3.org/WAI/tutorials/images/decision-tree/)
