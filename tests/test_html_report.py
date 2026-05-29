import json
from pathlib import Path

from creatives_analysis.html_report import (
    render_deconstruction_html,
    write_deconstruction_html_report,
)


def _sample_deconstruct() -> dict:
    return {
        "video_id": "ad1",
        "creative_signal_only": True,
        "cold_watch": {
            "immediate_felt_reaction": "Editing friction is visible immediately.",
            "moment_of_curiosity": "The opening implies a faster way to make a raw clip usable.",
            "moment_of_confusion_or_boredom": "The proof is not yet visible enough.",
            "most_memorable_image": "Raw footage becoming a polished captioned short.",
        },
        "evidence_timeline": [
            {
                "time": "0.0-3.0",
                "observation": "Creator points at a raw timeline before captions appear.",
                "viewer_perception": "The viewer recognizes repetitive editing labor.",
                "mechanism": "workflow compression",
                "narrative_function": "hook",
                "evidence_ids": [
                    "ev_keyframe_001",
                    "ev_ocr_001",
                    "ev_scene_001",
                    "ev_audio_001",
                ],
                "confidence": "high",
            }
        ],
        "core_mechanism": {
            "name": "workflow compression",
            "why_it_catches_attention": "It starts with a familiar editing bottleneck.",
            "why_it_might_persuade": "It promises visible reduction in manual work.",
            "what_cannot_be_copied": "Competitor wording, visual identity, or exact proof scene.",
        },
        "creative_intent": {
            "creative_label": "Raw Clip Workflow Compression Ad",
            "creative_type": "UGC / creator workflow demo / direct response",
            "likely_hypothesis": (
                "If creators see raw footage become publishable quickly, they will "
                "believe the tool can remove repetitive editing work."
            ),
            "target_audience": "Short-form creators and agencies with recurring editing bottlenecks.",
            "awareness_stage": "Problem-aware to solution-aware.",
            "funnel_stage": "Cold prospecting with conversion intent.",
            "likely_kpi": "Click-through, sign-up starts, trial activation, and CAC/ROAS.",
            "offer_strategy": (
                "Turn an annoying workflow into visible speed proof before asking "
                "for the click."
            ),
            "marketer_job_to_be_done": (
                "Make the product feel like an output multiplier, not another editing app."
            ),
            "evidence_ids": ["ev_keyframe_001", "ev_ocr_001"],
            "confidence": "medium",
            "unknowns": ["No media-buy data or landing-page analytics are available."],
        },
        "distilled_core": {
            "core_thesis": (
                "The creative turns a familiar editing bottleneck into a visible "
                "before-after promise that makes speed feel believable."
            ),
            "mechanism_formula": (
                "raw-work pain -> visible transformation -> workflow compression -> "
                "action prompt"
            ),
            "belief_shift_summary": (
                "The viewer moves from 'this clip still needs too much work' to "
                "'this can become publishable with a faster editing system.'"
            ),
            "why_it_works": (
                "It anchors the promise in a concrete workflow pain before asking "
                "the viewer to believe the product claim."
            ),
            "where_it_breaks": (
                "The proof weakens if the finished edited output is not shown "
                "clearly enough before the viewer loses patience."
            ),
            "submagic_transfer": (
                "Show raw footage becoming a captioned, cut, zoomed, publishable "
                "short inside the first few seconds."
            ),
            "steal": [
                "Open on a creator pain that is already emotionally expensive.",
                "Make the transformation visual before explaining features.",
            ],
            "avoid": [
                "Do not copy competitor wording, visuals, claims, creator likeness, or music.",
                "Do not let feature lists replace visible before-after proof.",
            ],
            "test_next": [
                "Test a first-three-seconds before-after edit reveal against a pain-only hook."
            ],
        },
        "core_understanding": {
            "human_truth": "Creators know raw clips can be valuable but feel trapped by repetitive editing work.",
            "belief_shift": {
                "before": "A raw clip still needs too much manual editing.",
                "after": "The same clip can become publishable quickly.",
                "bridge": "Visible captions, cuts, zooms, and B-roll compress the workflow.",
            },
            "tension_stack": [
                "The viewer wants output volume without losing quality.",
                "The viewer distrusts generic AI editor claims without seeing proof.",
            ],
            "proof_ladder": [
                {
                    "claim": "Manual editing work can be compressed.",
                    "proof_type": "before-after workflow scene",
                    "evidence_ids": ["ev_keyframe_001", "ev_ocr_001"],
                    "weakness": "The proof needs a clearer finished-video frame.",
                }
            ],
            "viewer_state_timeline": [
                {
                    "time": "0.0-3.0",
                    "state": "recognition",
                    "trigger": "The creator points at a raw editing timeline.",
                    "evidence_ids": ["ev_keyframe_001"],
                }
            ],
            "skeptic_read": "A skeptical creator may reject the claim if the finished edit is not shown.",
            "transfer_principle_for_submagic": "Turn invisible editing labor into a visible before-after workflow compression demo.",
            "counterfactuals": [
                "Showing the final edited clip in the first three seconds would make the promise more concrete."
            ],
        },
        "scores": [
            {
                "dimension": "hook_strength",
                "score": 2,
                "evidence": ["ev_keyframe_001"],
                "confidence": "high",
                "improvement_note": "Make the product proof visible in the first beat.",
            }
        ],
        "platform_fit": {
            "tiktok": {"fit_score": 2, "notes": "Needs native first-frame proof."},
            "reels": {"fit_score": 2, "notes": "Needs safe-zone caption review."},
            "shorts": {"fit_score": 2, "notes": "Needs proof before midpoint."},
            "meta_paid": {"fit_score": 2, "notes": "Needs earlier product visibility."},
            "linkedin": {"fit_score": 1, "notes": "Needs clearer agency framing."},
        },
        "drop_off_hypotheses": ["CTA appears after the likely midpoint retention drop."],
        "risks_and_unknowns": ["No performance metrics are available."],
    }


