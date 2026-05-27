# Deconstruction And Adaptation Pipeline

## Goal

Create a repeatable workflow that turns competitor MP4s into evidence packets, deconstruction reports, and Submagic adaptation briefs. V1 builds the workspace and tooling only. It does not generate reports for the existing videos.

## Pipeline

1. Inventory
   - Read MP4 metadata with `ffprobe`.
   - Record filename, duration, resolution, FPS, audio presence, codec, and orientation.

2. Evidence extraction
   - Extract keyframes with `ffmpeg`.
   - OCR sampled frames with `tesseract`.
   - Support future transcript and scene-detection steps through the `uv` toolchain.
   - Write only evidence artifacts under `outputs/<video-id>/evidence/`.

3. Timeline reconstruction
   - Convert raw evidence into timestamped beats: hook, setup, promise, proof, demo, objection, CTA, and end card.
   - Require evidence pointers for every beat.

4. Deconstruction
   - Score creative dimensions from `0` to `3`.
   - Include rationale, timestamp evidence, confidence, and drop-off hypotheses.
   - Mark all scores as inferred creative signals unless performance metrics are supplied.

5. Adaptation brainstorming
   - Translate competitor tactics into Submagic-native mechanisms.
   - Generate briefs plus scripts for creators/agencies.
   - Map each variant to Submagic features.

6. Validation
   - Check schema validity.
   - Check timestamp support.
   - Check no unsupported performance claims.
   - Check copycat/IP risk.
   - Check platform fit and safe-zone considerations.

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

## Quality Gates

- No deconstruction score without at least one evidence pointer.
- No adaptation variant without a Submagic feature mapping.
- No performance claim without metrics.
- No direct copy of competitor script, caption style, branded UI, music, creator identity, or proprietary claims.
- No final report with empty sections, unsupported timestamps, or missing platform fit.

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
