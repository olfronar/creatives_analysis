# Core Understanding HTML Distillation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade deconstruction output so the first screen gives a compact strategic read, while deeper evidence remains available in collapsed details.

**Architecture:** Keep validated JSON plus evidence packets as the source of truth. Add a small distilled layer to the deconstruct schema, then make `src/creatives_analysis/html_report.py` render a first-order Submagic-style review dashboard with second-order details hidden behind accordions. Prompts and rubrics should teach the model to produce the distilled layer rather than relying on the renderer to infer strategy from long prose.

**Tech Stack:** Python standard library HTML rendering, JSON Schema 2020-12, pytest, jsonschema, `uv` only for dependency sync and command execution.

---

## File Structure

- Modify `schemas/deconstruct_report.schema.json`
  - Add required `distilled_core` object above `core_understanding`.
  - Enforce short, decision-oriented fields for the visible report surface.
- Modify `tests/fixtures/deconstruct_report.sample.json`
  - Add a realistic `distilled_core` fixture.
- Modify `tests/test_validate.py`
  - Add rejection tests for missing or shallow `distilled_core`.
- Modify `tests/test_html_report.py`
  - Add tests for compact first-order sections, hidden details, and no noisy evidence IDs in visible prose.
- Modify `src/creatives_analysis/html_report.py`
  - Split report rendering into first-order sections and collapsed detail sections.
  - Add helpers for score diagnostics, key-shot selection, evidence redaction, and compact mechanism rendering.
- Modify `prompts/deconstruction/deconstruct_report.md`
  - Require `distilled_core` and define the compression rules.
- Modify `prompts/reporting/html_deconstruction_report.md`
  - Update the report policy so HTML is a review dashboard, not a document dump.
- Modify `rubrics/short_form_creative_rubric.md`
  - Add scoring guidance for core thesis, proof debt, and transferability.
- Modify `research/html_report_template_guidelines.md`
  - Document the first-order / second-order information hierarchy.
- Modify `research/submagic_report_brand_kit.md`
  - Add report-specific usage rules based on Submagic's light/orange site direction.
- Modify `README.md`
  - Document the distilled report contract and render command.
- Modify `AGENTS.md`
  - Add durable guidance for future agents: no inline evidence-ID noise, no all-fields-visible reports.

---

### Task 1: Schema Contract For Distilled Core

**Files:**
- Modify: `schemas/deconstruct_report.schema.json`
- Modify: `tests/fixtures/deconstruct_report.sample.json`
- Modify: `tests/test_validate.py`

- [ ] **Step 1: Write a failing validation test for missing `distilled_core`**

Add this test to `tests/test_validate.py`:

```python
def test_deconstruct_schema_requires_distilled_core() -> None:
    schema = json.loads(Path("schemas/deconstruct_report.schema.json").read_text())
    sample = json.loads(Path("tests/fixtures/deconstruct_report.sample.json").read_text())
    sample.pop("distilled_core", None)

    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(sample))

    assert any("distilled_core" in error.message for error in errors)
```

- [ ] **Step 2: Write a failing validation test for shallow `distilled_core`**

Add this test to `tests/test_validate.py`:

```python
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
```

- [ ] **Step 3: Run the new tests and verify they fail**

Run:

```bash
uv run pytest tests/test_validate.py::test_deconstruct_schema_requires_distilled_core tests/test_validate.py::test_deconstruct_schema_rejects_empty_distilled_core_fields -v
```

Expected: both tests fail because the schema does not yet define `distilled_core`.

- [ ] **Step 4: Add `distilled_core` to the schema**

In `schemas/deconstruct_report.schema.json`, add `"distilled_core"` to the top-level `required` array immediately after `"core_mechanism"`.

Add this property next to `core_mechanism` and `core_understanding`:

```json
"distilled_core": {
  "type": "object",
  "additionalProperties": false,
  "required": [
    "core_thesis",
    "mechanism_formula",
    "belief_shift_summary",
    "why_it_works",
    "where_it_breaks",
    "submagic_transfer",
    "steal",
    "avoid",
    "test_next"
  ],
  "properties": {
    "core_thesis": { "type": "string", "minLength": 24, "maxLength": 240 },
    "mechanism_formula": { "type": "string", "minLength": 12, "maxLength": 180 },
    "belief_shift_summary": { "type": "string", "minLength": 24, "maxLength": 220 },
    "why_it_works": { "type": "string", "minLength": 24, "maxLength": 220 },
    "where_it_breaks": { "type": "string", "minLength": 24, "maxLength": 220 },
    "submagic_transfer": { "type": "string", "minLength": 24, "maxLength": 260 },
    "steal": {
      "type": "array",
      "minItems": 1,
      "maxItems": 3,
      "items": { "type": "string", "minLength": 12, "maxLength": 140 }
    },
    "avoid": {
      "type": "array",
      "minItems": 1,
      "maxItems": 3,
      "items": { "type": "string", "minLength": 12, "maxLength": 140 }
    },
    "test_next": {
      "type": "array",
      "minItems": 1,
      "maxItems": 3,
      "items": { "type": "string", "minLength": 12, "maxLength": 160 }
    }
  }
}
```

- [ ] **Step 5: Add `distilled_core` to the fixture**

In `tests/fixtures/deconstruct_report.sample.json`, add:

```json
"distilled_core": {
  "core_thesis": "The creative turns a familiar editing bottleneck into a visible before-after promise that makes speed feel believable.",
  "mechanism_formula": "raw-work pain -> visible transformation -> workflow compression -> action prompt",
  "belief_shift_summary": "The viewer moves from 'this clip still needs too much work' to 'this can become publishable with a faster editing system.'",
  "why_it_works": "It anchors the promise in a concrete workflow pain before asking the viewer to believe the product claim.",
  "where_it_breaks": "The proof weakens if the finished edited output is not shown clearly enough before the viewer loses patience.",
  "submagic_transfer": "Show raw footage becoming a captioned, cut, zoomed, publishable short inside the first few seconds.",
  "steal": [
    "Open on a creator pain that is already emotionally expensive.",
    "Make the transformation visual before explaining features."
  ],
  "avoid": [
    "Do not copy competitor wording, visuals, claims, creator likeness, or music.",
    "Do not let feature lists replace visible before-after proof."
  ],
  "test_next": [
    "Test a first-three-seconds before-after edit reveal against a pain-only hook."
  ]
}
```

- [ ] **Step 6: Verify schema tests pass**

Run:

```bash
uv run pytest tests/test_validate.py -v
```

Expected: all validation tests pass.

- [ ] **Step 7: Commit**

```bash
git add schemas/deconstruct_report.schema.json tests/fixtures/deconstruct_report.sample.json tests/test_validate.py
git commit -m "feat: add distilled core report contract"
```

---

### Task 2: HTML Tests For Distilled First Screen

**Files:**
- Modify: `tests/test_html_report.py`

- [ ] **Step 1: Update the sample deconstruct object**

Add the same `distilled_core` object from Task 1 to `_sample_deconstruct()` in `tests/test_html_report.py`.

- [ ] **Step 2: Add a test for the compact first-order report**

Add:

```python
def test_render_deconstruction_html_has_distilled_first_order_sections() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert "Core thesis" in html
    assert "Creative mechanism" in html
    assert "What to steal" in html
    assert "What not to copy" in html
    assert "Test next" in html
    assert "Full evidence timeline" in html
    assert "Full score matrix" in html
```

- [ ] **Step 3: Add a test that visible prose hides raw evidence IDs**

Add:

```python
def test_render_deconstruction_html_hides_evidence_ids_outside_details() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())
    before_first_details = html.split("<details", 1)[0]

    assert "ev_keyframe_001" not in before_first_details
    assert "ev_ocr_001" not in before_first_details
    assert "Evidence sources" in html
```

- [ ] **Step 4: Add a test that timeline is compressed by default**

Add:

```python
def test_render_deconstruction_html_uses_compact_key_shots_not_full_timeline_first() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert "Key shots" in html
    assert "Full evidence timeline" in html
    assert html.index("Key shots") < html.index("Full evidence timeline")
```

- [ ] **Step 5: Run the HTML tests and verify they fail**

Run:

```bash
uv run pytest tests/test_html_report.py -v
```

Expected: failures for missing distilled sections and visible evidence-ID behavior.

- [ ] **Step 6: Commit failing tests if working in strict TDD checkpoint mode**

Use this only if the team wants test-first commits:

```bash
git add tests/test_html_report.py
git commit -m "test: specify distilled html report layout"
```

---

### Task 3: Renderer Refactor To First-Order / Second-Order Layout

**Files:**
- Modify: `src/creatives_analysis/html_report.py`
- Test: `tests/test_html_report.py`

- [ ] **Step 1: Add helpers for distilled content**

Add these helpers near the existing render helpers:

```python
def _distilled_core(deconstruct: dict[str, Any]) -> dict[str, Any]:
    distilled = deconstruct.get("distilled_core")
    if isinstance(distilled, dict):
        return distilled

    core = deconstruct.get("core_understanding", {})
    mechanism = deconstruct.get("core_mechanism", {})
    belief_shift = core.get("belief_shift", {})
    return {
        "core_thesis": core.get("human_truth", ""),
        "mechanism_formula": mechanism.get("name", ""),
        "belief_shift_summary": " -> ".join(
            value for value in [
                str(belief_shift.get("before", "")),
                str(belief_shift.get("after", "")),
            ]
            if value
        ),
        "why_it_works": mechanism.get("why_it_might_persuade", ""),
        "where_it_breaks": core.get("skeptic_read", ""),
        "submagic_transfer": core.get("transfer_principle_for_submagic", ""),
        "steal": [],
        "avoid": [mechanism.get("what_cannot_be_copied", "")],
        "test_next": [],
    }
```

- [ ] **Step 2: Add compact list/card helpers**

Add:

```python
def _render_action_list(title: str, items: list[Any]) -> str:
    clean_items = [str(item) for item in items if str(item).strip()]
    if not clean_items:
        return _render_mini_card(title, "No recommendation supplied.")
    return (
        '<div class="mini-card">'
        f'<div class="label">{_text(title)}</div>'
        + _render_list(clean_items)
        + "</div>"
    )
```

- [ ] **Step 3: Add a diagnostic score splitter**

Add:

```python
def _top_score_diagnostics(scores: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    ranked = _rank_scores(scores)
    weaknesses = sorted(ranked, key=lambda item: (item.get("score", 0), item.get("dimension", "")))[:3]
    strengths = sorted(
        ranked,
        key=lambda item: (item.get("score", 0), item.get("confidence", "")),
        reverse=True,
    )[:3]
    return strengths, weaknesses
```

- [ ] **Step 4: Add a key-shot selector**

Add:

```python
def _key_timeline_items(items: list[dict[str, Any]], limit: int = 4) -> list[dict[str, Any]]:
    if len(items) <= limit:
        return items

    selected: list[dict[str, Any]] = []
    selected.append(items[0])
    middle = items[1:-1]
    if middle:
        step = max(1, len(middle) // max(1, limit - 2))
        selected.extend(middle[::step][: max(0, limit - 2)])
    selected.append(items[-1])
    return selected[:limit]
```

- [ ] **Step 5: Replace the current first-order sections in `render_deconstruction_html()`**

Inside `render_deconstruction_html()`, compute:

```python
distilled = _distilled_core(deconstruct)
scores = deconstruct.get("scores", [])
strengths, weaknesses = _top_score_diagnostics(scores)
key_timeline = _key_timeline_items(deconstruct.get("evidence_timeline", []))
key_shot_cards = "\n".join(
    _render_timeline_card(
        item,
        evidence_by_id,
        output_dir=output_dir,
        submagic_lesson=distilled.get("submagic_transfer", ""),
        compact=True,
    )
    for item in key_timeline
)
```

Then restructure the HTML body to this order:

```html
<section class="hero">...</section>
<section class="section core-thesis-section">Core thesis...</section>
<section class="section">Creative mechanism...</section>
<section class="section">What to steal / What not to copy / Test next...</section>
<section class="section">Key shots...</section>
<section class="section">Top diagnostics...</section>
<section class="section details-hub">collapsed detail sections...</section>
```