def _sample_evidence() -> dict:
    return {
        "video_id": "ad1",
        "source_video": "creatives/ad1.mp4",
        "analysis_run": {
            "run_id": "run_sample",
            "source_sha256": "a" * 64,
            "extractor": "creatives-extract",
            "schema_version": "evidence_packet.v2",
        },
        "manifest": {
            "filename": "ad1.mp4",
            "path": "creatives/ad1.mp4",
            "duration_seconds": 26.9,
            "size_bytes": 4338977,
            "width": 480,
            "height": 848,
            "fps": 30,
            "video_codec": "h264",
            "audio_codec": "aac",
            "has_audio": True,
            "orientation": "vertical",
        },
        "timeline_evidence": [
            {
                "evidence_id": "ev_keyframe_001",
                "timestamp": "0.0",
                "source": "keyframe",
                "observation": "Creator points at a raw timeline before captions appear.",
                "confidence": "high",
                "artifact": "outputs/ad1/evidence/keyframes/frame_001_0.000s.jpg",
            },
            {
                "evidence_id": "ev_ocr_001",
                "timestamp": "0.0",
                "source": "ocr",
                "observation": "OCR text: Raw clip takes hours.",
                "confidence": "medium",
                "artifact": "outputs/ad1/evidence/ocr.json",
            },
            {
                "evidence_id": "ev_scene_001",
                "timestamp": "0.0-3.0",
                "source": "scene",
                "observation": "Manual scene note for the opening workflow proof.",
                "confidence": "medium",
                "artifact": "outputs/ad1/evidence/manual_frames/opening.jpg",
            },
            {
                "evidence_id": "ev_audio_001",
                "timestamp": "0.0-3.0",
                "source": "audio",
                "observation": "Audio note describes editing pain.",
                "confidence": "low",
            }
        ],
        "artifacts": {
            "manifest": "outputs/ad1/evidence/manifest.json",
            "keyframe_001": "outputs/ad1/evidence/keyframes/frame_001_0.000s.jpg",
            "contact_sheet": "outputs/ad1/evidence/keyframes/contact_sheet.jpg",
        },
        "reports_generated": [],
    }


def test_render_deconstruction_html_pairs_timeline_text_with_shot() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert html.lower().startswith("<!doctype html>")
    assert "Raw Clip Workflow Compression Ad" in html
    assert "workflow compression" in html
    assert "Creator points at a raw timeline before captions appear." in html
    assert "outputs/ad1/evidence/keyframes/frame_001_0.000s.jpg" in html
    assert 'alt="0.0-3.0 shot: Creator points at a raw timeline before captions appear."' in html
    assert "ev_keyframe_001" in html
    assert "<pre" not in html.lower()


