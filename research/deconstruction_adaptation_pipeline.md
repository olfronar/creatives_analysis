# Deconstruction And Adaptation Pipeline

## Goal

Create a repeatable workflow that turns competitor MP4s into evidence packets, deconstruction reports, human-readable HTML reports, and Submagic adaptation briefs. V1 builds the workspace and tooling only. It does not generate reports for the existing videos unless an analysis task is explicitly requested.

## Pipeline

1. Evidence manifest
   - Read MP4 metadata with `ffprobe`.
   - Record filename, duration, resolution, FPS, audio presence, codec, orientation, source hash, run ID, extractor, and schema version.

2. Evidence extraction
   - Extract dense first-3-second frames before uniform sampling.
   - OCR sampled frames with timestamped evidence IDs.
   - Support transcript, scene, and audio-event steps through the `uv` toolchain.
   - Write only evidence artifacts under `outputs/<video-id>/evidence/`.
   - Generated evidence packets must validate against `schemas/evidence_packet.schema.json`.

3. Timeline verbalization
   - Convert raw evidence into observation-only sensory timeline.
   - Add viewer-state hypotheses separately from observations.
   - Require evidence IDs for every beat.

4. Mechanism deconstruction
   - Score creative dimensions from `0` to `3`.
   - Include cold watch, evidence timeline, core mechanism, platform fit, confidence, risks, and drop-off hypotheses.
   - Include core understanding: human truth, belief shift, tension stack, proof ladder, viewer-state timeline, skeptic read, Submagic transfer principle, and counterfactuals.
   - Mark all scores as inferred creative signals unless performance metrics are supplied.

5. HTML report rendering
   - Render only after the deconstruct JSON validates and evidence IDs resolve.
   - Consume the deconstruct JSON plus evidence packet.
   - Use keyframe or scene artifacts to pair shots with timeline interpretations.
   - Use the contact sheet when available to show the whole creative arc before detailed reading.
   - Surface the core-understanding layer above the timeline.
   - Follow the Submagic-inspired light/orange report kit.
   - Keep HTML deterministic: no model-authored HTML, no raw JSON dump, no new claims.
   - Write human-readable reports under an explicit output path, usually `outputs/<video-id>/reports/deconstruct.html`.

6. Adaptation brainstorming
   - Translate competitor tactics into mechanism cards before scripts.
   - Generate briefs plus scripts for creators/agencies with visible proof scenes.
   - Map each variant to approved Submagic capability labels.
   - Include swappability and copycat checks.

7. Validation
   - Check schema validity.
   - Check evidence IDs resolve.
   - Check no unsupported performance claims.
   - Check copycat/IP risk.
   - Check platform fit and safe-zone considerations.
   - Check generic feature-list ideas fail the taste gate.
   - Check HTML report readability when a deconstruct report is rendered.

8. Synthesis
   - Compare multiple creatives to build a pattern library.
   - Separate repeated mechanisms from one-off stylistic choices.

## Prompt Architecture

- `prompts/core/system.md`: shared rules and evidence discipline.
- `prompts/extraction/evidence_packet.md`: convert raw extraction into normalized evidence.
- `prompts/deconstruction/deconstruct_report.md`: produce timestamped creative diagnosis.
- `prompts/reporting/html_deconstruction_report.md`: define the deterministic HTML report contract.
- `prompts/adaptation/submagic_variants.md`: produce Submagic-native briefs and scripts.
- `prompts/validation/judge.md`: block weak evidence, direct copying, and unsupported claims.
- `prompts/synthesis/pattern_library.md`: aggregate cross-video patterns.

## Enforced Artifact Graph

```text
AnalysisRun
  -> EvidenceEvent[]
  -> TimelineVerbalization
  -> MechanismDeconstruction
  -> HtmlDeconstructionReport
  -> SubmagicAdaptationVariant[]
  -> ValidationResult
```

The critical rule is that later artifacts cite earlier artifact IDs. A deconstruction score cites evidence IDs. An adaptation variant cites mechanism/evidence lineage. A validator rejects claims whose lineage cannot be resolved.

## Quality Gates

- No deconstruction score without at least one evidence pointer.
- No adaptation variant without a Submagic feature mapping.
- No performance claim without metrics.
- No direct copy of competitor script, caption style, branded UI, music, creator identity, or proprietary claims.
- No final report with empty sections, unsupported timestamps, or missing platform fit.
- No generic variant that could be rebranded as another AI editor without changing the proof scene.
- No prompt output that skips observation -> viewer perception -> mechanism before recommendation.
- No deconstruction that skips mechanism -> human truth -> belief shift -> Submagic transfer.
- No HTML report that hides evidence IDs, confidence, risk notes, or missing-shot states.
- No HTML report generated from invalid deconstruct JSON.

## V1 Command Boundary

V1 commands are allowed to generate metadata, keyframes, OCR, schema validation results, and HTML reports only when a deconstruct JSON already exists. They must not generate:

- `outputs/*/reports/deconstruct.md`
- `outputs/*/reports/adaptations.md`
- `outputs/aggregate/pattern_library.md`
- any claim that `ad1-ad5` have been fully analyzed

## HTML Report Construction

Best place: after deconstruction validation and before adaptation brainstorming. This gives the human and Codex a shared review surface for the creative mechanism before any Submagic variants are generated.

Best time: immediately after a single `deconstruct` task produces a valid JSON report. The report should be regenerated whenever the deconstruct JSON or evidence packet changes.

Implementation rule: the HTML renderer is a deterministic formatter. It can resolve evidence IDs, choose a supporting shot, compute relative asset paths, escape text, and apply Submagic-inspired styling. It cannot create new analysis.

Current command:

```bash
uv run creatives-render-report --deconstruct <deconstruct.json> --evidence <evidence_packet.json> --output <report.html>
```

## Sources

- [ffprobe documentation](https://ffmpeg.org/ffprobe.html)
- [PySceneDetect documentation](https://www.scenedetect.com/docs/latest/)
- [Tesseract OCR documentation](https://tesseract-ocr.github.io/)
- [Google Ads: ABCDs of effective video ads](https://support.google.com/google-ads/answer/14783551)
- [TikTok Creative Insights](https://ads.us.tiktok.com/help/article/creative-insights?lang=en)
- [Submagic AI video editor](https://www.submagic.co/ai-video-editor)
- [Submagic API introduction](https://docs.submagic.co/introduction)
- [Nielsen Norman Group visual design principles](https://media.nngroup.com/media/articles/attachments/Principles_Visual_Design-A4.pdf)
- [W3C WAI alt decision tree](https://www.w3.org/WAI/tutorials/images/decision-tree/)
- [HF Papers: VideoAds](https://hf.co/papers/2504.09282)
- [HF Papers: E-VAds](https://hf.co/papers/2602.08355)