- [ ] **Step 6: Add `compact` mode to `_render_timeline_card()`**

Change the signature:

```python
def _render_timeline_card(
    item: dict[str, Any],
    evidence_by_id: dict[str, dict[str, Any]],
    *,
    output_dir: Path | None,
    submagic_lesson: str,
    compact: bool = False,
) -> str:
```

In compact mode, render only:

```html
<h3>What happens</h3>
<p>...</p>
<h3>Why it works</h3>
<p>...</p>
<h3>Submagic lesson</h3>
<p>...</p>
```

Use the full mode only inside collapsed details.

- [ ] **Step 7: Move evidence IDs into details only**

Ensure `_render_evidence_summary()` is never called before the first `<details>` block. In compact cards, show a source count such as:

```python
source_count = len(evidence_items)
source_label = f"{source_count} evidence source{'s' if source_count != 1 else ''}"
```

Render that as visible text, not IDs.

- [ ] **Step 8: Add collapsed details hub**

Create details blocks in this order:

```html
<details>
  <summary>Full evidence timeline</summary>
  ...
</details>
<details>
  <summary>Full proof ladder</summary>
  ...
</details>
<details>
  <summary>Full score matrix</summary>
  ...
</details>
<details>
  <summary>Platform fit</summary>
  ...
</details>
<details>
  <summary>Drop-off and risk notes</summary>
  ...
</details>
```

- [ ] **Step 9: Run HTML tests**

Run:

```bash
uv run pytest tests/test_html_report.py -v
```

Expected: all HTML tests pass.

- [ ] **Step 10: Commit renderer changes**

```bash
git add src/creatives_analysis/html_report.py tests/test_html_report.py
git commit -m "feat: distill html deconstruction report"
```

---

### Task 4: Submagic-Aligned Visual Compression

**Files:**
- Modify: `src/creatives_analysis/html_report.py`
- Modify: `tests/test_html_report.py`

- [ ] **Step 1: Add a CSS regression test for old noise and current brand tokens**

Add to `tests/test_html_report.py`:

```python
def test_render_deconstruction_html_keeps_submagic_light_orange_direction() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert "#FF4F01" in html
    assert "#FFFCF7" in html
    assert "#D8FF3E" not in html
    assert "#8B5CF6" not in html
    assert "dark neon" not in html.lower()
```

- [ ] **Step 2: Add report metric strip CSS**

In the `<style>` block, add:

```css
.metric-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
  margin-top: 18px;
}
.metric {
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: 16px;
  background: var(--paper);
}
.metric strong {
  display: block;
  font-size: 24px;
  line-height: 1;
}
.details-hub details {
  border-top: 1px solid var(--line);
  padding: 14px 0;
}
.details-hub details:first-child {
  border-top: 0;
}
.mechanism-ladder {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
}
.mechanism-step {
  padding: 16px;
  border-radius: 18px;
  background: var(--accent-soft);
  border: 1px solid rgba(255, 79, 1, .20);
}
```

- [ ] **Step 3: Render a Submagic-style report metric strip**

Near the hero, render:

```html
<div class="metric-strip">
  <div class="metric"><strong>4</strong><span>key shots</span></div>
  <div class="metric"><strong>3</strong><span>strengths</span></div>
  <div class="metric"><strong>3</strong><span>weaknesses</span></div>
  <div class="metric"><strong>1</strong><span>transfer principle</span></div>
</div>
```

Compute the first number from `len(key_timeline)`.

- [ ] **Step 4: Render `mechanism_formula` as a ladder**

Split on `->` and render each step:

```python
def _render_mechanism_ladder(formula: str) -> str:
    steps = [step.strip() for step in formula.split("->") if step.strip()]
    if not steps:
        return f'<p class="muted">{_text(formula)}</p>'
    return (
        '<div class="mechanism-ladder">'
        + "".join(
            f'<div class="mechanism-step"><div class="label">Step {index}</div><p>{_text(step)}</p></div>'
            for index, step in enumerate(steps, start=1)
        )
        + "</div>"
    )
```

- [ ] **Step 5: Run visual/token tests**

Run:

```bash
uv run pytest tests/test_html_report.py -v
```