def test_render_deconstruction_html_surfaces_core_understanding_and_submagic_brand() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert "Core Read" in html
    assert "Human truth" in html
    assert "Belief shift" in html
    assert "Proof ladder" in html
    assert "Submagic transfer" in html
    assert "contact_sheet.jpg" in html
    assert "#FF4F01" in html
    assert "#D8FF3E" not in html
    assert "#8B5CF6" not in html
    assert "<details" in html
    assert html.count('class="chip"') < 8


def test_render_deconstruction_html_has_distilled_first_order_sections() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert "Core thesis" in html
    assert "Creative mechanism" in html
    assert "What to steal" in html
    assert "What not to copy" in html
    assert "Test next" in html
    assert "Full evidence timeline" in html
    assert "Full score matrix" in html


def test_render_deconstruction_html_surfaces_creative_intent_before_core_read() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert "Raw Clip Workflow Compression Ad" in html
    assert "Why this creative exists" in html
    assert "Hypothesis" in html
    assert "Audience" in html
    assert "Funnel" in html
    assert "Likely KPI" in html
    assert html.index("Why this creative exists") < html.index("Core Read")


def test_render_deconstruction_html_prioritizes_diagnostics_before_key_shots() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert "Top diagnostics" in html
    assert "Key shots" in html
    assert "Creative mechanism" in html
    assert html.index("Top diagnostics") < html.index("Key shots")


def test_render_deconstruction_html_unifies_filmstrip_and_mechanism() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert "Creative filmstrip" not in html
    assert html.count("<h2>Creative mechanism</h2>") == 1
    assert 'class="mechanism-filmstrip"' in html
    assert 'class="mechanism-card function-hook"' in html
    assert 'class="mechanism-ladder"' not in html


def test_render_deconstruction_html_hides_evidence_ids_outside_details() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())
    before_first_details = html.split("<details", 1)[0]

    assert "ev_keyframe_001" not in before_first_details
    assert "ev_ocr_001" not in before_first_details
    assert "Evidence sources" in html


def test_render_deconstruction_html_uses_compact_key_shots_not_full_timeline_first() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert "Key shots" in html
    assert "Full evidence timeline" in html
    assert html.index("Key shots") < html.index("Full evidence timeline")


def test_render_deconstruction_html_hides_key_shots_inside_details() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert "<summary>Key shots</summary>" in html
    assert "<h2>Key shots</h2>" not in html
    assert html.index("<summary>Key shots</summary>") > html.index("<h2>Details</h2>")


def test_render_deconstruction_html_uses_tighter_layout_spacing() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert "padding: 18px 16px 44px" in html
    assert "padding: 24px 18px 22px" in html
    assert "height: 220px" in html
    assert "min-height: 0" in html


def test_render_deconstruction_html_uses_minimal_header() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())
    hero_html = html.split("</section>", 1)[0]

    assert 'class="hero-context"' not in html
    assert 'class="metric-strip"' not in html
    assert "key shots" not in hero_html
    assert "strengths" not in hero_html
    assert "weaknesses" not in hero_html
    assert "transfer principle" not in hero_html


def test_render_deconstruction_html_uses_compact_core_read_cards() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert 'class="core-read"' in html
    assert 'class="core-thesis"' not in html
    assert 'class="thesis-card"' not in html
    assert ".core-thesis" not in html
    assert ".thesis-card" not in html


def test_render_deconstruction_html_uses_compact_intent_facts() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert 'class="intent-facts"' in html
    assert 'class="intent-stack"' not in html


def test_render_deconstruction_html_keeps_mechanism_annotation_below_shot() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert html.index('class="mechanism-shot"') < html.index('class="mechanism-copy"')
    assert "grid-template-rows: auto auto" in html
    assert "grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))" in html
    assert ".mechanism-shot {\n      height: 220px;" in html
    assert "overflow: hidden;\n      flex: 0 0 auto" in html
    assert "border-top: 1px solid var(--line)" in html
    assert "background: var(--paper)" in html


def test_render_deconstruction_html_keeps_long_mechanism_notes_readable() -> None:
    deconstruct = json.loads(json.dumps(_sample_deconstruct()))
    long_perception = (
        "The viewer is shown a concrete selection layer: the AI appears to find "
        "promising clips inside a larger content library instead of asking the "
        "creator to hunt manually."
    )
    deconstruct["evidence_timeline"][0]["viewer_perception"] = long_perception

    html = render_deconstruction_html(deconstruct, _sample_evidence())
    mechanism_section = html.split("<h2>Creative mechanism</h2>", 1)[1].split(
        "<h2>Core Read</h2>", 1
    )[0]

    assert "instead of asking the creator to hunt manually." in mechanism_section
    assert "..." not in mechanism_section


