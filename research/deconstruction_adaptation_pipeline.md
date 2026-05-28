# Deconstruction And Adaptation Pipeline

## Goal

Create a repeatable workflow that turns competitor MP4s into evidence packets, deconstruction reports, and Submagic adaptation briefs. V1 builds the workspace and tooling only. It does not generate reports for the existing videos.

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
   - Mark all scores as inferred creative signals unless performance metrics are supplied.

5. Adaptation brainstorming
   - Translate competitor tactics into mechanism cards before scripts.
   - Generate briefs plus scripts for creators/agencies with visible proof scenes.
   - Map each variant to approved Submagic capability labels.
   - Include swappability and copycat checks.

6. Validation
   - Check schema validity.
   - Check evidence IDs resolve.
   - Check no unsupported performance claims.
   - Check copycat/IP risk.
   - Check platform fit and safe-zone considerations.
   - Check generic feature-list ideas fail the taste gate.

7. Synthesis
   - Compare multiple creatives to build a pattern library.
   - Separate repeated mechanisms from one-off stylistic choices.

## Prompt Architecture

- `prompts/core/system.md`: shared rules and evidence discipline.
- `prompts/extraction/evidence_packet.md`: convert raw extraction into normalized evidence.
- `prompts/deconstruction/deconstruct_report.md`: produce timestamped creative diagnosis.
- `prompts/adaptation/submagic_variants.md`: produce Submagic-native briefs and scripts.
- `prompts/validation/judge.md`: block weak evidence, direct copying, and unsupported claims.
- `prompts/synthesis/pattern_library.md`: aggregate cross-video patterns.

## Enforced Artifact Graph

```text
AnalysisRun
  -> EvidenceEvent[]
  -> TimelineVerbalization
  -> MechanismDeconstruction
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

## V1 Command Boundary

V1 commands are allowed to generate metadata, keyframes, OCR, and schema validation results. They must not generate:

- `outputs/*/reports/deconstruct.md`
- `outputs/*/reports/adaptations.md`
- `outputs/aggregate/pattern_library.md`
- any claim that `ad1-ad5` have been fully analyzed

## Sources

- [ffprobe documentation](https://ffmpeg.org/ffprobe.html)
- [PySceneDetect documentation](https://www.scenedetect.com/docs/latest/)
- [Tesseract OCR documentation](https://tesseract-ocr.github.io/)
- [Google Ads: ABCDs of effective video ads](https://support.google.com/google-ads/answer/14783551)
- [TikTok Creative Insights](https://ads.us.tiktok.com/help/article/creative-insights?lang=en)
- [HF Papers: VideoAds](https://hf.co/papers/2504.09282)
- [HF Papers: E-VAds](https://hf.co/papers/2602.08355)
