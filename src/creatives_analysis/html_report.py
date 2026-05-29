from __future__ import annotations

import json
import os
import re
from html import escape
from pathlib import Path
from typing import Any


SUBMAGIC_REPORT_BRAND = {
    "product": "Submagic",
    "accent": "#FF4F01",
    "accent_soft": "#FFF2EA",
    "ink": "#0B0B0D",
    "muted": "#5F5F6D",
    "line": "#ECECEF",
    "paper": "#FFFFFF",
    "shell": "#FFFCF7",
    "soft": "#F7F7F8",
    "deep": "#26211F",
}


def write_deconstruction_html_report(
    *,
    deconstruct_path: Path,
    evidence_path: Path,
    output_path: Path,
) -> Path:
    deconstruct = json.loads(deconstruct_path.read_text())
    evidence = json.loads(evidence_path.read_text())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    html = render_deconstruction_html(
        deconstruct,
        evidence,
        output_dir=output_path.parent,
    )
    output_path.write_text(_strip_trailing_whitespace(html))
    return output_path


def render_deconstruction_html(
    deconstruct: dict[str, Any],
    evidence: dict[str, Any],
    *,
    output_dir: Path | None = None,
    brand: dict[str, str] = SUBMAGIC_REPORT_BRAND,
) -> str:
    evidence_by_id = _index_evidence(evidence)
    video_id = _text(deconstruct.get("video_id", "unknown_video"))
    mechanism = deconstruct.get("core_mechanism", {})
    core = deconstruct.get("core_understanding", {})
    creative_intent = _creative_intent(deconstruct)
    distilled = _distilled_core(deconstruct)
    scores = deconstruct.get("scores", [])
    strengths, weaknesses = _top_score_diagnostics(scores)
    transfer = distilled.get("submagic_transfer", "") or core.get(
        "transfer_principle_for_submagic", ""
    )
    contact_sheet = _contact_sheet_src(evidence, output_dir=output_dir)
    key_timeline = _key_timeline_items(deconstruct.get("evidence_timeline", []))
    mechanism_timeline = _mechanism_timeline_items(deconstruct.get("evidence_timeline", []))
    report_title = _text(
        creative_intent.get("creative_label")
        or f"{deconstruct.get('video_id', 'unknown_video')} Creative Deconstruction"
    )
    key_shot_cards = "\n".join(
        _render_timeline_card(
            item,
            evidence_by_id,
            output_dir=output_dir,
            submagic_lesson=transfer,
            compact=True,
        )
        for item in key_timeline
    )
    mechanism_filmstrip = _render_mechanism_filmstrip(
        mechanism_timeline,
        evidence_by_id,
        output_dir=output_dir,
    )
    timeline_cards = "\n".join(
        _render_timeline_card(
            item,
            evidence_by_id,
            output_dir=output_dir,
            submagic_lesson=transfer,
            compact=False,
        )
        for item in deconstruct.get("evidence_timeline", [])
    )
    score_rows = "\n".join(_render_score_row(item) for item in _rank_scores(scores))
    platform_cards = "\n".join(
        _render_platform_card(name, item)
        for name, item in deconstruct.get("platform_fit", {}).items()
    )
    contact_sheet_detail = _render_contact_sheet_detail(contact_sheet) if contact_sheet else ""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{report_title}</title>
  <style>
    :root {{
      --shell: {brand["shell"]};
      --paper: {brand["paper"]};
      --ink: {brand["ink"]};
      --muted: {brand["muted"]};
      --line: {brand["line"]};
      --soft: {brand["soft"]};
      --accent: {brand["accent"]};
      --accent-soft: {brand["accent_soft"]};
      --deep: {brand["deep"]};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--shell);
      color: var(--ink);
      font: 15px/1.55 Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    .shell {{ max-width: 1120px; margin: 0 auto; padding: 18px 16px 44px; }}
    .topbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      margin-bottom: 14px;
      color: var(--muted);
      font-weight: 700;
    }}
    .brand-mark {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      color: var(--ink);
      font-size: 19px;
      font-weight: 900;
    }}
    .brand-dot {{
      width: 30px;
      height: 30px;
      border-radius: 9px;
      background: var(--accent);
      box-shadow: 0 8px 24px rgba(255, 79, 1, .24);
    }}
    .hero {{
      padding: 24px 18px 22px;
      text-align: center;
      border-bottom: 1px solid var(--line);
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 12px;
      font-weight: 900;
      letter-spacing: .08em;
      text-transform: uppercase;
    }}
    h1, h2, h3, p {{ margin: 0; }}
    h1 {{
      margin: 8px auto 10px;
      max-width: 980px;
      font-size: clamp(30px, 3.8vw, 52px);
      line-height: 1.04;
      letter-spacing: 0;
    }}
    h2 {{ margin-bottom: 12px; font-size: 22px; letter-spacing: 0; }}
    h3 {{ font-size: 16px; letter-spacing: 0; }}
    .hero-copy {{
      max-width: 680px;
      margin: 0 auto;
      color: var(--muted);
      font-size: 16px;
    }}
    .section {{
      margin-top: 14px;
      padding: 18px;
      border-radius: 18px;
      background: var(--paper);
      border: 1px solid var(--line);
      box-shadow: 0 10px 28px rgba(38, 33, 31, .04);
    }}
    .core-read {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 12px;
    }}
    .intent-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 10px;
      align-items: start;
    }}
    .intent-card {{
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: var(--soft);
    }}
    .intent-card.primary {{
      background: var(--accent-soft);
      border-color: rgba(255, 79, 1, .24);
    }}
    .intent-card p {{
      margin-top: 8px;
    }}
    .intent-facts {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 8px;
      align-items: start;
    }}
    .intent-fact {{
      padding: 10px 12px;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: var(--soft);
    }}
    .intent-fact p {{
      margin-top: 4px;
      font-size: 14px;
      line-height: 1.42;
    }}
    .mechanism-filmstrip {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 10px;
    }}
    .function-legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 10px;
    }}
    .function-chip, .mechanism-kicker {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}
    .function-chip {{
      padding: 5px 8px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--paper);
    }}
    .function-dot {{
      width: 8px;
      height: 8px;
      border-radius: 999px;
      background: var(--function-accent);
      flex: 0 0 auto;
    }}
    .mechanism-card {{
      --function-accent: #7A7A86;
      --function-soft: var(--soft);
      display: grid;
      grid-template-rows: auto auto;
      align-content: start;
      border: 1px solid color-mix(in srgb, var(--function-accent) 38%, var(--line));
      border-radius: 14px;
      overflow: hidden;
      background: var(--paper);
    }}
    .function-hook, .function-cta {{ --function-accent: var(--accent); --function-soft: var(--accent-soft); }}
    .function-pain {{ --function-accent: #D97706; --function-soft: #FFF7E8; }}
    .function-proof {{ --function-accent: #2563EB; --function-soft: #EFF6FF; }}
    .function-risk {{ --function-accent: #DC2626; --function-soft: #FFF1F2; }}
    .mechanism-shot {{
      height: 220px;
      background: var(--deep);
      display: flex;
      align-items: center;
      justify-content: center;
      color: rgba(255,255,255,.72);
      overflow: hidden;
      flex: 0 0 auto;
    }}
    .mechanism-shot img {{
      width: auto;
      height: 100%;
      max-width: 100%;
      object-fit: cover;
      display: block;
    }}
    .mechanism-copy {{
      padding: 10px;
      background: linear-gradient(180deg, var(--function-soft), var(--paper) 78%);
      border-top: 1px solid var(--line);
    }}
    .mechanism-copy h3 {{
      margin-top: 6px;
      font-size: 13px;
      color: var(--muted);
    }}
    .mechanism-title {{
      margin-top: 4px;
      font-weight: 800;
      line-height: 1.25;
    }}
    .mechanism-note {{
      margin-top: 5px;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.35;
    }}
    .mini-card {{
      min-height: 0;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: var(--soft);
    }}
    .mini-card.accent {{
      background: var(--accent-soft);
      border-color: rgba(255, 79, 1, .24);
    }}
    .label, .timeline-meta, .chip, summary {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}
    .mini-card p {{ margin-top: 8px; }}
    .contact-sheet {{
      width: 100%;
      max-height: 520px;
      object-fit: contain;
      border-radius: 14px;
      border: 1px solid var(--line);
      background: var(--deep);
      display: block;
    }}
    .timeline {{
      display: grid;
      gap: 12px;
    }}
    .timeline-card {{
      display: grid;
      grid-template-columns: minmax(220px, 320px) minmax(0, 1fr);
      gap: 14px;
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 16px;
      background: #fff;
    }}
    .phone-frame {{
      padding: 8px;
      border-radius: 22px;
      background: var(--deep);
      box-shadow: inset 0 0 0 1px rgba(255,255,255,.08);
    }}
    .shot {{
      overflow: hidden;
      aspect-ratio: 9 / 16;
      border-radius: 14px;
      background: #151515;
      display: flex;
      align-items: center;
      justify-content: center;
      color: rgba(255,255,255,.78);
      text-align: center;
    }}
    .shot img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      background: #111;
      display: block;
    }}
    .timeline-copy {{ display: grid; gap: 10px; align-content: start; }}
    .timeline-copy p {{ color: #26262d; }}
    .story-grid, .platform-grid, .list-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 10px;
    }}
    .shift {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }}
    .chip-row {{ display: flex; flex-wrap: wrap; gap: 6px; }}
    .chip {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 4px 8px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: #8A2B00;
      text-transform: none;
      letter-spacing: 0;
    }}
    details {{
      padding-top: 2px;
    }}
    summary {{
      cursor: pointer;
    }}
    .details-hub details {{
      border-top: 1px solid var(--line);
      padding: 12px 0;
    }}
    .details-hub h2 + details {{
      border-top: 0;
      padding-top: 0;
    }}
    details ul {{ margin-top: 8px; }}
    table {{
      width: 100%;
      border-collapse: collapse;
    }}
    th, td {{
      padding: 12px 10px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
    }}
    th {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}
    .score-bar {{
      width: 92px;
      height: 9px;
      margin-top: 7px;
      border-radius: 999px;
      background: #F0F0F1;
      overflow: hidden;
    }}
    .score-bar-fill {{
      height: 100%;
      background: var(--accent);
      border-radius: inherit;
    }}
    .muted {{ color: var(--muted); }}
    ul {{ margin: 0; padding-left: 18px; }}
    li + li {{ margin-top: 7px; }}
    footer {{ color: var(--muted); margin-top: 18px; font-size: 13px; text-align: center; }}
    @media (max-width: 820px) {{
      .timeline-card, .shift, .intent-grid {{ grid-template-columns: 1fr; }}
      .intent-facts {{ grid-template-columns: 1fr; }}
      .hero, .section {{ padding: 18px; border-radius: 18px; }}
      .topbar {{ align-items: flex-start; flex-direction: column; }}
    }}
    @media print {{
      body {{ background: white; }}
      .shell {{ max-width: none; padding: 0; }}
      .section {{ box-shadow: none; break-inside: avoid; }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <div class="topbar">
      <div class="brand-mark"><span class="brand-dot"></span>{_text(brand["product"])}</div>
      <div>Creative intelligence report</div>
    </div>

    <section class="hero">
      <div class="eyebrow">Deconstruct</div>
      <h1>{report_title}</h1>
      <p class="hero-copy">{_text(distilled.get("core_thesis") or mechanism.get("why_it_catches_attention", "No mechanism summary supplied."))}</p>
    </section>

    <section class="section">
      <h2>Why this creative exists</h2>
      <div class="intent-grid">
        <article class="intent-card primary">
          <div class="label">Hypothesis</div>
          <p>{_text(creative_intent.get("likely_hypothesis", "Not supplied."))}</p>
        </article>
        <div class="intent-facts">
          {_render_intent_fact("Audience", creative_intent.get("target_audience"))}
          {_render_intent_fact("Funnel", creative_intent.get("funnel_stage"))}
          {_render_intent_fact("Likely KPI", creative_intent.get("likely_kpi"))}
          {_render_intent_fact("Awareness", creative_intent.get("awareness_stage"))}
          {_render_intent_fact("Confidence", creative_intent.get("confidence"))}
        </div>
      </div>
    </section>

    <section class="section">
      <h2>Creative mechanism</h2>
      {mechanism_filmstrip}
    </section>

    <section class="section core-thesis-section">
      <h2>Core Read</h2>
      <div class="core-read">
        {_render_mini_card("Core thesis", distilled.get("core_thesis", "No distilled thesis supplied."), accent=True)}
        {_render_mini_card("Belief shift", distilled.get("belief_shift_summary"), accent=True)}
        {_render_mini_card("Submagic transfer", transfer, accent=True)}
      </div>
    </section>

    <section class="section">
      <h2>What to steal / What not to copy</h2>
      <div class="story-grid">
        {_render_action_list("What to steal", distilled.get("steal", []))}
        {_render_action_list("What not to copy", distilled.get("avoid", []))}
        {_render_action_list("Test next", distilled.get("test_next", []))}
      </div>
    </section>

    <section class="section">
      <h2>Top diagnostics</h2>
      <div class="story-grid">
        {_render_score_cards("Top strengths", strengths)}
        {_render_score_cards("Top weaknesses", weaknesses)}
        {_render_mini_card("Proof gap", distilled.get("where_it_breaks") or _first_proof_gap(core) or core.get("skeptic_read"))}
      </div>
    </section>

    <section class="section details-hub">
      <h2>Details</h2>
      <details>
        <summary>Key shots</summary>
        <div class="timeline">
          {key_shot_cards}
        </div>
      </details>
      {contact_sheet_detail}
      <details>
        <summary>Creative intent evidence</summary>
        <div class="story-grid">
          {_render_mini_card("Offer strategy", creative_intent.get("offer_strategy"))}
          {_render_mini_card("Marketer job-to-be-done", creative_intent.get("marketer_job_to_be_done"))}
          {_render_action_list("Intent unknowns", creative_intent.get("unknowns", []))}
          <div class="mini-card"><div class="label">Intent evidence</div>{_render_evidence_details(creative_intent.get("evidence_ids", []))}</div>
        </div>
      </details>
      <details>
        <summary>Full evidence timeline</summary>
        <h3>Evidence timeline</h3>
        <div class="timeline">{timeline_cards}</div>
      </details>
      <details>
        <summary>Full proof ladder</summary>
        <h3>Proof ladder</h3>
        {_render_proof_ladder(core.get("proof_ladder", []))}
      </details>
      <details>
        <summary>Core-understanding notes</summary>
        <div class="story-grid">
          {_render_mini_card("Human truth", core.get("human_truth"))}
          {_render_mini_card("Skeptic read", core.get("skeptic_read"))}
          {_render_mini_card("Counterfactuals", _sentence_list(core.get("counterfactuals", [])))}
          {_render_mini_card("Tension stack", _sentence_list(core.get("tension_stack", [])))}
        </div>
        <h3>Viewer state timeline</h3>
        {_render_viewer_states(core.get("viewer_state_timeline", []))}
      </details>
      <details>
        <summary>Full score matrix</summary>
        <table>
          <thead>
            <tr><th>Dimension</th><th>Score</th><th>Weakness / next improvement</th><th>Evidence</th></tr>
          </thead>
          <tbody>{score_rows}</tbody>
        </table>
      </details>
      <details>
        <summary>Platform fit</summary>
        <div class="platform-grid">{platform_cards}</div>
      </details>
      <details>
        <summary>Drop-off and risk notes</summary>
        <div class="list-grid">
          <div class="mini-card"><div class="label">Likely drop-off points</div>{_render_list(deconstruct.get("drop_off_hypotheses", []))}</div>
          <div class="mini-card"><div class="label">Risks and unknowns</div>{_render_list(deconstruct.get("risks_and_unknowns", []))}</div>
        </div>
      </details>
    </section>

    <footer>
      Creative-signal report only. Use performance metrics before treating any score as proven market truth.
    </footer>
  </main>
</body>
</html>
"""


def _creative_intent(deconstruct: dict[str, Any]) -> dict[str, Any]:
    intent = deconstruct.get("creative_intent")
    if isinstance(intent, dict):
        return intent

    video_id = str(deconstruct.get("video_id", "unknown_video"))
    mechanism = deconstruct.get("core_mechanism", {})
    core = deconstruct.get("core_understanding", {})
    evidence_ids = []
    for item in deconstruct.get("evidence_timeline", [])[:1]:
        evidence_ids.extend(str(value) for value in item.get("evidence_ids", []))
    return {
        "creative_label": f"{video_id} Creative Deconstruction",
        "creative_type": "Short-form direct-response creative",
        "likely_hypothesis": mechanism.get(
            "why_it_might_persuade",
            "The creative is likely testing whether the hook can turn attention into product interest.",
        ),
        "target_audience": "Likely audience is inferred from the problem and offer shown in the creative.",
        "awareness_stage": "Inferred from visible claims only.",
        "funnel_stage": "Inferred creative-signal judgment.",
        "likely_kpi": "Click-through, conversion, CAC, or ROAS, depending on placement.",
        "offer_strategy": mechanism.get("why_it_catches_attention", ""),
        "marketer_job_to_be_done": core.get("transfer_principle_for_submagic", ""),
        "evidence_ids": evidence_ids or ["ev_manifest_000"],
        "confidence": "low",
        "unknowns": ["No media-buy, landing-page, or performance data was provided."],
    }


def _distilled_core(deconstruct: dict[str, Any]) -> dict[str, Any]:
    distilled = deconstruct.get("distilled_core")
    if isinstance(distilled, dict):
        return distilled

    core = deconstruct.get("core_understanding", {})
    mechanism = deconstruct.get("core_mechanism", {})
    belief_shift = core.get("belief_shift", {})
    before = str(belief_shift.get("before", "")).strip()
    after = str(belief_shift.get("after", "")).strip()
    return {
        "core_thesis": core.get("human_truth", ""),
        "mechanism_formula": mechanism.get("name", ""),
        "belief_shift_summary": " -> ".join(value for value in [before, after] if value),
        "why_it_works": mechanism.get("why_it_might_persuade", ""),
        "where_it_breaks": core.get("skeptic_read", ""),
        "submagic_transfer": core.get("transfer_principle_for_submagic", ""),
        "steal": [],
        "avoid": [mechanism.get("what_cannot_be_copied", "")],
        "test_next": [],
    }


def _top_score_diagnostics(
    scores: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    ranked = _rank_scores(scores)
    weaknesses = sorted(
        ranked,
        key=lambda item: (int(item.get("score", 0)), str(item.get("dimension", ""))),
    )[:3]
    strengths = sorted(
        ranked,
        key=lambda item: (
            int(item.get("score", 0)),
            str(item.get("confidence", "")),
            str(item.get("dimension", "")),
        ),
        reverse=True,
    )[:3]
    return strengths, weaknesses


def _key_timeline_items(
    items: list[dict[str, Any]],
    limit: int = 4,
) -> list[dict[str, Any]]:
    if len(items) <= limit:
        return items

    selected: list[dict[str, Any]] = [items[0]]
    middle = items[1:-1]
    if middle:
        step = max(1, len(middle) // max(1, limit - 2))
        selected.extend(middle[::step][: max(0, limit - 2)])
    selected.append(items[-1])
    return selected[:limit]


def _mechanism_timeline_items(
    items: list[dict[str, Any]],
    limit: int = 6,
) -> list[dict[str, Any]]:
    if len(items) <= limit:
        return items
    return _key_timeline_items(items, limit=limit)


def _index_evidence(evidence: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item["evidence_id"]): item
        for item in evidence.get("timeline_evidence", [])
        if "evidence_id" in item
    }


def _contact_sheet_src(evidence: dict[str, Any], *, output_dir: Path | None) -> str:
    artifacts = evidence.get("artifacts", {})
    artifact = artifacts.get("contact_sheet")
    if not artifact and artifacts.get("keyframes_dir"):
        artifact = str(Path(str(artifacts["keyframes_dir"])) / "contact_sheet.jpg")
    return _asset_src(str(artifact), output_dir=output_dir) if artifact else ""


def _render_contact_sheet_detail(src: str) -> str:
    return f"""
      <details>
        <summary>Contact sheet</summary>
        <img class="contact-sheet" src="{_text(src)}" alt="Contact sheet of sampled creative keyframes" loading="lazy">
      </details>
    """


FUNCTION_LABELS = {
    "hook": "Hook",
    "pain": "Pain",
    "proof": "Proof",
    "cta": "CTA",
    "risk": "Risk",
}


def _render_mechanism_filmstrip(
    items: list[dict[str, Any]],
    evidence_by_id: dict[str, dict[str, Any]],
    *,
    output_dir: Path | None,
) -> str:
    if not items:
        return '<p class="muted">No mechanism steps available.</p>'

    cards = []
    for index, item in enumerate(items, start=1):
        evidence_items = [
            evidence_by_id[str(evidence_id)]
            for evidence_id in item.get("evidence_ids", [])
            if str(evidence_id) in evidence_by_id
        ]
        shot = _select_shot(evidence_items)
        time = _text(item.get("time", "Unknown time"))
        mechanism = _text(item.get("mechanism", "beat"))
        function = _narrative_function(item, index=index)
        function_label = _text(FUNCTION_LABELS.get(function, "Proof"))
        note = _text(str(item.get("viewer_perception") or item.get("observation") or ""))
        if shot and shot.get("artifact"):
            src = _asset_src(str(shot["artifact"]), output_dir=output_dir)
            image = f'<img src="{_text(src)}" alt="{time} mechanism step shot" loading="lazy">'
        else:
            image = "No shot"
        cards.append(
            f"""
            <article class="mechanism-card function-{function}">
              <div class="mechanism-shot">{image}</div>
              <div class="mechanism-copy">
                <div class="mechanism-kicker"><span class="function-dot"></span>{function_label}</div>
                <h3>Step {index} / {time}</h3>
                <p class="mechanism-title">{mechanism}</p>
                <p class="mechanism-note">{note}</p>
              </div>
            </article>
            """
        )
    legend = "".join(
        f'<span class="function-chip function-{key}"><span class="function-dot"></span>{label}</span>'
        for key, label in FUNCTION_LABELS.items()
    )
    return (
        f'<div class="function-legend">{legend}</div>'
        + '<div class="mechanism-filmstrip">'
        + "".join(cards)
        + "</div>"
    )


def _narrative_function(item: dict[str, Any], *, index: int) -> str:
    explicit = str(item.get("narrative_function", "")).strip().lower()
    if explicit in FUNCTION_LABELS:
        return explicit

    mechanism_text = str(item.get("mechanism", "")).lower()
    text = " ".join(
        str(item.get(key, "")) for key in ("mechanism", "observation", "viewer_perception")
    ).lower()

    if any(keyword in text for keyword in ("risk", "skeptic", "drop-off", "weakness", "confusion", "reject")):
        return "risk"
    if _has_cta_signal(mechanism_text, text):
        return "cta"
    if any(keyword in mechanism_text for keyword in ("hook", "opening", "attention", "question", "curiosity")):
        return "hook"
    if any(keyword in text for keyword in ("proof", "demo", "product", "packet", "show", "result", "claim", "before-after", "evidence", "taste", "ease")):
        return "proof"
    if any(keyword in text for keyword in ("pain", "friction", "problem", "symptom", "discomfort", "fear", "objection", "tension")):
        return "pain"
    if index == 1 or any(keyword in text for keyword in ("hook", "opening", "first", "attention", "question", "curiosity")):
        return "hook"
    return "proof"


def _has_cta_signal(mechanism_text: str, text: str) -> bool:
    if bool(re.search(r"\bcta\b", text)):
        return True
    if any(
        keyword in mechanism_text
        for keyword in ("urgency", "scarcity", "sale", "offer", "close", "link", "purchase")
    ):
        return True
    return any(
        keyword in text
        for keyword in (
            "call to action",
            "urgency",
            "scarcity",
            "sale",
            "offer",
            "click",
            "buy",
            "purchase",
            "direct link",
            "grab yourself",
        )
    )


def _render_timeline_card(
    item: dict[str, Any],
    evidence_by_id: dict[str, dict[str, Any]],
    *,
    output_dir: Path | None,
    submagic_lesson: str,
    compact: bool = False,
) -> str:
    evidence_ids = [str(value) for value in item.get("evidence_ids", [])]
    evidence_items = [
        evidence_by_id[evidence_id]
        for evidence_id in evidence_ids
        if evidence_id in evidence_by_id
    ]
    shot = _select_shot(evidence_items)
    time = _text(item.get("time", "Unknown time"))
    observation_text = str(item.get("observation", "No observation supplied."))
    perception_text = str(item.get("viewer_perception", ""))
    observation = _text(_truncate(observation_text, 260) if compact else observation_text)
    perception = _text(_truncate(perception_text, 220) if compact else perception_text)
    alt = _text(f"{item.get('time', 'Unknown time')} shot: {item.get('observation', 'No observation supplied.')}")

    if shot and shot.get("artifact"):
        src = _asset_src(str(shot["artifact"]), output_dir=output_dir)
        shot_html = (
            '<div class="phone-frame"><div class="shot">'
            f'<img src="{_text(src)}" alt="{alt}" width="480" height="848" loading="lazy">'
            '</div></div>'
        )
    else:
        shot_html = '<div class="phone-frame"><div class="shot">No shot available for this beat</div></div>'

    evidence_html = (
        f'<p class="muted">{len(evidence_items)} Evidence sources</p>'
        if compact
        else _render_evidence_summary(evidence_ids, evidence_items)
    )
    mechanism_html = (
        ""
        if compact
        else f"""
            <h3>Mechanism</h3>
            <p>{_text(item.get("mechanism", ""))}</p>
        """
    )
    lesson = (
        _compact_lesson(submagic_lesson)
        if compact
        else submagic_lesson or "Translate the mechanism, not the competitor surface."
    )

    return f"""
        <article class="timeline-card">
          {shot_html}
          <div class="timeline-copy">
            <div class="timeline-meta">{time} / {_text(item.get("confidence", "unknown"))} confidence</div>
            <h3>What happens</h3>
            <p>{observation}</p>
            <h3>Why it works</h3>
            <p>{perception}</p>
            {mechanism_html}
            <h3>Submagic lesson</h3>
            <p>{_text(lesson)}</p>
            {evidence_html}
          </div>
        </article>
    """


def _select_shot(evidence_items: list[dict[str, Any]]) -> dict[str, Any] | None:
    for source in ("keyframe", "scene"):
        for item in evidence_items:
            if item.get("source") == source and item.get("artifact"):
                return item
    return None


def _render_belief_shift(shift: dict[str, Any]) -> str:
    return f"""
      <div class="shift">
        {_render_mini_card("Before", shift.get("before"))}
        {_render_mini_card("Bridge", shift.get("bridge"), accent=True)}
        {_render_mini_card("After", shift.get("after"))}
      </div>
    """


def _render_proof_ladder(items: list[dict[str, Any]]) -> str:
    if not items:
        return '<p class="muted">No proof ladder supplied.</p>'
    rows = []
    for index, item in enumerate(items, start=1):
        rows.append(
            f"""
            <tr>
              <td>{index}</td>
              <td>{_text(item.get("claim", ""))}</td>
              <td>{_text(item.get("proof_type", ""))}</td>
              <td>{_text(item.get("weakness", ""))}</td>
              <td>{_render_evidence_details(item.get("evidence_ids", []))}</td>
            </tr>
            """
        )
    return f"""
      <table>
        <thead><tr><th>#</th><th>Claim</th><th>Proof type</th><th>Weakness</th><th>Evidence</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    """


def _render_viewer_states(items: list[dict[str, Any]]) -> str:
    if not items:
        return '<p class="muted">No viewer state timeline supplied.</p>'
    rows = []
    for item in items:
        rows.append(
            f"""
            <tr>
              <td>{_text(item.get("time", ""))}</td>
              <td>{_text(item.get("state", ""))}</td>
              <td>{_text(item.get("trigger", ""))}</td>
              <td>{_render_evidence_details(item.get("evidence_ids", []))}</td>
            </tr>
            """
        )
    return f"""
      <table>
        <thead><tr><th>Time</th><th>Viewer state</th><th>Trigger</th><th>Evidence</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    """


def _rank_scores(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        scores,
        key=lambda item: (int(item.get("score", 0)), str(item.get("dimension", ""))),
    )


def _render_score_row(item: dict[str, Any]) -> str:
    score = int(item.get("score", 0))
    width = max(0, min(100, round((score / 3) * 100)))
    return f"""
      <tr>
        <td><strong>{_text(_titleize(item.get("dimension", "Score")))}</strong><br><span class="muted">{_text(item.get("confidence", "unknown"))} confidence</span></td>
        <td>{score}/3<div class="score-bar"><div class="score-bar-fill" style="width:{width}%"></div></div></td>
        <td>{_text(item.get("improvement_note", ""))}</td>
        <td>{_render_evidence_details(item.get("evidence", []))}</td>
      </tr>
    """


def _render_platform_card(name: str, item: dict[str, Any]) -> str:
    return f"""
      <article class="mini-card">
        <div class="label">{_text(_titleize(name))}</div>
        <h3>{_text(item.get("fit_score", "?"))}/3 fit</h3>
        <p>{_text(item.get("notes", ""))}</p>
      </article>
    """


def _render_score_cards(title: str, items: list[dict[str, Any]]) -> str:
    if not items:
        return _render_mini_card(title, "No score diagnostics supplied.")
    rows = []
    for item in items:
        score = int(item.get("score", 0))
        rows.append(
            f"{_titleize(item.get('dimension', 'Score'))}: {score}/3"
            + (
                f" - {item.get('improvement_note')}"
                if item.get("improvement_note")
                else ""
            )
        )
    return _render_action_list(title, rows)


def _render_intent_card(label: str, value: Any) -> str:
    return (
        '<article class="intent-card">'
        f'<div class="label">{_text(label)}</div>'
        f'<p>{_text(value or "Not supplied.")}</p>'
        "</article>"
    )


def _render_intent_fact(label: str, value: Any) -> str:
    return (
        '<article class="intent-fact">'
        f'<div class="label">{_text(label)}</div>'
        f'<p>{_text(value or "Not supplied.")}</p>'
        "</article>"
    )


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


def _render_mechanism_ladder(formula: str) -> str:
    steps = [step.strip() for step in formula.split("->") if step.strip()]
    if not steps:
        return f'<p class="muted">{_text(formula or "No mechanism formula supplied.")}</p>'
    return (
        '<div class="mechanism-ladder">'
        + "".join(
            f'<div class="mechanism-step"><div class="label">Step {index}</div><p>{_text(step)}</p></div>'
            for index, step in enumerate(steps, start=1)
        )
        + "</div>"
    )


def _render_mini_card(label: str, value: Any, *, accent: bool = False) -> str:
    classes = "mini-card accent" if accent else "mini-card"
    return f'<article class="{classes}"><div class="label">{_text(label)}</div><p>{_text(value or "Not supplied.")}</p></article>'


def _render_evidence_summary(
    evidence_ids: list[str],
    evidence_items: list[dict[str, Any]],
) -> str:
    visible = evidence_ids[:3]
    chips = "".join(f'<span class="chip">{_text(evidence_id)}</span>' for evidence_id in visible)
    source_notes = [
        f'{evidence.get("evidence_id", "")}: {evidence.get("source", "source")} at {evidence.get("timestamp", "")}'
        for evidence in evidence_items
    ]
    return f"""
      <div class="chip-row">{chips}</div>
      <details>
        <summary>Evidence sources</summary>
        {_render_list(source_notes or evidence_ids)}
      </details>
    """


def _render_evidence_details(evidence_ids: list[Any]) -> str:
    return f"""
      <details>
        <summary>{len(evidence_ids)} evidence IDs</summary>
        {_render_list([str(evidence_id) for evidence_id in evidence_ids])}
      </details>
    """


def _render_list(items: list[Any]) -> str:
    if not items:
        return '<p class="muted">None supplied.</p>'
    return "<ul>" + "".join(f"<li>{_text(item)}</li>" for item in items) + "</ul>"


def _sentence_list(items: list[Any]) -> str:
    return " ".join(str(item) for item in items) if items else "Not supplied."


def _compact_lesson(value: str) -> str:
    text = " ".join(str(value).split())
    if not text:
        return "Translate the mechanism, not the competitor surface."
    if len(text) <= 120:
        return text
    return text[:117].rsplit(" ", 1)[0] + "..."


def _truncate(value: str, limit: int) -> str:
    text = " ".join(str(value).split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rsplit(" ", 1)[0] + "..."


def _first_proof_gap(core: dict[str, Any]) -> str:
    proof_ladder = core.get("proof_ladder", [])
    if not proof_ladder:
        return ""
    return str(proof_ladder[0].get("weakness", ""))


def _asset_src(artifact: str, *, output_dir: Path | None) -> str:
    if artifact.startswith(("http://", "https://", "data:")):
        return artifact
    if output_dir is None:
        return artifact
    artifact_path = Path(artifact)
    if not artifact_path.is_absolute():
        artifact_path = Path.cwd() / artifact_path
    return os.path.relpath(artifact_path, output_dir)


def _titleize(value: Any) -> str:
    return str(value).replace("_", " ").strip().title()


def _text(value: Any) -> str:
    return escape(str(value), quote=True)


def _strip_trailing_whitespace(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.splitlines()) + "\n"