Expected: all tests pass.

- [ ] **Step 6: Commit visual compression**

```bash
git add src/creatives_analysis/html_report.py tests/test_html_report.py
git commit -m "style: align report layout with submagic review surface"
```

---

### Task 5: Prompt And Rubric Updates

**Files:**
- Modify: `prompts/deconstruction/deconstruct_report.md`
- Modify: `prompts/reporting/html_deconstruction_report.md`
- Modify: `rubrics/short_form_creative_rubric.md`

- [ ] **Step 1: Update the deconstruction prompt with `distilled_core` rules**

Add this section to `prompts/deconstruction/deconstruct_report.md` before the output schema instructions:

```markdown
## Distilled Core Requirement

Before writing detailed analysis, produce `distilled_core`. This is the first-order strategic read that the HTML report will show by default.

Rules:
- `core_thesis` must explain the creative's central persuasion idea in one sentence.
- `mechanism_formula` must use `->` to show the causal path, e.g. `pain trigger -> diagnostic escalation -> product proof -> urgency`.
- `belief_shift_summary` must describe the before/after belief change, not just summarize scenes.
- `why_it_works` must name the viewer psychology.
- `where_it_breaks` must name the main proof, trust, pacing, or audience-fit weakness.
- `submagic_transfer` must translate the mechanism to Submagic without copying competitor surface details.
- `steal`, `avoid`, and `test_next` must be action-oriented and short.

Do not include raw evidence IDs in `distilled_core` prose. Evidence belongs in detailed fields.
```

- [ ] **Step 2: Update reporting prompt with first-order / second-order hierarchy**

Add this to `prompts/reporting/html_deconstruction_report.md`:

```markdown
## Report Compression Policy

The HTML report is a review dashboard, not a complete dump of every field.

First-order visible sections:
1. Core thesis
2. Creative mechanism
3. What to steal / what not to copy / what to test
4. Key shots
5. Top diagnostics

Second-order collapsed sections:
- Full evidence timeline
- Full proof ladder
- Full score matrix
- Platform fit
- Drop-off and risk notes
- Raw evidence IDs

Visible prose should read like a strategy memo. Hide raw evidence IDs and long supporting reasoning inside `<details>`.
```

- [ ] **Step 3: Update creative rubric with deeper quality checks**

Add this to `rubrics/short_form_creative_rubric.md`:

```markdown
## Core-Understanding Quality Gate

A high-quality deconstruction must identify:
- The human truth the creative exploits.
- The belief shift it tries to create.
- The mechanism that moves attention into persuasion.
- The proof debt that may cause skepticism.
- The transferable principle that can become a Submagic-native creative.

Reject shallow reports that only describe what appears on screen or assign scores without explaining viewer psychology.
```

- [ ] **Step 4: Commit prompt and rubric updates**

```bash
git add prompts/deconstruction/deconstruct_report.md prompts/reporting/html_deconstruction_report.md rubrics/short_form_creative_rubric.md
git commit -m "docs: teach distilled core deconstruction"
```

---

### Task 6: Research, README, And Agent Guidance

**Files:**
- Modify: `research/html_report_template_guidelines.md`
- Modify: `research/submagic_report_brand_kit.md`
- Modify: `README.md`
- Modify: `AGENTS.md`

- [ ] **Step 1: Update HTML template guidelines**

Add:

```markdown
## First-Order / Second-Order Rule

The default HTML view should contain only the information needed for a human and Codex to discuss the creative productively:

- Core thesis
- Mechanism formula
- Transfer principle
- Top strengths
- Top weaknesses
- Key shots

Everything else is second-order and should be hidden in accordions. This includes full score matrices, raw evidence IDs, exhaustive viewer-state timelines, platform notes, and long risk lists.
```

- [ ] **Step 2: Update Submagic brand kit**

Add:

```markdown
## Report Brand Application

Reports should borrow Submagic's public-site discipline rather than only its colors:

- Light warm background.
- White rounded cards.
- Black headline text.
- Orange accent for primary emphasis.
- Short confident copy.
- Sparse first screen.
- Visual proof before dense explanation.

Avoid dark neon shells, purple/lime accents, excessive card grids, and long visible evidence strings.
```