def test_render_deconstruction_html_color_codes_narrative_functions() -> None:
    deconstruct = json.loads(json.dumps(_sample_deconstruct()))
    deconstruct["evidence_timeline"] = [
        {
            "time": "0.0-1.0",
            "observation": "Opening symptom question.",
            "viewer_perception": "This is immediately relevant.",
            "mechanism": "symptom-led hook",
            "evidence_ids": ["ev_keyframe_001"],
            "confidence": "high",
        },
        {
            "time": "1.0-3.0",
            "observation": "Skipped routine creates discomfort.",
            "viewer_perception": "The viewer feels the pain.",
            "mechanism": "habit pain",
            "evidence_ids": ["ev_keyframe_001"],
            "confidence": "medium",
        },
        {
            "time": "3.0-5.0",
            "observation": "Packet proof is shown.",
            "viewer_perception": "The claim gets a concrete object.",
            "mechanism": "packet proof",
            "evidence_ids": ["ev_keyframe_001"],
            "confidence": "medium",
        },
        {
            "time": "5.0-7.0",
            "observation": "Sale is mentioned.",
            "viewer_perception": "There is a reason to act now.",
            "mechanism": "urgency CTA",
            "evidence_ids": ["ev_keyframe_001"],
            "confidence": "medium",
        },
        {
            "time": "7.0-8.0",
            "observation": "The proof gap could create skepticism.",
            "viewer_perception": "The viewer may not believe the claim.",
            "mechanism": "skeptic risk",
            "evidence_ids": ["ev_keyframe_001"],
            "confidence": "low",
        },
    ]

    html = render_deconstruction_html(deconstruct, _sample_evidence())

    assert 'class="mechanism-card function-hook"' in html
    assert 'class="mechanism-card function-pain"' in html
    assert 'class="mechanism-card function-proof"' in html
    assert 'class="mechanism-card function-cta"' in html
    assert 'class="mechanism-card function-risk"' in html


def test_render_deconstruction_html_fallback_classifier_avoids_substring_mislabels() -> None:
    deconstruct = json.loads(json.dumps(_sample_deconstruct()))
    deconstruct["evidence_timeline"] = [
        {
            "time": "0.0-1.0",
            "observation": "Product label is shown as a bundled answer.",
            "viewer_perception": "The product label acts as a proof cue.",
            "mechanism": "bundle proof pivot",
            "evidence_ids": ["ev_keyframe_001"],
            "confidence": "medium",
        },
        {
            "time": "1.0-2.0",
            "observation": "The creator holds the packet close to camera while promising taste, ease, and family acceptance.",
            "viewer_perception": "The viewer sees the product as easier to use.",
            "mechanism": "friction reducer",
            "evidence_ids": ["ev_keyframe_001"],
            "confidence": "medium",
        },
    ]

    html = render_deconstruction_html(deconstruct, _sample_evidence())

    assert html.count('class="mechanism-card function-proof"') == 2
    assert 'class="mechanism-card function-cta"' not in html


def test_render_deconstruction_html_keeps_submagic_light_orange_direction() -> None:
    html = render_deconstruction_html(_sample_deconstruct(), _sample_evidence())

    assert "#FF4F01" in html
    assert "#FFFCF7" in html
    assert "#D8FF3E" not in html
    assert "#8B5CF6" not in html
    assert "dark neon" not in html.lower()


def test_write_deconstruction_html_report_writes_readable_html(tmp_path: Path) -> None:
    deconstruct_path = tmp_path / "deconstruct.json"
    evidence_path = tmp_path / "evidence.json"
    output_path = tmp_path / "ad1_report.html"
    deconstruct_path.write_text(json.dumps(_sample_deconstruct()))
    evidence_path.write_text(json.dumps(_sample_evidence()))

    written = write_deconstruction_html_report(
        deconstruct_path=deconstruct_path,
        evidence_path=evidence_path,
        output_path=output_path,
    )

    assert written == output_path
    assert output_path.exists()
    assert "Evidence timeline" in output_path.read_text()