- [ ] **Step 3: Update README command explanation**

In `README.md`, near the `creatives-render-report` command, add:

```markdown
The HTML report is intentionally distilled. It shows the strategic read first and hides raw evidence, full score matrices, and platform details in expandable sections. If a report feels long, fix the JSON prompt or renderer hierarchy rather than adding more visible blocks.
```

- [ ] **Step 4: Update AGENTS guidance**

In `AGENTS.md`, add:

```markdown
## HTML Report Rules

- Keep reports concise by default.
- Do not expose raw evidence IDs in first-order prose.
- Show key shots near the strategic insight.
- Hide full timelines, platform notes, score matrices, and evidence IDs in details blocks.
- Preserve Submagic's light/orange, clean creator-productivity tone.
```

- [ ] **Step 5: Commit docs**

```bash
git add research/html_report_template_guidelines.md research/submagic_report_brand_kit.md README.md AGENTS.md
git commit -m "docs: document distilled html report contract"
```

---

### Task 7: End-To-End Verification

**Files:**
- No new files.
- Verify generated temporary report only under `/private/tmp`.

- [ ] **Step 1: Run full test suite**

Run:

```bash
uv run pytest
```

Expected: all tests pass.

- [ ] **Step 2: Validate fixtures**

Run:

```bash
uv run creatives-validate
```

Expected: every fixture prints `PASS`.

- [ ] **Step 3: Render sample report to `/private/tmp`**

Run:

```bash
uv run creatives-render-report --deconstruct tests/fixtures/deconstruct_report.sample.json --evidence tests/fixtures/evidence_packet.sample.json --output /private/tmp/deconstruct_report.html
```

Expected: command prints `/private/tmp/deconstruct_report.html`.

- [ ] **Step 4: Check required report text**

Run:

```bash
rg -n "Core thesis|Creative mechanism|What to steal|What not to copy|Full evidence timeline|Full score matrix" /private/tmp/deconstruct_report.html
```

Expected: every required phrase appears.

- [ ] **Step 5: Check old colors are absent**

Run:

```bash
rg -n "#D8FF3E|#8B5CF6|dark neon" /private/tmp/deconstruct_report.html
```

Expected: no matches.

- [ ] **Step 6: Check workspace output remains ignored**

Run:

```bash
git status --short --ignored outputs
```

Expected: `outputs/` is ignored and no generated report is staged.

- [ ] **Step 7: Check formatting whitespace**

Run:

```bash
git diff --check
```

Expected: no whitespace errors.

- [ ] **Step 8: Final commit if previous tasks were not committed incrementally**

Only if changes were not already committed task-by-task:

```bash
git add AGENTS.md README.md prompts/deconstruction/deconstruct_report.md prompts/reporting/html_deconstruction_report.md research/html_report_template_guidelines.md research/submagic_report_brand_kit.md rubrics/short_form_creative_rubric.md schemas/deconstruct_report.schema.json src/creatives_analysis/html_report.py tests/fixtures/deconstruct_report.sample.json tests/test_html_report.py tests/test_validate.py
git commit -m "feat: distill core understanding html reports"
```

---

## Self-Review Checklist

- Spec coverage:
  - Deeper core-understanding analysis is covered by `distilled_core`, prompt rules, and rubric quality gates.
  - Visual compression is covered by first-order sections, details hub, key shots, score splitting, and Submagic brand CSS.
  - Brand following is covered by report-specific brand-kit guidance and token tests.
  - Unnecessary blocks are handled by moving full timelines, scorecards, platform notes, and raw evidence IDs into accordions.

- Placeholder scan:
  - No task uses TBD/TODO/fill-in language.
  - Every implementation task names exact files and verification commands.

- Type consistency:
  - `distilled_core` is used consistently across schema, fixtures, tests, prompts, and renderer.
  - Renderer fallback keeps older reports readable while schema requires the new field for future validated reports.

---

## Execution Options

Plan complete. Recommended execution path:

1. **Subagent-Driven**: one fresh subagent per task with review between tasks.
2. **Inline Execution**: execute the tasks in this session with verification checkpoints.
